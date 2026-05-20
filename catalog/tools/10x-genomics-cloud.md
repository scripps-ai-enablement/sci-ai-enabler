---
title: 10x Genomics Cloud MCP
parent: All tools
grand_parent: Catalog
nav_order: 1
tool_type: MCP server
supplier: 10x Genomics
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine]
last_verified: 2026-05-19
summary: Conversational orchestration of 10x Cloud single-cell, immune-profiling, and spatial-transcriptomics analyses.
---

# 10x Genomics Cloud MCP

Conversational orchestration of single-cell, immune-profiling, and spatial-transcriptomics analyses stored in 10x Genomics Cloud.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [10x Genomics](https://www.10xgenomics.com/) |
| **Availability** | GA — available from Oct 20, 2025 |
| **Pricing** | Free plugin; requires a paid 10x Genomics Cloud account with active analysis data |
| **Capabilities** | Read/Write — query and trigger single-cell, immune-profiling, and spatial-transcriptomics analyses stored in 10x Genomics Cloud |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install 10x-genomics@life-sciences
  ```
  Then run `/plugin` → **Configure** with a 10x Cloud access token.
- **Claude Desktop** — MCPB extension distributed by 10x Genomics; configure with the same 10x Cloud access token.

## What it does

Project and analysis listing, reference and annotation-model lookup, analysis-output retrieval, project-file inspection for 10x Cloud Analysis runs.

**Primary use cases**: Conversational orchestration of 10x Cloud single-cell / Visium / Xenium analyses, retrieval of analysis outputs, prompt-based pipeline configuration.

## Notes

Local MCPB binary hosted by 10x Genomics, not bundled in `anthropics/life-sciences`. Auth via 10x Cloud access token from Security settings. Requires existing cloud projects to be useful.

## Sources

- [10x Genomics Cloud MCP docs](https://www.10xgenomics.com/support/software/cloud-analysis/latest/tutorials/cloud-mcp-server-code)
- [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences)
- [DeepWiki: 10x Genomics Cloud](https://deepwiki.com/anthropics/life-sciences/3.7-10x-genomics-cloud)
