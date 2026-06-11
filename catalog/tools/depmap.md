---
title: DepMap (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-06-04
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

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/genomics-bioinformatics/databases/depmap-crispr-essentiality` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `depmap` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/depmap ~/.claude/skills/
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
- [`skills/depmap/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/depmap/SKILL.md)
- [DepMap portal](https://depmap.org/portal/)
- [`broadinstitute/depmap-portal`](https://github.com/broadinstitute/depmap-portal)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=depmap&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdepmap.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
