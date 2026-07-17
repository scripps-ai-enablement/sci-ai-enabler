---
title: Rfam (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
summary: Non-coding RNA families, covariance models, and alignments from EMBL-EBI's Rfam; the RNA connector in Claude Science.
---

# Rfam (Claude Science Connector)

Provides non-coding RNA families and covariance models from EMBL-EBI's Rfam, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — data CC0; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *RNA* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [rfam.org (REST; docs.rfam.org)](https://rfam.org/); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Look up Rfam RNA families — consensus secondary structure, covariance models, seed alignments, and family/clan metadata — and their genome annotations.

**Primary use cases**: ncRNA family lookup, RNA structure/annotation, family classification

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *RNA* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: EMBL-EBI Rfam. Also queryable via EBI Search.

## Sources

- [EMBL-EBI Rfam](https://rfam.org/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=rfam&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Frfam.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
