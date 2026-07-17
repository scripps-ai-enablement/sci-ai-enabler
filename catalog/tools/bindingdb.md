---
title: BindingDB (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-07-17
claude_science: true
summary: Measured protein–small-molecule binding affinities from BindingDB; a source in the Chemistry connector in Claude Science.
---

# BindingDB (Claude Science Connector)

Provides measured protein–ligand binding affinities from BindingDB, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — data CC BY-SA; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *Chemistry* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [bindingdb.org REST API](https://www.bindingdb.org/); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Retrieve experimentally measured binding affinities (Ki, IC50, Kd, EC50) for protein–small-molecule pairs, with links to targets and compounds, from BindingDB.

**Primary use cases**: Affinity data retrieval, SAR exploration, target–compound evidence

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Chemistry* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: BindingDB (CC BY-SA — share-alike). Bundled with PubChem, ChEBI, and Rhea in Claude Science.

## Sources

- [BindingDB](https://www.bindingdb.org/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=bindingdb&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbindingdb.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
