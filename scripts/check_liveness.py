#!/usr/bin/env python3
"""Prefetch the Verifier's mechanical liveness facts so the agent stops re-fetching them.

Why this exists
---------------
`VERIFIER_AGENT.md` asks the agent to resolve every entry's install target against
the GitHub / npm / PyPI / OSV APIs by WebFetch, per page, every run. Measured, that
work is ~96% confirmation that nothing changed: the 2026-07-29 pass reported 24 of
25 pages clean and 1 fix. Those lookups are deterministic HTTP with a stable
contract, so they belong in auditable Python — exactly like the smoke runner, whose
docstring already states the principle: *the decision of what runs is auditable
Python, not an LLM judgment.*

This script runs in the `verify` job before the agent and writes:

  .verify/liveness.json  — full per-page detail, plus a deduped `repos` map
  .verify/liveness.md    — a short digest the workflow injects into the prompt

It answers "did anything change since this page was last verified?" The agent is
then left with the parts a registry genuinely cannot answer: confirming a launch
command against a primary source, reading a manifest for risky patterns, and
judging whether a provenance mismatch or a new advisory actually matters.

**Shadow mode.** As shipped, `VERIFIER_AGENT.md` is unchanged and still tells the
agent to verify normally; the digest is injected as supplementary context only.
Run it that way for a few cycles and diff these verdicts against the agent's before
anything is allowed to depend on them.

What is reused, not reinvented
------------------------------
Install-command parsing is imported from `select_smoke_targets` (`INSTALL_PATTERNS`,
`MCP_BOOT`, `boot_for`, `section_block`, `gate_blocked`, `parse_frontmatter`,
`SMOKE_TYPES`). A second copy of those regexes would drift from the ones that decide
what may be executed, so `tests/test_check_liveness.py` asserts this module resolves
a page to the same install command the smoke selector does.

Token safety
------------
This step holds `github.token`, and every URL it builds derives from an LLM-authored
page. Three rules, all enforced in `Fetcher`:

  1. The `Authorization` header is attached only when the request host is exactly
     `api.github.com`, checked at request time.
  2. A redirect to a different host drops the header (same-host 3xx is kept — a repo
     rename is useful signal and is recorded as `renamed_from`).
  3. `api.github.com` URLs are built from *validated* `org`/`repo`/`path` components
     via `urllib.parse.quote`, never from a page's literal URL string. Page-supplied
     endpoint probes get no headers at all and are not followed.

Never fails the run
-------------------
Every network path is wrapped: a timeout, 5xx, malformed JSON, or blown wall-clock
budget yields `verdict: "error"` and `needs_model: true` for the affected pages, and
the script still exits 0. A page whose facts could not be established must reach the
model, never be treated as clean.

stdlib only. Run:
  python3 scripts/check_liveness.py --worklist .verify/worklist.json \
      --smoke .verify/smoke-results.json \
      --out .verify/liveness.json --digest .verify/liveness.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import select_smoke_targets as smoke  # noqa: E402  (first cross-script import in scripts/)

REPO = Path(__file__).resolve().parent.parent

GITHUB_API = "https://api.github.com"
PYPI_API = "https://pypi.org/pypi/{name}/json"
NPM_API = "https://registry.npmjs.org/{name}"
OSV_API = "https://api.osv.dev/v1/query"

USER_AGENT = "sci-ai-enabler-verifier/1 (+https://github.com/scripps-ai-enablement/sci-ai-enabler)"
TIMEOUT = 10
RETRIES = 1
RATE_FLOOR = 50          # stop optional GitHub calls below this many remaining
RATE_HARD_FLOOR = 5      # stop GitHub calls entirely below this
STALE_DAYS = 365         # "unmaintained" signal

# ---------------------------------------------------------------------------
# Target extraction — pure, no network. Every capture is SHAPE-VALIDATED before
# it is used to build a URL. The catalog contains real prose false positives
# (`npx skills add CLI`, `npx skills add https`, bare `npx skills add`), so a
# regex capture is a candidate, never a target.
# ---------------------------------------------------------------------------
SEGMENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
RESERVED = {".", "..", ".git", ".github"}

# This catalog's own repo. Pages link to it constantly (Sources rows, relative
# links rendered absolute, the smoke-test methodology page), so an indiscriminate
# "first github.com URL on the page" fallback resolves 24 of 459 pages to the
# catalog itself and then cheerfully reports the catalog as their install target.
# The Verifier agent caught exactly this in the first shadow-mode run. Excluded
# everywhere: a page's install target is never this repository.
SELF_REPO = "scripps-ai-enablement/sci-ai-enabler"

GIT_CLONE_RE = re.compile(r"git clone\s+(?:--[\w-]+\s+)*https://github\.com/([^\s/]+/[^\s/]+?)(?:\.git)?(?:\s|$)")
CP_DIR_RE = re.compile(r"^\s*cp\s+-r\s+([A-Za-z0-9][A-Za-z0-9._/-]*)\s", re.M)
NPX_SKILLS_RE = re.compile(r"npx skills add\s+([A-Za-z0-9][A-Za-z0-9._/-]*)")
PLUGIN_MARKET_RE = re.compile(r"/plugin marketplace add\s+([A-Za-z0-9][A-Za-z0-9._/-]*)")
SUPPLIER_LINK_RE = re.compile(r"\*\*Supplier\*\*\s*\|[^|]*?\((https://github\.com/[^)\s]+)\)")
GITHUB_URL_RE = re.compile(r"https://github\.com/([A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*)")

PKG_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def valid_repo(slug: str) -> str | None:
    """Return a normalized `org/repo`, or None when the capture isn't one.

    Rejects the prose false positives that a bare regex happily matches.
    """
    if not slug:
        return None
    slug = slug.strip().rstrip("/")
    if slug.endswith(".git"):
        slug = slug[:-4]
    parts = slug.split("/")
    if len(parts) != 2:
        return None
    org, repo = parts
    if org.lower() in RESERVED or repo.lower() in RESERVED:
        return None
    if not SEGMENT_RE.match(org) or not SEGMENT_RE.match(repo):
        return None
    slug = f"{org}/{repo}"
    if slug.casefold() == SELF_REPO.casefold():
        return None
    return slug


def valid_path(p: str) -> str | None:
    """Validate a repo-relative subdirectory path segment by segment."""
    if not p:
        return None
    p = p.strip().strip("/")
    if not p:
        return None
    segs = p.split("/")
    if any(s.lower() in RESERVED or not SEGMENT_RE.match(s) for s in segs):
        return None
    return "/".join(segs)


def _pkg_from_install(cmd: str, kind: str) -> str | None:
    """Pull a package name out of a validated install command."""
    toks = cmd.split()
    if kind == "pip" and len(toks) >= 3:
        name = toks[2]
    elif kind in ("uv", "uvx"):
        name = toks[-1]
    elif kind == "npx":
        name = toks[-1]
    else:
        return None
    name = re.split(r"[=<>!\[]", name)[0]
    # Scoped npm names (@scope/pkg) are legal and must survive validation.
    if name.startswith("@") and name.count("/") == 1:
        scope, _, rest = name.partition("/")
        if SEGMENT_RE.match(scope[1:]) and PKG_NAME_RE.match(rest):
            return name
        return None
    return name if PKG_NAME_RE.match(name) else None


def extract_targets(text: str) -> list[dict]:
    """Every checkable target on a page, deduped, in priority order.

    Pure: no network, no filesystem. Returns dicts of
    {kind, repo?, path?, name?, ecosystem?, url?, cmd?}.
    """
    out: list[dict] = []
    seen: set[tuple] = set()

    def add(t: dict) -> None:
        # Normalize before deduping: different extraction paths build dicts that
        # differ only by an absent key vs an explicit None (e.g. `git clone` yields
        # {kind, repo, path: None} while the marketplace path yields {kind, repo}),
        # which otherwise slips the same target through twice and shows up as a
        # repeated line in the digest.
        t = {k: v for k, v in t.items() if v is not None}
        key = (t.get("kind"), t.get("repo"), t.get("path"), t.get("name"), t.get("url"))
        if key not in seen:
            seen.add(key)
            out.append(t)

    install = smoke.section_block(text, "How to install") or text

    # 1. Package installs, using the smoke selector's own patterns.
    for pattern, kind in smoke.INSTALL_PATTERNS:
        m = pattern.search(install)
        if not m:
            continue
        cmd = m.group(1).strip()
        if kind == "npx-skills":
            slug = NPX_SKILLS_RE.search(cmd)
            repo = valid_repo("/".join(slug.group(1).split("/")[:2])) if slug else None
            if repo:
                sub = valid_path("/".join(slug.group(1).split("/")[2:])) if slug else None
                add({"kind": "github-dir" if sub else "github-repo",
                     "repo": repo, "path": sub, "cmd": cmd})
            continue
        name = _pkg_from_install(cmd, kind)
        if name:
            eco = "npm" if kind == "npx" else "PyPI"
            add({"kind": "npm" if eco == "npm" else "pypi",
                 "name": name, "ecosystem": eco, "cmd": cmd})

    # 2. `git clone` + the `cp -r <repo>/<subdir>` that follows it. 371 pages.
    for m in GIT_CLONE_RE.finditer(install):
        repo = valid_repo(m.group(1))
        if not repo:
            continue
        sub = None
        for c in CP_DIR_RE.finditer(install[m.end():]):
            cand = c.group(1)
            head, _, rest = cand.partition("/")
            if head == repo.split("/")[1]:
                sub = valid_path(rest)
                break
        add({"kind": "github-dir" if sub else "github-repo", "repo": repo, "path": sub})

    # 3. `npx skills add <org>/<repo>[/path]` anywhere on the page.
    for m in NPX_SKILLS_RE.finditer(install):
        segs = m.group(1).split("/")
        repo = valid_repo("/".join(segs[:2]))
        if repo:
            sub = valid_path("/".join(segs[2:]))
            add({"kind": "github-dir" if sub else "github-repo", "repo": repo, "path": sub})

    # 4. Plugin marketplace.
    for m in PLUGIN_MARKET_RE.finditer(install):
        repo = valid_repo(m.group(1))
        if repo:
            add({"kind": "github-repo", "repo": repo})

    # 5. Supplier table link, then any GitHub URL, as fallbacks.
    if not any(t["kind"].startswith("github") for t in out):
        m = SUPPLIER_LINK_RE.search(text)
        if m:
            u = urllib.parse.urlsplit(m.group(1))
            repo = valid_repo("/".join(u.path.strip("/").split("/")[:2]))
            if repo:
                add({"kind": "github-repo", "repo": repo})
    if not any(t["kind"].startswith("github") for t in out):
        # Last resort: the `## Sources` section only. A whole-page search is not
        # safe -- pages reference this catalog repo in prose and relative links, so
        # an unscoped "first github.com URL" resolves the page's install target to
        # the catalog itself. A page with genuinely no repo (an Anthropic-hosted
        # Connector, say) SHOULD yield no github target: `no-target-extracted`
        # routes it to the model, which is the honest outcome.
        for m in GITHUB_URL_RE.finditer(smoke.section_block(text, "Sources")):
            repo = valid_repo(m.group(1))
            if repo:
                add({"kind": "github-repo", "repo": repo})
                break

    # 6. Remote MCP endpoints. Status code only, never a verdict.
    for m in re.finditer(r"https://[A-Za-z0-9.-]+/(?:sse|mcp)\b[^\s`)\]]*", text):
        add({"kind": "endpoint", "url": m.group(0)})

    return out


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
class _NoAuthOnCrossHostRedirect(urllib.request.HTTPRedirectHandler):
    """Strip Authorization when a redirect leaves the original host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is None:
            return None
        if urllib.parse.urlsplit(newurl).hostname != urllib.parse.urlsplit(req.full_url).hostname:
            for h in list(new.headers):
                if h.lower() == "authorization":
                    del new.headers[h]
            new.unredirected_hdrs.pop("Authorization", None)
        return new


class Fetcher:
    """Small JSON/HEAD client. The one place credentials and hosts are decided."""

    def __init__(self, token: str | None = None, budget_seconds: float = 240.0,
                 opener=None, retry_sleep: float = 2.0):
        self.token = token or None
        self.retry_sleep = retry_sleep
        self.deadline = time.monotonic() + budget_seconds
        self.gh_remaining: int | None = None
        self.degraded = False
        self.calls = 0
        self._opener = opener or urllib.request.build_opener(_NoAuthOnCrossHostRedirect())

    # -- policy -----------------------------------------------------------
    def out_of_budget(self) -> bool:
        return time.monotonic() >= self.deadline

    def gh_allowed(self, optional: bool = False) -> bool:
        if self.out_of_budget():
            return False
        if self.gh_remaining is None:
            return True
        if self.gh_remaining < RATE_HARD_FLOOR:
            return False
        if optional and self.gh_remaining < RATE_FLOOR:
            return False
        return True

    def gh_url(self, *segments: str, **query: str) -> str:
        """Build an api.github.com URL from validated components only."""
        path = "/".join(urllib.parse.quote(s, safe="") for s in segments)
        url = f"{GITHUB_API}/{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)
        return url

    # -- transport --------------------------------------------------------
    def _request(self, url: str, method: str = "GET", data: bytes | None = None):
        host = urllib.parse.urlsplit(url).hostname
        req = urllib.request.Request(url, method=method, data=data)
        req.add_header("User-Agent", USER_AGENT)
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        # RULE 1: the token goes to api.github.com and nowhere else, decided here,
        # at request time, from the URL actually being fetched.
        if self.token and host == "api.github.com":
            req.add_header("Authorization", f"Bearer {self.token}")
            req.add_header("X-GitHub-Api-Version", "2022-11-28")
        self.calls += 1
        return self._opener.open(req, timeout=TIMEOUT)

    def json(self, url: str, data: dict | None = None) -> tuple[int, dict | list | None]:
        """(status, parsed) — status 0 means the request never completed."""
        body = json.dumps(data).encode() if data is not None else None
        for attempt in range(RETRIES + 1):
            if self.out_of_budget():
                return 0, None
            try:
                with self._request(url, "POST" if body else "GET", body) as r:
                    self._note_rate(r)
                    raw = r.read()
                    try:
                        return r.status, json.loads(raw) if raw else None
                    except (ValueError, TypeError):
                        return r.status, None
            except urllib.error.HTTPError as e:
                self._note_rate(e)
                if e.code >= 500 and attempt < RETRIES:
                    time.sleep(self.retry_sleep)
                    continue
                return e.code, None
            except Exception:
                if attempt < RETRIES:
                    time.sleep(self.retry_sleep)
                    continue
                return 0, None
        return 0, None

    def status(self, url: str) -> int:
        """Status code for a page-supplied URL. No headers, no redirects followed."""
        u = urllib.parse.urlsplit(url)
        if u.scheme != "https" or not u.hostname:
            return 0
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(url, method=method)
                req.add_header("User-Agent", USER_AGENT)
                self.calls += 1
                opener = urllib.request.build_opener(_NoRedirect())
                with opener.open(req, timeout=TIMEOUT) as r:
                    return r.status
            except urllib.error.HTTPError as e:
                return e.code
            except Exception:
                continue
        return 0

    def _note_rate(self, resp) -> None:
        try:
            v = resp.headers.get("X-RateLimit-Remaining")
            if v is not None:
                self.gh_remaining = int(v)
                if self.gh_remaining < RATE_FLOOR:
                    self.degraded = True
        except (ValueError, AttributeError):
            pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


# ---------------------------------------------------------------------------
# Per-kind lookups
# ---------------------------------------------------------------------------
def _iso_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def fetch_repo(f: Fetcher, slug: str) -> dict:
    """One `/repos/{org}/{repo}` call. Deduped by the caller — 119 distinct repos
    back 459 pages, and the top 8 cover most of them."""
    org, repo = slug.split("/")
    if not f.gh_allowed():
        return {"status": 0, "skipped": "budget"}
    st, body = f.json(f.gh_url("repos", org, repo))
    if st != 200 or not isinstance(body, dict):
        return {"status": st}
    full = body.get("full_name") or slug
    lic = (body.get("license") or {}).get("spdx_id")
    return {
        "status": st,
        "exists": True,
        "archived": bool(body.get("archived")),
        "disabled": bool(body.get("disabled")),
        "owner": (body.get("owner") or {}).get("login"),
        "renamed_from": slug if full.lower() != slug.lower() else None,
        "full_name": full,
        "license_spdx": None if lic in (None, "NOASSERTION") else lic,
        "license_raw": lic,
        "pushed_at": body.get("pushed_at"),
        "stars": body.get("stargazers_count"),
        "open_issues": body.get("open_issues_count"),
        "default_branch": body.get("default_branch"),
    }


def fetch_dir_listing(f: Fetcher, slug: str, parent: str) -> dict:
    """One `contents/<parent>` call covers every slug under it — a single call to
    `.../contents/skills` answers `dir-missing` for ~140 catalog pages."""
    org, repo = slug.split("/")
    if not f.gh_allowed(optional=True):
        return {"status": 0, "skipped": "budget", "names": []}
    segs = ["repos", org, repo, "contents"] + parent.split("/") if parent else ["repos", org, repo, "contents"]
    st, body = f.json(f.gh_url(*segs))
    names = [e.get("name") for e in body] if st == 200 and isinstance(body, list) else []
    return {"status": st, "names": [n for n in names if n]}


def fetch_path_last_commit(f: Fetcher, slug: str, path: str) -> str | None:
    """Last commit touching `path`. This is the delta signal the whole design rests on.

    Repo-level `pushed_at` is useless here: `K-Dense-AI/scientific-agent-skills`
    backs ~140 pages and is pushed almost daily, so a repo-level comparison would
    mark all 140 changed every run and erase the entire saving.
    """
    org, repo = slug.split("/")
    if not f.gh_allowed(optional=True):
        return None
    st, body = f.json(f.gh_url("repos", org, repo, "commits", path=path, per_page="1"))
    if st == 200 and isinstance(body, list) and body:
        return ((body[0].get("commit") or {}).get("committer") or {}).get("date")
    return None


def fetch_pypi(f: Fetcher, name: str) -> dict:
    """Compact PyPI facts. The `releases` map is discarded deliberately — it runs to
    hundreds of KB on a mature package and is one of the largest silent token sinks
    in the current design, since the agent WebFetches this JSON raw."""
    st, body = f.json(PYPI_API.format(name=urllib.parse.quote(name, safe="")))
    if st != 200 or not isinstance(body, dict):
        return {"status": st}
    info = body.get("info") or {}
    lic = info.get("license_expression") or info.get("license") or None
    if not lic:
        for c in info.get("classifiers") or []:
            if c.startswith("License ::"):
                lic = c.split("::")[-1].strip()
                break
    urls = body.get("urls") or []
    return {
        "status": st,
        "version": info.get("version"),
        "license": (lic or "").strip() or None,
        "yanked": bool(urls and all(u.get("yanked") for u in urls)),
        "last_release": (urls[0].get("upload_time_iso_8601") if urls else None),
    }


def fetch_npm(f: Fetcher, name: str) -> dict:
    st, body = f.json(NPM_API.format(name=urllib.parse.quote(name, safe="@/")))
    if st != 200 or not isinstance(body, dict):
        return {"status": st}
    latest = ((body.get("dist-tags") or {}).get("latest"))
    ver = (body.get("versions") or {}).get(latest) or {}
    return {
        "status": st,
        "latest": latest,
        "license": ver.get("license"),
        "deprecated": bool(ver.get("deprecated")),
        "last_publish": (body.get("time") or {}).get(latest),
    }


def fetch_osv(f: Fetcher, name: str, ecosystem: str) -> list[dict]:
    """Advisories for a package. Skipped for github-dir targets by the caller: OSV
    has no coverage for a skills monorepo, so querying is a wasted call rather than
    a null result."""
    st, body = f.json(OSV_API, data={"package": {"name": name, "ecosystem": ecosystem}})
    if st != 200 or not isinstance(body, dict):
        return []
    out = []
    for v in (body.get("vulns") or [])[:5]:
        out.append({"id": v.get("id"), "summary": (v.get("summary") or "")[:160]})
    return out


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def _smoke_index(smoke_results: dict) -> dict:
    idx = {}
    for r in (smoke_results or {}).get("results", []):
        slug = r.get("slug") or r.get("name")
        if slug:
            idx[slug] = r.get("status")
    return idx


def check(batch: list[dict], smoke_results: dict, f: Fetcher, today: str) -> dict:
    smoke_status = _smoke_index(smoke_results)
    repos: dict[str, dict] = {}
    listings: dict[tuple[str, str], dict] = {}
    pages: list[dict] = []

    for row in batch:
        path = REPO / row["path"]
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            pages.append({**_page_stub(row), "verdict": "error",
                          "flags": ["page-unreadable"], "needs_model": True})
            continue
        fm = smoke.parse_frontmatter(text)
        targets = extract_targets(text)
        page = _page_stub(row)
        page.update({
            "tool_type": fm.get("tool_type", ""),
            "supplier": fm.get("supplier", ""),
            "security": fm.get("security", ""),
            "smoke_eligible": fm.get("tool_type") in smoke.SMOKE_TYPES
                              and not smoke.gate_blocked(text),
            "smoke_status": smoke_status.get(row["slug"]),
            "launch_cmd": smoke.boot_for(text),
        })
        flags: list[str] = []
        resolved: list[dict] = []
        changed = False

        if not targets:
            flags.append("no-target-extracted")

        for t in targets:
            r = dict(t)
            if t["kind"] in ("github-repo", "github-dir"):
                slug = t["repo"]
                if slug not in repos:
                    repos[slug] = fetch_repo(f, slug)
                info = repos[slug]
                r["status"] = info.get("status", 0)
                if info.get("skipped"):
                    flags.append("fetch-error")
                elif info.get("status") == 404:
                    flags.append("repo-404")
                elif not info.get("exists"):
                    flags.append("fetch-error")
                else:
                    if info.get("archived"):
                        flags.append("repo-archived")
                    if info.get("renamed_from"):
                        flags.append("repo-renamed")
                    if not info.get("license_spdx"):
                        flags.append("license-missing")
                    pushed = _iso_date(info.get("pushed_at"))
                    if pushed and (date.fromisoformat(today) - pushed).days > STALE_DAYS:
                        flags.append("stale-12mo")
                    if t["kind"] == "github-dir" and t.get("path"):
                        parent = "/".join(t["path"].split("/")[:-1])
                        leaf = t["path"].split("/")[-1]
                        key = (slug, parent)
                        if key not in listings:
                            listings[key] = fetch_dir_listing(f, slug, parent)
                        if listings[key].get("names") and leaf not in listings[key]["names"]:
                            flags.append("dir-missing")
                        last = fetch_path_last_commit(f, slug, t["path"])
                        r["last_commit"] = last
                        d = _iso_date(last)
                        vo = row.get("verified_on") or ""
                        try:
                            if d and vo and d >= date.fromisoformat(vo):
                                changed = True   # equal dates count as changed
                        except ValueError:
                            changed = True
                r["resolved"] = bool(info.get("exists"))
            elif t["kind"] == "pypi":
                info = fetch_pypi(f, t["name"])
                r.update(info)
                if info.get("status") == 404:
                    flags.append("pkg-404")
                elif info.get("status") != 200:
                    flags.append("fetch-error")
                else:
                    if info.get("yanked"):
                        flags.append("pkg-yanked")
                    if not info.get("license"):
                        flags.append("license-missing")
                    for a in fetch_osv(f, t["name"], "PyPI"):
                        flags.append("osv-advisory")
                        r.setdefault("advisories", []).append(a)
                r["resolved"] = info.get("status") == 200
            elif t["kind"] == "npm":
                info = fetch_npm(f, t["name"])
                r.update(info)
                if info.get("status") == 404:
                    flags.append("pkg-404")
                elif info.get("status") != 200:
                    flags.append("fetch-error")
                else:
                    if info.get("deprecated"):
                        flags.append("pkg-yanked")
                    if not info.get("license"):
                        flags.append("license-missing")
                    for a in fetch_osv(f, t["name"], "npm"):
                        flags.append("osv-advisory")
                        r.setdefault("advisories", []).append(a)
                r["resolved"] = info.get("status") == 200
            elif t["kind"] == "endpoint":
                st = f.status(t["url"])
                r["status"] = st
                # Status only, never a verdict: a live MCP server answers 406 to a
                # browser-shaped request (see catalog/verifier-state.md).
                if st == 404 or st == 0:
                    flags.append("endpoint-non-2xx")
                r["resolved"] = st != 0
            resolved.append(r)

        if page["smoke_status"] == "boot_error":
            flags.append("smoke-boot-error")
        elif page["smoke_status"] == "install_error":
            flags.append("smoke-install-error")
        if changed:
            flags.append("changed-since-verified")

        # Provenance: exact/casefold owner-vs-supplier match clears; anything else
        # is for the model (a mismatch is often legitimate — supplier "NeuroClaw"
        # vs owner "CUHK-AIM-Group").
        owner = next((repos[t["repo"]].get("owner") for t in targets
                      if t["kind"].startswith("github") and t.get("repo") in repos), None)
        page["owner"] = owner
        page["provenance_match"] = bool(
            owner and page["supplier"]
            and owner.casefold().replace("-", "") == page["supplier"].casefold().replace("-", "").replace(" ", "")
        )

        if f.degraded:
            # A low global rate-limit budget is NOT the same as this page's fetch
            # failing: its own targets may all have resolved. Flag it distinctly so
            # the digest can say why the page reached the model, and so `verdict`
            # still reflects what was actually learned about the page.
            flags.append("budget-degraded")

        page["targets"] = resolved
        page["flags"] = sorted(set(flags))
        page["changed_since_verified"] = changed
        clean_grade = row.get("verification") == "works" and page["security"] == "cleared"
        launch_unconfirmed = bool(page["launch_cmd"]) and page["smoke_status"] != "pass"
        page["verdict"] = ("error" if any(x in page["flags"]
                                          for x in ("fetch-error", "page-unreadable"))
                           else "changed" if changed
                           else "unresolved" if "no-target-extracted" in page["flags"]
                           else "clean" if not page["flags"] else "changed")
        page["needs_model"] = bool(
            page["flags"] or not clean_grade or launch_unconfirmed or f.degraded
        )
        page["reason"] = ("; ".join(page["flags"]) if page["flags"]
                          else "grade is not works+cleared" if not clean_grade
                          else "launch command not confirmed by execution" if launch_unconfirmed
                          else "")
        pages.append(page)

    needs = sum(1 for p in pages if p["needs_model"])
    return {
        "schema": "liveness-v1",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "today": today,
        "budget": {"github_calls": f.calls, "github_remaining": f.gh_remaining,
                   "degraded": f.degraded, "out_of_budget": f.out_of_budget()},
        "repos": repos,
        "pages": pages,
        "summary": {"pages": len(pages), "clean": len(pages) - needs,
                    "needs_model": needs, "distinct_repos": len(repos)},
    }


def _page_stub(row: dict) -> dict:
    return {
        "path": row["path"], "slug": row["slug"],
        "verification": row.get("verification", ""),
        "verified_on": row.get("verified_on", ""),
        "targets": [], "flags": [], "needs_model": True, "verdict": "error",
        "reason": "",
    }


def render_digest(result: dict) -> str:
    s = result["summary"]
    clean = [p for p in result["pages"] if not p["needs_model"]]
    need = [p for p in result["pages"] if p["needs_model"]]
    out = [f"## Liveness prefetch ({s['pages']} pages, {s['distinct_repos']} repos)", ""]
    if result["budget"]["degraded"]:
        out += ["> The prefetch was rate-limited or ran out of budget, so some facts are "
                "incomplete. Every affected page is listed below for you to check "
                "directly — do not treat any page as clean on the strength of this run.", ""]
    if clean:
        out += [f"{len(clean)} page(s) resolved clean: every install target still exists, "
                "nothing has changed since the page's last verification, a license is "
                "present, no OSV advisory matches, and provenance matches the supplier.",
                ""]
        out += ["<details><summary>clean slugs</summary>", "",
                ", ".join(f"`{p['slug']}`" for p in clean), "", "</details>", ""]
    out += [f"### Needs your adjudication ({len(need)})", ""]
    if not need:
        out += ["_Nothing._", ""]
    for p in need:
        bits = []
        for t in p["targets"]:
            if t["kind"].startswith("github"):
                bits.append(f"repo `{t.get('repo')}`" + (f" path `{t['path']}`" if t.get("path") else "")
                            + f" -> {t.get('status')}")
            elif t["kind"] in ("pypi", "npm"):
                bits.append(f"{t['kind']} `{t.get('name')}` {t.get('version') or t.get('latest') or ''}"
                            f" ({t.get('license') or 'no license'}) -> {t.get('status')}")
            elif t["kind"] == "endpoint":
                bits.append(f"endpoint <{t.get('url')}> -> {t.get('status')}")
        out.append(f"- [ ] `{p['path']}` — {p['verification'] or 'unstamped'}"
                   f" · {p['verified_on'] or 'no date'}"
                   + (f" · flags: {', '.join(p['flags'])}" if p["flags"] else ""))
        if bits:
            out.append(f"      {'; '.join(bits)}")
        if p.get("launch_cmd"):
            out.append(f"      launch: `{p['launch_cmd']}` · smoke: {p.get('smoke_status') or 'not run'}")
        if p["reason"]:
            out.append(f"      why you: {p['reason']}")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--worklist", type=Path, required=True, help="worklist JSON from select_verify_targets.py")
    ap.add_argument("--smoke", type=Path, default=None, help="smoke-results.json")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--digest", type=Path, default=None)
    ap.add_argument("--budget-seconds", type=float, default=240.0)
    ap.add_argument("--today", default=None)
    args = ap.parse_args()

    today = args.today or date.today().isoformat()
    try:
        wl = json.loads(args.worklist.read_text(encoding="utf-8"))
        batch = wl.get("batch", [])
    except Exception as e:  # noqa: BLE001 — must never fail the run
        print(f"note: could not read {args.worklist}: {e}", file=sys.stderr)
        batch = []
    smoke_results = {}
    if args.smoke and args.smoke.exists():
        try:
            smoke_results = json.loads(args.smoke.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass

    f = Fetcher(token=os.environ.get("GH_API_TOKEN"), budget_seconds=args.budget_seconds)
    result = check(batch, smoke_results, f, today)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.digest:
        args.digest.write_text(render_digest(result), encoding="utf-8")
    s = result["summary"]
    print(f"liveness: {s['pages']} pages, {s['clean']} clean, {s['needs_model']} need the model, "
          f"{f.calls} HTTP calls, github_remaining={f.gh_remaining}")
    gho = os.environ.get("GITHUB_OUTPUT")
    if gho:
        with open(gho, "a", encoding="utf-8") as fh:
            fh.write(f"clean_count={s['clean']}\nneeds_model_count={s['needs_model']}\n")
    return 0  # never fail the run


if __name__ == "__main__":
    raise SystemExit(main())
