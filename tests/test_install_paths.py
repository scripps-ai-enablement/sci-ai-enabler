#!/usr/bin/env python3
"""Tests that no page ships an install command through a channel known to be dead.

Why this exists
---------------
Ten recipe pages told scientists to run:

    /plugin marketplace add K-Dense-AI/claude-scientific-skills
    /plugin install pydeseq2@claude-scientific-skills

That marketplace has never existed — `K-Dense-AI/scientific-agent-skills` ships no
`.claude-plugin/marketplace.json`, so the command fails outright and nothing installs.
The repo already *knew*: `AGENT.md` says the marketplace does not exist, and
`scripts/ingest_kdense.py` strips exactly this pattern. But that ingester only
regenerates **catalog** pages, so the hand-authored **recipes** kept the dead command
for months, and one had to be fixed by hand (#41) after a reader hit the failure.

Nothing mechanical stood between an LLM-authored page and a reader running a command
that cannot work. `scripts/check_liveness.py` cannot fill that gap: by design it
"never fails the run" and only inspects a per-run worklist, so it advises the
Verifier rather than gating the corpus. These tests gate it, offline, on every PR.

The `DEAD_CHANNELS` registry below is the extension point. When a supplier retires an
install channel or renames a path, add one entry with the date and the reason, and
every page is checked from then on.

Scope note
----------
Only *commands* are checked — fenced code blocks and inline code spans. Prose is left
free deliberately, because the useful thing to write about a dead channel is that it
is dead; `AGENT.md` and the #41 changelog note both name this marketplace in order to
warn against it, and must keep being able to.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Changelogs are an append-only historical record: they quote commands that were
# correct when written, and rewriting them would falsify the audit trail.
SKIP_NAMES = re.compile(r"CHANGELOG(_ARCHIVE)?\.md$")

# Install channels that are known dead. Each entry: the literal string that must not
# appear in any command, and why — surfaced verbatim in the failure message so whoever
# trips it gets the fix, not just a rejection.
DEAD_CHANNELS = [
    (
        "claude-scientific-skills",
        "The `K-Dense-AI/claude-scientific-skills` plugin marketplace does not exist "
        "(the repo ships no .claude-plugin/marketplace.json), so `/plugin marketplace add` "
        "and `/plugin install <x>@claude-scientific-skills` both fail. Verified upstream "
        "2026-07-30. Use `npx skills add K-Dense-AI/scientific-agent-skills`, or a manual "
        "clone copying `skills/<slug>/` into `~/.claude/skills/`.",
    ),
    (
        "scientific-skills/",
        "Upstream K-Dense migrated `scientific-skills/` to `skills/`, so this path 404s. "
        "Reference `skills/<slug>/SKILL.md` instead. `scripts/ingest_kdense.py` performs "
        "this migration for catalog pages; recipes are hand-authored and must not "
        "reintroduce it.",
    ),
]

# Phrases that mark a mention as a deliberate warning rather than an instruction. A
# line carrying one of these may name a dead channel even inside code formatting.
WARNING_MARKERS = (
    "does not exist",
    "non-existent",
    "nonexistent",
    "no longer",
    "was wrong",
    "not a marketplace",
)


def pages() -> list[Path]:
    """Every tracked `.md`, minus the changelogs.

    Tracked, not globbed: an `rglob` also walks scratch copies that are not part
    of the corpus — a `.claude/worktrees/<name>/` checkout of an older commit
    reintroduces all 25 original offenders and fails the lint locally while CI,
    which has no such directory, stays green. Only what is committed ships.
    """
    proc = subprocess.run(["git", "ls-files", "-z", "*.md"],
                          cwd=REPO, capture_output=True, text=True)
    if proc.returncode != 0:
        raise unittest.SkipTest("git ls-files unavailable")
    return sorted(REPO / p for p in proc.stdout.split("\0")
                  if p and not SKIP_NAMES.search(p))


def command_lines(text: str) -> list[tuple[int, str]]:
    """Lines that a reader could plausibly execute: fenced blocks and inline code.

    Returns (1-indexed line number, line) so failures point at a real location.
    """
    out: list[tuple[int, str]] = []
    fenced = False
    for i, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            out.append((i, line))
        else:
            for span in re.findall(r"`([^`\n]+)`", line):
                # An inline span is a command only if it looks like one.
                if re.match(r"^\s*(/plugin|npx |git clone|pip install|cp -r|claude mcp)", span):
                    out.append((i, span))
    return out


class DeadInstallChannels(unittest.TestCase):
    def test_no_command_uses_a_dead_channel(self):
        failures = []
        for p in pages():
            text = p.read_text()
            for lineno, line in command_lines(text):
                if any(m in line.lower() for m in WARNING_MARKERS):
                    continue
                for needle, why in DEAD_CHANNELS:
                    if needle in line:
                        rel = p.relative_to(REPO)
                        failures.append(f"{rel}:{lineno}: {line.strip()}\n      -> {why}")
        self.assertEqual(
            failures,
            [],
            "Install command(s) route through a channel known to be dead:\n  "
            + "\n  ".join(failures),
        )

    def test_prose_may_still_warn_about_dead_channels(self):
        """The guard must not have made it impossible to document the breakage."""
        agent = (REPO / "AGENT.md").read_text()
        self.assertIn(
            "claude-scientific-skills",
            agent,
            "AGENT.md should keep warning that this marketplace does not exist",
        )
        # ...and that warning must not be picked up as a command.
        flagged = [
            line
            for _, line in command_lines(agent)
            if "claude-scientific-skills" in line
            and not any(m in line.lower() for m in WARNING_MARKERS)
        ]
        self.assertEqual(flagged, [], f"AGENT.md warning misread as a command: {flagged}")


class SkillSlugsAreGrounded(unittest.TestCase):
    """A recipe may only name a K-Dense skill the catalog actually carries.

    `AGENT.md`'s grounding rule is that a recommendation must resolve to a real
    catalog entry. For K-Dense skills that is checkable offline: every slug a recipe
    cites must have a catalog page. This is what would have caught a recipe inventing
    a plausible-sounding skill, and it needs no network, unlike upstream existence.
    """

    SLUG = re.compile(r"scientific-agent-skills/(?:blob/main/)?skills/([a-z0-9_-]+)")

    def catalog_slugs(self) -> set[str]:
        slugs: set[str] = set()
        for p in (REPO / "catalog" / "tools").glob("*.md"):
            text = p.read_text()
            if not re.search(r"^supplier:\s*K-Dense", text, re.M):
                continue
            slugs.add(p.stem)
            slugs.update(self.SLUG.findall(text))
        return slugs

    def test_every_recipe_skill_slug_has_a_catalog_page(self):
        known = self.catalog_slugs()
        self.assertTrue(known, "no K-Dense catalog pages found — locator is wrong")
        orphans = []
        for p in sorted((REPO / "recipes" / "items").glob("*.md")):
            for slug in sorted(set(self.SLUG.findall(p.read_text()))):
                if slug not in known:
                    orphans.append(f"{p.relative_to(REPO)} -> skills/{slug}")
        self.assertEqual(
            orphans,
            [],
            "Recipe cites a K-Dense skill with no catalog page (ungrounded, or a "
            "slug renamed upstream):\n  " + "\n  ".join(orphans),
        )


class CuratorInstructionsTeachTheLivePath(unittest.TestCase):
    """AGENT.md:142 taught the pre-migration path, seeding it into new recipes.

    Fixing the recipes without fixing the instruction would let the next authored
    recipe reintroduce it, which is how this drifted for months.
    """

    def test_agent_md_install_guidance_uses_migrated_path(self):
        for name in ("AGENT.md", "RECIPE_AGENT.md"):
            text = (REPO / name).read_text()
            for lineno, line in enumerate(text.splitlines(), start=1):
                if "scientific-skills/" not in line:
                    continue
                if any(m in line.lower() for m in WARNING_MARKERS):
                    continue
                self.fail(
                    f"{name}:{lineno} teaches the pre-migration K-Dense path; "
                    f"use `skills/<slug>/`:\n    {line.strip()}"
                )


if __name__ == "__main__":
    unittest.main()
