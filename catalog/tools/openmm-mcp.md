---
title: OpenMM MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: PhelanShao (community OSS)
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Drug Repurposing and Discovery]
last_verified: 2026-06-20
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "provenance matches supplier PhelanShao, no OSV advisories, but GitHub license classifier reports NOASSERTION while page claims GPLv3, single-maintainer + stale (last push 2025-05-31)"
summary: MCP server that sets up and runs OpenMM molecular dynamics simulations (protein, membrane, advanced sampling) and Abacus DFT jobs from natural language.
---

# OpenMM MCP Server

MCP server that lets Claude configure, launch, monitor, and analyze OpenMM molecular dynamics simulations — including protein and membrane system setup, advanced sampling, and Abacus DFT calculations — through discrete tool calls.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [PhelanShao](https://github.com/PhelanShao/openmm-mcp-server) (community OSS) |
| **Availability** | GA — published on GitHub; stdio MCP server |
| **Pricing** | Free / OSS (GPLv3); OpenMM is MIT |
| **Capabilities** | Read/Write — writes simulation inputs and runs MD/DFT jobs on the host |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — PhelanShao/openmm-mcp-server resolves, no OSV advisories, NOASSERTION license vs GPLv3 claim, single-maintainer + stale (2025-05-31) |

## How to install

This is a local stdio server. Clone it, install its Python dependencies, then register it.

```
git clone https://github.com/PhelanShao/openmm-mcp-server
cd openmm-mcp-server
pip install -r requirements.txt
```

(`requirements.txt` pulls in OpenMM and the task-management dependencies; a CUDA-capable GPU is needed for non-trivial production runs — OpenMM's CPU platform works for small/tutorial systems.)

- **Claude Code** — register over stdio (Claude launches the process itself; no separate terminal needed). Run this from inside the clone, or replace `/path/to/openmm-mcp-server` with the absolute path of your clone (e.g. `/Users/you/repos/openmm-mcp-server`, or `$(pwd)` if you are still inside it from the previous step):

  ```
  claude mcp add --transport stdio openmm-server -- python /path/to/openmm-mcp-server/run_openmm_server.py
  ```

- **Claude Desktop** — add the equivalent stdio entry to `claude_desktop_config.json` (set `cwd` to the absolute path of your clone):

  ```json
  {
    "mcpServers": {
      "openmm-server": {
        "command": "python",
        "args": ["run_openmm_server.py"],
        "cwd": "/path/to/openmm-mcp-server"
      }
    }
  }
  ```

  (The upstream README also shows an `alwaysAllow` array listing every tool name — that field is optional and auto-approves those tool calls; omit it if you want to confirm each invocation.)

## What it does

Exposes discrete MCP tools for end-to-end MD and DFT work:

- `create_md_simulation` / `create_advanced_md_simulation` — build a basic or advanced MD job (advanced integrators, barostats, constraints, metadynamics / free-energy sampling)
- `setup_protein_simulation` — protein-system preparation template
- `setup_membrane_simulation` — membrane-system preparation template
- `create_dft_calculation` — DFT calculation via the Abacus engine
- `control_simulation` — start / stop / pause running jobs
- `get_task_status` / `list_all_tasks` — asynchronous task management with persistence
- `analyze_results` — post-run analysis

**Primary use cases**: protein-stability MD, membrane-protein simulations, advanced free-energy/metadynamics sampling, quick DFT calculations driven from natural language.

## Notes

- **Compute-heavy and write-capable.** The server runs simulations on the host machine and writes outputs; production MD assumes a CUDA-capable GPU. Treat it as a long-running compute tool, not a read-only data lookup.
- Licensed GPLv3 (the wrapper); OpenMM itself is MIT.
- Complements the [Molecular Dynamics (Claude Skill)](molecular-dynamics.html) — that skill teaches Claude to write and run OpenMM/MDAnalysis Python directly, whereas this server exposes MD/DFT as managed MCP tool calls with task tracking. Use [PDB MCP Server](pdb.html) / [AlphaFold MCP Server](alphafold.html) for structure retrieval upstream and trajectory-analysis skills downstream.
- **Unverified —** the exact `requirements.txt` contents and whether `run_openmm_server.py` is the canonical entry filename were read from the README excerpt only; confirm against the repo before a clean-room install.

## Sources

- [`PhelanShao/openmm-mcp-server`](https://github.com/PhelanShao/openmm-mcp-server)
- [OpenMM](https://openmm.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=openmm-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fopenmm-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
