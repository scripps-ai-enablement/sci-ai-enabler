---
title: Revvity Signals AI Connector
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Revvity Signals Software
availability: GA
tool_categories: [All]
last_verified: 2026-07-04
summary: Claude.ai connector giving natural-language access to the Revvity Signals electronic lab notebook and connected R&D data.
verification: degraded
verified_on: 2026-07-20
verification_note: "listing in Anthropic's MCP connector directory confirmed via cited press coverage (CLP, 2026-07-01); no public MCP endpoint or self-serve sign-up, so install path and tool list cannot be functionally resolved"
security: cleared
security_on: 2026-07-20
security_note: "vendor connector in Anthropic's MCP directory (provenance confirmed via press); read-only, enterprise-gated behind a Revvity Signals account, no public endpoint"
---

# Revvity Signals AI Connector

A Claude.ai connector that lets researchers search and query the Revvity Signals electronic lab notebook (ELN) and connected R&D knowledge in natural language from within Claude.

| | |
|---|---|
| **Type** | Claude.ai Connector (MCP) |
| **Supplier** | [Revvity Signals Software](https://www.revvitysignals.com) |
| **Availability** | GA — joined Anthropic's MCP connector directory 2026-07-01 |
| **Pricing** | Enterprise — requires a Revvity Signals account (contact vendor) |
| **Capabilities** | Read-only — ELN search, research-data retrieval, R&D knowledge querying |
| **Verified** | degraded · 2026-07-20 — directory listing confirmed via cited press; no public endpoint, so install path/tool list not functionally resolvable |
| **Security** | cleared · 2026-07-20 — vendor connector in Anthropic's MCP directory (provenance confirmed); read-only, enterprise-gated, no public endpoint |

## How to install

- **Claude.ai / Claude Science** — enable from the connector directory: **Settings → Connectors → Browse connectors**, find **Revvity Signals AI**, and complete the vendor authentication flow. Access requires an existing Revvity Signals account.

**Access is vendor-gated —** the connector surfaces data governed by your Signals platform tenancy; there is no public MCP endpoint URL or self-serve sign-up. Contact Revvity Signals to provision access for your organization.

## What it does

Provides Claude secure, natural-language access to Signals' "intelligence layer" over connected R&D data:

- Electronic lab notebook (ELN) search across experiments and entries.
- Research-data retrieval with the ontology-driven scientific context managed in the Signals platform.
- Querying governed R&D knowledge to help search, understand, and act on complex data.

**Primary use cases**: ELN search, experimental-data retrieval, R&D knowledge querying.

## Notes

Extends Revvity's Signals AI agentic framework (embedded in the Signals One platform) out to scientists working in Claude. Data access is governed by the organization's Signals tenancy and ontology.

Because access is enterprise-gated, there is no copy-pasteable `claude mcp add` snippet or public connector URL to verify; the install path is the directory toggle plus a vendor-provisioned Signals account. **Unverified —** the enumerated tool/endpoint list was not published in a primary source at verification time.

## Sources

- [Revvity Connects Signals Research Platform to Anthropic Claude (Clinical Lab Products, 2026-07-01)](https://clpmag.com/lab-essentials/information-technology/middleware-software/revvity-connects-signals-research-platform-anthropic-claude/)
- [Revvity Expands Signals AI With Anthropic Claude Integration (Yahoo Finance)](https://finance.yahoo.com/technology/ai/articles/revvity-expands-signals-ai-anthropic-135700455.html)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=revvity-signals&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Frevvity-signals.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
