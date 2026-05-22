---
title: AdisInsight Plugin
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Springer Nature
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-05-20
summary: Springer Nature AdisInsight MCP plugin surfacing drug-development pipeline, clinical-trial, and deal intelligence to Claude for repurposing and competitive scouting.
---

# AdisInsight Plugin

Anthropic-packaged Claude Code plugin that wraps Springer Nature's AdisInsight MCP server — a commercial drug-development-intelligence database covering global pipelines, clinical trials, and licensing deals.

| | |
|---|---|
| **Type** | Claude Code Plugin (wraps a remote MCP server) |
| **Supplier** | [Springer Nature](https://www.adisinsight.com/) (AdisInsight); plugin packaged by Anthropic |
| **Availability** | GA in the `life-sciences` marketplace (manifest v1.0.0) |
| **Pricing** | Commercial — requires an active AdisInsight subscription; plugin install is free |
| **Capabilities** | Read-only |

## How to install

```
/plugin marketplace add anthropics/life-sciences
/plugin install adisinsight@life-sciences
```

Direct MCP endpoint: `https://adisinsight-mcp.springer.com/mcp`.

## What it does

AdisInsight MCP tools cover drug-development pipeline queries, clinical-trial intelligence, and deal / licensing data across the AdisInsight database. Authentication uses an OAuth-style `authenticate` / `complete_authentication` flow on first use.

**Primary use cases**: Competitor pipeline scouting for repurposing candidates, drug-development stage tracking, deal / licensing landscape analysis.

## Notes

HTTP transport. Data access is gated by an AdisInsight subscription — verify your institution's entitlement before relying on this in a workflow. The plugin itself is free; the underlying data is the cost.

## Sources

- [`anthropics/life-sciences` marketplace manifest](https://github.com/anthropics/life-sciences/blob/main/.claude-plugin/marketplace.json)
- [AdisInsight plugin manifest](https://github.com/anthropics/life-sciences/blob/main/adisinsight/.claude-plugin/plugin.json)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=adisinsight&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fadisinsight.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
