---
title: MSI Detection (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-16
summary: "Calls microsatellite instability from WES/WGS/panel or cfDNA with MSIsensor-pro, MANTIS and mSINGS for dMMR, Lynch screening and ICI eligibility"
---

# MSI Detection (bioSkills)

A Claude Code skill that calls microsatellite instability status from sequencing data — paired, tumour-only or cfDNA — with the panel-specific thresholds each caller actually requires.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT). MSIsensor, MSIsensor-pro, MSIsensor-ct, MANTIS and mSINGS are separately installed command-line tools under their own licences |
| **Capabilities** | Read/Write — Claude drives the CLI tools locally on your BAMs; it is not an MCP tool |

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
  cp -r bioSkills/clinical-databases/msi-detection ~/.claude/skills/
  ```
  (run from the directory holding your clone — if you are still in `bioSkills/` from the previous step, use `cp -r clinical-databases/msi-detection ~/.claude/skills/`, or replace `bioSkills/` with the absolute path of your clone). Install the primary caller:
  ```
  conda install -c bioconda msisensor-pro
  ```
  (bioconda is the documented distribution route for MSIsensor-pro; MANTIS and mSINGS install from their own repositories.)

## What it does

Chooses the caller that matches the data you actually have, then applies its calibrated cutoff:

- **MSIsensor** — paired tumour–normal, the reference case.
- **MSIsensor-pro** — tumour-only, using a population baseline built from a cohort of normals.
- **MSIsensor-ct** — cfDNA and liquid biopsy, panel-aware.
- **MANTIS** — step-wise difference algorithm (> 0.4 instability threshold).
- **mSINGS** — background-panel approach for targeted panels.

Reported thresholds and gates:

| Parameter | Value |
|---|---|
| MSI-H | ≥ 20–30% unstable loci (panel-calibrated) |
| Bethesda 5-locus panel | ≥ 2/5 unstable = 40% |
| Minimum informative loci | ≥ 50 for NGS-derived site sets |
| Tumour purity | ≥ 20% |
| ctDNA fraction (MSIsensor-ct) | ≥ 3% |
| MANTIS step-wise difference | > 0.4 |

Output is the raw unstable-locus count, the percentage unstable, and an MSI-H / MSI-L / MSS classification, with concordance checks against MMR immunohistochemistry.

**Primary use cases**: checkpoint-inhibitor eligibility (FDA pembrolizumab pan-tumour MSI-H, 2017; KEYNOTE-177), Lynch syndrome screening, dMMR confirmation, liquid-biopsy MSI.

## Notes

**Research use, not a diagnostic result** — clinical MSI status comes from a validated assay plus MMR IHC, and the skill's own workflow treats IHC concordance as a required cross-check rather than an optional one.

Two failure modes it is explicit about: a tumour-only call without a properly matched population baseline is unreliable, and low tumour purity or low ctDNA fraction produces false-MSS results rather than a flagged failure. Distinguishing MSI-H from a POLE-exonuclease hypermutator matters clinically because the mutational signatures overlap.

Read alongside [Tumor Mutational Burden](tumor-mutational-burden.html) — MSI-H and TMB-H are correlated but separately reported ICI biomarkers (Sha 2020, Salem 2018) — and [Somatic Signatures](somatic-signatures.html) for MMR-deficiency versus POLE etiology.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection. Upstream skill front-matter name is `bio-clinical-databases-msi-detection`; upstream directory `clinical-databases/msi-detection`. The skill is description-activated — there is no bare `/msi-detection` slash command.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-databases/msi-detection/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-databases/msi-detection/SKILL.md)
- [`xjtu-omics/msisensor-pro`](https://github.com/xjtu-omics/msisensor-pro)
- [FDA approval of pembrolizumab for MSI-H/dMMR solid tumours (2017)](https://www.fda.gov/drugs/resources-information-approved-drugs/fda-grants-accelerated-approval-pembrolizumab-first-tissuesite-agnostic-indication)
- [Le et al. 2015, PD-1 blockade in mismatch-repair-deficient tumours](https://doi.org/10.1056/NEJMoa1500596)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=msi-detection&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmsi-detection.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
