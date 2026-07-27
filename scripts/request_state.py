#!/usr/bin/env python3
"""Read and mutate the `## User requests (*)` sections of a `curator-state.md`.

The inbound-request lifecycle spans three sections in `recipes/curator-state.md`
and `catalog/curator-state.md`:

    ## User requests (open)             queued, not yet worked
    ## User requests (blocked)          worked, but waiting on something external
    ## User requests (closed this run)  terminal; the loop-closer comments + closes

`(blocked)` exists because a request can be correctly *understood* and still be
unanswerable — most often a recipe whose load-bearing components are not in
`catalog/tools/` yet. Before this section existed such a request was moved to
`(closed this run)` and the issue was closed as `completed`, which told the user
"done" when the truth was "can't yet" (issue #74, 2026-07-27). Leaving it in
`(open)` is not an alternative: the scheduled pass would redo the same analysis
and re-post it every run.

Entries are single markdown bullets:

    - [#74 @goodb 2026-07-27] queue: recipes | question="…" | issue=74 → <result>

with optional machine-readable fields anywhere in the line:

    outcome=shipped|already-covered|declined|blocked   what happened
    blocked-on=catalog:slug-a,slug-b                   what `(blocked)` waits on
    chain=N                                            automated hops taken so far
    via=recipes-block                                  a derived, chained entry

Every mutation is idempotent, so a caller that loses a push race can reset to
`origin/main`, re-apply, and retry without checking what it already did.

Pure standard library. Run `--help` for the CLI.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

OPEN = "open"
BLOCKED = "blocked"
CLOSED = "closed this run"
SECTIONS = (OPEN, BLOCKED, CLOSED)

_HEAD = "## User requests ({})"
_NONE = "_None._"


# --------------------------------------------------------------------------- #
# section access
# --------------------------------------------------------------------------- #

def _span(text: str, section: str) -> tuple[int, int] | None:
    """Byte span of `section`'s body (excluding its heading), or None if absent."""
    head = _HEAD.format(section)
    i = text.find(head)
    if i < 0:
        return None
    start = i + len(head)
    j = text.find("\n## ", start)
    return (start, len(text) if j < 0 else j)


def bullets(text: str, section: str) -> list[str]:
    """The entry bullets in `section`, in file order. `_None._` yields []."""
    span = _span(text, section)
    if span is None:
        return []
    return [ln.rstrip() for ln in text[span[0]:span[1]].splitlines()
            if ln.startswith("- ")]


def _write_section(text: str, section: str, lines: list[str]) -> str:
    """Replace `section`'s body with `lines` (or the `_None._` placeholder)."""
    span = _span(text, section)
    if span is None:
        raise KeyError(f"section '{_HEAD.format(section)}' not found")
    body = "\n\n" + ("\n".join(lines) if lines else _NONE) + "\n"
    return text[:span[0]] + body + text[span[1]:]


def ensure_sections(text: str) -> str:
    """Add any missing `## User requests (…)` section, in lifecycle order.

    Only `(blocked)` is realistically missing — it postdates the other two — so
    it is inserted immediately before `(closed this run)` to keep the file
    reading open → blocked → closed.
    """
    for section in SECTIONS:
        if _span(text, section) is not None:
            continue
        head = _HEAD.format(section)
        anchor = None
        if section == BLOCKED:
            anchor = text.find(_HEAD.format(CLOSED))
        if anchor is None or anchor < 0:
            raise KeyError(f"cannot place '{head}': no anchor section present")
        text = text[:anchor] + f"{head}\n\n{_NONE}\n\n" + text[anchor:]
    return text


# --------------------------------------------------------------------------- #
# entry parsing
# --------------------------------------------------------------------------- #

def issue_of(line: str) -> str | None:
    """The issue number a bullet belongs to, preferring the `[#NN` prefix."""
    m = re.search(r"\[#(\d+)\b", line)
    if m:
        return m.group(1)
    m = re.search(r"\bissue=(\d+)\b", line)
    return m.group(1) if m else None


def _field(line: str, name: str) -> str | None:
    m = re.search(rf"\b{re.escape(name)}=([^\s|]+)", line)
    return m.group(1) if m else None


def blocked_on(line: str) -> list[str]:
    """Catalog slugs named by `blocked-on=catalog:a,b`; [] if absent."""
    m = re.search(r"\bblocked-on=catalog:([^\s|]+)", line)
    if not m:
        return []
    return [s for s in (p.strip() for p in m.group(1).split(",")) if s]


def chain_of(line: str) -> int:
    raw = _field(line, "chain")
    try:
        return max(0, int(raw))
    except (TypeError, ValueError):
        return 0


def outcome_of(line: str) -> str | None:
    raw = _field(line, "outcome")
    return raw.strip(".,;").lower() if raw else None


def result_of(line: str) -> str:
    """The prose after the `→` marker; the whole bullet if there is none."""
    if "→" in line:
        return line.split("→", 1)[1].strip()
    return re.sub(r"^-\s*", "", line).strip()


def find(text: str, issue: str) -> tuple[str, str] | None:
    """Locate `issue`'s entry as (section, line). `(open)` wins ties."""
    for section in SECTIONS:
        for line in bullets(text, section):
            if issue_of(line) == issue:
                return (section, line)
    return None


def classify(text: str, issue: str) -> dict:
    """Everything a caller needs to decide what to do about `issue`.

    Always returns every key, including for `absent`. Callers pipe this through
    `jq -r` in `set -u` shell, where a missing key yields `null` and
    `.blocked_on | join(",")` dies with "Cannot iterate over null" — so the
    complete-record guarantee is load-bearing, not tidiness.
    """
    empty = {"status": "absent", "issue": issue, "section": None, "line": "",
             "result": "", "outcome": None, "blocked_on": [], "chain": 0,
             "via": None}
    hit = find(text, issue)
    if hit is None:
        return empty
    section, line = hit
    outcome = outcome_of(line)
    # `(blocked)` is the state; a stray `outcome=blocked` in `(closed this run)`
    # is honoured too, so a mislabelled entry cannot close the user's issue.
    status = BLOCKED if (section == BLOCKED or outcome == "blocked") else section
    return {
        "status": status,
        "issue": issue,
        "section": section,
        "line": line,
        "result": result_of(line),
        "outcome": outcome,
        "blocked_on": blocked_on(line),
        "chain": chain_of(line),
        "via": _field(line, "via"),
    }


# --------------------------------------------------------------------------- #
# mutations (all idempotent)
# --------------------------------------------------------------------------- #

def append(text: str, line: str, section: str = OPEN) -> tuple[str, bool]:
    """Add `line` to `section` unless an entry for that issue is already there."""
    line = line.rstrip()
    if not line.startswith("- "):
        line = "- " + line.lstrip("- ")
    issue = issue_of(line)
    existing = bullets(text, section)
    if line in existing:
        return (text, False)
    if issue is not None and any(issue_of(e) == issue for e in existing):
        return (text, False)
    return (_write_section(text, section, existing + [line]), True)


def move(text: str, issue: str, to: str, *, chain: int | None = None,
         note: str | None = None) -> tuple[str, bool]:
    """Move `issue`'s entry to `to`, optionally rewriting `chain=` / the result."""
    if to not in SECTIONS:
        raise ValueError(f"unknown section '{to}'")
    hit = find(text, issue)
    if hit is None:
        return (text, False)
    section, line = hit

    if chain is not None:
        line = (re.sub(r"\bchain=\d+", f"chain={chain}", line)
                if re.search(r"\bchain=\d+", line)
                else _insert_field(line, f"chain={chain}"))
    if note is not None:
        head = line.split("→", 1)[0].rstrip() if "→" in line else line
        # A new result note supersedes any earlier outcome claim, including one
        # written into the field head rather than the note. Without this, an
        # entry handed back to `(open)` keeps a stale `outcome=blocked` and
        # classify() reports it blocked forever — the request would never run.
        head = re.sub(r"\s*\|?\s*\boutcome=[^\s|]+", "", head).rstrip(" |")
        line = f"{head} → {note}"

    if section == to and line == hit[1]:
        return (text, False)

    text = _write_section(text, section,
                          [e for e in bullets(text, section) if issue_of(e) != issue])
    dest = [e for e in bullets(text, to) if issue_of(e) != issue]
    return (_write_section(text, to, dest + [line]), True)


def _insert_field(line: str, field: str) -> str:
    """Add `field` to the pipe-delimited head, before any `→ result`."""
    head, sep, tail = line.partition("→")
    head = head.rstrip()
    return f"{head} | {field}" + (f" {sep} {tail.lstrip()}" if sep else "")


def prune(text: str, issue: str, section: str = CLOSED) -> tuple[str, bool]:
    """Drop `issue`'s entry from `section`, restoring `_None._` if it empties."""
    kept = [e for e in bullets(text, section) if issue_of(e) != issue]
    if len(kept) == len(bullets(text, section)):
        return (text, False)
    return (_write_section(text, section, kept), True)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _apply(path: Path, fn) -> bool:
    text = path.read_text()
    new, changed = fn(ensure_sections(text))
    if new != text:
        path.write_text(new)
    return changed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command",
                    choices=["classify", "append", "move", "prune", "ensure-sections"])
    ap.add_argument("--state", required=True, type=Path)
    ap.add_argument("--issue")
    ap.add_argument("--line")
    ap.add_argument("--to", choices=list(SECTIONS))
    ap.add_argument("--section", choices=list(SECTIONS), default=CLOSED)
    ap.add_argument("--chain", type=int)
    ap.add_argument("--note")
    args = ap.parse_args(argv)

    if not args.state.exists():
        print(f"no such state file: {args.state}", file=sys.stderr)
        return 2

    if args.command == "classify":
        if not args.issue:
            ap.error("classify needs --issue")
        print(json.dumps(classify(ensure_sections(args.state.read_text()), args.issue)))
        return 0

    if args.command == "ensure-sections":
        _apply(args.state, lambda t: (t, False))
        return 0

    if args.command == "append":
        if not args.line:
            ap.error("append needs --line")
        changed = _apply(args.state,
                         lambda t: append(t, args.line, args.section or OPEN))
    elif args.command == "move":
        if not (args.issue and args.to):
            ap.error("move needs --issue and --to")
        changed = _apply(args.state, lambda t: move(t, args.issue, args.to,
                                                   chain=args.chain, note=args.note))
    else:  # prune
        if not args.issue:
            ap.error("prune needs --issue")
        changed = _apply(args.state, lambda t: prune(t, args.issue, args.section))

    print("changed" if changed else "no-change")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
