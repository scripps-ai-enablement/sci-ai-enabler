---
title: CIViC (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-17
claude_science: true
summary: Crowd-curated clinical interpretations of cancer variants from CIViC (WashU); a source in the Clinical Genomics connector in Claude Science.
---

# CIViC (Claude Science Connector)

Provides expert/crowd-curated clinical interpretations of cancer variants from CIViC, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — data CC0; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *Clinical Genomics* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [civicdb.org/api/graphql](https://civicdb.org/api/graphql); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Query clinical evidence for cancer variants — predictive, prognostic, diagnostic, and predisposing interpretations with sources — via the CIViC GraphQL API.

**Primary use cases**: Cancer variant interpretation, therapy-association evidence, biomarker curation

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Clinical Genomics* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: CIViC (Washington University). Bundled with ClinGen and Open Targets in Claude Science.

## Sources

- [CIViC](https://civicdb.org/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=civic&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcivic.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
