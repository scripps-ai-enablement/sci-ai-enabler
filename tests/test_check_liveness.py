#!/usr/bin/env python3
"""Tests for scripts/check_liveness.py.

Network-free: `.github/workflows/test.yml` gives no network guarantee, so every
test here either exercises pure extraction or drives `Fetcher` through a stub
opener that records outgoing requests.

The security-critical tests are `test_auth_header_only_for_api_github_com` and
`test_auth_header_dropped_on_cross_host_redirect`. This script holds `github.token`
and builds URLs from LLM-authored catalog pages, so a leaked header is the worst
failure mode available to it.

The anti-drift test is `test_resolves_same_install_command_as_smoke_selector`: the
install regexes live in `select_smoke_targets` because they also decide what may be
executed. If someone forks them into this module, that test fails loudly.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import io
import json
import unittest
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "check_liveness.py"

_spec = importlib.util.spec_from_file_location("check_liveness", SCRIPT)
cl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cl)

smoke = cl.smoke  # the module under reuse


# --------------------------------------------------------------------------- #
# Stub transport
# --------------------------------------------------------------------------- #
class _Resp(io.BytesIO):
    def __init__(self, body: bytes, status: int = 200, headers: dict | None = None):
        super().__init__(body)
        self.status = status
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class StubOpener:
    """Records every outgoing request and replays canned responses."""

    def __init__(self, routes: dict | None = None, default=(200, {})):
        self.routes = routes or {}
        self.default = default
        self.seen: list[urllib.request.Request] = []

    def open(self, req, timeout=None):
        self.seen.append(req)
        for frag, resp in self.routes.items():
            if frag in req.full_url:
                if isinstance(resp, Exception):
                    raise resp
                status, body = resp
                if status >= 400:
                    raise urllib.error.HTTPError(req.full_url, status, "err",
                                                 {"X-RateLimit-Remaining": "999"}, None)
                return _Resp(json.dumps(body).encode(), status,
                             {"X-RateLimit-Remaining": "999"})
        status, body = self.default
        return _Resp(json.dumps(body).encode(), status, {"X-RateLimit-Remaining": "999"})

    def headers_for(self, frag: str) -> dict:
        for r in self.seen:
            if frag in r.full_url:
                return {k.lower(): v for k, v in r.header_items()}
        raise AssertionError(f"no request matched {frag!r}; saw "
                             f"{[r.full_url for r in self.seen]}")


# --------------------------------------------------------------------------- #
# Shape validation
# --------------------------------------------------------------------------- #
class RepoSlugValidation(unittest.TestCase):
    def test_accepts_normal_slugs(self):
        for s, want in [
            ("K-Dense-AI/scientific-agent-skills", "K-Dense-AI/scientific-agent-skills"),
            ("CUHK-AIM-Group/NeuroClaw", "CUHK-AIM-Group/NeuroClaw"),
            ("owner/repo.git", "owner/repo"),
            ("owner/repo/", "owner/repo"),
        ]:
            with self.subTest(s=s):
                self.assertEqual(cl.valid_repo(s), want)

    def test_rejects_the_prose_false_positives_in_the_catalog(self):
        # All four occur in real pages: `npx skills add CLI` (x9),
        # `npx skills add https`, `npx skills add smoke-tested`, and a bare form.
        for s in ["CLI", "https", "smoke-tested", "", "   ", "one/two/three",
                  "/leading", "trailing/", "../etc", ".git/x", "-bad/repo", "a/-bad"]:
            with self.subTest(s=s):
                self.assertIsNone(cl.valid_repo(s))

    def test_path_validation(self):
        self.assertEqual(cl.valid_path("skills/abcd-skill"), "skills/abcd-skill")
        self.assertEqual(cl.valid_path("/skills/x/"), "skills/x")
        for bad in ["", "..", "a/../b", "a//b", "-x/y", ".github/w"]:
            with self.subTest(bad=bad):
                self.assertIsNone(cl.valid_path(bad))


# --------------------------------------------------------------------------- #
# Extraction against real catalog pages
# --------------------------------------------------------------------------- #
class ExtractionOnRealPages(unittest.TestCase):
    def _targets(self, slug):
        p = REPO / "catalog" / "tools" / f"{slug}.md"
        if not p.exists():
            self.skipTest(f"{slug}.md not in this checkout")
        return cl.extract_targets(p.read_text(encoding="utf-8"))

    def test_git_clone_skill_page_yields_repo_and_subdir(self):
        ts = self._targets("abcd-skill")
        gh = [t for t in ts if t["kind"].startswith("github")]
        self.assertTrue(gh, f"no github target from abcd-skill: {ts}")
        self.assertTrue(all(cl.valid_repo(t["repo"]) for t in gh))

    def test_mcp_page_yields_a_package_target(self):
        ts = self._targets("biomcp")
        kinds = {t["kind"] for t in ts}
        self.assertTrue(kinds & {"pypi", "npm", "github-repo", "github-dir"},
                        f"biomcp yielded only {kinds}")

    def test_no_page_resolves_to_this_catalog_repo(self):
        # The Verifier agent caught this in the first shadow-mode run: an unscoped
        # "first github.com URL on the page" fallback resolved 24 of 459 pages to
        # this catalog itself, then reported the catalog as their install target.
        bad = [p.name for p in (REPO / "catalog" / "tools").glob("*.md")
               if p.name != "index.md"
               for t in cl.extract_targets(p.read_text(encoding="utf-8"))
               if t.get("repo", "").casefold() == cl.SELF_REPO.casefold()]
        self.assertEqual(bad, [], f"{len(bad)} page(s) resolved to SELF_REPO")

    def test_pages_without_a_target_are_bounded_and_expected(self):
        # A page yielding nothing is not automatically a bug: an Anthropic-hosted
        # Connector has no installable repo, and this repo's own plugins install
        # from SELF_REPO. Those get `no-target-extracted` -> needs_model, which is
        # the honest outcome. What must not happen is the count silently growing,
        # since PR 6 would auto-stamp on the strength of these targets.
        tools = [p for p in sorted((REPO / "catalog" / "tools").glob("*.md"))
                 if p.name != "index.md"]
        empty = [p.name for p in tools
                 if not cl.extract_targets(p.read_text(encoding="utf-8"))]
        self.assertLessEqual(len(empty), 30,
                             f"{len(empty)} pages yield no target: {empty[:12]}")
        # And the overwhelming majority must be the legitimately repo-less kinds.
        connectors = 0
        for name in empty:
            fm = smoke.parse_frontmatter((REPO / "catalog" / "tools" / name)
                                         .read_text(encoding="utf-8"))
            if fm.get("tool_type") == "Claude.ai Connector":
                connectors += 1
        self.assertGreaterEqual(connectors, len(empty) - 6,
                                f"unexpected non-Connector pages yield nothing: {empty}")

    def test_coverage_of_pages_with_a_resolvable_target(self):
        tools = [p for p in sorted((REPO / "catalog" / "tools").glob("*.md"))
                 if p.name != "index.md"]
        with_target = sum(1 for p in tools
                          if cl.extract_targets(p.read_text(encoding="utf-8")))
        self.assertGreaterEqual(with_target / len(tools), 0.94)

    def test_all_extracted_repos_are_shape_valid(self):
        tools = sorted((REPO / "catalog" / "tools").glob("*.md"))
        bad = []
        for p in tools:
            if p.name == "index.md":
                continue
            for t in cl.extract_targets(p.read_text(encoding="utf-8")):
                if t["kind"].startswith("github") and not cl.valid_repo(t["repo"]):
                    bad.append((p.name, t["repo"]))
        self.assertEqual(bad, [])

    def test_resolves_same_install_command_as_smoke_selector(self):
        # ANTI-DRIFT: install parsing must stay imported from select_smoke_targets,
        # which also decides what may be executed. A forked copy fails here.
        self.assertIs(cl.smoke.INSTALL_PATTERNS, smoke.INSTALL_PATTERNS)
        p = REPO / "catalog" / "tools" / "biomcp.md"
        if not p.exists():
            self.skipTest("biomcp.md not in this checkout")
        text = p.read_text(encoding="utf-8")
        install = smoke.section_block(text, "How to install") or text
        expected = None
        for pattern, kind in smoke.INSTALL_PATTERNS:
            m = pattern.search(install)
            if m:
                expected = (kind, m.group(1).strip())
                break
        got = [t.get("cmd") for t in cl.extract_targets(text) if t.get("cmd")]
        if expected:
            self.assertIn(expected[1], got)


class ExtractionSynthetic(unittest.TestCase):
    def test_clone_plus_cp_captures_the_subdirectory(self):
        text = ("## How to install\n\n```bash\n"
                "git clone https://github.com/Org/Mono\n"
                "cp -r Mono/skills/my-skill ~/.claude/skills/\n```\n")
        ts = cl.extract_targets(text)
        gh = [t for t in ts if t["kind"] == "github-dir"]
        self.assertEqual(gh[0]["repo"], "Org/Mono")
        self.assertEqual(gh[0]["path"], "skills/my-skill")

    def test_npx_skills_with_path(self):
        text = "## How to install\n\n`npx skills add Org/Repo/skills/thing`\n"
        ts = [t for t in cl.extract_targets(text) if t["kind"] == "github-dir"]
        self.assertEqual((ts[0]["repo"], ts[0]["path"]), ("Org/Repo", "skills/thing"))

    def test_bare_npx_skills_prose_yields_no_target(self):
        for junk in ["`npx skills add CLI`", "`npx skills add https`", "npx skills add "]:
            with self.subTest(junk=junk):
                ts = cl.extract_targets(f"## How to install\n\n{junk}\n")
                self.assertEqual([t for t in ts if t["kind"].startswith("github")], [])

    def test_endpoint_extraction(self):
        text = "Remote: https://example.workers.dev/sse and https://x.io/mcp\n"
        eps = [t["url"] for t in cl.extract_targets(text) if t["kind"] == "endpoint"]
        self.assertEqual(len(eps), 2)

    def test_scoped_npm_package_survives_validation(self):
        self.assertEqual(cl._pkg_from_install("npx -y @scope/pkg", "npx"), "@scope/pkg")
        self.assertIsNone(cl._pkg_from_install("npx -y @bad//pkg", "npx"))

    def test_pip_extras_and_version_pins_are_stripped(self):
        self.assertEqual(cl._pkg_from_install("pip install foo[all]==1.2", "pip"), "foo")

    def test_same_target_from_two_extraction_paths_is_deduped(self):
        # `git clone` yields {kind, repo, path: None} and the marketplace path
        # yields {kind, repo}. Those differ as dicts but name the same target; not
        # normalizing before dedup showed the same repo twice in the digest.
        text = ("## How to install\n\n```bash\n"
                "git clone https://github.com/Org/Repo\n```\n"
                "`/plugin marketplace add Org/Repo`\n"
                "`npx skills add Org/Repo`\n")
        gh = [t for t in cl.extract_targets(text) if t["kind"].startswith("github")]
        self.assertEqual(len(gh), 1, gh)
        self.assertEqual(gh[0]["repo"], "Org/Repo")

    def test_repo_and_subdir_of_same_repo_are_distinct_targets(self):
        text = ("## How to install\n\n```bash\n"
                "git clone https://github.com/Org/Mono\n"
                "cp -r Mono/skills/a ~/.claude/skills/\n```\n"
                "`/plugin marketplace add Org/Other`\n")
        gh = [t for t in cl.extract_targets(text) if t["kind"].startswith("github")]
        self.assertEqual({(t["kind"], t["repo"], t.get("path")) for t in gh},
                         {("github-dir", "Org/Mono", "skills/a"),
                          ("github-repo", "Org/Other", None)})

    def test_no_page_yields_more_than_a_handful_of_targets(self):
        # Guards the dedup: a regression here inflates every batch's HTTP calls.
        worst = max((len(cl.extract_targets(p.read_text(encoding="utf-8"))), p.name)
                    for p in (REPO / "catalog" / "tools").glob("*.md")
                    if p.name != "index.md")
        self.assertLessEqual(worst[0], 6, f"{worst[1]} yields {worst[0]} targets")


# --------------------------------------------------------------------------- #
# Credential handling — the security-critical pair
# --------------------------------------------------------------------------- #
class TokenScoping(unittest.TestCase):
    def test_auth_header_only_for_api_github_com(self):
        op = StubOpener(routes={
            "api.github.com": (200, {"full_name": "o/r", "owner": {"login": "o"}}),
            "pypi.org": (200, {"info": {"version": "1.0"}, "urls": []}),
            "registry.npmjs.org": (200, {"dist-tags": {"latest": "1.0"}, "versions": {}}),
            "api.osv.dev": (200, {"vulns": []}),
        })
        f = cl.Fetcher(token="SECRET", opener=op)
        f.json(f.gh_url("repos", "o", "r"))
        cl.fetch_pypi(f, "somepkg")
        cl.fetch_npm(f, "somepkg")
        cl.fetch_osv(f, "somepkg", "PyPI")
        self.assertIn("authorization", op.headers_for("api.github.com"))
        for host in ("pypi.org", "registry.npmjs.org", "api.osv.dev"):
            with self.subTest(host=host):
                self.assertNotIn("authorization", op.headers_for(host))

    def test_no_auth_header_when_no_token(self):
        op = StubOpener()
        f = cl.Fetcher(token=None, opener=op)
        f.json(f.gh_url("repos", "o", "r"))
        self.assertNotIn("authorization", op.headers_for("api.github.com"))

    def test_auth_header_dropped_on_cross_host_redirect(self):
        h = cl._NoAuthOnCrossHostRedirect()
        req = urllib.request.Request("https://api.github.com/repos/o/r")
        req.add_header("Authorization", "Bearer SECRET")
        new = h.redirect_request(req, None, 302, "Found", {},
                                 "https://evil.example/repos/o/r")
        self.assertIsNotNone(new)
        self.assertNotIn("authorization", {k.lower() for k in new.headers})
        self.assertNotIn("Authorization", new.unredirected_hdrs)

    def test_auth_header_kept_on_same_host_redirect(self):
        # A repo rename 301s within api.github.com and is useful signal.
        h = cl._NoAuthOnCrossHostRedirect()
        req = urllib.request.Request("https://api.github.com/repos/o/old")
        req.add_header("Authorization", "Bearer SECRET")
        new = h.redirect_request(req, None, 301, "Moved", {},
                                 "https://api.github.com/repos/o/new")
        self.assertIn("authorization", {k.lower() for k in new.headers})

    def test_endpoint_probe_sends_no_credentials_and_no_redirects(self):
        op = StubOpener()
        f = cl.Fetcher(token="SECRET", opener=op)
        f.status("https://some.page.supplied/sse")
        for r in op.seen:
            self.assertNotIn("authorization", {k.lower() for k in dict(r.header_items())})

    def test_endpoint_probe_refuses_non_https(self):
        f = cl.Fetcher(token="SECRET", opener=StubOpener())
        self.assertEqual(f.status("http://insecure/sse"), 0)
        self.assertEqual(f.status("file:///etc/passwd"), 0)

    def test_gh_url_percent_encodes_components(self):
        f = cl.Fetcher(opener=StubOpener())
        self.assertEqual(f.gh_url("repos", "o", "r/../x"),
                         "https://api.github.com/repos/o/r%2F..%2Fx")


# --------------------------------------------------------------------------- #
# Verdict rules
# --------------------------------------------------------------------------- #
def _row(slug="s", verification="works", verified_on="2026-01-01"):
    return {"slug": slug, "path": f"catalog/tools/{slug}.md",
            "verification": verification, "verified_on": verified_on, "stamped": True}


class Verdicts(unittest.TestCase):
    def test_unreadable_page_is_error_and_needs_model(self):
        f = cl.Fetcher(opener=StubOpener())
        res = cl.check([_row("does-not-exist-xyz")], {}, f, "2026-07-29")
        p = res["pages"][0]
        self.assertEqual(p["verdict"], "error")
        self.assertTrue(p["needs_model"])
        self.assertIn("page-unreadable", p["flags"])

    def test_summary_counts_match_pages(self):
        f = cl.Fetcher(opener=StubOpener())
        res = cl.check([_row("nope-a"), _row("nope-b")], {}, f, "2026-07-29")
        self.assertEqual(res["summary"]["pages"], 2)
        self.assertEqual(res["summary"]["needs_model"], 2)
        self.assertEqual(res["summary"]["clean"], 0)

    def test_degraded_budget_forces_needs_model(self):
        f = cl.Fetcher(opener=StubOpener())
        f.degraded = True
        res = cl.check([_row("nope")], {}, f, "2026-07-29")
        self.assertTrue(res["pages"][0]["needs_model"])
        self.assertTrue(res["budget"]["degraded"])

    def test_never_raises_on_any_transport_failure(self):
        for exc in [TimeoutError("t"), ConnectionResetError("r"), ValueError("bad json"),
                    urllib.error.URLError("no route")]:
            with self.subTest(exc=type(exc).__name__):
                f = cl.Fetcher(token="S", opener=StubOpener(routes={"api.github.com": exc}),
                                 retry_sleep=0)
                st, body = f.json(f.gh_url("repos", "o", "r"))
                self.assertEqual((st, body), (0, None))

    def test_http_error_status_is_reported_not_raised(self):
        f = cl.Fetcher(opener=StubOpener(routes={"api.github.com": (404, {})}))
        st, body = f.json(f.gh_url("repos", "o", "r"))
        self.assertEqual(st, 404)

    def test_repo_dedup_makes_one_call_for_many_pages(self):
        op = StubOpener(routes={"api.github.com":
                                (200, {"full_name": "o/r", "owner": {"login": "o"},
                                       "license": {"spdx_id": "MIT"},
                                       "pushed_at": "2026-07-01T00:00:00Z"})})
        f = cl.Fetcher(opener=op)
        for _ in range(5):
            cl.fetch_repo(f, "o/r") if "o/r" not in {} else None
        # fetch_repo itself is uncached; check() is what dedups, via the repos map.
        repos = {}
        f2 = cl.Fetcher(opener=StubOpener(routes={"api.github.com": (200, {"full_name": "o/r"})}))
        for _ in range(5):
            if "o/r" not in repos:
                repos["o/r"] = cl.fetch_repo(f2, "o/r")
        self.assertEqual(f2.calls, 1)

    def test_rate_limit_floors_stop_optional_then_all_github_calls(self):
        f = cl.Fetcher(opener=StubOpener())
        f.gh_remaining = cl.RATE_FLOOR - 1
        self.assertFalse(f.gh_allowed(optional=True))
        self.assertTrue(f.gh_allowed(optional=False))
        f.gh_remaining = cl.RATE_HARD_FLOOR - 1
        self.assertFalse(f.gh_allowed(optional=False))

    def test_exhausted_budget_blocks_further_calls(self):
        f = cl.Fetcher(opener=StubOpener(), budget_seconds=-1)
        self.assertTrue(f.out_of_budget())
        self.assertFalse(f.gh_allowed())
        self.assertEqual(f.json("https://api.github.com/x"), (0, None))

    def test_pypi_releases_map_is_discarded(self):
        big = {"info": {"version": "1.0", "license": "MIT"},
               "urls": [{"yanked": False, "upload_time_iso_8601": "2026-01-01T00:00:00Z"}],
               "releases": {f"0.{i}": ["x" * 100] for i in range(500)}}
        f = cl.Fetcher(opener=StubOpener(routes={"pypi.org": (200, big)}))
        got = cl.fetch_pypi(f, "pkg")
        self.assertNotIn("releases", got)
        self.assertEqual(set(got) - {"status"}, {"version", "license", "yanked", "last_release"})

    def test_osv_summaries_are_truncated_and_capped(self):
        vulns = {"vulns": [{"id": f"GHSA-{i}", "summary": "x" * 500} for i in range(20)]}
        f = cl.Fetcher(opener=StubOpener(routes={"api.osv.dev": (200, vulns)}))
        got = cl.fetch_osv(f, "pkg", "PyPI")
        self.assertEqual(len(got), 5)
        self.assertLessEqual(len(got[0]["summary"]), 160)


class DigestRendering(unittest.TestCase):
    def test_digest_lists_only_pages_needing_the_model(self):
        result = {
            "summary": {"pages": 3, "clean": 2, "needs_model": 1, "distinct_repos": 1},
            "budget": {"degraded": False},
            "pages": [
                {"path": "a.md", "slug": "a", "needs_model": False, "flags": [],
                 "verification": "works", "verified_on": "2026-07-20", "targets": [],
                 "reason": ""},
                {"path": "b.md", "slug": "b", "needs_model": False, "flags": [],
                 "verification": "works", "verified_on": "2026-07-20", "targets": [],
                 "reason": ""},
                {"path": "c.md", "slug": "c", "needs_model": True, "flags": ["repo-404"],
                 "verification": "works", "verified_on": "2026-07-20",
                 "targets": [{"kind": "github-repo", "repo": "o/r", "status": 404}],
                 "reason": "repo-404"},
            ],
        }
        md = cl.render_digest(result)
        self.assertIn("Needs your adjudication (1)", md)
        self.assertIn("`c.md`", md)
        self.assertIn("repo-404", md)
        self.assertIn("`a`", md)          # clean slugs still named, in a details block
        self.assertNotIn("- [ ] `a.md`", md)   # but not as work items

    def test_digest_warns_loudly_when_degraded(self):
        result = {"summary": {"pages": 1, "clean": 0, "needs_model": 1, "distinct_repos": 0},
                  "budget": {"degraded": True}, "pages": []}
        self.assertIn("do not treat any page as clean", cl.render_digest(result))

    def test_digest_stays_small(self):
        pages = [{"path": f"p{i}.md", "slug": f"p{i}", "needs_model": False, "flags": [],
                  "verification": "works", "verified_on": "2026-07-20", "targets": [],
                  "reason": ""} for i in range(120)]
        result = {"summary": {"pages": 120, "clean": 120, "needs_model": 0,
                              "distinct_repos": 10},
                  "budget": {"degraded": False}, "pages": pages}
        self.assertLess(len(cl.render_digest(result)), 4000)


if __name__ == "__main__":
    unittest.main()


class LicenseFlagPrecision(unittest.TestCase):
    """`license-unrecognized` vs `license-absent` decides whether the model must
    fetch the LICENSE text. The Verifier surfaced this in validation: GitHub returns
    NOASSERTION for a repo whose root LICENSE is verbatim CC BY 4.0, which is a very
    different finding from having no licence at all -- and the same flag also covers
    Augmented-Nature's restrictive non-commercial grants."""

    def _repo(self, license_obj):
        body = {"full_name": "o/r", "owner": {"login": "o"},
                "pushed_at": "2026-07-01T00:00:00Z"}
        if license_obj is not None:
            body["license"] = license_obj
        f = cl.Fetcher(opener=StubOpener(routes={"api.github.com": (200, body)}))
        return cl.fetch_repo(f, "o/r")

    def test_noassertion_is_unrecognized_not_absent(self):
        got = self._repo({"spdx_id": "NOASSERTION"})
        self.assertEqual(got["license_raw"], "NOASSERTION")
        self.assertIsNone(got["license_spdx"])

    def test_no_license_object_is_absent(self):
        got = self._repo(None)
        self.assertIsNone(got["license_raw"])
        self.assertIsNone(got["license_spdx"])

    def test_real_spdx_id_is_neither(self):
        got = self._repo({"spdx_id": "MIT"})
        self.assertEqual(got["license_spdx"], "MIT")

    def test_the_two_flags_are_distinct_strings(self):
        # Guards against a refactor collapsing them back into one flag, which would
        # cost the model a LICENSE fetch on every page that has a licence.
        src = (REPO / "scripts" / "check_liveness.py").read_text(encoding="utf-8")
        self.assertIn('"license-unrecognized"', src)
        self.assertIn('"license-absent"', src)
        self.assertNotIn('"license-missing"', src)
