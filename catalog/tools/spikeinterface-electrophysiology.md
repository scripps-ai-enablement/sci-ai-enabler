---
title: SpikeInterface (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "Unified Python framework for extracellular electrophysiology."
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches jaechang-hits SciAgent-Skills, CC BY 4.0 root LICENSE, no OSV advisories, read-only local skill"
---

# SpikeInterface (Claude Skill)

Unified Python framework for extracellular electrophysiology.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches jaechang-hits, CC BY 4.0, no OSV advisories |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/scientific-computing/spikeinterface-electrophysiology ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Unified Python framework for extracellular electrophysiology. Load 20+ formats (SpikeGLX, OpenEphys, NWB, Intan, Maxwell, Blackrock), preprocess, run 10+ sorters (Kilosort4, SpykingCircus2, Tridesclous, MountainSort5) via one API, compute quality metrics (SNR, ISI, firing rate), compare sorters, export NWB/Phy. For format-agnostic multi-sorter workflows. For Neuropixels-specific PSTH/decoding use neuropixels.

**Primary use cases**: Unified Python framework for extracellular electrophysiology.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/scientific-computing/spikeinterface-electrophysiology`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/scientific-computing/spikeinterface-electrophysiology/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/scientific-computing/spikeinterface-electrophysiology/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=spikeinterface-electrophysiology&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fspikeinterface-electrophysiology.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
