---
title: bio-research (Claude Code Plugin)
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Anthropic
availability: GA
tool_categories: [All]
last_verified: 2026-05-20
summary: Umbrella plugin bundling 5 analysis skills and ~10 MCP connectors (PubMed, BioRender, ChEMBL, Synapse, Wiley, Open Targets, Benchling, etc.) for preclinical R&D.
---

# bio-research

Anthropic umbrella plugin bundling literature search, single-cell QC, sequencing-pipeline orchestration, drug-discovery lookups, and research-strategy skills behind a single `/bio-research:start` command.

| | |
|---|---|
| **Type** | Claude Code Plugin |
| **Supplier** | [Anthropic](https://github.com/anthropics/knowledge-work-plugins) |
| **Availability** | GA — open-sourced in `anthropics/knowledge-work-plugins`; also surfaced inside Claude Cowork |
| **Pricing** | Free / OSS — plugin itself is Apache 2.0; individual bundled connectors carry their own pricing (Benchling requires institutional access, BioRender Premium gates the full library, …) |
| **Capabilities** | Read/Write — end-to-end preclinical R&D in a single install |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/knowledge-work-plugins
  /plugin install bio-research@knowledge-work-plugins
  ```
  Then run `/bio-research:start` to enumerate the bundled tools. (Upstream README still shows the bare `/start`, but plugin skills must be invoked with the `plugin:skill` namespace.)
- **Claude.ai (Cowork)** — surfaces the same plugin contents via the Cowork plugin browser.

## What it does

Five analysis skills (Literature Review, Single-Cell Analysis, Sequencing Pipeline, Drug Discovery, Research Strategy) plus ~10 MCP connectors named in the plugin docs: PubMed, BioRender, bioRxiv, ClinicalTrials.gov, ChEMBL, Synapse, Wiley Scholar Gateway, Owkin, Open Targets, Benchling.

**Primary use cases**: End-to-end preclinical R&D in a single install — literature triage, scRNA-seq QC and integration, nf-core pipelines, target prioritisation, clinical-trial review, project-strategy framing.

## Notes

Each bundled connector authenticates independently (PubMed needs no auth; Benchling requires an institutional API token; BioRender / Wiley / Synapse use OAuth; Owkin / Open Targets / ChEMBL / bioRxiv / ClinicalTrials are read-only). A known issue (`anthropics/claude-code#40106`, March 2026) reports plugin-bundled MCP tools returning "Session not found" in Claude Code while working in Cowork — verify before relying on it for production workflows.

## Sources

- [bio-research plugin README](https://github.com/anthropics/knowledge-work-plugins/tree/main/bio-research)
- [knowledge-work-plugins repo](https://github.com/anthropics/knowledge-work-plugins)
- [DeepWiki: knowledge-work-plugins](https://deepwiki.com/anthropics/knowledge-work-plugins)
- [Issue #40106 (Session not found bug)](https://github.com/anthropics/claude-code/issues/40106)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=bio-research&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbio-research.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
