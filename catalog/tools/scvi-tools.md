---
title: scvi-tools
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Anthropic
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine]
last_verified: 2026-05-19
summary: Deep-learning workflows for scVI, scANVI, totalVI, MultiVI, PeakVI, DestVI, and related scvi-tools models for single-cell omics.
---

# scvi-tools

Guides Claude through scvi-tools deep-learning workflows on AnnData single-cell inputs, writing trained model artifacts, latent representations, and normalized expression matrices.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Anthropic](https://github.com/anthropics/life-sciences) |
| **Availability** | GA — distributed via `anthropics/life-sciences` (Oct 2025) |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install scvi-tools@life-sciences
  ```
- **Claude.ai** — **Settings → Capabilities → Skills → Upload skill**, using the skill bundle from the `anthropics/life-sciences` repo.

## What it does

Workflows for scVI / scANVI (batch correction, semi-supervised cell-type annotation), totalVI and MultiVI (CITE-seq, RNA+ATAC multi-modal integration), PeakVI and scBasset (chromatin accessibility), DestVI / Tangram / cell2location / Stereoscope (spatial deconvolution), contrastiveVI (perturbation), sysVI (cross-cohort batch correction), and veloVI (RNA velocity). Covers model setup, training, and latent-extraction code patterns.

**Primary use cases**: Deep-learning-based batch integration, reference-mapped cell-type annotation, multi-modal CITE-seq / multiome analysis, spatial transcriptomics deconvolution.

## Notes

Requires Python with `scvi-tools` (PyTorch + AnnData stack) installed locally. GPU recommended for larger datasets. Expects a raw-count layer (not log-normalized) when registering AnnData via `setup_anndata`.

## Sources

- [Anthropic tutorial](https://claude.com/resources/tutorials/how-to-use-the-scvi-tools-bioinformatics-skill-bundle-with-claude)
- [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences)
- [scvi-tools documentation](https://docs.scvi-tools.org/)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=scvi-tools&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fscvi-tools.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
