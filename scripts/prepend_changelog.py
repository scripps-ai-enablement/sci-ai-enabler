#!/usr/bin/env python3
"""Prepend an agent's dated changelog block, then rotate old blocks to an archive.

Why this exists
---------------
The five changelogs reached 673 KB combined (CHANGELOG.md alone 205 KB). Every
curator was told to *edit* its changelog, so each run paid to read a ~100 KB file
into context before writing four lines into it, and `digest.yml` read four of them
in one prompt (~140 K input tokens per weekly run). Two fixes, both here:

1. **The agent no longer touches the changelog.** It `Write`s a small dated block
   to a scratch file and this script splices it in. That removes the file from the
   agent's context entirely and kills a failure class where an agent mangles a
   100 KB file with a fuzzy `Edit`.
2. **The live file is capped.** Only the newest `--keep` blocks stay; older ones
   move to `<NAME>_ARCHIVE.md`, newest-first, so the archive reads like the live
   file. Nothing is ever deleted.

`--keep` is a floor, not a ceiling. `digest.yml` reads four of these files with a
`since` window (7 days by default) and summarizes every block on or after it, so
archiving a block that is still inside that window would silently drop it from the
weekly digest — and the catalog curator alone writes 7-8 blocks per weekend, which
a plain count cap cannot bound. `--min-days` (default 21) therefore raises the
effective keep count as needed, measured back from the newest block's own date.

Two invariants the rotation must not break
------------------------------------------
Six workflows extract the newest block for their tracking-issue comment with
`awk '/^## / {n++} n>=2 {exit} n==1 {print}'`. That requires:

  (a) the newest block is the FIRST `^## ` line in the file, and
  (b) the preamble contains NO `^## ` line.

`verify_awk_invariant()` asserts both after every write, and
`tests/test_changelog_rotation.py` pins them with a Python reimplementation of
that exact awk program.

Jekyll: four of the five changelogs carry front matter and render as site pages;
VERIFIER_CHANGELOG.md has none and is copied verbatim. An archive inherits its
source's convention, and a rendered archive gets `nav_exclude: true` so it does
not clutter the sidebar.

stdlib only. Run:
  python3 scripts/prepend_changelog.py --file CHANGELOG.md --block .changelog-block.md --keep 12
  python3 scripts/prepend_changelog.py --file CHANGELOG.md --keep 12        # rotate only
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

BLOCK_RE = re.compile(r"^## ", re.M)
# Every block in all five changelogs opens `## YYYY-MM-DD`, optionally followed by
# a parenthetical. The awk extractor returns whatever the first `## ` block is, so
# a stray non-dated H2 landing on top (say, an archive pointer written as a
# heading) would silently replace the newest entry in six tracking-issue comments.
DATED_HEADING_RE = re.compile(r"^## \d{4}-\d{2}-\d{2}")
ARCHIVE_POINTER = "Older entries live in [{name}]({link})."


def split_blocks(text: str) -> tuple[str, list[str]]:
    """Split a changelog into (preamble, [blocks]). A block starts at a `## ` line.

    The preamble is everything before the first `## ` — front matter, the H1, and
    any intro prose. Returned verbatim so a round trip is byte-exact.
    """
    starts = [m.start() for m in BLOCK_RE.finditer(text)]
    if not starts:
        return text, []
    preamble = text[: starts[0]]
    bounds = starts + [len(text)]
    blocks = [text[bounds[i] : bounds[i + 1]] for i in range(len(starts))]
    return preamble, blocks


def verify_awk_invariant(text: str) -> None:
    """Fail loudly if the six workflows' `awk` newest-block extractor would break.

    The extractor returns the first `## ` block, so the only thing that can go
    wrong is a non-dated H2 reaching the top of the file — then every tracking
    issue gets that instead of the newest entry. A file with no blocks at all is
    fine (a freshly initialised changelog).
    """
    _, blocks = split_blocks(text)
    if blocks and not DATED_HEADING_RE.match(blocks[0]):
        raise AssertionError(
            "the first '## ' block is not a dated entry: "
            f"{blocks[0].splitlines()[0]!r}. The awk newest-block extractor in six "
            "workflows would return this instead of the newest changelog entry.")


def _min_kept_for_window(blocks: list[str], min_days: int) -> int:
    """How many leading blocks must stay so the newest `min_days` are all present.

    Dates come from the `## YYYY-MM-DD` headings, measured back from the newest
    block's own date rather than today's: rotation must be reproducible, and a file
    that has not been written to in a while should not shed its recent history just
    because the calendar moved on. An unparseable heading is conservatively kept.
    """
    if min_days <= 0 or not blocks:
        return 0
    dates: list[date | None] = []
    for b in blocks:
        m = DATED_HEADING_RE.match(b)
        try:
            dates.append(date.fromisoformat(m.group(0)[3:]) if m else None)
        except ValueError:
            dates.append(None)
        # A block whose date we cannot read is kept, so we never drop it by accident.
    newest = next((d for d in dates if d), None)
    if newest is None:
        return len(blocks)
    cutoff = newest - timedelta(days=min_days)
    keep = 0
    for i, d in enumerate(dates):
        if d is None or d >= cutoff:
            keep = i + 1
    return keep


def _front_matter(preamble: str) -> str:
    """Return the leading `---` front-matter block, or '' when there is none."""
    if not preamble.startswith("---"):
        return ""
    end = preamble.find("\n---", 3)
    return "" if end == -1 else preamble[: end + 4]


def archive_preamble(live_preamble: str, live_name: str, archive_name: str) -> str:
    """Build a preamble for a fresh archive that mirrors the live file's convention.

    Must contain no `## ` line, so the archive stays awk-compatible too.
    """
    fm = _front_matter(live_preamble)
    title_m = re.search(r"^title:\s*(.+)$", fm, re.M) if fm else None
    heading_m = re.search(r"^# (.+)$", live_preamble, re.M)
    label = (title_m.group(1).strip() if title_m
             else heading_m.group(1).strip() if heading_m
             else archive_name)
    out = []
    if fm:
        # Rendered by Jekyll; keep it out of the nav so archives don't pile up there.
        out.append("---\n"
                   f"title: {label} archive\n"
                   "nav_exclude: true\n"
                   "---\n")
    out.append(f"\n# {label} archive\n\n"
               f"Older entries rotated out of [{live_name}]({live_name}). "
               "Newest first, same format.\n")
    return "".join(out)


def ensure_pointer(preamble: str, live_name: str, archive_name: str) -> str:
    """Add a one-line pointer to the archive. Never an H2 (see the awk invariant)."""
    pointer = ARCHIVE_POINTER.format(name=archive_name, link=archive_name)
    if pointer in preamble:
        return preamble
    return preamble.rstrip("\n") + "\n\n" + pointer + "\n\n"


def run(live: Path, block: Path | None, keep: int, archive: Path | None,
        min_days: int = 21) -> int:
    if not live.exists():
        print(f"error: {live} does not exist", file=sys.stderr)
        return 1
    archive = archive or live.with_name(f"{live.stem}_ARCHIVE{live.suffix}")

    text = live.read_text(encoding="utf-8")
    verify_awk_invariant(text)  # refuse to operate on an already-broken file
    preamble, blocks = split_blocks(text)

    if block is not None:
        if not block.exists() or not block.read_text(encoding="utf-8").strip():
            print(f"note: {block} missing or empty; rotating only", file=sys.stderr)
        else:
            new = block.read_text(encoding="utf-8").strip("\n")
            if not DATED_HEADING_RE.match(new):
                print(f"error: {block} must start with a '## YYYY-MM-DD' heading",
                      file=sys.stderr)
                return 1
            if BLOCK_RE.search(new[3:]):
                print(f"error: {block} contains more than one '## ' block", file=sys.stderr)
                return 1
            blocks.insert(0, new + "\n\n")
            print(f"prepended {len(new)} bytes to {live.name}")

    evicted: list[str] = []
    if keep > 0 and len(blocks) > keep:
        # Never evict a block still inside the digest's reach. digest.yml reads
        # these files with a `since` window (7 days by default) and summarizes
        # every `## YYYY-MM-DD` block on or after it, so rotating a block out of
        # the live file *within* that window would silently drop it from the
        # weekly digest. The catalog curator alone writes 7-8 blocks a weekend, so
        # a plain count cap is not safe on its own.
        floor = _min_kept_for_window(blocks, min_days)
        effective = max(keep, floor)
        if len(blocks) > effective:
            evicted = blocks[effective:]
            blocks = blocks[:effective]

    if evicted:
        if archive.exists():
            a_pre, a_blocks = split_blocks(archive.read_text(encoding="utf-8"))
        else:
            a_pre, a_blocks = archive_preamble(preamble, live.name, archive.name), []
        # Evicted blocks are newer than everything already archived, so they go on
        # top: the archive stays newest-first, like the live file.
        a_text = a_pre + "".join(evicted + a_blocks)
        verify_awk_invariant(a_text)
        archive.write_text(a_text, encoding="utf-8")
        preamble = ensure_pointer(preamble, live.name, archive.name)
        print(f"rotated {len(evicted)} block(s) to {archive.name}")

    out = preamble + "".join(blocks)
    verify_awk_invariant(out)
    live.write_text(out, encoding="utf-8")
    print(f"{live.name}: {len(blocks)} block(s), {len(out)} bytes")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--file", type=Path, required=True, help="the live changelog")
    ap.add_argument("--block", type=Path, default=None,
                    help="scratch file holding one new '## ' block to prepend")
    ap.add_argument("--keep", type=int, default=12,
                    help="minimum blocks to keep in the live file; the rest are archived "
                         "(0 = no rotation). Raised automatically to cover --min-days.")
    ap.add_argument("--min-days", type=int, default=21,
                    help="never archive a block newer than this many days before the "
                         "newest block, whatever --keep says. Protects digest.yml's "
                         "`since` window (7 days by default).")
    ap.add_argument("--archive", type=Path, default=None,
                    help="archive path (default: <stem>_ARCHIVE.md)")
    args = ap.parse_args()
    return run(args.file, args.block, args.keep, args.archive, args.min_days)


if __name__ == "__main__":
    raise SystemExit(main())
