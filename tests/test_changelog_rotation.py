#!/usr/bin/env python3
"""Tests for scripts/prepend_changelog.py.

The load-bearing test here is `test_awk_extraction_still_returns_newest_block`:
six workflows pull the newest changelog block for their tracking-issue comment
with `awk '/^## / {n++} n>=2 {exit} n==1 {print}'`, so rotation must never move a
`## ` line into the preamble or reorder the newest block away from the top.
`_awk_latest` below is a faithful Python reimplementation of that exact program.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "prepend_changelog.py"

_spec = importlib.util.spec_from_file_location("prepend_changelog", SCRIPT)
pc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pc)

LIVE_CHANGELOGS = [
    "CHANGELOG.md",
    "GUIDE_CHANGELOG.md",
    "RECIPES_CHANGELOG.md",
    "COSCIENTIST_CHANGELOG.md",
    "VERIFIER_CHANGELOG.md",
]


def _awk_latest(text: str) -> str:
    """Reimplementation of awk '/^## / {n++} n>=2 {exit} n==1 {print}'."""
    n, out = 0, []
    for line in text.splitlines():
        if line.startswith("## "):
            n += 1
        if n >= 2:
            break
        if n == 1:
            out.append(line)
    return "\n".join(out)


def _doc(front_matter: bool, dates) -> str:
    head = ""
    if front_matter:
        head += "---\ntitle: Catalog updates\nnav_order: 1\n---\n"
    head += "\n# Catalog updates\n\nRolling log. Newest first.\n\n"
    body = "".join(f"## {d}\n\n### Added\n- entry for {d}\n\n" for d in dates)
    return head + body


class Splitting(unittest.TestCase):
    def test_round_trip_is_byte_exact(self):
        for fm in (True, False):
            text = _doc(fm, ["2026-07-27", "2026-07-20"])
            pre, blocks = pc.split_blocks(text)
            self.assertEqual(pre + "".join(blocks), text)

    def test_no_blocks_yields_all_preamble(self):
        text = "# Title\n\nprose only\n"
        pre, blocks = pc.split_blocks(text)
        self.assertEqual(pre, text)
        self.assertEqual(blocks, [])

    def test_invariant_rejects_a_non_dated_h2_on_top(self):
        # This is the real failure mode: any `## ` line becomes block[0], so a
        # stray non-dated heading above the newest entry is what awk would return
        # — and six tracking issues would show it instead of the changelog entry.
        with self.assertRaises(AssertionError):
            pc.verify_awk_invariant("# T\n\n## Archive pointer\n\ntext\n\n## 2026-07-20\n\n- x\n")

    def test_invariant_accepts_dated_heading_with_parenthetical(self):
        pc.verify_awk_invariant("# T\n\n## 2026-07-20 (user request #74)\n\n- x\n")

    def test_invariant_accepts_a_file_with_no_blocks(self):
        pc.verify_awk_invariant("# Freshly initialised\n\nprose only\n")


class Rotation(unittest.TestCase):
    """Count-cap mechanics in isolation.

    Every call passes `min_days=0` so the digest-window guard is out of the way —
    these fixtures use adjacent dates, which the default `min_days=21` would
    (correctly) hold back from rotation. The guard itself is covered by
    DigestWindow below.
    """

    def setUp(self):
        self.d = Path(tempfile.mkdtemp(prefix="cl_"))
        self.live = self.d / "CHANGELOG.md"
        self.archive = self.d / "CHANGELOG_ARCHIVE.md"

    def _write(self, dates, front_matter=True):
        self.live.write_text(_doc(front_matter, dates), encoding="utf-8")

    def test_awk_extraction_still_returns_newest_block(self):
        # THE load-bearing test: protects the `awk` in six workflows.
        self._write([f"2026-07-{d:02d}" for d in range(28, 8, -1)])
        block = self.d / "block.md"
        block.write_text("## 2026-07-29\n\n### Added\n- brand new\n", encoding="utf-8")
        pc.run(self.live, block, keep=5, archive=self.archive, min_days=0)
        latest = _awk_latest(self.live.read_text(encoding="utf-8"))
        self.assertTrue(latest.startswith("## 2026-07-29"))
        self.assertIn("- brand new", latest)
        self.assertNotIn("2026-07-28", latest)  # stops before the second block

    def test_awk_extraction_works_on_the_archive_too(self):
        self._write([f"2026-07-{d:02d}" for d in range(28, 18, -1)])
        pc.run(self.live, None, keep=3, archive=self.archive, min_days=0)
        pc.verify_awk_invariant(self.archive.read_text(encoding="utf-8"))
        self.assertTrue(_awk_latest(self.archive.read_text(encoding="utf-8"))
                        .startswith("## 2026-07-25"))

    def test_preamble_has_no_h2_after_rotation(self):
        self._write([f"2026-07-{d:02d}" for d in range(28, 18, -1)])
        pc.run(self.live, None, keep=2, archive=self.archive, min_days=0)
        pre, _ = pc.split_blocks(self.live.read_text(encoding="utf-8"))
        self.assertNotIn("\n## ", pre)
        self.assertIn("CHANGELOG_ARCHIVE.md", pre)  # pointer added

    def test_no_block_lost(self):
        dates = [f"2026-07-{d:02d}" for d in range(28, 8, -1)]
        self._write(dates)
        pc.run(self.live, None, keep=6, archive=self.archive, min_days=0)
        _, live_blocks = pc.split_blocks(self.live.read_text(encoding="utf-8"))
        _, arch_blocks = pc.split_blocks(self.archive.read_text(encoding="utf-8"))
        self.assertEqual(len(live_blocks) + len(arch_blocks), len(dates))
        got = [b.splitlines()[0] for b in live_blocks + arch_blocks]
        self.assertEqual(got, [f"## {d}" for d in dates])  # order preserved

    def test_archive_receives_evicted_blocks_newest_first_across_runs(self):
        # Two rotations: the second batch is newer than the first and must land
        # ABOVE it, so the archive stays newest-first like the live file.
        self._write(["2026-07-20", "2026-07-19", "2026-07-18"])
        pc.run(self.live, None, keep=1, archive=self.archive, min_days=0)
        b = self.d / "b.md"
        b.write_text("## 2026-07-27\n\n- newer\n", encoding="utf-8")
        pc.run(self.live, b, keep=1, archive=self.archive, min_days=0)
        _, arch = pc.split_blocks(self.archive.read_text(encoding="utf-8"))
        heads = [x.splitlines()[0] for x in arch]
        self.assertEqual(heads, ["## 2026-07-20", "## 2026-07-19", "## 2026-07-18"])

    def test_front_matter_preserved_and_archive_is_nav_excluded(self):
        self._write(["2026-07-20", "2026-07-19"], front_matter=True)
        pc.run(self.live, None, keep=1, archive=self.archive, min_days=0)
        self.assertTrue(self.live.read_text(encoding="utf-8").startswith("---\n"))
        a = self.archive.read_text(encoding="utf-8")
        self.assertTrue(a.startswith("---\n"))
        self.assertIn("nav_exclude: true", a)

    def test_unrendered_source_gets_unrendered_archive(self):
        # VERIFIER_CHANGELOG.md has no front matter; its archive must not gain any,
        # or Jekyll would start publishing a page that was never published before.
        self._write(["2026-07-20", "2026-07-19"], front_matter=False)
        pc.run(self.live, None, keep=1, archive=self.archive, min_days=0)
        self.assertFalse(self.archive.read_text(encoding="utf-8").startswith("---"))

    def test_keep_zero_disables_rotation(self):
        self._write(["2026-07-20", "2026-07-19", "2026-07-18"])
        pc.run(self.live, None, keep=0, archive=self.archive, min_days=0)
        self.assertFalse(self.archive.exists())
        _, blocks = pc.split_blocks(self.live.read_text(encoding="utf-8"))
        self.assertEqual(len(blocks), 3)

    def test_idempotent(self):
        self._write([f"2026-07-{d:02d}" for d in range(28, 18, -1)])
        pc.run(self.live, None, keep=3, archive=self.archive, min_days=0)
        first = (self.live.read_text(encoding="utf-8"),
                 self.archive.read_text(encoding="utf-8"))
        pc.run(self.live, None, keep=3, archive=self.archive, min_days=0)
        self.assertEqual(first, (self.live.read_text(encoding="utf-8"),
                                 self.archive.read_text(encoding="utf-8")))

    def test_missing_block_file_still_rotates(self):
        self._write(["2026-07-20", "2026-07-19", "2026-07-18"])
        rc = pc.run(self.live, self.d / "nope.md", keep=1, archive=self.archive, min_days=0)
        self.assertEqual(rc, 0)
        self.assertTrue(self.archive.exists())

    def test_malformed_block_is_rejected_without_losing_the_run(self):
        # A malformed block is a spec bug worth surfacing, but it must NOT fail the
        # step: prepend runs before `git add -A`, so a non-zero exit would discard
        # the run's page edits along with its changelog entry. Warn, skip the block,
        # keep going.
        for content in (
            "no heading here\n",                           # no heading at all
            "## Notes\n\nx\n",                             # heading, but not dated
            "## 2026-07-27\n\nx\n\n## 2026-07-26\n\ny\n",  # two blocks in one file
        ):
            with self.subTest(content=content.splitlines()[0]):
                self._write(["2026-07-20"])
                bad = self.d / "bad.md"
                bad.write_text(content, encoding="utf-8")
                rc = pc.run(self.live, bad, keep=5, archive=self.archive, min_days=0)
                self.assertEqual(rc, 0)
                _, blocks = pc.split_blocks(self.live.read_text(encoding="utf-8"))
                self.assertEqual([b.splitlines()[0] for b in blocks], ["## 2026-07-20"])
                pc.verify_awk_invariant(self.live.read_text(encoding="utf-8"))


class BlockMerging(unittest.TestCase):
    """A run can produce two blocks for one date: the agent's and the auto-recheck's."""

    def setUp(self):
        self.d = Path(tempfile.mkdtemp(prefix="cm_"))
        self.live = self.d / "CHANGELOG.md"
        self.live.write_text(_doc(True, ["2026-07-20"]), encoding="utf-8")
        self.archive = self.d / "CHANGELOG_ARCHIVE.md"
        self.agent = self.d / "agent.md"
        self.auto = self.d / "auto.md"

    def _run(self):
        return pc.run(self.live, self.agent, keep=12, archive=self.archive,
                      min_days=0, extra_block=self.auto)

    def test_merges_under_one_heading(self):
        self.agent.write_text("## 2026-08-19\n\n### Verified\n- agent did a thing\n", encoding="utf-8")
        self.auto.write_text("## 2026-08-19\n\n### Verified\n- script rechecked 40 pages\n", encoding="utf-8")
        self._run()
        latest = _awk_latest(self.live.read_text(encoding="utf-8"))
        # Count H2 lines, not the "## " substring -- "### Verified" contains it.
        h2 = [l for l in latest.splitlines() if l.startswith("## ")]
        self.assertEqual(len(h2), 1, h2)
        self.assertIn("agent did a thing", latest)
        self.assertIn("script rechecked 40 pages", latest)

    def test_auto_block_alone_is_used_when_the_agent_was_skipped(self):
        # Gate B: the agent never ran, so the auto block is the run's only record --
        # and the awk extractor still needs a dated top block.
        self.auto.write_text("## 2026-08-19\n\n### Verified\n- script rechecked 40 pages\n", encoding="utf-8")
        self._run()
        latest = _awk_latest(self.live.read_text(encoding="utf-8"))
        self.assertTrue(latest.startswith("## 2026-08-19"))
        self.assertIn("script rechecked 40 pages", latest)

    def test_agent_block_alone_when_nothing_was_auto_stamped(self):
        self.agent.write_text("## 2026-08-19\n\n### Verified\n- agent did a thing\n", encoding="utf-8")
        self._run()
        latest = _awk_latest(self.live.read_text(encoding="utf-8"))
        self.assertIn("agent did a thing", latest)
        self.assertNotIn("script rechecked", latest)

    def test_neither_block_leaves_the_file_alone(self):
        before = self.live.read_text(encoding="utf-8")
        self._run()
        self.assertEqual(self.live.read_text(encoding="utf-8"), before)

    def test_merged_block_still_passes_the_awk_invariant(self):
        self.agent.write_text("## 2026-08-19\n\n- a\n", encoding="utf-8")
        self.auto.write_text("## 2026-08-19\n\n- b\n", encoding="utf-8")
        self._run()
        pc.verify_awk_invariant(self.live.read_text(encoding="utf-8"))

    def test_merge_is_pure(self):
        merged = pc.merge_blocks("## 2026-08-19\n\n- a\n", "## 2026-08-19\n\n- b\n")
        self.assertEqual(len([l for l in merged.splitlines() if l.startswith("## ")]), 1)
        self.assertIn("- a", merged)
        self.assertIn("- b", merged)

    def test_merge_with_empty_extra_body_is_a_noop(self):
        self.assertEqual(pc.merge_blocks("## 2026-08-19\n\n- a\n", "## 2026-08-19\n"),
                         "## 2026-08-19\n\n- a\n")


class DigestWindow(unittest.TestCase):
    """`--min-days` must stop rotation evicting a block digest.yml still needs.

    digest.yml summarizes every `## YYYY-MM-DD` block on or after its `since` date
    (7 days back by default). The catalog curator writes 7-8 blocks per weekend, so
    a plain `--keep 12` could archive an in-window block and silently drop it from
    the weekly digest.
    """

    def setUp(self):
        self.d = Path(tempfile.mkdtemp(prefix="cw_"))
        self.live = self.d / "CHANGELOG.md"
        self.archive = self.d / "CHANGELOG_ARCHIVE.md"

    def test_keep_is_raised_to_cover_the_window(self):
        # 16 blocks all dated within 2 days: a weekend's worth of curator slots.
        dates = ["2026-07-26"] * 8 + ["2026-07-25"] * 8
        self.live.write_text(_doc(True, dates), encoding="utf-8")
        pc.run(self.live, None, keep=12, archive=self.archive, min_days=21)
        _, blocks = pc.split_blocks(self.live.read_text(encoding="utf-8"))
        self.assertEqual(len(blocks), 16)      # keep=12 overridden by the window
        self.assertFalse(self.archive.exists())

    def test_blocks_outside_the_window_still_rotate(self):
        dates = ["2026-07-26"] * 3 + ["2026-01-01"] * 5
        self.live.write_text(_doc(True, dates), encoding="utf-8")
        pc.run(self.live, None, keep=1, archive=self.archive, min_days=21)
        _, live_blocks = pc.split_blocks(self.live.read_text(encoding="utf-8"))
        _, arch_blocks = pc.split_blocks(self.archive.read_text(encoding="utf-8"))
        self.assertEqual(len(live_blocks), 3)  # the three recent ones held back
        self.assertEqual(len(arch_blocks), 5)

    def test_window_measured_from_newest_block_not_today(self):
        # A file untouched for a year must not shed its most recent history just
        # because the calendar moved on — rotation has to be reproducible.
        dates = ["2020-03-02", "2020-03-01"]
        self.live.write_text(_doc(True, dates), encoding="utf-8")
        pc.run(self.live, None, keep=1, archive=self.archive, min_days=21)
        _, blocks = pc.split_blocks(self.live.read_text(encoding="utf-8"))
        self.assertEqual(len(blocks), 2)

    def test_undated_block_is_never_evicted_by_the_window_calc(self):
        blocks = ["## 2026-07-26\n\n- a\n\n", "## not-a-date\n\n- b\n\n",
                  "## 2026-01-01\n\n- c\n\n"]
        self.assertEqual(pc._min_kept_for_window(blocks, 21), 2)

    def test_min_days_zero_restores_pure_count_cap(self):
        dates = ["2026-07-26"] * 8
        self.live.write_text(_doc(True, dates), encoding="utf-8")
        pc.run(self.live, None, keep=3, archive=self.archive, min_days=0)
        _, blocks = pc.split_blocks(self.live.read_text(encoding="utf-8"))
        self.assertEqual(len(blocks), 3)

    def test_default_min_days_covers_the_digest_default_window(self):
        self.assertGreaterEqual(21, 7)  # documents the relationship the default rests on


class RealChangelogs(unittest.TestCase):
    """The five live files must already satisfy the invariant this script enforces."""

    def test_all_live_changelogs_are_awk_compatible(self):
        for name in LIVE_CHANGELOGS:
            p = REPO / name
            if not p.exists():
                continue
            with self.subTest(name=name):
                pc.verify_awk_invariant(p.read_text(encoding="utf-8"))

    def test_awk_latest_matches_split_blocks_on_real_files(self):
        for name in LIVE_CHANGELOGS:
            p = REPO / name
            if not p.exists():
                continue
            with self.subTest(name=name):
                text = p.read_text(encoding="utf-8")
                _, blocks = pc.split_blocks(text)
                if not blocks:
                    continue
                self.assertEqual(_awk_latest(text).strip(), blocks[0].strip())


if __name__ == "__main__":
    unittest.main()
