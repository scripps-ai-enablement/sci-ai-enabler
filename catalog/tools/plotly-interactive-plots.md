---
title: Plotly (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: SciAgent
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-06-11
summary: "Interactive scientific visualization with Plotly."
---

# Plotly (Claude Skill)

Interactive scientific visualization with Plotly.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0) |
| **Availability** | GA — part of the BixBench-evaluated SciAgent-Skills collection |
| **Pricing** | Free / OSS (MIT) |
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
  cp -r SciAgent-Skills/skills/data-visualization/plotly-interactive-plots ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use.

## What it does

Interactive scientific visualization with Plotly. Two APIs: plotly.express (px) for one-liner DataFrame plots, plotly.graph_objects (go) for trace-level control. 40+ chart types with hover, zoom, pan, animation. Exports HTML or static PNG/SVG/PDF via kaleido. Use for volcano plots with gene hover, dose-response dashboards, expression heatmaps, 3D molecular views. Use seaborn for stats; matplotlib for publication figures.

**Primary use cases**: volcano plots with gene hover, dose-response dashboards, expression heatmaps, 3D molecular views.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the SciAgent-Skills collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/data-visualization/plotly-interactive-plots`.

## Sources

- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills)
- [`skills/data-visualization/plotly-interactive-plots/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/data-visualization/plotly-interactive-plots/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=plotly-interactive-plots&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fplotly-interactive-plots.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
