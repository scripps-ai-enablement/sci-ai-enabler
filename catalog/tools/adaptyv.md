---
title: Adaptyv (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Immunology and Microbiology, Integrative Structural and Computational Biology]
last_verified: 2026-06-04
summary: How to use the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results retrieval.
---

# Adaptyv (Claude Skill)

How to use the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results retrieval.

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
  Installs the K-Dense collection; enable the `adaptyv` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/adaptyv ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

How to use the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results retrieval. Use this skill whenever the user mentions Adaptyv, Foundry API, protein binding assays, protein screening experiments, BLI/SPR assays, thermostability assays, or wants to submit protein sequences for experimental characterization. Also trigger when code imports `adaptyv`, `adaptyv_sdk`, or `FoundryClient`, or references `foundry-api-public.adaptyvbio.com`.

**Primary use cases**: How to use the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results retrieval.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill name to enable after install is `adaptyv`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/adaptyv/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/adaptyv/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=adaptyv&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fadaptyv.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
