---
title: Trial Reporting (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-02
summary: "Produce CONSORT 2025 / ICH E9(R1)-conformant trial statistical reports: estimands, analysis populations, Table 1, MMRM, and multiplicity control"
---

# Trial Reporting (bioSkills)

A Claude Code skill that takes a clinical trial from estimand definition through Table 1, primary analysis, missing-data sensitivity and multiplicity control to a CONSORT-conformant statistical report.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — the Python (`pandas`, `numpy`, `statsmodels`, `scikit-learn`, `tableone`, `rpy2`) and R (`mmrm`, `rbmi`, `gMCP`, `RBesT`, `mice`, `miceforest`) packages are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python, with R via `rpy2` for confirmatory steps), not as an MCP tool |

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
  cp -r bioSkills/clinical-biostatistics/trial-reporting ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the packages on first use, e.g. `pip install "pandas>=2.1" "tableone>=0.9" "statsmodels>=0.14"` and, for the confirmatory steps, `install.packages(c("mmrm", "gMCP"))` in R.

## What it does

Seven stages:

- **Estimand definition** — specify all five ICH E9(R1) attributes before selecting a method, and name the intercurrent-event strategy (treatment policy, hypothetical, composite, while-on-treatment, principal stratum).
- **Analysis populations** — define ITT, full analysis set, per-protocol and safety populations with explicit inclusion and exclusion criteria.
- **Baseline characterization** — Table 1 via `tableone`, using standardized mean differences (SMD > 0.1 flags imbalance) rather than baseline significance tests, which CONSORT advises against.
- **Primary analysis** — MMRM under MAR for continuous endpoints (preferred), or reference-based MI under MNAR, reporting the treatment-by-visit contrast at the primary timepoint.
- **Missing-data sensitivity** — Permutt tipping-point delta-adjustment and reference-based MI variants (J2R, CR, CIR), with the mechanism assumptions documented.
- **Multiplicity control** — graphical procedures (Bretz–Maurer) via `gMCP` for co-primary and key secondary endpoints.
- **Regulatory reporting** — CONSORT 2025 flow diagram, Item 21c (missing-data methods) and Item 4 (data and code sharing), plus ITT-versus-per-protocol reconciliation.

Software: Python `tableone` 0.9+ (primary), `pandas` 2.1+, `numpy` 1.26+, `statsmodels` 0.14+, `scikit-learn` 1.4+, `rpy2` 3.x+; R `mmrm` 0.3+, `rbmi` 1.5+, `gMCP` 0.8+, `RBesT` 1.6+ (Bayesian shrinkage for subgroup estimates), `mice` 3.14+, `miceforest` 5.x+.

**Primary use cases**: writing a clinical study report's statistics sections, defining an estimand for an SAP, generating Table 1 and the CONSORT flow.

## Notes

Standards cited: **CONSORT 2025**, **SPIRIT 2025**, **ICH E9(R1)** estimands, and the FDA 2023 covariate-adjustment guidance. The same caveat as elsewhere in this category applies — `statsmodels.mixedlm` has no Kenward–Roger correction and is exploratory only; confirmatory MMRM goes through R `mmrm`, which is why `rpy2` is in the stack.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-clinical-biostatistics-trial-reporting`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/trial-reporting`. Upstream directory: `clinical-biostatistics/trial-reporting`.

Pairs with [Adaptive Designs](adaptive-designs.html) at the design stage and [Missing Data Sensitivity](missing-data-sensitivity.html) when the missing-data package needs more depth than the one stage here provides. For generating the protocol document itself, see [Clinical Trial Protocol](clinical-trial-protocol.html); for time-to-event modelling, [scikit-survival](scikit-survival.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-biostatistics/trial-reporting/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/trial-reporting/SKILL.md)
- [CONSORT statement](https://www.consort-statement.org/)
- [ICH E9(R1) Estimands and Sensitivity Analysis in Clinical Trials](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=trial-reporting&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftrial-reporting.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
