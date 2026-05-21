---
title: PubChem MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: JackKuo666
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-05-20
summary: MCP server that lets Claude query PubChem for compounds by name, SMILES, CID, or formula and pull structure files.
---

# PubChem MCP Server

Read-only MCP wrapper over PubChem's public chemical-compound database. Complements bioactivity-focused ChEMBL by adding broad compound lookup.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [JackKuo666](https://github.com/JackKuo666/PubChem-MCP-Server) (community OSS, hosted on Smithery) |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT); PubChem API is public, no key required |
| **Capabilities** | Read-only |

## How to install

- **Claude Desktop / Code — Smithery one-liner** (handles install + Claude config in one step):
  ```
  npx -y @smithery/cli@latest install @JackKuo666/pubchem-mcp-server --client claude --config "{}"
  ```
- **Manual install** — pip-install the package first, then register:
  ```
  pip install pubchem-mcp-server
  ```
  Claude Code:
  ```
  claude mcp add --transport stdio pubchem -- python -m pubchem-mcp-server
  ```
  Claude Desktop — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "pubchem": { "command": "python", "args": ["-m", "pubchem-mcp-server"] }
    }
  }
  ```

## What it does

- `search_pubchem_by_name`
- `search_pubchem_by_smiles`
- `get_pubchem_compound_by_cid`
- `search_pubchem_advanced` (formula / property filters)

**Primary use cases**: Look up compounds by name / SMILES / CID / formula, retrieve PubChem property records, generate structure files for downstream cheminformatics.

## Notes

stdio transport. Backed by FastMCP. No authentication required. PubChem's broad compound coverage makes this a natural pair with the ChEMBL bioactivity connector bundled in `bio-research`.

## Sources

- [`JackKuo666/PubChem-MCP-Server`](https://github.com/JackKuo666/PubChem-MCP-Server)
- [Alternative TypeScript implementation `@cyanheads/pubchem-mcp-server`](https://www.npmjs.com/package/@cyanheads/pubchem-mcp-server)
