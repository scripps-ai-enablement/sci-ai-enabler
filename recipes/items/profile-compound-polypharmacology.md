---
title: Profile a compound's polypharmacology from ChEMBL bioactivity data
parent: All recipes
grand_parent: Recipes
nav_order: 9
problem_class: Knowledge synthesis
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-05-25
summary: Use the ChEMBL connector in Claude Code to pull every measured activity for one compound, group by target and assay, and surface the off-target profile a medicinal chemist needs before committing to a chemotype.
---

# Profile a compound's polypharmacology from ChEMBL bioactivity data

Hand Claude Code a SMILES or ChEMBL ID; get back a target-by-target table of measured potencies, the assay descriptions behind each number, and a flagged short-list of off-targets that warrant counter-screening before the chemotype goes any further.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A new lead's *intended* target is the easy part — that comes free with the project. The hard part is the rest of the activity profile: every other protein the molecule was ever tested against, the assays behind those numbers, and whether the off-targets are dose-relevant. Medicinal chemists need this before they invest in analogs; pharmacologists need it before they pick an animal model; safety scientists need it before tox planning. The reference data is in ChEMBL — manually curated from medicinal-chemistry literature, with IC50 / Ki / Kd values, pChEMBL scores, and the assay descriptions — but pulling it cleanly for a single compound by name or SMILES and grouping it by target takes more REST calls than a chemist wants to write.

Solved looks like: one prompt, one table, one screen. Compound name in; target / standard relation / standard value / standard units / assay description / pChEMBL / ChEMBL document ID out, sorted by potency. Off-targets within 10-fold of the intended target flagged.

## Recommended approach

1. **Install the [ChEMBL connector](../../catalog/tools/chembl.html).** Two options depending on the surface:

   - **Claude Code** — plugin marketplace:
     ```
     /plugin marketplace add anthropics/life-sciences
     /plugin install chembl@life-sciences
     ```
     Restart, then `/mcp` to confirm.
   - **Claude.ai (Team / Enterprise or individual)** — Settings → Connectors → ChEMBL → **Connect**.

2. **Resolve the compound, then pull every activity.** A minimal prompt:

   ```
   Compound: imatinib (or paste a SMILES / ChEMBL ID).

   Use the ChEMBL connector:
     1. compound_search to resolve to a ChEMBL molecule ID.
        Print the canonical SMILES, max phase, ATC code, and synonyms.
     2. get_bioactivity for that ChEMBL ID. Keep only rows with
        standard_type in {IC50, Ki, Kd, EC50}, standard_relation = "=",
        standard_units = "nM", and pchembl_value not null.
     3. Group by target ChEMBL ID and target pref_name. For each
        target, report: median pchembl, n measurements, best (lowest)
        nM value and its document_chembl_id, and the assay_description
        of the best measurement.

   Sort by median pchembl descending. Emit as a markdown table.
   ```

3. **Flag the polypharmacology.** Add a follow-up:

   ```
   For the intended target (ABL1 in the imatinib example),
   list every other target whose best measured value is within
   10-fold of the intended target's best value. For each off-target,
   give the ChEMBL document_chembl_id and a one-sentence note on
   whether the off-target is in a related family (e.g., another
   tyrosine kinase) or a clearly unrelated protein.
   ```

   The 10-fold cut-off is the standard rule of thumb for "this is plausibly hit in vivo at the dose that hits the intended target"; tune to project context.

4. **Cross-reference mechanism if the compound is approved.** ChEMBL `get_mechanism` returns curated MoA. Add:

   ```
   If max phase >= 3, call get_mechanism for this molecule and
   print the action_type and target. Compare to the polypharmacology
   table — flag any approved mechanism target that does NOT appear
   in the bioactivity hits (sign that the curated MoA target may not
   be the highest-potency target measured).
   ```

5. **Persist the table.** Save the markdown plus the underlying JSON to `compounds/<name>_profile_<date>.md` and `.json`. ChEMBL refreshes quarterly; re-run any time a new release lands to catch added measurements.

## Why this assembly

Rung 2 of the simplicity ladder. ChEMBL is the canonical source for measured bioactivity, and the [ChEMBL connector](../../catalog/tools/chembl.html) wraps six tool calls — `compound_search`, `target_search`, `get_bioactivity`, `get_mechanism`, plus cross-reference and metadata — that map directly onto this question. Plain Claude Code with raw HTTP could hit the REST API but loses the curated, scoped tool surface and the typed responses. A multi-tool harness is unnecessary — every column on the desired output table comes from ChEMBL.

## Availability

Fully open. The ChEMBL connector is GA in the `anthropics/life-sciences` marketplace; ChEMBL data is CC-BY-SA-3.0. No subscription, no institutional licence. Any current Claude plan supports the connector.

## Compute requirements

Laptop. The full bioactivity profile for a well-studied drug (imatinib has ~6 000 ChEMBL measurements) returns in <30 seconds over the HTTP MCP transport; obscure compounds with <100 measurements return in <5 seconds. No local compute beyond the Claude client.

## Evidence

Reported. Anthropic's [ChEMBL Connector tutorial](https://claude.com/resources/tutorials/using-the-chembl-connector-in-claude) walks through this exact assembly — compound resolution → bioactivity pull → target grouping — for medicinal-chemistry SAR work. The underlying ChEMBL bioactivity workflow is the de-facto reference for polypharmacology profiling: Mendez et al. ([*Nucleic Acids Res.* 2019, 47:D930](https://doi.org/10.1093/nar/gky1075)) describe the curation pipeline, and ChEMBL underpins the off-target benchmarks in DeepDrug (Li et al., *Sci. Rep.* 2025) and the ToolUniverse polypharmacology evaluations (Lin et al., *bioRxiv* 2024).

No peer-reviewed benchmark of "Claude + ChEMBL connector" vs a hand-written ChEMBL REST script is known — the productivity gain is the named tool surface, not new data. ChEMBL coverage is itself a known limitation: the activities are only what literature reports, with selection bias toward published positive results.

## Alternatives considered

- **PubChem MCP alone.** [PubChem](../../catalog/tools/pubchem.html) covers a wider compound universe but its assay data is heterogeneous and lacks the pChEMBL normalisation. Use it when a compound is not in ChEMBL at all; use ChEMBL when both have records.
- **Open Targets plugin.** [Open Targets](../../catalog/tools/open-targets.html) is target-centric (disease → target → drug), not compound-centric — wrong axis for this question.
- **DrugBank MCP.** [DrugBank](../../catalog/tools/drugbank.html) gives mechanism, indications, and interactions for approved drugs, not raw bioactivity at off-targets. Reach for it after this recipe, not instead of it.
- **ToolUniverse harness.** [ToolUniverse](../../catalog/tools/tooluniverse.html) bundles ChEMBL alongside 600+ other tools. Worth it if the workflow needs *more* than polypharmacology — for the single-question case here, the focused ChEMBL connector is the lower rung.

## See also

- [ChEMBL Connector](../../catalog/tools/chembl.html)
- [PubChem MCP Server](../../catalog/tools/pubchem.html)
- [Filter a virtual screening hit list with drug-likeness rules and structural alerts](filter-virtual-screening-hits.html) — what to do *before* a compound earns a polypharmacology profile.
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — the target-centric mirror of this recipe.
- [Scan approved drugs for repurposing candidates against a disease](scan-drug-repurposing-candidates.html) — bulk version of the same lookup, target-driven.

## Sources

- [Anthropic tutorial — Using the ChEMBL Connector in Claude](https://claude.com/resources/tutorials/using-the-chembl-connector-in-claude) — verified 2026-05-25 (this run).
- [`anthropics/life-sciences` marketplace](https://github.com/anthropics/life-sciences) — verified 2026-05-25 (this run).
- [Mendez D. et al., "ChEMBL: towards direct deposition of bioassay data," *Nucleic Acids Res.* 2019](https://doi.org/10.1093/nar/gky1075) — published 2018-11.
- [ChEMBL — EMBL-EBI](https://www.ebi.ac.uk/chembl/) — verified 2026-05-25 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=profile-compound-polypharmacology&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fprofile-compound-polypharmacology.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
