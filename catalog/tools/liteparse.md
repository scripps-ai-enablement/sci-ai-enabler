---
title: LiteParse (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-06-04
summary: Local document and PDF parsing with spatial text and bounding boxes.
---

# LiteParse (Claude Skill)

Local document and PDF parsing with spatial text and bounding boxes.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (Apache-2.0) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `liteparse` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/liteparse ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Local document and PDF parsing with spatial text and bounding boxes. Use for extracting text from PDFs, DOCX, Office files, and images; OCR on scans; layout-preserved JSON for RAG; batch-ingesting paper folders; or page screenshots for multimodal agents — even when the user does not name liteparse. Prefer over MarkItDown when you need bboxes, fast local parsing, or PNG page renders; prefer over the pdf skill for merge/split/forms.

**Primary use cases**: extracting text from PDFs, DOCX, Office files, and images; OCR on scans; layout-preserved JSON for RAG; batch-ingesting paper folders; or page screenshots for multimodal agents — even when the user does not name liteparse.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: Apache-2.0. The skill name to enable after install is `liteparse`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/liteparse/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/liteparse/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=liteparse&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fliteparse.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
