---
title: Research Lookup (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "provenance and MIT clear, but ships user PARALLEL_API_KEY to api.parallel.ai and OPENROUTER_API_KEY to openrouter.ai — query text leaves the machine to external paid services"
summary: Look up current research information using parallel-cli search (primary, fast web search), the Parallel Chat API (deep research), or Perplexity sonar-pro-search (academic paper searches).
---

# Research Lookup (Claude Skill)

Look up current research information using parallel-cli search (primary, fast web search), the Parallel Chat API (deep research), or Perplexity sonar-pro-search (academic paper searches).

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — MIT and provenance clear, but ships user API keys to external api.parallel.ai and openrouter.ai |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `research-lookup` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/research-lookup ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Look up current research information using parallel-cli search (primary, fast web search), the Parallel Chat API (deep research), or Perplexity sonar-pro-search (academic paper searches). Automatically routes queries to the best backend. Use for finding papers, gathering research data, and verifying scientific information. Note: query text is transmitted to api.parallel.ai (PARALLEL_API_KEY) and, for academic searches, to openrouter.ai (OPENROUTER_API_KEY).

**Primary use cases**: finding papers, gathering research data, and verifying scientific information.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill name to enable after install is `research-lookup`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/research-lookup/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/research-lookup/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=research-lookup&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fresearch-lookup.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
