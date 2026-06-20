---
title: Open Targets Plugin
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Open Targets
availability: GA
flagged: MCP endpoint fails `initialize` handshake with JSON-RPC -32602 ("Invalid request parameters") under protocolVersion 2025-06-18 and 2024-11-05 — no tools register; reported 2026-06-15
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-06-20
summary: Official Open Targets MCP plugin giving Claude GraphQL access to target-disease associations, drug evidence, and target-prioritisation scores.
---

# Open Targets Plugin

Anthropic-packaged Claude Code plugin that wraps the **official Open Targets MCP server**, the canonical resource for target-disease associations and target-prioritisation scores in drug discovery.

| | |
|---|---|
| **Type** | Claude Code Plugin (wraps a remote MCP server) |
| **Supplier** | Open Targets consortium (EMBL-EBI, Wellcome Sanger, GSK, Bristol Myers Squibb, …); plugin packaged by Anthropic |
| **Availability** | GA in the `life-sciences` marketplace; underlying MCP server tagged "experimental" — release 2026.03.1 (April 7, 2026) |
| **Pricing** | Free / OSS (Apache-2.0 server; Open Targets data CC0) |
| **Capabilities** | Read-only |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install open-targets@life-sciences
  ```
- **Claude Code / Desktop** — direct MCP:
  ```
  claude mcp add --transport http open-targets https://mcp.platform.opentargets.org/mcp
  ```

## What it does

- `get_open_targets_graphql_schema` — retrieve the live GraphQL schema
- `get_type_dependencies`
- `query_open_targets_graphql` — execute a GraphQL query
- `batch_query_open_targets_graphql`
- `search_entities`

**Primary use cases**: Target prioritisation, drug repurposing via target-disease evidence, mechanism and genetics lookup, building cross-evidence panels for a target shortlist.

## Notes

Streamable HTTP transport, no auth. The `bio-research` umbrella plugin references Open Targets indirectly; this is the discrete first-party entry. Tagged experimental — schema may evolve.

**Field report (2026-06-15):** The remote endpoint `https://mcp.platform.opentargets.org/mcp` currently fails the MCP `initialize` handshake, returning JSON-RPC `-32602 "Invalid request parameters"` under both protocolVersion `2025-06-18` and `2024-11-05`. The endpoint is reachable (HTTP 200, `content-type: text/event-stream`) but non-compliant on initialize, so `claude mcp list` shows "Failed to connect", no tools register, and a Claude Code restart does not help (server-side issue). Workarounds that work today: (1) query the Open Targets public GraphQL API directly at `https://api.platform.opentargets.org/api/v4/graphql`, or (2) use [ToolUniverse](tooluniverse.html)'s `OpenTargets_*` / `disease_target_score` tools.

## Sources

- [`anthropics/life-sciences` marketplace](https://github.com/anthropics/life-sciences)
- [`opentargets/open-targets-platform-mcp`](https://github.com/opentargets/open-targets-platform-mcp)
- [Open Targets blog: official MCP](https://blog.opentargets.org/official-open-targets-mcp/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=open-targets&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fopen-targets.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
