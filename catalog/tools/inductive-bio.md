---
title: Inductive Bio ADMET Connector
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Inductive Bio
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-07-04
summary: Claude.ai connector surfacing Inductive Bio's ADMET prediction models so drug-discovery chemists can predict compound properties in-conversation.
verification: degraded
verified_on: 2026-07-20
verification_note: "launch as an MCP connector in Anthropic's life-sciences ecosystem confirmed via cited PR Newswire release (2026-06-30); no public MCP endpoint or self-serve sign-up, so install path and tool list cannot be functionally resolved"
security: cleared
security_on: 2026-07-20
security_note: "vendor connector in Anthropic's life-sciences ecosystem (provenance confirmed via press); read-only, enterprise-gated, per vendor submitted structures are not retained or used for training"
---

# Inductive Bio ADMET Connector

A Claude.ai connector that brings Inductive Bio's ADMET (Absorption, Distribution, Metabolism, Excretion, and Toxicity) prediction models into a Claude conversation so medicinal chemists can score compound designs alongside their reasoning.

| | |
|---|---|
| **Type** | Claude.ai Connector (MCP) |
| **Supplier** | [Inductive Bio](https://www.inductive.bio) |
| **Availability** | GA — joined Anthropic's Life Sciences connector ecosystem 2026-06-30 |
| **Pricing** | Enterprise (contact Inductive Bio) — no public self-serve tier |
| **Capabilities** | Read-only — submit chemical structures, receive ADMET property predictions |
| **Verified** | degraded · 2026-07-20 — launch confirmed via cited PR Newswire release; no public endpoint, so install path/tool list not functionally resolvable |
| **Security** | cleared · 2026-07-20 — vendor connector in Anthropic's life-sciences ecosystem (provenance confirmed); read-only, enterprise-gated, structures not retained per vendor |

## How to install

- **Claude.ai / Claude Science** — enable from the connector directory: **Settings → Connectors → Browse connectors**, find **Inductive Bio**, and follow the vendor authentication flow. Access requires an Inductive Bio account arranged with the vendor (Book a Demo at [inductive.bio](https://www.inductive.bio)).

**Access is vendor-gated —** Inductive Bio does not publish a public MCP endpoint URL or a self-serve sign-up; the connector is provisioned per organization. Contact Inductive Bio to obtain the enable path and credentials for your workspace.

## What it does

Exposes Inductive Bio's ADMET prediction models (marketed as the Beacon-1 model family) to Claude. Within a conversation you can:

- Submit chemical structures (e.g., SMILES) and get predicted ADMET properties — absorption, distribution, metabolism, excretion, and toxicity endpoints.
- Reason about the predictions alongside the rest of a compound-design rationale, iterating on structures in natural language.

Inductive Bio's ADMET models placed first among 370+ entries from large-pharma and AI teams in the OpenADMET-ExpansionRx blind challenge.

**Primary use cases**: ADMET property prediction, lead optimization, compound triage during medicinal-chemistry design.

## Notes

Data privacy: per the vendor, chemical structures submitted through Claude are not retained or used to train Inductive's models.

Because access is enterprise/contact-gated, there is no copy-pasteable `claude mcp add` snippet or public connector URL to verify; the install path is the directory toggle plus a vendor-provisioned account. The specific ADMET endpoints and the enumerated tool/property list are not published in the launch materials — treat the property coverage above as the vendor's general description rather than a verified endpoint list. **Unverified —** exact tool names and per-endpoint coverage were not documented in a primary source at verification time.

## Sources

- [Inductive Bio joins Anthropic's Connector Ecosystem for Life Sciences (PR Newswire, 2026-06-30)](https://www.prnewswire.com/news-releases/inductive-bio-joins-anthropics-connector-ecosystem-for-life-sciences-surfacing-state-of-the-art-admet-prediction-to-drug-discovery-scientists-through-claude-302813935.html)
- [Inductive Bio Brings AI-Powered ADMET Prediction Models to Claude via New MCP Connector (BioPharma APAC)](https://biopharmaapac.com/news/32/8126/inductive-bio-brings-ai-powered-admet-prediction-models-to-claude-via-new-mcp-connector.html)
- [Inductive Bio](https://www.inductive.bio)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=inductive-bio&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Finductive-bio.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
