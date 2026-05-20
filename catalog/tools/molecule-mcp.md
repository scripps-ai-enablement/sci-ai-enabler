---
title: Molecule-MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: chatmol
availability: GA
tool_categories: [Chemistry, Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
last_verified: 2026-05-20
summary: MCP bundle letting Claude drive PyMOL and ChimeraX visualization and run GROMACS molecular dynamics simulations via natural language.
---

# Molecule-MCP

Bundle of three MCP servers that turn Claude into a natural-language driver for molecular visualization (PyMOL, ChimeraX) and molecular dynamics (GROMACS).

| | |
|---|---|
| **Type** | MCP server (bundle of three) |
| **Supplier** | [chatmol](https://github.com/chatmol/molecule-mcp) (community OSS) |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write |

## How to install

```
pip install "mcp[cli]" chatmol
git clone https://github.com/chatmol/molecule-mcp
```

Register three entries in `claude_desktop_config.json` pointing at the bundled scripts:

```json
{
  "mcpServers": {
    "pymol":            { "command": "python", "args": ["/path/to/molecule-mcp/pymol_server.py"] },
    "chimerax":         { "command": "python", "args": ["/path/to/molecule-mcp/ChimeraX_server.py"] },
    "gromacs_copilot":  { "command": "python", "args": ["/path/to/molecule-mcp/mcp_server.py"] }
  }
}
```

## What it does

- **PyMOL server** — visualization commands driven from chat (load, color, select, render).
- **ChimeraX server** — same shape for ChimeraX.
- **GROMACS Copilot** — MD setup, solvation, equilibration, and production runs from natural language.

**Primary use cases**: Conversational molecular visualization, agent-driven MD setup and execution, structural-biology demos and teaching.

## Notes

Requires local PyMOL, ChimeraX, and (optionally) GROMACS installations. stdio transport. Research-use disclaimer (no warranty) — validate results independently before drawing conclusions from the simulations.

## Sources

- [`chatmol/molecule-mcp`](https://github.com/chatmol/molecule-mcp)
- [Playbooks listing](https://playbooks.com/mcp/chatmol/molecule-mcp)
