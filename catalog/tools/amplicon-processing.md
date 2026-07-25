---
title: Amplicon Processing (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-25
summary: "Convert demultiplexed 16S/ITS amplicon FASTQs into exact amplicon sequence variants (ASVs) with DADA2 — primer removal, per-run error modeling, pair merging and chimera removal"
---

# Amplicon Processing (bioSkills)

A Claude Code skill that turns demultiplexed 16S rRNA or ITS amplicon FASTQ files into exact amplicon sequence variants (ASVs) using DADA2, handling the primer-removal and per-run error-modeling steps correctly.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — DADA2, cutadapt, QIIME2 and related tools are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/R), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "microbiome"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/microbiome/amplicon-processing ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install DADA2 (R) / cutadapt / QIIME2 when prompted on first use.

## What it does

Runs the denoising pipeline that converts raw amplicon reads into ASVs, enforcing the order-of-operations that DADA2 requires:

- **Primer removal** — cutadapt with `--discard-untrimmed` (mandatory before quality filtering); ITSxpress for variable-length ITS spacer trimming.
- **Quality filtering** — `filterAndTrim()` with expected-error and truncation thresholds.
- **Per-run error learning** — `learnErrors()` fit to individual sequencing runs only (never pooled across runs).
- **Denoising** — `dada()` against run-specific error models; Deblur available as a static-profile alternative for 16S.
- **Pair merging** — `mergePairs()` with overlap validation.
- **Chimera + contaminant removal** — DADA2 chimera detection and `decontam` for control-based contaminant identification.
- **QIIME2** available as a wrapper interface over DADA2/Deblur.

**Primary use cases**: 16S/ITS ASV inference, amplicon QC and denoising, feature-table generation for downstream taxonomy and diversity analysis.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-microbiome-amplicon-processing`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/amplicon-processing`. The output ASV table feeds `taxonomy-assignment` (classification) and the diversity/differential-abundance microbiome skills. Upstream directory: `microbiome/amplicon-processing`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`microbiome/amplicon-processing/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/microbiome/amplicon-processing/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=amplicon-processing&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Famplicon-processing.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
