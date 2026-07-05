---
title: BCI-MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: enkhbold470 (community)
availability: Alpha
tool_categories: [Neuroscience]
last_verified: 2026-07-05
summary: MCP server streaming live EEG brain-state metrics (focus, calm, attention, band powers) from OpenBCI/Muse/LSL devices — or a hardware-free synthetic mode — into Claude.
---

# BCI-MCP

An MCP server that streams live EEG brain-state metrics — focus, calm, attention, band powers, signal quality — from consumer/research EEG headsets (or a hardware-free synthetic source) into Claude and other MCP clients.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [enkhbold470](https://github.com/enkhbold470/bci-mcp) (community, MIT) |
| **Availability** | Alpha — PyPI/npm `bci-mcp` v0.1.3, released 2026-06-24 |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — reads live/recorded EEG streams; can record sessions and run neurofeedback loops |

## How to install

- **Claude Code** — direct MCP add (npm entrypoint):
  ```
  claude mcp add bci-mcp -- npx -y bci-mcp
  ```
- **Claude Code** — Python entrypoint (installs from PyPI on first run via `uvx`):
  ```
  claude mcp add bci-mcp -- uvx bci-mcp serve
  ```
- **Claude Desktop** — Settings → Developer → Edit Config, add:
  ```json
  {
    "mcpServers": {
      "bci-mcp": {
        "command": "npx",
        "args": ["-y", "bci-mcp"]
      }
    }
  }
  ```
- **Manual PyPI install** (for the `bci-mcp` CLI — `stream`, `record`, `play`, `neurofeedback`, `dashboard`):
  ```
  pip install "bci-mcp[all]"
  ```
  Use extras `[devices]` (BrainFlow), `[lsl]` (pylsl), `[edf]` (recording playback), or `[dashboard]` to install only what you need.

This is a **stdio** server (built with FastMCP): the `claude mcp add`/Desktop config launch the process on demand — you do not keep it running in a separate terminal. Running `uvx bci-mcp serve` or `npx -y bci-mcp` by hand is only a one-shot check that it boots (Ctrl-C after it starts).

## What it does

Exposes 13 tools: `list_devices`, `connect`, `disconnect`, `get_brain_state`, `get_band_powers`, `get_signal_quality`, `get_metric_definitions`, `calibrate`, `record`, `start_neurofeedback`, `get_neurofeedback_score`, `mark_event`, `stream_summary`.

Devices are addressed by URI scheme:

- `synthetic://` — built-in synthetic signal, **no hardware required** (lets you exercise the whole toolchain offline)
- `brainflow://cyton`, `brainflow://muse_s` — OpenBCI Cyton/Ganglion, Muse 2/S via BrainFlow
- `lsl://<name>` — any Lab Streaming Layer source (pylsl)
- `serial://<port>` — generic serial device (pyserial)
- `playback://<file>` — replay a previously recorded session

**Primary use cases**: neurofeedback experiments, live EEG band-power/brain-state monitoring in-conversation, recording and replaying EEG sessions, prototyping BCI workflows without hardware.

## Notes

Community/independent project (not affiliated with any device vendor). Early-stage (v0.1.x, ~120 commits as of verification) — treat as Alpha. The `synthetic://` source means Claude can drive the full tool surface with no headset attached, which is useful for evaluation; real-device use requires the matching hardware and BrainFlow/pylsl extras. A documentation-derived HTTP deployment mode also exists but the stdio path above is the supported Claude integration.

## Sources

- [`enkhbold470/bci-mcp` README](https://github.com/enkhbold470/bci-mcp)
- [PyPI `bci-mcp`](https://pypi.org/project/bci-mcp/)
- [Project docs](https://enkhbold470.github.io/bci-mcp/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=bci-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbci-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
