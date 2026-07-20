---
title: Fraud Detection (Anthropic Healthcare Plugin)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-07-12
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "first-party anthropics/healthcare, fraud-detection skill dir confirmed via contents API, but repo has no top-level LICENSE despite Free/OSS claim and skill reads/writes Medicare/Medicaid claims data"
summary: Anthropic Claude skill that screens Medicare/Medicaid claims for fraud, waste, and abuse, producing ranked, fully-cited investigation referrals for SIU teams.
---

# Fraud Detection (Anthropic Healthcare Plugin)

Anthropic-published skill from the `anthropics/healthcare` plugin marketplace that screens Medicare and Medicaid claims for fraud, waste, and abuse and produces ranked investigation referrals with full citations.

| | |
|---|---|
| **Type** | Claude Skill (shipped inside the `healthcare` Claude Code plugin) |
| **Supplier** | [Anthropic](https://github.com/anthropics/healthcare) |
| **Availability** | GA |
| **Pricing** | Free / OSS — provided under Anthropic's terms of service |
| **Capabilities** | Read/Write — reads a claims corpus, writes referral packets and a dashboard |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — first-party Anthropic, skill dir confirmed, but repo has no LICENSE and it handles claims data |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/healthcare
  /plugin install healthcare@healthcare
  ```
  The `fraud-detection` skill is bundled inside the consolidated `healthcare` plugin (the older standalone plugins are now deprecated in favor of `healthcare@healthcare`). Invoke it as `/healthcare:fraud-detection` (namespaced by the plugin — not a bare `/fraud-detection`).
- **Claude.ai / Claude Desktop** — the healthcare plugin's skills load wherever the marketplace plugin is enabled; the enrichment MCPs (ICD-10, NPI, CMS Coverage) are optional and connect over the hosted `hcls.mcp.claude.com` endpoints.

## What it does

Runs a three-tier claims-screening pipeline:

- **Deterministic detection** — rule-based screening of a claims corpus against public rulesets (NCCI MUE, OIG LEIE exclusions, CMS enrollment, Physician Fee Schedule).
- **Model adjudication** — the model narrates patterns and may dismiss or downgrade findings but never adds new allegations.
- **Synthesis** — generates investigator narratives with adversarial verification.

Input is a claims corpus in a DuckDB canonical six-table schema plus a quarter and line of business (Medicare / Medicaid); reference rulesets are fetched from CMS, OIG, and NLM and cached locally. Output is ranked referrals with per-provider HTML packets, an `index.html` dashboard, and an Excel export. A "citation-or-zero" gate requires every dollar and rule allegation to trace to a deterministic recompute, and findings are framed as "indicators consistent with [scheme]" rather than definitive fraud.

**Primary use cases**: Special Investigation Unit (SIU) referral generation, program-integrity screening, auditable claims review.

## Notes

Pairs with the `icd10-cm`, `procedure-coding`, and `prior-auth` skills and the ICD-10 / NPI Registry / CMS Coverage MCPs in the same `healthcare` plugin. Output is decision-support, not a legal determination — establishing intent is a downstream determination. Requires the caller to supply a claims corpus in the expected DuckDB schema.

## Sources

- [`anthropics/healthcare`](https://github.com/anthropics/healthcare)
- [`plugins/healthcare/skills/fraud-detection/SKILL.md`](https://github.com/anthropics/healthcare/blob/main/plugins/healthcare/skills/fraud-detection/SKILL.md)
- [Marketplace manifest](https://raw.githubusercontent.com/anthropics/healthcare/main/.claude-plugin/marketplace.json)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=fraud-detection&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ffraud-detection.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
