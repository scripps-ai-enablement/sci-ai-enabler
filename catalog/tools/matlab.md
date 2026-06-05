---
title: MATLAB / Octave (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-06-04
summary: MATLAB and GNU Octave numerical computing for matrix operations, data analysis, visualization, and scientific computing.
---

# MATLAB / Octave (Claude Skill)

MATLAB and GNU Octave numerical computing for matrix operations, data analysis, visualization, and scientific computing.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (For MATLAB (https://www.mathworks.com/pricing-licensing.html) and for Octave (GNU General Public version 3)) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `matlab` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/matlab ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

MATLAB and GNU Octave numerical computing for matrix operations, data analysis, visualization, and scientific computing. Use when writing MATLAB/Octave scripts for linear algebra, signal processing, image processing, differential equations, optimization, statistics, or creating scientific visualizations. Also use when the user needs help with MATLAB syntax, functions, or wants to convert between MATLAB and Python code. Scripts can be executed with MATLAB or the open-source GNU Octave interpreter.

**Primary use cases**: writing MATLAB/Octave scripts for linear algebra, signal processing, image processing, differential equations, optimization, statistics, or creating scientific visualizations.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: For MATLAB (https://www.mathworks.com/pricing-licensing.html) and for Octave (GNU General Public version 3). The skill name to enable after install is `matlab`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/matlab/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/matlab/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=matlab&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmatlab.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
