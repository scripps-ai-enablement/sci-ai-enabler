---
title: ADMETlab MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: ToxMCP (community)
availability: Beta
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-07-26
summary: Self-hostable MCP server wrapping the ADMETlab 3.0 API for molecule washing, SVG rendering, ADMET property prediction, and CSV retrieval.
---

# ADMETlab MCP Server

A self-hostable MCP server that fronts the ADMETlab 3.0 web API so Claude can wash structures, render them, and predict ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) properties in a drug-discovery workflow.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [ToxMCP](https://github.com/ToxMCP/admetlab-mcp) (community) |
| **Availability** | Beta — install-from-source, part of the ToxMCP suite |
| **Pricing** | Free / OSS (Apache-2.0); backed by the public ADMETlab 3.0 API |
| **Capabilities** | Read-only — submits SMILES to ADMETlab and returns predictions/renderings |

## How to install

This is a **long-lived HTTP MCP server** — it does not run over stdio. You must start it in its own terminal and leave it running; Claude connects to it over HTTP. It is not on PyPI, so install from a clone.

- **Prerequisite** — Python 3.10+ and Claude Code / Claude Desktop.

- **Clone, install, and start the server (keep this terminal open):**
  ```
  git clone https://github.com/ToxMCP/admetlab-mcp
  cd admetlab-mcp
  python -m venv .venv
  source .venv/bin/activate
  pip install -e ".[dev]"
  cp .env.example .env
  uvicorn admetlab_mcp.transport.http:app --host 127.0.0.1 --port 8200
  ```
  The MCP endpoint is then `http://127.0.0.1:8200/mcp` (health check at `http://127.0.0.1:8200/health`). Leave this process running while you use the tool.

- **Claude Code** — register the running HTTP endpoint (in a second terminal):
  ```
  claude mcp add --transport http admetlab http://127.0.0.1:8200/mcp
  ```

- **Claude Desktop** — Claude Desktop has no native HTTP transport, so proxy the HTTP endpoint through `mcp-remote` in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "admetlab": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "http://127.0.0.1:8200/mcp"]
      }
    }
  }
  ```
  (Requires Node.js for `npx`; the `uvicorn` server above must already be running.)

## What it does

Exposes four tools that front the ADMETlab 3.0 API:

- `wash_molecule` — standardize/clean an input molecule (POST `/api/washmol`).
- `render_molecule_svg` — render a structure to SVG (POST `/api/molsvg`).
- `predict_admet` — run ADMET property prediction for a molecule (POST `/api/single/admet`, with a documented fallback to `/api/admet`).
- `fetch_admet_csv` — retrieve prediction results as CSV by task ID (POST `/api/admetCSV`).

Batching is supported (up to ~1000 SMILES per prediction call) with rate limiting (≤5 rps), retries/backoff, and fallback endpoints.

**Primary use cases**: ADMET property prediction, compound triage during lead optimization, structure washing and rendering for drug-discovery pipelines.

## Notes

No API key is required (an optional placeholder for future authentication is included). Predictions depend on the upstream ADMETlab 3.0 service, which the project notes can be unstable — expect occasional 5xx/404 responses passed through from upstream. Because this is an HTTP/SSE server, it must be kept running in a separate terminal; this is the most common cause of "the tool doesn't show up" for HTTP MCP servers.

For a zero-install, enterprise-hosted ADMET path in Claude.ai, see the [Inductive Bio ADMET Connector](inductive-bio.html); for broader cheminformatics property modeling see [PyTDC](pytdc.html) and [DeepChem](deepchem.html).

## Sources

- [`ToxMCP/admetlab-mcp`](https://github.com/ToxMCP/admetlab-mcp)
- [ToxMCP suite](https://github.com/ToxMCP/toxmcp)
- [ADMETlab 3.0](https://admetlab3.scbdd.com/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=admetlab-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fadmetlab-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
