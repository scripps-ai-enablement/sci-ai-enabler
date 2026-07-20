---
title: ClinGen (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-17
claude_science: true
summary: Expert-curated gene–disease validity and variant clinical significance from ClinGen; a source in the Clinical Genomics connector in Claude Science.
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "Anthropic-hosted Claude Science featured connector (Clinical Genomics) confirmed in Anthropic connectors-and-skills doc; read-only public ClinGen (NHGRI) CC0 data, no credentials"
---

# ClinGen (Claude Science Connector)

Provides ClinGen's expert-curated gene–disease validity and dosage/variant assertions, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — data CC0; access via Claude Science |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — Anthropic-hosted Claude Science featured connector (Clinical Genomics) confirmed in Anthropic doc; read-only public ClinGen CC0 data, no credentials |

## How to install

- **Claude Science** — enable the *Clinical Genomics* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [clinicalgenome.org](https://clinicalgenome.org/); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Look up ClinGen gene–disease validity classifications, dosage sensitivity, actionability, and variant/expert-panel curations for clinical interpretation.

**Primary use cases**: Gene–disease validity, variant interpretation support, clinical actionability

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Clinical Genomics* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: ClinGen (NHGRI). Bundled with CIViC and Open Targets in Claude Science.

## Sources

- [ClinGen](https://clinicalgenome.org/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=clingen&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fclingen.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
