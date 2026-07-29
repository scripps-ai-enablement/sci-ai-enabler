---
title: What-If Oracle (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-29
verification_note: "repo and skills/what-if-oracle dir resolve on K-Dense-AI/scientific-agent-skills"
security: caution
security_on: 2026-07-29
security_note: "provenance matches K-Dense-AI but page states CC BY-NC-SA 4.0 (non-commercial) while the collection root is MIT — non-commercial restriction limits reuse"
summary: Run structured What-If scenario analysis with 4–6 branch possibility exploration (best, likely, worst, wild card, contrarian, second-order).
---

# What-If Oracle (Claude Skill)

Run structured What-If scenario analysis with 4–6 branch possibility exploration (best, likely, worst, wild card, contrarian, second-order).

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (CC BY-NC-SA 4.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-29 |
| **Security** | caution · 2026-07-29 — provenance matches K-Dense-AI but page states CC BY-NC-SA 4.0 non-commercial while the collection root is MIT |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `what-if-oracle` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/what-if-oracle ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Run structured What-If scenario analysis with 4–6 branch possibility exploration (best, likely, worst, wild card, contrarian, second-order). Use when the user asks speculative what-if questions about uncertain futures, strategic forks, contingency planning, or stress-testing a decision before committing.

**Primary use cases**: the user asks speculative what-if questions about uncertain futures, strategic forks, contingency planning, or stress-testing a decision before committing.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: CC BY-NC-SA 4.0. The skill name to enable after install is `what-if-oracle`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/what-if-oracle/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/what-if-oracle/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=what-if-oracle&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fwhat-if-oracle.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
