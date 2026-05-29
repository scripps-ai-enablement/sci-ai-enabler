---
title: Integrate multiple single-cell RNA-seq datasets across batches
parent: All recipes
grand_parent: Recipes
nav_order: 8
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology, Neuroscience]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-05-22
summary: Use the scvi-tools skill in Claude Code to fit scVI (or scANVI when labels are available) on a concatenated AnnData of multiple batches, returning a batch-corrected latent space and integrated UMAP.
---

# Integrate multiple single-cell RNA-seq datasets across batches

Hand Claude Code two or more single-cell RNA-seq AnnData files from different donors, tissues, or technologies; get back a single AnnData with a batch-corrected latent representation, an integrated UMAP, and (if cell-type labels exist in one batch) scANVI-propagated labels in the others.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology, Neuroscience |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

Almost no real single-cell study sits in one batch. Donors, capture days, 10x chemistries, and sequencing runs each contribute technical variance that swamps biology if you cluster the concatenated raw counts. Integration is the step that aligns shared cell states across batches while preserving batch-specific biology, and it has to happen before clustering, annotation, or differential expression. Solved looks like: one AnnData with `obsm["X_scVI"]` (the corrected latent), a UMAP where cell types co-locate across batches, and — when at least one batch is labeled — propagated labels on the others via scANVI.

The harder problem hidden inside this is choosing a method that does not over-correct away real biology. Recent benchmarks (Hrovatin 2025; Yi 2025) show every integration method trades off batch-mixing against biological conservation, so the recipe has to name the right tool *and* the knobs that matter.

## Recommended approach

1. **QC each batch first.** Run the [single-cell-rna-qc](../../catalog/tools/single-cell-rna-qc.html) skill once per input file so the inputs into integration are already MAD-filtered. See the [QC recipe](qc-single-cell-rna-seq.html). Skipping this step makes integration look worse than it is.

2. **Install the [scvi-tools skill](../../catalog/tools/scvi-tools.html)** in Claude Code:

   ```
   /plugin marketplace add anthropics/life-sciences
   /plugin install scvi-tools@life-sciences
   ```

   Confirm with `/plugin list`. You will also want the [AnnData skill](../../catalog/tools/anndata.html) installed to make the concatenation step idiomatic.

3. **Concatenate the QC'd batches into one AnnData, keeping a `batch` column.** A minimal prompt:

   ```
   I have three QC'd .h5ad files: data/donorA_qc.h5ad,
   data/donorB_qc.h5ad, data/donorC_qc.h5ad. Use the AnnData skill
   to concatenate them along obs with join="outer", writing a
   "batch" column from the source filename. Keep raw counts in a
   "counts" layer. Save to data/combined.h5ad and print the obs and
   var shapes.
   ```

4. **Fit scVI for unsupervised batch correction.** Drive the scvi-tools skill with explicit batch key and a raw-count layer:

   ```
   Use the scvi-tools skill on data/combined.h5ad:
     - setup_anndata with layer="counts", batch_key="batch"
     - n_latent=30, n_layers=2, gene_likelihood="nb"
     - train on GPU with early stopping
     - write get_latent_representation() to obsm["X_scVI"]
     - compute neighbors and UMAP from X_scVI
     - save to data/combined_scvi.h5ad and emit a UMAP coloured by
       batch and by leiden clusters into figures/integration/.
   ```

5. **If at least one batch is labeled, propagate with scANVI.** Add a step after scVI:

   ```
   Take the trained scVI model and run scANVI initializing from it,
   using "cell_type" as the labels_key and "Unknown" as
   unlabeled_category. Train, then write the predicted labels to
   obs["scANVI_label"] and a confusion table for the labeled batch.
   ```

6. **Sanity-check with scIB metrics before publishing.** Ask Claude to run the standard `scib-metrics` panel (silhouette by batch / by label, kBET, graph connectivity, iLISI/cLISI) on `X_scVI` vs an uncorrected PCA baseline. If batch-removal scores collapse but biological-conservation scores tank, lower `n_latent` or use scANVI with stronger label supervision; if the reverse, raise `n_latent` or add `n_layers`. Hrovatin 2025 documents this trade-off in detail.

7. **Hand off to downstream Scanpy work.** The integrated AnnData is the standard input for the [Scanpy-MCP](../../catalog/tools/scanpy.html) — use it for clustering, marker gene calls, and DE per cell type.

## Why this assembly

Rung 2 of the simplicity ladder. The skill encapsulates a deep-learning method (scVI / scANVI) with very specific input requirements — raw counts, registered AnnData, GPU-friendly training — and the [scvi-tools skill](../../catalog/tools/scvi-tools.html) is the recipe that documents how Claude should call it. Plain Claude Code would have to invent that boilerplate from scratch every session; the dedicated skill makes the workflow reproducible. There is no need for a toolbelt or autonomous system here — integration is a single-step problem with one canonical method family.

## Availability

Fully open. The scvi-tools skill ships in the `anthropics/life-sciences` marketplace under Apache-2.0; the underlying `scvi-tools` library is BSD-3-Clause; AnnData is BSD. Any current Claude plan supports the skill. No institutional license required.

## Compute requirements

Workstation with GPU recommended. scVI trains in tens of minutes on a single CUDA GPU (8–12 GB VRAM) for a typical 50k-cell, 3-batch dataset. CPU training works but is roughly 10× slower. For atlas-scale runs (>500k cells), expect 1–3 hours on a single A100 / H100 and 32+ GB system RAM. Storage: budget ~3× the size of the concatenated `.h5ad` for the trained model artifacts and saved latent.

## Evidence

Reported. The scvi-tools skill's [Anthropic tutorial](https://claude.com/resources/tutorials/how-to-use-the-scvi-tools-bioinformatics-skill-bundle-with-claude) documents this assembly end-to-end on a multi-batch example. The underlying method evidence is strong: Hrovatin et al. ([*Genome Biology* 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12577435/)) and Yi et al. ([scIB-E preprint 2024, doi:10.1101/2024.12.09.627450](https://doi.org/10.1101/2024.12.09.627450)) both rank scVI / scANVI among the leading deep-learning integration methods on the scIB benchmark, with scANVI gaining ~6.5% biological conservation over scVI at the cost of ~5.6% batch-removal — the trade-off the recipe surfaces in step 6.

No peer-reviewed benchmark of "Claude + scvi-tools skill" against a hand-coded scvi-tools pipeline is known. The agent loop adds reproducibility and convenience, not new analytical capability.

## Alternatives considered

- **Plain Claude Code, no skill.** Works but error-prone. The most common failure modes — forgetting `layer="counts"` (scVI silently trains on log-normalized data), forgetting `batch_key`, mismatched gene sets — are exactly what the skill is designed to prevent.
- **Scanpy-MCP with Harmony.** Harmony is faster and runs on CPU. Hrovatin 2025 finds it competitive on within-cell-type preservation but weaker on cross-species batches and on heavy batch effects. Reach for Harmony when you need a 60-second integration on a laptop; reach for scVI when the batches are heterogeneous or you want propagated labels.
- **An autonomous-science system (Biomni).** Overkill for a single integration step. Biomni's published case studies include >336,000-nucleus integrations, but the recipe to integrate two donors and call clusters does not need an autonomous loop.
- **scIB benchmarking only.** If your goal is *choosing* a method rather than running one, run `scib-metrics` on multiple methods directly instead — that's a different recipe (deferred).

## See also

- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — the upstream step before integration.
- [scvi-tools (Claude Skill)](../../catalog/tools/scvi-tools.html)
- [AnnData (Claude Skill)](../../catalog/tools/anndata.html)
- [Scanpy-MCP](../../catalog/tools/scanpy.html)
- [Biomni](../../autonomous-science/systems/biomni.html) — for autonomous pipelines that include integration as one node.

## Sources

- [scvi-tools skill tutorial (Anthropic)](https://claude.com/resources/tutorials/how-to-use-the-scvi-tools-bioinformatics-skill-bundle-with-claude) — published 2025-10; verified 2026-05-22 (this run).
- [Hrovatin K. et al., "Integrating single-cell RNA-seq datasets with substantial batch effects" (PMC12577435)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12577435/) — published 2025.
- [Yi C. et al., scIB-E preprint, doi:10.1101/2024.12.09.627450](https://doi.org/10.1101/2024.12.09.627450) — posted 2024-12-09.
- [scvi-tools documentation](https://docs.scvi-tools.org/) — verified 2026-05-22 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=integrate-single-cell-datasets&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fintegrate-single-cell-datasets.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
