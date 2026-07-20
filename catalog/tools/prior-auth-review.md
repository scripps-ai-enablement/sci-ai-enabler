---
title: prior-auth-review (Anthropic Healthcare Plugin)
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-07-12
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "first-party Anthropic plugin confirmed in anthropics/healthcare manifest (consolidated healthcare plugin + prior-auth skill dir) but repo has no top-level LICENSE and the skill reads/drafts clinical PA documents"
summary: Anthropic Claude Code skill (in the consolidated healthcare plugin) that reviews prior-authorization request documents and surfaces gaps against payer rules.
---

# prior-auth-review

Anthropic-published Claude Code plugin from the `anthropics/healthcare` marketplace. Reviews prior-authorization request bundles and surfaces missing documentation, miscoded items, and likely denial reasons before submission.

| | |
|---|---|
| **Type** | Claude Code Plugin |
| **Supplier** | [Anthropic](https://github.com/anthropics/healthcare) |
| **Availability** | GA |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write — reads PA documents, drafts a review summary |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — first-party Anthropic but no repo LICENSE; handles clinical PA documents |

## How to install

```
/plugin marketplace add anthropics/healthcare
/plugin install healthcare@healthcare
```

The standalone `prior-auth-review@healthcare` plugin is now **deprecated upstream** — the `anthropics/healthcare` marketplace has consolidated its skills into a single `healthcare` plugin. Install that and invoke this workflow as `/healthcare:prior-auth` (the skill directory is `prior-auth`, namespaced by the plugin — not a bare `/prior-auth`).

## What it does

A document-review workflow for prior-authorization requests: cross-checks supplied clinical documentation against payer criteria, surfaces missing items (ICD-10, CPT, labs, imaging, prior therapies), and drafts a structured review summary.

**Primary use cases**: Pre-submission QA of PA bundles, identifying denial-risk gaps before they reach the payer, structured triage for utilization-management teams.

## Notes

Pair with the `cms-coverage`, `icd10-codes`, and `npi-registry` plugins from the same `anthropics/healthcare` marketplace for end-to-end PA workflows. Verify payer-specific rules against current policy — the plugin encodes general patterns, not vendor-specific schemas.

## Sources

- [`anthropics/healthcare`](https://github.com/anthropics/healthcare)
- [Marketplace manifest](https://raw.githubusercontent.com/anthropics/healthcare/main/.claude-plugin/marketplace.json)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=prior-auth-review&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fprior-auth-review.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
