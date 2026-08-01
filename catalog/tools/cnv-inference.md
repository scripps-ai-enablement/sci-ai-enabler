---
title: CNV Inference (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-08-01
summary: "Infer chromosome-scale copy-number alterations from tumor scRNA-seq to separate malignant from normal cells and call subclones with inferCNV, copyKAT, Numbat and SCEVAN"
---

# CNV Inference (bioSkills)

A Claude Code skill that infers large-scale copy-number alterations from tumor single-cell or single-nucleus RNA-seq, so malignant cells can be told apart from normal ones without a matched DNA assay.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — inferCNV, copyKAT, Numbat and SCEVAN are separately installed OSS with their own licenses |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (R), not as an MCP tool |

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
  cp -r bioSkills/single-cell/cnv-inference ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the chosen inference package on first use: `BiocManager::install("infercnv")`, or the GitHub sources for copyKAT, Numbat and SCEVAN.

## What it does

Turns expression averaged over genomic windows into copy-number calls, then uses those calls to partition the dataset:

- **Method panel** — inferCNV 1.18+ (reference-based, HMM-smoothed), copyKAT 1.1+ and SCEVAN 1.0+ (reference-free), and Numbat 1.4+ (allele-aware, combining expression with phased SNP evidence for subclone resolution).
- **Workflow** — assemble a raw counts matrix, cell annotations, and a gene-order file with genomic coordinates; choose reference-based vs reference-free vs allele-aware; pick a normal reference (in-sample non-malignant cells preferred, sex-matched, with enough cells); smooth expression across genomic windows and apply the HMM for discrete states; call malignant cells by thresholding the CNV score or by subclustering, validating against lineage markers and allele evidence; refine subclones with Numbat where allelic information is available.
- **Parameter guidance** — inferCNV's `cutoff` is 0.1 for droplet data versus 1 for Smart-seq, because sparse droplet counts need a lower threshold; `HMM_type` i6 is the default six-state model.

**Primary use cases**: malignant-vs-normal cell separation in tumor scRNA-seq, aneuploidy and chromosome-arm CNV inference from expression, tumor subclone calling.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-single-cell-cnv-inference` (`tool_type: r`, `primary_tool: inferCNV`); if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/cnv-inference`. Expression-based CNV inference is an indirect measurement — a "CNV" signal can also arise from a strong regional expression program, which is why the skill insists on lineage-marker and allele cross-checks before a cell is labelled malignant. Reference-free methods avoid needing normal cells in the sample but are more sensitive to tumor purity. Pairs with [Single-cell RNA QC](single-cell-rna-qc.html) upstream and [cBioPortal](cbioportal.html) or [COSMIC](cosmic-database.html) for orthogonal bulk copy-number context. Upstream directory: `single-cell/cnv-inference`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`single-cell/cnv-inference/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/single-cell/cnv-inference/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cnv-inference&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcnv-inference.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
