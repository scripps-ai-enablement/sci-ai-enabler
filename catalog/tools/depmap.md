---
title: DepMap (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-05-21
summary: Claude skill for querying the Cancer Dependency Map — CRISPR Chronos gene-effect scores, PRISM drug sensitivity, mutation, expression, and CN data across cancer cell lines.
---

# DepMap (Claude Skill)

Claude skill for working with the Broad Institute's Cancer Dependency Map data — genome-wide CRISPR knockout screens, RNAi, and compound-sensitivity assays across hundreds of cancer cell lines.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS skill; underlying DepMap data is publicly licensed |
| **Capabilities** | Read-only — pulls and analyses public DepMap files |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install depmap@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/depmap ~/.claude/skills/
  ```

## What it does

- Identifies cancer cell lines by DepMap ID (cell-line names are ambiguous)
- Downloads and analyses standard DepMap files locally: `CRISPRGeneEffect.csv`, `OmicsExpressionProteinCodingGenesTPMLogp1.csv`, `OmicsSomaticMutationsMatrixDamaging.csv`, `OmicsCNGene.csv`, `sample_info.csv`
- Computes biomarker associations with multiple-testing correction
- Adjusts for copy-number effects when interpreting essentiality scores

**Primary use cases**: Target validation (e.g., essentiality in KRAS-mutant lines), synthetic-lethal screening, biomarker discovery for oncology drug targets.

## Notes

References Behan et al. 2019 (Nature, PMID 30971826) and Dempster et al. 2021 (Nature Methods, PMID 34349281) for methodology. Pulls files from the [DepMap portal](https://depmap.org/portal/); large downloads are cached locally.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/depmap/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/depmap/SKILL.md)
- [DepMap portal](https://depmap.org/portal/)
- [`broadinstitute/depmap-portal`](https://github.com/broadinstitute/depmap-portal)
