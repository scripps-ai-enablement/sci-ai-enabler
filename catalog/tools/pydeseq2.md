---
title: PyDESeq2 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-05-21
summary: Claude skill for bulk RNA-seq differential expression with PyDESeq2 — size factors, dispersion, Wald / LRT testing, BH-adjusted p-values.
---

# PyDESeq2 (Claude Skill)

Claude skill guiding bulk RNA-seq differential expression analysis with PyDESeq2, the Python reimplementation of DESeq2's negative-binomial GLM workflow.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write — Claude executes PyDESeq2 via Python/Bash |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install pydeseq2@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/pydeseq2 ~/.claude/skills/
  pip install pydeseq2
  ```

## What it does

Recipes covering:

- Size-factor estimation for library-size normalisation
- Dispersion estimation and shrinkage
- Wald test and likelihood ratio test for differential expression
- Benjamini–Hochberg FDR correction, filtering, and ranking of results
- Multi-factor designs, batch effects, and replicate handling
- Producing log2 fold-change estimates, p-values, and adjusted p-values per gene as a pandas DataFrame

**Primary use cases**: Bulk RNA-seq DE between conditions, biomarker discovery, batch-corrected expression studies, downstream input to enrichment workflows.

## Notes

Pairs with the AnnData and Scanpy skills for end-to-end transcriptomics. For pseudobulk single-cell DE, combine with Scanpy/Scanpy-MCP to aggregate counts before passing to PyDESeq2.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/pydeseq2/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/pydeseq2/SKILL.md)
- [PyDESeq2 documentation](https://pydeseq2.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pydeseq2&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpydeseq2.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
