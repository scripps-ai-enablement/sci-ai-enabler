---
title: Synapse.org Connector
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Sage Bionetworks
availability: GA
tool_categories: [All]
last_verified: 2026-08-01
verification: works
verified_on: 2026-07-20
verification_note: "synapse plugin dir confirmed in the anthropics/life-sciences marketplace repo and endpoint is on Sage's mcp.synapse.org; functional connect is OAuth/account-gated so verified via primary source not a live call"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier Sage Bionetworks (endpoint on synapse.org, plugin in official marketplace); hosted connector, per-project governance controls apply and Synapse ToS restrict redistribution"
summary: Discovery and metadata retrieval across Synapse-hosted biomedical datasets and consortium projects.
---

# Synapse.org Connector

Discover Synapse projects, browse data-asset structure, and retrieve metadata for authorised users across Synapse-hosted biomedical data.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Sage Bionetworks](https://www.synapse.org/) |
| **Availability** | GA — released with the Claude for Life Sciences launch (Oct 2025) |
| **Pricing** | Free / OSS — requires a free Synapse account; some datasets require governance approval |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 — synapse plugin confirmed in anthropics/life-sciences marketplace, endpoint on mcp.synapse.org (OAuth-gated) |
| **Security** | cleared · 2026-07-20 — provenance matches Sage Bionetworks; hosted connector, per-project governance + ToS restrictions |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install synapse@life-sciences
  ```
- **Claude Code** — direct MCP add:
  ```
  claude mcp add --transport http synapse https://mcp.synapse.org/mcp
  ```
- **Claude.ai** — Synapse.org connector; toggle in **Settings → Connectors** (OAuth2 sign-in).

## What it does

Project discovery and listing, file/folder structure inspection, metadata retrieval for Synapse-hosted data assets, cross-project search subject to per-project access controls.

**Primary use cases**: Discovering biomedical datasets hosted on Synapse, retrieving project and file metadata, navigating consortium and DREAM-challenge data structures.

## Notes

Remote MCP server hosted at `mcp.synapse.org/mcp` over HTTP transport. OAuth2 default (browser-based); personal access tokens are supported as an alternative. Data access is governed by per-project controls (some require Synapse governance approval). Synapse Terms of Service restrict data redistribution, which may include third-party AI providers — review before connecting controlled datasets.

## Sources

- [Anthropic tutorial](https://claude.com/resources/tutorials/using-the-synapse-org-connector-in-claude)
- [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences)
- [Synapse MCP server source](https://github.com/susheel/synapse-mcp)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=synapse&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fsynapse.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
