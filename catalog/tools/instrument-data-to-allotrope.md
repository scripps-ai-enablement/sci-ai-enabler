---
title: instrument-data-to-allotrope
parent: All tools
grand_parent: Catalog
nav_order: 6
tool_type: Claude Skill
supplier: Anthropic
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery, Immunology and Microbiology, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-05-19
summary: Converts 40+ lab-instrument output formats to Allotrope Simple Model JSON / CSV for LIMS and data-lake ingestion.
---

# instrument-data-to-allotrope

Parses lab-instrument output (PDF, CSV, Excel, TXT) and writes Allotrope Simple Model (ASM) JSON, flattened 2D CSV, and exportable Python parser code.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Anthropic](https://github.com/anthropics/life-sciences) |
| **Availability** | GA — distributed via `anthropics/life-sciences` marketplace alongside Claude for Life Sciences (Oct 2025) |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add anthropics/life-sciences
  /plugin install instrument-data-to-allotrope@life-sciences
  ```
- **Claude.ai** — **Settings → Capabilities → Skills → Upload skill**, using the skill bundle from the `anthropics/life-sciences` repo.

## What it does

Instrument auto-detection, native parsing via the `allotropy` library with flexible/PDF-table fallback, ASM JSON emission, flattened-CSV emission, ASM validation with strict mode, exportable Python parser code.

**Primary use cases**: Standardising 40+ instrument types (cell counters, spectrophotometers, plate readers, qPCR, chromatography) for LIMS ingestion, data-lake loading, and downstream analysis.

## Notes

Depends on `pip install allotropy`. Falls back to a flexible parser or PDF table extraction when native parsing fails, with reduced metadata completeness reported. Also bundled in the Anthropic `bio-research` plugin.

## Sources

- [Skill listing (playbooks)](https://playbooks.com/skills/anthropics/life-sciences/instrument-data-to-allotrope)
- [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences)
- [Allotrope ASM overview](https://www.allotrope.org/asm)
