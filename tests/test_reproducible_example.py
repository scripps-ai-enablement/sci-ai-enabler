#!/usr/bin/env python3
"""End-to-end test of the reproducibility doctrine.

The cookbook's standing rule is that an AI-assisted analysis is captured as
committed code + a pinned environment + a provenance record, and that the code
reproduces. This test exercises that end to end against the reference artifact
in recipes/examples/functional-enrichment/:

  1. Run enrichment.py --offline into two separate temp dirs and assert every
     output byte is identical (determinism) and matches the recorded provenance
     hashes (the artifact verifies itself).
  2. Assert the artifact ships the things the doctrine requires: a pinned
     requirements file and a provenance record with the mandatory fields.
  3. Assert the SUMMARY only names terms that are actually present in the saved
     tables (the grounding rule).
  4. Assert the doctrine is wired into the prompts/docs that generate the
     cookbook, so it propagates to future recipes — not just this example.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXAMPLE = REPO / "recipes" / "examples" / "functional-enrichment"
SCRIPT = EXAMPLE / "enrichment.py"
FIXTURE = EXAMPLE / "fixtures" / "enrichr_response.json"
GENES = EXAMPLE / "genes.txt"

# Import enrichment.py as a module without needing a package.
_spec = importlib.util.spec_from_file_location("enrichment", SCRIPT)
enrichment = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(enrichment)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_example(outdir: Path) -> dict:
    return enrichment.run(GENES, outdir, enrichment.DEFAULT_LIBRARIES,
                          offline=FIXTURE, run_date=None)


class TestArtifactExists(unittest.TestCase):
    def test_bundle_is_complete(self):
        for p in (SCRIPT, FIXTURE, GENES,
                  EXAMPLE / "requirements.txt", EXAMPLE / "README.md"):
            self.assertTrue(p.exists(), f"missing artifact file: {p}")

    def test_requirements_are_pinned(self):
        reqs = (EXAMPLE / "requirements.txt").read_text()
        pinned = [ln for ln in reqs.splitlines()
                  if ln.strip() and not ln.strip().startswith("#")]
        self.assertTrue(pinned, "requirements.txt has no dependency lines")
        for line in pinned:
            self.assertIn("==", line,
                          f"dependency not pinned to an exact version: {line!r}")


class TestReproducibility(unittest.TestCase):
    def test_two_runs_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a", Path(d) / "b"
            out_a, out_b = run_example(a), run_example(b)
            names_a = sorted(p.name for p in a.iterdir())
            names_b = sorted(p.name for p in b.iterdir())
            self.assertEqual(names_a, names_b)
            for name in names_a:
                self.assertEqual(
                    sha256(a / name), sha256(b / name),
                    f"output {name} differs between identical runs — not reproducible",
                )
            # at least the five libraries + summary + provenance
            self.assertGreaterEqual(len(names_a), 7)

    def test_provenance_matches_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            out = run_example(Path(d))
            prov = json.loads(out["provenance"].read_text())
            for name, meta in prov["outputs"].items():
                self.assertEqual(
                    meta["sha256"], sha256(Path(d) / name),
                    f"provenance hash for {name} does not match the file on disk",
                )

    def test_provenance_has_mandatory_fields(self):
        with tempfile.TemporaryDirectory() as d:
            out = run_example(Path(d))
            prov = json.loads(out["provenance"].read_text())
            for field in ("script_version", "environment", "run_date",
                          "external_source", "input", "outputs", "parameters"):
                self.assertIn(field, prov, f"provenance missing field: {field}")
            self.assertIn("snapshot_date", prov["external_source"])
            self.assertIn("genes_sha256", prov["input"])

    def test_provenance_is_deterministic(self):
        """No wall-clock leakage: provenance.json itself is reproducible."""
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a", Path(d) / "b"
            out_a, out_b = run_example(a), run_example(b)
            self.assertEqual(out_a["provenance"].read_text(),
                             out_b["provenance"].read_text())


class TestGrounding(unittest.TestCase):
    def test_summary_only_cites_terms_in_tables(self):
        with tempfile.TemporaryDirectory() as d:
            out = run_example(Path(d))
            table_terms = set()
            for csv_path in out["tables"]:
                for line in csv_path.read_text().splitlines()[1:]:
                    cols = line.split(",")
                    if len(cols) > 1:
                        table_terms.add(cols[1])
            summary = out["summary"].read_text()
            cited = re.findall(r"\*\*(.+?)\*\*", summary)
            self.assertTrue(cited, "summary cited no terms")
            for term in cited:
                self.assertIn(
                    term, table_terms,
                    f"SUMMARY cites a term not present in any table: {term!r}",
                )


class TestDoctrineWiredIntoPrompts(unittest.TestCase):
    """The doctrine must live in the generators, so every future recipe inherits
    it — not only this hand-built example."""

    def test_recipe_agent_requires_reproducibility(self):
        text = (REPO / "RECIPE_AGENT.md").read_text().lower()
        self.assertIn("reproducib", text)
        self.assertIn("provenance", text)

    def test_composer_skill_records_an_artifact(self):
        text = (REPO / "composer" / "skills" / "compose" / "SKILL.md").read_text().lower()
        self.assertIn("provenance", text)
        self.assertTrue("script" in text or "notebook" in text)

    def test_guide_page_exists(self):
        page = REPO / "guide" / "advanced" / "reproducibility.md"
        self.assertTrue(page.exists(), "missing guide/advanced/reproducibility.md")


if __name__ == "__main__":
    unittest.main(verbosity=2)
