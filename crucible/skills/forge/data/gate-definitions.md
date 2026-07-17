# The falsification gauntlet — gate definitions

The gauntlet is the point of this system. Most hypothesis-generation systems *rank and surface*;
Crucible **aggressively rejects**. Each candidate connection must survive **every** gate below.
Gates are **independent vetoes**: any one gate can kill a candidate on its own, and every kill is
written to `kill-log.jsonl` with the gate id, a reason code, and the evidence that killed it.

Design objective: **specificity / precision over recall.** It is correct behavior for the gauntlet
to kill a true hypothesis rather than surface a false one. A run that surfaces nothing is a valid,
honest outcome — better than one that surfaces a confident wrong answer.

Run the gates in this order (cheapest / most-decisive first, so most candidates die early):

## G1 — Novelty gate (active negative search)
Issue targeted searches for the **direct** A–C claim (`pubmed` / `consensus` / `ot` known-drug and
association queries). If any source already asserts the direct connection → **KILL** with reason
`not-novel`, citing the fragment/search that found it. Rationale: a connection is only "novel" if a
deliberate search for it *fails* (Swanson's undiscovered-public-knowledge test). This gate also
kills the trivially-true (e.g. an already-approved indication).

- reason codes: `not-novel`
- evidence: the fragment id or the search result that asserts the direct claim.

## G2 — Groundedness gate (no fragment → no claim)
Walk every step of the candidate's `bridge_chain`. Each step must map to a fragment in the run's
fragment store with a resolvable `source_id`. Any step that cannot be bound to a fragment is a
hallucinated link → **KILL** with reason `ungrounded-link`, naming the missing link. (Adapts the
KnowHD groundedness idea; mirrors the self-verification pattern used in the functional-enrichment
recipe.)

- reason codes: `ungrounded-link`
- evidence: the specific unsupported claim / missing link.

## G3 — Contradiction / red-team gate (seek disconfirmation)
Actively search for evidence that would *break* the candidate, not confirm it:
contradicting fragments (`polarity: contradicts`), failed or terminated trials for the pair
(`c-trials`), opposing experimental signatures (e.g. a GEO direction opposite to the mechanism),
and known counter-mechanisms. A dedicated red-team pass argues the strongest case *against* the
hypothesis. If disconfirmation is sufficient → **KILL** with reason `contradicted`.

- reason codes: `contradicted`
- evidence: the contradicting fragment(s) / failed-trial NCT id.

## G4 — Plausibility / consistency gate
Type- and direction-check against the ontology and pharmacology:
- direction sanity (e.g. an activator proposed where the mechanism needs inhibition),
- unit / entity-type coherence across the chain,
- pharmacological feasibility for the target compartment (for CNS goals: blood–brain-barrier
  penetration / P-gp efflux via ChEMBL ADMET; exposure; approved route).
Incoherent → **KILL** with reason `implausible`.

- reason codes: `wrong-direction`, `type-mismatch`, `implausible`
- evidence: the failing check (e.g. ChEMBL ADMET fragment showing no CNS exposure).

## kill-log.jsonl line schema
One JSON object per killed candidate:
```json
{"candidate": "<drug> -> <disease>", "gate": "G3", "reason": "contradicted",
 "evidence": {"fragment_id": "f10", "note": "Phase III, no cognitive benefit"}}
```
A candidate is only eligible to be surfaced if it appears in **no** kill-log line and passed G1–G4.
