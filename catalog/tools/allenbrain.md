---
title: allenbrain-mcp
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: maflot (community)
availability: Alpha
tool_categories: [Neuroscience]
last_verified: 2026-05-20
summary: Community MCP wrapper exposing Allen Brain Atlas RMA queries, cell-types, mouse connectivity, ontologies, and image/grid downloads to Claude.
---

# allenbrain-mcp

Community MCP server wrapping the Allen Brain Atlas API — cell types, mouse connectivity experiments, brain-structure ontologies, atlas images, and 3D expression grids.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [maflot](https://github.com/maflot/allenbrain-mcp) (community; **not officially endorsed by the Allen Institute**) |
| **Availability** | Alpha — created February 2026, "work in progress" |
| **Pricing** | Free / OSS — no explicit license file in the repo; flag for legal review before redistributing |
| **Capabilities** | Read-only |

## How to install

```
git clone https://github.com/maflot/allenbrain-mcp
cd allenbrain-mcp
npm install
npm run build
npm start
```

Register with Claude Code (replace `/path/to/allenbrain-mcp` with the absolute path of the clone — e.g., `$(pwd)` if you're still inside the directory from the previous step):

```
claude mcp add --transport stdio allenbrain -- node /path/to/allenbrain-mcp/build/index.js
```

## What it does

- `execute_rma_query` — raw RMA queries
- `get_cell_specimens`
- `get_mouse_connectivity_experiments`
- `get_atlases`, `get_structure_graphs`, `get_structures`
- `get_atlas_images`, `get_section_images`
- `get_grid_data_download_url` — 3D expression grids (streamed to disk)
- `get_neuronal_models`

**Primary use cases**: Query Allen Cell Types and Mouse Connectivity, resolve brain-structure ontologies, fetch atlas / section images and 3D expression grids.

## Notes

TypeScript / Node, stdio transport. Calls the public Allen Brain Atlas API — no auth. Streams large downloads to disk. Alpha status and absent LICENSE file mean this is best used as an exploration tool, not a production dependency, until upstream clarifies licensing.

## Sources

- [`maflot/allenbrain-mcp`](https://github.com/maflot/allenbrain-mcp)
- [Allen Brain Map forum announcement](https://community.brain-map.org/t/allenbrain-mcp-mcp-server-wrapper-for-allen-brain-atlas-api-rma-downloads/4858)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=allenbrain&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fallenbrain.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
