---
title: Specificity Annotation (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-25
summary: "Annotate TCR/BCR sequences against antigen-specificity databases and cluster by shared-specificity signal, treating matches as hypotheses with generation-probability nulls"
---

# Specificity Annotation (bioSkills)

A Claude Code skill that maps immune-receptor sequences to candidate antigen specificities and clusters repertoires by shared-specificity signal — explicitly treating database matches and cluster labels as hypotheses, not calls.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — the wrapped databases and tools (VDJdb, tcrdist3, OLGA, …) are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |

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
  cp -r bioSkills/tcr-bcr-analysis/specificity-annotation ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the referenced databases/tools when prompted on first use.

## What it does

Assigns candidate antigen specificity to TCR/BCR clonotypes and groups them into specificity clusters, with statistical guardrails to avoid over-interpretation:

- **Database annotation** — VDJdb, McPAS-TCR, IEDB, and TCRMatch, merging on CDR3 **plus** V-gene (never CDR3 alone), filtering to VDJdb confidence ≥1, and verifying donor HLA carriage.
- **Sequence clustering** — tcrdist3 meta-clonotypes (primary), GLIPH2, GIANA, clusTCR, iSMART, CoNGA; runs ≥2 independent methods and reports agreement plus the reference repertoire.
- **Generation-probability nulls** — OLGA (Pgen), IGoR, SONIA/soNNia (Ppost) to distinguish enrichment from convergent recombination.
- **ML predictors (optional)** — DeepTCR, ERGO-II, NetTCR-2.0, pMTnet, TITAN.
- **BCR support** — hands off to `immcantation-analysis` and `scirpy` for paired single-cell.

**Primary use cases**: antigen-specificity annotation of TCR/BCR repertoires, meta-clonotype clustering, generation-probability control for convergence claims.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-tcr-bcr-analysis-specificity-annotation`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/specificity-annotation`. The skill is deliberately conservative: database matches and cluster labels are reported as hypotheses with confidence levels, not definitive antigen assignments. Complements `mixcr-analysis`/`scirpy-analysis` (assembly), `repertoire-visualization` (figures), and `vdjtools-analysis` (diversity). Upstream directory: `tcr-bcr-analysis/specificity-annotation`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`tcr-bcr-analysis/specificity-annotation/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/specificity-annotation/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=specificity-annotation&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fspecificity-annotation.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
