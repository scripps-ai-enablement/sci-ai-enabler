# Composer plugin A/B — results

- runs scored: **60** (30 with / 30 without)
- prompts: **10**
- model: claude-sonnet-5
- compose skill actually invoked in the *with* arm: **0.767** (must be ~1.0, else the plugin never fired and results are void)
- permission denials: with=104, without=52 — **asymmetric**: the `with` arm was denied more tool calls, so it is handicapped. Read any `with` win as a lower bound, and treat a `without` win as possibly an artefact of the denials rather than a result.

## Per-arm means

| metric | with plugin | without plugin |
|---|---|---|
| key_recall | 0.602 | 0.338 |
| key_hits | 1.433 | 0.733 |
| catalog_hits | 4.0 | 3.433 |
| unknown_components | 0.033 | 0.0 |
| recipes_cited | 1.267 | 0.367 |
| has_evidence_label | 0.7 | 0.1 |
| has_availability | 0.633 | 0.0 |
| has_compute | 0.733 | 0.067 |
| tool_calls | 20.533 | 10.133 |
| permission_denials | 3.467 | 1.733 |
| cost_usd | 1.152 | 0.572 |
| num_turns | 19.633 | 8.133 |
| words | 1364.067 | 1170.967 |

## Win / tie / loss on answer-key recall

**with plugin won 5, tied 5, lost 0** of 10 comparable prompts.

Recall = fraction of the tools that prompt's curated recipe links to that the answer actually named.

| prompt | key | recall with | recall without | delta | spread with/without | unknown with/without |
|---|---|---|---|---|---|---|
| `design-crispr-sgrnas-for-a-gene-knockout` | 1 | 1.0 | 0.0 | 1.0 | 0.0/0.0 | 0.333/0.0 |
| `estimate-pk-properties` | 3 | 0.889 | 0.111 | 0.778 | 0.333/0.333 | 0.0/0.0 |
| `scan-drug-repurposing-candidates` | 5 | 0.4 | 0.0 | 0.4 | 0.6/0.0 | 0.0/0.0 |
| `map-disease-to-genes-and-pathways` | 3 | 0.667 | 0.333 | 0.334 | 0.0/0.0 | 0.0/0.0 |
| `build-target-dossier` | 5 | 0.733 | 0.6 | 0.133 | 0.2/0.0 | 0.0/0.0 |
| `draft-phase23-clinical-trial-protocol` | 2 | 0.0 | 0.0 | 0.0 | 0.0/0.0 | 0.0/0.0 |
| `extract-structured-data-from-clinical-notes` | 1 | 0.0 | 0.0 | 0.0 | 0.0/0.0 | 0.0/0.0 |
| `benchmark-admet-property-with-pytdc` | 3 | 0.333 | 0.333 | 0.0 | 0.0/0.0 | 0.0/0.0 |
| `identify-bacterial-isolate-from-16s-sequence` | 1 | 1.0 | 1.0 | 0.0 | 0.0/0.0 | 0.0/0.0 |
| `find-selective-cancer-dependencies-with-depmap` | 1 | 1.0 | 1.0 | 0.0 | 0.0/0.0 | 0.0/0.0 |

### Read the spread column before believing a delta

`spread` is max-minus-min recall across reps within one arm. Where spread is as large as the delta, that prompt shows run-to-run noise, not an effect.


## Sliced by complexity

| complexity | n | recall with | recall without |
|---|---|---|---|
| Claude Code alone | 1 | 0.0 | 0.0 |
| Multi-tool harness | 4 | 0.672 | 0.261 |
| One skill or MCP | 5 | 0.667 | 0.467 |

## Sliced by problem class

| problem class | n | recall with | recall without |
|---|---|---|---|
| Data analysis | 3 | 0.444 | 0.444 |
| Experimental design | 1 | 1.0 | 0.0 |
| Hypothesis generation | 1 | 1.0 | 1.0 |
| Knowledge synthesis | 4 | 0.672 | 0.261 |
| Manuscript prep | 1 | 0.0 | 0.0 |

## Cost

total **$51.73** across 60 runs (with=$34.56, without=$17.17)


## Caveats baked into these numbers

- `unknown_components` is a heuristic (component-shaped names absent from all three catalogs). Read the `_unknown` column of results.csv before quoting it; a matcher miss looks identical to an invention.
- Recall credits naming a tool, not using it correctly. A wrong recommendation that happens to name the right tool still scores.
- n=10 prompts. Report the rows, not a confidence interval.
