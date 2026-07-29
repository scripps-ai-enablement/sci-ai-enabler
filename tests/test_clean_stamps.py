#!/usr/bin/env python3
"""Tests for scripts/apply_clean_stamps.py.

`test_never_writes_reviewed_on` is the load-bearing one. The whole integrity
argument for letting a script write `verified_on` is that `reviewed_on` stays put,
so `verified_on > reviewed_on` reliably means "a script confirmed nothing moved"
rather than "a model reviewed this". Without that test the distinction is decorative.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "apply_clean_stamps.py"

_spec = importlib.util.spec_from_file_location("apply_clean_stamps", SCRIPT)
acs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(acs)


def _page(verification="works", security="cleared", verified_on="2026-07-20",
          reviewed_on=None, row=True, front_matter=True, note=None):
    fm = ["title: Thing", "tool_type: Claude Skill", "supplier: Org",
          f"verification: {verification}", f"verified_on: {verified_on}"]
    if reviewed_on:
        fm.append(f"reviewed_on: {reviewed_on}")
    if note:
        fm.append(f'verification_note: "{note}"')
    fm += [f"security: {security}", f"security_on: {verified_on}",
           'security_note: "provenance matches, MIT, no advisories"',
           "summary: A thing."]
    body = "\n# Thing\n\n| | |\n|---|---|\n| **Capabilities** | x |\n"
    if row:
        body += f"| **Verified** | {verification} · {verified_on} |\n"
    body += f"| **Security** | {security} · {verified_on} — fine |\n\n## How to install\n\n`pip install thing`\n"
    if not front_matter:
        return body
    return "---\n" + "\n".join(fm) + "\n---" + body


class StampPage(unittest.TestCase):
    def test_stamps_works_cleared(self):
        out, reviewed = acs.stamp_page(_page(), "2026-08-19")
        self.assertIn("verified_on: 2026-08-19", out)
        self.assertEqual(reviewed, "2026-07-20")
        self.assertIn("| **Verified** | works · 2026-08-19 (auto-recheck; reviewed 2026-07-20) |", out)

    def test_never_writes_reviewed_on(self):
        # THE integrity invariant. reviewed_on is seeded once from the page's
        # existing verified_on and never advanced by this script.
        out, _ = acs.stamp_page(_page(verified_on="2026-07-20"), "2026-08-19")
        self.assertIn("reviewed_on: 2026-07-20", out)
        self.assertNotIn("reviewed_on: 2026-08-19", out)
        # And on a page that already carries one, it is preserved untouched.
        out2, reviewed = acs.stamp_page(
            _page(verified_on="2026-08-01", reviewed_on="2026-06-01"), "2026-09-01")
        self.assertEqual(reviewed, "2026-06-01")
        self.assertIn("reviewed_on: 2026-06-01", out2)
        self.assertIn("verified_on: 2026-09-01", out2)

    def test_refuses_non_works_or_non_cleared(self):
        for v, s in [("degraded", "cleared"), ("broken", "caution"),
                     ("works", "caution"), ("works", "unknown")]:
            with self.subTest(v=v, s=s):
                self.assertIsNone(acs.stamp_page(_page(verification=v, security=s),
                                                 "2026-08-19"))

    def test_refuses_page_with_no_front_matter(self):
        self.assertIsNone(acs.stamp_page(_page(front_matter=False), "2026-08-19"))

    def test_refuses_page_with_unterminated_front_matter(self):
        self.assertIsNone(acs.stamp_page("---\ntitle: x\nverification: works\n", "2026-08-19"))

    def test_refuses_page_with_no_verified_table_row(self):
        self.assertIsNone(acs.stamp_page(_page(row=False), "2026-08-19"))

    def test_refuses_page_with_no_date_to_anchor_the_recheck(self):
        self.assertIsNone(acs.stamp_page(_page(verified_on=""), "2026-08-19"))

    def test_note_contains_no_colon_space(self):
        # VERIFIER_AGENT.md: a note containing ": " breaks the hand-rolled
        # front-matter parser and Jekyll's YAML.
        out, _ = acs.stamp_page(_page(), "2026-08-19")
        note = [l for l in out.splitlines() if l.startswith("verification_note:")][0]
        self.assertNotIn(": ", note[len("verification_note:"):].strip().strip('"'))

    def test_front_matter_and_table_row_stay_in_sync(self):
        out, _ = acs.stamp_page(_page(), "2026-08-19")
        self.assertIn("verified_on: 2026-08-19", out)
        self.assertIn("· 2026-08-19 (auto-recheck", out)

    def test_only_the_verified_row_is_rewritten(self):
        out, _ = acs.stamp_page(_page(), "2026-08-19")
        self.assertIn("| **Security** | cleared · 2026-07-20 — fine |", out)
        self.assertIn("| **Capabilities** | x |", out)

    def test_unrelated_front_matter_is_byte_preserved(self):
        src = _page()
        out, _ = acs.stamp_page(src, "2026-08-19")
        for line in ("title: Thing", "tool_type: Claude Skill", "supplier: Org",
                     "summary: A thing."):
            self.assertIn(line, out)

    def test_idempotent(self):
        once, _ = acs.stamp_page(_page(), "2026-08-19")
        twice, _ = acs.stamp_page(once, "2026-08-19")
        self.assertEqual(once, twice)

    def test_second_recheck_keeps_the_original_review_date(self):
        first, _ = acs.stamp_page(_page(verified_on="2026-07-20"), "2026-08-19")
        second, reviewed = acs.stamp_page(first, "2026-09-18")
        self.assertEqual(reviewed, "2026-07-20")
        self.assertIn("verified_on: 2026-09-18", second)
        self.assertIn("reviewed_on: 2026-07-20", second)


class RunHarness(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp(prefix="acs_"))
        self.tools = self.d / "catalog" / "tools"
        self.tools.mkdir(parents=True)
        self._real_repo = acs.REPO
        acs.REPO = self.d

    def tearDown(self):
        acs.REPO = self._real_repo

    def _liveness(self, pages, degraded=False):
        p = self.d / "liveness.json"
        p.write_text(json.dumps({
            "budget": {"degraded": degraded},
            "pages": pages,
        }), encoding="utf-8")
        return p

    def _page_file(self, slug, **kw):
        (self.tools / f"{slug}.md").write_text(_page(**kw), encoding="utf-8")
        return {"slug": slug, "path": f"catalog/tools/{slug}.md",
                "needs_model": False, "verdict": "clean"}

    def test_dry_run_is_the_default_and_writes_nothing(self):
        row = self._page_file("a")
        before = (self.tools / "a.md").read_text()
        acs.run(self._liveness([row]), "2026-08-19", apply=False, changelog_block=None)
        self.assertEqual((self.tools / "a.md").read_text(), before)

    def test_apply_writes(self):
        row = self._page_file("a")
        acs.run(self._liveness([row]), "2026-08-19", apply=True, changelog_block=None)
        self.assertIn("verified_on: 2026-08-19", (self.tools / "a.md").read_text())

    def test_skips_pages_the_prefetch_flagged(self):
        row = self._page_file("a")
        row["needs_model"] = True
        acs.run(self._liveness([row]), "2026-08-19", apply=True, changelog_block=None)
        self.assertIn("verified_on: 2026-07-20", (self.tools / "a.md").read_text())

    def test_skips_non_clean_verdicts(self):
        row = self._page_file("a")
        row["verdict"] = "changed"
        acs.run(self._liveness([row]), "2026-08-19", apply=True, changelog_block=None)
        self.assertIn("verified_on: 2026-07-20", (self.tools / "a.md").read_text())

    def test_refuses_the_whole_batch_when_the_prefetch_was_degraded(self):
        # A rate-limited prefetch cannot support a clean claim about anything.
        row = self._page_file("a")
        acs.run(self._liveness([row], degraded=True), "2026-08-19",
                apply=True, changelog_block=None)
        self.assertIn("verified_on: 2026-07-20", (self.tools / "a.md").read_text())

    def test_unparseable_page_is_left_untouched_not_corrupted(self):
        (self.tools / "bad.md").write_text("---\ntitle: x\nverification: works\n",
                                           encoding="utf-8")
        before = (self.tools / "bad.md").read_text()
        row = {"slug": "bad", "path": "catalog/tools/bad.md",
               "needs_model": False, "verdict": "clean"}
        rc = acs.run(self._liveness([row]), "2026-08-19", apply=True, changelog_block=None)
        self.assertEqual(rc, 0)
        self.assertEqual((self.tools / "bad.md").read_text(), before)

    def test_missing_file_does_not_raise(self):
        row = {"slug": "gone", "path": "catalog/tools/gone.md",
               "needs_model": False, "verdict": "clean"}
        self.assertEqual(acs.run(self._liveness([row]), "2026-08-19",
                                 apply=True, changelog_block=None), 0)

    def test_unreadable_liveness_file_does_not_raise(self):
        self.assertEqual(acs.run(self.d / "nope.json", "2026-08-19",
                                 apply=True, changelog_block=None), 0)

    def test_changelog_block_is_written_and_says_no_model_reviewed(self):
        row = self._page_file("a")
        blk = self.d / "block.md"
        acs.run(self._liveness([row]), "2026-08-19", apply=True, changelog_block=blk)
        body = blk.read_text()
        self.assertTrue(body.startswith("## 2026-08-19"))
        self.assertIn("reviewed_on` is unchanged", body)
        self.assertIn("no model", body.lower())

    def test_no_changelog_block_on_a_dry_run(self):
        row = self._page_file("a")
        blk = self.d / "block.md"
        acs.run(self._liveness([row]), "2026-08-19", apply=False, changelog_block=blk)
        self.assertFalse(blk.exists())

    def test_changelog_block_is_a_single_dated_h2(self):
        # prepend_changelog.py rejects anything else.
        row = self._page_file("a")
        blk = self.d / "block.md"
        acs.run(self._liveness([row]), "2026-08-19", apply=True, changelog_block=blk)
        body = blk.read_text()
        self.assertEqual(sum(1 for l in body.splitlines() if l.startswith("## ")), 1)


class RealCatalogEligibility(unittest.TestCase):
    """How much of the live catalog phase 1 would touch, and what it must not."""

    def test_eligibility_is_narrow_and_excludes_every_open_problem(self):
        tools = [p for p in (REPO / "catalog" / "tools").glob("*.md")
                 if p.name != "index.md"]
        if not tools:
            self.skipTest("no catalog in this checkout")
        stampable, degraded_or_broken, caution = 0, 0, 0
        for p in tools:
            text = p.read_text(encoding="utf-8")
            split = acs.split_front_matter(text)
            fm = acs.read_fm(split[0]) if split else {}
            v, s = fm.get("verification"), fm.get("security")
            if v in ("degraded", "broken"):
                degraded_or_broken += 1
            if s == "caution":
                caution += 1
            if acs.stamp_page(text, "2026-08-19") is not None:
                stampable += 1
        # Every page with an open problem must be ineligible.
        for p in tools:
            text = p.read_text(encoding="utf-8")
            split = acs.split_front_matter(text)
            fm = acs.read_fm(split[0]) if split else {}
            if fm.get("verification") in ("degraded", "broken") or fm.get("security") != "cleared":
                with self.subTest(page=p.name):
                    self.assertIsNone(acs.stamp_page(text, "2026-08-19"))
        self.assertGreater(stampable, 0)
        self.assertLess(stampable, len(tools),
                        "phase 1 must not be eligible for the entire catalog")


if __name__ == "__main__":
    unittest.main()
