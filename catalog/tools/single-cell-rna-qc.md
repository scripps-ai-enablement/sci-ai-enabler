---
title: single-cell-rna-qc
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Anthropic
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine]
last_verified: 2026-05-19
summary: scverse MAD-based QC for .h5ad and 10x .h5 single-cell RNA-seq inputs.
---

# single-cell-rna-qc

Runs QC on `.h5ad` and 10x `.h5` single-cell files using scverse best practices, writing filtered matrices and QC plots.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Anthropic](https://github.com/anthropics/life-sciences) |
| **Availability** | GA — first Anthropic-published scientific skill, released with Claude for Life Sciences (Oct 2025) |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install single-cell-rna-qc@life-sciences
  ```
- **Claude.ai** — **Settings → Capabilities → Skills → Upload skill**, using the skill ZIP from the `anthropics/life-sciences` repo.

## What it does

Skill instructions plus bundled scripts that perform MAD-based filtering on gene counts, total counts, and mitochondrial percentage, and emit standard QC visualizations.

**Primary use cases**: First-pass single-cell RNA-seq quality control, doublet / empty-droplet filtering, generating QC figures for downstream Scanpy / scvi-tools workflows.

## Notes

Reads AnnData `.h5ad` or 10x Cell Ranger `.h5`. Uses median-absolute-deviation thresholds in line with scverse guidance. Auto-detects format.

## Sources

- [Skill source (SKILL.md)](https://github.com/anthropics/life-sciences/blob/main/single-cell-rna-qc/SKILL.md)
- [Anthropic tutorial](https://claude.com/resources/tutorials/how-to-use-the-single-cell-rna-qc-skill-with-claude)
- [Claude for Life Sciences announcement](https://www.anthropic.com/news/claude-for-life-sciences)
