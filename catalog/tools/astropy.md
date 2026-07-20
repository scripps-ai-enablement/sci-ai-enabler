---
title: Astropy (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-20
verification_note: "repo and skills/astropy dir resolve on K-Dense-AI/scientific-agent-skills"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT repo wrapping BSD-3 Astropy, maintained (pushed 2026-07-15), no OSV advisories"
summary: Core Python library for astronomy and astrophysics workflows that need Astropy APIs, including units/quantities, coordinates, FITS I/O, tables, time systems, WCS, and cosmology.
---

# Astropy (Claude Skill)

Core Python library for astronomy and astrophysics workflows that need Astropy APIs, including units/quantities, coordinates, FITS I/O, tables, time systems, WCS, and cosmology.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (BSD-3-Clause) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches K-Dense-AI, MIT repo, maintained, no OSV advisories |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/scientific-computing/astropy-astronomy` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `astropy` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/astropy ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Core Python library for astronomy and astrophysics workflows that need Astropy APIs, including units/quantities, coordinates, FITS I/O, tables, time systems, WCS, and cosmology. Use when implementing or debugging astronomical data analysis code with Astropy.

**Primary use cases**: implementing or debugging astronomical data analysis code with Astropy.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: BSD-3-Clause. The skill name to enable after install is `astropy`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/astropy/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/astropy/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=astropy&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fastropy.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
