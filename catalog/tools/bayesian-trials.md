---
title: Bayesian Trials (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-09
summary: "Design Bayesian dose-finding, basket and platform trials with RBesT MAP priors, BOIN/CRM escalation and EXNEX borrowing, against current FDA Bayesian guidance"
---

# Bayesian Trials (bioSkills)

A Claude Code skill for designing Bayesian clinical trials — Phase I dose-finding, external-data borrowing with MAP priors, basket and platform designs — with the borrowing weights, stopping thresholds and regulatory anchors made explicit.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — `RBesT`, `OncoBayes2`, `BOIN`, `dfcrm`, `escalation`, `trialr`, `bayesDP`, `psborrow2`, `bhmbasket` and `c212` are separately installed OSS R packages, several of which compile against Stan. |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (R), not as an MCP tool |

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
  cp -r bioSkills/clinical-biostatistics/bayesian-trials ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the R packages on first use, e.g. `install.packages(c("RBesT", "BOIN", "dfcrm", "OncoBayes2"))`. `RBesT` and `OncoBayes2` build on Stan, so expect a working C++ toolchain and a multi-minute first install.

## What it does

Four design families, each with its package and its calibrated defaults:

- **Phase I dose-finding** — BOIN (primary, `get.boundary()` / `get.oc()`), CRM and EWOC via `dfcrm`, mTPI-2 and Keyboard via `escalation`. Standard oncology target DLT rate **30%**, with escalation below **0.6 × target** and de-escalation above **1.4 × target**; an early-stop futility floor at **12 patients** on the lowest dose; CRM indifference-interval halfwidth **0.05** (Lee–Cheung 2009); EWOC's overdose constraint **P(dose > MTD) ≤ 0.25** (Babb–Rogatko–Zacks 1998).
- **External-data borrowing** — meta-analytic-predictive priors with `RBesT` (`gMAP()`, `robustify()`). Target a MAP prior effective sample size of **20–80% of the new control arm** (Schmidli 2014), and protect against prior-data conflict with a robust mixture weight of **0.1–0.3** on the informative component. Power-prior discounting for paediatric extrapolation runs **γ = 0.3–0.6** as a working convention — the skill is explicit that the FDA January 2026 draft **does not prescribe a range**.
- **Basket trials** — EXNEX (`OncoBayes2`, `bhmbasket`) with the Neuenschwander 2016 baseline **0.5 / 0.5** exchangeable / non-exchangeable weights, and a required sensitivity sweep over **0.1, 0.3, 0.5, 0.7, 0.9**.
- **Platform trials and safety** — the I-SPY 2, GBM AGILE and REMAP-CAP patterns, with I-SPY 2 graduation at a posterior predictive probability of Phase 3 success **≥ 0.85**; Berry–Berry three-level hierarchical AE modelling via `c212`.

Diagnostics the skill requires before any posterior is reported: Stan **R-hat < 1.01** (Vehtari 2021) and **effective sample size > 1000 per chain**.

**Primary use cases**: designing a Phase I dose-escalation study, borrowing a historical control arm, planning a basket or platform trial.

## Notes

**Borrowing weights are the design, not a detail.** Every threshold above is a prior choice made before data are seen, and the skill treats the sensitivity sweep — over EXNEX weights, over robust-mixture weights, over the power-prior discount — as mandatory reporting rather than an optional extra. A single-weight analysis is not interpretable.

Regulatory anchors cited: the **FDA Bayesian Devices Guidance (2010)**, the **FDA draft guidance on Bayesian methodology in drug development (January 2026)**, the **BOIN Fit-for-Purpose qualification (December 2021)**, and **Project Optimus** dose-optimisation. The January 2026 FDA document is a **draft** — treat it as one when writing an SAP.

An MTD chosen by BOIN or CRM answers a toxicity question, not a dose-optimisation question; Project Optimus expects randomised dose comparison for efficacy, which is a separate design.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-clinical-biostatistics-bayesian-trials`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/bayesian-trials`. Upstream directory: `clinical-biostatistics/bayesian-trials`.

Related: [Adaptive Designs](adaptive-designs.html) (frequentist group-sequential and SSR machinery, and the same `BOIN`/`dfcrm`/`trialr` dose-finding packages), [Subgroup Analysis](subgroup-analysis.html) (Bayesian shrinkage across subgroups uses the same EXNEX/MAP toolkit), [Power and Sample Size](power-and-sample-size.html), [PyMC](pymc.html) for general-purpose Bayesian modelling outside the trial-design frame.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-biostatistics/bayesian-trials/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/bayesian-trials/SKILL.md)
- [FDA Guidance for the Use of Bayesian Statistics in Medical Device Clinical Trials (2010)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/guidance-use-bayesian-statistics-medical-device-clinical-trials)
- [`RBesT` on CRAN](https://cran.r-project.org/package=RBesT)
- [`BOIN` on CRAN](https://cran.r-project.org/package=BOIN)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=bayesian-trials&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbayesian-trials.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
