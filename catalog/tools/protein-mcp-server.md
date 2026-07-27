---
title: Protein MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: cyanheads
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-07-25
summary: Federated protein-structure search across experimental (PDB) and predicted (AlphaFold) models — homolog search, structural alignment, ligand and annotation lookup, keyless.
verification: works
verified_on: 2026-07-27
verification_note: "npm @cyanheads/protein-mcp-server 0.4.0 resolves and its bin protein-mcp-server maps to dist/index.js confirming the npx launch"
security: cleared
security_on: 2026-07-27
security_note: "provenance matches cyanheads, Apache-2.0, maintained (pushed 2026-07-03), no OSV advisories"
---

# Protein MCP Server

Query experimental and predicted protein structures through one keyless MCP server that federates RCSB PDB, AlphaFold DB, 3D-Beacons, UniProt, InterPro, and Foldseek.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [cyanheads](https://github.com/cyanheads/protein-mcp-server) |
| **Availability** | GA |
| **Pricing** | Free / OSS (Apache-2.0) |
| **Capabilities** | Read-only — searches, fetches, aligns, and annotates public structure/sequence data; no writes |
| **Verified** | works · 2026-07-27 — npm 0.4.0 resolves; bin protein-mcp-server confirms the npx launch |
| **Security** | cleared · 2026-07-27 — provenance matches cyanheads, Apache-2.0, maintained, no OSV advisories |

## How to install

- **Claude Code** — direct MCP add (stdio via npx):
  ```
  claude mcp add --transport stdio protein-mcp-server -- npx -y @cyanheads/protein-mcp-server@latest
  ```
- **Claude Code** — public hosted HTTP instance:
  ```
  claude mcp add --transport http protein https://protein.caseyjhand.com/mcp
  ```
- **Claude Desktop** — stdio via npx in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "protein-mcp-server": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@cyanheads/protein-mcp-server@latest"],
        "env": {
          "MCP_TRANSPORT_TYPE": "stdio",
          "MCP_LOG_LEVEL": "info"
        }
      }
    }
  }
  ```
- **Claude Desktop** — to use the hosted HTTP instance instead (Desktop has no native HTTP transport), proxy it with `mcp-remote`:
  ```json
  {
    "mcpServers": {
      "protein": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://protein.caseyjhand.com/mcp"]
      }
    }
  }
  ```

`npx` fetches the package on first launch; no separate `pip`/`npm install` step is required. Claude Code/Desktop launches the stdio process itself — there is no long-running server to keep open in another terminal.

## What it does

Exposes seven tools over public structure and annotation APIs:

- `protein_search_structures` — search experimental (PDB) and predicted structures.
- `protein_get_structure` — fetch metadata and coordinate files by ID.
- `protein_find_similar` — find sequence homologs (RCSB mmseqs2) or fold homologs (Foldseek) from a sequence, PDB ID, or UniProt accession.
- `protein_track_ligands` — ligand discovery and binding-site analysis.
- `protein_compare_structures` — structurally align 2–10 structures via TM-align / jFATCAT.
- `protein_analyze_collection` — profile a set of PDB entries with server-side facets.
- `protein_get_annotations` — fetch UniProt features and InterPro domains.

**Primary use cases**: federated experimental-plus-predicted structure lookup, sequence/fold homolog search, multi-structure alignment, ligand and annotation retrieval.

## Notes

Every upstream provider (RCSB PDB, AlphaFold DB, 3D-Beacons, UniProt, InterPro, Foldseek) is public and keyless, so the server runs out of the box with no configuration. Both stdio and Streamable HTTP transports are supported. It is a data-retrieval and comparison layer — pair it with [PyMOL](pymol.html) or the [ChimeraX MCP Server](chimerax-mcp.html) to render or edit the structures it returns, and with [AlphaFold](alphafold.html) for de-novo prediction. Overlaps but broadens the RCSB-only [PDB MCP Server](pdb.html) by federating predicted models and adding TM-align/Foldseek comparison.

## Sources

- [`cyanheads/protein-mcp-server`](https://github.com/cyanheads/protein-mcp-server)
- [`@cyanheads/protein-mcp-server` on npm](https://www.npmjs.com/package/@cyanheads/protein-mcp-server)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=protein-mcp-server&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fprotein-mcp-server.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
