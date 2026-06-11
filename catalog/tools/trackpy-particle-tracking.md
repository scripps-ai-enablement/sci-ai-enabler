---
title: trackpy (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-11
summary: "Python library for single-particle tracking (SPT) in video microscopy via the Crocker-Grier algorithm."
---

# trackpy (Claude Skill)

Python library for single-particle tracking (SPT) in video microscopy via the Crocker-Grier algorithm.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (BSD-3-Clause) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/jaechang-hits/SciAgent-Skills
  ```
  Then inside Claude Code run `/plugin install sciagent-skills` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r SciAgent-Skills/skills/cell-biology/trackpy-particle-tracking ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Python library for single-particle tracking (SPT) in video microscopy via the Crocker-Grier algorithm. Locate particles (fluorescent spots, colloids, vesicles, cells) per frame, link into trajectories, filter short tracks, and compute MSD for diffusion analysis. 2D/3D with subpixel accuracy; reads TIF stacks, AVI, image series via pims. Use for quantitative SPT and diffusion coefficient extraction from fluorescence or brightfield video.

**Primary use cases**: quantitative SPT and diffusion coefficient extraction from fluorescence or brightfield video.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: BSD-3-Clause. The skill directory upstream is `skills/cell-biology/trackpy-particle-tracking`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/cell-biology/trackpy-particle-tracking/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/cell-biology/trackpy-particle-tracking/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=trackpy-particle-tracking&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftrackpy-particle-tracking.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
