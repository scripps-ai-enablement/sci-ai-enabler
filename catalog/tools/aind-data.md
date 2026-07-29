---
title: AIND Data MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Allen Institute for Neural Dynamics
availability: Beta
tool_categories: [Neuroscience]
last_verified: 2026-06-14
verification: degraded
verified_on: 2026-07-29
verification_note: "PyPI aind-data-mcp v0.4.5 resolves but upstream README now documents a remote HTTP endpoint (metadata-portal.allenneuraldynamics.org/mcp, responds 406 to browser) not the stdio console-script the page had; fixed the install block to the current HTTP transport this run"
security: cleared
security_on: 2026-07-29
security_note: "provenance matches supplier Allen Institute (AllenNeuralDynamics org), PyPI aind-data-mcp v0.4.5 MIT present, repo maintained (pushed 2026-07-13), read-only, no OSV advisories"
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
| **Verified** | degraded · 2026-07-29 — PyPI package resolves but upstream now ships a remote HTTP endpoint; install block fixed to the HTTP transport this run |
| **Security** | cleared · 2026-07-29 — provenance matches Allen Institute, PyPI MIT, maintained, read-only, no OSV advisories |

The server is now hosted by AIND as a remote HTTP MCP endpoint (`https://metadata-portal.allenneuraldynamics.org/mcp/`); no local install is required.

Register with Claude Code:

```
claude mcp add --transport http aind_data_access https://metadata-portal.allenneuraldynamics.org/mcp/
```

Or for Claude Desktop, add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "aind_data_access": { "type": "http", "url": "https://metadata-portal.allenneuraldynamics.org/mcp/" }
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

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=aind-data&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Faind-data.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
