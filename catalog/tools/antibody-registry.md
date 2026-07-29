---
title: Antibody Registry (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Anthropic
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-17
claude_science: true
summary: Persistent antibody identifiers (RRIDs) and vendor/catalog metadata from the Antibody Registry; a source in the Research Resources connector in Claude Science.
verification: works
verified_on: 2026-07-29
security: cleared
security_on: 2026-07-29
security_note: "Anthropic-hosted Claude Science featured connector (Research Resources) confirmed in Anthropic connectors-and-skills doc; read-only public Antibody Registry (RRID/SciCrunch) data, no credentials"
---

# Antibody Registry (Claude Science Connector)

Provides persistent antibody identifiers (RRIDs) and catalog metadata from the Antibody Registry, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic-hosted connector |
| **Pricing** | Free — open; access via Claude Science |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-29 |
| **Security** | cleared · 2026-07-29 — Anthropic-hosted Claude Science featured connector (Research Resources) confirmed in Anthropic doc; read-only public Antibody Registry data, no credentials |

## How to install

- **Claude Science** — enable the *Research Resources* featured connector. These featured connectors are Anthropic-hosted and have no separately addressable per-connector MCP URL.
- **Public API** — the same data is reachable directly at [antibodyregistry.org](https://www.antibodyregistry.org/); wrap it as a custom MCP server if you need programmatic access outside Claude Science.

## What it does

Resolve and look up antibody RRIDs, vendor/catalog numbers, clones, and target metadata for reagent identification and reproducibility reporting.

**Primary use cases**: Antibody RRID resolution, reagent identification, methods reproducibility

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Research Resources* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Data provider: The Antibody Registry (RRID / SciCrunch). Bundled with Grants.gov in the Research Resources connector; see [Grants.gov](research-grants.html).

## Sources

- [The Antibody Registry](https://www.antibodyregistry.org/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=antibody-registry&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fantibody-registry.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
