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

Install the server:

```
pip install scanpy-mcp
```

The `scanpy-mcp` package exposes two transports:

- `scanpy-mcp run` — stdio
- `scanpy-mcp run --transport shttp --port 8000` — streamable HTTP

Register with Claude Code (stdio — recommended; Claude Code launches the process itself, so don't run `scanpy-mcp run` separately):

```
claude mcp add --transport stdio scanpy -- scanpy-mcp run
```

Or with Claude Desktop, add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "scanpy": { "command": "scanpy-mcp", "args": ["run"] }
  }
}
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

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=scanpy&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fscanpy.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
