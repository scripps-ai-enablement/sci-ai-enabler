---
title: SpikeLab
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Braingeneers
availability: Beta
tool_categories: [Neuroscience]
last_verified: 2026-06-14
summary: Agent-skill suite for multi-electrode-array spike-train analysis and spike sorting (Kilosort2/4, RT-Sort), with an optional built-in MCP server.
---

# SpikeLab

A suite of computational-neuroscience agent skills for loading, sorting, analyzing, and visualizing neuronal spike-train data from multi-electrode-array (MEA) electrophysiology experiments.

| | |
|---|---|
| **Type** | Claude Skill (bundled with an optional MCP server) |
| **Supplier** | [Braingeneers](https://github.com/braingeneers/SpikeLab) |
| **Availability** | Beta — bioRxiv preprint posted 2026-04-25 |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skills' Python locally (Bash); the sorter writes results, the educator skill is read-only |

## How to install

SpikeLab ships its skills inside the installed Python package at `spikelab/agent/skills/`. A lightweight **router** skill detects the environment and delegates to the specialized skills.

1. **Install the package** (with the MCP extra if you also want the MCP server):
   ```
   pip install "spikelab[all]"
   ```
   (Add the `mcp` extra explicitly if you used a narrower install — e.g. `pip install "spikelab[s3,ml,mcp]"`. Kilosort4 is not pulled in by `[all]`; install it separately if you need that sorter.)

2. **Make the skills visible to Claude Code** — copy or symlink them into your skills directory:
   ```
   cp -r "$(python -c 'import spikelab, os; print(os.path.join(os.path.dirname(spikelab.__file__), "agent", "skills"))')" ~/.claude/skills/spikelab
   ```
   (The `python -c …` resolves the installed package's `agent/skills` path for you; replace `~/.claude/skills/spikelab` with your agent's skills directory if different. CLI agents that auto-load skills from installed packages pick these up without the copy.)

3. **(Optional) register the MCP server** for programmatic tool access instead of skills. The upstream README documents the MCP extra but **does not publish a copy-pasteable `claude mcp add` snippet — see the project README and adapt the stdio form below to the module/entry point it ships.**
   - **Claude Code:**
     ```
     claude mcp add --transport stdio spikelab -- python -m spikelab.agent.mcp
     ```
   - **Claude Desktop** (`claude_desktop_config.json`):
     ```json
     {
       "mcpServers": {
         "spikelab": { "command": "python", "args": ["-m", "spikelab.agent.mcp"] }
       }
     }
     ```
   (Both snippets assume the MCP entry point is `spikelab.agent.mcp`; **Unverified —** confirm the exact module/console-script from the README before relying on it. The MCP server is launched by Claude over stdio — no long-running process to keep open.)

## What it does

Skills bundled in the package:

- **spikelab-spikesorter** — sort raw recordings with Kilosort2, Kilosort4, or RT-Sort; curate units; run stim-aligned sorting; inspect sorting output (can submit compute-heavy jobs to remote Kubernetes clusters).
- **spikelab-analysis-implementer** — load data, write and run analysis scripts, generate figures, manage results.
- **spikelab-educator** — explain analyses and methods (read-only).
- **spikelab-developer** — promote analysis code into the library, write tests, expose methods via MCP, open PRs.
- **spikelab-map-updater** — regenerate repo map files after changes.

Loads HDF5, NWB, KiloSort/Phy, and SpikeInterface formats; represents spike trains as `SpikeData` objects (per-unit spike times in ms) and firing rates as `RateData`.

**Primary use cases**: spike sorting MEA recordings, spike-train analysis and figure generation, teaching electrophysiology methods.

## Notes

Python package; the spike sorters (Kilosort2/4, RT-Sort) have heavy GPU/compute dependencies and the package can offload to remote Kubernetes. The MCP server is optional and only present with the `mcp` extra. For a format-agnostic multi-sorter skill without the MEA/Kubernetes focus, see [SpikeInterface](spikeinterface-electrophysiology.html); for Neuropixels-specific workflows see [Neuropixels Analysis](neuropixels-analysis.html).

## Sources

- [`braingeneers/SpikeLab`](https://github.com/braingeneers/SpikeLab)
- [SpikeLab preprint (bioRxiv 2026.04.25.720833)](https://www.biorxiv.org/content/10.64898/2026.04.25.720833v1)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=spikelab&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fspikelab.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
