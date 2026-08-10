---
title: Effect Measures (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-09
summary: "Compute OR, RR, RD, HR and NNT with calibrated confidence intervals, and report marginal versus conditional estimands per FDA 2023 covariate-adjustment guidance"
verification: works
verified_on: 2026-08-10
reviewed_on: 2026-08-10
security: cleared
security_on: 2026-08-10
security_note: "GPTomics/bioSkills MIT root confirmed, provenance matches, bundled Python/CRAN packages open source"
---

# Effect Measures (bioSkills)

A Claude Code skill for reporting treatment effects correctly — choosing the measure, pairing it with a confidence interval that has the coverage it claims, and being explicit about whether the estimand is marginal or conditional.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — `statsmodels`, `numpy`, `pandas`, `matplotlib`, `marginaleffects` (Python) and `marginaleffects`, `ratesci`, `exact2x2`, `riskCommunicator`, `RobinCar`, `MASS`, `VGAM` (R) are separately installed OSS. |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python primary, R for the specialised interval methods), not as an MCP tool |
| **Verified** | works · 2026-08-10 |
| **Security** | cleared · 2026-08-10 — MIT, provenance matches, bundled Python/CRAN packages open source |

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
  cp -r bioSkills/clinical-biostatistics/effect-measures ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the Python side on first use with `pip install "statsmodels>=0.14" "numpy>=1.26" "pandas>=2.1" "matplotlib>=3.8" "marginaleffects>=0.0.13"`; the stratified and exact interval methods need R with `install.packages(c("marginaleffects", "ratesci", "exact2x2", "riskCommunicator", "RobinCar"))`.

## What it does

- **Effect measures** — odds ratio, risk ratio, risk difference, hazard ratio and number needed to treat, computed from 2×2 tables or from a fitted GLM.
- **Confidence intervals matched to the measure** — Wilson for a single proportion, Newcombe and MOVER for differences and ratios of proportions, Miettinen–Nurminen score intervals (stratified, via `ratesci`), exact unconditional intervals via `exact2x2`, profile-likelihood intervals via `MASS::confint.glm`, and Bender's method for the NNT interval. Wald intervals on a ratio scale are the default the skill replaces.
- **Marginal versus conditional estimands** — the distinction the **FDA 2023 covariate-adjustment guidance** requires trials to be explicit about. A logistic-regression coefficient is a *conditional* log-odds ratio; the population-level *marginal* effect comes from g-computation, which the skill runs via `marginaleffects` with HC3 standard errors, or via `RobinCar` for covariate-adjusted trial estimates.
- **Diagnostics** — Hauck–Donner effect detection via `VGAM::hdeff()`, which catches the case where a Wald test loses power as the effect gets larger (near-separation), and sandwich / HC3 standard errors for model misspecification.
- **Forest plots** — for cross-study or cross-subgroup comparison of the chosen measure.

**Primary use cases**: reporting the primary treatment effect of a confirmatory trial, building a forest plot, converting between effect scales for a meta-analysis.

## Notes

**The odds ratio and hazard ratio are non-collapsible**, which is the reason the marginal/conditional distinction matters at all: adjusting for a prognostic covariate changes a conditional OR even with no confounding, so a conditional OR from an adjusted model is not the same quantity as the unadjusted one and the two should not be compared as if they were. Risk difference and risk ratio are collapsible. When the outcome is common, the OR also diverges substantially from the RR and cannot be read as one.

**An NNT interval is not symmetric and can be discontinuous.** When the risk-difference interval spans zero, the NNT interval runs through infinity and must be reported as two intervals (benefit and harm), not as a single range — hence Bender's method rather than inverting the endpoints naively.

The FDA 2023 covariate-adjustment guidance is the anchor for the estimand framing; state in the SAP which estimand the primary analysis targets before unblinding.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-clinical-biostatistics-effect-measures`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/effect-measures`. Upstream directory: `clinical-biostatistics/effect-measures`.

Related: [Trial Reporting](trial-reporting.html) (the CONSORT write-up that consumes these estimates), [Subgroup Analysis](subgroup-analysis.html) (forest plots and interaction on the ratio versus difference scale), [Power and Sample Size](power-and-sample-size.html) (the same measure has to be the one you powered on), [Multiplicity and Graphical Procedures](multiplicity-graphical.html), [statsmodels](statsmodels.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-biostatistics/effect-measures/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/effect-measures/SKILL.md)
- [FDA Adjusting for Covariates in Randomized Clinical Trials for Drugs and Biological Products (2023)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adjusting-covariates-randomized-clinical-trials-drugs-and-biological-products)
- [`marginaleffects`](https://marginaleffects.com/)
- [`ratesci` on CRAN](https://cran.r-project.org/package=ratesci)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=effect-measures&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Feffect-measures.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
