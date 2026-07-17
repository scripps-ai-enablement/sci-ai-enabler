---
title: FinnGen (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-17
claude_science: true
summary: Finnish biobank GWAS summary statistics across thousands of endpoints from FinnGen; a source in the Human Genetics connector in Claude Science.
---

# FinnGen (Claude Science Connector)

Provides FinnGen's Finnish-biobank GWAS summary statistics across thousands of disease endpoints, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — public summary statistics (individual data controlled); access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *Human Genetics* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [finngen.fi (summary-stats downloads)](https://www.finngen.fi/en/access_results); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Retrieve FinnGen GWAS summary statistics and per-endpoint association results across thousands of curated disease endpoints in the Finnish population.

**Primary use cases**: Disease-association lookup, cross-population replication, target genetics support

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Human Genetics* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: FinnGen. Summary statistics are open; individual-level data are access-controlled. Bundled with GWAS Catalog, eQTL Catalogue, and BioBank Japan in Claude Science.

## Sources

- [FinnGen](https://www.finngen.fi/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=finngen&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ffinngen.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
