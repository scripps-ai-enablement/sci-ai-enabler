#!/usr/bin/env python3
"""Tests for the Verifier worklist selector (scripts/select_verify_targets.py).

The selector must not re-serve the identical batch when the whole catalog shares
one `verified_on` — that stalled the Monday verify run for 5 consecutive runs
(same 25 slugs, 422 pages never re-verified). These tests pin the rotation that
advances the served window, and confirm the plain ordering (unstamped-first,
oldest-first, alphabetical) and full-coverage tiling.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "select_verify_targets.py"

_spec = importlib.util.spec_from_file_location("select_verify_targets", SCRIPT)
sv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sv)


def _page(verification: str = "works", date: str = "2026-07-20") -> str:
    body = "---\n"
    if verification:
        body += f"verification: {verification}\n"
        body += f"verified_on: {date}\n"
    body += "title: X\n---\n\n# X\n"
    return body


class Ordering(unittest.TestCase):
    def _dir(self, stamped_n=6, unstamped=()):
        d = Path(tempfile.mkdtemp(prefix="wl_"))
        (d / "index.md").write_text("index", encoding="utf-8")  # must be skipped
        for i in range(stamped_n):
            (d / f"s{i:02d}.md").write_text(_page(), encoding="utf-8")
        for name in unstamped:
            (d / f"{name}.md").write_text(_page(verification=""), encoding="utf-8")
        return d

    def test_index_skipped_and_default_is_alphabetical(self):
        d = self._dir(stamped_n=4)
        slugs = [r["slug"] for r in sv.worklist(d)]
        self.assertEqual(slugs, ["s00", "s01", "s02", "s03"])
        self.assertNotIn("index", slugs)

    def test_unstamped_first_and_never_rotated(self):
        d = self._dir(stamped_n=4, unstamped=["aaa", "zzz"])
        for offset in (0, 1, 3, 10):
            slugs = [r["slug"] for r in sv.worklist(d, offset)]
            with self.subTest(offset=offset):
                self.assertEqual(slugs[:2], ["aaa", "zzz"])  # unstamped, stable order

    def test_rotation_advances_window(self):
        d = self._dir(stamped_n=6)
        base = [r["slug"] for r in sv.worklist(d, 0)]
        self.assertEqual(base, [f"s{i:02d}" for i in range(6)])
        # offset left-rotates the single same-date group.
        rot2 = [r["slug"] for r in sv.worklist(d, 2)]
        self.assertEqual(rot2, ["s02", "s03", "s04", "s05", "s00", "s01"])

    def test_windows_tile_full_catalog_over_runs(self):
        # With N=7 pages and count=3, run r uses offset = r*count. The union of
        # the top-`count` windows across runs must cover every page (no starvation).
        #
        # NOTE: production no longer relies on rotation to advance the window —
        # `verify.yml` passes --max-age-days, and a page that gets stamped simply
        # drops out of the due set (see Staleness below). Rotation is kept as a
        # safety valve for --max-age-days 0 / omitted; these two tests pin it.
        d = self._dir(stamped_n=7)
        count, n = 3, 7
        seen = set()
        for run in range(0, (n // count) + 1 + 1):
            batch = [r["slug"] for r in sv.worklist(d, run * count)][:count]
            seen.update(batch)
        self.assertEqual(seen, {f"s{i:02d}" for i in range(7)})

    def test_same_page_not_reserved_run_over_run(self):
        # The actual regression: consecutive runs must not serve the same batch.
        d = self._dir(stamped_n=10)
        count = 3
        b0 = [r["slug"] for r in sv.worklist(d, 0 * count)][:count]
        b1 = [r["slug"] for r in sv.worklist(d, 1 * count)][:count]
        b2 = [r["slug"] for r in sv.worklist(d, 2 * count)][:count]
        self.assertNotEqual(b0, b1)
        self.assertNotEqual(b1, b2)


class Staleness(unittest.TestCase):
    """The --max-age-days gate: a page verified inside the window is not served.

    This is what makes a Verifier run with nothing stale cost zero tokens —
    `verify.yml`'s Gate A skips the Claude step when the batch is empty.
    """

    def _rows(self, dates, unstamped=0):
        """Build worklist-shaped rows directly; `due()` is pure and takes rows."""
        rows = [
            {"slug": f"s{i:02d}", "path": f"catalog/tools/s{i:02d}.md",
             "verification": "works", "verified_on": d, "stamped": True}
            for i, d in enumerate(dates)
        ]
        rows += [
            {"slug": f"u{i:02d}", "path": f"catalog/tools/u{i:02d}.md",
             "verification": "", "verified_on": "", "stamped": False}
            for i in range(unstamped)
        ]
        return rows

    def test_max_age_days_excludes_fresh(self):
        rows = self._rows(["2026-07-29", "2026-06-28"])  # fresh, 31 days old
        got = [r["slug"] for r in sv.due(rows, "2026-07-29", 30)]
        self.assertEqual(got, ["s01"])

    def test_boundary_is_inclusive_at_exactly_n_days(self):
        # Exactly N days old is due; one day younger is not.
        rows = self._rows(["2026-06-29", "2026-06-30"])
        got = [r["slug"] for r in sv.due(rows, "2026-07-29", 30)]
        self.assertEqual(got, ["s00"])

    def test_empty_when_all_fresh(self):
        # Backs Gate A. Without this, a regression silently pays for a full run.
        rows = self._rows(["2026-07-29"] * 25)
        self.assertEqual(sv.due(rows, "2026-07-29", 30), [])

    def test_unstamped_always_due(self):
        rows = self._rows(["2026-07-29"], unstamped=2)
        got = [r["slug"] for r in sv.due(rows, "2026-07-29", 30)]
        self.assertEqual(got, ["u00", "u01"])

    def test_malformed_verified_on_is_due(self):
        # A page whose freshness cannot be established must be re-checked, and
        # nothing may raise.
        rows = self._rows(["soon", "2026-13-99", "", "2026-07-29"])
        got = [r["slug"] for r in sv.due(rows, "2026-07-29", 30)]
        self.assertEqual(got, ["s00", "s01", "s02"])

    def test_none_reproduces_current_behavior(self):
        rows = self._rows(["2026-07-29", "2026-01-01"], unstamped=1)
        self.assertEqual(sv.due(rows, "2026-07-29", None), rows)

    def test_zero_forces_everything_including_today(self):
        rows = self._rows(["2026-07-29", "2026-01-01"])
        got = [r["slug"] for r in sv.due(rows, "2026-07-29", 0)]
        self.assertEqual(got, ["s00", "s01"])

    def test_unusable_today_does_not_drop_the_batch(self):
        rows = self._rows(["2026-07-29", "2026-01-01"])
        self.assertEqual(sv.due(rows, "not-a-date", 30), rows)

    def test_due_set_fully_covered_within_a_cycle(self):
        # The staleness analogue of test_windows_tile_full_catalog_over_runs, and
        # the direct guard against the rotation/staleness double-skip: stamping a
        # served page must retire it, so successive runs tile the catalog with
        # offset 0 and no page is skipped or served twice.
        dates = {f"s{i:02d}": "2026-06-01" for i in range(10)}
        count, today, seen = 3, "2026-07-29", []
        for _ in range(4):
            rows = self._rows([])
            rows = [
                {"slug": s, "path": f"catalog/tools/{s}.md", "verification": "works",
                 "verified_on": d, "stamped": True}
                for s, d in sorted(dates.items())
            ]
            batch = sv.due(rows, today, 30)[:count]
            seen.extend(r["slug"] for r in batch)
            for r in batch:  # the run stamps what it served
                dates[r["slug"]] = today
        self.assertEqual(sorted(seen), [f"s{i:02d}" for i in range(10)])
        self.assertEqual(len(seen), len(set(seen)))  # nothing served twice


if __name__ == "__main__":
    unittest.main()
