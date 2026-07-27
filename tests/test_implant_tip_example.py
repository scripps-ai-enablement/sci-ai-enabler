#!/usr/bin/env python3
"""Tests for the implant-tip-localization reference artifact.

Mirrors `tests/test_reproducible_example.py`: the bundle must replay
deterministically, hash its own inputs and outputs, and pin its live environment
exactly. On top of that this suite pins the thing that actually goes wrong in
this workflow — the pixel→atlas transform.

QuickNII/DeepSlice anchoring is `[ox,oy,oz, ux,uy,uz, vx,vy,vz]` and the transform
is `O + (x/width)*U + (y/height)*V`, dividing by `width`, NOT `width-1`. An
off-by-one there produces coordinates that look plausible and are wrong, with no
error raised, so it is asserted directly against a fixture whose answer is
checkable by hand (and against the canonical PyNutil implementation's formula).

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUNDLE = REPO / "recipes" / "examples" / "implant-tip-localization"
SCRIPT = BUNDLE / "localize_tips.py"

_spec = importlib.util.spec_from_file_location("localize_tips", SCRIPT)
lt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lt)


def _run(outdir: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--offline", "--target", "TGT",
         "--outdir", str(outdir), *extra],
        capture_output=True, text=True, cwd=BUNDLE,
    )


def _rows(outdir: Path) -> list[dict]:
    with (outdir / "placements.csv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


class TestTransform(unittest.TestCase):
    """The arithmetic. This is the test that earns the bundle's existence."""

    ANCHOR = [0.0, 0.0, 0.0, 8.0, 0.0, 0.0, 0.0, 8.0, 0.0]

    def test_matches_the_canonical_formula(self):
        # O + (x/width)*U + (y/height)*V, per PyNutil transform_to_atlas_space.
        got = lt.pixel_to_atlas(self.ANCHOR, 100, 80, 25, 40)
        self.assertAlmostEqual(got[0], 8 * 25 / 100)   # 2.0
        self.assertAlmostEqual(got[1], 8 * 40 / 80)    # 4.0
        self.assertAlmostEqual(got[2], 0.0)

    def test_divides_by_width_not_width_minus_one(self):
        """The off-by-one that silently shifts every coordinate.

        Both conventions agree at x=0 and at the far edge, so the discriminating
        case is an interior pixel: with width=100 and |U|=8, x=50 must give 4.0
        (x/width), never 4.0404 (x/(width-1)).
        """
        got = lt.pixel_to_atlas(self.ANCHOR, 100, 80, 50, 40)
        self.assertAlmostEqual(got[0], 8 * 50 / 100, msg="x/width convention broken")
        self.assertNotAlmostEqual(got[0], 8 * 50 / 99, places=3,
                                  msg="divided by width-1")
        self.assertAlmostEqual(got[1], 8 * 40 / 80, msg="y/height convention broken")
        self.assertNotAlmostEqual(got[1], 8 * 40 / 79, places=3,
                                  msg="divided by height-1")
        # And the far edge maps exactly onto O + U + V.
        edge = lt.pixel_to_atlas(self.ANCHOR, 100, 80, 100, 80)
        self.assertAlmostEqual(edge[0], 8.0)
        self.assertAlmostEqual(edge[1], 8.0)

    def test_origin_maps_to_o(self):
        anchor = [3.0, -2.0, 5.0, 8.0, 0.0, 0.0, 0.0, 8.0, 0.0]
        self.assertEqual(lt.pixel_to_atlas(anchor, 100, 80, 0, 0), (3.0, -2.0, 5.0))

    def test_oblique_anchoring_uses_both_vectors(self):
        """An off-axis plane is the whole reason DeepSlice is load-bearing."""
        anchor = [0.0, 0.0, 0.0, 8.0, 1.0, 0.0, 0.0, 8.0, 2.0]
        got = lt.pixel_to_atlas(anchor, 100, 80, 50, 40)
        self.assertAlmostEqual(got[0], 4.0)          # 0.5*8
        self.assertAlmostEqual(got[1], 0.5 + 4.0)    # 0.5*1 + 0.5*8
        self.assertAlmostEqual(got[2], 1.0)          # 0.5*2

    def test_rejects_malformed_input(self):
        with self.assertRaises(ValueError):
            lt.pixel_to_atlas(self.ANCHOR, 0, 80, 1, 1)
        with self.assertRaises(ValueError):
            lt.pixel_to_atlas([0, 0, 0], 100, 80, 1, 1)


class TestScientificGroundTruth(unittest.TestCase):
    """The fixture's answers are derivable by hand; assert the derived values."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="implant_")
        cls.out = Path(cls.tmp) / "results"
        cls.proc = _run(cls.out)
        assert cls.proc.returncode == 0, cls.proc.stderr
        cls.rows = _rows(cls.out)

    def test_three_tips_three_distinct_verdicts(self):
        self.assertEqual([r["verdict"] for r in self.rows],
                         ["hit", "miss", "marginal"])

    def test_clean_hit(self):
        r = self.rows[0]
        self.assertEqual((r["x_px"], r["acronym"]), ("25", "TGT"))
        self.assertAlmostEqual(float(r["ap"]), 2.0)      # 8*25/100
        self.assertAlmostEqual(float(r["margin_um"]), 50.0)

    def test_clean_miss_lands_in_the_neighbour(self):
        r = self.rows[1]
        self.assertEqual((r["x_px"], r["acronym"]), ("75", "NBR"))
        self.assertAlmostEqual(float(r["ap"]), 6.0)      # 8*75/100

    def test_marginal_is_reported_not_called(self):
        """x=48 -> ap=3.84, boundary at ap=4 -> 0.16 voxel * 25um = 4um.

        Inside the plane-prediction AP error, so it must NOT be a clean hit even
        though the voxel it lands in is the target — that is the design
        constraint the requester asked for.
        """
        r = self.rows[2]
        self.assertAlmostEqual(float(r["ap"]), 3.84)
        self.assertAlmostEqual(float(r["margin_um"]), 4.0)
        self.assertEqual(r["acronym"], "TGT", "the voxel really is the target")
        self.assertEqual(r["verdict"], "marginal", "must not be reported a clean hit")

    def test_margin_threshold_is_honoured(self):
        """Lower the AP error below the margin and the marginal call becomes a hit."""
        out = Path(self.tmp) / "loose"
        proc = _run(out, "--ap-error-um", "1.0")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual([r["verdict"] for r in _rows(out)], ["hit", "miss", "hit"])


class TestReproducibility(unittest.TestCase):
    def test_reruns_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            pa, pb = Path(a) / "r", Path(b) / "r"
            self.assertEqual(_run(pa).returncode, 0)
            self.assertEqual(_run(pb).returncode, 0)
            for name in ("placements.csv", "provenance.json"):
                self.assertEqual((pa / name).read_bytes(), (pb / name).read_bytes(),
                                 f"{name} differs between runs")

    def test_no_wallclock_leaks_into_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "r"
            _run(out)
            prov = json.loads((out / "provenance.json").read_text())
            self.assertNotIn("run_date", prov, "a date leaked without --run-date")
            _run(Path(d) / "dated", "--run-date", "2026-07-27")
            prov2 = json.loads((Path(d) / "dated" / "provenance.json").read_text())
            self.assertEqual(prov2["run_date"], "2026-07-27")

    def test_provenance_hashes_match_the_files_on_disk(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "r"
            _run(out)
            prov = json.loads((out / "provenance.json").read_text())
            self.assertEqual(prov["inputs"]["tips_csv_sha256"],
                             lt.sha256_file(BUNDLE / "tips.csv"))
            self.assertEqual(prov["inputs"]["alignment_sha256"],
                             lt.sha256_file(BUNDLE / "fixtures" / "alignment.json"))
            self.assertEqual(prov["outputs"]["placements.csv_sha256"],
                             lt.sha256_file(out / "placements.csv"))

    def test_provenance_records_what_an_auditor_needs(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "r"
            _run(out)
            prov = json.loads((out / "provenance.json").read_text())
            for key in ("atlas", "atlas_orientation", "atlas_resolution_um",
                        "transform", "transform_reference", "ap_error_um", "mode"):
                self.assertIn(key, prov, f"provenance is missing {key}")
            self.assertIn("(x/width)", prov["transform"])
            self.assertEqual(prov["verdict_counts"],
                             {"hit": 1, "marginal": 1, "miss": 1})


class TestPinnedEnvironment(unittest.TestCase):
    def test_every_requirement_is_exactly_pinned(self):
        for line in (BUNDLE / "requirements.txt").read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            with self.subTest(line):
                self.assertIn("==", line, f"{line} is not ==pinned")

    def test_python_version_constraint_is_documented(self):
        """The gate that fails a tester in the first five minutes if unstated."""
        text = (BUNDLE / "requirements.txt").read_text()
        self.assertIn("3.11", text)
        self.assertIn("3.13", text)

    def test_copyleft_dependency_is_flagged(self):
        self.assertIn("GPL-3.0", (BUNDLE / "requirements.txt").read_text())

    def test_pins_match_the_recipe_dependencies_block(self):
        """The bundle and the recipe page must not drift apart."""
        spec = importlib.util.spec_from_file_location(
            "build_index", REPO / "scripts" / "build_index.py")
        bi = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bi)
        recipe = (REPO / "recipes" / "items"
                  / "localize-implant-tip-in-brain-atlas-subregion.md")
        block = bi.section_block(recipe.read_text(encoding="utf-8"), "Dependencies")
        recipe_pins = bi.dependency_pins(block)
        bundle_pins = {}
        for line in (BUNDLE / "requirements.txt").read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "==" in line:
                name, _, version = line.partition("==")
                bundle_pins[name] = version
        for pkg, version in recipe_pins.items():
            with self.subTest(pkg):
                self.assertIn(pkg, bundle_pins,
                              f"{pkg} is in the recipe but not requirements.txt")
                self.assertEqual(bundle_pins[pkg], version,
                                 f"{pkg} pin differs between recipe and bundle")


class TestWiredIntoTheRecipe(unittest.TestCase):
    def test_recipe_links_the_bundle(self):
        recipe = (REPO / "recipes" / "items"
                  / "localize-implant-tip-in-brain-atlas-subregion.md").read_text()
        self.assertIn("implant-tip-localization", recipe,
                      "the recipe does not point at its reference artifact")


if __name__ == "__main__":
    unittest.main()
