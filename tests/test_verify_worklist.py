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


if __name__ == "__main__":
    unittest.main()
