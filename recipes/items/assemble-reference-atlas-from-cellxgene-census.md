---
title: Assemble a tissue reference atlas from the CELLxGENE Census
parent: All recipes
grand_parent: Recipes
nav_order: 1
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology, Translational Medicine]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-05-28
summary: Use the cellxgene-census Claude skill to slice a tissue- or disease-specific AnnData from the CZ CELLxGENE Census, optionally fetching the precomputed scVI embedding for reference mapping or downstream integration.
---

# Assemble a tissue reference atlas from the CELLxGENE Census

Hand Claude Code a tissue, cell-type, or disease query and a Census version; get back a harmonised AnnData of every public single-cell observation that matches, with the CZ-trained scVI embedding attached for immediate reference mapping or as the substrate for a custom integration.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology, Translational Medicine |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

Before you can interpret a new single-cell experiment, you need context: which cell types appear in this tissue across published studies, what their canonical expression looks like, and which donor or disease variability is already documented. Assembling that reference by hand means scraping a dozen Studies on CELLxGENE Discover, resolving incompatible obs schemas, harmonising gene symbols, and re-running integration. The CZ CELLxGENE Discover Census collapses that work into a single TileDB-SOMA-backed snapshot — 50M+ standardized human and mouse cells across 1,000+ datasets, versioned, with a community-maintained scVI model fit across the whole thing. Solved looks like: a single AnnData with the cells you asked for, a `scvi` embedding in `obsm`, and a UMAP coloured by cell type and dataset that you can compare your query against.

The non-obvious failure mode is forgetting that the Census is versioned. Different LTS snapshots have different schemas; the precomputed scVI model is tied to one snapshot. A reference atlas pulled from `2025-11-08` is not interchangeable with one pulled from a later release.

## Recommended approach

1. **Install the [cellxgene-census skill](../../catalog/tools/cellxgene-census.html)** in Claude Code:

   ```
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install cellxgene-census@claude-scientific-skills
   ```

   Confirm with `/plugin list`. If you intend to integrate the query atlas with your own data, install the [scvi-tools skill](../../catalog/tools/scvi-tools.html) too; if you want to do downstream clustering, also install the [Scanpy-MCP](../../catalog/tools/scanpy.html).

2. **Pin a Census version up front.** Pinning is the single most important reproducibility decision. A minimal prompt:

   ```
   Use the cellxgene-census skill to open the public census at
   version "2025-11-08" (LTS) with cellxgene_census.open_soma().
   Print the schema version and the total cell count.
   ```

3. **Filter on obs metadata before downloading.** Pull only the cells you need — the Census is hundreds of millions of rows and a naive `get_anndata()` will OOM a workstation. Example for a lung disease cohort:

   ```
   From the open Census handle, build an AnnData of human lung cells
   from healthy and IPF donors:
     - organism="Homo sapiens"
     - obs_value_filter: tissue_general == "lung" AND
       (disease == "normal" OR disease == "idiopathic pulmonary fibrosis") AND
       is_primary_data == True
     - obs_embeddings=["scvi"]
   Save to data/lung_ipf_census.h5ad and print obs.value_counts()
   for dataset_id, donor_id, and cell_type.
   ```

   The `is_primary_data == True` filter is mandatory unless you want duplicates — the Census ships overlapping cells across datasets.

4. **Sanity-check the precomputed embedding.** Census ships a CZ-trained scVI embedding in `obsm["scvi"]`. Have Claude compute neighbours from that, run UMAP, and colour by `dataset_id`, `cell_type`, and `disease`. If `dataset_id` mixes well and `cell_type` clusters, the precomputed embedding is usable as-is.

5. **(Optional) Project a new query onto the reference.** If you have your own AnnData of unlabeled cells from the same tissue, use the scvi-tools skill to load the [Census-wide scVI model from scvi-hub](https://docs.scvi-tools.org/en/latest/tutorials/notebooks/hub/cellxgene_census_model.html) and call `load_query_data` on your AnnData. Concatenate with the reference, run UMAP, and inspect whether your query overlays existing cell-type clusters.

6. **(Optional) Re-fit scVI if you need finer-grained batch correction.** If your application needs `dataset_id + donor_id + assay` as the batch key rather than the Census default, follow the [integrate-single-cell-datasets recipe](integrate-single-cell-datasets.html) with the concatenated reference + query AnnData as input.

7. **Record the Census version in the AnnData uns.** Have Claude write `adata.uns["census_version"] = "2025-11-08"` before saving. Without this, the analysis is not reproducible across releases.

## Why this assembly

Rung 2 of the simplicity ladder. The Census is a Python-only API over a TileDB-SOMA store; plain Claude Code can drive it, but the skill encapsulates the parameter footguns that matter — `obs_value_filter` syntax, version pinning, `is_primary_data` deduplication, the right `obs_embeddings` arguments — and the [skill page](../../catalog/tools/cellxgene-census.html) cites the Census docs as the SKILL.md source. There is no need for an autonomous system because the task is bounded: filter, fetch, embed, save.

## Availability

Fully open. The cellxgene-census skill is MIT-licensed (K-Dense Inc.) and the Census itself is CC-BY. Pretrained scVI models from scvi-hub are Apache-2.0. No account or institutional access required; the data are public.

## Compute requirements

Workstation with GPU recommended for the optional reference-mapping step (step 5). The Census query (steps 1–4) is CPU-bound and runs on a laptop: a 100k-cell slice typically downloads in 1–5 minutes over a fast connection and uses ~3–6 GB RAM. The precomputed scVI embedding is included in the fetched AnnData, so no GPU is needed just to inspect the reference. If you re-fit scVI (step 6) on a 200k-500k-cell concatenation, budget an A100 / H100 (8–24 GB VRAM) and 30–90 minutes. Storage: a tissue slice is typically 1–10 GB on disk; full-tissue atlases (e.g. all lung) can exceed 30 GB.

## Evidence

Reported. The Census team publishes the [`comp_bio_data_integration_scvi`](https://chanzuckerberg.github.io/cellxgene-census/notebooks/analysis_demo/comp_bio_data_integration_scvi.html) notebook documenting the exact filter → fetch → scVI pipeline this recipe wraps, and the [scvi-hub paper](https://www.nature.com/articles/s41592-025-02799-9) (Ergen et al., *Nature Methods* 2025) reports the Census-wide scVI model as the showcase application. The Sikkema et al. integrated lung atlas ([*Nature Medicine* 2023, doi:10.1038/s41591-023-02327-2](https://doi.org/10.1038/s41591-023-02327-2)) is the canonical demonstration that the Census + scVI workflow recovers biologically meaningful cell states across 43 lung datasets — the same workflow this recipe wraps under a Claude skill.

No peer-reviewed benchmark of "Claude + cellxgene-census skill" against the hand-written Census notebooks is known. The skill adds reproducibility and prompt-level convenience, not new analytical capability.

## Alternatives considered

- **Plain Claude Code with `pip install cellxgene-census`.** Works for one-off queries but reproduces the most common Census footguns (forgotten `is_primary_data` filter, missing version pin, unknown schema-2.4.0 multi-value disease strings). The skill exists to prevent these.
- **Downloading studies one at a time from cellxgene.cziscience.com.** Viable for one or two studies; combinatorially expensive past that. The Census exists because that pattern doesn't scale.
- **Biomni or another autonomous-science system.** Overkill for a query-and-fetch task. Biomni can incorporate Census as a step but the assembly here is bounded enough that an autonomous loop is dead weight.
- **Pre-built tissue atlases (HLCA, Tabula Sapiens) downloaded directly.** Often easier when one exists; the Census wins when you want a cohort the published atlas does not cover (e.g. a specific disease arm) or when you want to update against the latest LTS without waiting for a new atlas release.

## See also

- [Cellxgene Census (Claude Skill)](../../catalog/tools/cellxgene-census.html)
- [scvi-tools (Claude Skill)](../../catalog/tools/scvi-tools.html)
- [Integrate multiple single-cell RNA-seq datasets across batches](integrate-single-cell-datasets.html) — the downstream integration recipe.
- [Run first-pass QC on a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — for the query side of a reference-mapping workflow.
- [AnnData (Claude Skill)](../../catalog/tools/anndata.html)

## Sources

- [CELLxGENE Census documentation](https://chanzuckerberg.github.io/cellxgene-census/) — verified 2026-05-28 (this run).
- [`comp_bio_data_integration_scvi` notebook](https://chanzuckerberg.github.io/cellxgene-census/notebooks/analysis_demo/comp_bio_data_integration_scvi.html) — Census team, verified 2026-05-28.
- [Ergen C. et al., "Scvi-hub: an actionable repository for model-driven single-cell analysis", *Nature Methods* 2025, doi:10.1038/s41592-025-02799-9](https://www.nature.com/articles/s41592-025-02799-9) — published 2025.
- [Sikkema L. et al., "An integrated cell atlas of the human lung in health and disease", *Nature Medicine* 2023, doi:10.1038/s41591-023-02327-2](https://doi.org/10.1038/s41591-023-02327-2) — published 2023.
- [`scientific-skills/cellxgene-census/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/cellxgene-census/SKILL.md) — K-Dense-AI, verified 2026-05-28.

---

## Tried this recipe?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=assemble-reference-atlas-from-cellxgene-census&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fassemble-reference-atlas-from-cellxgene-census.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
