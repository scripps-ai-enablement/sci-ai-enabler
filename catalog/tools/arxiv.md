---
title: arXiv MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: blazickjp
availability: GA
tool_categories: [All]
last_verified: 2026-07-17
claude_science: true
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches blazickjp, GitHub Apache-2.0 and PyPI arxiv-mcp-server v0.5.1 present, no OSV advisories"
summary: Search and retrieve arXiv preprints (incl. q-bio) and metadata; part of the Literature Graph connector in Claude Science.
---

# arXiv MCP Server

Searches arXiv and retrieves preprint metadata and full text via a community MCP server.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [blazickjp](https://github.com/blazickjp/arxiv-mcp-server) |
| **Availability** | GA — community OSS (PyPI) |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches blazickjp, Apache-2.0, no OSV advisories |

## How to install

- **Claude Code** — community MCP server ([blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server), OSS):
  ```
  claude mcp add arxiv -- uvx arxiv-mcp-server
  ```
- **Claude Science** — also available as the *Literature Graph* featured connector (Anthropic-hosted; enable in Claude Science).
- **Public API** — query directly at [export.arxiv.org/api](https://export.arxiv.org/api).

## What it does

Search arXiv by query/author/category, fetch paper metadata and abstracts, and download/parse full text — covering the q-bio and related preprint corpus alongside physics/CS.

**Primary use cases**: Preprint discovery, literature triage, methods-paper retrieval

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Literature Graph* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

In Claude Science, arXiv is paired with OpenAlex in the Literature Graph connector; see [OpenAlex](openalex-database.html).

## Sources

- [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server)
- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=arxiv&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Farxiv.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
