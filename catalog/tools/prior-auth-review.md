---
title: prior-auth-review (Anthropic Healthcare Plugin)
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-05-20
summary: Anthropic Claude Code plugin that reviews prior-authorization request documents and surfaces gaps against payer rules.
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

## How to install

```
/plugin marketplace add anthropics/healthcare
/plugin install prior-auth-review@healthcare
```

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

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=prior-auth-review&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fprior-auth-review.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
