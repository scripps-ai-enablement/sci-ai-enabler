---
title: PDB MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: RCSB PDB
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
last_verified: 2026-06-27
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "official first-party rcsb/rcsb-mcp MIT (GitHub API) plus PyPI rcsb-mcp 0.9.0 both resolve; provenance matches RCSB PDB, no OSV/GitHub advisories, read-only public APIs"
claude_science: true
summary: MCP servers that let Claude search, fetch, and validate RCSB Protein Data Bank structures — including the official first-party RCSB server.
---

# PDB MCP Server

MCP server fronting the RCSB Protein Data Bank — experimental structures, validation reports, and UniProt cross-references. Four servers are catalogued here: the **official first-party server maintained by RCSB PDB** (`rcsb-mcp`, recommended), plus three community servers — a local REST-based server (Augmented Nature), a hosted GraphQL server (QuentinCody), and a multi-provider server orchestrating RCSB PDB + PDBe + UniProt (cyanheads).

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [RCSB PDB](https://github.com/rcsb/rcsb-mcp) (first-party) · [Augmented Nature](https://github.com/Augmented-Nature/PDB-MCP-Server) · [QuentinCody](https://github.com/QuentinCody/rcsb-pdb-mcp-server) · [cyanheads](https://github.com/cyanheads/protein-mcp-server) (community OSS) |
| **Availability** | GA — official `rcsb-mcp` on PyPI and in the official MCP Registry (`io.github.rcsb/rcsb-mcp`); Augmented Nature on mcpservers.org/LobeHub, QuentinCody on Cloudflare Workers, cyanheads in the official MCP Registry |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — official rcsb/rcsb-mcp MIT + PyPI rcsb-mcp 0.9.0 resolve, provenance matches RCSB PDB, no advisories, read-only |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/structural-biology-drug-discovery/pdb-database` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->

**Option A — RCSB PDB official (`rcsb-mcp`, first-party, recommended).** Published to PyPI as `rcsb-mcp`; no API key (the RCSB APIs are public). Nothing to clone. Register with Claude Code over stdio (Claude launches the process itself via `uvx` — no separate terminal needed):

```
claude mcp add --transport stdio rcsb-mcp -- uvx rcsb-mcp
```

For Claude Desktop, add the equivalent stdio entry to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rcsb-mcp": {
      "command": "uvx",
      "args": ["rcsb-mcp"]
    }
  }
}
```

(`uvx` requires [uv](https://docs.astral.sh/uv/) installed — `pip install uv` or the official installer. To pin a non-`uvx` workflow instead, `pip install rcsb-mcp` and replace the command/args with `python -m rcsb_mcp.server`. The server speaks stdio, so Claude launches it on demand; you do not keep it running in a separate terminal.)

**Option B — Augmented Nature (local, REST, fixed tool set).** Clone and build:

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

**Option C — cyanheads (multi-provider, RCSB PDB + PDBe + UniProt).** Published to npm as `protein-mcp-server`; requires [Bun](https://bun.sh/) ≥ 1.2.0. No clone needed. Register with Claude Code over stdio (Claude launches the process itself — no separate terminal needed):

```
claude mcp add --transport stdio protein-mcp-server --env MCP_TRANSPORT_TYPE=stdio -- bunx protein-mcp-server@latest
```

For Claude Desktop, add the equivalent stdio entry to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "protein-mcp-server": {
      "command": "bunx",
      "args": ["protein-mcp-server@latest"],
      "env": { "MCP_TRANSPORT_TYPE": "stdio" }
    }
  }
}
```

(The server defaults to HTTP on port 3010; setting `MCP_TRANSPORT_TYPE=stdio` forces stdio so Claude Desktop, which has no native HTTP transport, can launch it directly.)

**Option D — QuentinCody (hosted, GraphQL).** This server is deployed on Cloudflare Workers; nothing to build or keep running locally. Register the remote endpoint with Claude Code:

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

**RCSB PDB official (`rcsb-mcp`)** — 40+ tools mirroring the three RCSB web APIs:

- **Search API** (~13 tools): fulltext, attribute-based, sequence-similarity, chemical-structure, 3D-shape, sequence-motif, and structural-motif search, plus resolvers for GO terms, InterPro domains, enzyme classes, diseases, and organisms.
- **Data API** (~18 tools): entry / entity / assembly / ligand lookups, annotations, experimental info, chemical components, groups, and UniProt / PubMed records.
- **Sequence Coordinates API** (~5 tools): cross-reference alignments and annotations across PDB / UniProt / NCBI.

**Augmented Nature (REST)** — fixed tool set:

- `search_structures`
- `get_structure_info`
- `download_structure` (PDB / mmCIF / mmTF / XML)
- `search_by_uniprot`
- `get_structure_quality`

**QuentinCody (GraphQL)** — exposes the RCSB Data API's GraphQL endpoint so Claude composes arbitrary queries: entry metadata, experimental method, molecules/sequences, and Computed Structure Models (CSMs).

**cyanheads (multi-provider)** — orchestrates RCSB PDB, PDBe, and UniProt behind a unified tool set:

- `protein_search_structures` — keyword/filter search with pagination
- `protein_get_structure` — full structure data by PDB ID
- `protein_find_similar` — structural / sequence homologs
- `protein_track_ligands` — find structures binding a given small molecule
- `protein_compare_structures` / `protein_analyze_collection` — comparison and database statistics (marked in development upstream)

**Primary use cases**: Pull experimental 3D structures into Claude workflows; map UniProt to PDB; assess structure validation quality before downstream modeling; flexible GraphQL queries over PDB metadata and computed models.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Structures & Interactions* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

The official `rcsb-mcp` server is maintained directly by RCSB PDB (MIT License, default branch `master`), needs no API key (the RCSB Search / Data / Sequence Coordinates APIs are public), and speaks stdio via `uvx rcsb-mcp` or `python -m rcsb_mcp.server` — prefer it over the community options for authoritative coverage. The Augmented Nature server is Node/stdio, no auth, calls the public RCSB REST API; its LICENSE file is present but type unspecified in the README — verify before redistributing. The QuentinCody server is a hosted Cloudflare Worker (MIT License with an academic-citation requirement) and exposes a single GraphQL query surface rather than discrete typed tools. The cyanheads server is Apache-2.0, requires Bun ≥ 1.2.0, needs no API key by default (supports optional JWT/OAuth modes), and supports both HTTP (default, port 3010) and stdio transports. All four servers are read-only.

## Sources

- [`rcsb/rcsb-mcp`](https://github.com/rcsb/rcsb-mcp) (official, MIT)
- [MCP Registry: `io.github.rcsb/rcsb-mcp`](https://registry.modelcontextprotocol.io/)
- [`Augmented-Nature/PDB-MCP-Server`](https://github.com/Augmented-Nature/PDB-MCP-Server)
- [mcpservers.org listing](https://mcpservers.org/servers/Augmented-Nature/PDB-MCP-Server)
- [`QuentinCody/rcsb-pdb-mcp-server`](https://github.com/QuentinCody/rcsb-pdb-mcp-server)
- [`cyanheads/protein-mcp-server`](https://github.com/cyanheads/protein-mcp-server)
- [MCP Registry: `io.github.cyanheads/protein-mcp-server`](https://registry.modelcontextprotocol.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pdb&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpdb.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
