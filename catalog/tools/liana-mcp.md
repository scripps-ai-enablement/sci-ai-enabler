---
title: LIANA-MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: scmcphub
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-06-13
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "provenance matches scmcphub, PyPI liana-mcp v0.4.0 present, no OSV advisories, but no repo LICENSE file and ecosystem unmaintained since 2025-06"
summary: MCP server wrapping LIANA so Claude can infer and plot cell-cell communication from single-cell data in natural language.
---

# LIANA-MCP

MCP server that exposes the Python LIANA cell-cell communication workflow as natural-language tools — run multiple ligand-receptor methods, aggregate their ranks, and plot the results.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [scmcphub](https://github.com/scmcphub/liana-mcp) |
| **Availability** | GA — v0.4.0 (2025-06-27) |
| **Pricing** | Free / OSS — BSD-3-Clause (per the scmcphub ecosystem; per-repo LICENSE file not separately confirmed) |
| **Capabilities** | Read/Write — runs analysis on a loaded AnnData object and writes plots |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — provenance matches scmcphub, no OSV advisories, no repo LICENSE and unmaintained since 2025-06 |

## How to install

Install the package first (required before any registration snippet below works):

```
pip install liana-mcp
```

- **Claude Code** — stdio (recommended; Claude Code launches the process itself, so do **not** run `liana-mcp run` separately):
  ```
  claude mcp add --transport stdio liana -- liana-mcp run
  ```
- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "liana": { "command": "liana-mcp", "args": ["run"] }
    }
  }
  ```
- **HTTP transport** (long-lived service — keep it running in its own terminal; not needed for the stdio setups above):
  ```
  liana-mcp run --transport shttp --port 8000
  ```

To verify the install before registering, run `liana-mcp run` once and Ctrl-C after it boots — for stdio use the host launches it for you.

## What it does

- `ls_ccc_method` — list available cell-cell communication methods
- `communicate` — run ligand-receptor inference (CellPhoneDB, CellChat, Connectome, NATMI, …)
- `rank_aggregate` — aggregate ligand-receptor scores across methods
- `circle_plot` — circular network visualization
- `ccc_dotplot` — dotplot of communication events

**Primary use cases**: Natural-language cell-cell communication inference, multi-method ligand-receptor ranking, communication-network plotting.

## Notes

Built on [liana-py](https://liana-py.readthedocs.io/). Part of the scmcphub single-cell ecosystem alongside `scanpy-mcp`, `cellrank-mcp`, and `decoupler-mcp` — typically run together on a shared AnnData object. For an R-based alternative to ligand-receptor inference, see the CellChat skill.

## Sources

- [`scmcphub/liana-mcp`](https://github.com/scmcphub/liana-mcp)
- [scmcphub documentation — liana-mcp](https://docs.scmcphub.org/servers/liana-mcp)
- [LIANA (liana-py) documentation](https://liana-py.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=liana-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fliana-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
