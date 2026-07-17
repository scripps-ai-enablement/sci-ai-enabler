---
title: Rhea (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Chemistry, Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
summary: Expert-curated biochemical reactions from Rhea (SIB); a source in the Chemistry connector in Claude Science.
---

# Rhea (Claude Science Connector)

Provides expert-curated biochemical reactions and their participants from Rhea, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — data CC BY 4.0; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *Chemistry* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Also** — Rhea offers a public SPARQL endpoint at `https://sparql.rhea-db.org`.
- **Public API** — the same data is reachable directly at [rhea-db.org/help/rest-api](https://www.rhea-db.org/); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Query balanced, expert-curated biochemical reactions (with ChEBI participants and enzyme/UniProt links) from Rhea, the reference reaction resource used by UniProt and others.

**Primary use cases**: Reaction lookup, enzyme–reaction mapping, metabolic annotation

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Chemistry* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: Rhea (SIB Swiss Institute of Bioinformatics). Bundled with PubChem, ChEBI, and BindingDB in Claude Science.

## Sources

- [Rhea](https://www.rhea-db.org/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=rhea&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Frhea.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
