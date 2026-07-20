---
title: BioRender Connector
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: BioRender
availability: GA
tool_categories: [All]
last_verified: 2026-06-20
summary: Scientific-figure assembly from the 50,000+ BioRender icon and template library.
verification: degraded
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "official biorender plugin confirmed in anthropics/life-sciences marketplace; vendor-hosted remote MCP by BioRender, OAuth login required, no known advisories"
verification_note: "biorender plugin resolves in the anthropics/life-sciences marketplace but the remote MCP requires BioRender OAuth login so boot is unverifiable without an account"
---

# BioRender Connector

Search BioRender's icon and template library and request scientific-figure suggestions for slides, papers, posters, and grants.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [BioRender](https://www.biorender.com/) |
| **Availability** | GA — launched Oct 23, 2025 alongside the Claude for Life Sciences partnership |
| **Pricing** | Freemium — Free and Individual plans access a limited icon/template set; Premium / Team plans access the full library |
| **Capabilities** | Read/Write |
| **Verified** | degraded · 2026-07-20 — plugin resolves in life-sciences marketplace but OAuth-gated, boot unverifiable without an account |
| **Security** | cleared · 2026-07-20 — official biorender plugin in anthropics/life-sciences, vendor-hosted by BioRender, no advisories |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install biorender@life-sciences
  ```
- **Claude.ai** — BioRender connector; toggle in **Settings → Connectors**, then sign in with BioRender credentials.

## What it does

Scientific-icon search, template search, and figure recommendations across the 50,000+ vetted BioRender icon library.

**Primary use cases**: Building scientific figures, generating slide-deck illustrations, sourcing curated templates for grants and publications.

## Notes

Remote MCP server hosted by BioRender. OAuth login required. Access scope depends on your BioRender subscription tier.

## Sources

- [Anthropic tutorial](https://claude.com/resources/tutorials/using-the-biorender-connector-in-claude)
- [BioRender × Anthropic partnership announcement (BusinessWire, 2025-10-23)](https://www.businesswire.com/news/home/20251023858531/en/BioRender-and-Anthropic-Partner-To-Bring-Scientific-Illustrations-to-Claude-For-Life-Sciences)
- [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=biorender&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbiorender.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
