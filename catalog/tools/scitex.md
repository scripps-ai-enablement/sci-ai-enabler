---
title: SciTeX Dataset MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: SciTeX
availability: Beta
tool_categories: [Neuroscience]
last_verified: 2026-06-28
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "PyPI scitex 2.30.8 AGPL-3.0-only resolves (author scitex.ai matches supplier SciTeX), no OSV advisories, but single-maintainer and strong AGPL copyleft to weigh for reuse"
summary: MCP server giving Claude a unified search across OpenNeuro, DANDI, PhysioNet, and Zenodo for BIDS/NWB neuroscience datasets.
---

# SciTeX Dataset MCP

MCP server that lets Claude discover and search neuroscience datasets across OpenNeuro, DANDI, PhysioNet, and Zenodo through one unified BIDS/NWB-aware interface.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [SciTeX](https://pypi.org/project/scitex/) |
| **Availability** | Beta (v2.30.2, released 2026-06-20) |
| **Pricing** | Free / OSS — AGPL-3.0-only |
| **Capabilities** | Read-only — queries public dataset-repository APIs |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — PyPI scitex 2.30.8 AGPL-3.0-only resolves, provenance matches, no OSV advisories, single-maintainer + AGPL copyleft |

## How to install

The dataset/neuroscience tools ship inside the broader `scitex` package; the `scitex mcp start` console script exposes them over MCP.

- **Install the package** (PyPI). The `[dataset]` extra pulls in the OpenNeuro / DANDI / PhysioNet / Zenodo fetchers; `[all]` installs everything:
  ```
  uv pip install "scitex[dataset]"
  ```
  (or `pip install "scitex[dataset]"`; requires Python 3.10+.)
- **Verify the server starts** (one-shot — Ctrl-C after it boots; Claude launches the process itself via stdio):
  ```
  scitex mcp start
  ```
- **Claude Code** — register the stdio server:
  ```
  claude mcp add --transport stdio scitex -- scitex mcp start
  ```
- **Claude Desktop** — add the equivalent stdio entry to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "scitex": { "command": "scitex", "args": ["mcp", "start"] }
    }
  }
  ```

## What it does

Exposes the `scitex.dataset` module's neuroscience fetchers as MCP tools so Claude can:

- Search and list datasets on **OpenNeuro**, **DANDI**, **PhysioNet**, and **Zenodo** through one API
- Run text queries over dataset metadata (e.g., "phase-amplitude coupling") across repositories
- Surface BIDS- and NWB-format dataset metadata for downstream analysis

**Primary use cases**: cross-archive neuroscience dataset discovery, BIDS/NWB metadata search, building reproducible dataset-fetch steps for analysis pipelines.

## Notes

Read-only against public repository APIs; no API key required for core dataset discovery (optional cloud integrations exist but are not needed). SciTeX is a 37-package scientific-computing ecosystem and the `scitex` console script bundles many non-neuroscience MCP tools alongside the dataset module — the neuroscience-relevant surface is the `dataset` extra. For inspecting individual NWB files and DANDI/OpenNeuro semantic search, see also [Neurosift Tools MCP]({{ '/catalog/tools/neurosift.html' | relative_url }}). The exact per-tool MCP names are not enumerated in the upstream docs — **Unverified —** the tool list above reflects the documented `scitex.dataset.neuroscience` Python API surface (`openneuro` / `dandi` / `physionet` / `zenodo` fetchers, `search_datasets`).

## Sources

- [`scitex` on PyPI](https://pypi.org/project/scitex/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=scitex&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fscitex.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
