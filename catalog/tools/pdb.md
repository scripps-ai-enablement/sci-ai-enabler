---
title: PDB MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Augmented Nature
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
last_verified: 2026-06-10
summary: MCP server that lets Claude search, fetch, and validate RCSB Protein Data Bank structures with UniProt cross-referencing.
---

# PDB MCP Server

MCP server fronting the RCSB Protein Data Bank — experimental structures, validation reports, and UniProt cross-references. Two community servers are catalogued here: a local REST-based server (Augmented Nature) and a hosted GraphQL server (QuentinCody).

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Augmented Nature](https://github.com/Augmented-Nature/PDB-MCP-Server) · [QuentinCody](https://github.com/QuentinCody/rcsb-pdb-mcp-server) (community OSS) |
| **Availability** | GA — both actively published; Augmented Nature on mcpservers.org/LobeHub, QuentinCody deployed on Cloudflare Workers |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only |

## How to install

**Option A — Augmented Nature (local, REST, fixed tool set).** Clone and build:

```
git clone https://github.com/Augmented-Nature/PDB-MCP-Server
cd PDB-MCP-Server
npm install
npm run build
```

Then add to `claude_desktop_config.json` (replace `/path/to/PDB-MCP-Server` with the absolute path of your clone — e.g., `/Users/you/repos/PDB-MCP-Server`, or `$(pwd)` if you're still inside it from the previous step):

```json
{
  "mcpServers": {
    "pdb-server": {
      "command": "node",
      "args": ["/path/to/PDB-MCP-Server/build/index.js"]
    }
  }
}
```

For Claude Code, the equivalent registration is (stdio — Claude launches the process itself, no separate terminal needed):

```
claude mcp add --transport stdio pdb-server -- node /path/to/PDB-MCP-Server/build/index.js
```

**Option B — QuentinCody (hosted, GraphQL).** This server is deployed on Cloudflare Workers; nothing to build or keep running locally. Register the remote endpoint with Claude Code:

```
claude mcp add --transport sse rcsb-pdb https://rcsb-pdb-mcp-server.quentincody.workers.dev/sse
```

For Claude Desktop (no native SSE transport), use an `mcp-remote` proxy entry in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rcsb-pdb": {
      "command": "npx",
      "args": ["mcp-remote", "https://rcsb-pdb-mcp-server.quentincody.workers.dev/sse"]
    }
  }
}
```

## What it does

**Augmented Nature (REST)** — fixed tool set:

- `search_structures`
- `get_structure_info`
- `download_structure` (PDB / mmCIF / mmTF / XML)
- `search_by_uniprot`
- `get_structure_quality`

**QuentinCody (GraphQL)** — exposes the RCSB Data API's GraphQL endpoint so Claude composes arbitrary queries: entry metadata, experimental method, molecules/sequences, and Computed Structure Models (CSMs).

**Primary use cases**: Pull experimental 3D structures into Claude workflows; map UniProt to PDB; assess structure validation quality before downstream modeling; flexible GraphQL queries over PDB metadata and computed models.

## Notes

The Augmented Nature server is Node/stdio, no auth, calls the public RCSB REST API; its LICENSE file is present but type unspecified in the README — verify before redistributing. The QuentinCody server is a hosted Cloudflare Worker (MIT License with an academic-citation requirement) and exposes a single GraphQL query surface rather than discrete typed tools. Both are read-only.

## Sources

- [`Augmented-Nature/PDB-MCP-Server`](https://github.com/Augmented-Nature/PDB-MCP-Server)
- [mcpservers.org listing](https://mcpservers.org/servers/Augmented-Nature/PDB-MCP-Server)
- [`QuentinCody/rcsb-pdb-mcp-server`](https://github.com/QuentinCody/rcsb-pdb-mcp-server)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pdb&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpdb.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
