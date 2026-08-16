---
title: Design a Bayesian trial that borrows external control data
parent: All recipes
grand_parent: Recipes
nav_order: 8
problem_class: Experimental design
subject_areas: [Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-16
summary: Use the Bayesian Trials skill and RBesT to turn historical controls into a MAP prior with a declared effective sample size, then simulate what it costs under prior-data conflict.
---

# Design a Bayesian trial that borrows external control data

You have historical or external control data and want to shrink the concurrent control arm. Quantify exactly how many patients' worth of information you are borrowing, simulate what that borrowing does when the external data and the concurrent control disagree, and put both numbers in the protocol before enrolment.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Borrowing external control information is the most attractive and the most dangerous move in early-phase trial design. It is attractive because a smaller control arm means faster recruitment, lower cost, and fewer patients randomised to a comparator nobody wants. It is dangerous because the borrowing decision is made *before* the new data exist, and if the external controls turn out not to look like your concurrent controls, the prior does not politely step aside — it drags the posterior with it and inflates the false-positive rate on the treatment effect.

The failure mode is not a crash. It is a design memo that says "we will use a MAP prior from four historical studies," a reviewer who cannot tell from that sentence whether 8 patients or 80 patients of information are being injected, and an operating-characteristic table computed only under the assumption that the borrowing is correct. "Solved" means three things are on paper before the first patient enrols: the borrowed information expressed as an **effective sample size in patients**, the design's type I error and power **measured under disagreement as well as agreement**, and a no-borrowing comparator showing what the borrowing actually bought.

## Recommended approach

Install the [Bayesian Trials skill](../../catalog/tools/bayesian-trials.html) (bioSkills, `clinical-biostatistics/bayesian-trials`) and its CRAN dependencies. Everything below lands in a version-controlled `design/` directory; the chat is where the scripts get written, not where the answer lives.

1. **Design the no-borrowing trial first and commit it.** Write `design/00_no_borrowing_reference.R`: the conventional two-arm design at your target power with a full concurrent control, and its sample size. This file is the load-bearing comparator — without it, "borrowing saved 40 patients" is an assumption, not a measurement. Commit it before you look at the historical data.

2. **Assemble the external evidence into `design/historical.csv`, one row per source study**, with the control-arm event count or mean, its n, and the study identifier. Record why each study is *eligible* to be exchangeable with your concurrent control — same endpoint definition, same population, same standard of care — in `design/borrowing_rationale.md`. Studies that fail that test are excluded here, not down-weighted later.

3. **Fit the MAP prior and report its effective sample size in patients.** `design/01_map_prior.R` runs the skill's `RBesT` workflow (`gMAP()` → mixture approximation → `robustify()`) and writes `design/map_prior.json` containing the mixture components, the between-trial heterogeneity τ, the robust-component weight, and — the field the whole design turns on — the prior **ESS in patients**. Declare a target before you fit: the skill's convention is **20–80% of the planned new control arm** ([Schmidli et al. 2014](https://doi.org/10.1111/biom.12242)). If the fitted ESS lands outside your declared band, change the design deliberately and say so; do not quietly accept it.

   ```
   Fit a MAP prior from design/historical.csv using the bayesian-trials skill.
   Emit design/map_prior.json with the mixture components, tau, the robust weight,
   and the prior effective sample size expressed in patients. Do not proceed to
   operating characteristics until that ESS is written to the file.
   ```

4. **Simulate operating characteristics over a two-way grid: true treatment effect × prior-data conflict.** `design/02_operating_characteristics.R` writes `design/oc_grid.csv`, one row per (true effect, conflict magnitude, robust weight, replicate count). Conflict is parameterised as the concurrent control rate shifted away from the MAP mean — at minimum ±1 and ±2 τ, plus a shift large enough to be clinically noticeable. Report type I error and power **per cell**, never averaged over the grid. Sweep the robust-mixture weight over the skill's range (**0.1–0.3** on the informative component) and keep each weight as its own set of rows.

5. **Read the conflict column before the agreement column.** The design is acceptable only if the type I error under the conflict scenarios you consider plausible is one you are willing to defend. Robustification alleviates prior-data conflict; it does not remove it ([Schmidli et al. 2014](https://doi.org/10.1111/biom.12242)), and selecting the borrowing amount adaptively rather than pre-specifying it is an active methods area, not a solved one ([Hupf et al. 2021](https://doi.org/10.1002/sim.8970)). If the inflation is unacceptable, the fix is less borrowing or a smaller robust weight on the informative component — not a footnote.

6. **Gate every reported posterior on convergence.** The skill requires Stan **R-hat < 1.01** and **effective sample size > 1000 per chain** before a posterior is quoted. Have the script abort rather than warn: a non-converged chain emits a clean-looking posterior summary with nothing in the table to flag it.

7. **For a basket design, sweep the exchangeability weight; never report a single one.** With `OncoBayes2`/`bhmbasket` EXNEX, the baseline is **0.5 / 0.5** exchangeable / non-exchangeable (Neuenschwander 2016, as recorded on the skill's catalog page) and the skill treats a sensitivity sweep over **0.1, 0.3, 0.5, 0.7, 0.9** as mandatory reporting. A single-weight basket analysis is not interpretable, because the weight *is* the assumption about whether the baskets are the same disease.

8. **For a dose-finding design, state which question the design answers.** BOIN/CRM/EWOC identify an MTD, which is a toxicity answer. Project Optimus expects a randomised dose comparison for efficacy — a different design that this one does not deliver. Write that boundary into the protocol explicitly.

9. **Emit `design/provenance.json` and draft the SAP section from the files, not from memory.** Record R version, the exact `RBesT` / `OncoBayes2` / `BOIN` / `dfcrm` versions, the RNG seed, the replicate count, the fitted ESS, and the regulatory documents cited *with their status*. The SAP section quotes `oc_grid.csv` and `map_prior.json`; any sentence not traceable to those files does not go in.

Commit `design/` — scripts, `historical.csv`, `borrowing_rationale.md`, `map_prior.json`, `oc_grid.csv`, `provenance.json`, and the SAP section — as one changeset. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) for the pattern.

## Why this assembly

Rung 2. One skill plus its R packages, and the recipe stops there.

Rung 1 fails for a specific reason, and it is not that the code is hard — an `RBesT` MAP fit is a handful of lines. It is that the arithmetic is the settled part and the *choices around it* are not. Asked to "design a trial borrowing historical controls," Claude Code alone will produce a syntactically valid `gMAP()` call, a posterior, and a sample size, with no ESS reported, no conflict scenarios simulated, and no no-borrowing comparator — an output that looks like a design and cannot be reviewed. The skill supplies the calibrated conventions (the 20–80% ESS band, the 0.1–0.3 robust weight, the EXNEX sweep, the R-hat and ESS gates) that turn the run into something a statistician or a regulator can argue with. Rung 3 buys nothing: no second component is needed to compute or defend the borrowing.

## Availability

`Fully open`. The skill is MIT-licensed and every statistical package (`RBesT`, `OncoBayes2`, `BOIN`, `dfcrm`, `escalation`, `trialr`, `bayesDP`, `psborrow2`, `bhmbasket`, `c212`) is open-source on CRAN. Two practical frictions: several of them compile against **Stan**, so expect a working C++ toolchain and a multi-minute first install, and this is an R workflow — none of it is pip-installable.

The design work is entirely local, so a confidential development plan never leaves the machine. Nothing here requires patient-level data; `historical.csv` holds summary statistics.

Regulatory anchors cited in the skill: the FDA Bayesian Devices Guidance (2010), the BOIN Fit-for-Purpose qualification (December 2021), and the **draft** FDA guidance on Bayesian methodology in drug development (January 2026). Cite the January 2026 document as a draft in any SAP — the skill is explicit that it does not prescribe a borrowing range.

## Compute requirements

`Laptop`. The `gMAP()` Stan fit runs once and takes minutes, not hours; because the resulting mixture priors are conjugate for the one-parameter exponential family, the operating-characteristic grid updates analytically and a few thousand replicates per cell finish in minutes on a laptop.

The one step that is genuinely expensive is **basket-trial simulation**: EXNEX has no conjugate shortcut, so each replicate is its own MCMC fit, and a full weight sweep (5 weights × an effect grid × 1,000+ replicates) is an overnight job. Reduce the effect grid before reducing the replicate count — Monte-Carlo error around 1 percentage point is enough to reorder two close designs. Budget C++ toolchain setup separately; it is the step that most often eats the first afternoon.

## Evidence

`Proposed`. No documented attempt is known of an agent driving this skill end-to-end for a borrowing design, and the skill itself carries no published benchmark.

The method leg is strong and directly on point. Robust MAP priors were introduced precisely because "under prior-data conflict, a too optimistic use of historical data may be inappropriate," with mixture robustification giving "a more rapid reaction to prior-data conflicts" and frequentist operating characteristics reported across data scenarios ([Schmidli et al., *Biometrics* 2014](https://doi.org/10.1111/biom.12242)) — that paper is both the source of the recipe's ESS convention and the reason step 5 exists. The problem is not closed: a semiparametric MAP using a Dirichlet-process mixture was proposed specifically to relax the need to pre-specify the borrowing amount, with a generalised prior-ESS estimator "to aid in tuning the prior to the specific task at hand" ([Hupf et al., *Statistics in Medicine* 2021](https://doi.org/10.1002/sim.8970)) — evidence that the borrowing weight is a live design decision rather than a default.

For the dose-finding family, simulation across 3+3, CRM, Keyboard and BOIN found the 3+3 design selects the correct MTD with up to **three times lower** probability, often landing one or two dose levels below the true MTD, while the model-based and model-assisted designs consistently outperformed it ([Chiuzan & Dehbi, *Clinical Trials* 2024](https://doi.org/10.1177/17407745241240401)). That is component-level evidence for the escalation machinery, not for this assembly.

The closest documented analogue in the cookbook is [design-a-group-sequential-trial-with-interim-looks](design-a-group-sequential-trial-with-interim-looks.html), which is also `Proposed` and built on the same "simulate the operating characteristics, commit the comparator" discipline.

## Alternatives considered

**Stay frequentist.** If what you actually want is early stopping rather than a smaller control arm, [design-a-group-sequential-trial-with-interim-looks](design-a-group-sequential-trial-with-interim-looks.html) is the right page — alpha-spending boundaries, a fixed-sample comparator, and no prior to defend. Reach for the Bayesian route when the external information is the point; reach for the frequentist one when the interim looks are.

**A propensity-score-matched external control arm.** Where the external data are patient-level rather than summary-level, matching or weighting is a different framework with a different set of assumptions to defend, and `psborrow2` sits at that boundary. This recipe assumes summary-level historical controls; if you hold patient-level external data, the exchangeability argument in step 2 gets both easier to make and harder to satisfy, and the design deserves its own statistical review.

**No borrowing at all.** This is the honest answer more often than it looks. If step 4 shows type I error inflating past what you can defend under a conflict scenario you consider plausible, `design/00_no_borrowing_reference.R` is already written and already committed — ship that instead.

## See also

- [Bayesian Trials (bioSkills)](../../catalog/tools/bayesian-trials.html)
- [Adaptive Designs (bioSkills)](../../catalog/tools/adaptive-designs.html)
- [Design a group-sequential trial with interim looks](design-a-group-sequential-trial-with-interim-looks.html)
- [Draft a Phase 2/3 clinical trial protocol](draft-phase23-clinical-trial-protocol.html)
- [Handle missing endpoint data in a trial](handle-missing-endpoint-data-in-a-trial.html)

## Sources

- [Bayesian Trials (bioSkills) catalog page](../../catalog/tools/bayesian-trials.html) — authoritative for install path, package list, and the skill's calibrated defaults; verified 2026-08-10.
- [Schmidli H et al., "Robust meta-analytic-predictive priors in clinical trials with historical control information", *Biometrics*](https://doi.org/10.1111/biom.12242) — published 2014; verified 2026-08-16 (this run).
- [Hupf B, Bunn V, Lin J, Dong C, "Bayesian semiparametric meta-analytic-predictive prior for historical control borrowing in clinical trials", *Statistics in Medicine*](https://doi.org/10.1002/sim.8970) — published 2021; verified 2026-08-16 (this run).
- [Chiuzan C, Dehbi HM, "The 3 + 3 design in dose-finding studies with small sample sizes: Pitfalls and possible remedies", *Clinical Trials*](https://doi.org/10.1177/17407745241240401) — published 2024; verified 2026-08-16 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=design-a-bayesian-trial-that-borrows-external-data&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdesign-a-bayesian-trial-that-borrows-external-data.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
