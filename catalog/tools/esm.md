---
title: ESM (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Integrative Structural and Computational Biology]
last_verified: 2026-06-04
summary: Comprehensive toolkit for EvolutionaryScale protein language models including ESM3 (generative multimodal design across sequence, structure, and function) and ESM C (efficient embeddings).
---

# ESM (Claude Skill)

Comprehensive toolkit for EvolutionaryScale protein language models including ESM3 (generative multimodal design across sequence, structure, and function) and ESM C (efficient embeddings).

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/proteomics-protein-engineering/esm-protein-language-model` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `esm` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/esm ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Comprehensive toolkit for EvolutionaryScale protein language models including ESM3 (generative multimodal design across sequence, structure, and function) and ESM C (efficient embeddings). Use for protein sequence/structure/function tasks, inverse folding, embeddings, variant design, and ESMFold2 structure prediction via Biohub. Supports local open weights (Python 3.12, esm on PyPI) and cloud Forge/Biohub APIs with ESM_API_KEY authentication.

**Primary use cases**: protein sequence/structure/function tasks, inverse folding, embeddings, variant design, and ESMFold2 structure prediction via Biohub.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill name to enable after install is `esm`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/esm/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/esm/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=esm&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fesm.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
