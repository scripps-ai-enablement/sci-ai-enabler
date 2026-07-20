---
title: Pathway Enrichment (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT collection, skills/pathway-enrichment dir resolves, wraps gseapy/g:Profiler locally, no OSV advisories"
summary: Run pathway and gene-set enrichment analysis on gene lists or ranked gene data, then interpret the results.
---

# Pathway Enrichment (Claude Skill)

Run pathway and gene-set enrichment analysis on gene lists or ranked gene data, then interpret the results.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches K-Dense-AI, MIT collection, wraps gseapy/g:Profiler locally, no OSV advisories |

## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `pathway-enrichment` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/pathway-enrichment ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Run pathway and gene-set enrichment analysis on gene lists or ranked gene data, then interpret the results. Use whenever the user has a set of genes (differentially expressed genes from PyDESeq2/Scanpy, CRISPR-screen hits, cluster marker genes, proteomics hits) and wants to know which biological pathways, GO terms, or gene sets are over-represented or enriched. Covers over-representation analysis (ORA / Enrichr / Fisher / hypergeometric), ranked Gene Set Enrichment Analysis (GSEA / preranked), single-sample scoring (ssGSEA/GSVA), and functional profiling via gseapy, g:Profiler, Enrichr libraries, MSigDB, GO, KEGG, Reactome, and WikiPathways — plus gene-ID mapping, choosing the right background universe, multiple-testing correction, redundancy reduction, dotplots/enrichment maps, and publication-ready tables. Use this for "pathway analysis", "enrichment analysis", "GO enrichment", "KEGG/Reactome pathways", "GSEA", "over-representation", "functional annotation", or "what pathways are my genes in".

**Primary use cases**: Run pathway and gene-set enrichment analysis on gene lists or ranked gene data, then interpret the results.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill name to enable after install is `pathway-enrichment`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/pathway-enrichment/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/pathway-enrichment/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pathway-enrichment&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpathway-enrichment.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
