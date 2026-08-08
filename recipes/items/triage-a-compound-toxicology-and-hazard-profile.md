---
title: Triage a compound's toxicology and hazard profile before committing to it
parent: All recipes
grand_parent: Recipes
nav_order: 27
problem_class: Knowledge synthesis
subject_areas: [Chemistry, Drug Repurposing and Discovery, Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-08
summary: Drive the ToolUniverse Chemical Safety skill to build a graded, source-attributed toxicology dossier per compound, distinguishing no-data from no-hazard.
---

# Triage a compound's toxicology and hazard profile before committing to it

Hand Claude Code a short list of compounds; get back a per-compound toxicology dossier assembled by the [Chemical Safety skill](../../catalog/tools/tooluniverse-chemical-safety.html) — predicted endpoints, experimental toxicogenomics, structural alerts and regulatory findings, each attributed to its source and tier, with the gaps marked as gaps.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery, Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A screening campaign produces a shortlist. Before anyone commits synthesis time, animal work, or a medicinal-chemistry programme to those compounds, someone has to ask what is already known about their liabilities — mutagenicity, hepatotoxicity, hERG, acute toxicity, reactive substructures, and for anything with clinical history, boxed warnings and contraindications. The same question arrives from a different direction when a collaborator ships an unfamiliar compound and the lab needs to know how to handle it.

The information exists, but it is scattered across predictive models, toxicogenomics databases, structural-alert sets, and regulatory filings, each with a different identifier scheme and a different meaning of "negative". Doing it by hand takes an afternoon per compound and is usually skipped. Doing it badly is worse than skipping it: the two failure modes are reading an empty database result as a clean bill of health, and letting a substructure alert veto a compound that was fine. "Solved" here means a committed, re-runnable dossier where every claim carries its source and its evidence tier, and where "we did not find anything" and "we found nothing adverse" are different cells in the table.

## Recommended approach

1. **Install the [Chemical Safety skill](../../catalog/tools/tooluniverse-chemical-safety.html)**, which requires the [ToolUniverse](../../catalog/tools/tooluniverse.html) MCP server first — the catalog pages own both install commands. The skill sets `disable-model-invocation: true` upstream, so you must invoke it explicitly rather than hoping it dispatches.

2. **Key your input on structure, not name.** Write `compounds.csv` with columns `compound_id`, `smiles`, and `intended_use` (`screening hit`, `tool compound`, `clinical candidate`, `handling assessment`). Names and vendor codes resolve ambiguously and a mis-resolved identifier makes the entire dossier belong to a different molecule. Have the skill's phase-0 disambiguation echo back the resolved SMILES, PubChem CID, InChIKey, and ChEMBL ID, and **stop on any compound where the resolved SMILES does not match the input** — record it in `identity_mismatch.csv` and exclude it from the run rather than profiling the wrong compound.

3. **Commit the workflow as a slash command.** Ask Claude Code to write `.claude/commands/triage-hazard.md` capturing the instruction, the output schema, and the gates below, so the next shortlist is triaged by the same text rather than by a re-typed prompt. Run it with `/triage-hazard`.

4. **Emit one row per (compound, endpoint, source) — never one row per compound.** `hazard_profile.csv` carries `compound_id`, `endpoint`, `value`, `source` (ADMET-AI, CTD, PubChemTox, AOPWiki, ChEMBL, STITCH, FDA, DrugBank), `evidence_tier` (the skill's T1–T4 grading), and `retrieved_utc`. Collapsing a predicted AMES call and an experimental Ames result into one "mutagenicity" cell is the mistake that makes the whole table untrustworthy; keeping the source column means a reviewer can see at a glance whether a red flag is measured or modelled.

5. **Write `coverage.csv` and treat it as the first table anyone reads.** For every (compound, source) pair record one of `queried_negative`, `queried_no_record`, or `not_applicable`. Phases 4 and 5 — FDA labelling and DrugBank safety — only return anything for compounds with pharmaceutical history, so a novel screening hit produces an empty result there *by construction*. Without this table, that emptiness reads as reassurance. It is the single most common misreading of an automated safety profile.

6. **Send structural alerts to their own file, and do not let them reject anything.** `structural_alerts.csv` takes the ChEMBL PAINS/Brenk/Glaxo matches with the alert name and the matched substructure. Flag them for orthogonal-assay follow-up; do not filter on them. The published PAINS filters were derived from a narrow proprietary dataset, which limits their applicability domain, and frequent-hitter behaviour is circumstantial evidence rather than proof of interference ([Kenny 2017](https://pubmed.ncbi.nlm.nih.gov/29048168/)).

7. **Ground the summary in the tables.** The skill synthesizes a Critical/High/Medium/Low classification; require every such call in `risk_summary.md` to cite the specific `hazard_profile.csv` rows that support it, and to state which sources returned no record. A risk grade with no row references is a model opinion, not a finding.

8. **Record provenance.** `provenance.json` carries the ToolUniverse version, the skill commit SHA, the UTC query timestamp (these are live APIs — the underlying databases move and nothing here is byte-reproducible), the sha256 of `compounds.csv`, and the model id. Commit `.claude/commands/triage-hazard.md`, the input CSV, all four output tables, and `provenance.json`. See the [reproducibility guide](../../guide/advanced/reproducibility.html) for the pattern.

**This is a research triage, not a safety data sheet.** It does not replace an SDS, a GHS classification of record, or your institution's EHS review, and nothing in it authorizes handling an unfamiliar compound at the bench.

## Why this assembly

Rung 2. The work is entirely retrieval and synthesis across eight source families, and the [Chemical Safety skill](../../catalog/tools/tooluniverse-chemical-safety.html) already encodes the phase ordering and the T1–T4 evidence grading — a reasoning layer over ToolUniverse tool calls, verified working in the catalog. Rung 1 fails on grounding, not on capability: plain Claude Code will happily produce a fluent toxicology paragraph about a known drug from pre-training, and there is no way to tell from the output which claims came from a database. The skill's value is that every row has a retrieval behind it. Rung 3 would add a second ADMET predictor for cross-checking, which is a real refinement but not required to answer the question; see **Alternatives**.

## Availability

Fully open on licence: ToolUniverse is Apache-2.0 and the skill wraps public APIs (ADMET-AI, CTD, PubChem/PubChemTox, AOPWiki, ChEMBL, STITCH, FDA, DrugBank) at no cost. No subscription, no institutional account.

The real access bar is **disclosure**. Every structure you profile is sent to third-party public services, so this recipe is unsuitable for confidential or unpublished chemistry. There is no offline substitute in the catalog today — the toxicogenomics and regulatory layers are the databases, so a local mode is not merely missing, it is not possible for those phases. If the structure cannot leave your machine, the only components you can run are local descriptor and structural-alert calculations via the [RDKit skill](../../catalog/tools/rdkit-skill.html) or [MedChem](../../catalog/tools/medchem.html), which cover step 6 and nothing else.

## Compute requirements

Laptop. Everything is API-bound; the wall clock is network round-trips, not computation. Budget on the order of a minute or two per compound across the eight phases and batch in groups of a few dozen to stay clear of public-API rate limits — a several-hundred-compound library is the wrong input for this recipe. For libraries at that scale, filter first with a bulk predictor ([ADMETlab MCP](../../catalog/tools/admetlab-mcp.html) or the [ADMET series recipe](predict-admet-properties-for-a-compound-series.html)) and reserve this dossier for the survivors.

## Evidence

Proposed. No documented attempt at this assembly — Claude Code driving the ToolUniverse Chemical Safety skill over a compound shortlist — is known, and the skill itself has not been benchmarked end-to-end. The closest evidence is component-level, and each of the recipe's gates traces to a specific published result:

- **The predictive layer is the strongest component.** ADMET-AI, which supplies the skill's phase-1 and phase-2 endpoints, holds the highest average rank on the TDC ADMET Benchmark Group leaderboard and predicts one million molecules in 3.1 hours locally ([Swanson et al. 2023](https://pubmed.ncbi.nlm.nih.gov/38234753/)). That is a benchmark of the model, not of the dossier around it — which is why step 4 keeps the predicted and experimental rows in separate, source-labelled lines.
- **Step 6's refusal to filter on alerts is the published position, not caution for its own sake.** The applicability domain of the PAINS filters is limited by the narrow proprietary data they were derived from, and matching one should not change how a compound's reported activity is treated ([Kenny 2017](https://pubmed.ncbi.nlm.nih.gov/29048168/)). Nuisance behaviour spans mechanisms — colloidal aggregation, luciferase inhibition, covalent reactivity, promiscuity — that rigid substructure filters cannot separate from genuine pharmacology; a recent multimodal model reaches macro-averaged PR-AUC 0.73 and ROC-AUC 0.94 on that four-category classification task, and the framing of the problem is itself the argument that a substructure match is a flag rather than a verdict ([Rath et al., *J Cheminform* 2026](https://doi.org/10.1186/s13321-026-01207-4)).
- The catalog records the skill as `verified: works` (2026-07-20) with security cleared against the Zitnik Lab provenance, which establishes that the tool calls resolve — not that the synthesized risk grade is calibrated.

## Alternatives considered

**A bulk ML predictor instead.** [ADMETlab MCP](../../catalog/tools/admetlab-mcp.html), driven by [predict-admet-properties-for-a-compound-series](predict-admet-properties-for-a-compound-series.html), gives calibrated per-endpoint numbers with uncertainty across a whole series, fast. Reach for it when you need to *rank* many compounds on predicted liability. Reach for this recipe when you need to *understand* a few — the toxicogenomics, adverse-outcome-pathway and regulatory layers are what a predictor cannot give you, and they are the part a reviewer will ask about. Running both and treating disagreement between the two predictive layers as a flag is a reasonable rung-3 escalation.

**Mechanistic pathway reasoning instead of a compound profile.** If the question is *how* a compound causes an effect — molecular initiating event through key events to an apical endpoint — the [Adverse Outcome Pathway skill](../../catalog/tools/tooluniverse-adverse-outcome-pathway.html) is the right sibling; this recipe touches AOPWiki only as one retrieval among eight.

**Benchmark-grade endpoint evaluation.** If you are building or validating a tox model rather than profiling a compound, use [benchmark-admet-property-with-pytdc](benchmark-admet-property-with-pytdc.html) and the [PyTDC](../../catalog/tools/pytdc.html) splits instead.

## See also

- [Chemical Safety (ToolUniverse Claude Skill)](../../catalog/tools/tooluniverse-chemical-safety.html)
- [ToolUniverse](../../catalog/tools/tooluniverse.html)
- [Predict ADMET properties for a compound series](predict-admet-properties-for-a-compound-series.html)
- [Source purchasable compounds for a hit list](source-purchasable-compounds-for-a-hit-list.html)
- [Filter virtual screening hits](filter-virtual-screening-hits.html)
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [ADMET-AI: A machine learning ADMET platform for evaluation of large-scale chemical libraries](https://pubmed.ncbi.nlm.nih.gov/38234753/) — published 2023; verified 2026-08-08 (this run).
- [Comment on The Ecstasy and Agony of Assay Interference Compounds](https://pubmed.ncbi.nlm.nih.gov/29048168/) — published 2017; canonical statement of the PAINS applicability-domain limit, verified 2026-08-08 (this run).
- [Deep learning for assay nuisance compound detection (CAGE-Fusion)](https://doi.org/10.1186/s13321-026-01207-4) — published 2026; verified 2026-08-08 (this run).
- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse) — per the catalog page, last verified 2026-07-19.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=triage-a-compound-toxicology-and-hazard-profile&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftriage-a-compound-toxicology-and-hazard-profile.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
