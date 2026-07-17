# Crucible evaluation protocol (T1–T6)

The evaluation exists to answer one question: **does the falsification gauntlet actually raise
precision without destroying discovery recall?** If it does not, Crucible does not justify itself
over a plain generator and should not ship. Scoring a captured run is deterministic
(`score.py`); the *runs* being scored are produced agentically via `/crucible:forge`.

## How to run the scorer

```
python3 score.py --run ../runs/alz-drug-repurposing --gold ./gold --out /tmp/metrics.json
```

`score.py` is stdlib-only. It prints the metrics and (with `--out`) writes a byte-stable
`metrics.json`. The reference bundle under `../runs/alz-drug-repurposing` is a **synthetic,
illustrative** run used to exercise the scorer and the CI test; replace it with a real captured run
to evaluate the system for a decision.

## The tests

**T1 — Retrospective time-sliced rediscovery (efficacy / recall).**
Produce a forge run with the time-slice cutoff set to a past date `T` (every source adapter honors
`snapshot_date <= T`). Score against `gold/known-repurposings.json`, whose entries became
established *after* `T`. Metric: `rediscovery_recall`. Because the direct claim did not exist at
`T`, a hit is genuine discovery, not memorization. Sanity-check general runs against
`gold/swanson-anchors.json`.

**T2 — Precision / false-positive control (the differentiator).**
Include `gold/planted-negatives.json` (retracted, failed-trial, and pharmacologically implausible
pairs) in the candidate universe. Metrics: `planted_negative_kill_rate` (should be high),
`planted_negatives_surfaced` (should be 0), and `per_gate_kills` (which gate did the work). A run
that surfaces a planted negative is a hard failure.

**T3 — Gate ablation + baselines (does the gauntlet earn its place?).**
Score four configurations on the same candidate universe and tabulate the deltas:
| config | how |
|---|---|
| (a) raw generation | generator only, gauntlet disabled |
| (b) tournament-only | Stage 4 ranking, gauntlet disabled (Co-Scientist-like) |
| (c) Crucible full | all four gates + tournament |
| (d) leave-one-gate-out | disable G1, G2, G3, G4 in turn |
**Ship gate:** (c) must beat (a) and (b) on `precision` at comparable `rediscovery_recall`, and
each leave-one-out in (d) must show a higher `planted_negatives_surfaced` / lower `precision` than
(c) — i.e. every gate demonstrably removes false positives.

**T4 — Groundedness invariant (hard gate).** `groundedness` must equal `1.0` for any run whose
hypotheses are surfaced — every chain step binds to a real fragment. A value below 1.0 means an
ungrounded claim escaped gate G2 and the run is rejected.

**T5 — Novelty-gate correctness.** `novelty_gate_ok` must equal `1.0`: no surfaced hypothesis may
have a fragment that directly asserts the drug→disease claim at the cutoff. `novelty_violations`
lists any offenders.

**T6 — Blinded expert / LLM-judge rubric.** Out of band of `score.py`: have blinded reviewers (or a
strong LLM judge) rate surfaced hypotheses on plausibility, novelty, and testability versus the
baselines, and audit a sample of `kill-log.jsonl` entries for correct rejection (REFUTE-style
calibration).

## Reference-bundle expected metrics
Scoring the shipped synthetic bundle yields, deterministically:
`rediscovery_recall = 0.5` (montelukast rediscovered; sildenafil missed), `precision = 1.0`,
`planted_negative_kill_rate = 1.0`, `planted_negatives_surfaced = 0`,
`per_gate_kills = {G1:1, G2:1, G3:2, G4:1}`, `groundedness = 1.0`, `novelty_gate_ok = 1.0`.
`tests/test_crucible_eval.py` asserts these and that `metrics.json` is byte-stable across runs.
