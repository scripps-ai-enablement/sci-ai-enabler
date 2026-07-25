---
title: ChimeraX MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: mahynotch
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-07-25
summary: Drive UCSF ChimeraX from Claude in natural language — open, mutate, visualize, measure, and render protein structures; ChimeraX auto-launches.
---

# ChimeraX MCP Server

Control UCSF ChimeraX conversationally from Claude — load structures, mutate residues, color and render surfaces, measure geometry, and capture snapshots without typing ChimeraX commands.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [mahynotch](https://github.com/mahynotch/chimerax-mcp) |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT); UCSF ChimeraX is licensed separately (free for academic/non-profit) — review [rbvi.ucsf.edu/chimerax](https://www.rbvi.ucsf.edu/chimerax/) |
| **Capabilities** | Read/Write — Claude issues ChimeraX commands and runs arbitrary scripts against structures on your machine, writing snapshots and edited coordinate files |

## How to install

1. Install [UCSF ChimeraX](https://www.rbvi.ucsf.edu/chimerax/download.html) separately, then install the MCP server (Python 3.10+):
   ```
   pip install chimerax-mcp
   ```
2. Register it:
   - **Claude Code** — direct MCP add (stdio):
     ```
     claude mcp add -s user chimerax -- chimerax-mcp
     ```
   - **Claude Desktop** — stdio entry in `claude_desktop_config.json`:
     ```json
     {
       "mcpServers": {
         "chimerax": {
           "command": "chimerax-mcp",
           "args": []
         }
       }
     }
     ```

The `pip install` step above provides the `chimerax-mcp` binary both registration snippets reference. Claude Code/Desktop launches the stdio process itself — there is no long-running server to keep open in another terminal, and ChimeraX is launched automatically when the first tool is called (no manual REST-API setup).

## What it does

Exposes 39 tools that map onto ChimeraX operations:

- **Structure (6)** — `open_structure`, `close_structure`, `save_structure`, `list_models`, `get_sequence`, `run_script` (arbitrary ChimeraX Python).
- **Editing (4)** — `mutate_residue`, `delete_atoms`, `add_hydrogen`, `minimize_energy`.
- **Visualization (18)** — surfaces (electrostatic, hydrophobicity, plain), cartoon/stick/atom representations, coloring, labels, zoom/view control, snapshots, and recording/spin.
- **Measurement (6)** — `measure_distance`, `measure_angle`, `align_and_rmsd`, `find_contacts`, `get_bfactors`, `measure_buried_area`.
- **Selection (5)** — `select_atoms`, `select_near`, `select_chain`, `invert_selection`, `name_selection`.

**Primary use cases**: interactive structural-biology sessions, residue mutation and energy minimization, publication figures and turntable movies, distance/angle/RMSD measurement and contact analysis.

## Notes

Requires a local UCSF ChimeraX install (any version after 2024-03-18) and Python 3.10+; transport is stdio. Because it drives a full desktop application, it needs a graphical environment (ChimeraX auto-launches on first tool call). Complements the headless, GPU-free [PyMOL](pymol.html) skill (batch rendering) and the data-retrieval [Protein MCP Server](protein-mcp-server.html) / [PDB MCP Server](pdb.html) (fetch structures first, then visualize/edit here). For AlphaFold/ESMFold prediction wired directly into ChimeraX, the sibling `GDAmitha/chimerax-alphafold-mcp` is an alternative packaging (not yet catalogued).

## Sources

- [`mahynotch/chimerax-mcp`](https://github.com/mahynotch/chimerax-mcp)
- [`chimerax-mcp` on PyPI](https://pypi.org/project/chimerax-mcp/)
- [UCSF ChimeraX](https://www.rbvi.ucsf.edu/chimerax/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=chimerax-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fchimerax-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
