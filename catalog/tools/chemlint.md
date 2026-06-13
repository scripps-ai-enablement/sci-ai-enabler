---
title: ChemLint
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: molML (TU/e)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-06-13
summary: MCP server exposing 150+ molecular machine-learning tools — SMILES cleaning, descriptors, similarity, clustering, model training — so Claude runs cheminformatics ML without Python scripting.
---

# ChemLint

MCP server that hands Claude 150+ molecular machine-learning tools — SMILES standardization, descriptor and fingerprint calculation, scaffold and similarity analysis, model training, and reporting — so cheminformatics ML workflows run through tool calls instead of hand-written Python.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [molML](https://github.com/molML/ChemLint) |
| **Availability** | GA — actively maintained |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — computes locally on molecules you supply |

## How to install

Requires [`uv`](https://docs.astral.sh/uv/) (Python 3.13+ is provisioned by `uv`); Cairo is optional for molecular-structure rendering.

- **Install and verify it starts** (the `pytest` run is a one-shot check — Ctrl-C is not needed, it exits on its own; Claude Code/Desktop launch the server themselves via stdio):
  ```
  git clone https://github.com/molML/ChemLint.git
  cd ChemLint
  uv sync
  uv run pytest -m server -q
  ```

- **Claude Code** — direct MCP add (replace `/path/to/ChemLint` with the absolute path of your clone — e.g., `$(pwd)` if you are still inside it from the previous step):
  ```
  claude mcp add --transport stdio chemlint -- uv run --with "mcp[cli]" --directory /path/to/ChemLint mcp run ./src/chemlint/server.py
  ```

- **Claude Desktop** — add to `claude_desktop_config.json` (replace `/path/to/uv` with the absolute path to your `uv` binary — `which uv` prints it — and `/path/to/ChemLint` with your clone's absolute path):
  ```json
  {
    "mcpServers": {
      "chemlint": {
        "command": "/path/to/uv",
        "args": [
          "run",
          "--with",
          "mcp[cli]",
          "--directory",
          "/path/to/ChemLint",
          "mcp",
          "run",
          "./src/chemlint/server.py"
        ],
        "enabled": true
      }
    }
  }
  ```
  (`./install.sh` from the clone automates the Claude Desktop config edit.)

## What it does

150+ tools across 13 categories: data management, molecular cleaning (standardization, canonicalization, validation pipelines), descriptors and fingerprints (MW, LogP, TPSA, ECFP, MACCS, RDKit), scaffolds, similarity (Tanimoto), clustering, machine learning (33+ algorithms with cross-validation and hyperparameter tuning), statistics, visualization, quality reports, activity-cliff detection, outlier detection, and dimensionality reduction.

**Primary use cases**: SMILES dataset cleaning and QC, molecular descriptor/fingerprint featurization, QSAR/property model training, similarity and scaffold analysis.

## Notes

stdio transport — Claude Code/Desktop launch the server process; you do not keep it running in a separate terminal. Molecular-structure image rendering needs Cairo installed; descriptor/ML tools work without it. A separately-developed sibling, `derekvantilborg/molml_mcp`, shares the "molecular machine learning MCP" description; the relationship is not documented upstream — **Unverified —** treat them as distinct projects until upstream clarifies.

## Sources

- [`molML/ChemLint`](https://github.com/molML/ChemLint)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=chemlint&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fchemlint.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
