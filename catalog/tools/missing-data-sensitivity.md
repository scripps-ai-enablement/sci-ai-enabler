---
title: Missing Data Sensitivity (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-02
summary: "Run regulatory-grade missing-data analyses for confirmatory trials — MMRM, reference-based multiple imputation, tipping-point and pattern-mixture sensitivity"
---

# Missing Data Sensitivity (bioSkills)

A Claude Code skill for handling missing endpoint data in confirmatory clinical trials the way regulators expect: an estimand fixed first, MMRM or multiple imputation as the primary analysis, and reference-based and tipping-point sensitivity analyses around it.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — the R packages it drives (`mmrm` and `rbmi`, Apache-2.0; `mice` and `mitools`, GPL-2) and the Python ones (`scikit-learn`, `statsmodels`, `numpy`, `pandas`, BSD-3) are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (R and Python), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "clinical-biostatistics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/clinical-biostatistics/missing-data-sensitivity ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the analysis packages on first use, e.g. `install.packages(c("mmrm", "rbmi", "mice", "mitools"))` in R.

## What it does

Six stages, from estimand to submission-ready sensitivity table:

- **Estimand pre-specification** — fix the intercurrent-event strategy (treatment policy, hypothetical, composite, while-on-treatment, principal stratum) per **ICH E9(R1)** before choosing any analysis method.
- **Missingness-mechanism assessment** — inspect the CDISC DS domain for differential dropout, run Little's MCAR test, and document the MAR-versus-MNAR argument in the SAP rather than assuming one.
- **Primary analysis** — MMRM under MAR with unstructured covariance and the Kenward–Roger degrees-of-freedom correction for continuous longitudinal endpoints, or multiple imputation under MAR for less regular patterns.
- **Sensitivity analyses** — reference-based multiple imputation in the Carpenter–Roger 2013 family (jump-to-reference, copy-reference, copy-increments-in-reference, last-mean-carried-forward); Permutt delta-adjustment and tipping-point analysis; pattern-mixture identifying restrictions (CCMV, NCMV, ACMV).
- **Variance reconciliation** — report both Rubin's (information-anchored) and frequentist (conditional MI plus jackknife) variances for reference-based MI, which is the substance of the Cro-versus-Bartlett debate.
- **Regulatory reporting** — express the tipping delta in residual-SD units, articulate what the MNAR assumption means clinically, and keep the SAP's pre-specified fallback hierarchy.

Software: R `mmrm` ≥0.3 (Roche/openpharma), `rbmi` ≥1.5, `mice` ≥3.16, `mitools` ≥2.4; Python `scikit-learn` ≥1.4 (`IterativeImputer` with `sample_posterior=True`, BayesianRidge only), `statsmodels` ≥0.14, `numpy`, `pandas`. Imputation count follows von Hippel's **m ≥ 100 × FMI** rule for a stable pooled standard error.

**Primary use cases**: primary-endpoint analysis with dropout, a submission's missing-data sensitivity package, defending an MNAR assumption to a regulator.

## Notes

The skill is explicit about one trap: `statsmodels.mixedlm` in Python has **no Kenward–Roger correction**, so it is exploratory only — confirmatory MMRM must go through R `mmrm`. The upstream framing follows **NRC 2010** and **ICH E9(R1)**.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-clinical-biostatistics-missing-data`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/missing-data-sensitivity`. Upstream directory: `clinical-biostatistics/missing-data-sensitivity`.

Overlaps deliberately with [Trial Reporting](trial-reporting.html), which covers the same MMRM/`rbmi` machinery inside a wider CONSORT reporting workflow; use this skill when the missing-data package is itself the deliverable. Design-stage interim and re-estimation questions belong to [Adaptive Designs](adaptive-designs.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-biostatistics/missing-data-sensitivity/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/missing-data-sensitivity/SKILL.md)
- [ICH E9(R1) Estimands and Sensitivity Analysis in Clinical Trials](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf)
- [`rbmi` on CRAN](https://cran.r-project.org/package=rbmi)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=missing-data-sensitivity&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmissing-data-sensitivity.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
