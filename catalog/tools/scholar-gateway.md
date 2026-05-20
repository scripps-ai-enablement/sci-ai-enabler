---
title: Scholar Gateway Connector (Wiley)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Wiley
availability: Beta
tool_categories: [All]
last_verified: 2026-05-20
summary: Wiley remote connector for peer-reviewed scholarly content — 3M+ articles, 300+ Life Sciences journals.
---

# Scholar Gateway Connector (Wiley)

Search Wiley's Scholar Gateway corpus and retrieve scholarly article metadata, abstracts, and DOI-linked content.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Wiley](https://www.wiley.com/) |
| **Availability** | Beta — released alongside Claude for Life Sciences (Oct 2025) |
| **Pricing** | Free / OSS — requires a free Scholar Gateway account |
| **Capabilities** | Read-only |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install wiley-scholar-gateway@life-sciences
  ```
  Sign in with Scholar Gateway credentials when prompted.
- **Claude.ai** — Scholar Gateway connector; toggle in **Settings → Connectors**, then sign in with Scholar Gateway credentials.

## What it does

Scholarly-article search, publication metadata retrieval, full-text and DOI-linked access for Wiley-indexed content (3M+ articles across STEM, including 300+ Life Sciences journals covering 900,000+ research articles).

**Primary use cases**: Literature search grounded in peer-reviewed sources, citation-verifiable Q&A, supplementing PubMed with Wiley-published journal content.

## Notes

Remote MCP server hosted at `connector.scholargateway.ai/mcp`. HTTP transport. OAuth login flow on first use. Access scope is tied to your Scholar Gateway account.

## Sources

- [Anthropic tutorial](https://claude.com/resources/tutorials/using-the-scholar-gateway-connector-in-claude)
- [DeepWiki: Wiley Scholar Gateway](https://deepwiki.com/anthropics/life-sciences/3.5-wiley-scholar-gateway)
- [Wiley AI Gateway press release (2025)](https://newsroom.wiley.com/press-releases/press-release-details/2025/Wiley-Launches-Interoperable-Platform-to-Power-Scientific-Discovery-in-Worlds-Leading-AI-Technologies/default.aspx)
