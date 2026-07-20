---
title: Medidata Connector
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Medidata Solutions
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-06-14
summary: Medidata's clinical-trial MCP connector — query platform documentation (Rave EDC, Data Connect) and predict high-enrollment trial sites during protocol planning.
verification: works
verified_on: 2026-07-20
verification_note: "listed as medidata in anthropics/life-sciences marketplace.json (confirmed); install path resolves to the published hosted endpoint mcp.imedidata.com/mcp; tool responses require an iMedidata login"
security: cleared
security_on: 2026-07-20
security_note: "official anthropics/life-sciences marketplace entry (provenance confirmed); vendor-hosted remote HTTP MCP, read-only, access gated by iMedidata account"
---

# Medidata Connector

Anthropic-listed connector wrapping Medidata's hosted MCP server, giving Claude two clinical-operations capabilities: querying Medidata platform documentation and predicting high-performing clinical-trial sites during protocol planning.

| | |
|---|---|
| **Type** | Claude.ai Connector / Claude Code Plugin (wraps a remote HTTP MCP server) |
| **Supplier** | [Medidata Solutions](https://www.medidata.com) (Dassault Systèmes) |
| **Availability** | GA in the `anthropics/life-sciences` marketplace |
| **Pricing** | Connector install is free; Predictive Site Ranking requires a Medidata Intelligent Trials subscription, Platform Help requires an iMedidata account |
| **Capabilities** | Read-only — documentation Q&A and site-ranking predictions |
| **Verified** | works · 2026-07-20 — provenance confirmed in anthropics/life-sciences marketplace; install path resolves to published endpoint mcp.imedidata.com/mcp (responses require iMedidata login) |
| **Security** | cleared · 2026-07-20 — official Anthropic marketplace entry; vendor-hosted remote HTTP MCP, read-only, access gated by iMedidata account |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install medidata@life-sciences
  ```
- **Claude Code** — direct MCP add: `claude mcp add --transport http medidata https://mcp.imedidata.com/mcp`
- **Claude.ai / Claude Desktop** — add a custom connector pointing at `https://mcp.imedidata.com/mcp` (Settings → Connectors → Add custom connector). Claude Desktop has no native HTTP transport, so register it via an `mcp-remote` proxy:
  ```
  claude mcp add medidata -- npx -y mcp-remote https://mcp.imedidata.com/mcp
  ```

Authenticate with your iMedidata credentials when prompted. The HTTP endpoint is a long-lived hosted service — you do not run a local process.

## What it does

Two services exposed over a single hosted MCP server:

- **Platform Help** — queries Medidata's Knowledge Hub documentation and FAQs for products such as Rave EDC, Data Connect, and Clinical Data Studio, so Claude can answer how-to questions about the platform and combine that with internal policies.
- **Predictive Site Ranking** — for Intelligent Trials customers, ranks clinical-trial sites by predicted enrollment performance during protocol/study planning, using aggregated historical operational, population/country, and standardized site data. Inputs include planned phase, indication, and study criteria; outputs include top-predicted sites, sites in the top performance percentiles, site addresses, and sites in countries of interest.

**Primary use cases**: Clinical-trial site-selection strategy, protocol planning, Medidata platform documentation Q&A.

## Notes

HTTP transport at `https://mcp.imedidata.com/mcp`. Platform Help is gated behind an iMedidata login (public viewers see limited content); Predictive Site Ranking is restricted to Medidata Intelligent Trials customers. Announced as part of Anthropic's Claude for Healthcare / Life Sciences expansion alongside new CMS and ClinicalTrials.gov connectors. Verify your institution's Medidata entitlement before relying on the site-ranking tools.

## Sources

- [`anthropics/life-sciences` marketplace](https://github.com/anthropics/life-sciences)
- [Using the Medidata Connector in Claude](https://claude.com/resources/tutorials/using-the-medidata-connector-in-claude)
- [Medidata: Clinical Trial Data with AI](https://www.medidata.com/en/clinical-trial-data-with-ai/)
- [Anthropic: Advancing Claude in healthcare and the life sciences](https://www.anthropic.com/news/healthcare-life-sciences)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=medidata&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmedidata.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
