#!/usr/bin/env python3
"""Refresh `verified_on` for pages the liveness prefetch found unchanged and clean.

The integrity question, answered honestly
----------------------------------------
A script-written stamp is NOT what `verification: works` currently claims.
`VERIFIER_AGENT.md` defines `works` as resolving **and** either a smoke-test pass or
an install path *and its launch command* confirmed against a primary source, and it
says outright that a resolvable package alone is never enough. No liveness script
can establish that clause.

What a script CAN establish is narrower and still load-bearing: *nothing about this
target has changed since the run where that clause was established.* The install
target still resolves, the skill directory is still present, the repo is not
archived or renamed, the license is unchanged, no new OSV advisory matches, and no
commit has touched the page's own path since `verified_on`. That is a recheck, not a
fresh verification — the same basis every "unchanged since last audit" control uses.

Writing that as though a model had looked would be the dishonest version. So this
script writes `verified_on` and **never writes `reviewed_on`**:

    verification: works        # closed vocabulary, unchanged
    verified_on: 2026-08-19    # last date the entry was confirmed LIVE (script or agent)
    reviewed_on: 2026-07-20    # last date a MODEL did the full primary-source review
    verification_note: "automated recheck — targets resolve unchanged since 2026-07-20"

`verified_on == reviewed_on` means a model looked. `verified_on > reviewed_on` means
a script confirmed nothing moved. That invariant is the whole point, and
`tests/test_clean_stamps.py::test_never_writes_reviewed_on` is what keeps it true.

Eligibility is deliberately narrow (phase 1)
--------------------------------------------
Only `works` + `cleared` + zero flags + unchanged. Measured over the 459 pages:
`works`+`cleared` 348, `works`+`caution` 85, `degraded`/`broken` 26. So ~76% is
eligible and every page carrying a narrative caution or an open problem still
reaches the model — those have a story in `catalog/verifier-state.md` that a script
cannot advance. Extending to `works`+`caution` needs a machine-readable caution
reason the pages do not carry; not attempted here.

Off by default
--------------
`--apply` is required to write anything. Without it this reports what it *would*
stamp and changes nothing. The liveness prefetch has one validated shadow cycle so
far, and that cycle found a defect affecting 24 pages, so the default has to be the
safe one.

Fails soft, never fails the run: a page whose front matter will not parse, or whose
`| **Verified** |` row cannot be found, is left untouched and reported so it reaches
the model instead.

stdlib only. Run:
  python3 scripts/apply_clean_stamps.py --liveness .verify/liveness.json --date 2026-08-19
  python3 scripts/apply_clean_stamps.py --liveness .verify/liveness.json --date 2026-08-19 --apply

The `--changelog-block` it writes is a SEPARATE file from the agent's own
`.changelog-block.md`; `prepend_changelog.py --extra-block` merges the two into one
dated entry so a run where both happened records both.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

NOTE_TEMPLATE = "automated recheck — targets resolve unchanged since {reviewed}"
VERIFIED_ROW_RE = re.compile(r"^\|\s*\*\*Verified\*\*\s*\|(.*)\|\s*$", re.M)

# The front-matter parser used across this repo is hand-rolled and line-oriented
# (see build_index.parse_frontmatter). Edits here are line-oriented too: there is no
# YAML dependency in scripts/, and re-emitting through a dumper would reflow every
# page it touched.
FM_LINE_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")


def split_front_matter(text: str) -> tuple[list[str], str] | None:
    """([front-matter lines], rest) or None when the page has no usable front matter."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return text[4:end].splitlines(), text[end + 4:]


def read_fm(lines: list[str]) -> dict:
    fm = {}
    for line in lines:
        m = FM_LINE_RE.match(line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fm


def set_fm_key(lines: list[str], key: str, value: str, after: str | None = None) -> list[str]:
    """Set or insert `key: value`, preserving every other line byte-for-byte."""
    out = list(lines)
    for i, line in enumerate(out):
        m = FM_LINE_RE.match(line)
        if m and m.group(1) == key:
            out[i] = f"{key}: {value}"
            return out
    # Insert immediately after `after` when given, else append.
    if after:
        for i, line in enumerate(out):
            m = FM_LINE_RE.match(line)
            if m and m.group(1) == after:
                out.insert(i + 1, f"{key}: {value}")
                return out
    out.append(f"{key}: {value}")
    return out


def stamp_page(text: str, date: str) -> tuple[str, str] | None:
    """Return (new_text, reviewed_on) or None when the page must be left alone.

    `reviewed_on` is seeded from the page's existing `verified_on` the first time —
    that date IS when a model last looked, since until now only the agent ever wrote
    a stamp. It is never advanced here.
    """
    split = split_front_matter(text)
    if split is None:
        return None
    fm_lines, rest = split
    fm = read_fm(fm_lines)

    if fm.get("verification") != "works" or fm.get("security") != "cleared":
        return None
    if not VERIFIED_ROW_RE.search(rest):
        return None  # no table row to keep in sync; the agent owns this page

    reviewed = fm.get("reviewed_on") or fm.get("verified_on") or ""
    if not reviewed:
        return None  # cannot describe what the recheck is relative to

    note = NOTE_TEMPLATE.format(reviewed=reviewed)
    # The hand-rolled front-matter parser and Jekyll both choke on ": " inside an
    # unquoted note (VERIFIER_AGENT.md spells this out), so assert it rather than
    # trusting the template to stay safe under edits.
    assert ": " not in note, note

    fm_lines = set_fm_key(fm_lines, "verified_on", date)
    fm_lines = set_fm_key(fm_lines, "reviewed_on", reviewed, after="verified_on")
    fm_lines = set_fm_key(fm_lines, "verification_note", f'"{note}"', after="reviewed_on")

    def _row(m: re.Match) -> str:
        return f"| **Verified** | works · {date} (auto-recheck; reviewed {reviewed}) |"

    rest = VERIFIED_ROW_RE.sub(_row, rest, count=1)
    return "---\n" + "\n".join(fm_lines) + "\n---" + rest, reviewed


def run(liveness: Path, date: str, apply: bool, changelog_block: Path | None) -> int:
    try:
        data = json.loads(liveness.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 — must never fail the run
        print(f"note: could not read {liveness}: {e}", file=sys.stderr)
        return 0

    if data.get("budget", {}).get("degraded"):
        # A rate-limited or truncated prefetch cannot support a clean claim about
        # anything, so refuse the whole batch rather than stamping part of it.
        print("refusing to stamp: the liveness prefetch reported a degraded budget",
              file=sys.stderr)
        return 0

    eligible = [p for p in data.get("pages", [])
                if not p.get("needs_model") and p.get("verdict") == "clean"]
    stamped, skipped = [], []
    for p in eligible:
        path = REPO / p["path"]
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            skipped.append((p["slug"], "unreadable"))
            continue
        result = stamp_page(text, date)
        if result is None:
            skipped.append((p["slug"], "not stampable"))
            continue
        new_text, reviewed = result
        if new_text != text and apply:
            path.write_text(new_text, encoding="utf-8")
        stamped.append((p["slug"], reviewed))

    verb = "stamped" if apply else "would stamp"
    print(f"{verb} {len(stamped)} page(s) of {len(eligible)} eligible "
          f"({len(data.get('pages', []))} in batch); {len(skipped)} skipped")
    for slug, why in skipped:
        print(f"  skipped {slug}: {why} — leaving it for the model", file=sys.stderr)

    if changelog_block and stamped and apply:
        # The workflow's `awk` newest-block extractor still needs a top block on a
        # run where the agent was skipped entirely (Gate B).
        # Its own heading, not "### Verified": merged into the agent's block this
        # would otherwise read as two "Verified" sections for one run, and the
        # distinction between script-confirmed and model-reviewed is the point.
        body = [f"## {date}", "", "### Automated recheck",
                f"- Automated recheck: {len(stamped)} page(s) re-confirmed live and "
                f"unchanged by `scripts/check_liveness.py`; `verified_on` refreshed to "
                f"{date}. `reviewed_on` is unchanged on every one of them — no model "
                f"reviewed these pages this run.", ""]
        if skipped:
            body += [f"- {len(skipped)} eligible page(s) were left for a model: "
                     + ", ".join(f"`{s}` ({w})" for s, w in skipped[:8]), ""]
        changelog_block.parent.mkdir(parents=True, exist_ok=True)
        changelog_block.write_text("\n".join(body), encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--liveness", type=Path, required=True)
    ap.add_argument("--date", required=True, help="run's UTC date, YYYY-MM-DD")
    ap.add_argument("--apply", action="store_true",
                    help="actually write. Without this, reports and changes nothing.")
    ap.add_argument("--changelog-block", type=Path, default=None)
    args = ap.parse_args()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        print(f"error: --date must be YYYY-MM-DD, got {args.date!r}", file=sys.stderr)
        return 0
    return run(args.liveness, args.date, args.apply, args.changelog_block)


if __name__ == "__main__":
    raise SystemExit(main())
