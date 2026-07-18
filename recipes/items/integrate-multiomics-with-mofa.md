---
title: Integrate multi-omics layers into interpretable factors with MOFA+
parent: All recipes
grand_parent: Recipes
nav_order: 15
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology, Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-18
summary: Use the MOFA+ Claude skill to jointly decompose several omics layers on the same samples into a handful of latent factors, then read off which factors capture biology and which layers drive them.
---

# Integrate multi-omics layers into interpretable factors with MOFA+

Hand Claude Code two or more omics matrices measured on the same samples or cells (e.g., RNA + ATAC + protein, or transcriptome + methylation + CNV); get back a trained MOFA+ model, a variance-explained breakdown per factor per layer, factor–metadata associations, and the top feature loadings that make each factor interpretable.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology, Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Multi-omics studies measure several molecular layers on one set of samples — transcriptome, chromatin accessibility, methylation, surface protein, copy number — and the analyst has to find the axes of variation shared across layers versus those private to one. Concatenating the matrices and running PCA mixes scales and lets the highest-variance layer dominate; analyzing each layer separately misses the cross-layer structure that is usually the point. MOFA+ solves this by fitting an unsupervised factor model that, like PCA, returns a low-dimensional latent space, but decomposes the variance *per factor per layer* — so you can see that Factor 1 is driven by RNA+methylation while Factor 3 is ATAC-only, and correlate each factor with sample metadata (subtype, survival, treatment). Solved looks like: a trained model, a variance-decomposition heatmap, a table of factors ranked by association with your outcome, and the top-loading features per factor as the biological handle — all reproducible from a committed script.

This is a different problem from batch integration. [scVI integration](integrate-single-cell-datasets.html) aligns *the same modality across batches*; MOFA+ integrates *different modalities of the same samples* into shared factors. Reach for MOFA+ when the layers differ, not when the batches do.

## Recommended approach

1. **Assemble one view per omics layer, aligned on the same samples/cells.** Each view is a `(samples × features)` matrix; features can differ across views but the sample axis must match. For single-cell multi-modal data (10x Multiome, CITE-seq), build a MuData object with the [muon skill](../../catalog/tools/muon-multiomics-singlecell.html); for bulk multi-omics, a dict of AnnData views is enough (see the [AnnData skill](../../catalog/tools/anndata.html)). Feature-select each view first (e.g., highly variable genes/peaks) — MOFA+ scales poorly with tens of thousands of features per view and factors get noisier.

2. **Install the [MOFA+ skill](../../catalog/tools/mofaplus-multi-omics.html).** From the SciAgent-Skills collection:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm it appears under `/plugin` → Installed. The skill runs `mofapy2` locally via Bash/Python; install its declared dependencies when prompted.

3. **Have the skill build the model, train, and write the artifact.** Drive it to a versioned script — a minimal prompt:

   ```
   Use the mofaplus-multi-omics skill. Load these views (samples on
   the shared axis):
     - rna:    data/rna_hvg.h5ad
     - atac:   data/atac_features.h5ad
     - protein: data/adt.h5ad
   Build a MOFA+ model, scale each view, train with 15 factors and
   the default convergence settings, seed=1. Write the workflow to a
   committed script mofa_run.py that:
     - trains the model and saves it to results/mofa_model.hdf5
     - writes results/variance_explained.csv (factor x view)
     - writes results/factor_metadata_assoc.csv (Pearson/ANOVA of
       each factor vs the columns in obs: subtype, treatment, ...)
     - writes results/top_loadings_<view>.csv (top 30 features per
       factor per view)
     - saves the variance-decomposition heatmap to figures/.
   Pin the environment in requirements.txt.
   ```

4. **Read the model as a diagnostic, not a black box.** Drop factors that explain negligible variance across all views; a factor loading on a single view at high variance often flags a technical or batch axis rather than biology. Ask the skill to correlate factors against known covariates (batch, library size, percent-mito) as a sanity check before interpreting any factor as a biological program.

5. **Ground the interpretation and hand off.** Ask Claude to name only factors and features that appear in the saved CSVs, citing the variance-explained and loading values. Feed the top-loading gene list of an interesting factor into the [functional-enrichment recipe](run-functional-enrichment-on-a-gene-list.html) to annotate its biology.

6. **Record provenance.** Emit a `provenance.json` capturing the MOFA+/`mofapy2` and muon versions, the number of factors and seed, per-view feature counts, input file sha256s, the run date, and the model id. `mofapy2` training is stochastic in initialization; the seed plus the saved `mofa_model.hdf5` make the run re-attributable. Keep `mofa_run.py`, `requirements.txt`, the CSV tables, and `provenance.json` under version control.

## Why this assembly

Rung 2 of the simplicity ladder. Multi-omics factor analysis is a single statistical procedure with one canonical implementation (`mofapy2`), and the MOFA+ skill encapsulates the view-construction, scaling, training, and variance-decomposition idioms that are easy to get wrong by hand. Plain Claude Code (rung 1) can write `mofapy2` code from docs but reliably fumbles the view-scaling and the per-view feature-selection footgun. A toolbelt (rung 3) buys nothing — the muon/AnnData helper is just the data container feeding the one core skill. Autonomous systems (rung 4) are the wrong tier for a bounded, single-model decomposition.

## Availability

Fully open. The MOFA+ and muon skills are community OSS in [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) (CC BY 4.0 collection); `mofapy2` is LGPL-3.0; muon/MuData is BSD-3-Clause. No subscription, no institutional access, no API key — all computation is local.

## Compute requirements

Laptop-sufficient for typical designs. MOFA+ variational inference on a few thousand samples/cells × a few thousand features per view across 3–4 views trains in minutes to tens of minutes on CPU; no GPU. Memory is dominated by the input views held in memory. Very wide views (tens of thousands of features) or hundreds of thousands of cells push training to tens of minutes–hours and 16–32 GB RAM — feature-select aggressively (step 1) rather than throwing raw matrices at the model, and downsample cells per group if needed.

## Evidence

Proposed. No documented end-to-end attempt of "Claude + the MOFA+ skill" on a real dataset, with quantitative pass/fail, is known to the curator. The evidence is component-level and strong:

- **MOFA+ is the reference method** for unsupervised multi-omics factor analysis, introduced with variational inference, flexible sparsity, and multi-group/multi-modal support ([Argelaguet et al., "MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data," *Genome Biology* 21:111, 2020](https://doi.org/10.1186/s13059-020-02015-1); [PMID 32393329](https://pubmed.ncbi.nlm.nih.gov/32393329/)), building on the original MOFA ([Argelaguet et al., *Mol. Syst. Biol.* 2018](https://doi.org/10.15252/msb.20178124)).
- **The exact workflow is used in current biomedical practice.** A 2026 study applied MOFA+ to transcriptomic, methylation, and genomic profiles of 667 TCGA diffuse gliomas, derived 12 latent factors, and validated a factor-score prognostic signature across two independent cohorts (n = 1685 total) without retraining ([Saleh et al., *Cancers* 18:1652, 2026](https://doi.org/10.3390/cancers18101652); [PMID 42193012](https://pubmed.ncbi.nlm.nih.gov/42193012/)) — the same load-views → train → variance-decompose → correlate-with-outcome pattern this recipe automates.
- **No head-to-head benchmark** of the skill-driven assembly versus hand-written `mofapy2` code is published; the skill buys reproducibility and the pinned view/scaling/seed choices, not new statistics. The closest catalogued-component sibling is the [scVI integration recipe](integrate-single-cell-datasets.html), which drives a different skill on the batch-integration problem.

## Alternatives considered

- **scVI/scANVI batch integration (rung 2).** [Integrate multiple single-cell RNA-seq datasets](integrate-single-cell-datasets.html) is the answer when the layers are the *same modality across batches*. Use it for donor/technology harmonization; use MOFA+ for cross-modality factorization. They compose — integrate within modality first, then MOFA+ across modalities.
- **WNN / MultiVI joint embeddings.** muon's Weighted Nearest Neighbors and scvi-tools' MultiVI produce a joint *embedding* for clustering paired single-cell modalities but do not give the interpretable per-factor per-view variance decomposition that makes MOFA+ useful for hypothesis generation. Reach for WNN/MultiVI when the deliverable is a joint UMAP; reach for MOFA+ when it is "which axis of variation is shared and what drives it."
- **Plain Claude Code + `mofapy2` (rung 1).** Viable for a throwaway one-off if the package is already installed; the skill earns its place by pinning the view-scaling and feature-selection conventions and keeping the run reproducible.
- **An autonomous system (Biomni).** Overkill for a single decomposition step; reach for it only when factor analysis is one node in a larger autonomous loop.

## See also

- [MOFA+ (Claude Skill)](../../catalog/tools/mofaplus-multi-omics.html)
- [muon (Claude Skill)](../../catalog/tools/muon-multiomics-singlecell.html) — builds the MuData views for single-cell multi-modal input.
- [AnnData (Claude Skill)](../../catalog/tools/anndata.html)
- [Integrate multiple single-cell RNA-seq datasets across batches](integrate-single-cell-datasets.html) — within-modality batch integration, upstream of cross-modality MOFA+.
- [Run functional enrichment on a gene list](run-functional-enrichment-on-a-gene-list.html) — annotate the biology of a factor's top-loading genes.
- [Infer transcription-factor and pathway activities from expression](infer-tf-and-pathway-activities-from-expression.html) — complementary regulator-level readout on the RNA layer.

## Sources

- [Argelaguet R. et al., "MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data," *Genome Biology* 21:111 (2020)](https://doi.org/10.1186/s13059-020-02015-1) — published 2020-05; verified 2026-07-18 (this run).
- [Argelaguet R. et al., "Multi-Omics Factor Analysis—a framework for unsupervised integration of multi-omics data sets," *Mol. Syst. Biol.* 14:e8124 (2018)](https://doi.org/10.15252/msb.20178124) — published 2018-06.
- [Saleh S.H. et al., "A Vascular-Extracellular Matrix Molecular Program Identifies High-Risk Diffuse Glioma Across Independent Multi-Omics," *Cancers* 18:1652 (2026)](https://doi.org/10.3390/cancers18101652) — published 2026; verified 2026-07-18 (this run).
- [MOFA+ skill (`SKILL.md`)](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/systems-biology-multiomics/mofaplus-multi-omics/SKILL.md) — verified 2026-07-18 (this run).
- [`jaechang-hits/SciAgent-Skills` repository](https://github.com/jaechang-hits/SciAgent-Skills) — verified 2026-07-18 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=integrate-multiomics-with-mofa&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fintegrate-multiomics-with-mofa.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
