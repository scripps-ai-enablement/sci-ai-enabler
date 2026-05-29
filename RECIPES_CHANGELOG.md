---
title: Recipes updates
parent: Updates
nav_order: 4
permalink: /updates/recipes.html
---

# Recipes updates

Reverse-chronological log of changes to the [recipes cookbook](recipes/). Newest at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-05-27

### Added

- **Estimate pharmacokinetic properties of a small molecule** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-3 RDKit + MedChem + ChEMBL assembly producing a descriptor / rule-based / analog-anchored PK card for a single SMILES. Ships in response to user request [#8](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/8). Closest documented analogues: [ChemCrow](https://doi.org/10.1038/s42256-024-00832-8) (Bran et al., *Nature Machine Intelligence* 2024) and [PharmaBench](https://doi.org/10.1038/s41597-024-03731-0) (Niu et al., *Scientific Data* 2024).
- **Triage an AlphaFold model for structure-based drug design** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-2 [AlphaFold MCP](catalog/tools/alphafold.html) recipe producing a pLDDT-anchored go/refine/fall-back-to-PDB verdict on a UniProt accession. First Integrative Structural and Computational Biology-primary recipe. Evidence grounded in the EBI AlphaFold DB papers ([Varadi 2022](https://doi.org/10.1093/nar/gkab1061), [Varadi 2024](https://doi.org/10.1093/nar/gkad1011)), the interface-pLDDT benchmark ([Bryant 2022](https://doi.org/10.1038/s41467-022-28865-w)), and the AlphaFold-for-docking assessment ([Karelina 2023](https://doi.org/10.1021/acs.jcim.3c00601)).

### Updated

- Nav orders rebalanced across the recipe set to keep alphabetical ordering after the two additions: **Estimate PK properties** → 2, **Filter virtual screening hits** → 3, **Integrate single-cell datasets** → 4, **Interpret clinical variant** → 5, **Match patient to trials** → 6, **Profile polypharmacology** → 7, **Run bulk RNA-seq DE** → 8, **QC single-cell RNA-seq** → 9, **Scan repurposing candidates** → 10, **Sort spikes** → 11, **Triage preprints** → 12, **Triage AlphaFold model** → 13.

### Missing components flagged to the catalog curator

- **ADMET-AI / AdmetLab 3.0 / Deep-PK wrapper** — would let the new PK-properties recipe move from descriptor-and-analog estimation to defensible ML prediction for CYP / hERG / microsomal endpoints.
- **DeepChem (K-Dense Skill)** — already flagged in the catalog curator's state; would also strengthen the PK-properties recipe.
- **Co-folding / AlphaFold-Multimer / Boltz-2 wrapper** — would unlock a complex-modelling companion to the AlphaFold triage recipe.

### Verified (no changes)

- All recipes have `last_verified` within the 30-day window; no aging verifications were due this run.

## 2026-05-25

### Added

- **Filter a virtual screening hit list with drug-likeness rules and structural alerts** (Problem class: Data analysis; Evidence: Reported) — rung-2 [MedChem](catalog/tools/medchem.html) + [Datamol](catalog/tools/datamol.html) cascade for Lipinski → Veber → PAINS → BRENK triage of SMILES hit lists. First Chemistry-primary recipe in the cookbook. Evidence anchored in the K-Dense lead-optimisation workflow and the foundational filter papers ([Baell & Holloway PAINS 2010](https://doi.org/10.1021/jm901137j), [Brenk 2008](https://doi.org/10.1002/cmdc.200700139), [Lipinski 2001](https://doi.org/10.1016/S0169-409X(00)00129-0), [Veber 2002](https://doi.org/10.1021/jm020017n)).
- **Profile a compound's polypharmacology from ChEMBL bioactivity data** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 single-tool recipe over the [ChEMBL connector](catalog/tools/chembl.html). Second Chemistry-primary recipe and the compound-centric mirror of the existing target-dossier recipe. Evidence grounded in the [Anthropic ChEMBL Connector tutorial](https://claude.com/resources/tutorials/using-the-chembl-connector-in-claude) and the ChEMBL curation paper ([Mendez et al., *NAR* 2019](https://doi.org/10.1093/nar/gky1075)).

### Updated

- **Integrate multiple single-cell RNA-seq datasets across batches** — nav_order 2 → 3 for alphabetical position after the new Filter recipe.
- **Interpret a clinical variant from a natural-language query** — nav_order 3 → 4.
- **Match a patient summary to recruiting clinical trials** — nav_order 4 → 5.
- **Run bulk RNA-seq differential expression from a counts matrix** — nav_order 5 → 7 (after the new Profile recipe).
- **Run first-pass QC on a single-cell RNA-seq dataset** — nav_order 6 → 8.
- **Scan approved drugs for repurposing candidates against a disease** — nav_order 7 → 9.
- **Sort spikes from a Neuropixels recording end-to-end** — nav_order 8 → 10.
- **Triage a stack of new preprints in your field** — nav_order 9 → 11.

### Verified (no changes)

- 9 existing recipes spot-checked; all `last_verified` dates within the 30-day window, all linked catalog pages resolve.

## 2026-05-24

### Added

- **Scan approved drugs for repurposing candidates against a disease** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-3 toolbelt composing the [Open Targets plugin](catalog/tools/open-targets.html), [ChEMBL connector](catalog/tools/chembl.html), and [DrugBank MCP](catalog/tools/drugbank.html); first focused Drug Repurposing and Discovery recipe in the cookbook. Evidence anchors: [DeepDrug Alzheimer's repurposing graph](https://www.nature.com/articles/s41598-025-85947-7) (Li et al., *Scientific Reports* 2025), [Robin / ripasudil dAMD discovery](https://doi.org/10.1038/s41586-026-10652-y) (Ghareeb et al., *Nature* 2026), and [DREBIOP LLM-validation benchmark](https://www.biorxiv.org/content/10.1101/2025.06.13.659527v1) (Zunzunegui Sanz et al., *bioRxiv* 2025-06-13).

### Updated

- **Sort spikes from a Neuropixels recording end-to-end** — nav_order 7 → 8 for alphabetical position.
- **Triage a stack of new preprints in your field** — nav_order 8 → 9 for alphabetical position.

### Verified (no changes)

- 8 existing recipes spot-checked; all `last_verified` dates within the 30-day window, all linked catalog pages resolve.

## 2026-05-23

### Added

- **Match a patient summary to recruiting clinical trials** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 BioMCP / cyanheads-ClinicalTrials.gov-MCP recipe; first Translational-Medicine-focused recipe in the cookbook. Evidence grounded in TrialGPT ([Jin et al., *Nature Communications* 2024](https://www.nature.com/articles/s41467-024-53081-z), 87.3% criterion-matching accuracy).
- **Interpret a clinical variant from a natural-language query** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-2 BioMCP recipe; pairs with the trial-matching recipe for variant-driven enrollment. Closest analogous benchmark is MARRVEL-MCP ([bioRxiv 2025-11](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1)).

### Updated

- **Run bulk RNA-seq differential expression from a counts matrix** — nav_order 3 → 5 for alphabetical position after the two new TM recipes.
- **Run first-pass QC on a single-cell RNA-seq dataset** — nav_order 4 → 6 for alphabetical position.
- **Sort spikes from a Neuropixels recording end-to-end** — nav_order 5 → 7 for alphabetical position.
- **Triage a stack of new preprints in your field** — nav_order 6 → 8 for alphabetical position.

### Verified (no changes)

- 5 existing recipes spot-checked; all `last_verified` dates within the 30-day window, all linked catalog pages resolve.

## 2026-05-22

### Added

- **Integrate multiple single-cell RNA-seq datasets across batches** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping the Anthropic `scvi-tools` skill for scVI / scANVI batch integration; written in response to user request [#7](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/7); evidence grounded in Hrovatin 2025 and scIB-E 2025 ([source](https://claude.com/resources/tutorials/how-to-use-the-scvi-tools-bioinformatics-skill-bundle-with-claude)).
- **Sort spikes from a Neuropixels recording end-to-end** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping the K-Dense `neuropixels-analysis` skill (SpikeInterface + Kilosort4); first Neuroscience-only recipe in the cookbook ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/neuropixels-analysis/SKILL.md)).

### Updated

- **Run bulk RNA-seq differential expression from a counts matrix** — nav_order shifted 2 → 3 for alphabetical position.
- **Run first-pass QC on a single-cell RNA-seq dataset** — nav_order shifted 3 → 4 for alphabetical position.
- **Triage a stack of new preprints in your field** — nav_order shifted 4 → 6 for alphabetical position.

### Verified (no changes)

- 4 existing recipes spot-checked (all linked catalog pages resolve; `last_verified` 2026-05-21 still within the 30-day window so no bumps).

## 2026-05-21

### Added

- **Run first-pass QC on a single-cell RNA-seq dataset** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping Anthropic's `single-cell-rna-qc` skill for canonical scverse MAD-based filtering of 10x `.h5` / AnnData `.h5ad` inputs ([source](https://claude.com/resources/tutorials/how-to-use-the-single-cell-rna-qc-skill-with-claude)).
- **Run bulk RNA-seq differential expression from a counts matrix** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping the K-Dense PyDESeq2 skill for negative-binomial GLM differential expression, including pseudobulk single-cell handoff guidance ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/pydeseq2/SKILL.md)).
- **Build a target dossier from gene name to structure to cancer dependency** (Problem class: Knowledge synthesis; Evidence: Proposed) — first rung-3 toolbelt recipe composing Open Targets, UniProt, AlphaFold, and DepMap into a one-page target dossier; first `Proposed`-evidence entry in the cookbook ([closest analogue](https://doi.org/10.1101/2025.05.30.656746)).

### Updated

- **Triage a stack of new preprints in your field** — nav_order shifted from 1 to 4 to reflect alphabetical ordering after the three new Mol/Cell Bio additions; no content changes.

### Verified (no changes)

- 1 recipe spot-checked, current (`triage-new-preprints`, last_verified 2026-05-21).

## 2026-05-21 (initial seed)

### Added

- **Section bootstrap** — `recipes/` section created with landing page, landscape page, and the all-recipes index; `recipes/curator-state.md` initialized; `RECIPES_CHANGELOG.md` (this file) created. Curator prompt and daily workflow added at `RECIPE_AGENT.md` and `.github/workflows/recipes.yml`.
- **Triage a stack of new preprints in your field** (Problem class: Literature triage; Evidence: Reported) — first seed recipe demonstrating the schema and the lowest rung of the simplicity ladder (Claude Code alone + bioRxiv MCP) ([source](https://github.com/biorxiv/biorxiv-mcp)).
