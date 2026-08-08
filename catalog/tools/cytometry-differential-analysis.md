---
title: Cytometry Differential Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Tests cytometry clusters for differential abundance and differential state with diffcyt — sample-as-unit aggregation, design/contrast matrices, compositionality checks, BH FDR"
---

# Cytometry Differential Analysis (bioSkills)

A Claude Code skill that compares cell populations between experimental groups in flow and mass cytometry without the per-cell pseudoreplication that inflates significance.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — diffcyt, CATALYST, edgeR and limma are separately installed Bioconductor packages |
| **Capabilities** | Read/Write — Claude runs the skill's R workflow locally, not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "flow-cytometry"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/flow-cytometry/differential-analysis ~/.claude/skills/
  ```
  (run from inside the directory holding your clone — if you are still in `bioSkills/` from the previous step, use `cp -r flow-cytometry/differential-analysis ~/.claude/skills/`, or replace `bioSkills/` with the absolute path of your clone). Note the upstream directory is `differential-analysis`; this page is titled *Cytometry* Differential Analysis to distinguish it from the metagenomics [Differential Abundance](differential-abundance.html) skill. Install the Bioconductor packages when prompted on first use:
  ```
  R -e 'BiocManager::install(c("diffcyt","CATALYST","edgeR","limma"))'
  ```

## What it does

Splits the question into the two tests diffcyt distinguishes, and aggregates to the sample before testing either:

- **Differential abundance (DA)** — per-sample-per-cluster cell counts tested with edgeR, voom, or a GLMM.
- **Differential state (DS)** — per-sample-per-cluster arcsinh-median marker expression tested with limma or an LMM.
- **Design and contrast matrices** — built from the experimental metadata (condition, patient, batch, paired timepoints).
- **Compositional validation** — when a dominant population shifts, results are re-checked with simplex-aware methods (sccomp, scCODA, DCATS); cydar and CITRUS are covered as alternatives to cluster-based testing.

Stated rules:

| Rule | Value |
|---|---|
| Biological replicates per group | **≥2–3**, mandatory for a valid error term |
| Multiple testing | Benjamini-Hochberg FDR across clusters and across cluster × marker combinations |
| DS summary statistic | arcsinh-median per sample per cluster |

**Primary use cases**: comparing immune-cell frequencies between patient groups, detecting activation-state changes within a population, treatment-vs-control CyTOF cohort analysis.

## Notes

Four failure modes the skill guards against:

- **Per-cell pseudoreplication** — a Wilcoxon or t-test across all cells treats cells as independent samples and manufactures significance. Aggregate to sample-level summaries first.
- **Compositional artifacts** — one expanding population mechanically depletes the others' proportions, so an apparent decrease may be arithmetic. Validate with simplex-aware methods.
- **Batch handling** — model batch as a covariate in the design; do not normalize it out before testing.
- **No single-sample designs** — a design with one sample per condition has no error term and cannot be tested.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the R workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-flow-cytometry-differential-analysis`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/differential-analysis`. Upstream directory: `flow-cytometry/differential-analysis`.

Last step of the bioSkills flow-cytometry chain — it consumes clusters from [Clustering and Phenotyping](clustering-phenotyping.html) or populations from [Gating Analysis](gating-analysis.html), which in turn depend on [Compensation and Transformation](compensation-transformation.html) and [Cytometry QC](cytometry-qc.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`flow-cytometry/differential-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/differential-analysis/SKILL.md)
- [diffcyt (Bioconductor)](https://bioconductor.org/packages/diffcyt/)
- [Weber et al., *Communications Biology* 2:183 (2019) — diffcyt](https://doi.org/10.1038/s42003-019-0415-5)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cytometry-differential-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcytometry-differential-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
