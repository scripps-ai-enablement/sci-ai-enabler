---
title: ArrayExpress / BioStudies MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Augmented Nature
availability: Beta
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-07-17
claude_science: true
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "provenance matches supplier Augmented-Nature, repo resolves and read-only, no OSV advisories, but no LICENSE file and repo unmaintained since 2025-12 (community, 2 stars)"
summary: Search functional-genomics studies and metadata in ArrayExpress/BioStudies; part of the Omics Archives connector in Claude Science.
---

# ArrayExpress / BioStudies MCP Server

Exposes ArrayExpress functional-genomics studies (via BioStudies) to Claude through a community MCP server.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Augmented Nature](https://github.com/Augmented-Nature/BioStudies-MCP-Server) |
| **Availability** | Beta — community OSS |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — provenance matches Augmented-Nature, read-only, but no LICENSE and unmaintained since 2025-12 |

## How to install

- **Claude Code / Desktop** — community MCP server ([Augmented Nature](https://github.com/Augmented-Nature/BioStudies-MCP-Server), OSS):
  ```
  git clone https://github.com/Augmented-Nature/BioStudies-MCP-Server
  cd BioStudies-MCP-Server
  npm install && npm run build
  claude mcp add --transport stdio biostudies-server -- node /path/to/BioStudies-MCP-Server/build/index.js
  ```
- **Claude Science** — also available as the *Omics Archives* featured connector (Anthropic-hosted; enable in Claude Science).
- **Public API** — query directly at [ebi.ac.uk/biostudies/api](https://www.ebi.ac.uk/biostudies/api).

## What it does

Search and retrieve ArrayExpress/BioStudies study records — sample/assay metadata, protocols, and file listings for functional-genomics experiments — via the BioStudies API.

**Primary use cases**: Functional-genomics study discovery, experiment metadata retrieval

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Omics Archives* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

ArrayExpress is now served through EMBL-EBI BioStudies. Part of the Omics Archives bundle alongside [GEO](geo-database.html) and [PRIDE](pride-database.html).

## Sources

- [Augmented-Nature/BioStudies-MCP-Server](https://github.com/Augmented-Nature/BioStudies-MCP-Server)
- [EMBL-EBI BioStudies / ArrayExpress](https://www.ebi.ac.uk/biostudies/arrayexpress)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=arrayexpress&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Farrayexpress.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
