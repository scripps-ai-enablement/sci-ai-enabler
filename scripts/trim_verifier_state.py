#!/usr/bin/env python3
"""Cap the `## Recently verified` section of catalog/verifier-state.md.

Why only that section
---------------------
`catalog/verifier-state.md` reached 60,558 bytes, and the Verifier agent reads it
in full at the start of every run and rewrites it at the end. Measured breakdown:

    ## Recently verified            12,628 B    8 items   (longest item 2,323 B)
    ## Flagged (broken or security)  19,638 B   42 items
    ## Deferred — next-run priority  25,650 B   35 items
    ## Smoke-test queue               1,580 B    7 items

`VERIFIER_AGENT.md` already caps `## Recently verified` at "~last 8" and the agent
honors it — there are exactly 8 items. The cap is on the wrong axis: each item is a
~2.3 KB wall of prose that duplicates, almost verbatim, the changelog block for the
same run. That section is pure redundant history, so it is safe to trim by dropping
whole trailing items.

The other three sections are deliberately NOT trimmed here. `## Flagged` is a
registry of real broken entries and security findings, and `## Deferred` is the
queue of unresolved work; mechanically dropping items from either would silently
lose information a script cannot judge the value of. Those get per-item length
guidance and an expiry rule in `VERIFIER_AGENT.md`, enforced by the agent, not by
truncation here. Truncating prose mid-sentence would also mangle the evidence
anchors that make a flag auditable.

stdlib only. Run:
  python3 scripts/trim_verifier_state.py --file catalog/verifier-state.md --keep 6
  python3 scripts/trim_verifier_state.py --file catalog/verifier-state.md --check
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SECTION_RE = re.compile(r"^## ", re.M)
TARGET = "## Recently verified"
# Items are top-level bullets; continuation lines are indented under them.
ITEM_RE = re.compile(r"^- ", re.M)


def split_sections(text: str) -> tuple[str, list[str]]:
    """Split into (preamble, [sections]); a section starts at a `## ` line."""
    starts = [m.start() for m in SECTION_RE.finditer(text)]
    if not starts:
        return text, []
    bounds = starts + [len(text)]
    return text[: starts[0]], [text[bounds[i] : bounds[i + 1]] for i in range(len(starts))]


def split_items(section: str) -> tuple[str, list[str]]:
    """Split one section into (heading+intro, [items]) on top-level `- ` bullets."""
    starts = [m.start() for m in ITEM_RE.finditer(section)]
    if not starts:
        return section, []
    bounds = starts + [len(section)]
    return section[: starts[0]], [section[bounds[i] : bounds[i + 1]] for i in range(len(starts))]


def trim(text: str, keep: int) -> tuple[str, int, list[int]]:
    """Return (new_text, dropped_count, sizes_of_kept_items)."""
    preamble, sections = split_sections(text)
    dropped, sizes = 0, []
    for i, sec in enumerate(sections):
        if not sec.startswith(TARGET):
            continue
        head, items = split_items(sec)
        sizes = [len(x) for x in items[:keep]]
        if keep >= 0 and len(items) > keep:
            dropped = len(items) - keep
            kept = items[:keep]
            # Preserve the trailing blank line that separated this section.
            body = "".join(kept).rstrip("\n") + "\n\n"
            sections[i] = head + body
        break
    return preamble + "".join(sections), dropped, sizes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--file", type=Path, default=Path("catalog/verifier-state.md"))
    ap.add_argument("--keep", type=int, default=6, help="items to keep in Recently verified")
    ap.add_argument("--max-item-bytes", type=int, default=400,
                    help="report (do not truncate) items longer than this")
    ap.add_argument("--check", action="store_true",
                    help="report only; exit 0 regardless. Never fails a run.")
    args = ap.parse_args()

    if not args.file.exists():
        print(f"note: {args.file} does not exist; nothing to trim", file=sys.stderr)
        return 0

    text = args.file.read_text(encoding="utf-8")
    out, dropped, sizes = trim(text, args.keep)

    over = [n for n in sizes if n > args.max_item_bytes]
    if over:
        # Reported, not truncated: cutting an evidence anchor mid-sentence would
        # make a flag unauditable. VERIFIER_AGENT.md asks the agent to keep these
        # short; this is the signal that it did not.
        print(f"note: {len(over)} '{TARGET}' item(s) exceed {args.max_item_bytes} bytes "
              f"(largest {max(over)}); the agent is writing changelog-length prose here",
              file=sys.stderr)

    if args.check:
        print(f"{args.file}: {len(text)} bytes; would drop {dropped} item(s) "
              f"-> {len(out)} bytes")
        return 0

    if out != text:
        args.file.write_text(out, encoding="utf-8")
        print(f"{args.file}: dropped {dropped} '{TARGET}' item(s), "
              f"{len(text)} -> {len(out)} bytes")
    else:
        print(f"{args.file}: already within the cap ({len(text)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
