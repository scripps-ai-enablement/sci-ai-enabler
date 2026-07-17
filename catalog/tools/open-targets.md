---
title: Open Targets Plugin
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Open Targets
availability: GA
flagged: MCP endpoint fails `initialize` handshake with JSON-RPC -32602 ("Invalid request parameters") under protocolVersion 2025-06-18 and 2024-11-05 — no tools register; reported 2026-06-15
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-17
claude_science: true
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
- **Claude Code / Desktop** — working community alternative (Augmented Nature, OSS) while the official endpoint is down (see Notes):
  ```
  git clone https://github.com/Augmented-Nature/OpenTargets-MCP-Server
  cd OpenTargets-MCP-Server
  npm install && npm run build
  claude mcp add --transport stdio opentargets-server -- node /path/to/OpenTargets-MCP-Server/build/index.js
  ```

## What it does

- `get_open_targets_graphql_schema` — retrieve the live GraphQL schema
- `get_type_dependencies`
- `query_open_targets_graphql` — execute a GraphQL query
- `batch_query_open_targets_graphql`
- `search_entities`

**Primary use cases**: Target prioritisation, drug repurposing via target-disease evidence, mechanism and genetics lookup, building cross-evidence panels for a target shortlist.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Clinical Genomics* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Streamable HTTP transport, no auth. The `bio-research` umbrella plugin references Open Targets indirectly; this is the discrete first-party entry. Tagged experimental — schema may evolve.

**Field report (2026-06-15):** The remote endpoint `https://mcp.platform.opentargets.org/mcp` currently fails the MCP `initialize` handshake, returning JSON-RPC `-32602 "Invalid request parameters"` under both protocolVersion `2025-06-18` and `2024-11-05`. The endpoint is reachable (HTTP 200, `content-type: text/event-stream`) but non-compliant on initialize, so `claude mcp list` shows "Failed to connect", no tools register, and a Claude Code restart does not help (server-side issue). Workarounds that work today: (1) query the Open Targets public GraphQL API directly at `https://api.platform.opentargets.org/api/v4/graphql`, (2) use [ToolUniverse](tooluniverse.html)'s `OpenTargets_*` / `disease_target_score` tools, or (3) run the community **Augmented Nature Open Targets MCP** (install path above).

**Verified 2026-07-17:** the [Augmented Nature Open Targets MCP](https://github.com/Augmented-Nature/OpenTargets-MCP-Server) builds cleanly (`npm install && npm run build`) and **passes the `initialize` handshake** (protocolVersion `2024-11-05`) over stdio locally — the exact step the official endpoint fails. It registers 6 tools (`search_targets`, `search_diseases`, `get_target_disease_associations`, `get_disease_targets_summary`, `get_target_details`, `get_disease_details`) and returns live data from the public GraphQL API (e.g., `search_targets{query:"BRAF"}` → `ENSG00000157764`; `get_target_disease_associations{targetId:"ENSG00000157764"}` → cardiofaciocutaneous syndrome (0.88), Noonan syndrome, …). Its tool set is smaller and its schema differs from the official server (e.g., associations take `targetId`/`diseaseId`, and require at least one).

## Sources

- [`anthropics/life-sciences` marketplace](https://github.com/anthropics/life-sciences)
- [`opentargets/open-targets-platform-mcp`](https://github.com/opentargets/open-targets-platform-mcp)
- [Open Targets blog: official MCP](https://blog.opentargets.org/official-open-targets-mcp/)
- [`Augmented-Nature/OpenTargets-MCP-Server`](https://github.com/Augmented-Nature/OpenTargets-MCP-Server) (working community alternative, verified 2026-07-17)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=open-targets&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fopen-targets.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
