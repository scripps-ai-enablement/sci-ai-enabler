---
title: OpenNeuro MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Quentin Cody (community)
availability: Beta
tool_categories: [Neuroscience]
last_verified: 2026-05-29
summary: Community MCP server giving Claude GraphQL access to the OpenNeuro archive of MRI, MEG, EEG, iEEG, and ECoG datasets.
---

# OpenNeuro MCP

Community MCP server wrapping the OpenNeuro GraphQL API for dataset, snapshot, and file-listing queries over the public archive of MRI, MEG, EEG, iEEG, and ECoG data.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Quentin Cody](https://github.com/QuentinCody/open-neuro-mcp-server) (community; **not officially endorsed by OpenNeuro / Stanford**) |
| **Availability** | Beta — hosted Cloudflare Workers deployment at `open-neuro-mcp-server.quentincody.workers.dev` |
| **Pricing** | Free / OSS — MIT License with an Academic Citation Requirement (see upstream `LICENSE.md` / `CITATION.md`) |
| **Capabilities** | Read-only — public OpenNeuro data, no auth |

## How to install

- **Claude Desktop** — Settings → Developer → Edit Config, add the following to `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "openneuro": {
        "command": "npx",
        "args": ["mcp-remote", "https://open-neuro-mcp-server.quentincody.workers.dev/sse"]
      }
    }
  }
  ```

  Restart Claude Desktop. (Claude Desktop has no native HTTP/SSE transport — the `mcp-remote` proxy is required.)

- **Claude Code** — add the hosted endpoint directly (Claude Code speaks SSE/HTTP natively):

  ```
  claude mcp add --transport sse openneuro https://open-neuro-mcp-server.quentincody.workers.dev/sse
  ```

- **Self-host (optional)** — clone, deploy your own Cloudflare Worker, then point either client at `http://localhost:8787/sse` or your own `*.workers.dev/sse` URL:

  ```
  git clone https://github.com/QuentinCody/open-neuro-mcp-server
  cd open-neuro-mcp-server
  npm install
  npm run dev   # local on http://localhost:8787
  # or: npm run deploy   # deploy to your own Cloudflare Workers account
  ```

## What it does

- `openneuro_graphql_query` — execute arbitrary GraphQL queries against the OpenNeuro API
- Schema introspection — discover available fields and operations
- Dataset / snapshot / file-listing access over the OpenNeuro archive

**Primary use cases**: Search OpenNeuro for MRI / MEG / EEG / iEEG / ECoG datasets matching a task or modality, inspect dataset snapshots and file manifests before download, ground analysis-pipeline planning in the actual contents of public neuroimaging datasets.

## Notes

SSE transport; no authentication required for the public GraphQL endpoint. Complements the Neurosift Tools MCP (which covers DANDI + NWB) — OpenNeuro and DANDI are separate archives, so installing both gives a single Claude session reach across the major open neuroscience-data repositories.

Citation requirement: academic use must cite per upstream `CITATION.md`.

## Sources

- [`QuentinCody/open-neuro-mcp-server`](https://github.com/QuentinCody/open-neuro-mcp-server)
- [OpenNeuro](https://openneuro.org/)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=openneuro&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fopenneuro.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
