---
title: UniProt MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Augmented Nature
availability: GA
tool_categories: [Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Drug Repurposing and Discovery]
last_verified: 2026-05-20
summary: MCP server giving Claude 26 tools over the UniProt REST API for protein search, domains, orthologs, PTMs, pathways, and multi-format export.
---

# UniProt MCP Server

MCP wrapper over the UniProt REST API — the standard protein-annotation layer linking sequence, structure, function, and cross-references to other databases.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Augmented Nature](https://github.com/Augmented-Nature/UniProt-MCP-Server) (community OSS) |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read-only |

## How to install

```
git clone https://github.com/Augmented-Nature/UniProt-MCP-Server
cd UniProt-MCP-Server
npm install
npm run build
```

Then add to `claude_desktop_config.json` (replace `/path/to/UniProt-MCP-Server` with the absolute path of your clone — e.g., `/Users/you/repos/UniProt-MCP-Server`):

```json
{
  "mcpServers": {
    "uniprot": { "command": "node", "args": ["/path/to/UniProt-MCP-Server/build/index.js"] }
  }
}
```

For Claude Code, the equivalent registration is:

```
claude mcp add --transport stdio uniprot -- node /path/to/UniProt-MCP-Server/build/index.js
```

Docker alternative: `docker build -t uniprot-mcp-server . && docker run -i uniprot-mcp-server`.

## What it does

26 tools across:

- **Core protein analysis** — search, get by accession, sequence and feature retrieval.
- **Comparative / evolutionary** — orthologs, taxonomy, phylogeny.
- **Structure / function** — domain, PTM, active-site annotation; AlphaFold cross-references.
- **Biological context** — pathways, GO terms, subcellular localization.
- **Batch search** and cross-reference resolution.
- **Export** — FASTA, GFF, GenBank, EMBL, TSV, XML, JSON.

**Primary use cases**: Resolve gene-to-protein-to-domain context for a hit list; pull orthologs and PTMs; build cross-reference tables for a target panel.

## Notes

stdio transport. No auth required — calls the public UniProt REST API. Complements ChEMBL (small molecules) and AlphaFold (3D) by covering the annotation layer.

## Sources

- [`Augmented-Nature/UniProt-MCP-Server`](https://github.com/Augmented-Nature/UniProt-MCP-Server)
