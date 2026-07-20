---
title: CELLxGENE CellGuide (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
summary: Cell-type reference cards (markers, ontology, descriptions) from CZ CELLxGENE CellGuide; the CellGuide connector in Claude Science.
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "Anthropic-hosted Claude Science featured connector (CellGuide) confirmed in Anthropic connectors-and-skills doc; read-only public CZ CELLxGENE CellGuide data, no credentials"
---

# CELLxGENE CellGuide (Claude Science Connector)

Provides cell-type reference information — canonical markers, ontology, and descriptions — from CZ CELLxGENE CellGuide, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — open; access via Claude Science |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — Anthropic-hosted Claude Science featured connector (CellGuide) confirmed in Anthropic doc; read-only public CZ CELLxGENE CellGuide data, no credentials |

## How to install

- **Claude Science** — enable the *CellGuide* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Related** — CELLxGENE *Census* expression data is in the catalog as [CELLxGENE Census](cellxgene-census.html); the `gget`/`gget-mcp` tools also wrap Census.
- **Public API** — the same data is reachable directly at [cellxgene.cziscience.com/cellguide](https://cellxgene.cziscience.com/cellguide); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Look up cell-type reference cards — canonical marker genes, Cell Ontology mapping, computed marker sets, and curated descriptions — from CZ CELLxGENE CellGuide.

**Primary use cases**: Cell-type annotation reference, marker-gene lookup, cell ontology mapping

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *CellGuide* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: Chan Zuckerberg Initiative (CELLxGENE). For single-cell expression matrices see [CELLxGENE Census](cellxgene-census.html).

## Sources

- [CZ CELLxGENE CellGuide](https://cellxgene.cziscience.com/cellguide)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cellguide&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcellguide.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
