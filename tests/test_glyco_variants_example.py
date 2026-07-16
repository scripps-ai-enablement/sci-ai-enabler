#!/usr/bin/env python3
"""End-to-end test of the glycosylation-variant reference artifact.

Mirrors tests/test_reproducible_example.py for the recipe
"Interpret variants that gain or lose glycosylation sites". Exercises the
reproducibility doctrine (committed code + pinned env + provenance that
reproduces) and locks in the demonstration's scientific ground truth:

  1. The offline replay is deterministic (two runs byte-identical) and matches
     the provenance-recorded output hash (the artifact verifies itself).
  2. The bundle ships what the doctrine requires (script, pinned requirements,
     provenance, README, fixtures).
  3. Every variant's computed class matches the `expected_class` ground-truth
     column in variants.csv — LOG, both GOG mechanisms, the `none` controls,
     and the `unmapped` numbering-harmonization guard.
  4. The headline finding holds: IFNGR2 T168N is a gain-of-glycosylation call
     that standard missense predictors miss (ClinVar Pathogenic, CADD < 20,
     PolyPhen benign).

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXAMPLE = REPO / "recipes" / "examples" / "glyco-variants"
SCRIPT = EXAMPLE / "glyco_variants.py"
VARIANTS = EXAMPLE / "variants.csv"
FIXTURES = EXAMPLE / "fixtures"

_spec = importlib.util.spec_from_file_location("glyco_variants", SCRIPT)
glyco = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(glyco)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_offline(outdir: Path) -> dict:
    return glyco.run(VARIANTS, FIXTURES, outdir, live=False, run_date=None)


def read_rows(outdir: Path) -> list[dict]:
    return list(csv.DictReader((outdir / "glyco_candidates.csv").open()))


class TestArtifactExists(unittest.TestCase):
    def test_bundle_is_complete(self):
        for p in (SCRIPT, VARIANTS, EXAMPLE / "requirements.txt", EXAMPLE / "README.md",
                  FIXTURES / "glygen" / "glycosylation_sites_P01008.json",
                  FIXTURES / "uniprot" / "P01008.fasta",
                  FIXTURES / "biomcp" / "P38484_T168N.json"):
            self.assertTrue(p.exists(), f"missing artifact file: {p}")

    def test_requirements_are_pinned(self):
        pinned = [ln for ln in (EXAMPLE / "requirements.txt").read_text().splitlines()
                  if ln.strip() and not ln.strip().startswith("#")]
        self.assertTrue(pinned, "requirements.txt has no dependency lines")
        for line in pinned:
            self.assertIn("==", line, f"dependency not pinned: {line!r}")


class TestReproducibility(unittest.TestCase):
    def test_two_runs_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a", Path(d) / "b"
            run_offline(a)
            run_offline(b)
            for name in ("glyco_candidates.csv", "provenance.json"):
                self.assertEqual(sha256(a / name), sha256(b / name),
                                 f"{name} differs between identical runs — not reproducible")

    def test_provenance_hash_matches_output(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            prov = run_offline(out)
            self.assertEqual(prov["outputs"]["glyco_candidates.csv"],
                             sha256(out / "glyco_candidates.csv"),
                             "provenance output hash does not match the emitted CSV")


class TestScientificGroundTruth(unittest.TestCase):
    def test_classes_match_expected(self):
        expected = {(r["uniprot"], r["protein_change"]): r["expected_class"]
                    for r in csv.DictReader(VARIANTS.open())}
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            for r in read_rows(out):
                key = (r["uniprot"], r["protein_change"])
                self.assertEqual(r["class"], expected[key],
                                 f"{r['gene']} {r['protein_change']}: got {r['class']}, expected {expected[key]}")

    def test_headline_finding_ifngr2_t168n(self):
        """The value case: a pathogenic GOG variant that predictors miss."""
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            row = next(r for r in read_rows(out) if r["protein_change"] == "T168N")
            self.assertEqual(row["class"], "GOG")
            self.assertEqual(row["clinvar_significance"], "Pathogenic")
            self.assertEqual(row["predictors_miss_it"], "True")
            self.assertLess(float(row["cadd"]), 20.0)
            self.assertEqual(row["rank"], "1")

    def test_unmapped_guard_fires_on_numbering_discordance(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            row = next(r for r in read_rows(out) if r["protein_change"] == "R220C")
            self.assertEqual(row["class"], "unmapped")


class TestClassifierUnits(unittest.TestCase):
    def test_sequon_helpers(self):
        # N-A-S is a sequon; N-P-S is not (X == Pro); N-A-A is not (+2 not S/T).
        self.assertEqual(glyco.n_sequon_starts("NAS"), {1})
        self.assertEqual(glyco.n_sequon_starts("NPS"), set())
        self.assertEqual(glyco.n_sequon_starts("NAA"), set())

    def test_ref_mismatch_is_unmapped(self):
        cls, _ = glyco.classify("MKT", {}, "R", 1, "C")  # residue 1 is M, not R
        self.assertEqual(cls, "unmapped")


if __name__ == "__main__":
    unittest.main()
