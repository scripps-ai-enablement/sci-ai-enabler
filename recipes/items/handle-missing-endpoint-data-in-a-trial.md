---
title: Handle missing endpoint data in a confirmatory trial
parent: All recipes
grand_parent: Recipes
nav_order: 34
problem_class: Data analysis
subject_areas: [Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-02
summary: Use the Missing Data Sensitivity skill to fix an estimand, run MMRM as primary, and build a reference-based and tipping-point sensitivity package.
---

# Handle missing endpoint data in a confirmatory trial

Patients dropped out of your randomised trial. Fix the estimand first, run MMRM under MAR as the primary analysis, then surround it with the reference-based and tipping-point sensitivity analyses a regulator will ask for — with every assumption written down.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Every confirmatory trial loses participants, and the primary endpoint analysis has to say something defensible about the values that were never observed. This is the step where otherwise-clean trials get into trouble. The usual failure is method-first thinking: someone picks LOCF or a complete-case model, runs it, and only then works out what question it answers — which is often not the question the protocol asked. ICH E9(R1) inverted that order, requiring the estimand (including the intercurrent-event strategy) to be fixed before any analysis method is chosen, and regulators now read the sensitivity package as seriously as the primary result.

The technical traps stack up behind that. Little's MCAR test is routinely quoted as if a non-significant result licenses MAR — it does not; MAR versus MNAR is untestable from the observed data and has to be argued. Python's `statsmodels.mixedlm` has no Kenward–Roger denominator degrees-of-freedom correction, so a Python MMRM is anticonservative in small trials. Reference-based multiple imputation has a live variance debate (Rubin's estimator versus a frequentist one) that changes the standard error you report. And "we did 5 imputations" is not enough when the fraction of missing information is high. Solved looks like: a pre-specified estimand, one primary estimate, a sensitivity table spanning jump-to-reference through a tipping point expressed in residual-SD units, and a script anyone can re-run.

## Recommended approach

1. **Install the [Missing Data Sensitivity skill](../../catalog/tools/missing-data-sensitivity.html)** and its R packages (`mmrm`, `rbmi`, `mice`, `mitools`). Install paths are on the catalog page.

2. **Write the estimand down before you touch the data.** This is step one because every later choice branches on it. Ask the agent to draft it against ICH E9(R1)'s five attributes and, critically, to name a strategy per intercurrent event — treatment discontinuation and rescue medication usually need *different* strategies:

   ```
   Use the missing-data-sensitivity skill. Draft the estimand for our primary
   endpoint (change from baseline in <endpoint> at week 24) covering all five
   ICH E9(R1) attributes. For each intercurrent event we recorded — study-drug
   discontinuation, rescue medication, death — state the strategy (treatment
   policy / hypothetical / composite / while-on-treatment / principal stratum)
   and what each one implies for how the unobserved data must be handled.
   Write it to analysis/estimand.md. Do not choose an analysis method yet.
   ```

   Commit `analysis/estimand.md`. If it disagrees with the SAP, resolve that now, not after seeing a p-value.

3. **Characterise the missingness, and keep the MCAR test in its lane.** Have the agent tabulate dropout by arm and visit from the CDISC DS domain, plot missingness patterns, and run Little's test — then explicitly record that a non-significant MCAR test does **not** establish MAR. Differential dropout between arms is the finding that most often forces a stronger sensitivity package.

   ```
   Produce results/missingness_profile.csv: per arm and visit, n randomised,
   n observed, cumulative dropout, and reason category from the DS domain.
   Run Little's MCAR test and report it. Then write, in one paragraph, the
   substantive MAR-vs-MNAR argument for this endpoint and say plainly that
   the test cannot adjudicate it.
   ```

4. **Run the primary analysis in R, not Python.** For a continuous longitudinal endpoint that means MMRM with an unstructured covariance matrix and the Kenward–Roger correction, via R `mmrm`. Tell the agent this is confirmatory:

   ```
   Write analysis/mmrm_primary.R: MMRM on the ADaM analysis dataset, fixed
   effects treatment*visit + baseline*visit + stratification factors,
   unstructured covariance by subject, Kenward-Roger df. Report the week-24
   treatment contrast with 95% CI. Use R mmrm — statsmodels.mixedlm has no
   Kenward-Roger correction and is not acceptable as confirmatory here.
   If the unstructured model fails to converge, fall back down the SAP's
   pre-specified covariance hierarchy and record which structure was used.
   ```

   The convergence-fallback instruction matters: unstructured covariance fails on trials with many visits, and an undocumented switch to Toeplitz or AR(1) is a silent protocol deviation.

5. **Build the sensitivity ladder with `rbmi`.** Reference-based imputation makes explicit, clinically-interpretable assumptions about post-discontinuation behaviour. Run the Carpenter–Roger family rather than picking one:

   ```
   Write analysis/rbmi_sensitivity.R. Using rbmi with control as reference,
   run jump-to-reference, copy-reference, and copy-increments-in-reference.
   Set the number of imputations from a pilot run using von Hippel's
   two-stage rule (m scales with the square of the FMI), and record both the
   pilot FMI and the final m. Emit results/sensitivity_table.csv with one row
   per method: estimate, SE, 95% CI, m, FMI.
   ```

6. **Report both variances for the reference-based analyses.** Rubin's estimator gives information-anchored inference; the frequentist (conditional MI plus jackknife) estimator does not, and the two can differ materially. Put them side by side in `sensitivity_table.csv` as separate columns rather than choosing silently — this is the Cro-versus-Bartlett debate, and a reviewer will want to see you knew about it.

7. **Run the tipping point and express it in residual-SD units.** A delta in raw endpoint units is unreadable to a clinician; a delta of "1.4 residual SDs worse in the active arm's missing data" is arguable.

   ```
   Delta-adjustment tipping-point analysis over a grid of delta applied to
   the active arm's imputed values. Emit results/tipping_point.csv with delta
   in both raw units and residual-SD units, plus the p-value at each point,
   and state the delta at which significance is lost. Then write one sentence
   on what that magnitude of departure would mean clinically.
   ```

   If the tipping delta is small relative to the treatment effect itself, say so — that is the honest read, and it is better found by you than by a reviewer.

8. **Commit the artifact and record provenance.** The deliverable is `analysis/estimand.md`, `analysis/mmrm_primary.R`, `analysis/rbmi_sensitivity.R`, the `results/*.csv` tables, and a pinned environment (`renv.lock` for R, `requirements.txt` if any Python exploratory work is included). Emit `provenance.json` recording: R version and exact `mmrm` / `rbmi` / `mice` versions, the bioSkills commit SHA, the analysis-dataset sha256 and its extract date, the covariance structure actually used, the pilot FMI and final `m`, the RNG seed for the imputations, and the model id. Multiple imputation is stochastic — without the seed the sensitivity table is not reproducible, and that is exactly the table someone will try to reproduce.

## Why this assembly

Rung 2. This is one well-defined analytical task, and the whole value of the skill is ordering: estimand before method, MCAR test as description rather than justification, R `mmrm` rather than the Python mixed model, reference-based MI as a family rather than a single pick, and both variance estimators reported. Plain Claude Code will write competent `mmrm` and `rbmi` code from memory but reliably skips the ordering — it will happily produce an MMRM before anyone has said what the estimand is, and it will report one variance without flagging that a second exists. Nothing here needs a multi-tool harness: the data is one analysis dataset on your machine, and the escalation risk runs the other way, toward doing more modelling than the protocol pre-specified.

## Availability

Fully open, with a copyleft flag. The skill is MIT (bioSkills). `mmrm` and `rbmi` are Apache-2.0; `mice` and `mitools` are **GPL-2**, so redistributing a derived pipeline carries obligations — use the `rbmi`/`mmrm` path if that matters to you. Everything runs locally: no trial data leaves the machine, which is what makes this usable on unblinded confirmatory data at all. The *data* carries its own gate — sponsor SOPs, unblinding controls, and (for a regulatory submission) a validated-environment requirement that a laptop analysis does not satisfy. Treat the committed scripts as the specification that a validated run reproduces, not as the submission run itself.

## Compute requirements

Laptop. MMRM on a few hundred subjects across six visits fits in seconds. The binding cost is `rbmi`: imputations × bootstrap or jackknife replicates, and the jackknife variance scales with sample size. A 500-subject trial at `m = 200` with jackknife variance is minutes to low tens of minutes on 8 GB RAM; run the pilot at small `m` first, read the FMI, then commit to the final `m` rather than discovering the cost at the end. The tipping-point grid multiplies that by the number of delta values — keep the grid coarse on the first pass and refine around the crossing point.

## Evidence

Proposed. No documented attempt at running this assembly (Claude Code + the bioSkills Missing Data Sensitivity skill) on a trial endpoint is known, and no benchmark compares an agent-driven missing-data package against a statistician-authored one. The statistical content is settled and each step above traces to a specific published result:

- **Reference-based imputation has a causal justification, and it generates the tipping point.** [White, Joseph & Best, *J Biopharm Stat* (2020)](https://doi.org/10.1080/10543406.2019.1684308) show that jump-to-reference, copy-reference and copy-increments-in-reference are special cases of a potential-outcomes causal model with specific assumptions about the maintained treatment effect after discontinuation — and that varying that assumption *is* the tipping-point analysis. This is why step 5 runs the family rather than one method.
- **The variance question is real, and Rubin's estimator is information-anchored.** [Cro, Carpenter & Kenward, *JRSS-A* (2019)](https://doi.org/10.1111/rssa.12423) prove that a broad class of controlled and reference-based MI analyses are information-anchored — the proportion of information lost to missing data matches that of the primary analysis — which is the argument for reporting Rubin's variance alongside the frequentist one rather than substituting it.
- **δ- and reference-based MI as the practical sensitivity toolkit.** [Cro, Morris, Kenward & Carpenter, *Stat Med* (2020)](https://doi.org/10.1002/sim.8569) is the tutorial this workflow follows, worked through a paediatric eczema trial and a chronic-headache trial, including the choice of δ.
- **How many imputations.** [von Hippel, *Sociol Methods Res*](https://doi.org/10.1177/0049124117747303) shows the required `m` for replicable standard errors grows *quadratically* with the fraction of missing information, not linearly, and gives the two-stage pilot-then-final procedure step 5 uses. The common "5 to 10 imputations is fine" advice addresses point estimates only.

The skill contributes the ICH E9(R1) ordering and the Kenward–Roger guardrail; it does not change any of the underlying statistics.

## Alternatives considered

- **Plain Claude Code, no skill.** Reasonable if you are a trial statistician who already works estimand-first and knows the `rbmi` API — you lose little. Reach for the skill when the ordering discipline needs to survive across collaborators and runs, or when the missing-data package itself is the deliverable a regulator reads.
- **[Trial Reporting skill](../../catalog/tools/trial-reporting.html).** Covers the same MMRM/`rbmi` machinery inside a wider CONSORT reporting workflow. Use it when the missing-data analysis is one section of a full trial report; use this recipe when the sensitivity package stands alone.
- **[Adaptive Designs skill](../../catalog/tools/adaptive-designs.html).** Design-stage questions — interim analyses, sample-size re-estimation — belong there, not here. If you are still choosing the design, that is the earlier problem.
- **Doing this in Python.** Tempting for a Python-first group, and `scikit-learn`'s `IterativeImputer` (with `sample_posterior=True` and BayesianRidge) is fine for exploratory work. It is not a substitute for the confirmatory path: no Kenward–Roger correction in `statsmodels.mixedlm`, and no reference-based imputation implementation of `rbmi`'s standing. Keep Python for exploration and R for the analysis you will defend.

## See also

- [Missing Data Sensitivity (bioSkills)](../../catalog/tools/missing-data-sensitivity.html)
- [Trial Reporting (bioSkills)](../../catalog/tools/trial-reporting.html)
- [Adaptive Designs (bioSkills)](../../catalog/tools/adaptive-designs.html)
- [Draft a Phase 2/3 clinical trial protocol](draft-phase23-clinical-trial-protocol.html) — the design-stage step where the estimand should first have been written.
- [Fit a survival model to censored clinical outcomes](fit-survival-model-to-clinical-outcomes.html) — the time-to-event sibling, where censoring rather than dropout is the missing-data mechanism.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [White, Joseph & Best 2020 — causal framework for reference-based imputation and tipping point](https://doi.org/10.1080/10543406.2019.1684308) — published 2020; verified 2026-08-02 (this run).
- [Cro, Carpenter & Kenward 2019 — information-anchored sensitivity analysis (JRSS-A)](https://doi.org/10.1111/rssa.12423) — published 2019; verified 2026-08-02 (this run).
- [Cro, Morris, Kenward & Carpenter 2020 — controlled MI practical guide (Stat Med)](https://doi.org/10.1002/sim.8569) — published 2020; verified 2026-08-02 (this run).
- [von Hippel — how many imputations, quadratic rule](https://doi.org/10.1177/0049124117747303) — verified 2026-08-02 (this run).
- [ICH E9(R1) — Estimands and Sensitivity Analysis in Clinical Trials](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf) — Step 4 guideline 2019-11-20; verified 2026-08-02 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=handle-missing-endpoint-data-in-a-trial&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fhandle-missing-endpoint-data-in-a-trial.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
