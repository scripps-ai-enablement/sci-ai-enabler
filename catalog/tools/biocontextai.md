---
title: BioContextAI Knowledgebase MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: BioContextAI
availability: GA
tool_categories: [All]
last_verified: 2026-05-20
summary: Read-only MCP that unifies 14+ biomedical databases (Antibody Registry, UniProt, STRING, AlphaFold, KEGG, Open Targets) for immune and protein-context queries.
---

# BioContextAI Knowledgebase MCP

A single MCP server that fronts 14+ biomedical APIs as a unified retrieval layer — antibody and protein identifier resolution, pathway and interaction lookups, predicted structures, drug and clinical trial cross-references.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [BioContextAI](https://biocontext.ai/) (Heidelberg-led OSS initiative) |
| **Availability** | GA — v0.2.1 (May 2026) |
| **Pricing** | Free / OSS (Apache-2.0). Underlying data sources keep their own licenses; KEGG restricts commercial remote hosting. |
| **Capabilities** | Read-only |

## How to install

- **stdio (recommended for Claude Desktop / Code)**:
  ```
  uvx biocontext_kb@latest
  ```
- **Claude Desktop config** (HTTP):
  ```json
  {
    "mcpServers": {
      "biocontext_kb": {
        "command": "uvx",
        "args": ["biocontext_kb@latest"],
        "env": { "UV_PYTHON": "3.12" }
      }
    }
  }
  ```
- **Docker**: `docker run -p 127.0.0.1:8000:8000 biocontext_kb:latest`
- **Remote test endpoint**: `https://biocontext-kb.fastmcp.app/mcp`

## What it does

Unified access to:

- **Antibody / immunology**: Antibody Registry, PRIDE
- **Protein / structure**: UniProt, InterPro, AlphaFold DB, Human Protein Atlas
- **Interactions / pathways**: STRING, Reactome, KEGG
- **Targets / drugs**: Open Targets, Drugs@openFDA
- **Single-cell context**: PanglaoDB
- **Genomes / literature**: Ensembl, EuropePMC, bioRxiv
- **Ontologies**: OLS
- **Trials**: ClinicalTrials.gov

**Primary use cases**: Antibody and reagent identifier resolution; immune protein and pathway context; pulling AlphaFold structures for antigen-binding analysis; building integrated knowledge graphs for a target list.

## Notes

stdio (dev) and HTTP/uvicorn (prod) transports. No auth for the server itself, but it respects upstream rate limits. IEDB is not yet integrated.

## Sources

- [`biocontext-ai/knowledgebase-mcp`](https://github.com/biocontext-ai/knowledgebase-mcp)
- [BioContextAI Registry](https://biocontext.ai/registry)
