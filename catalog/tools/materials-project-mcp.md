---
title: Materials Project MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Path Integral Institute
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-08-01
summary: MCP server for querying Materials Project crystal structures by formula, exporting CIF/POSCAR, and building supercells and moiré bilayers.
---

# Materials Project MCP Server

MCP server that lets Claude search the [Materials Project](https://next-gen.materialsproject.org/) database for inorganic crystal structures, export them in CIF or POSCAR form, and build derived cells.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Path Integral Institute](https://github.com/pathintegral-institute/mcp.science) — the `mcp.science` collection |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT); a free Materials Project account is required for the API key |
| **Capabilities** | Read/Write — reads the database, writes structure files and plots locally |

Launch directly with `uvx` (no clone needed — `uvx` installs and runs the collection package in one step):

```
uvx mcp-science materials-project
```

Get an API key first: register at [next-gen.materialsproject.org](https://next-gen.materialsproject.org/), open your Dashboard, go to **API Keys**, and generate one. Pass it as the `MP_API_KEY` environment variable.

Register with Claude Code:

```
claude mcp add --transport stdio materials-project --env MP_API_KEY=your_key_here -- uvx mcp-science materials-project
```

For Claude Desktop, add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "materials-project": {
      "command": "uvx",
      "args": ["mcp-science", "materials-project"],
      "env": { "MP_API_KEY": "your_key_here" }
    }
  }
}
```

Both clients launch the process themselves over stdio — you do not keep a terminal open.

## What it does

Seven tools:

- `search_materials_by_formula` — find entries by chemical composition.
- `select_material_by_id` — pull a specific material by its `mp-*` identifier.
- `get_structure_data` — export the structure as CIF or POSCAR.
- `create_structure_from_poscar` — parse a POSCAR string into a structure object.
- `plot_structure` — render the crystal structure, optionally as a supercell.
- `build_supercell` — expand a bulk structure into a supercell.
- `moire_homobilayer` — construct moiré superstructures from 2D materials.

**Primary use cases**: Pulling reference crystal structures for a composition, preparing POSCAR/CIF inputs for downstream electronic-structure runs, quick structure visualization.

## Notes

stdio transport. Requires the `MP_API_KEY` environment variable; requests are made against the Materials Project API under its own terms of use.

This is one server in the `mcp.science` collection (MIT), which also ships GPAW density-functional-theory, sandboxed Python execution, Jupyter-kernel, Wolfram-Language, and web/academic-search servers under the same `uvx mcp-science <server-name>` launch pattern.

Materials science rather than life science, catalogued here because structure retrieval and cell construction recur in biomaterials, nanoparticle, and solid-state formulation work.

## Sources

- [`pathintegral-institute/mcp.science`](https://github.com/pathintegral-institute/mcp.science)
- [materials-project server directory](https://github.com/pathintegral-institute/mcp.science/tree/main/servers/materials-project)
- [Materials Project](https://next-gen.materialsproject.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=materials-project-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmaterials-project-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
