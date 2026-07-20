---
title: Indication Dossier (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Anthropic
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-07-17
claude_science: true
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "first-party Anthropic; listed by name as a featured Claude Science skill in the claude.com connectors-and-skills doc fetched this run, orchestrates existing connectors with no extra credentials"
summary: Anthropic agent skill that compiles an indication/target dossier by orchestrating Claude Science connectors (Open Targets, ClinicalTrials, literature).
---

# Indication Dossier (Claude Skill)

Compiles a structured drug-indication dossier by orchestrating Claude Science data connectors, as an Anthropic agent skill.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Anthropic](https://claude.com/docs/claude-science/connectors-and-skills) |
| **Availability** | GA — Claude Science agent skill |
| **Pricing** | Anthropic proprietary — included with Claude Science |
| **Capabilities** | Read/Write — synthesizes a dossier document from connector queries |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — first-party Anthropic, confirmed in Claude Science doc, no extra credentials |

## How to install

- **Claude Science** — enable the built-in **Indication Dossier** agent skill. It is an Anthropic workflow skill available inside Claude Science and is not published as a standalone package.
- **No standalone install** — it orchestrates other connectors rather than shipping its own model or MCP server.

## What it does

Runs an agentic workflow that pulls target–disease associations (Open Targets), clinical-trial activity (ClinicalTrials.gov), and literature evidence, then assembles a structured indication/target dossier. Has no model API of its own — it composes the underlying Claude Science connectors.

**Primary use cases**: Indication assessment, target dossier assembly, competitive/landscape synthesis

## Notes

**Claude Science:** Featured as a research skill in Anthropic's **Claude Science**. Its inclusion there is an independent signal of quality and trustworthiness for life-science work.

Anthropic proprietary; available only inside Claude Science. Depends on the connectors it orchestrates (e.g., [Open Targets](open-targets.html), clinical-trials, literature).

## Sources

- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=indication-dossier&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Findication-dossier.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
