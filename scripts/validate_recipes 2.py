#!/usr/bin/env python3
"""Validate recipe pages and emit report.json.

This is the re-runnable signal for the repair loop (see repair_agent.py). For each
recipe under ``recipes/items/*.md`` it checks:

- required frontmatter fields are present  -> ``missing_fields``
- every external link resolves             -> ``broken_links`` / ``blocked_links``

Buckets follow the semantics of the original report.json:

- broken  = 404/410/5xx, DNS/connection errors, timeouts. These set ``passed=False``.
- blocked = 401/403/429. Recorded but NON-fatal: these are almost always valid pages
            that block bots or rate-limit, so they do not fail a recipe.

Known difference from the original report.json: the old ``links_checked`` counted
every href on the *rendered* HTML page (~580/recipe), including the shared site nav.
This validator counts each recipe's *own* links (extracted from the markdown source),
which is what actually drives the broken/blocked signal. ``fetch_ok`` here means the
source file parsed and its frontmatter loaded (we do not build the Jekyll site).

Usage:
    python3 scripts/validate_recipes.py                 # validate all -> report.json
    python3 scripts/validate_recipes.py --only <slug>   # one recipe, print JSON
    python3 scripts/validate_recipes.py --out out.json --workers 16 --timeout 10
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import sys
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ITEMS_DIR = REPO_ROOT / "recipes" / "items"
PAGES_BASE = "https://scripps-ai-enablement.github.io/sci-ai-enabler/recipes/items"

# Frontmatter keys every recipe is expected to carry (derived from existing recipes).
REQUIRED_FIELDS = [
    "title",
    "parent",
    "problem_class",
    "subject_areas",
    "evidence_level",
    "complexity",
    "availability",
    "compute_requirements",
    "last_verified",
    "summary",
]

# The site's own domain — links to it are "internal" and not fetched externally.
INTERNAL_HOST = "scripps-ai-enablement.github.io"

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

BLOCKED_STATUS = {401, 403, 429}

# Reference defs: [id]: url
_MD_REF = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
# Bare URLs (destination form is parsed separately, with balanced parens).
_BARE_URL = re.compile(r"https?://[^\s<>\"'\]]+")


def _read_destination(body: str, i: int) -> tuple[str, int]:
    """Read a markdown link destination starting just after ``(``.

    Handles both the ``<url>`` form and bare destinations, where CommonMark
    allows *balanced* parentheses inside the URL (e.g. DOIs like
    ``10.1016/s0169-409x(00)00129-0``). Returns (url, index_after_url)."""
    n = len(body)
    if i < n and body[i] == "<":
        j = body.find(">", i + 1)
        if j != -1:
            return body[i + 1:j], j + 1
    depth = 0
    buf: list[str] = []
    while i < n:
        c = body[i]
        if c == "(":
            depth += 1
            buf.append(c)
        elif c == ")":
            if depth == 0:
                break  # closes the markdown link
            depth -= 1
            buf.append(c)
        elif c.isspace():
            break  # start of an optional title
        else:
            buf.append(c)
        i += 1
    return "".join(buf), i


def _trim_bare(u: str) -> str:
    """Trim trailing punctuation / unbalanced close-parens from a bare URL."""
    while u and u[-1] in ".,;:!?":
        u = u[:-1]
    while u.endswith(")") and u.count("(") < u.count(")"):
        u = u[:-1]
    return u


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Empty dict if no/invalid frontmatter."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        fm = {}
    if not isinstance(fm, dict):
        fm = {}
    return fm, parts[2]


def extract_links(body: str) -> list[str]:
    """All URLs referenced in the markdown body, de-duplicated, order-preserved."""
    urls: list[str] = []
    seen: set[str] = set()

    def add(u: str) -> None:
        u = u.strip()
        if u and u not in seen:
            seen.add(u)
            urls.append(u)

    # Markdown inline links: scan each "](", reading a balanced destination.
    pos = 0
    while True:
        k = body.find("](", pos)
        if k == -1:
            break
        url, end = _read_destination(body, k + 2)
        add(url)
        pos = end

    for m in _MD_REF.finditer(body):
        add(_trim_bare(m.group(1)))
    for m in _BARE_URL.finditer(body):
        add(_trim_bare(m.group(0)))
    return urls


def is_external(url: str) -> bool:
    if not url.startswith(("http://", "https://")):
        return False  # relative link within the site
    return INTERNAL_HOST not in url


def classify_response(url: str, session: requests.Session, timeout: float) -> dict | None:
    """Fetch a URL once (with one retry) and classify it.

    Returns None if the link is OK, otherwise a finding dict with ``kind`` set to
    ``broken`` or ``blocked``.
    """
    last_detail = ""
    for attempt in range(2):
        try:
            resp = session.get(
                url, headers=BROWSER_HEADERS, timeout=timeout,
                allow_redirects=True, stream=True,
            )
            status = resp.status_code
            resp.close()
        except requests.RequestException as exc:
            last_detail = f"error: {type(exc).__name__}"
            continue  # transient — retry once
        if status in BLOCKED_STATUS:
            return {"href": url, "url": url, "kind": "external",
                    "bucket": "blocked", "detail": f"HTTP {status}"}
        if status >= 400:
            return {"href": url, "url": url, "kind": "external",
                    "bucket": "broken", "detail": f"HTTP {status}"}
        return None  # 2xx/3xx-resolved -> OK
    return {"href": url, "url": url, "kind": "external",
            "bucket": "broken", "detail": last_detail or "error: RequestException"}


def validate_recipe(path: Path, url_status: dict[str, dict | None]) -> dict:
    """Build the per-recipe result dict from precomputed URL statuses."""
    slug = path.stem
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)

    missing = [f for f in REQUIRED_FIELDS if f not in fm or fm[f] in (None, "", [])]
    fetch_ok = bool(fm)  # frontmatter parsed => source is well-formed

    external = [u for u in extract_links(body) if is_external(u)]
    broken, blocked = [], []
    for u in external:
        finding = url_status.get(u)
        if finding is None:
            continue
        entry = {k: finding[k] for k in ("href", "url", "kind", "detail")}
        (broken if finding["bucket"] == "broken" else blocked).append(entry)

    passed = fetch_ok and not missing and not broken
    return {
        "slug": slug,
        "url": f"{PAGES_BASE}/{slug}.html",
        "passed": passed,
        "fetch_ok": fetch_ok,
        "fetch_detail": "" if fetch_ok else "frontmatter did not parse",
        "missing_fields": missing,
        "links_checked": len(external),
        "broken_links": broken,
        "blocked_links": blocked,
    }


def is_recipe(path: Path) -> bool:
    """True for real recipe pages. Section/listing pages (e.g. index.md) carry no
    ``problem_class`` and must not be validated as recipes."""
    fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    return "problem_class" in fm


def collect_recipes(only: str | None) -> list[Path]:
    if only:
        p = ITEMS_DIR / f"{only}.md"
        if not p.exists():
            sys.exit(f"No such recipe: {p}")
        return [p]  # explicit request — validate as asked
    return [p for p in sorted(ITEMS_DIR.glob("*.md")) if is_recipe(p)]


def build_report(only: str | None, workers: int, timeout: float) -> dict:
    paths = collect_recipes(only)

    # Gather the full set of external URLs across the selected recipes, then fetch
    # each unique URL once (many links are shared across recipes).
    all_urls: set[str] = set()
    for p in paths:
        _, body = split_frontmatter(p.read_text(encoding="utf-8"))
        all_urls.update(u for u in extract_links(body) if is_external(u))

    url_status: dict[str, dict | None] = {}
    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(classify_response, u, session, timeout): u
                for u in all_urls
            }
            for fut in concurrent.futures.as_completed(futures):
                url_status[futures[fut]] = fut.result()

    recipes = [validate_recipe(p, url_status) for p in paths]
    passed = sum(1 for r in recipes if r["passed"])
    with_blocked = sum(1 for r in recipes if r["blocked_links"])
    return {
        "summary": {
            "total": len(recipes),
            "passed": passed,
            "failed": len(recipes) - passed,
            "recipes_with_blocked_links": with_blocked,
        },
        "recipes": recipes,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate recipes and emit report.json")
    ap.add_argument("--only", help="Validate a single recipe by slug")
    ap.add_argument("--out", default=None,
                    help="Write the report to this path (default: report.json, "
                         "or stdout when --only is used)")
    ap.add_argument("--workers", type=int, default=16, help="Concurrent fetchers")
    ap.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout (s)")
    args = ap.parse_args()

    report = build_report(args.only, args.workers, args.timeout)

    if args.only and args.out is None:
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        out = Path(args.out) if args.out else (REPO_ROOT / "report.json")
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        s = report["summary"]
        print(f"Wrote {out} — {s['passed']}/{s['total']} passed, {s['failed']} failed")

    return 1 if report["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
