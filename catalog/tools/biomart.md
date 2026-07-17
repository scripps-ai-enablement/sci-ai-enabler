---
title: BioMart (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
summary: Bulk biological data-mining and ID mapping via Ensembl BioMart; the BioMart connector in Claude Science.
---

# BioMart (Claude Science Connector)

Provides bulk data-mining and cross-reference retrieval through Ensembl BioMart, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — open; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *BioMart* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Related MCP** — the [Ensembl MCP server](https://github.com/Augmented-Nature/Ensembl-MCP-Server) covers Ensembl gene/annotation queries; see also [Ensembl](ensembl.html).
- **Public API** — the same data is reachable directly at [ensembl.org/biomart/martservice](https://www.ensembl.org/biomart/martservice); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Run BioMart queries against Ensembl for bulk attribute retrieval and identifier mapping across genes, transcripts, proteins, and cross-references (e.g., Ensembl↔Entrez↔UniProt↔HGNC).

**Primary use cases**: Bulk ID mapping, attribute export, cross-reference retrieval

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *BioMart* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: Ensembl / EMBL-EBI BioMart. For interactive Ensembl gene queries see [Ensembl](ensembl.html).

## Sources

- [Ensembl BioMart](https://www.ensembl.org/biomart/martview)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=biomart&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbiomart.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
