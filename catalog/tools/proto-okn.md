---
title: Proto-OKN MCP Server
parent: All tools
grand_parent: Catalog
nav_order: 1
tool_type: MCP server
supplier: SBL-SDSC (San Diego Supercomputer Center)
availability: Beta
tool_categories: [All]
last_verified: 2026-07-18
summary: Natural-language access to 30+ NSF Proto-OKN scientific knowledge graphs (SPOKE biomedicine, BioBricks chemical safety, more) via SPARQL, schema inspection, and cross-graph bridging.
---

# Proto-OKN MCP Server

A single MCP server that lets Claude discover, inspect, and query 30+ NSF-funded Prototype Open Knowledge Network (Proto-OKN) scientific knowledge graphs — including SPOKE biomedicine and BioBricks ICE chemical safety — in natural language.

| | |
|---|---|
| **Type** | MCP server (remote, streamable HTTP; self-host also available) |
| **Supplier** | [SBL-SDSC](https://github.com/sbl-sdsc/mcp-proto-okn) — Structural Bioinformatics Laboratory, San Diego Supercomputer Center |
| **Availability** | Beta — hosted endpoint live; source repo [`sbl-sdsc/mcp-proto-okn`](https://github.com/sbl-sdsc/mcp-proto-okn) |
| **Pricing** | Free / OSS (BSD 3-Clause); hosted endpoint is free but requires a Claude Pro/Max subscription for custom connectors |
| **Capabilities** | Read-only — knowledge-graph discovery, SPARQL query, cross-graph identifier bridging |

## How to install

- **Claude.ai / Claude Desktop** — Settings → Connectors → **Add custom connector**. Name it `proto-okn`, server URL `https://apps.okn.us/okn-mcp/mcp`, then click **Configure** and set tool permissions to **Always allow**. In a new chat, toggle `proto-okn` on. (Requires a Claude Pro or Max subscription for MCP connectors.)
- **Claude Code** — direct remote MCP add:
  ```
  claude mcp add --transport http proto-okn https://apps.okn.us/okn-mcp/mcp
  ```
  This is a long-lived hosted service — nothing to run locally. After adding, run `/mcp` to confirm the server is connected. (Equivalently, add a `"proto-okn"` entry with `"type": "url"` and `"url": "https://apps.okn.us/okn-mcp/mcp"` under `mcpServers` in your project `.mcp.json`.)
- **Self-host (optional)** — clone [`sbl-sdsc/mcp-proto-okn`](https://github.com/sbl-sdsc/mcp-proto-okn) and follow `docs/develop.md` to run the server locally; only needed if you want your own instance rather than the hosted endpoint above.

## What it does

Exposes 30+ Proto-OKN knowledge graphs (hosted on the FRINK federation platform, catalogued in the OKN Knowledge Graph Registry) through one unified interface. Capabilities:

- **Graph discovery and filtering** — list and route to relevant knowledge graphs
- **Schema inspection** — inspect a graph's classes, predicates, and structure
- **SPARQL execution** — run queries against a chosen graph
- **Cross-graph identifier bridging** — link IDs across graphs
- **Multi-graph querying** — combine results from several sources
- **Ontology-driven query expansion** — automatically expand queries via MONDO, HP, GO, UBERON, and ChEBI hierarchies (through Ubergraph) so a search for a parent concept matches all descendants
- **Transcript / schema-visualization generation**

Covered graphs include SPOKE (Scalable Precision Medicine Open Knowledge Engine), BioBricks ICE (chemical safety / cheminformatics), DREAM-KG, and SAWGraph (agricultural products and water monitoring).

**Primary use cases**: Cross-domain scientific knowledge-graph Q&A, SPARQL query authoring, biomedical/chemical-safety knowledge integration.

## Notes

Beta as of 2026-07-18; the team welcomes feedback and bug reports via GitHub issues. The hosted endpoint (`https://apps.okn.us/okn-mcp/mcp`) requires no local install and no API key, but visiting it in a browser returns a JSON-RPC / HTTP error (it speaks the MCP protocol, not plain HTTP GET) — that is expected and does not indicate an outage. The MCP URL and setup steps have changed over the project's life; check the GitHub repo for the latest.

Surfaced from user request [#50](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/50) (@goodb). The request suggested the `General-Purpose Utilities` shelf, but the server is a cross-domain life-science knowledge-graph gateway (SPOKE biomedicine, BioBricks chemical safety, ChEBI/MONDO/GO/HP/UBERON ontology expansion), so it is tagged `All`.

Part of the NSF Proto-OKN program. Described in arXiv preprint [2605.30283](https://arxiv.org/abs/2605.30283).

## Sources

- [`sbl-sdsc/mcp-proto-okn`](https://github.com/sbl-sdsc/mcp-proto-okn)
- [OKN — MCP Server page](https://okn.us/mcp)
- [mcp-proto-okn: Natural-language access to open scientific knowledge graphs (arXiv 2605.30283)](https://arxiv.org/abs/2605.30283)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=proto-okn&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fproto-okn.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
