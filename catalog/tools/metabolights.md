---
title: MetaboLights (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Chemistry, Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
summary: Metabolomics studies, metadata, and metabolite data from EMBL-EBI's MetaboLights; a source in the Omics Archives connector in Claude Science.
---

# MetaboLights (Claude Science Connector)

Provides metabolomics studies and metabolite annotations from EMBL-EBI's MetaboLights, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — open; access via Claude Science |
| **Capabilities** | Read-only |

## How to install

- **Claude Science** — enable the *Omics Archives* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [ebi.ac.uk/metabolights/ws](https://www.ebi.ac.uk/metabolights/ws); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Query MetaboLights studies — study/assay metadata, protocols, and metabolite identifications across MS and NMR metabolomics experiments — via the MetaboLights web service.

**Primary use cases**: Metabolomics study discovery, metabolite annotation, experiment metadata

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Omics Archives* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: EMBL-EBI MetaboLights. Bundled with GEO, ArrayExpress, PRIDE, and MGnify in Claude Science.

## Sources

- [EMBL-EBI MetaboLights](https://www.ebi.ac.uk/metabolights/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=metabolights&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmetabolights.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
