---
title: XLSX (Claude Skill)
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
security_note: "skills/xlsx/SKILL.md resolves in K-Dense-AI collection but LICENSE.txt is Anthropic PBC proprietary (all rights reserved, no redistribution) — the MIT collection redistributes it, and the page's Free/OSS claim is inaccurate"
summary: Create, edit, analyze, or convert Excel spreadsheets (.xlsx, .xlsm) where the workbook file is the primary deliverable.
---

# XLSX (Claude Skill)

Create, edit, analyze, or convert Excel spreadsheets (.xlsx, .xlsm) where the workbook file is the primary deliverable.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (Proprietary..txt has complete terms) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — dir resolves but LICENSE.txt is Anthropic proprietary (all rights reserved), not the Free/OSS the page claims |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `xlsx` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/xlsx ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Create, edit, analyze, or convert Excel spreadsheets (.xlsx, .xlsm) where the workbook file is the primary deliverable. Use for formulas, formatting, financial models, multi-sheet workbooks, and tabular cleanup exported to Excel. Also applies to .csv/.tsv when the user wants spreadsheet output. Do NOT use for Word documents, HTML reports, standalone Python scripts, database pipelines, or Google Sheets API work.

**Primary use cases**: formulas, formatting, financial models, multi-sheet workbooks, and tabular cleanup exported to Excel.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: Proprietary..txt has complete terms. The skill name to enable after install is `xlsx`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/xlsx/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/xlsx/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=xlsx&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fxlsx.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
