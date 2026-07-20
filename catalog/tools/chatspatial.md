---
title: ChatSpatial
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Chen Yang (cafferychen777)
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-27
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches cafferychen777/ChatSpatial, PyPI chatspatial 1.2.10 present, MIT, active (pushed 2026-07-16), no GitHub advisories"
summary: "MCP server for spatial transcriptomics — preprocessing, spatial domains, deconvolution, cell-cell communication, and SVG detection via Scanpy/Squidpy."
---

# ChatSpatial

An MCP server that drives end-to-end spatial transcriptomics analysis through natural language, wrapping Scanpy, Squidpy, and 60+ spatial methods.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [cafferychen777/ChatSpatial](https://github.com/cafferychen777/ChatSpatial) |
| **Availability** | GA — v1.2.10 |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — reads/writes `.h5ad` AnnData files on local disk and produces figures/result tables |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches cafferychen777, PyPI chatspatial 1.2.10, MIT, no advisories |

## How to install

ChatSpatial runs as a local stdio MCP server. Install the PyPI package into a virtualenv first, then register it.

- **Claude Code** — pip-based:
  ```
  python -m venv venv
  source venv/bin/activate
  pip install chatspatial
  which python   # note the absolute path printed
  claude mcp add chatspatial /path/to/venv/bin/python -- -m chatspatial server
  ```
  (replace `/path/to/venv/bin/python` with the absolute path that `which python` printed — e.g. `/Users/you/ChatSpatial/venv/bin/python`, or `$(pwd)/venv/bin/python` if you are still in the project dir.)
- **Claude Desktop** — pip-based, in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "chatspatial": {
        "command": "/path/to/venv/bin/python",
        "args": ["-m", "chatspatial", "server"]
      }
    }
  }
  ```
  Fully quit and relaunch Claude Desktop after editing the config (it is not hot-reloaded). The `pip install chatspatial` step above is still required before this works.
- **Claude Desktop / Claude Code** — Docker (no local Python env):
  ```json
  {
    "mcpServers": {
      "chatspatial": {
        "command": "docker",
        "args": [
          "run", "--rm", "-i",
          "-v", "/absolute/path/to/your/data:/data:ro",
          "-v", "/absolute/path/to/outputs:/outputs",
          "ghcr.io/cafferychen777/chatspatial:v1.2.10",
          "server", "--transport", "stdio"
        ]
      }
    }
  }
  ```
  Pull the image first with `docker pull ghcr.io/cafferychen777/chatspatial:v1.2.10`. Reference container paths (e.g. `/data/sample.h5ad`) in prompts, and use `--rm -i` (not `-it`) for MCP stdio. Replace the two `/absolute/path/to/…` mounts with your real input/output directories.

This is a long-lived stdio server launched by Claude itself — you do not run `chatspatial server` in a separate terminal; the registration above starts it on demand.

## What it does

Exposes 20 schema-validated tools orchestrating ~65 spatial transcriptomics methods across 15 analytical categories: data loading and preprocessing, visualization, spatial domain identification, deconvolution, cell-cell communication, cell-type annotation, differential expression, trajectory inference, RNA velocity, spatial statistics, enrichment analysis, spatially variable gene (SVG) detection, multi-sample integration, CNV analysis, and spatial registration. Operates on AnnData (`.h5ad`) inputs.

**Primary use cases**: spatial transcriptomics preprocessing and QC, spatial domain identification, cell-cell communication analysis, spatially variable gene detection.

## Notes

No API key required. Built on the scverse stack (Scanpy/Squidpy) plus additional spatial methods. Works with any MCP-compatible client (Claude Desktop, Claude Code, Codex). For non-spatial single-cell workflows see `scanpy.md` and the `single-cell-rna-qc` / `scvi-tools` plugins.

## Sources

- [`cafferychen777/ChatSpatial`](https://github.com/cafferychen777/ChatSpatial)
- [ChatSpatial configuration guide](https://github.com/cafferychen777/ChatSpatial/blob/main/docs/advanced/configuration.md)
- [ChatSpatial documentation](https://docs.cafferyang.com/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=chatspatial&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fchatspatial.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
