---
title: NeuroFlow
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: Stanislav Jiříček
availability: Beta
tool_categories: [Neuroscience]
last_verified: 2026-07-19
summary: End-to-end Claude Code plugin for neuroscience research — ideation, grant writing, experiment design, data analysis, computational brain modeling, and paper drafting.
---

# NeuroFlow

A Claude Code plugin that orchestrates a full neuroscience research project — from ideation and grant writing through experiment design, data preprocessing/analysis, computational brain modeling, and manuscript drafting — as a set of phase-aware slash commands.

| | |
|---|---|
| **Type** | Claude Code Plugin |
| **Supplier** | [Stanislav Jiříček](https://github.com/stanislavjiricek/neuroflow) (community, MIT) |
| **Availability** | Beta — v0.2.20 |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — runs slash-command workflows locally; bundles a literature-search MCP server |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add stanislavjiricek/neuroflow
  /plugin install neuroflow@neuroflow
  ```
  (The marketplace and the plugin are both named `neuroflow`, so the install target is `neuroflow@neuroflow`.)

After install, the commands resolve namespaced under the plugin — e.g. `/neuroflow:ideation`, `/neuroflow:grant-proposal`, `/neuroflow:brain-build` (not the bare `/ideation` form the upstream README lists). Run `/neuroflow:setup` first to save your GitHub username so the collaboration "flowie" handle is pre-filled on new projects.

The plugin integrates a bundled literature-search MCP (`paper-search-mcp-nodejs`, for bioRxiv/PubMed lookups) that Claude Code launches on demand as part of the plugin — no separate registration step.

## What it does

Provides 20+ phase-aware slash commands, each loading workflow guidance and relevant skills for that stage of a research project. Grouped by phase:

- **Ideation & planning** — `/neuroflow:ideation` (brainstorm a question, inline literature exploration, formalize into a project definition), `/neuroflow:interview`, `/neuroflow:phase`, `/neuroflow:preregistration`.
- **Funding & admin** — `/neuroflow:grant-proposal` (funder-adaptive drafting for NIH/ERC/Wellcome/GAČR with word-count tracking and review-criteria alignment), `/neuroflow:finance` (budget planning, expense logging, funder reporting).
- **Experiments & tools** — `/neuroflow:experiment`, `/neuroflow:tool-build`, `/neuroflow:tool-validate`, `/neuroflow:pipeline`.
- **Data** — `/neuroflow:data`, `/neuroflow:data-preprocess`, `/neuroflow:data-analyze` (with a BIDS support skill).
- **Computational modeling** — `/neuroflow:brain-build`, `/neuroflow:brain-optimize`, `/neuroflow:brain-run` for assembling and running computational brain models.
- **Writing & output** — `/neuroflow:paper`, `/neuroflow:review`, `/neuroflow:poster`, `/neuroflow:output`, `/neuroflow:autoresearch`.
- **Collaboration & meta** — `/neuroflow:notes`, `/neuroflow:meeting`, `/neuroflow:hive`, `/neuroflow:git`, `/neuroflow:flowie`, `/neuroflow:fails`, `/neuroflow:idk`.

Plus 30+ supporting skills covering phase guidance, wiki crystallization (auto-ingesting decisions/hypotheses/insights at the end of each command), and worker-critic review loops.

**Primary use cases**: end-to-end neuroscience project orchestration, grant-proposal drafting, computational brain-model building, experiment-to-manuscript workflow.

## Notes

Community/independent project; not vendor-affiliated. Early-stage (v0.2.x) — treat as Beta. As with any third-party plugin, review the marketplace source before installing; Anthropic does not vet plugin contents. The bundled literature-search MCP overlaps dedicated catalog entries ([PubMed](pubmed.html), [bioRxiv](biorxiv-database.html)) but is packaged here as part of the research workflow. For a standalone spike-train/electrophysiology skill suite see [SpikeLab](spikelab.html); for fMRI modeling see [NeuroSTORM](neurostorm.html).

## Sources

- [`stanislavjiricek/neuroflow` README](https://github.com/stanislavjiricek/neuroflow)
- [`stanislavjiricek/neuroflow` LICENSE (MIT)](https://github.com/stanislavjiricek/neuroflow/blob/main/LICENSE)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=neuroflow&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fneuroflow.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
