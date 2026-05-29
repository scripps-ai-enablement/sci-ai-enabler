---
title: Recipes updates
parent: Updates
nav_order: 4
permalink: /updates/recipes.html
---

# Recipes updates

Reverse-chronological log of changes to the [recipes cookbook](recipes/). Newest at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-05-29

### Added

- **Compute HRV from an ECG recording** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [NeuroKit2 Claude skill](catalog/tools/neurokit2.html) recipe taking a single-lead ECG to validated R-peaks plus time-domain, frequency-domain, and non-linear HRV indices, with `nk.signal_quality`-driven epoch exclusion. Second Neuroscience-primary recipe in the cookbook (joins the Neuropixels spike-sorting recipe). Component evidence: [Makowski et al. *Behavior Research Methods* 2021](https://doi.org/10.3758/s13428-020-01516-y) (NeuroKit2 reference) and [Pham et al. *Sensors* 2021](https://doi.org/10.3390/s21123998) (HRV indices tutorial). Closest LLM-orchestrated analogue: [EEGAgent (Yan et al., arXiv:2511.09947, 2025-11-12)](https://arxiv.org/abs/2511.09947), AAAI-26 — different signal modality and custom toolbox, not NeuroKit2.

### Updated

- Nav orders rebalanced across the recipe set to keep alphabetical ordering after the addition: **Assemble Census atlas** → 1, **Build target dossier** → 2, **Compute HRV** → 3, **Estimate PK** → 4, **Filter virtual screening** → 5, **Infer GRN** → 6, **Integrate single-cell** → 7, **Interpret clinical variant** → 8, **Match patient to trials** → 9, **Profile polypharmacology** → 10, **Run bulk RNA-seq DE** → 11, **QC single-cell** → 12, **Scan repurposing** → 13, **Sort spikes** → 14, **Triage preprints** → 15, **Triage AlphaFold** → 16.

### Verified (no changes)

- 4 recipes spot-checked at the 30-day boundary and bumped to `last_verified: 2026-05-29` — **Triage preprints**, **QC single-cell**, **Build target dossier**, **Run bulk RNA-seq DE**. All linked catalog tools (bio-research, pubmed, single-cell-rna-qc, pydeseq2, open-targets, uniprot, alphafold, depmap) remain present and unflagged.

### User requests

- **#12** (`claude:recipe-feedback`) — remains in `## User requests (open)`; `gh` CLI is not available in this run's environment so the issue body still cannot be inspected. Retry on the next run that has `gh` access.

## 2026-05-28

### Added

- **Assemble a tissue reference atlas from the CELLxGENE Census** (Problem class: Data analysis; Evidence: Reported) — rung-2 [cellxgene-census skill](catalog/tools/cellxgene-census.html) recipe pulling a versioned AnnData slice from the CZ CELLxGENE Discover Census with the CZ-trained scVI embedding attached for reference mapping. First Molecular and Cellular Biology focus-day recipe to consume the Census. Evidence anchored in the Census team's [`comp_bio_data_integration_scvi` notebook](https://chanzuckerberg.github.io/cellxgene-census/notebooks/analysis_demo/comp_bio_data_integration_scvi.html), the [scvi-hub paper](https://www.nature.com/articles/s41592-025-02799-9) (Ergen et al., *Nature Methods* 2025), and the [integrated human lung atlas](https://doi.org/10.1038/s41591-023-02327-2) (Sikkema et al., *Nature Medicine* 2023).
- **Infer a gene-regulatory network from single-cell RNA-seq** (Problem class: Data analysis; Evidence: Reported) — rung-2 [Arboreto skill](catalog/tools/arboreto.html) recipe running GRNBoost2 on a QC'd / integrated AnnData with a TF-restricted regressor and seed-stabilised reruns; produces the ranked TF–target edge table that pySCENIC consumes downstream. Evidence anchored in [Moerman et al. *Bioinformatics* 2019](https://doi.org/10.1093/bioinformatics/bty916) (GRNBoost2), [Van de Sande et al. *Nature Protocols* 2020](https://doi.org/10.1038/s41596-020-0336-2) (SCENIC workflow), and [Bravo González-Blas et al. *Nature Methods* 2023](https://doi.org/10.1038/s41592-023-01938-4) (SCENIC+).

### Updated

- Nav orders rebalanced across the recipe set to keep alphabetical ordering after the two additions: **Assemble Census atlas** → 1, **Build target dossier** → 2, **Estimate PK** → 3, **Filter virtual screening** → 4, **Infer GRN** → 5, **Integrate single-cell** → 6, **Interpret clinical variant** → 7, **Match patient to trials** → 8, **Profile polypharmacology** → 9, **Run bulk RNA-seq DE** → 10, **QC single-cell** → 11, **Scan repurposing** → 12, **Sort spikes** → 13, **Triage preprints** → 14, **Triage AlphaFold** → 15.

### Missing components flagged to the catalog curator

- **pySCENIC wrapper (cisTarget + AUCell)** — would unlock the full SCENIC pipeline downstream of the new GRN-inference recipe (motif filtering against cisTarget databases, per-cell regulon AUCell scoring).

### Verified (no changes)

- All 13 pre-existing recipes have `last_verified` within the 30-day window (oldest 2026-05-21); no aging verifications were due this run.

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
