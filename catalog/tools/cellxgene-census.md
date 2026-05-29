---
title: Cellxgene Census (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Molecular and Cellular Biology, Immunology and Microbiology, Translational Medicine]
last_verified: 2026-05-28
summary: Claude skill for querying the CZ CELLxGENE Discover census — 50M+ standardized single-cell observations across 1,000+ datasets via TileDB-SOMA, with AnnData / Scanpy integration.
---

# Cellxgene Census (Claude Skill)

Claude skill that drives the [CZ CELLxGENE Discover Census](https://chanzuckerberg.github.io/cellxgene-census/) — a TileDB-SOMA-backed atlas of standardized human and mouse single-cell RNA-seq data — for population-scale subsetting, metadata filtering, and AnnData export.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill (MIT collection); the CELLxGENE Census itself is free / CC-BY |
| **Capabilities** | Read-only — queries the public census; Claude executes Python locally |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install cellxgene-census@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/cellxgene-census ~/.claude/skills/
  pip install cellxgene-census
  ```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- Opening the public census via `cellxgene_census.open_soma()` with version pinning
- Metadata filtering (tissue, cell type, disease, assay, donor) before download to minimise transfer
- Pulling cell- or gene-axis subsets directly into AnnData / Scanpy
- Cross-dataset cell-type or disease comparisons across 1,000+ studies
- Local caching and batched reads for memory-constrained workflows
- Building reference atlases for downstream scVI / scANVI integration

**Primary use cases**: Reference-atlas construction for scVI / scANVI integration, cell-type-of-interest meta-analyses across public datasets, disease-vs-healthy expression comparisons, harmonised cohort assembly for downstream DE.

## Notes

Pairs naturally with the catalog's `scanpy`, `anndata`, `scvi-tools`, and `scvelo` entries for end-to-end single-cell workflows. Census versions are immutable snapshots; record the version you opened to keep analyses reproducible. Skill is documentation plus Python recipes — Claude calls `cellxgene-census` locally via Bash/Python, not as an MCP tool.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/cellxgene-census/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/cellxgene-census/SKILL.md)
- [CELLxGENE Census documentation](https://chanzuckerberg.github.io/cellxgene-census/)
- [`chanzuckerberg/cellxgene-census`](https://github.com/chanzuckerberg/cellxgene-census)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cellxgene-census&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcellxgene-census.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
