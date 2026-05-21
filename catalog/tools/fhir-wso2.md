---
title: WSO2 FHIR MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: WSO2
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-05-20
summary: Open-source MCP bridge that lets Claude search, read, and write FHIR R4 resources against any EHR or sandbox FHIR API with SMART-on-FHIR auth.
---

# WSO2 FHIR MCP Server

Open-source MCP bridge between Claude and any HL7 FHIR R4 server — Cerner / Oracle Health, Epic, Azure Health Data Services, public sandboxes, or local FHIR test servers.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [WSO2](https://github.com/wso2/fhir-mcp-server) (open source) |
| **Availability** | GA — v0.10.0 (released 2025-10-30) |
| **Pricing** | Free / OSS (Apache-2.0) |
| **Capabilities** | Read/Write — full FHIR R4 CRUD |

Install the server and start it (defaults to HTTP on `localhost:8000` — keep it running in a separate terminal):

```
pip install fhir-mcp-server
fhir-mcp-server
```

Then register the HTTP endpoint with Claude Code:

```
claude mcp add --transport http fhir http://localhost:8000/mcp
```

Or for Claude Desktop (no native HTTP support — proxy via `mcp-remote`):

```json
{
  "mcpServers": {
    "fhir": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:8000/mcp"]
    }
  }
}
```

## What it does

- `search` — FHIR-style query across resource types
- `read` — fetch by resource ID
- `get_capabilities` — server capability statement
- `create`, `update`, `delete` — full CRUD
- SMART-on-FHIR authenticated user-resource fetch

**Primary use cases**: Pull patient / observation / condition records into Claude for cohort review, draft FHIR resources from clinician text, prototype agentic EHR workflows.

## Notes

SMART-on-FHIR OAuth2 (authorization-code flow) with an optional public-server mode for sandboxes. Supports stdio, SSE, and Streamable HTTP transports.

## Sources

- [`wso2/fhir-mcp-server`](https://github.com/wso2/fhir-mcp-server)
- [PyPI `fhir-mcp-server`](https://pypi.org/project/fhir-mcp-server/)
