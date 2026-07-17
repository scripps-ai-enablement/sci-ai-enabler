#!/usr/bin/env python3
"""End-to-end test of the glycosylation-variant reference artifact.

Mirrors tests/test_reproducible_example.py for the recipe
"Interpret variants that gain or lose glycosylation sites". Exercises the
reproducibility doctrine, the scientific ground truth, and — new in v2 — that
the run emits an IEEE-2791 BioCompute Object that reproduces and validates.

  1. The offline replay is deterministic (two runs byte-identical across the CSV,
     provenance, AND the BCO) and matches the provenance-recorded output hashes.
  2. The bundle ships what the doctrine requires (script, pinned requirements,
     provenance, BCO, README, fixtures, bundled IEEE-2791 schema).
  3. Every variant's computed class matches the `expected_class` ground truth.
  4. The headline finding holds (IFNGR2 T168N: a pathogenic gain-of-glycosylation
     call the standard predictors miss).
  5. The BCO is structurally sound (all eight required domains; etag recomputes;
     cites GlyGen's dataset BCOs) — checked with the standard library — and, when
     jsonschema + referencing are installed, validates against the bundled
     IEEE-2791 schema.

The structural checks are pure standard library so they run in CI. The full
schema validation is skipped unless the optional deps are present.

Run: python3 -m unittest discover -s tests
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
SCHEMA_DIR = FIXTURES / "ieee2791"

_spec = importlib.util.spec_from_file_location("glyco_variants", SCRIPT)
glyco = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(glyco)

REQUIRED_BCO_DOMAINS = ["object_id", "spec_version", "etag", "provenance_domain",
                        "usability_domain", "description_domain", "execution_domain", "io_domain"]

try:
    import jsonschema  # noqa: F401
    import referencing  # noqa: F401
    _HAS_SCHEMA_DEPS = True
except Exception:
    _HAS_SCHEMA_DEPS = False


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
                  FIXTURES / "biomcp" / "P38484_T168N.json",
                  SCHEMA_DIR / "2791object.json"):
            self.assertTrue(p.exists(), f"missing artifact file: {p}")

    def test_requirements_are_pinned(self):
        pinned = [ln for ln in (EXAMPLE / "requirements.txt").read_text().splitlines()
                  if ln.strip() and not ln.strip().startswith("#")]
        self.assertTrue(pinned, "requirements.txt has no dependency lines")
        for line in pinned:
            self.assertIn("==", line, f"dependency not pinned: {line!r}")


class TestReproducibility(unittest.TestCase):
    def test_all_outputs_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a", Path(d) / "b"
            run_offline(a)
            run_offline(b)
            for name in ("glyco_candidates.csv", "provenance.json", "glyco_run.bco.json"):
                self.assertEqual(sha256(a / name), sha256(b / name),
                                 f"{name} differs between identical runs — not reproducible")

    def test_provenance_hashes_match_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            prov = run_offline(out)["provenance"]
            for name, h in prov["outputs"].items():
                self.assertEqual(h, sha256(out / name), f"provenance hash mismatch for {name}")


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
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            row = next(r for r in read_rows(out) if r["protein_change"] == "T168N")
            self.assertEqual(row["class"], "GOG")
            self.assertEqual(row["clinvar_significance"], "Pathogenic")
            self.assertEqual(row["predictors_miss_it"], "True")
            self.assertLess(float(row["cadd"]), 20.0)
            self.assertEqual(row["rank"], "1")

    def test_unmapped_guard_fires(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            row = next(r for r in read_rows(out) if r["protein_change"] == "R220C")
            self.assertEqual(row["class"], "unmapped")


class TestBioComputeObject(unittest.TestCase):
    """Structural checks — standard library only, so they run in CI."""

    def _bco(self, out: Path) -> dict:
        run_offline(out)
        return json.loads((out / "glyco_run.bco.json").read_text())

    def test_required_domains_present(self):
        with tempfile.TemporaryDirectory() as d:
            bco = self._bco(Path(d))
            for k in REQUIRED_BCO_DOMAINS:
                self.assertIn(k, bco, f"BCO missing required top-level field: {k}")
            self.assertEqual(bco["spec_version"], glyco.SPEC_VERSION)
            self.assertTrue(bco["description_domain"]["pipeline_steps"], "no pipeline_steps")

    def test_etag_recomputes(self):
        with tempfile.TemporaryDirectory() as d:
            bco = self._bco(Path(d))
            self.assertEqual(bco["etag"], glyco._etag(bco))

    def test_cites_glygen_dataset_bcos(self):
        with tempfile.TemporaryDirectory() as d:
            bco = self._bco(Path(d))
            uris = {i["uri"]["uri"] for i in bco["io_domain"]["input_subdomain"]}
            self.assertIn("https://data.glygen.org/GLY_001534", uris)
            self.assertIn("https://data.glygen.org/GLY_001537", uris)

    @unittest.skipUnless(_HAS_SCHEMA_DEPS, "jsonschema + referencing not installed")
    def test_validates_against_ieee2791_schema(self):
        # Both a fresh build and the committed artifact must validate.
        with tempfile.TemporaryDirectory() as d:
            res = run_offline(Path(d))
            self.assertTrue(res["bco_valid"], f"fresh BCO invalid: {res['bco_errors']}")
        committed = json.loads((EXAMPLE / "results" / "glyco_run.bco.json").read_text())
        ok, errors = glyco.validate_bco(committed, SCHEMA_DIR)
        self.assertTrue(ok, f"committed BCO invalid: {errors}")


class TestClassifierUnits(unittest.TestCase):
    def test_sequon_helpers(self):
        self.assertEqual(glyco.n_sequon_starts("NAS"), {1})
        self.assertEqual(glyco.n_sequon_starts("NPS"), set())
        self.assertEqual(glyco.n_sequon_starts("NAA"), set())

    def test_ref_mismatch_is_unmapped(self):
        cls, _ = glyco.classify("MKT", {}, "R", 1, "C")
        self.assertEqual(cls, "unmapped")


if __name__ == "__main__":
    unittest.main()
