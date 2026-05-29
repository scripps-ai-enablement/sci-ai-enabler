---
title: Owkin Pathology Explorer Connector
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: Owkin
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-05-24
summary: Owkin's Pathology Explorer agent — H&E whole-slide image analysis, cell-type detection, and tumour-microenvironment profiling — exposed to Claude as a remote MCP connector.
---

# Owkin Pathology Explorer Connector

Remote MCP connector for **Pathology Explorer**, Owkin's specialised biological AI agent that turns H&E pathology slides (TCGA cohorts and partner data) into queryable insights for drug discovery, clinical research, and tumour-microenvironment analysis.

| | |
|---|---|
| **Type** | Claude.ai Connector (remote MCP); also referenced from `anthropics/life-sciences` |
| **Supplier** | [Owkin](https://www.owkin.com/) |
| **Availability** | GA — launched 2026-01-12 with Claude for Healthcare and Life Sciences |
| **Pricing** | Owkin account / subscription required (contact Owkin); free for evaluation per their docs |
| **Capabilities** | Read-only — runs Owkin's proprietary models on referenced whole-slide images and returns structured results plus image previews |

## How to install

- **Claude.ai** — Settings → **Connectors** → search for **Owkin** → **Connect**, then authenticate with an Owkin account. Organisation admins can add it via Admin settings → Connectors → Browse connectors → Owkin → **Add to your team**.
- **Claude Code** — direct MCP add against Owkin's hosted endpoint:
  ```
  claude mcp add --transport http owkin <Owkin MCP endpoint from your Owkin account dashboard>
  ```
  **Unverified —** the exact endpoint URL is gated behind Owkin's MCP Server Documentation; consult that page after signing in for the canonical URL and any required auth header.
- **Claude Desktop** — install via the Owkin connector tutorial linked under Sources; the Owkin docs walk through pasting the remote MCP URL into the desktop connector pane.

## What it does

- Cell-type and tissue-type detection across whole-slide H&E images
- Spatial analysis of six distinct cell types (including understudied populations like neutrophils and eosinophils) and their organisation within the tumour microenvironment
- Whole-slide image retrieval and visualisation directly inside the Claude chat surface
- Cohort-level survival analysis tied to extracted image biomarkers — designed for hypothesis generation and validation against TCGA and Owkin's hospital-network cohorts

**Primary use cases**: Pathology-driven target and biomarker discovery, immunotherapy-response stratification (e.g., low-infiltration LUAD cohorts), spatial-biology hypothesis testing, clinical-trial cohort design.

## Notes

First highly specialised biological agent trained primarily on multimodal patient data made available via MCP. Backed by Owkin's federated network spanning 800+ hospitals across 104 healthcare centres. Outputs are intended for research use; not a regulated diagnostic.

## Sources

- [Anthropic tutorial — Using the Owkin Connector in Claude](https://claude.com/resources/tutorials/using-the-owkin-connector-in-claude)
- [Owkin press release — Pathology Explorer launches with Claude (2026-01-12)](https://www.owkin.com/newsfeed/owkins-specialized-biological-ai-agent-pathology-explorer-launches-with-anthropics-claude-for-healthcare-and-life-sciences)
- [Anthropic — Advancing Claude in healthcare and the life sciences](https://www.anthropic.com/news/healthcare-life-sciences)
- [`anthropics/life-sciences` marketplace](https://github.com/anthropics/life-sciences)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=owkin&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fowkin.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
