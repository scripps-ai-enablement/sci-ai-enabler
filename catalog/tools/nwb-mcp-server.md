---
title: NWB MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Ben Hardcastle
availability: Beta
tool_categories: [Neuroscience]
last_verified: 2026-08-16
summary: Query local, S3, or DANDI-hosted NWB neurophysiology files as a virtual SQL database, read-only, without writing Python.
---

# NWB MCP Server

MCP server that exposes Neurodata Without Borders (NWB) files — on disk, on S3, or in a DANDI dandiset — as a virtual SQL database Claude can explore and query read-only.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Ben Hardcastle](https://github.com/bjhardcastle/nwb-mcp-server) |
| **Availability** | Beta (PyPI 0.1.9, released 2026-06-07; repo last pushed 2026-06-07) |
| **Pricing** | Free / OSS — MIT |
| **Capabilities** | Read-only — the server never writes to NWB files |

## How to install

Requires Python 3.10+ and [`uv`](https://docs.astral.sh/uv/getting-started/installation/) (`pip install uv`). No clone is needed — `uvx` fetches the published package.

- **Verify it starts** (one-shot; Ctrl-C once it boots — Claude Code and Claude Desktop launch the process themselves over stdio):
  ```
  uvx nwb-mcp-server --root_dir data --glob_pattern "*.nwb"
  ```
  (replace `data` with the directory holding your NWB files — e.g. `/Users/you/data/nwb`, or `$(pwd)/data`.)

- **Claude Code** — direct MCP add (stdio):
  ```
  claude mcp add --transport stdio nwb -- uvx nwb-mcp-server --root_dir /absolute/path/to/nwb-files --glob_pattern "*.nwb"
  ```
  (replace `/absolute/path/to/nwb-files` with the absolute path of the directory containing your `.nwb` files.)

- **Claude Code** — point it at a DANDI dandiset instead of local files:
  ```
  claude mcp add --transport stdio nwb-dandi -- uvx nwb-mcp-server --dandiset_id 000363 --anon
  ```

- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "nwb": {
        "command": "uvx",
        "args": [
          "nwb-mcp-server",
          "--root_dir", "/absolute/path/to/nwb-files",
          "--glob_pattern", "*.nwb"
        ]
      }
    }
  }
  ```
  (`uvx` must be on the `PATH` Claude Desktop sees; if it is not, use the absolute path to the `uvx` binary, e.g. `/Users/you/.local/bin/uvx`.)

## What it does

Builds a lazy, schema-inferred virtual table view over a collection of NWB files using [`lazynwb`](https://github.com/bjhardcastle/lazynwb), then lets Claude interrogate it with SQL rather than by generating and running analysis scripts. Ten read-only tools:

- **Discovery** — `get_tables`, `get_table_schema`, `get_nwb_paths`, `preview_table_values`
- **Query** — `execute_query` (SQL against the virtual NWB database)
- **Source switching** — `get_active_source`, `use_local_source`, `use_dandiset_source`, `reset_active_source`
- **Escape hatch** — `nwb_file_search_code_snippet`, which returns Python for locating files when SQL is not enough

Configuration flags include `--root_dir`, `--glob_pattern`, `--dandiset_id`, `--dandiset_version`, `--dandiset_path_filter`, `--tables`, `--infer_schema_length`, `--anon` (anonymous S3), `--unattended`, and `--max_result_rows` (default 50).

**Primary use cases**: rapid exploration of an unfamiliar NWB dataset, cross-file unit/trial table queries, generating summary reports over a dandiset.

## Notes

- **Read-only by design.** The server has no write path into NWB files, which is the main reason to prefer it over letting Claude run `pynwb` code directly.
- **Schema inference reads one file by default** (`--infer_schema_length 1`). If files in a collection have heterogeneous tables or columns, raise this or the schema will be incomplete.
- **Result rows are capped** at `--max_result_rows` (50) and the README documents a `table_element_limit` of 500 elements (columns × rows) — large result sets are truncated rather than streamed, so aggregate in SQL rather than pulling raw traces.
- **SQL, not signal processing.** This surfaces the tabular side of NWB (units, trials, epochs, electrodes, subject metadata). Continuous acquisition data and spike-waveform analysis are out of its remit — pair it with [SpikeLab](spikelab.html), [SpikeInterface](spikeinterface-electrophysiology.html), or [Neurosift Tools MCP](neurosift.html) (which covers DANDI semantic search and `dandiset_info`).
- **Upstream flag spelling.** The README's JSON example uses underscore flags (`--root_dir`, `--glob_pattern`); the snippets above follow it. The upstream docs are written for VS Code Copilot Chat, and state only that "similar agent extensions, such as Cline or Claude Code, should also be able to connect to the server" — the Claude Code and Claude Desktop forms above are adapted from the published `command`/`args` pair. **Unverified —** the maintainer does not publish Claude-specific registration snippets.
- **`lazynwb` is pinned to a pre-release** (`lazynwb==1.0.0dev3`), so expect API churn.
- Experimental, undocumented support exists for non-NWB tabular files (CSV, Parquet) via Polars I/O.
- Small project: 2 GitHub stars as of 2026-08-16. The maintainer works on Allen Institute neuropixels data tooling, which is the workload the server is shaped around.

## Sources

- [`bjhardcastle/nwb-mcp-server`](https://github.com/bjhardcastle/nwb-mcp-server)
- [`nwb-mcp-server` on PyPI](https://pypi.org/project/nwb-mcp-server/)
- [`lazynwb`](https://github.com/bjhardcastle/lazynwb)
- [Neurodata Without Borders](https://nwb.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=nwb-mcp-server&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fnwb-mcp-server.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
