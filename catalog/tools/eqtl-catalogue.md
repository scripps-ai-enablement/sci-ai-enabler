---
title: eQTL Catalogue (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-17
claude_science: true
summary: Uniformly processed cis-QTL (eQTL/sQTL) summary statistics from EMBL-EBI's eQTL Catalogue; a source in the Human Genetics connector in Claude Science.
---

# eQTL Catalogue (Claude Science Connector)

Provides uniformly processed cis-QTL summary statistics from the EMBL-EBI eQTL Catalogue, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — open summary statistics; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *Human Genetics* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [ebi.ac.uk/eqtl/api](https://www.ebi.ac.uk/eqtl/api/); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Query harmonized eQTL/sQTL associations across many tissues and cell types — effect sizes and p-values by gene/variant — from the eQTL Catalogue.

**Primary use cases**: Colocalization inputs, variant-to-gene mapping, regulatory-effect lookup

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Human Genetics* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: EMBL-EBI eQTL Catalogue. Bundled with GWAS Catalog, FinnGen, and BioBank Japan in Claude Science.

## Sources

- [EMBL-EBI eQTL Catalogue](https://www.ebi.ac.uk/eqtl/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=eqtl-catalogue&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Feqtl-catalogue.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
