---
title: BioMCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: GenomOncology
availability: GA
tool_categories: [All]
last_verified: 2026-05-19
summary: Unified biomedical lookup across PubMed, ClinicalTrials.gov, MyVariant, and OpenFDA.
---

# BioMCP

Unified MCP access to ClinicalTrials.gov, PubMed, MyVariant.info, OpenFDA, NCI CTS, and related biomedical sources.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [GenomOncology](https://biomcp.org/) |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT); optional API keys (NCBI, OpenFDA, NCI CTS, OncoKB, AlphaGenome) raise rate limits or unlock private sources |
| **Capabilities** | Read-only |

- **Claude Code** — install the CLI, then register the server:
  ```
  uv tool install biomcp-cli
  claude mcp add --transport stdio biomcp -- biomcp run
  ```
  (If you prefer not to install the CLI globally, swap the second command for `claude mcp add --transport stdio biomcp -- uv run --with biomcp-python biomcp run`.)
- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "biomcp": { "command": "biomcp", "args": ["run"] }
    }
  }
  ```
  Or, to avoid a global install, use `{ "command": "uv", "args": ["run", "--with", "biomcp-python", "biomcp", "run"] }`.

## What it does

About 21 tools including `trial_searcher`, `trial_getter`, PubMed search, MyVariant.info variant lookup, OpenFDA adverse-event queries.

**Primary use cases**: Clinical trial discovery, variant lookup, drug adverse-event review, biomedical Q&A for agents.

## Notes

stdio transport. Supports both ClinicalTrials.gov default and NCI CTS source. Ships an agent skill via `biomcp skill install`.

## Sources

- [biomcp.org](https://biomcp.org/)
- [mcpservers.org listing](https://mcpservers.org/servers/genomoncology/biomcp)
- [ClinicalTrials.gov source page](https://biomcp.org/sources/clinicaltrials-gov/)
