---
title: Database Lookup (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [All]
last_verified: 2026-06-04
summary: Search 78 public scientific, biomedical, materials science, and economic databases via REST APIs.
---

# Database Lookup (Claude Skill)

Search 78 public scientific, biomedical, materials science, and economic databases via REST APIs.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS — license not stated upstream |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `database-lookup` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/database-lookup ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Search 78 public scientific, biomedical, materials science, and economic databases via REST APIs. Covers physics/astronomy (NASA, NIST, SDSS, SIMBAD), earth/environment (USGS, NOAA, EPA), chemistry/drugs (PubChem, ChEMBL, DrugBank, FDA, KEGG, ZINC, BindingDB), materials (Materials Project, COD), biology/genomics (Reactome, UniProt, STRING, Ensembl, NCBI Gene, GEO, GTEx, PDB, AlphaFold, InterPro, BioGRID, Gene Ontology, dbSNP, gnomAD, ENCODE, Human Protein Atlas, Human Cell Atlas), disease/clinical (COSMIC, Open Targets, ClinicalTrials.gov, OMIM, ClinVar, GDC/TCGA, cBioPortal, DisGeNET, GWAS Catalog), regulatory (FDA, USPTO, SEC EDGAR), economics/finance (FRED, World Bank, US Treasury), demographics (US Census, Eurostat, WHO). Use when looking up compounds, genes, proteins, pathways, variants, clinical trials, patents, economic indicators, or any public database API query.

**Primary use cases**: looking up compounds, genes, proteins, pathways, variants, clinical trials, patents, economic indicators, or any public database API query.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: not stated upstream. The skill name to enable after install is `database-lookup`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/database-lookup/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/database-lookup/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=database-lookup&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdatabase-lookup.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
