---
title: Complex Portal (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Molecular and Cellular Biology, Integrative Structural and Computational Biology]
last_verified: 2026-07-17
claude_science: true
summary: Curated macromolecular complexes from EMBL-EBI's Complex Portal; a source in the Structures & Interactions connector in Claude Science.
---

# Complex Portal (Claude Science Connector)

Provides curated macromolecular complex compositions from EMBL-EBI's Complex Portal, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — data CC0; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *Structures & Interactions* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [ebi.ac.uk/complexportal/ws](https://www.ebi.ac.uk/complexportal/ws); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Look up manually curated stable macromolecular complexes — subunit composition, stoichiometry, and function — from the Complex Portal (EMBL-EBI).

**Primary use cases**: Complex composition lookup, subunit/stoichiometry queries, interaction context

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Structures & Interactions* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: EMBL-EBI Complex Portal (curated by the IntAct team). Bundled with PDB, AlphaFold DB, EMDB, and IntAct in Claude Science.

## Sources

- [EMBL-EBI Complex Portal](https://www.ebi.ac.uk/complexportal/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=complex-portal&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcomplex-portal.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
