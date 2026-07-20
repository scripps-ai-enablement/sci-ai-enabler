---
title: GROMACS MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: MacromNex
availability: Alpha
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-07-11
verification: works
verified_on: 2026-07-20
verification_note: "MacromNex/gromacs_mcp repo and Dockerfile build path resolve; prebuilt ghcr image tag not independently confirmable statically"
security: caution
security_on: 2026-07-20
security_note: "provenance matches supplier MacromNex, no repo LICENSE file (redistribution terms unclear), alpha single-community project, no OSV advisories"
summary: "Run GROMACS molecular-dynamics simulations and trajectory analysis from Claude via a Docker container with GROMACS 2025.4 pre-installed."
---

# GROMACS MCP Server

Drive GROMACS molecular-dynamics simulations and analysis from Claude through a self-contained Docker container that ships GROMACS 2025.4, with async job tracking for long-running runs.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [MacromNex](https://github.com/MacromNex/gromacs_mcp) |
| **Availability** | Alpha (repo created 2025-12-24, last updated 2026-04-17) |
| **Pricing** | Free / OSS (**Unverified —** upstream declares no repository LICENSE file; the README lists only "LGPL (GROMACS)", which is GROMACS's own license, not the wrapper's. Do not assume redistribution terms until a license is published upstream) |
| **Capabilities** | Read/Write — runs GROMACS commands and simulations against files in the mounted working directory |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — provenance matches MacromNex, no repo LICENSE, alpha, no OSV advisories |

## How to install

Both paths register the server with Claude Code over stdio; Claude launches the `docker run` process itself on demand (no separate long-running terminal). The container mounts your current directory so GROMACS can read/write your input and output files.

- **Prerequisite** — [Docker](https://docs.docker.com/get-docker/) installed and running, plus Claude Code.

- **Claude Code — pull the prebuilt image (recommended):**
  ```
  docker pull ghcr.io/macromnex/gromacs_mcp:latest
  claude mcp add gromacs -- docker run -i --rm --user `id -u`:`id -g` -v `pwd`:`pwd` ghcr.io/macromnex/gromacs_mcp:latest
  ```
  (Run the `claude mcp add` command from the directory that holds your simulation files — the `` -v `pwd`:`pwd` `` mount and `` `id -u`:`id -g` `` are evaluated by your shell at registration time, so the container sees that directory at the same absolute path.)

- **Claude Code — build locally:**
  ```
  git clone https://github.com/MacromNex/gromacs_mcp.git
  cd gromacs_mcp
  docker build -t gromacs_mcp:latest .
  claude mcp add gromacs -- docker run -i --rm --user `id -u`:`id -g` -v `pwd`:`pwd` gromacs_mcp:latest
  ```

- **Claude Desktop** — Claude Desktop cannot expand shell backticks in a JSON config, so it cannot reproduce the `` `id -u` ``/`` `pwd` `` substitutions the way Claude Code does. **Registration not documented upstream for Claude Desktop** — the Desktop `claude_desktop_config.json` entry would need the `docker run` args pre-expanded to literal values, e.g.:
  ```json
  {
    "mcpServers": {
      "gromacs": {
        "command": "docker",
        "args": ["run", "-i", "--rm", "-v", "/absolute/path/to/your/workdir:/absolute/path/to/your/workdir", "ghcr.io/macromnex/gromacs_mcp:latest"]
      }
    }
  }
  ```
  (replace `/absolute/path/to/your/workdir` with the absolute path of the directory holding your GROMACS files — e.g. `/Users/you/md-run`; adapt/verify against the upstream README before relying on it.)

## What it does

Exposes six tools that front the GROMACS command-line toolkit inside the container:

- `run_gromacs_command` — execute a single GROMACS command with input/output files and parameters; also analyzes TPR files.
- `run_gromacs_workflow` — orchestrate a predefined multi-step workflow (a `demo` workflow is documented; other named workflows are not enumerated upstream).
- `submit_md_simulation` — submit a long-running MD production run (input TPR, step count, output dir, job name) for asynchronous background execution.
- `submit_batch_analysis` — batch-analyze multiple molecular systems / TPR files in parallel.
- `get_job_status` — poll a background job's progress without pulling full results.
- `get_job_result` — retrieve a completed job's outputs.

Operations returning in under ~10 minutes run synchronously; longer tasks use the async job-submission tools (`submit_*` → `get_job_status` → `get_job_result`).

**Primary use cases**: run and monitor GROMACS MD simulations from Claude, batch trajectory/energetics analysis across multiple systems, TPR inspection.

## Notes

Alpha-stage community project, not vendor-affiliated. The container bundles GROMACS 2025.4, so no local GROMACS install is needed — everything runs inside Docker. GPU-acceleration support, memory requirements, and the full set of named workflows / supported force fields are **not documented upstream** (`detail.md` covers only tool signatures); verify capability against your own systems. Force-field files and topology preparation are your responsibility — the tools operate on files you provide in the mounted directory. Because the server writes into the mounted working directory, treat it as Read/Write and mount only the directory you intend GROMACS to touch. For MD runners without Docker, see the catalogued [OpenMM MCP](openmm-mcp.html); for GROMACS+VMD visualization workflows, `egtai/gmx-vmd-mcp` remains deferred pending a followable install path.

## Sources

- [`MacromNex/gromacs_mcp`](https://github.com/MacromNex/gromacs_mcp)
- [`MacromNex/gromacs_mcp` README](https://github.com/MacromNex/gromacs_mcp/blob/main/README.md)
- [`MacromNex/gromacs_mcp` detail.md](https://github.com/MacromNex/gromacs_mcp/blob/main/detail.md)
- [GROMACS](https://www.gromacs.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=gromacs-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgromacs-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
