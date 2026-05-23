---
title: CMS Coverage MCP (Anthropic Healthcare)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-05-23
summary: Anthropic-published MCP server over the CMS Coverage Database — Local and National Coverage Determinations for Medicare prior-auth, appeals, and policy lookup.
---

# CMS Coverage MCP

Anthropic-published MCP server distributed via the `anthropics/healthcare` plugin marketplace. Exposes the Centers for Medicare & Medicaid Services (CMS) Coverage Database — both Local Coverage Determinations (LCDs) and National Coverage Determinations (NCDs) — to Claude for prior-authorization checks, appeals drafting, and Medicare policy lookup.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Anthropic](https://github.com/anthropics/healthcare) |
| **Availability** | GA — shipped 2026-01 with the Claude for Healthcare launch |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only — queries CMS coverage policy data |

## How to install

- **Claude Code** — plugin marketplace (recommended):

  ```
  /plugin marketplace add anthropics/healthcare
  claude mcp add-from-marketplace anthropics/healthcare/cms-coverage
  ```

- **Claude Desktop** — proxy the marketplace MCP via `mcp-remote` if the upstream endpoint is HTTP; otherwise install the marketplace per the Anthropic Healthcare README and consult the per-server `mcp.json` for the literal stdio command.

  **Registration form not exhaustively documented upstream — adapt the snippet to whatever the marketplace's `mcp.json` ships for this server.**

## What it does

Wraps the CMS Coverage Database with MCP tools that let Claude:

- Look up LCDs and NCDs by region, contractor, code, or condition.
- Verify locally-applicable Medicare coverage requirements ahead of a prior-authorization submission.
- Surface coverage gaps when drafting a claims appeal.

**Primary use cases**: Revenue-cycle teams checking coverage prior to claim submission; prior-authorization triage; payer-policy research; appeals-drafting workflows. Pair with `prior-auth-review` (skill) and `icd-10-codes` / `npi-registry` (MCPs) for end-to-end PA review.

## Notes

US-Medicare-specific. Does not cover Medicaid managed-care plans, commercial payers, or non-US health systems — for those, draft from payer-specific medical policy documents independently. Verify policy currency: CMS publishes updates on a rolling basis.

## Sources

- [`anthropics/healthcare`](https://github.com/anthropics/healthcare)
- [Advancing Claude in healthcare and the life sciences](https://www.anthropic.com/news/healthcare-life-sciences)
- [CMS Medicare Coverage Database](https://www.cms.gov/medicare-coverage-database/)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cms-coverage&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcms-coverage.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
