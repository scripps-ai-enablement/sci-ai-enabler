---
title: Ensembl MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: effieklimi
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine]
last_verified: 2026-06-11
summary: MCP server over the Ensembl REST API for gene/transcript lookup, sequence retrieval, variant consequences, comparative genomics, and assembly lift-over.
---

# Ensembl MCP Server

An MCP server that exposes the Ensembl REST API so Claude can look up genes and transcripts, fetch sequences, interpret variants, and run comparative-genomics queries from natural language.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [effieklimi](https://github.com/effieklimi/ensembl-mcp-server) |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT). Ensembl REST API needs no key; the Smithery installer path requires a free Smithery key. |
| **Capabilities** | Read-only — queries the public Ensembl REST API |

## How to install

The server is published to npm as `ensembl-mcp-server` and runs over stdio via `npx`.

- **Claude Code** — direct MCP add (stdio; Claude Code launches the process itself, so don't run `npx` separately):
  ```
  claude mcp add --transport stdio ensembl -- npx -y ensembl-mcp-server
  ```
- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "ensembl": { "command": "npx", "args": ["-y", "ensembl-mcp-server"] }
    }
  }
  ```
- **Either client — via Smithery** (requires a free Smithery key; replace `your-smithery-key` with the key from your Smithery dashboard):
  ```
  npx -y @smithery/cli@latest install @effieklimi/ensembl-mcp-server --client claude --key your-smithery-key
  ```

Requires Node.js. No Ensembl account or API key is needed for the REST API itself.

## What it does

Ten tools spanning the Ensembl REST API:

- `ensembl_lookup` — ID/symbol translation, cross-references, variant recoding
- `ensembl_sequence` — DNA, RNA, and protein sequence retrieval
- `ensembl_feature_overlap` — genes/transcripts/regulatory elements overlapping a region
- `ensembl_mapping` — coordinate conversion and assembly lift-over
- `ensembl_variation` — variant lookup, VEP consequences, phenotype mapping
- `ensembl_compara` — comparative genomics, homology, gene trees
- `ensembl_regulatory` — regulatory features, binding matrices, annotations
- `ensembl_protein_features` — protein domains and functional sites
- `ensembl_ontotax` — ontology and taxonomy traversal
- `ensembl_meta` — server metadata, species lists, release info

**Primary use cases**: Gene/transcript annotation lookup, sequence retrieval, variant consequence prediction, cross-species homology, genome-coordinate lift-over.

## Notes

Read-only wrapper over the public Ensembl REST API; no write operations. A separate hosted HTTP variant exists via the Pipeworx gateway (`claude mcp add --transport http ensembl https://gateway.pipeworx.io/ensembl/mcp`), and `Augmented-Nature/Ensembl-MCP-Server` is an alternative implementation — the npm `ensembl-mcp-server` package documented above is the most direct install for Claude.

## Sources

- [`effieklimi/ensembl-mcp-server`](https://github.com/effieklimi/ensembl-mcp-server)
- [Ensembl REST API](https://rest.ensembl.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=ensembl&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fensembl.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
