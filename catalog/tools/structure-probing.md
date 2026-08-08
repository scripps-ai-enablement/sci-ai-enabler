---
title: RNA Structure Probing (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Turn SHAPE-MaP or DMS-MaPseq reads into per-nucleotide reactivity profiles with ShapeMapper2, then fold RNA with those reactivities as soft restraints"
---

# RNA Structure Probing (bioSkills)

A Claude Code skill for the experimental half of RNA structure work: processing chemical-probing reads into normalized reactivity profiles, then using them to restrain — not replace — thermodynamic folding.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — ShapeMapper2 (Weeks Lab), ViennaRNA and SEISMIC-RNA are installed separately under their own licences |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "rna-structure"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/rna-structure/structure-probing ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites** — the folding and plotting layer installs cleanly from conda/pip:
  ```
  conda install -c conda-forge -c bioconda viennarna
  pip install "matplotlib>=3.8" "pandas>=2.2" "numpy>=1.26"
  ```
- **ShapeMapper2 2.1.5+** — **do not `conda install shapemapper`**: the bioconda package of that name is ShapeMapper **1.2** (checked 2026-08-08), a different generation of the pipeline that will not satisfy this skill. Install ShapeMapper2 from the Weeks Lab release for your platform and put its directory on `PATH`. **Unverified —** the exact release filename and build steps were not confirmed from upstream this run; follow the install section of the [`Weeks-UNC/shapemapper2`](https://github.com/Weeks-UNC/shapemapper2) README. ShapeMapper2 is **Linux-only**; on macOS run it under Docker or Singularity.
- **SEISMIC-RNA** (optional, only for multi-conformation clustering) — see [`rouskinlab/seismic-rna`](https://github.com/rouskinlab/seismic-rna) for its own install path; the skill targets 0.20+.

## What it does

Walks the probing experiment end to end, with the decisions that determine whether the resulting profile means anything:

- **Reagent choice** — SHAPE reagents (1M7, NAI, 2A3) report on all four bases; **DMS reads only A and C**, so G and U must be masked to `-999` rather than recorded as unreactive. Four-base DMS is treated as valid only when the protocol and analysis explicitly enable it.
- **Readout choice** — mutational profiling (MaP) and RT-stop readouts need different scoring pipelines; the skill does not let one be processed as the other.
- **Sample design** — three libraries, not one: **MODIFIED** (signal), **UNTREATED** (background), **DENATURED** (normalization reference).
- **Processing** — ShapeMapper2 produces normalized per-nucleotide reactivity profiles with per-position depth and error.
- **Normalization** — per-transcript 2–8% box-plot scaling.
- **Restrained folding** — reactivities enter ViennaRNA as soft pseudo-energy restraints, via the Deigan model (`m = 1.8`, `b = -0.6`) or the Zarringhalam model.
- **Multiple conformations** — per-read mutation data clustered with SEISMIC-RNA or DREEM when a single consensus structure is the wrong model.

QC thresholds the skill enforces: effective depth **≥ 5,000** (also ShapeMapper2's `--min-depth`), untreated mutation rate **< 0.5%**, modified mutation rate roughly **1–10%** (below that is undermodification, above it suggests degradation), and `--max-bg 0.05`. Nucleotides failing depth are reported as `-999`, never as zero.

**Primary use cases**: processing SHAPE-MaP/DMS-MaPseq libraries into reactivity profiles, folding a transcript with experimental restraints, detecting structural heterogeneity in a single transcript.

## Notes

The framing rule is that **reactivity probes constraint, not pairing** — a protected nucleotide may be base-paired, or bound by protein, or stacked, or simply in a badly-sequenced region, and the skill insists the technical explanations be ruled out first. The corollary that most often goes wrong in practice: **raw reactivities from different transcripts or experiments are not comparable**, so they must never be pooled or compared before per-transcript normalization.

Upstream skill front-matter name is `bio-rna-structure-structure-probing`; upstream directory `rna-structure/structure-probing`. ShapeMapper2's Linux-only constraint is the main practical obstacle for Mac users. Downstream and adjacent: [ViennaRNA](viennarna-structure-prediction.html) is the folding engine the restraints feed, [Covariation Analysis](covariation-analysis.html) provides the independent evolutionary line of evidence for the same structure, and [ncRNA Search](ncrna-search.html) identifies which family a probed transcript belongs to.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`rna-structure/structure-probing/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/rna-structure/structure-probing/SKILL.md)
- [`Weeks-UNC/shapemapper2`](https://github.com/Weeks-UNC/shapemapper2)
- [`rouskinlab/seismic-rna`](https://github.com/rouskinlab/seismic-rna)
- [`bioconda::shapemapper` (version 1.2 — not ShapeMapper2)](https://anaconda.org/bioconda/shapemapper)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=structure-probing&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fstructure-probing.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
