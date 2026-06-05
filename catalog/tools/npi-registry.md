---
title: NPI Registry MCP (Anthropic Healthcare)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Anthropic
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-05-30
summary: Anthropic-published MCP server over the CMS NPPES NPI Registry — validate, look up, and search US healthcare providers by National Provider Identifier.
---

# NPI Registry MCP

Anthropic-published MCP server distributed via the `anthropics/healthcare` plugin marketplace. Exposes the Centers for Medicare & Medicaid Services (CMS) **National Plan and Provider Enumeration System (NPPES)** NPI Registry API v2.1 — Claude can validate a 10-digit National Provider Identifier, look up the full provider record, or search providers by name, organization, location, or specialty.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Anthropic](https://github.com/anthropics/healthcare) |
| **Availability** | GA — shipped 2026-01 with the Claude for Healthcare launch |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only — provider validation, lookup, and search |

## How to install

- **Claude Code** — plugin marketplace (recommended):

  ```
  /plugin marketplace add anthropics/healthcare
  /plugin install npi-registry@healthcare
  ```

  Restart Claude Code, then `/mcp` to confirm the server is connected.

  Equivalent direct add (skips the marketplace install step):

  ```
  claude mcp add-from-marketplace anthropics/healthcare/npi-registry
  ```

- **Claude.ai** — Settings → Connectors → **NPI Registry** → **Connect**.

- **Claude Desktop** — proxy the marketplace MCP via `mcp-remote` if the upstream endpoint is HTTP; otherwise install the marketplace per the Anthropic Healthcare README and consult the per-server `mcp.json` for the literal stdio command.

  **Registration form not exhaustively documented upstream — adapt the snippet to whatever the marketplace's `mcp.json` ships for this server.**

## What it does

Wraps the NPPES NPI Registry API with MCP tools that let Claude:

- **`npi_validate`** — confirm an NPI number has valid format and passes the Luhn check-digit algorithm before doing a registry lookup.
- **`npi_lookup`** — retrieve the complete provider record for a specific NPI: legal name, credentials, taxonomy / specialty, practice locations, enumeration date, and entity type (individual vs. organization).
- **`npi_search`** — find providers by combinations of first / last name, organization name, location (city / state / ZIP), and specialty / taxonomy description; supports wildcards and name-alias expansion.

**Primary use cases**: Provider-credential verification before onboarding, contracting, or referral; provider discovery by specialty / location for network construction; clinical-trial investigator validation; revenue-cycle and prior-authorization workflows that need to confirm a billing or rendering provider. Pair with `cms-coverage`, `icd-10-codes`, and `prior-auth-review` for end-to-end prior-auth review.

## Notes

US-specific. The NPI is required under HIPAA for covered US healthcare providers; non-US clinicians and foreign trial sites are not in this registry. CMS publishes weekly NPPES updates — record currency depends on the upstream registry refresh cadence.

## Sources

- [Anthropic tutorial — Using the NPI Registry Connector in Claude](https://claude.com/resources/tutorials/using-the-npi-registry-connector-in-claude)
- [`anthropics/healthcare`](https://github.com/anthropics/healthcare)
- [Advancing Claude in healthcare and the life sciences](https://www.anthropic.com/news/healthcare-life-sciences)
- [CMS NPPES NPI Registry](https://npiregistry.cms.hhs.gov/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=npi-registry&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fnpi-registry.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
