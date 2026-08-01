---
title: XTB MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: PhelanShao (community)
availability: Beta
tool_categories: [Chemistry]
last_verified: 2026-08-01
summary: MCP server that builds, validates, and explains xtb semi-empirical quantum-chemistry input decks for optimizations, frequencies, MD, and spectroscopy.
---

# XTB MCP Server

MCP server that generates and validates input files for **xtb**, the Grimme-group extended tight-binding code, so Claude can set up semi-empirical quantum-chemistry calculations without you hand-writing control decks.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [PhelanShao](https://github.com/PhelanShao/xtb-mcp-server) (community OSS) |
| **Availability** | Beta — install from a clone; not published to PyPI |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — writes input files and control decks to disk |

Clone and install:

```
git clone https://github.com/PhelanShao/xtb-mcp-server
cd xtb-mcp-server
pip install -r requirements.txt
python run_tests.py   # optional: confirms the install; not a long-lived server
```

Register with Claude Code (replace `/path/to/xtb-mcp-server` with the absolute path of your clone — e.g., `/Users/you/repos/xtb-mcp-server`, or `$(pwd)` if you are still inside it from the previous step):

```
claude mcp add --transport stdio xtb -- python /path/to/xtb-mcp-server/main.py
```

For Claude Desktop, add to `claude_desktop_config.json` (this is the snippet the upstream README shows, with the placeholder path made explicit):

```json
{
  "mcpServers": {
    "xtb-mcp-server": {
      "command": "python",
      "args": ["/path/to/xtb-mcp-server/main.py"],
      "env": {}
    }
  }
}
```

Claude Code and Claude Desktop launch the process themselves over stdio — you do not keep a terminal open.

## What it does

Ten tools:

- `generate_xtb_input_package` — build a complete input set for a calculation type (single point, optimization, frequency, scan, MD).
- `generate_xcontrol_file` — write an `xcontrol` deck with custom constraints and parameters.
- `validate_xtb_input_files` — syntax- and parameter-check an input set before submission.
- `convert_structure_file_format` — interconvert XYZ, TURBOMOLE `coord`, and Gaussian geometry formats.
- `explain_xtb_parameters` — narrate what a given keyword or Hamiltonian choice does.
- `generate_enhanced_sampling_input` — metadynamics and pathfinder sampling setups.
- `generate_wavefunction_analysis_input` — orbital and population analysis runs.
- `generate_oniom_input` — multi-layer QM/MM (ONIOM) partitions.
- `generate_spectroscopy_input` — spectroscopic property calculations.
- `analyze_trajectory` — post-process MD trajectory output.

Covers the GFN0-xTB, GFN1-xTB, GFN2-xTB, and GFN-FF Hamiltonians.

**Primary use cases**: Conformer optimization and frequency checks on small organics, reaction-coordinate scans, QM/MM partitioning, metadynamics setup for conformational search.

## Notes

stdio transport. The server's job is **input preparation and validation** — the tool names are all `generate_*` / `validate_*` / `explain_*`. **Unverified —** the README does not state whether the `xtb` binary itself must be installed separately to execute the generated decks (or for `analyze_trajectory`); assume you need [xtb](https://github.com/grimme-lab/xtb) on `PATH` to actually run the calculations, and install it via `conda install -c conda-forge xtb` if so.

**Unverified —** the README states no minimum Python version.

The README's license statement appears only in its Chinese section ("本项目采用 MIT 许可证" — this project uses the MIT License).

For a full agentic compchem stack rather than input generation, see [ChemGraph](https://github.com/argonne-lcf/ChemGraph) (Argonne, ships an MCP server over ASE/TBLite/NWChem/ORCA/MACE) — not yet catalogued pending license and tool-list confirmation.

## Sources

- [`PhelanShao/xtb-mcp-server`](https://github.com/PhelanShao/xtb-mcp-server)
- [`grimme-lab/xtb`](https://github.com/grimme-lab/xtb)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=xtb-mcp-server&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fxtb-mcp-server.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
