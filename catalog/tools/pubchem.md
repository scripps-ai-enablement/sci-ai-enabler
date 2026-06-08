---
title: PubChem MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: JackKuo666
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-06-08
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
- **Hosted HTTP alternative (cyanheads, no local install)** — a public Streamable HTTP instance of the TypeScript `@cyanheads/pubchem-mcp-server` is published at `https://pubchem.caseyjhand.com/mcp`. Claude Code:
  ```
  claude mcp add --transport http pubchem https://pubchem.caseyjhand.com/mcp
  ```
  Claude Desktop has no native HTTP transport — proxy it via `mcp-remote` in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "pubchem": { "command": "npx", "args": ["-y", "mcp-remote", "https://pubchem.caseyjhand.com/mcp"] }
    }
  }
  ```
  To run the cyanheads server locally instead (requires Bun ≥ 1.3 or Node ≥ 24), register the stdio package — Claude Code launches it itself, no separate terminal needed:
  ```
  claude mcp add --transport stdio pubchem -- bunx @cyanheads/pubchem-mcp-server@latest
  ```

## What it does

- `search_pubchem_by_name`
- `search_pubchem_by_smiles`
- `get_pubchem_compound_by_cid`
- `search_pubchem_advanced` (formula / property filters)

**Primary use cases**: Look up compounds by name / SMILES / CID / formula, retrieve PubChem property records, generate structure files for downstream cheminformatics.

## Notes

stdio transport. Backed by FastMCP. No authentication required. PubChem's broad compound coverage makes this a natural pair with the ChEMBL bioactivity connector bundled in `bio-research`.

The cyanheads alternative (HTTP/stdio paths above) exposes a wider, read-only surface — 8 tools following a `pubchem_verb_noun` naming pattern, including substructure / superstructure / 2D-similarity search and GHS hazard classification (`pubchem_get_compound_safety`: signal word, pictograms, H-/P-codes) — and rate-limits PUG REST/View calls to 5 req/s with retry. Prefer it when you need safety data or structure-search modes; prefer the JackKuo666 server for a pure-Python stdio install.

## Sources

- [`JackKuo666/PubChem-MCP-Server`](https://github.com/JackKuo666/PubChem-MCP-Server)
- [Alternative TypeScript implementation `cyanheads/pubchem-mcp-server`](https://github.com/cyanheads/pubchem-mcp-server) ([npm](https://www.npmjs.com/package/@cyanheads/pubchem-mcp-server); hosted instance `https://pubchem.caseyjhand.com/mcp`)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pubchem&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpubchem.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
