---
title: PDB MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Augmented Nature
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
last_verified: 2026-05-20
summary: MCP server that lets Claude search, fetch, and validate RCSB Protein Data Bank structures with UniProt cross-referencing.
---

# PDB MCP Server

MCP server fronting the RCSB Protein Data Bank — experimental structures, validation reports, and UniProt cross-references.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Augmented Nature](https://github.com/Augmented-Nature/PDB-MCP-Server) (community OSS) |
| **Availability** | GA — active main branch, listed on mcpservers.org and LobeHub |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only |

## How to install

```
git clone https://github.com/Augmented-Nature/PDB-MCP-Server
cd PDB-MCP-Server
npm install
npm run build
```

Then add to `claude_desktop_config.json`:

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

## What it does

- `search_structures`
- `get_structure_info`
- `download_structure` (PDB / mmCIF / mmTF / XML)
- `search_by_uniprot`
- `get_structure_quality`

**Primary use cases**: Pull experimental 3D structures into Claude workflows; map UniProt to PDB; assess structure validation quality before downstream modeling.

## Notes

Node/stdio transport. No auth required — calls the public RCSB REST API. LICENSE file present but type unspecified in the README; verify before redistributing.

## Sources

- [`Augmented-Nature/PDB-MCP-Server`](https://github.com/Augmented-Nature/PDB-MCP-Server)
- [mcpservers.org listing](https://mcpservers.org/servers/Augmented-Nature/PDB-MCP-Server)
