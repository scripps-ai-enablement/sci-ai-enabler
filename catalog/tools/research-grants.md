---
title: Research Grants (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-06-04
claude_science: true
summary: Write competitive research proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC.
---

# Research Grants (Claude Skill)

Write competitive research proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `research-grants` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/research-grants ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Write competitive research proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC. Agency-specific formatting, review criteria, budget preparation, broader impacts, significance statements, innovation narratives, and compliance with submission requirements.

**Primary use cases**: Write competitive research proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Research Resources* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill name to enable after install is `research-grants`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/research-grants/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/research-grants/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=research-grants&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fresearch-grants.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
