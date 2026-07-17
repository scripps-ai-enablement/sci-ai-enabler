---
title: Ontology Lookup Service (OLS) MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: seandavi
availability: Beta
tool_categories: [All]
last_verified: 2026-07-17
claude_science: true
summary: Search and resolve terms across hundreds of biomedical ontologies via EMBL-EBI's OLS; part of the Genes & Ontologies connector in Claude Science.
---

# Ontology Lookup Service (OLS) MCP Server

Searches and resolves terms across biomedical ontologies through EMBL-EBI's Ontology Lookup Service via a community MCP server.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [seandavi](https://github.com/seandavi/ols-mcp-server) |
| **Availability** | Beta — community OSS |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only |

## How to install

- **Claude Code / Desktop** — MCP server ([seandavi/ols-mcp-server](https://github.com/seandavi/ols-mcp-server), OSS):
  ```
  git clone https://github.com/seandavi/ols-mcp-server
  cd ols-mcp-server
  uv run ols-mcp-server
  ```
- **Claude Science** — also available as the *Genes & Ontologies* featured connector (Anthropic-hosted).
- **Public API** — [ebi.ac.uk/ols4/api](https://www.ebi.ac.uk/ols4/api).

## What it does

Search across hundreds of ontologies (e.g., GO, EFO, MONDO, HP, ChEBI, Uberon), resolve terms and CURIEs, and traverse term hierarchies via the OLS4 API.

**Primary use cases**: Ontology term search, CURIE resolution, disease/phenotype ontology mapping

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Genes & Ontologies* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Wraps the EMBL-EBI OLS4 API. Confirm the exact entry point in the repo README.

## Sources

- [seandavi/ols-mcp-server](https://github.com/seandavi/ols-mcp-server)
- [EMBL-EBI OLS](https://www.ebi.ac.uk/ols4/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=ontology-lookup-service&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fontology-lookup-service.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
