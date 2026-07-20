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

stdlib only. Run: python3 scripts/select_verify_targets.py --count 25 --rotate 0 --out .verify/worklist.md
"""
from __future__ import annotations

import argparse
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


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic Verifier worklist.")
    ap.add_argument("--count", type=int, default=25, help="max pages this run")
    ap.add_argument("--rotate", type=int, default=0,
                    help="run counter (e.g. github.run_number); rotates same-date "
                         "groups so the served window advances each run")
    ap.add_argument("--out", type=Path, default=None, help="write markdown checklist here")
    args = ap.parse_args()

    count = max(1, args.count)
    # Slide the window by a full batch each run so successive runs tile the catalog.
    offset = max(0, args.rotate) * count
    rows = worklist(TOOLS, offset)
    unstamped = sum(1 for r in rows if not r["stamped"])
    batch = rows[:count]

    lines = [
        "## This run's worklist (verify EXACTLY these pages — do not enumerate the tree yourself)",
        "",
        f"Catalog total: {len(rows)} tool pages · unstamped: {unstamped} · this batch: {len(batch)}.",
        "Ordered unstamped-first, then oldest `verified_on`, with same-date groups rotated per run",
        "so the window advances (no page is starved when the catalog shares one date). Work",
        "top-to-bottom; if the count budget runs out, stop — the next run serves the next window.",
        "",
    ]
    for r in batch:
        tag = "UNSTAMPED" if not r["stamped"] else f"{r['verification']} · {r['verified_on'] or 'no-date'}"
        lines.append(f"- [ ] `{r['path']}` — {tag}")
    text = "\n".join(lines) + "\n"

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
