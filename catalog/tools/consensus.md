---
title: Consensus Plugin
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Consensus
availability: GA
tool_categories: [All]
last_verified: 2026-06-07
verification: degraded
verified_on: 2026-07-20
verification_note: "install path resolves (consensus plugin in anthropics/life-sciences marketplace) but the MCP server needs a Consensus.app account so it is functionally unverifiable without a subscription"
security: cleared
security_on: 2026-07-20
security_note: "Anthropic-packaged plugin in the official anthropics/life-sciences marketplace; provenance matches Consensus.app supplier; read-only"
summary: Consensus.app MCP plugin bringing AI-powered scientific literature search and evidence synthesis into Claude across all research areas.
---

# Consensus Plugin

Anthropic-packaged Claude Code plugin that wraps the Consensus MCP server, bringing Consensus.app's AI-powered scientific search engine and evidence synthesis into Claude.

| | |
|---|---|
| **Type** | Claude Code Plugin (wraps a remote MCP server) |
| **Supplier** | [Consensus](https://consensus.app/); plugin packaged by Anthropic |
| **Availability** | GA in the `life-sciences` marketplace |
| **Pricing** | Requires a Consensus account (free tier available; paid tiers for higher usage); plugin install is free |
| **Capabilities** | Read-only |
| **Verified** | degraded · 2026-07-20 — resolves in anthropics/life-sciences but needs a Consensus.app account |
| **Security** | cleared · 2026-07-20 — Anthropic-packaged in official life-sciences marketplace, provenance matches Consensus.app |

## How to install

```
/plugin marketplace add anthropics/life-sciences
/plugin install consensus@life-sciences
```

After install, authenticate with your Consensus account when prompted (all `life-sciences` servers except PubMed require authentication).

## What it does

Consensus searches across peer-reviewed scientific literature and returns evidence-backed, citation-linked answers rather than raw keyword hits. Through the MCP plugin, Claude can run literature queries, retrieve supporting papers, and synthesize what the research consensus says on a question.

**Primary use cases**: Evidence synthesis, literature-grounded Q&A, finding supporting/contradicting studies for a claim, rapid background research across any life-science domain.

## Notes

HTTP transport. Requires a Consensus account; sign-in is completed on first use. Complementary to PubMed and other literature connectors — Consensus emphasizes synthesized, claim-level answers over raw citation retrieval.

## Sources

- [`anthropics/life-sciences` marketplace](https://github.com/anthropics/life-sciences)
- [Consensus](https://consensus.app/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=consensus&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fconsensus.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
