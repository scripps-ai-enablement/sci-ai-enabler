---
title: CellRank-MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: scmcphub
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-13
summary: MCP server wrapping CellRank so Claude can model cell fate and trajectories from single-cell data in natural language.
---

# CellRank-MCP

MCP server that exposes the CellRank cell-fate workflow as natural-language tools — build kernels, fit a GPCCA estimator, predict initial/terminal states, and compute fate probabilities.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [scmcphub](https://github.com/scmcphub/cellrank-mcp) |
| **Availability** | GA — v0.4.0 (2025-06-27) |
| **Pricing** | Free / OSS — BSD-3-Clause (per the scmcphub ecosystem; per-repo LICENSE file not separately confirmed) |
| **Capabilities** | Read/Write — runs analysis on a loaded AnnData object and writes plots |

## How to install

Install the package first (required before any registration snippet below works):

```
pip install cellrank-mcp
```

- **Claude Code** — stdio (recommended; Claude Code launches the process itself, so do **not** run `cellrank-mcp run` separately):
  ```
  claude mcp add --transport stdio cellrank -- cellrank-mcp run
  ```
- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "cellrank": { "command": "cellrank-mcp", "args": ["run"] }
    }
  }
  ```
- **HTTP transport** (long-lived service — keep it running in its own terminal; not needed for the stdio setups above):
  ```
  cellrank-mcp run --transport shttp --port 8000
  ```

To verify the install before registering, run `cellrank-mcp run` once and Ctrl-C after it boots — for stdio the host launches it for you.

## What it does

- `create_kernel` / `compute_transition_matrix` — build a kernel and its cell-to-cell transition matrix
- `create_and_fit_gpcca` — fit the GPCCA estimator
- `predict_terminal_states` / `predict_initial_states` — identify macrostates
- `compute_fate_probabilities` — per-cell fate probabilities toward terminal states
- `kernel_projection` / `circular_projection` — trajectory visualizations

**Primary use cases**: Cell-fate and trajectory modeling, terminal/initial state discovery, fate-probability mapping for developmental single-cell data.

## Notes

Built on [CellRank](https://cellrank.readthedocs.io/). Part of the scmcphub single-cell ecosystem alongside `scanpy-mcp`, `liana-mcp`, and `decoupler-mcp` — typically run together on a shared AnnData object. RNA-velocity kernels require velocity estimates (e.g., from scVelo) precomputed on the object.

## Sources

- [`scmcphub/cellrank-mcp`](https://github.com/scmcphub/cellrank-mcp)
- [scmcphub documentation — cellrank-mcp](https://docs.scmcphub.org/servers/cellrank-mcp)
- [CellRank documentation](https://cellrank.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cellrank-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcellrank-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
