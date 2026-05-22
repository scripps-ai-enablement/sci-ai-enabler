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

The server is published as the `biocontext_kb` package and is most easily run with `uv` (which handles its own Python). To verify it starts:

```
uvx biocontext_kb@latest
```

Then register it as an MCP server (Claude Code launches the process itself — don't keep the verification command running):

- **Claude Code (stdio, recommended)**:
  ```
  claude mcp add --transport stdio biocontext_kb -- uvx biocontext_kb@latest
  ```
- **Claude Desktop (stdio)** — add to `claude_desktop_config.json`:
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
- **Docker (HTTP)** — start the container, then register the HTTP endpoint:
  ```
  docker run -p 127.0.0.1:8000:8000 biocontext_kb:latest
  claude mcp add --transport http biocontext_kb http://127.0.0.1:8000/mcp
  ```
- **Remote test endpoint** (no install):
  ```
  claude mcp add --transport http biocontext_kb https://biocontext-kb.fastmcp.app/mcp
  ```

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

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=biocontextai&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbiocontextai.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
