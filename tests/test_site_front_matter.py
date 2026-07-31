#!/usr/bin/env python3
"""Every page GitHub Pages renders must carry Jekyll front matter.

Why this exists
---------------
`_config.yml` publishes the whole repo except an explicit `exclude:` list, so a
new `.md` file is built as a page by default. A file with no front matter still
builds — it just has no `parent`/`nav_order`/`nav_exclude` to place or hide it,
so just-the-docs floats it into the top-level sidebar next to "Start here" and
"Recipes". Nothing errors; the nav just quietly grows a stray entry.

That has happened repeatedly, because the agents that write these files (the
curators, the verifier, the recipe agent) are told about the file's content, not
about the site build. As of 2026-07-31 it had leaked `VERIFIER_AGENT.md`, both
verifier changelogs, and a reproducible-example README into the main index. This
test turns that silent leak into a CI failure at the moment the file lands.

Three rules, matching the three legitimate dispositions for a new `.md`:

  1. A rendered page starts with `---` on line 1. (A leading blank line breaks
     front-matter detection just as thoroughly as having none — that is exactly
     how VERIFIER_CHANGELOG_ARCHIVE.md was broken.)
  2. A rendered page declares a non-empty `title:`, which is what the sidebar and
     the search index show.
  3. An agent spec (`*_AGENT.md`) is internal, never a page, so it belongs in
     `_config.yml`'s `exclude:` list.

Anything genuinely internal goes in `exclude:`; anything rendered but not wanted
in the nav gets `nav_exclude: true`.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "_config.yml"

EXCLUDE_BLOCK_RE = re.compile(r"^exclude:\n((?:[ \t]*-[ \t]+.*\n)+)", re.M)
FRONT_MATTER_END_RE = re.compile(r"^---[ \t]*$", re.M)
TITLE_RE = re.compile(r"^title:[ \t]*\S", re.M)


def excluded_paths() -> list[str]:
    """The `exclude:` entries from _config.yml, without a YAML dependency.

    Only ever a flat list of quoted-or-bare scalars, so a line parser is enough
    and keeps this test stdlib-only like the rest of the suite.
    """
    m = EXCLUDE_BLOCK_RE.search(CONFIG.read_text(encoding="utf-8"))
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        entry = re.sub(r"^[ \t]*-[ \t]+", "", line).strip().strip("'\"")
        if entry:
            out.append(entry.rstrip("/"))
    return out


def is_rendered(path: str, exclude: list[str]) -> bool:
    """Would Jekyll build this repo-relative path into a page?"""
    # Jekyll ignores any entry whose name starts with `.` or `_` (so `.github/`,
    # `.claude/`, `_sass/`, `_includes/` need no `exclude:` entry of their own).
    if any(part.startswith((".", "_")) for part in path.split("/")):
        return False
    return not any(path == e or path.startswith(e + "/") for e in exclude)


def front_matter(text: str) -> str | None:
    """The front-matter body, or None when the file has no usable front matter."""
    if not text.startswith("---\n"):
        return None
    end = FRONT_MATTER_END_RE.search(text, 4)
    return None if end is None else text[4:end.start()]


def tracked_markdown() -> list[str]:
    """Every tracked `.md` path. Tracked, not globbed: untracked scratch files
    are not deployed, and a worktree under .claude/ must not fail the suite."""
    proc = subprocess.run(["git", "ls-files", "-z", "*.md"],
                          cwd=REPO, capture_output=True, text=True)
    if proc.returncode != 0:
        raise unittest.SkipTest("git ls-files unavailable")
    return [p for p in proc.stdout.split("\0") if p]


class RenderedPagesHaveFrontMatter(unittest.TestCase):
    def setUp(self):
        self.exclude = excluded_paths()
        # A parse failure here would silently make every assertion below vacuous
        # (or fail every file at once), so pin the shape of what we parsed.
        self.assertIn("README.md", self.exclude,
                      "could not parse `exclude:` out of _config.yml")
        self.pages = [p for p in tracked_markdown()
                      if is_rendered(p, self.exclude)]
        self.assertGreater(len(self.pages), 100,
                           "suspiciously few rendered pages — check the parser")

    def test_every_rendered_page_starts_with_front_matter(self):
        for path in self.pages:
            with self.subTest(path=path):
                text = (REPO / path).read_text(encoding="utf-8")
                self.assertIsNotNone(
                    front_matter(text),
                    f"{path} is built as a site page but has no Jekyll front "
                    f"matter (it must start with `---` on line 1, no leading "
                    f"blank line), so just-the-docs will drop it into the "
                    f"top-level nav. Give it front matter, or add it to "
                    f"`exclude:` in _config.yml if it is internal.",
                )

    def test_every_rendered_page_has_a_title(self):
        for path in self.pages:
            with self.subTest(path=path):
                fm = front_matter((REPO / path).read_text(encoding="utf-8"))
                if fm is None:
                    continue  # reported by the test above
                self.assertRegex(
                    fm, TITLE_RE,
                    f"{path} renders as a page but declares no `title:`, which "
                    f"is what the sidebar and search index display.",
                )


class AgentSpecsAreNotPublished(unittest.TestCase):
    """The `*_AGENT.md` specs are prompts for the automated curators, not pages.
    Each new agent adds one, and forgetting the `exclude:` line is how
    VERIFIER_AGENT.md ended up in the sidebar."""

    def test_agent_specs_are_excluded(self):
        exclude = excluded_paths()
        specs = [p for p in tracked_markdown()
                 if "/" not in p and p.endswith("_AGENT.md")]
        self.assertTrue(specs, "no *_AGENT.md specs found at the repo root")
        for spec in specs:
            with self.subTest(spec=spec):
                self.assertIn(
                    spec, exclude,
                    f"{spec} is an internal agent spec but is not in "
                    f"`exclude:` in _config.yml, so it will be published.",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
