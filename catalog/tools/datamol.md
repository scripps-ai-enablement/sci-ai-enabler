---
title: Datamol (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Chemistry, Drug Repurposing and Discovery]
last_verified: 2026-05-25
summary: Claude skill wrapping Datamol — an RDKit-based Python library for molecular standardization, transformations, featurization, and parallel processing on large compound libraries.
---

# Datamol (Claude Skill)

Claude skill providing Python recipes for [Datamol](https://datamol.io/), an RDKit-built molecular-manipulation library optimised for drug-discovery pipelines (standardization, tautomer/stereoisomer enumeration, featurization, and pandas-friendly batch operations).

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill (MIT collection); Datamol itself is Apache-2.0 |
| **Capabilities** | Read/Write — Claude executes Datamol via the Bash/Python tool |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install datamol@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/datamol ~/.claude/skills/
  pip install datamol
  ```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- Molecular I/O (SMILES / SDF / MOL) and dataframe round-tripping
- Standardization and sanitization (charge, tautomer, stereochemistry)
- Molecular transformations (tautomer / stereoisomer enumeration)
- Featurization — descriptors, fingerprints, and graph representations
- Parallel processing for large compound libraries
- Reference datasets bundled in `references/reactions_data.md` (CDK2 kinase inhibitors, FreeSolv hydration free energies, RDKit solubility train/test splits)

**Primary use cases**: Compound-library cleanup and standardization for ML pipelines, analog generation in lead optimisation, large-scale molecular preprocessing, similarity searching.

## Notes

Skill is documentation plus Python recipes — Claude executes Datamol locally via Bash/Python. Sits alongside the catalog's `rdkit-skill` page in the same K-Dense marketplace; Datamol layers higher-level workflows (caching, dataframe integration, batch ops) on top of raw RDKit calls.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/datamol/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/datamol/SKILL.md)
- [Datamol library — datamol.io](https://datamol.io/)
- [`datamol-io/datamol`](https://github.com/datamol-io/datamol)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=datamol&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdatamol.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
