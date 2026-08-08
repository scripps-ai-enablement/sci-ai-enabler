---
title: Clustering and Phenotyping (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Unsupervised cell-type discovery in high-dimensional cytometry with FlowSOM, PhenoGraph and CATALYST — type-vs-state markers, over-provision then metacluster, UMAP for display only"
---

# Clustering and Phenotyping (bioSkills)

A Claude Code skill that finds and annotates cell populations in high-parameter flow, spectral and mass cytometry data without drawing a manual gating hierarchy.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — CATALYST, FlowSOM, flowCore are separately installed Bioconductor packages; Rphenograph is GitHub-only |
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
  cp -r bioSkills/flow-cytometry/clustering-phenotyping ~/.claude/skills/
  ```
  (run from inside the directory holding your clone — if you are still in `bioSkills/` from the previous step, use `cp -r flow-cytometry/clustering-phenotyping ~/.claude/skills/`, or replace `bioSkills/` with the absolute path of your clone). Install the packages when prompted on first use:
  ```
  R -e 'BiocManager::install(c("CATALYST","FlowSOM","flowCore"))'
  R -e 'remotes::install_github("JinmiaoChenLab/Rphenograph")'
  ```
  (Rphenograph is not on CRAN or Bioconductor — it installs from GitHub, and it is optional if you only use FlowSOM.)

## What it does

Runs the CATALYST workflow end to end, with the marker-role distinction built in:

- **Data prep** — `prepData()` with a panel annotation that labels each channel a **type** marker (lineage) or a **state** marker (activation, phospho-epitope, proliferation).
- **Clustering** — `cluster()` (FlowSOM self-organizing map plus ConsensusClusterPlus metaclustering), or `Rphenograph()` for graph-based Louvain clustering — on type markers only.
- **Visualization** — `runDR()` for UMAP or t-SNE on a subsample.
- **Annotation** — median-expression heatmap review, then `mergeClusters()` with a curated cluster→population table.

Stated defaults and thresholds:

| Parameter | Value |
|---|---|
| FlowSOM SOM grid | 10×10 — deliberately over-provisioned relative to expected populations |
| `maxK` (metaclusters) | 20 default; raise when more populations are expected |
| Arcsinh cofactor | 5 for CyTOF; ~150 for fluorescence |
| Embedding subsample | 2,000 cells per sample |
| PhenoGraph `k` | 30 neighbors — the primary tuning parameter |

**Primary use cases**: unsupervised immunophenotyping of 20+ parameter panels, CyTOF cluster discovery and annotation, generating per-sample per-cluster inputs for differential testing.

## Notes

Three rules the skill treats as non-negotiable:

- **Never cluster on state markers.** Activation, phospho and Ki-67 channels are tested *within* clusters, not used to define them — otherwise the same lineage splits into activation states and abundance comparisons become uninterpretable.
- **Embeddings are for visualization only.** Do not gate on a UMAP or t-SNE, and do not measure distances in the embedding.
- **Over-provision, then metacluster.** Metaclustering can merge over-fine SOM nodes but cannot split a node that already merged two populations, so err toward too many nodes. Set the seed explicitly — FlowSOM and Louvain are stochastic.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the R workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-flow-cytometry-clustering-phenotyping`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/clustering-phenotyping`. Upstream directory: `flow-cytometry/clustering-phenotyping`.

Run after [Compensation and Transformation](compensation-transformation.html) and [Cytometry QC](cytometry-qc.html); the alternative population-definition route is [Gating Analysis](gating-analysis.html), and the cluster assignments feed [Cytometry Differential Analysis](cytometry-differential-analysis.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`flow-cytometry/clustering-phenotyping/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/clustering-phenotyping/SKILL.md)
- [CATALYST (Bioconductor)](https://bioconductor.org/packages/CATALYST/)
- [FlowSOM (Bioconductor)](https://bioconductor.org/packages/FlowSOM/)
- [Nowicka et al., *F1000Research* 6:748 (2017) — CyTOF workflow](https://doi.org/10.12688/f1000research.11622.4)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=clustering-phenotyping&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fclustering-phenotyping.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
