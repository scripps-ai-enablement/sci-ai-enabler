#!/usr/bin/env python3
"""End-to-end test of the glycosylation-variant reference artifact.

Mirrors tests/test_reproducible_example.py for the recipe
"Interpret variants that gain or lose glycosylation sites". This artifact was
regenerated to follow the recipe faithfully: the recipe's 7-column output
(`uniprot, site, class, glygen_evidence, clinvar_significance, alphamissense,
rank`) and its ranking rule (GOG/LOG above none — unmapped last — then within
that group by AlphaMissense pathogenicity, then ClinVar significance).

  1. Offline replay is deterministic (CSV, provenance, AND BCO byte-identical)
     and matches the provenance-recorded output hashes.
  2. Bundle ships what the doctrine requires (script, pinned requirements,
     provenance, BCO, README, fixtures, bundled IEEE-2791 schema).
  3. Every variant's class matches the `expected_class` ground truth.
  4. The recipe ranking holds: the four glycosylation-altering hits rank above
     the `none` controls (unmapped last); S114N (pathogenic + AlphaMissense
     pathogenic) is #1, and the predictor-discordant T168N sits mid-pack.
  5. AlphaMissense is joined (from BioMCP's predictions section).
  6. The BCO validates (structurally in stdlib; against the schema when
     jsonschema + referencing are installed).

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
RECIPE_COLUMNS = ["uniprot", "site", "class", "glygen_evidence",
                  "clinvar_significance", "alphamissense", "rank"]

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

    def test_output_columns_match_recipe(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            header = (out / "glyco_candidates.csv").read_text().splitlines()[0].split(",")
            self.assertEqual(header, RECIPE_COLUMNS)


class TestScientificGroundTruth(unittest.TestCase):
    def test_classes_match_expected(self):
        expected = {(r["uniprot"], r["protein_change"]): r["expected_class"]
                    for r in csv.DictReader(VARIANTS.open())}
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            for r in read_rows(out):
                key = (r["uniprot"], r["site"])
                self.assertEqual(r["class"], expected[key],
                                 f"{r['uniprot']} {r['site']}: got {r['class']}, expected {expected[key]}")

    def test_recipe_ranking(self):
        """GOG/LOG above none (unmapped last); S114N #1; T168N present but not #1."""
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            rows = sorted(read_rows(out), key=lambda r: int(r["rank"]))
            classes = [r["class"] for r in rows]
            self.assertEqual(classes[:4].count("GOG") + classes[:4].count("LOG"), 4,
                             "the four glyco-altering hits should occupy ranks 1-4")
            self.assertEqual(classes[4:6], ["none", "none"])
            self.assertEqual(classes[6], "unmapped")
            self.assertEqual(rows[0]["site"], "S114N", "recipe ranking puts S114N (AM pathogenic) first")
            t168n = next(r for r in rows if r["site"] == "T168N")
            self.assertEqual(t168n["class"], "GOG")
            self.assertGreater(int(t168n["rank"]), 1,
                               "under the recipe's AM-pathogenicity ranking T168N is not #1")

    def test_alphamissense_is_joined(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            by_site = {r["site"]: r for r in read_rows(out)}
            self.assertTrue(by_site["S114N"]["alphamissense"].startswith("Pathogenic"))
            # T168N is ClinVar Pathogenic but AlphaMissense calls it benign — it, too, misses the mechanism.
            self.assertTrue(by_site["T168N"]["alphamissense"].startswith("Benign"))
            self.assertEqual(by_site["T168N"]["clinvar_significance"], "Pathogenic")

    def test_unmapped_guard_fires(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            run_offline(out)
            row = next(r for r in read_rows(out) if r["site"] == "R220C")
            self.assertEqual(row["class"], "unmapped")


class TestBioComputeObject(unittest.TestCase):
    def _bco(self, out: Path) -> dict:
        run_offline(out)
        return json.loads((out / "glyco_run.bco.json").read_text())

    def test_required_domains_present(self):
        with tempfile.TemporaryDirectory() as d:
            bco = self._bco(Path(d))
            for k in REQUIRED_BCO_DOMAINS:
                self.assertIn(k, bco, f"BCO missing required top-level field: {k}")
            self.assertEqual(bco["spec_version"], glyco.SPEC_VERSION)
            self.assertTrue(bco["description_domain"]["pipeline_steps"])

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

    def test_glygen_inputs_name_the_dataset_file(self):
        """Each GlyGen BCO input names the file it distributes, not a prose label."""
        with tempfile.TemporaryDirectory() as d:
            bco = self._bco(Path(d))
            names = {i["uri"]["uri"]: i["uri"].get("filename")
                     for i in bco["io_domain"]["input_subdomain"]}
            self.assertEqual(names["https://data.glygen.org/GLY_001534"],
                             "human_protein_mutation_germline_all.csv")
            self.assertEqual(names["https://data.glygen.org/GLY_001537"],
                             "human_protein_mutation_cancer_all.csv")

    @unittest.skipUnless(_HAS_SCHEMA_DEPS, "jsonschema + referencing not installed")
    def test_validates_against_ieee2791_schema(self):
        with tempfile.TemporaryDirectory() as d:
            res = run_offline(Path(d))
            self.assertTrue(res["bco_valid"], f"fresh BCO invalid: {res['bco_errors']}")
        committed = json.loads((EXAMPLE / "results" / "glyco_run.bco.json").read_text())
        ok, errors = glyco.validate_bco(committed, SCHEMA_DIR)
        self.assertTrue(ok, f"committed BCO invalid: {errors}")


class TestProtVarJoin(unittest.TestCase):
    """The annotation join is accession-keyed; refuse rather than annotate the wrong residue."""

    # Shape of a ProtVar /mapping input entry, canonical isoform flagged.
    OK_ENTRY = {
        "inputStr": "P01008 114 S N", "messages": [],
        "derivedGenomicVariants": [{"genes": [{"isoforms": [
            {"accession": "Q8TCE1", "canonical": False, "isoformPosition": 114,
             "amScore": {"type": "AM", "amPathogenicity": 0.9209, "amClass": "PATHOGENIC"}},
            {"accession": "P01008", "canonical": True, "isoformPosition": 114,
             "amScore": {"type": "AM", "amPathogenicity": 0.8726, "amClass": "PATHOGENIC"}},
        ]}]}],
    }
    # The real P01008 220 R C response: reference-residue WARN + 9 derived variants.
    WARN_ENTRY = {
        "inputStr": "P01008 220 R C",
        "messages": [{"type": "WARN", "text": "User input reference amino acid (Arg) does not match "
                                              "the UniProt sequence (Lys) at position 220."}],
        "derivedGenomicVariants": [{"genes": [{"isoforms": []}]} for _ in range(9)],
    }

    def test_picks_the_canonical_isoform_not_the_first(self):
        iso, warns = glyco.protvar_canonical(self.OK_ENTRY)
        self.assertEqual(warns, [])
        self.assertEqual(iso["accession"], "P01008")       # not the Q8TCE1 fragment listed first
        self.assertEqual(iso["isoformPosition"], 114)
        # 0.8726 is P01008's score; 0.9209 is the fragment's, and is what the old
        # first-element behaviour reported.
        self.assertEqual(glyco.protvar_alphamissense(iso), ("PATHOGENIC", 0.8726))

    def test_reference_residue_warning_is_surfaced(self):
        iso, warns = glyco.protvar_canonical(self.WARN_ENTRY)
        self.assertIsNone(iso)
        self.assertTrue(any("does not match" in w for w in warns))
        self.assertTrue(any("derived genomic variants" in w for w in warns))

    def test_clinvar_only_counts_clinvar_sourced_calls(self):
        """P01008 N167S: ProtVar says Pathogenic, but sourced from Ensembl, not ClinVar."""
        pop = {"variants": [{"alternativeSequence": "Ser",
                             "clinicalSignificances": [{"type": "Pathogenic", "sources": ["Ensembl"]}],
                             "xrefs": [{"name": "dbSNP", "id": "rs121909570"}]}]}
        self.assertEqual(glyco.protvar_clinvar(pop, "S"), ("", ""))

    def test_clinvar_sourced_call_is_taken_with_its_rsid(self):
        pop = {"variants": [{"alternativeSequence": "Asn",
                             "clinicalSignificances": [{"type": "Pathogenic", "sources": ["Ensembl", "ClinVar"]}],
                             "xrefs": [{"name": "dbSNP", "id": "rs1657909645"}]}]}
        self.assertEqual(glyco.protvar_clinvar(pop, "N"), ("Pathogenic", "rs1657909645"))

    def test_alt_residue_must_match(self):
        pop = {"variants": [{"alternativeSequence": "Thr",
                             "clinicalSignificances": [{"type": "Pathogenic", "sources": ["ClinVar"]}]}]}
        self.assertEqual(glyco.protvar_clinvar(pop, "S"), ("", ""))


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
