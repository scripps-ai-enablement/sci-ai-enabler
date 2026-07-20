---
title: BGPT Paper Search (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [All]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-20
verification_note: "repo and skills/bgpt-paper-search dir resolve on K-Dense-AI/scientific-agent-skills"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT collection, maintained (pushed 2026-07-15), no OSV advisories"
summary: Search scientific papers and retrieve structured experimental data extracted from full-text studies via the BGPT MCP server.
---

# BGPT Paper Search (Claude Skill)

Search scientific papers and retrieve structured experimental data extracted from full-text studies via the BGPT MCP server.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches K-Dense-AI, MIT collection, maintained, no OSV advisories |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `bgpt-paper-search` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/bgpt-paper-search ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Search scientific papers and retrieve structured experimental data extracted from full-text studies via the BGPT MCP server. Returns 25+ fields per paper including methods, results, sample sizes, quality scores, and conclusions. Use for literature reviews, evidence synthesis, and finding experimental details not available in abstracts alone.

**Primary use cases**: literature reviews, evidence synthesis, and finding experimental details not available in abstracts alone.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill name to enable after install is `bgpt-paper-search`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/bgpt-paper-search/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/bgpt-paper-search/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=bgpt-paper-search&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbgpt-paper-search.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
