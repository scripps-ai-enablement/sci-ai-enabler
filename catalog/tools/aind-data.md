---
title: AIND Data MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Allen Institute for Neural Dynamics
availability: Beta
tool_categories: [Neuroscience]
last_verified: 2026-05-20
summary: Official Allen Institute MCP server giving Claude query and NWB-introspection access to AIND's V2 neuroscience data assets.
---

# AIND Data MCP

Official Allen Institute for Neural Dynamics MCP server for querying AIND's V2 metadata DocDB and inspecting NWB assets. Supersedes the now-archived `aind-metadata-mcp`.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Allen Institute for Neural Dynamics](https://github.com/AllenNeuralDynamics/aind-data-mcp) |
| **Availability** | Beta — active through April 2026 |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read-only — public read access to AIND DocDB |

## How to install

```
uv tool install aind-data-mcp
```

Then add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "aind_data_access": { "type": "stdio", "command": "aind-data-mcp", "timeout": 300 }
  }
}
```

## What it does

- MongoDB-style `filter` / `projection` queries against the AIND DocDB
- Aggregation pipelines across AIND data assets
- NWB file metadata access (V2 schema)

**Primary use cases**: Find AIND open neurophysiology / imaging datasets; build cohort queries over the AIND DocDB; inspect NWB structure before downstream pipelines.

## Notes

stdio transport, public read access, Python 3.11+. The V1 predecessor `aind-metadata-mcp` is archived — use this one.

## Sources

- [`AllenNeuralDynamics/aind-data-mcp`](https://github.com/AllenNeuralDynamics/aind-data-mcp)
- [mcpmarket.com listing](https://mcpmarket.com/server/aind-data)
