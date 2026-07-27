---
title: VDJtools Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-25
summary: "Compute depth-normalized TCR/BCR repertoire diversity (Hill profiles), overlap, clonality and segment usage with VDJtools/immunarch, with estimator and normalization guidance"
verification: works
verified_on: 2026-07-27
security: cleared
security_on: 2026-07-27
security_note: "provenance matches GPTomics/bioSkills, MIT, maintained (pushed 2026-07-25), no OSV advisories; VDJtools (Java) and immunarch (R) are separately-installed OSS"
---

# VDJtools Analysis (bioSkills)

A Claude Code skill that computes immune-repertoire diversity, clonal structure, overlap, and segment usage from clonotype tables, guiding the critical estimator and depth-normalization choices.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — VDJtools (Java) and immunarch (R) are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Java/R), not as an MCP tool |
| **Verified** | works · 2026-07-27 — GPTomics/bioSkills resolves; clone + copy install path current |
| **Security** | cleared · 2026-07-27 — provenance matches GPTomics/bioSkills, MIT, maintained, no OSV advisories |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "tcr-bcr-analysis"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/tcr-bcr-analysis/vdjtools-analysis ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install VDJtools (Java) and/or immunarch (R) when prompted on first use.

## What it does

Turns TCR/BCR clonotype tables into diversity, overlap, and usage statistics, with explicit warnings against depth-biased conclusions:

- **Tools** — VDJtools (Java CLI, v1.2.1+) and immunarch (R/tidyverse, v1.0+ equivalents).
- **Diversity** — `CalcDiversityStats`, `RarefactionPlot`; Hill profile at orders q=0 (richness / observedDiversity / chaoE), q=1 (Shannon-Wiener), q=2 (inverse Simpson, most depth-robust).
- **Overlap** — `CalcPairwiseDistances`, `OverlapPair`, `TrackClonotypes` with depth-robust metrics.
- **Segments** — `CalcSegmentUsage`, `CalcSpectratype`.
- **Conversion / prep** — `Convert` (from MiXCR/Adaptive/IMGT), `FilterNonFunctional`, `DownSample`.
- **Workflow** — prepare/convert → downsample to common depth → analyze (diversity/overlap/clonality) → visualize → interpret (condition public clonotypes on generation probability).

**Primary use cases**: repertoire diversity estimation, depth-normalized cross-sample overlap, V/J segment-usage and clonality quantification.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-tcr-bcr-analysis-vdjtools-analysis`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/vdjtools-analysis`. Upstream assembly is handled by `mixcr-analysis` (bulk) or `scirpy-analysis` (single-cell); figure rendering by `repertoire-visualization`; antigen-specificity by `specificity-annotation`. Upstream directory: `tcr-bcr-analysis/vdjtools-analysis`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`tcr-bcr-analysis/vdjtools-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/vdjtools-analysis/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=vdjtools-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fvdjtools-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
