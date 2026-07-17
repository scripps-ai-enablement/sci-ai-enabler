#!/usr/bin/env python3
"""CI test for the Hypothesis Crucible evaluation harness.

Crucible's forge run is agentic and not unit-testable, but the *scorer* that
evaluates a captured run bundle is deterministic — and that is exactly the part
that decides whether the falsification gauntlet earns its place. This test:

  1. Scores the shipped reference bundle and asserts the expected metrics
     (rediscovery recall, precision, planted-negative kill rate, per-gate
     attribution, the groundedness and novelty invariants).
  2. Confirms metrics.json is byte-identical across repeated scoring runs.
  3. Checks the run bundle ships every file the doctrine requires, and that the
     committed run.bco.json is structurally valid and its etag recomputes.

Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXAMPLE = REPO / "recipes" / "examples" / "hypothesis-crucible"
RUN = EXAMPLE / "runs" / "alz-drug-repurposing"
GOLD = EXAMPLE / "eval" / "gold"
SCORE = EXAMPLE / "eval" / "score.py"

_spec = importlib.util.spec_from_file_location("crucible_score", SCORE)
crucible_score = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(crucible_score)

REQUIRED_BCO_DOMAINS = ["object_id", "spec_version", "etag", "provenance_domain",
                        "usability_domain", "description_domain", "execution_domain", "io_domain"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TestBundleComplete(unittest.TestCase):
    def test_all_bundle_files_present(self):
        for name in ("hypotheses.json", "kill-log.jsonl", "fragments.jsonl",
                     "provenance.json", "run.bco.json"):
            self.assertTrue((RUN / name).is_file(), f"missing run-bundle file: {name}")

    def test_eval_files_present(self):
        for p in (SCORE, EXAMPLE / "eval" / "PROTOCOL.md", EXAMPLE / "eval" / "requirements.txt",
                  GOLD / "known-repurposings.json", GOLD / "planted-negatives.json",
                  GOLD / "swanson-anchors.json", EXAMPLE / "README.md"):
            self.assertTrue(p.exists(), f"missing eval file: {p}")

    def test_requirements_are_pinned(self):
        lines = [ln for ln in (EXAMPLE / "eval" / "requirements.txt").read_text().splitlines()
                 if ln.strip() and not ln.strip().startswith("#")]
        self.assertTrue(lines)
        for line in lines:
            self.assertIn("==", line, f"dependency not pinned: {line!r}")


class TestScorerMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = crucible_score.score(RUN, GOLD)

    def test_counts(self):
        self.assertEqual(self.m["counts"],
                         {"fragments": 12, "surfaced": 2, "killed": 5, "candidates_considered": 7})

    def test_rediscovery_recall(self):
        self.assertEqual(self.m["rediscovery_recall"], 0.5)
        self.assertEqual(self.m["rediscovered"], ["montelukast"])

    def test_precision_and_planted_negatives(self):
        self.assertEqual(self.m["precision"], 1.0)
        self.assertEqual(self.m["planted_negative_kill_rate"], 1.0)
        self.assertEqual(self.m["planted_negatives_surfaced"], 0)

    def test_per_gate_attribution(self):
        self.assertEqual(self.m["per_gate_kills"], {"G1": 1, "G2": 1, "G3": 2, "G4": 1})

    def test_groundedness_invariant(self):
        # T4: every surfaced chain step must bind to a real fragment.
        self.assertEqual(self.m["groundedness"], 1.0)
        self.assertEqual(self.m["hypotheses_fully_grounded"], 2)

    def test_novelty_gate_invariant(self):
        # T5: no surfaced hypothesis has a direct-claim fragment at the cutoff.
        self.assertEqual(self.m["novelty_gate_ok"], 1.0)
        self.assertEqual(self.m["novelty_violations"], [])


class TestScorerDeterminism(unittest.TestCase):
    def test_metrics_json_byte_identical(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a.json", Path(d) / "b.json"
            for out in (a, b):
                text = json.dumps(crucible_score.score(RUN, GOLD), indent=2, sort_keys=True) + "\n"
                out.write_text(text, encoding="utf-8")
            self.assertEqual(sha256(a), sha256(b),
                             "metrics.json differs between identical scoring runs — not reproducible")


class TestGroundednessCatchesRegression(unittest.TestCase):
    def test_orphan_fragment_drops_groundedness(self):
        # If a hypothesis cites a fragment id that isn't in the store, groundedness
        # must fall below 1.0 — the guard that an ungrounded claim escaping G2 fails the run.
        with tempfile.TemporaryDirectory() as d:
            run2 = Path(d) / "run"
            run2.mkdir()
            for name in ("kill-log.jsonl", "fragments.jsonl"):
                (run2 / name).write_text((RUN / name).read_text(), encoding="utf-8")
            doc = json.loads((RUN / "hypotheses.json").read_text())
            doc["hypotheses"][0]["bridge_chain"][0]["fragment_id"] = "f_does_not_exist"
            (run2 / "hypotheses.json").write_text(json.dumps(doc), encoding="utf-8")
            m = crucible_score.score(run2, GOLD)
            self.assertLess(m["groundedness"], 1.0)
            self.assertEqual(m["hypotheses_fully_grounded"], 1)


class TestBioComputeObject(unittest.TestCase):
    def _bco(self) -> dict:
        return json.loads((RUN / "run.bco.json").read_text())

    def test_required_domains_present(self):
        bco = self._bco()
        for k in REQUIRED_BCO_DOMAINS:
            self.assertIn(k, bco, f"BCO missing required top-level field: {k}")
        self.assertTrue(bco["description_domain"]["pipeline_steps"])

    def test_etag_recomputes(self):
        bco = self._bco()
        tmp = dict(bco)
        tmp["etag"] = ""
        recomputed = hashlib.sha256(
            json.dumps(tmp, indent=2, sort_keys=True).encode("utf-8")).hexdigest()
        self.assertEqual(bco["etag"], recomputed, "committed BCO etag does not recompute")

    def test_provenance_hashes_match_outputs(self):
        prov = json.loads((RUN / "provenance.json").read_text())
        for name, rec in prov["outputs"].items():
            self.assertEqual(rec["sha256"], sha256(RUN / name),
                             f"provenance hash mismatch for {name}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
