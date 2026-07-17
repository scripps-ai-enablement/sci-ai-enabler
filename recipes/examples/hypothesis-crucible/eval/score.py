#!/usr/bin/env python3
"""Deterministic scorer for a Crucible run bundle.

Generation in Crucible is agentic and non-deterministic, but *scoring a captured
run* is fully deterministic — so the evaluation lives here as a reproducible
artifact (stdlib only, no wall-clock, sorted output). It reads a run bundle
(hypotheses.json + kill-log.jsonl + fragments.jsonl) and a gold set
(known-repurposings.json + planted-negatives.json) and computes the metrics that
decide whether the falsification gauntlet earns its place:

  * rediscovery_recall        (T1) — of post-cutoff known repurposings, how many surfaced
  * precision                 (T2) — of adjudicable surfaced hypotheses, fraction that are known-good
  * planted_negative_kill_rate(T2) — of planted negatives seen as candidates, fraction killed
  * planted_negatives_surfaced(T2) — planted negatives that leaked through (should be 0)
  * per_gate_kills            (T2) — how many candidates each gate G1-G4 removed
  * groundedness              (T4) — fraction of hypothesis chain steps bound to a real fragment
  * novelty_gate_ok           (T5) — fraction of surfaced hypotheses with no direct-claim fragment

The scorer is intentionally strict and simple: names are matched case-insensitively;
a hypothesis is credited against a gold entry only on an exact drug-name match.

Run: python3 score.py --run <run_dir> --gold <gold_dir> [--out metrics.json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCRIPT_VERSION = "1.0.0"
DIRECT_CLAIM_PREDICATES = {"treats", "indicated_for", "approved_for", "indicated"}


def _norm(name: str) -> str:
    return " ".join(str(name).strip().lower().split())


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _drug_of_candidate(candidate: str) -> str:
    """'rosiglitazone -> Alzheimer disease' -> 'rosiglitazone' (normalized)."""
    return _norm(candidate.split("->")[0])


def _is_alzheimer(obj: dict) -> bool:
    return "alzheimer" in _norm(obj.get("name", "")) or obj.get("ontology_id") == "EFO_0000249"


def score(run_dir: Path, gold_dir: Path) -> dict:
    hyp_doc = json.loads((run_dir / "hypotheses.json").read_text(encoding="utf-8"))
    hypotheses = hyp_doc.get("hypotheses", [])
    kills = _load_jsonl(run_dir / "kill-log.jsonl")
    fragments = _load_jsonl(run_dir / "fragments.jsonl")

    known = json.loads((gold_dir / "known-repurposings.json").read_text(encoding="utf-8"))["entries"]
    planted = json.loads((gold_dir / "planted-negatives.json").read_text(encoding="utf-8"))["entries"]

    surfaced = {_norm(h["subject"]["name"]) for h in hypotheses}
    killed = {_drug_of_candidate(k["candidate"]) for k in kills}
    known_drugs = {_norm(e["drug"]) for e in known}
    planted_drugs = {_norm(e["drug"]) for e in planted}

    # T1 — retrospective rediscovery recall
    rediscovered = sorted(surfaced & known_drugs)
    rediscovery_recall = round(len(rediscovered) / len(known_drugs), 6) if known_drugs else None

    # T2 — precision over adjudicable surfaced hypotheses (those we have ground truth for)
    adjudicable = surfaced & (known_drugs | planted_drugs)
    correct = surfaced & known_drugs
    precision = round(len(correct) / len(adjudicable), 6) if adjudicable else None

    # T2 — planted-negative handling
    planted_surfaced = sorted(surfaced & planted_drugs)
    planted_candidates = planted_drugs & (surfaced | killed)
    planted_killed = planted_drugs & killed
    planted_kill_rate = (round(len(planted_killed) / len(planted_candidates), 6)
                         if planted_candidates else None)

    per_gate_kills: dict[str, int] = {}
    for k in kills:
        per_gate_kills[k["gate"]] = per_gate_kills.get(k["gate"], 0) + 1

    # T4 — groundedness: every chain step must bind to a real fragment id
    frag_ids = {f["id"] for f in fragments}
    total_steps = grounded_steps = 0
    fully_grounded = 0
    for h in hypotheses:
        steps = h.get("bridge_chain", [])
        ok = True
        for s in steps:
            total_steps += 1
            if s.get("fragment_id") in frag_ids:
                grounded_steps += 1
            else:
                ok = False
        if ok and steps:
            fully_grounded += 1
    groundedness = round(grounded_steps / total_steps, 6) if total_steps else None

    # T5 — novelty-gate correctness: no fragment directly asserts a surfaced drug -> AD
    novelty_violations = sorted({
        _norm(f["subject"]["name"])
        for f in fragments
        if _norm(f["subject"]["name"]) in surfaced
        and f.get("predicate") in DIRECT_CLAIM_PREDICATES
        and _is_alzheimer(f.get("object", {}))
    })
    novelty_gate_ok = (round((len(surfaced) - len(novelty_violations)) / len(surfaced), 6)
                       if surfaced else None)

    return {
        "run": run_dir.name,
        "time_slice_cutoff": hyp_doc.get("time_slice_cutoff"),
        "counts": {
            "fragments": len(fragments),
            "surfaced": len(surfaced),
            "killed": len(kills),
            "candidates_considered": len(surfaced | killed),
        },
        "rediscovery_recall": rediscovery_recall,
        "rediscovered": rediscovered,
        "precision": precision,
        "planted_negative_kill_rate": planted_kill_rate,
        "planted_negatives_surfaced": len(planted_surfaced),
        "per_gate_kills": per_gate_kills,
        "groundedness": groundedness,
        "hypotheses_fully_grounded": fully_grounded,
        "novelty_gate_ok": novelty_gate_ok,
        "novelty_violations": novelty_violations,
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_provenance(out_dir: Path, run_dir: Path, gold_dir: Path, metrics_path: Path) -> Path:
    """Emit provenance.json for the scoring step. Deterministic: input hashes only,
    no wall-clock. Mirrors recipes/examples/functional-enrichment/enrichment.py."""
    inputs = {
        p.name: _sha256(p)
        for p in sorted(
            [run_dir / "hypotheses.json", run_dir / "kill-log.jsonl", run_dir / "fragments.jsonl",
             gold_dir / "known-repurposings.json", gold_dir / "planted-negatives.json"],
            key=lambda p: p.name,
        )
    }
    record = {
        "analysis": "crucible-eval-score",
        "script": "score.py",
        "script_version": SCRIPT_VERSION,
        "environment": "requirements.txt (pinned); scorer itself is stdlib-only",
        "inputs": inputs,
        "outputs": {metrics_path.name: {"sha256": _sha256(metrics_path)}},
    }
    path = out_dir / "score.provenance.json"
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description="Score a Crucible run bundle against a gold set.")
    ap.add_argument("--run", type=Path,
                    default=here.parent / "runs" / "alz-drug-repurposing",
                    help="run-bundle directory (hypotheses.json, kill-log.jsonl, fragments.jsonl)")
    ap.add_argument("--gold", type=Path, default=here / "gold", help="gold fixtures directory")
    ap.add_argument("--out", type=Path, default=None, help="write metrics JSON here")
    ap.add_argument("--provenance", action="store_true", help="also write score.provenance.json")
    args = ap.parse_args()

    metrics = score(args.run, args.gold)
    text = json.dumps(metrics, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        if args.provenance:
            write_provenance(args.out.parent, args.run, args.gold, args.out)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
