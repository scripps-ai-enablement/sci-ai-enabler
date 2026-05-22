---
title: scientific-problem-selection
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Anthropic
availability: GA
tool_categories: [All]
last_verified: 2026-05-20
summary: Structured framework for research project ideation, risk assessment, and troubleshooting, based on Fischbach & Walsh (Cell 2024).
---

# scientific-problem-selection

Guides Claude through a structured framework for evaluating research questions, based on Fischbach & Walsh's *Cell* (2024) framework for selecting tractable scientific problems.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Anthropic](https://github.com/anthropics/life-sciences) |
| **Availability** | GA — distributed via `anthropics/life-sciences` (Oct 2025) |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only — does not write files unless you ask Claude to summarise outputs to disk |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install scientific-problem-selection@life-sciences
  ```
- **Claude.ai** — **Settings → Capabilities → Skills → Upload skill**, using the skill bundle from the `anthropics/life-sciences` repo.

## What it does

Skill instructions encoding Fischbach & Walsh's *Cell* (2024) framework — covers project ideation, risk assessment, troubleshooting stuck projects, and strategic scientific planning.

**Primary use cases**: PI / postdoc project ideation, go/no-go decisions on lab projects, structured triage of competing research directions.

## Notes

Pure prompt-based skill — no external services or runtime dependencies. Applies to any life-science research planning conversation.

## Sources

- [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences)
- [Claude for Life Sciences announcement](https://www.anthropic.com/news/claude-for-life-sciences)
- [Fischbach & Walsh, *Cell* (2024)](https://www.cell.com/cell/fulltext/S0092-8674(24)00077-3)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=scientific-problem-selection&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fscientific-problem-selection.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
