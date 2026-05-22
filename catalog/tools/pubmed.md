---
title: Anthropic PubMed Connector
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Anthropic
availability: GA
tool_categories: [All]
last_verified: 2026-05-19
summary: Anthropic-managed NCBI literature search via PubMed and PubMed Central.
---

# Anthropic PubMed Connector

Anthropic-managed search across PubMed and PubMed Central via NCBI E-utilities, with related NCBI databases (Gene, Protein, Nucleotide) discoverable through Claude.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Anthropic](https://claude.com/) |
| **Availability** | GA (Claude.ai / Claude Code); Beta MCP HTTP endpoint |
| **Pricing** | Free / OSS — included with Claude plans; no extra cost beyond model usage |
| **Capabilities** | Read-only — PubMed and PubMed Central search via NCBI E-utilities |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install pubmed@life-sciences
  ```
- **Claude Code** — direct MCP add:
  ```
  claude mcp add --transport http pubmed https://pubmed.mcp.claude.com/mcp
  ```
  with beta header `mcp-client-2025-11-20`.
- **Claude.ai** — Healthcare connector; toggle in **Settings → Connectors**.

## What it does

PubMed/PMC search and article metadata retrieval. Related NCBI E-utilities databases (Gene, Protein, Nucleotide) are discoverable through Claude.

**Primary use cases**: Literature search, systematic review scaffolding, MeSH-aware Boolean query refinement.

## Notes

Anthropic-managed hosted HTTP transport. NCBI rate limits apply server-side. Index is updated daily from PubMed. Released as part of the Claude for Life Sciences launch (Oct 2025).

## Sources

- [Anthropic tutorial](https://claude.com/resources/tutorials/using-the-pubmed-connector-in-claude)
- [Claude for Life Sciences coverage](https://www.cnbc.com/2025/10/20/anthropic-claude-life-sciences-research-ai.html)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pubmed&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpubmed.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
