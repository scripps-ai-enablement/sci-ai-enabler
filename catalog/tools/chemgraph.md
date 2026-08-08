---
title: ChemGraph
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Argonne National Laboratory (ALCF)
availability: Beta
tool_categories: [Chemistry]
last_verified: 2026-08-08
summary: Argonne MCP server that runs real molecular simulations through ASE — geometry optimization, energies, and frequencies via xTB, DFT, or ML potentials.
---

# ChemGraph

MCP server from Argonne National Laboratory that lets Claude set up **and actually run** molecular simulations — name-to-SMILES lookup, 3D structure generation, and ASE-driven geometry optimization or energy/frequency calculations against semi-empirical, DFT, or machine-learning-potential backends.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Argonne National Laboratory / ALCF](https://github.com/argonne-lcf/ChemGraph) |
| **Availability** | Beta — PyPI `chemgraph` 0.6.0, released 2026-07-19 |
| **Pricing** | Free / OSS (Apache-2.0, confirmed via the GitHub license API). The wrapped engines carry their own terms — TBLite/xTB (LGPL-3.0) and NWChem (ECL-2.0) are free, ORCA is free for academic use after registration, Gaussian is commercial. |
| **Capabilities** | Read/Write — executes calculations and writes coordinate and JSON result files to disk |

## How to install

Python 3.10+ is required. Install into a virtual environment so the calculator extras stay isolated:

```
python -m venv chemgraph-env
source chemgraph-env/bin/activate
pip install "chemgraph[calculators]"
```

The `[calculators]` extra pulls in TBLite (xTB), which is the only backend that works out of the box. DFT engines (NWChem, ORCA) and ML potentials (MACE, UMA) must be installed separately and be reachable on `PATH`.

Register with Claude Code. Use the **absolute path to the virtual environment's `python`**, not bare `python` — Claude Code launches the process outside your activated shell (replace `/path/to/chemgraph-env` with the absolute path of the venv you just created — e.g., `/Users/you/chemgraph-env`, or `$(pwd)/chemgraph-env` if you are still in the directory from the previous step):

```
claude mcp add --transport stdio chemgraph -- /path/to/chemgraph-env/bin/python -m chemgraph.mcp.mcp_tools
```

For Claude Desktop, add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chemgraph": {
      "command": "/path/to/chemgraph-env/bin/python",
      "args": ["-m", "chemgraph.mcp.mcp_tools"]
    }
  }
}
```

Both clients launch the process themselves over stdio — you do not keep a terminal open. `stdio` is the module's default transport, so no flags are needed.

To run it instead as a long-lived HTTP service (useful when the compute node is not the machine running Claude), start it in its own terminal and leave it running:

```
/path/to/chemgraph-env/bin/python -m chemgraph.mcp.mcp_tools --transport streamable_http --host 127.0.0.1 --port 9003
claude mcp add --transport http chemgraph http://127.0.0.1:9003/mcp
```

**Unverified —** the HTTP endpoint path is not documented upstream; `/mcp` is the FastMCP default for `streamable_http_app()`. If the connection fails, try the bare host and port.

## What it does

Four tools in `chemgraph.mcp.mcp_tools`:

- `molecule_name_to_smiles` — resolve a common or IUPAC name to a canonical SMILES string via PubChem.
- `smiles_to_coordinate_file` — generate a 3D coordinate file from SMILES.
- `run_ase` — run an ASE calculation (single point, geometry optimization, vibrational frequencies) with a specified calculator and parameters.
- `extract_output_json` — load and summarize the JSON results a `run_ase` job wrote.

Backends reach through ASE to semi-empirical xTB (via TBLite), DFT and coupled-cluster methods (NWChem, ORCA), and machine-learning potentials (MACE, UMA).

**Primary use cases**: Geometry optimization and single-point energies for small molecules, vibrational frequency checks, name→structure→calculation workflows without hand-writing input decks.

## Notes

The MCP server itself calls no language model and needs no API key — it is a plain tool surface. The wider ChemGraph project is a LangGraph agent framework, and *that* side does require model credentials; you do not need them to use the server described here.

`chemgraph.mcp.mcp_tools` is the general-purpose server. The package ships several sibling modules for HPC and ensemble work — `mace_mcp_parsl.py`, `graspa_mcp_parsl.py` (gRASPA adsorption), `xanes_mcp_parsl.py` (XANES spectra), `ase_mcp_hpc.py`, and `data_analysis_mcp.py` — each launched the same way by swapping the module name. They are undocumented upstream; treat them as unverified.

The upstream `docker run ghcr.io/argonne-lcf/chemgraph:latest` command in the README starts **JupyterLab, not the MCP server** — it is not an install path for Claude.

`run_ase` executes computations on your machine and writes files to disk. Run it in a scratch directory, and be aware that a DFT job requested casually in conversation can consume real wall time and cores.

For input-deck preparation without execution, see [XTB MCP Server](xtb-mcp-server.html), which generates and validates xtb control files but does not run them.

## Sources

- [`argonne-lcf/ChemGraph`](https://github.com/argonne-lcf/ChemGraph)
- [`chemgraph` on PyPI](https://pypi.org/project/chemgraph/)
- [`src/chemgraph/mcp/mcp_tools.py`](https://github.com/argonne-lcf/ChemGraph/blob/main/src/chemgraph/mcp/mcp_tools.py)
- [`src/chemgraph/mcp/server_utils.py`](https://github.com/argonne-lcf/ChemGraph/blob/main/src/chemgraph/mcp/server_utils.py)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=chemgraph&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fchemgraph.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
