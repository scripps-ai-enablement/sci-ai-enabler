---
title: ChEMBL Connector
parent: All tools
grand_parent: Catalog
tool_type: Claude Code Plugin
supplier: EMBL-EBI (Anthropic-packaged)
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-05-30
summary: Anthropic-packaged plugin and Claude.ai connector over EMBL-EBI's ChEMBL bioactive-compound database — compound, target, bioactivity, and mechanism-of-action lookup.
---

# ChEMBL Connector

Anthropic-packaged plugin and Claude.ai connector over **ChEMBL**, EMBL-EBI's manually curated database of bioactive compounds, biological targets, and quantitative activity measurements drawn from medicinal-chemistry literature.

| | |
|---|---|
| **Type** | Claude Code Plugin (wraps a remote MCP server) · Claude.ai Connector |
| **Supplier** | [EMBL-EBI ChEMBL](https://www.ebi.ac.uk/chembl/) (data); plugin packaged by Anthropic |
| **Availability** | GA in the `anthropics/life-sciences` marketplace; announced at J.P. Morgan 2026 (January 2026) |
| **Pricing** | Free / OSS (ChEMBL data CC-BY-SA-3.0) |
| **Capabilities** | Read-only |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install chembl@life-sciences
  ```
  Restart Claude Code, then `/mcp` to confirm the server is connected. If skills don't appear, `/reload-plugins`.
- **Claude.ai (Team / Enterprise)** — Admin settings → Connectors → Browse connectors → ChEMBL → **Add to your team**.
- **Claude.ai (individual)** — Settings → Connectors → ChEMBL → **Connect**.

## What it does

Six tool calls over the ChEMBL REST API:

- `compound_search` — find molecules by name, ChEMBL ID, or SMILES; returns molecular properties, synonyms, approval status, ATC codes
- `target_search` — query biological targets by name, gene symbol, or organism; returns protein accessions, GO annotations, UniProt cross-refs
- `get_bioactivity` — quantitative activity measurements (IC50, EC50, Ki, Kd) with assay descriptions, pChEMBL scores, and literature references
- `get_mechanism` — curated mechanism-of-action data for approved drugs
- Plus two further tools for cross-referencing and metadata lookup

**Primary use cases**: Medicinal-chemistry SAR analysis, target validation, polypharmacology and off-target screening, lead-compound optimisation against ChEMBL bioactivity data.

## Notes

Streamable HTTP transport — Claude Code uses the marketplace plugin entry directly; Claude.ai uses the managed connector. Replaces ad-hoc Augmented-Nature / iwatobipen community wrappers for users with marketplace access. ChEMBL data is updated quarterly by EMBL-EBI.

**Field report (2026-05-29)**: install via `/plugin marketplace add anthropics/life-sciences` then `/plugin install chembl@life-sciences` reported working without modification ([feedback #17](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/17)).

## Sources

- [Anthropic tutorial — Using the ChEMBL Connector in Claude](https://claude.com/resources/tutorials/using-the-chembl-connector-in-claude)
- [`anthropics/life-sciences` marketplace](https://github.com/anthropics/life-sciences)
- [Anthropic — Advancing Claude in healthcare and the life sciences](https://www.anthropic.com/news/healthcare-life-sciences)
- [ChEMBL — EMBL-EBI](https://www.ebi.ac.uk/chembl/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=chembl&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fchembl.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
