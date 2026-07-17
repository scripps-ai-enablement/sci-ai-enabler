# Hypothesis Crucible — worked example + evaluation harness

This is the reference bundle for the recipe
[Generate falsification-tested drug-repurposing hypotheses across corpora](../../items/generate-cross-corpus-drug-repurposing-hypotheses.html)
and the [Hypothesis Crucible plugin](../../../catalog/tools/hypothesis-crucible.html). It shows
(1) what a `/crucible:forge` **run bundle** looks like and (2) how to **evaluate** a run so you can
decide whether the falsification gauntlet actually earns its place.

> **This run bundle is synthetic and illustrative.** The fragments and accessions under
> `runs/alz-drug-repurposing/` are representative examples chosen to demonstrate the schema and to
> drive the scorer and CI test deterministically — they are **not** a live literature-mined result,
> and the two surfaced hypotheses are **Proposed**, not validated. Replace the bundle with a real
> captured run to evaluate the system for a decision.

## The run bundle (`runs/alz-drug-repurposing/`)

A forge run writes one directory per run. This one captures a time-sliced (cutoff 2019-12-31)
Alzheimer drug-repurposing run:

| file | what it holds |
|---|---|
| `hypotheses.json` | the 2 surviving hypotheses — each with a fragment-cited bridge chain, the novelty searches that failed, the disconfirmation sought, and a discriminating experiment |
| `kill-log.jsonl` | the 5 rejected candidates, each with the gate (G1–G4) and evidence that killed it |
| `fragments.jsonl` | the 12 typed, provenance-carrying fragments mined across five corpora |
| `provenance.json` | analysis id, model id, per-source snapshot dates, and a sha256 of each output |
| `run.bco.json` | the IEEE-2791 BioCompute Object — the auditable, re-attemptable ledger |

What the run demonstrates: two candidates survive (baricitinib and montelukast, each bridged across
ChEMBL + PubMed + Open Targets + GEO), while five die in the gauntlet — donepezil at **G1** (already
an approved indication, not novel), fingolimod at **G2** (an ungrounded mechanistic step),
rosiglitazone and semagacestat at **G3** (failed Phase III trials), and loperamide at **G4** (no
blood–brain-barrier exposure). The kill-log is the point: aggressive, logged rejection.

## Evaluation (`eval/`)

Generation is agentic and non-deterministic, but **scoring a captured run is deterministic**, so the
evaluation is a reproducible, stdlib-only artifact.

```
python3 eval/score.py --run runs/alz-drug-repurposing --gold eval/gold --out /tmp/metrics.json
```

Scoring this bundle yields, deterministically:

| metric | value | meaning |
|---|---|---|
| `rediscovery_recall` | 0.5 | of post-cutoff known repurposings (montelukast, sildenafil), montelukast was rediscovered |
| `precision` | 1.0 | of adjudicable surfaced hypotheses, all are known-good |
| `planted_negative_kill_rate` | 1.0 | all three planted negatives were killed, not surfaced |
| `planted_negatives_surfaced` | 0 | none leaked through |
| `per_gate_kills` | G1:1, G2:1, G3:2, G4:1 | which gate did the work |
| `groundedness` | 1.0 | every surfaced chain step binds to a real fragment (T4 invariant) |
| `novelty_gate_ok` | 1.0 | no surfaced hypothesis had a direct-claim fragment at the cutoff |

- `eval/gold/` — the gold fixtures: `known-repurposings.json` (post-cutoff truths for T1),
  `planted-negatives.json` (false/failing pairs for T2), `swanson-anchors.json` (classic LBD sanity
  checks).
- `eval/PROTOCOL.md` — the full T1–T6 protocol, including the ablation/baseline matrix and the
  **ship gate** (full Crucible must beat a no-gauntlet baseline on precision at comparable recall).
- `eval/score.py` — the deterministic scorer.

`tests/test_crucible_eval.py` asserts these metrics and that `metrics.json` is byte-stable across
repeated scoring runs.

## Relationship to the doctrine

The run bundle is the durable, auditable record the
[reproducibility doctrine](../../../guide/advanced/reproducibility.html) requires. Because a forge
run is agentic, the BCO makes it *auditable and re-attemptable* rather than byte-reproducible; the
deterministic part (scoring) is captured as committed code with pinned extras and its own
provenance.
