---
title: BioBank Japan (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-17
claude_science: true
summary: East Asian biobank GWAS summary statistics from BioBank Japan (PheWeb); a source in the Human Genetics connector in Claude Science.
---

# BioBank Japan (Claude Science Connector)

Provides BioBank Japan's East-Asian GWAS summary statistics (via PheWeb), offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — public summary statistics; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *Human Genetics* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [pheweb.jp / biobankjp.org](https://pheweb.jp/); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Browse and retrieve BioBank Japan GWAS summary statistics across many traits in an East-Asian cohort, served through PheWeb.

**Primary use cases**: Cross-ancestry replication, East-Asian trait genetics, association lookup

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Human Genetics* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: BioBank Japan. Bundled with GWAS Catalog, eQTL Catalogue, and FinnGen in Claude Science.

## Sources

- [BioBank Japan](https://biobankjp.org/)
- [BBJ PheWeb](https://pheweb.jp/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=biobank-japan&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbiobank-japan.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
