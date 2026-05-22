---
title: gget (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology]
last_verified: 2026-05-21
summary: Claude skill wrapping the gget command-line / Python tool for fast unified queries against Ensembl, UniProt, NCBI, PDB, COSMIC, and other genomics databases.
---

# gget (Claude Skill)

Claude skill that teaches the gget unified API for querying 20+ genomics databases from a single Python or command-line interface.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS |
| **Capabilities** | Read-only — queries public databases via gget |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install gget@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/gget ~/.claude/skills/
  pip install gget
  ```

## What it does

Recipes for gget commands against:

- Ensembl — gene information, sequences, orthologs, variants
- UniProt — protein sequences and annotations
- NCBI — BLAST searches, gene information
- RCSB PDB — protein structures
- COSMIC — cancer mutations
- Other curated databases through a single Python/CLI interface

Includes batch-query support, pandas DataFrame integration, and result formatting.

**Primary use cases**: Quick gene lookups, sequence retrieval, variant annotation, orthology checks, protein structure access without per-database API setup.

## Notes

Useful when a workflow needs heterogeneous lookups (gene → sequence → ortholog → structure) without orchestrating separate database clients. For dedicated UniProt or PDB workflows, the standalone MCP servers expose more specialised tooling.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/gget/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/gget/SKILL.md)
- [gget documentation](https://pachterlab.github.io/gget/)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=gget&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgget.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
