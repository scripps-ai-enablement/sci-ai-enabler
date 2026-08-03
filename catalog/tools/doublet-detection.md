---
title: Doublet Detection (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-01
summary: "Flag and remove droplets containing two or more cells in single-cell RNA-seq using scDblFinder, Scrublet and DoubletFinder before clustering"
verification: works
verified_on: 2026-08-03
reviewed_on: 2026-08-03
security: cleared
security_on: 2026-08-03
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.1k stars, skill dir current"
---

# Doublet Detection (bioSkills)

A Claude Code skill that identifies multi-cell droplets in single-cell RNA-seq before they are mistaken for real intermediate or transitional cell states.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — scDblFinder, Scrublet, DoubletFinder, Seurat and scanpy are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (R/Python), not as an MCP tool |
| **Verified** | works · 2026-08-03 |
| **Security** | cleared · 2026-08-03 — GPTomics/bioSkills MIT confirmed, provenance matches, no advisories |

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
  cp -r bioSkills/single-cell/doublet-detection ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the chosen detector on first use: `BiocManager::install("scDblFinder")` in R, or use the Scrublet implementation bundled with scanpy in Python.

## What it does

Runs simulate-and-score doublet detection per sample and helps decide what to do with the calls:

- **Method panel** — scDblFinder 1.16+ (R, the collection's recommended 2024–2026 default), Scrublet via scanpy 1.10+ (Python), and DoubletFinder (R, current release — the `*_v3` function suffixes were removed after November 2023). Works alongside Seurat 5.0+ / `SingleCellExperiment` objects.
- **Workflow** — detect **per sample on raw counts after basic QC and before integration or clustering**; set the expected doublet rate from recovered-cell counts (~0.8% per 1,000 cells, i.e. `dbr.per1k = 0.008`); apply a homotypic adjustment (`modelHomotypic()`) to discount same-cell-type pairs that scoring cannot see; tune the cutoff when a Scrublet score histogram is not bimodal; and flag-and-inspect rather than deleting blindly.
- **Design rules the skill encodes** — for multiplexed pools the expected rate comes from the **total lane** cell count, not the demultiplexed subset, otherwise doublets are systematically underestimated.

**Primary use cases**: single-cell QC before clustering, ruling out artefactual "intermediate" populations, per-sample cleanup ahead of multi-sample integration.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-single-cell-doublet-detection` and it declares `tool_type: mixed` (it spans both R and Python detectors); if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/doublet-detection`. Complements the earlier QC step in [Single-cell RNA QC](single-cell-rna-qc.html) and the downstream annotation work in [CellTypist](celltypist-cell-annotation.html) and [popV](popv-cell-annotation.html). Homotypic doublets — two cells of the same type — remain largely undetectable by any of these methods, which is why the skill treats calls as flags for inspection. Upstream directory: `single-cell/doublet-detection`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`single-cell/doublet-detection/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/single-cell/doublet-detection/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=doublet-detection&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdoublet-detection.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
