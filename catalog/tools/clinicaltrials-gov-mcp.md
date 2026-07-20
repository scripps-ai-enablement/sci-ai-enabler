---
title: ClinicalTrials.gov MCP Server (cyanheads)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: cyanheads (Casey Hand)
availability: GA
tool_categories: [Translational Medicine, Drug Repurposing and Discovery]
last_verified: 2026-06-28
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches cyanheads, GitHub Apache-2.0 active 2026-07 and npm clinicaltrialsgov-mcp-server v2.8.2 present, no OSV advisories"
summary: Apache-2.0 MCP server over the ClinicalTrials.gov v2 API — trial search, full study records, outcomes / adverse-event extraction, and patient-to-trial matching. Hosted public instance available.
---

# ClinicalTrials.gov MCP Server (cyanheads)

Community-maintained MCP server wrapping the ClinicalTrials.gov v2 API. Supports full-text trial search, complete study retrieval by NCT ID, extraction of outcomes / adverse events / participant flow from completed studies, and patient-to-trial matching against current recruiting trials.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [cyanheads (Casey Hand)](https://github.com/cyanheads/clinicaltrialsgov-mcp-server) |
| **Availability** | GA — distributed on npm as `clinicaltrialsgov-mcp-server` |
| **Pricing** | Free / OSS (Apache-2.0). No API key required; public hosted instance hosted on Cloudflare Workers free tier. |
| **Capabilities** | Read-only — ClinicalTrials.gov API queries; optional patient-matching tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches cyanheads, Apache-2.0, npm v2.8.2, no OSV advisories |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/structural-biology-drug-discovery/clinicaltrials-database-search` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code** — point at the hosted public instance (zero install):

  ```
  claude mcp add --transport http clinicaltrials https://clinicaltrials.caseyjhand.com/mcp
  ```

- **Claude Code** — local stdio via npx:

  ```
  claude mcp add-json clinicaltrialsgov-mcp-server '{"command":"npx","args":["-y","clinicaltrialsgov-mcp-server@latest"],"env":{"MCP_LOG_LEVEL":"info"}}'
  ```

- **Claude Desktop** — add to `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "clinicaltrialsgov-mcp-server": {
        "type": "stdio",
        "command": "bunx",
        "args": ["clinicaltrialsgov-mcp-server@latest"],
        "env": { "MCP_TRANSPORT_TYPE": "stdio" }
      }
    }
  }
  ```

  Or, to use the hosted endpoint from Claude Desktop (no native HTTP transport), proxy via `mcp-remote`:

  ```json
  {
    "mcpServers": {
      "clinicaltrials": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://clinicaltrials.caseyjhand.com/mcp"]
      }
    }
  }
  ```

## What it does

- **search_studies** — full-text search across studies with filters, pagination, sorting, and field selection.
- **get_study** — full record by NCT ID: protocol, eligibility, outcomes, arms, interventions, contacts, locations.
- **get_study_results** — outcomes, adverse events, participant flow, and baseline data from completed studies; optional summary mode reduces a ~200KB payload to ~5KB.
- **match_patient** — match patient demographics and conditions to eligible recruiting trials.

**Primary use cases**: Trial-eligibility screening, competitive landscaping for protocol drafting, adverse-event review across completed trials, patient-trial matching at point of care, and meta-analysis sourcing.

## Notes

The server works with defaults and no API keys. The hosted instance is convenient for evaluation; for production or PHI-adjacent workflows, self-host (local stdio or Cloudflare Workers deploy supported). Pluggable auth modes — `none`, `jwt`, `oauth` — are documented in the repo.

## Sources

- [`cyanheads/clinicaltrialsgov-mcp-server`](https://github.com/cyanheads/clinicaltrialsgov-mcp-server)
- [npm `clinicaltrialsgov-mcp-server`](https://www.npmjs.com/package/clinicaltrialsgov-mcp-server)
- [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/data-api/api)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=clinicaltrials-gov-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fclinicaltrials-gov-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
