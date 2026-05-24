---
title: Recipes updates
parent: Updates
nav_order: 4
permalink: /updates/recipes.html
---

# Recipes updates

Reverse-chronological log of changes to the [recipes cookbook](recipes/). Newest at the top.

<!-- Curator appends new dated entries directly below this line. -->

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

- **Integrate multiple single-cell RNA-seq datasets across batches** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping the Anthropic `scvi-tools` skill for scVI / scANVI batch integration; written in response to user request [#7](https://github.com/goodb/sci-ai-enabler/issues/7); evidence grounded in Hrovatin 2025 and scIB-E 2025 ([source](https://claude.com/resources/tutorials/how-to-use-the-scvi-tools-bioinformatics-skill-bundle-with-claude)).
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
