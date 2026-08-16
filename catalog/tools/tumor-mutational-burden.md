---
title: Tumor Mutational Burden (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-16
summary: "Calculates TMB from WES/WGS/panel data with Friends of Cancer Research harmonization, per-assay calibration, hypermutator tiering and blood TMB"
---

# Tumor Mutational Burden (bioSkills)

A Claude Code skill that computes tumour mutational burden the way assay-harmonization work says it must be computed — per-assay calibration and explicit filtering — instead of dividing a raw variant count by a nominal panel size.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT). cyvcf2, pandas and numpy are separately installed; VEP/snpEff, LOHHLA and DASH carry their own licences |
| **Capabilities** | Read/Write — Claude runs the skill's Python workflow locally on your VCFs; it is not an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "clinical-databases"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/clinical-databases/tumor-mutational-burden ~/.claude/skills/
  ```
  (run from the directory holding your clone — if you are still in `bioSkills/` from the previous step, use `cp -r clinical-databases/tumor-mutational-burden ~/.claude/skills/`, or replace `bioSkills/` with the absolute path of your clone). Install the Python dependencies:
  ```
  pip install "cyvcf2>=0.30" "pandas>=2.2" "numpy>=1.26"
  ```
  Consequence annotation requires **VEP ≥ 111** or **snpEff ≥ 5.2** to have been run on the VCF beforehand.

## What it does

- **Counts and normalizes** — parses an annotated somatic VCF with cyvcf2, counts nonsynonymous variants (missense, frameshift, stop-gained, splice-site), and divides by the assay's actual scored megabases rather than its nominal panel size.
- **Filters that change the answer** — VAF floors (≥ 5% with a paired normal, ≥ 10% tumour-only), depth ≥ 100, and germline removal by gnomAD population frequency (AF ≤ 0.5%). Tumour-only calling without germline subtraction is the classic source of inflated TMB.
- **Cross-assay harmonization** — Friends of Cancer Research equations and per-assay calibration, so the FDA's 10 mut/Mb cutoff maps to ~7.8 on TSO500 and ~8.4 on Oncomine TML instead of being applied identically everywhere.
- **Tiering and context** — hypermutator tiers (POLE/POLD1, MMR-deficient), tumour-type-specific cutoffs per McGrail 2021, and ESMO 2024 / FDA pan-tumour pembrolizumab (2020) reporting expectations.
- **Blood TMB** — tissue vs bTMB comparison, with the ctDNA-fraction caveats that make low-shedding tumours unreliable.
- **Immunogenicity integration** — pairs TMB with HLA loss-of-heterozygosity (LOHHLA, DASH) and neoantigen quality (Luksza 2017 fitness), since a high count with lost HLA presentation is not the same thing.

**Primary use cases**: checkpoint-inhibitor eligibility assessment, tissue-vs-blood TMB comparison, auditing a TMB-H call against the assay it came from.

## Notes

**Research use, not a diagnostic result.** A TMB value that drives a treatment decision must come from a validated clinical assay with its own cutoff; this skill's value is making explicit the filtering and calibration choices that a report usually hides.

The single most common error it guards against is comparing TMB across assays as if the number were assay-independent — panel size, scored region, synonymous-inclusion convention (FoundationOne includes them) and germline handling all shift the value by enough to cross the 10 mut/Mb line.

Read alongside [MSI Detection](msi-detection.html) — MSI-H and TMB-H are separate but correlated immunotherapy biomarkers, and POLE-exonuclease hypermutators can mimic one another — and [Somatic Signatures](somatic-signatures.html) for the mutational-process etiology behind a high count. Downstream neoantigen work is covered by [Neoantigen Prediction](neoantigen-prediction.html) and [Immunotherapy Response Prediction](tooluniverse-immunotherapy-response-prediction.html).

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection. Upstream skill front-matter name is `bio-clinical-databases-tumor-mutational-burden`; upstream directory `clinical-databases/tumor-mutational-burden`. The skill is description-activated — there is no bare `/tumor-mutational-burden` slash command.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-databases/tumor-mutational-burden/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-databases/tumor-mutational-burden/SKILL.md)
- [Merino et al. 2020, Friends of Cancer Research TMB Harmonization Project](https://doi.org/10.1136/jitc-2019-000147)
- [FDA approval of pembrolizumab for TMB-H solid tumours (2020)](https://www.fda.gov/drugs/resources-information-approved-drugs/fda-approves-pembrolizumab-adults-and-children-tmb-h-solid-tumors)
- [McGrail et al. 2021, tumour-type-specific TMB and ICI response](https://doi.org/10.1016/j.annonc.2021.02.006)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tumor-mutational-burden&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftumor-mutational-burden.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
