---
title: Morning (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Anthropic
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-07-17
claude_science: true
verification: degraded
verified_on: 2026-07-20
verification_note: "neither documented path resolves this run — anthropics/skills/skills has no morning dir and the claude.com Claude Science skills doc does not list Morning"
security: unknown
security_on: 2026-07-20
security_note: "first-party Anthropic org but the morning skill could not be located in anthropics/skills or the Claude Science doc this run so its manifest/permissions cannot be assessed"
summary: Anthropic 'morning brief' agent skill that assembles a daily briefing from the user's own calendar and mail connectors; used in Claude Science.
---

# Morning (Claude Skill)

Assembles a daily 'morning brief' from the user's calendar and mail connectors, as an Anthropic agent skill offered in Claude Science.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Anthropic agent skill |
| **Pricing** | Anthropic proprietary / example skill |
| **Capabilities** | Read/Write — reads calendar/mail, renders a briefing |
| **Verified** | degraded · 2026-07-20 — skill not found in anthropics/skills or Claude Science doc this run |
| **Security** | unknown · 2026-07-20 — skill not locatable this run to assess |

## How to install

- **Claude Science** — available as the built-in **Morning** skill.
- **Claude Code** — also distributed in Anthropic's `anthropic-skills` plugin bundle (`anthropic-skills:morning`).

## What it does

Renders a daily briefing (schedule, messages, priorities) by pulling the user's own calendar and mail connectors. Not a science model — a general productivity skill that ships alongside the Claude Science research skills.

**Primary use cases**: Daily briefing, schedule/mail triage, start-of-day summary

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

General-purpose (not a science model); listed here because it is one of the skills bundled in Claude Science. Uses the user's own connectors.

## Sources

- [anthropic-skills (morning)](https://github.com/anthropics/skills)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=morning&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmorning.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
