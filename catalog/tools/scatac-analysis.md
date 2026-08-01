---
title: scATAC Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-01
summary: "Process single-cell ATAC-seq with Signac, ArchR or SnapATAC2 — fragment QC, TF-IDF/LSI, consensus peaks and chromVAR motif deviations"
---

# scATAC Analysis (bioSkills)

A Claude Code skill for single-cell ATAC-seq that covers fragment QC through consensus peak calling and transcription-factor motif scoring, with explicit guidance on the depth artefacts that dominate the assay.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — Signac, Seurat, ArchR, SnapATAC2, chromVAR, AMULET and TOBIAS are separately installed OSS |
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
  cp -r bioSkills/single-cell/scatac-analysis ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the R stack on first use (`Signac`, `Seurat`, `JASPAR2020`, `TFBSTools`, `motifmatchr`, `BSgenome.Hsapiens.UCSC.hg38`), or `pip install snapatac2` for the Python route.

## What it does

Six workflow stages over a fragments file:

1. **Fragment QC and matrix creation** — load fragments, compute TSS enrichment and nucleosome-signal metrics, filter cells.
2. **Dimensionality reduction** — TF-IDF peak reweighting followed by truncated SVD (LSI), with a diagnostic step for the first component's correlation with sequencing depth (usually discarded).
3. **Clustering and visualization** — neighbor graph and UMAP on the retained LSI dimensions.
4. **Consensus peak calling** — call peaks per cluster and merge into a single non-overlapping set, rather than using a whole-sample peak call that misses rare populations.
5. **Differential accessibility** — logistic-regression testing with depth as a covariate.
6. **Motif analysis** — chromVAR TF motif deviations scored against GC-matched background peak sets; TOBIAS for footprinting.

**Framework choice** — Signac 1.13+ with Seurat 5.0+ (R, the skill's default), ArchR 1.0+ (R, arrow-file-backed for large atlases), or SnapATAC2 2.x (Python; API still evolving). Doublets are handled with AMULET and scDblFinder, and the skill distinguishes homotypic from heterotypic cases. It also takes a position on whether to binarize the count matrix.

**Primary use cases**: chromatin-accessibility cell typing, cluster-specific regulatory element discovery, TF activity inference from motif deviations.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-single-cell-scatac-analysis` (`tool_type: r`, `primary_tool: Signac`); if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/scatac-analysis`. Depth is the recurring confounder — it contaminates LSI component 1, biases differential accessibility, and inflates motif deviation scores if the background is not GC-matched, and the skill flags each of these separately. Peak-level and motif-level follow-up connects to [MACS3](macs3-peak-calling.html), [HOMER](homer-motif-analysis.html), [JASPAR](jaspar-database.html) and [deepTools](deeptools.html). Upstream directory: `single-cell/scatac-analysis`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`single-cell/scatac-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/single-cell/scatac-analysis/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=scatac-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fscatac-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
