---
title: ChEBI (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Chemistry]
last_verified: 2026-07-17
claude_science: true
summary: Chemical Entities of Biological Interest — curated small-molecule ontology and annotations; a source in the Chemistry connector in Claude Science.
---

# ChEBI (Claude Science Connector)

Provides curated small-molecule structures, names, and ontology from EMBL-EBI's ChEBI, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — data CC BY 4.0; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *Chemistry* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Also queryable** via the [OLS MCP server](ontology-lookup-service.html) (ChEBI is an OLS ontology).
- **Public API** — the same data is reachable directly at [ebi.ac.uk/chebi/webServices](https://www.ebi.ac.uk/chebi/); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Look up biologically interesting chemical entities — structures, synonyms, roles, and the ChEBI ontology relationships — from EMBL-EBI.

**Primary use cases**: Small-molecule identification, chemical ontology mapping, metabolite annotation

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Chemistry* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: EMBL-EBI ChEBI. Bundled with PubChem, Rhea, and BindingDB in Claude Science.

## Sources

- [EMBL-EBI ChEBI](https://www.ebi.ac.uk/chebi/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=chebi&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fchebi.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
