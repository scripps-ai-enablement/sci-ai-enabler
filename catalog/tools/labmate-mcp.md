---
title: LabMate MCP
parent: All tools
grand_parent: Catalog
nav_order: 1
tool_type: MCP server
supplier: Jonas Rackl
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-07-18
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "PyPI labmate-mcp 7.3.1 MIT + GitHub JonasRackl/labmate-mcp MIT resolve (author matches supplier), no OSV advisories, but single-maintainer (2 stars) and a few tools call free third-party APIs via labmate-mcp --setup"
summary: One-install cheminformatics MCP with 81 tools — retrosynthesis, forward/ADMET/pKa/NMR prediction, 202 named reactions, reagent calculators, compound and literature lookup.
---

# LabMate MCP

A single MCP server that gives Claude a chemistry-focused research workbench — retrosynthesis and reaction prediction, ADMET/pKa/NMR estimation, a library of 202 named reactions, reagent-mass calculators, and compound/literature lookup.

| | |
|---|---|
| **Type** | MCP server (stdio) |
| **Supplier** | [Jonas Rackl](https://github.com/JonasRackl/labmate-mcp) |
| **Availability** | GA — PyPI `labmate-mcp` v7.3.1 (released 2026-02-02) |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read-only — computation, prediction, and database lookup; no lab-instrument writes |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — PyPI labmate-mcp 7.3.1 MIT + GitHub MIT resolve, no OSV advisories, single-maintainer (2 stars) + optional free third-party API keys |

## How to install

1. **Install the package** (Python ≥ 3.10):
   ```
   pip install labmate-mcp
   ```
2. **(Optional) Configure free API keys** — 61 of 81 tools work with no keys. Retrosynthesis, pKa prediction, and NMR-shift tools need free keys; add them once with:
   ```
   labmate-mcp --setup
   ```
3. **Register the server:**
   - **Claude Code** — direct stdio add:
     ```
     claude mcp add --transport stdio labmate -- labmate-mcp
     ```
     (Equivalently, add a `"labmate"` entry with `"command": "labmate-mcp"` under `mcpServers` in your project `.mcp.json`.) The `labmate-mcp` binary is installed by the `pip install` in step 1; Claude Code launches it over stdio, so there is no long-running process to keep open. Run `/mcp` to confirm it connected.
   - **Claude Desktop** — add to `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`; Windows: `%APPDATA%\Claude\claude_desktop_config.json`), then restart Claude Desktop:
     ```json
     {
       "mcpServers": {
         "labmate": {
           "command": "labmate-mcp"
         }
       }
     }
     ```

## What it does

81 MCP tools grouped into five areas:

- **Synthesis (11 tools)** — retrosynthesis, forward-reaction prediction, pKa, ADMET, NMR-shift prediction
- **Bench (30 tools)** — 202 named reactions (Aldol, Appel, Baeyer-Villiger, Birch, Brown hydroboration, …), protecting-group and solvent references, reagent/limiting-reagent mass calculators
- **Analysis (15 tools)** — isotope patterns, simulated mass spectra, binding data, crystal-structure lookup
- **Literature (15 tools)** — multi-database paper search ranked by citations, abstracts, author profiles, open-access PDFs
- **Publication (10 tools)** — citation formatting, manuscript templates, journal guides, SI checklists

**Primary use cases**: Retrosynthetic planning and reaction lookup, ADMET/pKa/NMR property estimation, reagent stoichiometry calculations, compound/literature research.

## Notes

stdio server — Claude Code / Claude Desktop launch the `labmate-mcp` process themselves; nothing needs to stay running in a separate terminal. Most tools (61/81) require no API keys; the retrosynthesis, pKa, and NMR-prediction tools rely on free third-party APIs configured via `labmate-mcp --setup`. The literature and publication tool groups overlap dedicated catalog entries (PubMed, OpenAlex, scientific-writing); LabMate bundles them for a single-install chemistry workflow.

## Sources

- [`JonasRackl/labmate-mcp`](https://github.com/JonasRackl/labmate-mcp)
- [labmate-mcp on PyPI](https://pypi.org/project/labmate-mcp/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=labmate-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Flabmate-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
