---
title: Neurosift Tools MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Flatiron Institute
availability: Beta
tool_categories: [Neuroscience]
last_verified: 2026-05-20
summary: MCP server that lets Claude search DANDI/OpenNeuro and introspect NWB neurophysiology files, plus semantic search over PyNWB docs.
---

# Neurosift Tools MCP

MCP server for discovering, inspecting, and writing analyses against NWB-format neurophysiology data on DANDI and OpenNeuro.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | Jeremy Magland / [Flatiron Institute](https://github.com/magland/neurosift-mcps) |
| **Availability** | Beta — active through November 2025 |
| **Pricing** | Free / OSS — parent project is Apache-2.0; this repo's license field is unset (verify before redistributing) |
| **Capabilities** | Read-only |

## How to install

```
git clone https://github.com/magland/neurosift-mcps
cd neurosift-mcps/neurosift-tools
npm install
npm run build
```

Register with Claude Code (replace `/path/to/neurosift-tools` with the absolute path — e.g., `$(pwd)` if you're still inside `neurosift-mcps/neurosift-tools` from the previous step):

```
claude mcp add --transport stdio neurosift-tools -- node /path/to/neurosift-tools/build/index.js
```

## What it does

- `dandi_search`, `dandi_semantic_search`, `dandiset_info`, `dandiset_assets` — DANDI discovery and inspection
- `openneuro_search` — OpenNeuro discovery
- `nwb_file_info` — NWB neurodata-object introspection (without downloading the file)
- `dandi_list_neurodata_types`, `dandi_search_by_neurodata_type`
- `pynwb_docs_semantic_search` — ground PyNWB code generation in current docs

**Primary use cases**: Discover NWB datasets on DANDI / OpenNeuro, inspect NWB neurodata objects before downloading, ground PyNWB code generation in current documentation.

## Notes

stdio transport, no auth — uses public DANDI and OpenNeuro APIs.

## Sources

- [Install docs in Neurosift repo](https://github.com/flatironinstitute/neurosift/blob/main/docs/mcp-neurosift-tools.md)
- [`magland/neurosift-mcps`](https://github.com/magland/neurosift-mcps)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=neurosift&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fneurosift.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
