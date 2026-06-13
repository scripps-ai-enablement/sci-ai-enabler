---
title: decoupler-MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: scmcphub
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-06-13
summary: MCP server wrapping decoupler so Claude can infer pathway and transcription-factor activities from expression data in natural language.
---

# decoupler-MCP

MCP server that exposes the Python decoupler footprint-analysis workflow as natural-language tools — infer pathway activities (PROGENy) and transcription-factor activities (CollecTRI) from single-cell or bulk expression.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [scmcphub](https://github.com/scmcphub/decoupler-mcp) |
| **Availability** | GA — v0.4.0 (2025-06-27) |
| **Pricing** | Free / OSS — BSD-3-Clause (per the scmcphub ecosystem; per-repo LICENSE file not separately confirmed) |
| **Capabilities** | Read/Write — runs inference on a loaded AnnData object |

## How to install

Install the package first (required before any registration snippet below works):

```
pip install decoupler-mcp
```

- **Claude Code** — stdio (recommended; Claude Code launches the process itself, so do **not** run `decoupler-mcp run` separately):
  ```
  claude mcp add --transport stdio decoupler -- decoupler-mcp run
  ```
- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "decoupler": { "command": "decoupler-mcp", "args": ["run"] }
    }
  }
  ```
- **HTTP transport** (long-lived service — keep it running in its own terminal; not needed for the stdio setups above):
  ```
  decoupler-mcp run --transport shttp --port 8000
  ```

To verify the install before registering, run `decoupler-mcp run` once and Ctrl-C after it boots — for stdio the host launches it for you.

## What it does

- `pathway_activity` — infer pathway activities using PROGENy with the MLM (multivariate linear model) method
- `tf_activity` — infer transcription-factor activities using CollecTRI with the ULM (univariate linear model) method

**Primary use cases**: Pathway-activity scoring per cell/sample, transcription-factor activity inference, functional interpretation of differential expression.

## Notes

Built on [decoupler](https://decoupler.readthedocs.io/). Part of the scmcphub single-cell ecosystem alongside `scanpy-mcp`, `cellrank-mcp`, and `liana-mcp` — typically run together on a shared AnnData object.

## Sources

- [`scmcphub/decoupler-mcp`](https://github.com/scmcphub/decoupler-mcp)
- [scmcphub documentation — decoupler-mcp](https://docs.scmcphub.org/servers/decoupler-mcp)
- [decoupler documentation](https://decoupler.readthedocs.io/en/latest/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=decoupler-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdecoupler-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
