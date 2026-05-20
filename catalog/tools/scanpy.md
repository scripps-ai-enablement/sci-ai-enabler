---
title: Scanpy-MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: scmcphub
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine]
last_verified: 2026-05-20
summary: MCP server wrapping Scanpy so Claude can run end-to-end single-cell RNA-seq analyses (QC, clustering, DE, plotting) from natural language.
---

# Scanpy-MCP

MCP server that exposes the full Scanpy / AnnData workflow as natural-language tools — IO, QC, normalization, PCA, clustering, differential expression, and plotting.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [scmcphub (huang-sh)](https://github.com/scmcphub/scanpy-mcp) |
| **Availability** | GA — v0.5.0 (10 releases) |
| **Pricing** | Free / OSS (BSD-3-Clause) |
| **Capabilities** | Read/Write |

## How to install

```
pip install scanpy-mcp
scanpy-mcp run                                  # stdio
scanpy-mcp run --transport shttp --port 8000    # streamable HTTP
```

Compatible with Claude Desktop, Claude Code, Cherry Studio, Cline, and Agno.

## What it does

- `io.read` / `io.write` — AnnData / 10x file I/O
- `pp.*` — QC filter, normalize, find HVGs, scale, PCA, neighbors
- `tl.*` — UMAP, Leiden clustering, `rank_genes_groups`
- `pl.*` — violin, heatmap, dotplot

**Primary use cases**: Natural-language single-cell RNA-seq QC and clustering, reproducible Scanpy pipelines driven from chat, onboarding for users new to Scanpy.

## Notes

stdio and streamable-HTTP transports. Complements the `single-cell-rna-qc` skill: that skill is a workflow checklist that Claude follows; this server lets Claude call Scanpy functions as discrete tools mid-conversation.

## Sources

- [`scmcphub/scanpy-mcp`](https://github.com/scmcphub/scanpy-mcp)
- [scmcphub documentation](https://docs.scmcphub.org/servers/scanpy-mcp)
