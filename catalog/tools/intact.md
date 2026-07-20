---
title: IntAct (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Molecular and Cellular Biology, Integrative Structural and Computational Biology]
last_verified: 2026-07-17
claude_science: true
summary: Molecular-interaction evidence from EMBL-EBI's IntAct database; a source in the Structures & Interactions connector in Claude Science.
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "Anthropic-hosted Claude Science featured connector (Structures & Interactions) confirmed in Anthropic connectors-and-skills doc; read-only public EMBL-EBI IntAct CC BY 4.0 data, no credentials"
---

# IntAct (Claude Science Connector)

Provides curated molecular-interaction data from EMBL-EBI's IntAct database, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — data CC BY 4.0; access via Claude Science |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — Anthropic-hosted Claude Science featured connector (Structures & Interactions) confirmed in Anthropic doc; read-only public EMBL-EBI CC BY 4.0 data, no credentials |

## How to install

- **Claude Science** — enable the *Structures & Interactions* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [ebi.ac.uk/intact/ws](https://www.ebi.ac.uk/intact/ws); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Query curated protein–protein and molecular interaction records with experimental evidence and confidence scores from IntAct (EMBL-EBI).

**Primary use cases**: Interaction evidence lookup, interactome construction, complex context

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Structures & Interactions* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: EMBL-EBI IntAct. Bundled with PDB, AlphaFold DB, EMDB, and Complex Portal in Claude Science.

## Sources

- [EMBL-EBI IntAct](https://www.ebi.ac.uk/intact/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=intact&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fintact.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
