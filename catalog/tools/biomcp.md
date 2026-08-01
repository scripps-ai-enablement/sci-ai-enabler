---
title: BioMCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: GenomOncology
availability: GA
tool_categories: [All]
last_verified: 2026-08-01
verification: degraded
verified_on: 2026-07-20
verification_note: "launch command was biomcp run (not a real subcommand) — corrected to canonical biomcp serve, verified against the biomcp.org MCP-server reference; biomcp mcp is the docs' legacy alias"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches GenomOncology, PyPI biomcp-cli v0.8.25 and biomcp-python v0.7.3 present, MIT, no OSV advisories"
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
| **Verified** | degraded · 2026-07-20 — launch command corrected from `biomcp run` to `biomcp serve` |
| **Security** | cleared · 2026-07-20 — provenance matches GenomOncology, MIT, no OSV advisories |

- **Claude Code** — install the CLI, then register the server:
  ```
  uv tool install biomcp-cli
  claude mcp add --transport stdio biomcp -- biomcp serve
  ```
  (If you prefer not to install the CLI globally, swap the second command for `claude mcp add --transport stdio biomcp -- uv run --with biomcp-python biomcp serve`.)
- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "biomcp": { "command": "biomcp", "args": ["serve"] }
    }
  }
  ```
  Or, to avoid a global install, use `{ "command": "uv", "args": ["run", "--with", "biomcp-python", "biomcp", "serve"] }`.

## What it does

About 21 tools including `trial_searcher`, `trial_getter`, PubMed search, MyVariant.info variant lookup, OpenFDA adverse-event queries.

**Primary use cases**: Clinical trial discovery, variant lookup, drug adverse-event review, biomedical Q&A for agents.

## Notes

stdio transport. Supports both ClinicalTrials.gov default and NCI CTS source. Ships an agent skill via `biomcp skill install`.

## Sources

- [biomcp.org](https://biomcp.org/)
- [mcpservers.org listing](https://mcpservers.org/servers/genomoncology/biomcp)
- [ClinicalTrials.gov source page](https://biomcp.org/sources/clinicaltrials-gov/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=biomcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbiomcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
