---
title: Procedure Coding (Anthropic Healthcare Plugin)
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
security_note: "first-party anthropics/healthcare, procedure-coding skill dir confirmed via contents API, but repo has no top-level LICENSE despite Free/OSS claim"
summary: Anthropic Claude skill that converts a clinical encounter's documentation into claim-ready CPT and HCPCS Level II procedure codes the way a professional coder would.
---

# Procedure Coding (Anthropic Healthcare Plugin)

Anthropic-published skill from the `anthropics/healthcare` plugin marketplace that abstracts billable services from encounter documentation and assigns CPT and HCPCS Level II codes.

| | |
|---|---|
| **Type** | Claude Skill (shipped inside the `healthcare` Claude Code plugin) |
| **Supplier** | [Anthropic](https://github.com/anthropics/healthcare) |
| **Availability** | GA |
| **Pricing** | Free / OSS — provided under Anthropic's terms of service |
| **Capabilities** | Read/Write — reads clinical notes, emits assigned procedure codes |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — first-party Anthropic, skill dir confirmed, but repo has no LICENSE |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/healthcare
  /plugin install healthcare@healthcare
  ```
  The `procedure-coding` skill is bundled inside the consolidated `healthcare` plugin (the older standalone plugins are now deprecated in favor of `healthcare@healthcare`). Invoke it as `/healthcare:procedure-coding` (namespaced by the plugin — not a bare `/procedure-coding`).
- **Claude.ai / Claude Desktop** — the healthcare plugin's skills load wherever the marketplace plugin is enabled.

## What it does

Transforms a single encounter's clinical notes into the procedure codes needed for insurance claims. It identifies billable services across evaluation-and-management, ancillary services, procedures, labs, imaging, and medicine services, then assigns:

- **CPT codes** (five digits, or four digits + F for Category II tracking) — physician services, procedures, and quality measures.
- **HCPCS Level II codes** (letter + four digits) — supplies, devices, drugs, and services CPT does not cover.

It extracts visit type/complexity, procedures performed (from operative reports, not plans), lab tests with results, imaging by modality and body part, devices/implants consumed, drugs administered, observation hours, and documented preventive services. It explicitly excludes planned-but-unperformed services, prior results, bundled items, and (by default) Category II quality codes.

**Primary use cases**: Encounter coding QA, claim preparation, revenue-cycle support.

## Notes

Complements `icd10-cm` (diagnosis coding) — CPT/HCPCS govern procedures where ICD-10-CM governs diagnoses. Pairs with `prior-auth` and `fraud-detection` in the same `healthcare` plugin. Output is decision-support for a professional coder to review, not a substitute for one; confirm payer-specific bundling and modifier rules separately.

## Sources

- [`anthropics/healthcare`](https://github.com/anthropics/healthcare)
- [`plugins/healthcare/skills/procedure-coding/SKILL.md`](https://github.com/anthropics/healthcare/blob/main/plugins/healthcare/skills/procedure-coding/SKILL.md)
- [Marketplace manifest](https://raw.githubusercontent.com/anthropics/healthcare/main/.claude-plugin/marketplace.json)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=procedure-coding&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fprocedure-coding.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
