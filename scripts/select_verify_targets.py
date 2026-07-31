#!/usr/bin/env python3
"""Deterministically pick which catalog pages the Verifier agent stamps this run.

The agent must NOT enumerate the tree itself — doing so produced a reproducible
blind spot (7 pages were missed across dozens of runs while the agent's own count
settled at "440/440 complete"). This script is the single source of truth for the
per-run worklist: it lists every `catalog/tools/*.md` (except `index.md`), orders
them **unstamped-first, then oldest `verified_on`, then alphabetically**, and
emits the top `--count` as a markdown checklist the workflow injects into the
agent prompt.

Rotation (--rotate): when the whole catalog shares one `verified_on` (e.g. after
a bulk stamp), the oldest-first tie-break collapses to alphabetical and the same
top `--count` slugs are served every run — the pointer never advances and most
pages are never re-verified. To guarantee forward progress, each equal-
`verified_on` group of *stamped* pages is rotated by `--rotate * --count`, so
successive runs (the workflow passes `github.run_number`) serve a sliding window
that tiles the whole catalog. Unstamped pages are never rotated — they stay at
the front and drain in order. --rotate 0 (the default) reproduces the plain
deterministic ordering.

Staleness (--max-age-days): a page verified within the last N days is not due, so it
never reaches the worklist and never costs the agent a token. When nothing is due the
batch is empty and `verify.yml` skips the Claude step outright. The filter lives in
`due()` and is applied in `main()` — deliberately NOT inside `worklist()`, because
`tests/test_composer.py::test_covers_every_tool_page` asserts `worklist()` returns
every page on disk and exists to guard the enumeration blind spot described above.
Do not "simplify" the filter into `worklist()`.

--max-age-days and --rotate must not compose: rotation exists only because stamped
pages never leave the candidate set, and once staleness removes them the pointer
advances by itself. Applying both would advance the window *and* shrink the list — a
double-skip that opens coverage gaps inside a cycle. main() forces offset 0 whenever
--max-age-days is in effect.

stdlib only. Run: python3 scripts/select_verify_targets.py --count 25 --max-age-days 30 --out .verify/worklist.md
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from itertools import groupby
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "catalog" / "tools"


def _frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm: dict = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def worklist(tools_dir: Path, offset: int = 0) -> list[dict]:
    """Every tool page, ordered unstamped-first then oldest verified_on then slug.

    `offset` left-rotates each equal-`verified_on` group of *stamped* pages so
    that, run over run, a different slice of a same-date group reaches the front.
    This is what stops the worklist re-serving the identical top `--count` when
    the whole catalog shares one `verified_on`. offset 0 = no rotation.
    """
    rows = []
    for p in sorted(tools_dir.glob("*.md")):
        if p.name == "index.md":
            continue
        fm = _frontmatter(p.read_text(encoding="utf-8"))
        stamped = bool(fm.get("verification"))
        rows.append({
            "slug": p.stem,
            "path": f"catalog/tools/{p.name}",
            "verification": fm.get("verification", ""),
            "verified_on": fm.get("verified_on", ""),
            "stamped": stamped,
        })
    # unstamped (0) before stamped (1); within stamped, oldest verified_on first
    # ("" sorts before any date, so a stamped-but-dateless page is treated as old);
    # slug breaks ties for full determinism.
    rows.sort(key=lambda r: (r["stamped"], r["verified_on"], r["slug"]))
    if not offset:
        return rows
    # Rotate each stamped, equal-verified_on group so the served window advances.
    ordered = []
    for (stamped, _date), grp in groupby(rows, key=lambda r: (r["stamped"], r["verified_on"])):
        g = list(grp)
        if stamped and len(g) > 1:
            k = offset % len(g)
            g = g[k:] + g[:k]
        ordered.extend(g)
    return ordered


def due(rows: list[dict], today: str, max_age_days: int | None) -> list[dict]:
    """Rows whose `verified_on` is older than `max_age_days` days before `today`.

    An unstamped page is always due. A missing, empty, or unparseable `verified_on`
    is also treated as due — a page whose freshness cannot be established must be
    re-checked, never silently skipped. `max_age_days=None` is a no-op (returns
    `rows` unchanged), which preserves the pre-staleness behaviour exactly.

    `max_age_days=0` makes every page due, including ones stamped today: it is the
    manual "re-verify everything" override, not a drain-across-runs setting.
    """
    if max_age_days is None:
        return rows
    try:
        cutoff = date.fromisoformat(today) - timedelta(days=max(0, max_age_days))
    except ValueError:
        # An unusable --today must not silently drop the whole batch.
        return rows
    out = []
    for r in rows:
        if not r["stamped"]:
            out.append(r)
            continue
        try:
            stamped_on = date.fromisoformat(r["verified_on"])
        except ValueError:
            out.append(r)  # no/garbled date -> due
            continue
        if stamped_on <= cutoff:
            out.append(r)
    return out


def effective_offset(rotate: int, count: int, max_age_days: int | None) -> int:
    """The rotation offset to actually use, given the staleness setting.

    Rotation and a positive staleness threshold must never compose. Rotation exists
    only because stamped pages never left the candidate set; once staleness retires
    them the pointer advances by itself, so applying both would advance the window
    AND shrink the list — a double-skip that opens coverage gaps inside a cycle.

    `max_age_days=0` is the exception: it makes every page due regardless of when it
    was stamped, so nothing retires and rotation is still the correct pointer there.
    """
    offset = max(0, rotate) * max(1, count)
    if max_age_days is not None and max_age_days > 0:
        return 0
    return offset


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic Verifier worklist.")
    ap.add_argument("--count", type=int, default=25, help="max pages this run")
    ap.add_argument("--rotate", type=int, default=0,
                    help="run counter (e.g. github.run_number); rotates same-date "
                         "groups so the served window advances each run. Ignored "
                         "when --max-age-days is set (see module docstring)")
    ap.add_argument("--max-age-days", type=int, default=None,
                    help="only serve pages last verified more than N days ago; "
                         "omit for the previous always-serve behaviour")
    ap.add_argument("--today", default=None,
                    help="UTC date as YYYY-MM-DD (default: today); injectable for tests")
    ap.add_argument("--out", type=Path, default=None, help="write markdown checklist here")
    ap.add_argument("--json", dest="json_out", type=Path, default=None,
                    help="write the batch as JSON here (consumed by check_liveness.py "
                         "and by the workflow's empty-batch gate)")
    args = ap.parse_args()

    count = max(1, args.count)
    today = args.today or date.today().isoformat()

    # Slide the window by a full batch each run so successive runs tile the catalog.
    offset = effective_offset(args.rotate, count, args.max_age_days)
    if args.rotate and not offset:
        print("note: --rotate ignored because --max-age-days is set", file=sys.stderr)

    rows = worklist(TOOLS, offset)
    total = len(rows)
    unstamped = sum(1 for r in rows if not r["stamped"])
    candidates = due(rows, today, args.max_age_days)
    batch = candidates[:count]

    if args.max_age_days is None:
        window = ("Ordered unstamped-first, then oldest `verified_on`, with same-date groups "
                  "rotated per run\nso the window advances (no page is starved when the catalog "
                  "shares one date). Work\ntop-to-bottom; if the count budget runs out, stop — "
                  "the next run serves the next window.")
    else:
        window = (f"Only pages last verified more than {args.max_age_days} days before {today} are "
                  f"due; {len(candidates)} of\n{total} pages qualify. Ordered unstamped-first then "
                  "oldest `verified_on`. Work top-to-bottom;\nif the budget runs out, stop — the "
                  "remainder stays due and leads the next run.")

    lines = [
        "## This run's worklist (verify EXACTLY these pages — do not enumerate the tree yourself)",
        "",
        f"Catalog total: {total} tool pages · unstamped: {unstamped} · due: {len(candidates)} · "
        f"this batch: {len(batch)}.",
        window,
        "",
    ]
    for r in batch:
        tag = "UNSTAMPED" if not r["stamped"] else f"{r['verification']} · {r['verified_on'] or 'no-date'}"
        lines.append(f"- [ ] `{r['path']}` — {tag}")
    if not batch:
        lines.append("_Nothing is due this run._")
    text = "\n".join(lines) + "\n"

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps({
            "schema": "worklist-v1",
            "today": today,
            "max_age_days": args.max_age_days,
            "total": total,
            "unstamped": unstamped,
            "due": len(candidates),
            "batch": batch,
        }, indent=2) + "\n", encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
