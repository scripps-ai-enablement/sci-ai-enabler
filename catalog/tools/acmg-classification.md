---
title: ACMG Classification (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-16
summary: "Classifies germline variants P/LP/VUS/LB/B under ACMG-AMP 2015 with ClinGen SVI specifications, Tavtigian Bayesian points, and calibrated in-silico thresholds"
---

# ACMG Classification (bioSkills)

A Claude Code skill that applies the ACMG/AMP variant-classification framework as it is actually practised today — ClinGen SVI specifications, the Tavtigian Bayesian point system, and calibrated thresholds for in-silico predictors — rather than the 2015 rules read literally.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT). The predictor scores and population data it reasons over (REVEL, BayesDel, AlphaMissense, SpliceAI, gnomAD, ClinVar) come from their own sources under their own terms |
| **Capabilities** | Read/Write — Claude runs the skill's Python workflow locally and queries public APIs; it is not an MCP tool |

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
  cp -r bioSkills/clinical-databases/acmg-classification ~/.claude/skills/
  ```
  (run from the directory holding your clone — if you are still in `bioSkills/` from the previous step, use `cp -r clinical-databases/acmg-classification ~/.claude/skills/`, or replace `bioSkills/` with the absolute path of your clone). The workflow uses `requests` for API lookups:
  ```
  pip install requests
  ```

## What it does

Walks the evidence codes and combines them on the **Tavtigian 2018/2020 Bayesian point scale**, which is the arithmetic behind current ClinGen practice:

- **Loss-of-function** — the Abou Tayoun 2018 PVS1 decision tree (exon skipping, NMD escape, last-exon truncation), with AutoPVS1-style automation.
- **In-silico evidence, calibrated** — Pejaver 2022 thresholds for REVEL/BayesDel/VEST4 and Bergquist 2025 calibration for AlphaMissense, so PP3/BP4 is applied at a defensible strength rather than as a blanket "predicted damaging".
- **Splicing** — Walker 2023 SpliceAI DS_max bands (≥ 0.2 → PP3_Supporting), with SpliceVault for aberrant-transcript expectations.
- **Functional data** — Brnich 2020 OddsPath for setting PS3/BS3 strength from assay validity.
- **Population frequency** — ClinGen SVI BA1 (> 5% by default) and the Whiffin 2017 maximum-credible-allele-frequency computation for BS1.
- **Gene-specific rules** — VCEP CSpec specifications, which override the generic defaults where they exist.
- **Somatic tiers** — AMP/ASCO/CAP 2017 Tier I–IV assignment (Li 2017) for tumour variants, kept separate from germline P/LP/VUS/LB/B.

**Primary use cases**: germline variant curation, resolving VUS with calibrated evidence, applying VCEP rules for a specific gene, assigning clinical actionability tiers to somatic findings.

## Notes

Classification output is **research and curation support, not a clinical report**. ACMG/AMP classification in a diagnostic setting requires a qualified laboratory director and phenotype context the skill does not have; case-level data (segregation, de novo status, phenotype specificity) has to be supplied by the analyst.

Two practical traps the skill is explicit about: point-scale combination is not interchangeable with the 2015 combining rules in edge cases, and PP3/BP4 must not be applied at full strength from raw predictor output — use the calibrated bands.

Complements the data-source pages it draws on: [ClinVar](clinvar-database.html), [gnomAD](gnomad-database.html) and [dbSNP](dbsnp-database.html). For somatic interpretation reasoning through ToolUniverse, see [Cancer Variant Interpretation](tooluniverse-cancer-variant-interpretation.html).

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection. Upstream skill front-matter name is `bio-clinical-databases-acmg-classification`; upstream directory `clinical-databases/acmg-classification`. The skill is description-activated — there is no bare `/acmg-classification` slash command.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-databases/acmg-classification/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-databases/acmg-classification/SKILL.md)
- [Richards et al. 2015, ACMG/AMP standards and guidelines](https://doi.org/10.1038/gim.2015.30)
- [Tavtigian et al. 2020, Bayesian point system](https://doi.org/10.1002/humu.24088)
- [ClinGen Sequence Variant Interpretation working group](https://clinicalgenome.org/working-groups/sequence-variant-interpretation/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=acmg-classification&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Facmg-classification.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
