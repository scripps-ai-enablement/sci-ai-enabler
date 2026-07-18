---
title: ENCODE Toolkit
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: ammawla
availability: Beta
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-07-18
summary: "MCP server + Claude Code plugin for the ENCODE Project: search/download functional-genomics data and run ChIP/ATAC/RNA-seq/Hi-C/WGBS/CUT&RUN pipelines."
---

# ENCODE Toolkit

A Claude Code plugin (and standalone MCP server) that searches, downloads, and analyzes ENCODE Project functional-genomics data, bundling 20 MCP tools with seven reference analysis pipelines.

| | |
|---|---|
| **Type** | Claude Code Plugin (bundles an MCP server + workflow skills) |
| **Supplier** | [ammawla](https://github.com/ammawla/encode-toolkit) |
| **Availability** | Beta — PyPI v0.3.0 (2026-03-21) |
| **Pricing** | Free / OSS (AGPL-3.0-only) |
| **Capabilities** | Read/Write — read-only ENCODE API queries; writes downloaded files and local experiment-tracking records to disk |

## How to install

The plugin path installs the MCP server **and** the 47 workflow skills + 7 pipelines. The MCP-only path installs just the 20 tools.

- **Prerequisite** — [`uv`](https://docs.astral.sh/uv/) (provides `uvx`) or Python with `pip`, plus Claude Code. `uvx` fetches and runs `encode-toolkit` on demand, so no separate install step is required for the MCP-only path.

- **Claude Code — plugin marketplace (recommended; includes skills + pipelines):**
  ```
  /plugin marketplace add ammawla/encode-toolkit
  /plugin install encode-toolkit
  ```
  (Plugin-shipped skills resolve as `/encode-toolkit:<skill>`, not bare `/<skill>`.)

- **Claude Code — MCP server only (20 tools, no skills):**
  ```
  claude mcp add encode -- uvx encode-toolkit
  ```
  Claude Code launches `uvx encode-toolkit` itself over stdio — do not run it separately.

- **Claude Desktop** — add to `claude_desktop_config.json` (Claude Desktop has no plugin-marketplace path, so this gives the MCP tools only):
  ```json
  {
    "mcpServers": {
      "encode": {
        "command": "uvx",
        "args": ["encode-toolkit"]
      }
    }
  }
  ```
  (If `uvx` is not on Claude Desktop's PATH, install the package first with `pip install encode-toolkit` and set `"command": "encode-toolkit"` with `"args": []`.)

## What it does

Twenty MCP tools front the live ENCODE Portal REST API — including `encode_search_experiments` (20+ filters), `encode_get_experiment`, `encode_list_files` / `encode_search_files`, `encode_get_metadata` / `encode_get_facets` (valid filter values and live availability counts), `encode_download_files` (with MD5 verification), `encode_batch_download` (search + download in one call), and `encode_track_experiment` (local tracking with linked publications), plus tools for compatibility and provenance analysis.

The plugin also ships seven reference analysis pipelines, each with staged reference files and a Nextflow DSL2 workflow:

- **ChIP-seq** (BWA-MEM, MACS2 + IDR)
- **ATAC-seq** (Bowtie2, MACS2 with Tn5 adjustment)
- **RNA-seq** (STAR, RSEM + Kallisto)
- **WGBS** methylation (Bismark, MethylDackel)
- **Hi-C** (BWA, Juicer + HiCCUPS)
- **DNase-seq** (BWA, Hotspot2)
- **CUT&RUN** (Bowtie2, SEACR)

**Primary use cases**: querying and bulk-downloading ENCODE functional-genomics data, scaffolding ChIP/ATAC/RNA-seq/Hi-C/WGBS/CUT&RUN analyses, annotating regions with regulatory tracks.

## Notes

Community project, not ENCODE- or vendor-affiliated. Most ENCODE data is public and needs **no API key**; restricted-data credentials, when used, are stored in the OS keyring. The package advertises integration with 14 databases (ENCODE plus GTEx, ClinVar, GWAS Catalog, JASPAR, CellxGene, gnomAD, Ensembl, UCSC, GEO, PubMed, bioRxiv, and others), but the 20 live MCP tools target the ENCODE Portal; the other sources appear in the bundled pipeline/skill references. **Licensed AGPL-3.0** — network use of a modified version triggers the AGPL source-availability obligation; review before deploying a modified copy as a service. This entry is distinct from the read-only ENCODE REST-API Claude Skill catalogued at [ENCODE (Claude Skill)](encode-database.html): this toolkit adds download management, local tracking, and executable pipelines.

## Sources

- [`ammawla/encode-toolkit`](https://github.com/ammawla/encode-toolkit)
- [`ammawla/encode-toolkit` README](https://github.com/ammawla/encode-toolkit/blob/main/README.md)
- [`encode-toolkit` on PyPI](https://pypi.org/project/encode-toolkit/)
- [ENCODE Project](https://www.encodeproject.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=encode-toolkit&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fencode-toolkit.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
