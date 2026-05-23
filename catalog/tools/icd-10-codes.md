---
title: ICD-10 Codes MCP (Anthropic Healthcare)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-05-23
summary: Anthropic-published MCP server for ICD-10 diagnosis and procedure code lookup, sourced from CMS and CDC, for medical coding and claims workflows.
---

# ICD-10 Codes MCP

Anthropic-published MCP server distributed via the `anthropics/healthcare` plugin marketplace. Exposes the International Classification of Diseases, 10th Revision (ICD-10) — both **diagnosis** (ICD-10-CM) and **procedure** (ICD-10-PCS) codes — for medical coding, billing accuracy, and claims management. Underlying data is published by CMS and the CDC.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Anthropic](https://github.com/anthropics/healthcare) |
| **Availability** | GA — integrated into the marketplace per the `anthropics/healthcare` release history (PR #11) |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only — code lookups and validation |

## How to install

- **Claude Code** — plugin marketplace (recommended):

  ```
  /plugin marketplace add anthropics/healthcare
  claude mcp add-from-marketplace anthropics/healthcare/icd-10-codes
  ```

- **Claude Desktop** — proxy the marketplace MCP via `mcp-remote` if the upstream endpoint is HTTP; otherwise consult the marketplace `mcp.json` for the literal stdio command.

  **Registration form not exhaustively documented upstream — adapt the snippet to whatever the marketplace's `mcp.json` ships for this server.**

## What it does

Wraps ICD-10-CM and ICD-10-PCS code sets with MCP tools that let Claude:

- Look up a diagnosis or procedure code by ICD-10 identifier.
- Search the code set by clinical term, body system, or chapter.
- Validate a code's currency against the most recent CMS / CDC release.

**Primary use cases**: Medical coding QA, claims-validation pipelines, prior-authorization review (pairs with `prior-auth-review` skill and `cms-coverage` MCP), and reference lookup inside clinical-trial protocol drafting.

## Notes

ICD-10 is the US baseline; some payers also require ICD-10-CM modifiers and external-cause codes. This MCP covers the core code set — confirm payer-specific modifier requirements separately. Does not include CPT or HCPCS — those are governed by separate code sets.

## Sources

- [`anthropics/healthcare`](https://github.com/anthropics/healthcare)
- [Advancing Claude in healthcare and the life sciences](https://www.anthropic.com/news/healthcare-life-sciences)
- [CMS ICD-10 resources](https://www.cms.gov/medicare/coding-billing/icd-10-codes)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=icd-10-codes&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ficd-10-codes.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
