---
title: ISO 13485 Certification (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-20
verification_note: "repo and skills/iso-13485-certification dir resolve on K-Dense-AI/scientific-agent-skills"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT collection, maintained (pushed 2026-07-15), no OSV advisories"
summary: Comprehensive toolkit for preparing ISO 13485 certification documentation for medical device Quality Management Systems.
---

# ISO 13485 Certification (Claude Skill)

Comprehensive toolkit for preparing ISO 13485 certification documentation for medical device Quality Management Systems.

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
  Installs the K-Dense collection; enable the `iso-13485-certification` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/iso-13485-certification ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Comprehensive toolkit for preparing ISO 13485 certification documentation for medical device Quality Management Systems. Use when users need help with ISO 13485 QMS documentation, including (1) conducting gap analysis of existing documentation, (2) creating Quality Manuals, (3) developing required procedures and work instructions, (4) preparing Medical Device Files, (5) understanding ISO 13485 requirements, or (6) identifying missing documentation for medical device certification. Also use when users mention medical device regulations, QMS certification, FDA QMSR, EU MDR, or need help with quality system documentation.

**Primary use cases**: users need help with ISO 13485 QMS documentation, including (1) conducting gap analysis of existing documentation, (2) creating Quality Manuals, (3) developing required procedures and work instructions, (4) preparing Medical Device Files, (5) understanding ISO 13485 requirements, or (6) identifying missing documentation for medical device certification.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill name to enable after install is `iso-13485-certification`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/iso-13485-certification/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/iso-13485-certification/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=iso-13485-certification&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fiso-13485-certification.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
