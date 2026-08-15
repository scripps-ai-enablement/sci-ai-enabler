---
title: Cortellis Plugin
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Clarivate
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-08-15
verification: degraded
verified_on: 2026-07-20
verification_note: "cortellis plugin dir confirmed in the anthropics/life-sciences marketplace repo, but the underlying Cortellis MCP data is behind a commercial Clarivate subscription so functional use is not verifiable without an entitled account"
security: caution
security_on: 2026-07-20
security_note: "provenance matches supplier Clarivate via the official marketplace, but closed-source commercial connector and Clarivate announced (Feb 2026) it is exploring a sale of its Life Sciences and Healthcare segment introducing ownership uncertainty"
summary: Clarivate Cortellis MCP plugin surfacing global drug-pipeline, clinical-trial, regulatory, safety, and deals intelligence to Claude for competitive scouting and regulatory work.
---

# Cortellis Plugin

Anthropic-packaged Claude Code plugin that wraps Clarivate's Cortellis MCP server — a commercial life-sciences intelligence platform covering global drug development pipelines, clinical trials, regulatory submissions, safety, and licensing deals.

| | |
|---|---|
| **Type** | Claude Code Plugin (wraps a remote MCP server) |
| **Supplier** | [Clarivate](https://clarivate.com/cortellis) (Cortellis); plugin packaged by Anthropic |
| **Availability** | GA in the `life-sciences` marketplace; Cortellis Regulatory Intelligence MCP announced March 10, 2026 |
| **Pricing** | Commercial — requires an active Cortellis subscription; plugin install is free |
| **Capabilities** | Read-only |
| **Verified** | degraded · 2026-07-20 — plugin resolves in anthropics/life-sciences but data is Clarivate-subscription-gated |
| **Security** | caution · 2026-07-20 — provenance matches Clarivate via official marketplace, closed-source, ownership uncertainty (Clarivate exploring LS&H sale) |

## How to install

```
/plugin marketplace add anthropics/life-sciences
/plugin install cortellis@life-sciences
```

After install, configure your Cortellis credentials when prompted (all `life-sciences` servers except PubMed require authentication).

## What it does

Cortellis MCP tools surface drug-development pipeline data, clinical-trial intelligence, regulatory submissions/approvals and guidance documents, drug-safety signals, and deal / licensing intelligence. The Cortellis Regulatory Intelligence (CRI) integration embeds authoritative, referenced regulatory content directly into Claude workflows, letting agents combine CRI with internal data.

**Primary use cases**: Competitive pipeline scouting for repurposing candidates, regulatory-submission research, drug-development stage tracking, deal / licensing landscape analysis.

## Notes

HTTP transport. Data access is gated by a Cortellis subscription — verify your institution's entitlement before relying on this in a workflow. The plugin itself is free; the underlying data is the cost. CRI MCP is available to customers who hold both Cortellis CRI and Claude subscriptions. Clarivate announced in February 2026 that it is exploring a sale of its Life Sciences & Healthcare segment, which introduces some uncertainty about Cortellis's long-term ownership.

## Sources

- [`anthropics/life-sciences` marketplace](https://github.com/anthropics/life-sciences)
- [Clarivate: Expands Access to Trusted Regulatory Intelligence Within Claude](https://clarivate.com/news/clarivate-expands-access-to-trusted-regulatory-intelligence-within-claude/)
- [Cortellis](https://clarivate.com/cortellis)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cortellis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcortellis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
