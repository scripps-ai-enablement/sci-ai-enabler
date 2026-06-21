---
title: Fit a survival model to censored clinical outcomes
parent: All recipes
grand_parent: Recipes
nav_order: 29
problem_class: Data analysis
subject_areas: [Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-21
summary: Use the scikit-survival Claude Skill to fit Cox and Random Survival Forest models to censored time-to-event data and report concordance with proper validation.
---

# Fit a survival model to censored clinical outcomes

Hand Claude Code a tidy table of patient covariates plus a time-to-event column and an event/censoring indicator; get back a fitted Kaplan-Meier baseline, a Cox proportional-hazards model, a Random Survival Forest, honest cross-validated concordance, and the risk stratification that goes into a prognosis paper.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Time-to-event data is the backbone of clinical prognosis work — overall survival, progression-free survival, time-to-readmission. The analysis is standard but easy to get subtly wrong: censoring must be encoded as a structured `(event, time)` outcome (not a plain float), the concordance index must be evaluated out-of-sample (an in-sample c-index flatters every model), the proportional-hazards assumption needs checking before a Cox hazard ratio is trustworthy, and tree-based models like Random Survival Forests need the right censoring-aware splitting criterion. Every group rebuilds this boilerplate, and a misencoded outcome silently corrupts the whole analysis. Solved looks like: hand the agent a table, get a Kaplan-Meier curve, a Cox model with checked assumptions, an RSF for non-linear effects, and an honest held-out c-index — with every modeling choice written down.

## Recommended approach

1. **Install the [scikit-survival skill](../../catalog/tools/scikit-survival.html)** in Claude Code:

   ```
   /plugin marketplace add K-Dense-AI/claude-scientific-skills
   /plugin install scikit-survival@claude-scientific-skills
   ```

   The skill wraps the GPL-3.0 `scikit-survival` (`sksurv`) library. Confirm `pip show scikit-survival` returns a version ≥ 0.23.

2. **Put a tidy table in your project.** One row per subject, numeric/categorical covariate columns, a duration column (follow-up time), and a binary event indicator (1 = event observed, 0 = censored). State the time unit explicitly — most survival bugs trace back to mixed units or to treating censored rows as events.

3. **Invoke the skill with the file path and the outcome encoding.** A minimal prompt:

   ```
   Run the scikit-survival skill on data/cohort.csv. Outcome columns:
   `os_months` (follow-up time, months) and `dead` (1=death, 0=censored).
   Covariates: age, stage, ecog, treatment_arm, biomarker_high.
   1. Build the structured survival outcome (Surv.from_arrays).
   2. Plot the Kaplan-Meier curve overall and stratified by treatment_arm,
      with a log-rank p-value.
   3. Fit a CoxPHSurvivalAnalysis model; report hazard ratios with 95% CIs.
   4. Fit a RandomSurvivalForest (n_estimators=300, min_samples_leaf=15).
   5. Report Harrell's c-index for both models via 5-fold cross-validation
      (concordance_index_censored on held-out folds, not in-sample).
   Save the fitted-metrics table to results/survival_metrics.csv and the
   KM + RSF figures to results/.
   ```

4. **Check the proportional-hazards assumption before trusting the Cox HRs.** Ask the agent to inspect scaled-Schoenfeld-style residuals or stratify on any covariate that violates PH. A Cox HR is only meaningful if the hazards are proportional.

   ```
   Check the proportional-hazards assumption for each Cox covariate.
   For any covariate that violates it, refit stratifying on that
   covariate and show how the remaining HRs shift.
   ```

5. **Stratify into risk groups for the clinical readout.** Use the model's risk score to split the cohort (e.g., tertiles), then re-plot Kaplan-Meier per risk group with a log-rank test — this is the figure clinicians read.

6. **Hand off.** The metrics CSV and figures drop into a manuscript. For external validation, run the saved model on a second cohort table in the same conversation and compare held-out c-index.

## Why this assembly

Rung 2. scikit-survival *is* the validated Python survival-analysis stack (Cox, RSF, Gradient Boosted survival, c-index, integrated Brier score); the skill is a thin wrapper that pins the right idioms — structured `Surv` outcomes, censoring-aware scoring, out-of-sample evaluation. Plain Claude Code can write `sksurv` from memory but tends to drift on outcome encoding (the single most common survival bug) and on whether the c-index it reports is in-sample or held-out — exactly what the skill prevents. There is no need for a multi-tool harness or an autonomous system: this is one well-defined analytical task and a skill is the right grain.

## Availability

Fully open. scikit-survival is GPL-3.0 and the K-Dense skill wrapper is OSS on the K-Dense marketplace. Any current Claude plan suffices. The cohort table stays local — no institutional license or data-residency gate from the tooling itself. Note that the *data* (e.g., MIMIC, a hospital registry) usually carries its own access and IRB constraints; those are the user's to satisfy.

## Compute requirements

Laptop. A cohort of a few thousand subjects with a dozen covariates fits Cox and a 300-tree RSF, with 5-fold CV, in seconds to a couple of minutes on 8 GB RAM. RSF memory and wall-clock scale with `n_estimators × n_samples`; tens of thousands of subjects still finish in minutes. No GPU needed.

## Evidence

Proposed. No peer-reviewed paper documents this *exact* assembly (Claude Code + the K-Dense scikit-survival skill) running a survival analysis end-to-end. The component evidence is robust:

- **scikit-survival itself** — [Pölsterl, *JMLR* 21(212):1–6 (2020)](https://jmlr.org/papers/v21/20-729.html) is the canonical reference for the library, implementing Cox, Random Survival Forests, Gradient Boosted survival models, and censoring-aware metrics.
- **Random Survival Forests + concordance as the standard clinical method (analogous)** — recent prognosis studies use exactly this pattern: [Zhang et al., *Transl. Cancer Res.* (2026)](https://doi.org/10.21037/tcr-2025-aw-2462) compares nomograms and RSF for triple-negative breast-cancer survival on SEER; [Liu et al., *Medicine* (2026)](https://doi.org/10.1097/MD.0000000000048757) screens 101 survival algorithms (including RSF, LASSO-Cox, survival SVM) by mean c-index for colorectal-cancer prognosis. These validate the method, not the Claude assembly.

No published comparison of LLM-driven survival analysis against a hand-coded `sksurv` script is known. The skill adds consistent outcome encoding and out-of-sample scoring; it does not change the underlying statistical method.

## Alternatives considered

- **Plain Claude Code, no skill.** Works for users fluent in `sksurv`/`lifelines`. Reach for the skill when you want the outcome encoding and the held-out-c-index discipline pinned across runs and collaborators.
- **lifelines (Python) or the R `survival` / `survminer` stack.** Domain-standard alternatives; `lifelines` is friendlier for pure Kaplan-Meier and parametric AFT models, R for publication-grade KM plots. Neither has a Claude-installable wrapper today; use them outside Claude Code when you need their specific idioms.
- **PyHealth deep-learning survival.** For very large EHR cohorts where deep models add value, the [PyHealth skill](../../catalog/tools/pyhealth.html) targets neural clinical-prediction tasks. That is a rung-2-to-3 escalation; reach for it only when classical Cox/RSF underperforms on a large, high-dimensional cohort.

## See also

- [scikit-survival (Claude Skill)](../../catalog/tools/scikit-survival.html)
- [PyHealth (Claude Skill)](../../catalog/tools/pyhealth.html) — the deep-learning escalation for large EHR cohorts.
- [Run bulk RNA-seq differential expression](run-bulk-rnaseq-differential-expression.html) — the upstream step when survival covariates are expression-derived signatures.
- [Profile a cancer cohort's genomics with cBioPortal](profile-cancer-cohort-genomics-with-cbioportal.html) — the first-read Kaplan-Meier split; escalate here when you need adjusted, validated modelling.

## Sources

- [scikit-survival paper, Pölsterl 2020 (JMLR)](https://jmlr.org/papers/v21/20-729.html) — published 2020; verified 2026-06-06 (this run).
- [Zhang et al. 2026, nomogram vs RSF in TNBC (Transl. Cancer Res.)](https://doi.org/10.21037/tcr-2025-aw-2462) — published 2026; verified 2026-06-06 (this run).
- [Liu et al. 2026, 101 ML survival methods in CRC (Medicine)](https://doi.org/10.1097/MD.0000000000048757) — published 2026; verified 2026-06-06 (this run).
- [`scientific-skills/scikit-survival/SKILL.md` (K-Dense)](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/scikit-survival/SKILL.md) — verified 2026-06-06 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=fit-survival-model-to-clinical-outcomes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffit-survival-model-to-clinical-outcomes.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
