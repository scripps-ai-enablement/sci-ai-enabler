---
title: Hashtag Demultiplexing (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Assign pooled single-cell data back to sample of origin from HTO, MULTI-seq or CellPlex tags and call cross-sample doublets"
---

# Hashtag Demultiplexing (bioSkills)

A Claude Code skill for the step between a multiplexed 10x run and any per-sample analysis: assigning each cell to its sample of origin from hashtag counts, and calling the cross-sample doublets that hashing makes visible.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — Seurat, scanpy, pegasus, demuxmix and GMM-Demux are installed separately (all open source) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (R/Python), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "single-cell"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/single-cell/hashing-demultiplexing ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisite — the R path** (Seurat 5.0+ for HTODemux / MULTIseqDemux; demuxmix 1.4+ from Bioconductor):
  ```
  Rscript -e 'install.packages("Seurat", repos="https://cloud.r-project.org")'
  Rscript -e 'if (!requireNamespace("BiocManager", quietly=TRUE)) install.packages("BiocManager", repos="https://cloud.r-project.org"); BiocManager::install("demuxmix")'
  ```
- **Prerequisite — the Python path** (scanpy 1.10+ exposes hashsolo as `sc.external.pp.hashsolo`; pegasus 1.8+ provides demuxEM):
  ```
  pip install "scanpy>=1.10" "pegasuspy>=1.8"
  ```
- **Optional — GMM-Demux** (explicit multiplet accounting). **Unverified —** the skill lists GMM-Demux as a CLI tool without a version or install command; install from the upstream project ([`CHPGenetics/GMM-Demux`](https://github.com/CHPGenetics/GMM-Demux)) and confirm with `GMM-demux --help`. The Seurat and scanpy paths cover the workflow without it.

You do not need all five back-ends — pick the one the decision rules below point to and install only that stack.

## What it does

Runs the demultiplexing workflow end to end and, more usefully, picks the method:

- **Normalize** — centered log-ratio (CLR) transform of the HTO counts. Margin defaults to 1 (within-cell) in Seurat, but **margin=2** (across cells, per tag) is a common alternative for HTO/ADT because it corrects per-tag capture-efficiency differences.
- **Choose a method** — clean antibody HTO → **HTODemux** (fast, standard); MULTI-seq lipid tags → **MULTIseqDemux** with `autoThresh=TRUE`; weak or variable staining and nucleus hashing → **demuxmix** or **demuxEM**, both of which model background explicitly; few hashtags with many negatives → **hashsolo** (Bayesian); explicit multiplet accounting → **GMM-Demux**.
- **Call assignments** — classify every cell as singlet, cross-sample doublet, or negative.
- **Filter and validate** — extract singlets and cross-check against expression-based doublet detection.

Working parameters carried by the skill: HTODemux `positive.quantile = 0.99` (raise for fewer false singlets and more negatives, lower to rescue weak staining); demuxEM `min_signal = 10.0` (lower to rescue low-capture nucleus hashing); hashsolo priors `(0.01, 0.8, 0.19)` for negative/singlet/doublet, with the doublet prior tracking expected loading doublets at roughly **0.8% per 1,000 cells** on 10x.

**Primary use cases**: assigning pooled hashed cells back to their samples, calling cross-sample doublets, rescuing an oversized Negative pile.

## Notes

Two diagnostics do most of the work. A **huge Negative pile with few singlets** means weak staining or high ambient signal — the fix is to lower `positive.quantile`, switch to demuxEM (which estimates background from empty droplets), or use demuxmix (which brings RNA covariates into the model). Conversely, a **cross-sample doublet rate near zero while expression-based doublet detection flags many cells** means the hashing thresholds are too loose, not that the library is unusually clean.

Worth keeping straight: hashing only detects doublets formed between *different* samples, so it systematically misses same-sample doublets. That is the reason the skill insists on cross-checking against an expression-based caller rather than treating the hashing call as complete. Genetic demultiplexing (via SNPs) is the alternative the skill weighs against hashing when samples are genetically distinct.

Upstream skill front-matter name is `bio-single-cell-hashing-demultiplexing` (`tool_type: mixed`, `primary_tool: Seurat`); upstream directory `single-cell/hashing-demultiplexing`. Pairs with [Doublet Detection](doublet-detection.html) — the expression-based counterpart, and the page to read for the per-sample-before-integration rule — plus [Single-cell RNA QC](single-cell-rna-qc.html), [scanpy](scanpy.html), and [AnnData](anndata.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`single-cell/hashing-demultiplexing/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/single-cell/hashing-demultiplexing/SKILL.md)
- [Seurat hashing vignette](https://satijalab.org/seurat/articles/hashing_vignette)
- [demuxmix (Bioconductor)](https://bioconductor.org/packages/demuxmix)
- [Pegasus (demuxEM) documentation](https://pegasus.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=hashing-demultiplexing&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fhashing-demultiplexing.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
