---
title: UCSC Cell Browser MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: MCPmed
availability: Beta
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-15
summary: "Search the UCSC Cell Browser's public single-cell dataset collection by organism, tissue, disease or project, and pull per-dataset metadata."
---

# UCSC Cell Browser MCP

Find single-cell RNA-seq datasets in the [UCSC Cell Browser](https://cells.ucsc.edu/) by organism, body part, disease or project, and retrieve each dataset's metadata without leaving Claude.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [MCPmed](https://github.com/MCPmed/UCSCCBmcp) |
| **Availability** | Beta — `pyproject.toml` declares v1.0.0; last upstream commit 2025-07-28 |
| **Pricing** | Free / OSS — BSD-3-Clause (repository `LICENSE`); note the `pyproject.toml` `license` field says MIT, so the two disagree |
| **Capabilities** | Read-only — queries the public `cells.ucsc.edu` dataset index; no account, no API key |

## How to install

**The README's `pip install ucsc-cell-browser-mcp` does not work — that package is not published on PyPI (404 as of 2026-08-15).** Install from source instead.

1. **Clone and install** (the README's `cd ucsccbMCP` is a typo; the clone directory is `UCSCCBmcp`):
   ```
   git clone https://github.com/MCPmed/UCSCCBmcp
   cd UCSCCBmcp
   pip install -e .
   ```
   This installs the `ucsc-mcp` console command (entry point `ucsccbmcp.main:main_cli`). Python 3.8+ required.

2. **Find the absolute path** to the installed command — you need it for both clients below:
   ```
   which ucsc-mcp
   ```

3. **Claude Code** — register the stdio server:
   ```
   claude mcp add ucsc-cell-browser /path/to/ucsc-mcp
   ```
   (replace `/path/to/ucsc-mcp` with the absolute path that `which ucsc-mcp` printed — e.g. `/Users/you/.local/bin/ucsc-mcp`).

4. **Claude Desktop** — add to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "ucsc-cell-browser": {
         "command": "/path/to/ucsc-mcp"
       }
     }
   }
   ```
   Fully quit and relaunch Claude Desktop after editing.

This is a stdio server that Claude launches itself. Running `ucsc-mcp` in a terminal only verifies that it boots — press Ctrl-C afterwards and do **not** leave it running.

## What it does

Parses the UCSC Cell Browser's public dataset index (`https://cells.ucsc.edu/dataset.json`) and exposes it as queryable tools:

- `search_datasets` — keyword search across the collection
- `get_dataset_details` — full metadata for one dataset
- `list_organisms` — organisms represented
- `list_body_parts` — tissues / body parts represented
- `list_diseases` — disease annotations represented
- `list_projects` — parent projects / consortia
- `refresh_data` — re-pull the cached dataset index

**Primary use cases**: locating a public scRNA-seq dataset for a tissue or disease, scoping what single-cell data already exists before generating new data, assembling dataset shortlists for reanalysis.

## Notes

This is a discovery-and-metadata layer, not a data-access layer: it tells you which datasets exist and what they cover, but does not download expression matrices. Pair it with [cellxgene-census](cellxgene-census.html) or [NCBI GEO](geo-database.html) to fetch the underlying counts, and with [Scanpy](scanpy.html) to analyse them.

Dependencies are light (`httpx`, `mcp`). No API key or account is needed because the backing index is public.

The repository is small (1 star) and has not been updated since 2025-07-28; the license discrepancy between the `LICENSE` file (BSD-3-Clause) and `pyproject.toml` (MIT) is unresolved upstream. Both are permissive, but confirm with the maintainers before redistributing.

The server is one of the reference implementations described in the MCPmed paper (*Briefings in Bioinformatics*, 2026), alongside the already-catalogued [NCBI GEO](geo-database.html) and STRING servers from the same group.

## Sources

- [`MCPmed/UCSCCBmcp`](https://github.com/MCPmed/UCSCCBmcp)
- [UCSC Cell Browser](https://cells.ucsc.edu/)
- [MCPmed: a call for Model Context Protocol-enabled bioinformatics web services for LLM-driven discovery (*Brief Bioinform* 2026;27(1):bbag076)](https://academic.oup.com/bib/article/27/1/bbag076/8495038)
- [MCPmed hub](https://mcpmed.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=ucsc-cell-browser&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fucsc-cell-browser.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
