---
title: ICD-10 Codes MCP (Anthropic Healthcare)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-07-12
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "first-party Anthropic plugin confirmed in anthropics/healthcare manifest and hosted endpoint reachable (405 to GET as expected), but repo has no top-level LICENSE despite Free/OSS claim"
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
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — first-party Anthropic, endpoint reachable, but no repo LICENSE |

## How to install

- **Claude Code** — plugin marketplace (recommended):

  ```
  /plugin marketplace add anthropics/healthcare
  /plugin install healthcare@healthcare
  ```

  The ICD-10 MCP now ships as one of the connected MCP servers inside the consolidated `healthcare` plugin (the older standalone `icd10-codes@healthcare` plugin is deprecated upstream). The server is a hosted HTTP endpoint at `https://hcls.mcp.claude.com/icd10_codes/mcp`.

- **Claude Code** — direct MCP add (without the plugin):

  ```
  claude mcp add --transport http icd10-codes https://hcls.mcp.claude.com/icd10_codes/mcp
  ```

- **Claude Desktop** — Desktop has no native HTTP transport; proxy the hosted endpoint via `mcp-remote`:

  ```json
  {
    "mcpServers": {
      "icd10-codes": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://hcls.mcp.claude.com/icd10_codes/mcp"]
      }
    }
  }
  ```

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

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=icd-10-codes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ficd-10-codes.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
