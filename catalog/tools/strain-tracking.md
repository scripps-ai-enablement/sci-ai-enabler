---
title: Strain Tracking (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-08-01
summary: "Resolve and compare bacterial strains below species level from shotgun metagenomes using inStrain popANI, StrainPhlAn, MIDAS2, StrainGE and skani/fastANI"
---

# Strain Tracking (bioSkills)

A Claude Code skill that resolves sub-species bacterial strains from shotgun metagenomes and tests whether two samples share the same strain — the analysis behind transmission, engraftment, and persistence claims.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — inStrain, StrainPhlAn, MIDAS2, StrainGE, metaSNV, dRep, Bowtie2 and skani are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "metagenomics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/metagenomics/strain-tracking ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the chosen strain profiler and its reference genomes when prompted on first use.

## What it does

Builds a reference set, profiles microdiversity, and compares strains across samples:

- **Workflow** — dRep-dereplicate dataset MAGs to representative genomes (97–99% ANI) and build scaffold-to-bin metadata; Bowtie2-map sample reads to the concatenated reference; `inStrain profile` per sample to extract SNV populations and microdiversity; `inStrain compare` across samples using popANI (shared-strain threshold ≥99.999% over ≥50% genome breadth at ≥5× coverage); optionally MetaPhlAn + StrainPhlAn for marker-SNV consensus phylogeny and normalized genetic distance (nGD); skani for genome-to-genome ANI with the ~95% species boundary.
- **Method panel** — inStrain (popANI/conANI population microdiversity), StrainPhlAn (marker-based cross-sample phylogeny), MIDAS2 (pan-genome SNVs plus gene copy-number variation), StrainGE (low-abundance strains down to ~0.5× coverage), metaSNV v2 (subspecies structure), and skani/fastANI/MASH for isolate and MAG comparison.

**Primary use cases**: transmission and engraftment inference (FMT, mother–infant, hospital outbreaks), strain persistence over time, isolate-to-metagenome matching.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-metagenomics-strain-tracking`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/strain-tracking`. Coverage is the binding constraint — the popANI shared-strain call requires ≥5× breadth-qualified coverage, so shallow surveys profiled with [MetaPhlAn Profiling](metaphlan-profiling.html) or [Kraken Classification](kraken-classification.html) generally cannot be re-analysed at strain level without deeper sequencing. Upstream directory: `metagenomics/strain-tracking`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`metagenomics/strain-tracking/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/strain-tracking/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=strain-tracking&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fstrain-tracking.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
