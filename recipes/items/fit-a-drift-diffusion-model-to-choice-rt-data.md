---
title: Fit a drift-diffusion model to choice and reaction-time data
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-16
summary: Use the Drift-Diffusion Model skill in Claude Code with PyDDM to decompose two-choice accuracy and RT into drift rate, boundary, bias and non-decision time.
---

# Fit a drift-diffusion model to choice and reaction-time data

Take a two-alternative task's trial table — choice, correctness, reaction time, condition — and get back fitted evidence-accumulation parameters with the convergence, model-comparison and posterior-predictive checks that make them interpretable, as committed code.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A two-choice task gives you accuracy and reaction time, and neither alone answers the question you asked. A group that is slower and more accurate might be accumulating evidence more poorly, or setting a more cautious boundary, or just moving its hand more slowly — three different claims with three different neural interpretations, and mean RT plus percent-correct cannot tell them apart. The drift-diffusion model separates them into drift rate, boundary separation, starting-point bias and non-decision time, which is why it is the standard read-out for speed–accuracy tradeoff, individual-difference and model-based fMRI/EEG work.

The cost is that a DDM fit is easy to obtain and easy to over-interpret. Choices made before the optimizer runs decide the answer: which RT outliers are cut, which parameters are free versus fixed, whether the optimizer actually converged or stopped in a local minimum, and — the one most often skipped — whether the parameters are recoverable at all for your trial count and design. Reporting a drift-rate group difference from an unidentifiable fit is a real and common failure. Solved looks like: a committed script that goes from the trial table to fitted parameters plus the diagnostics, with the exclusion rule and the free-parameter set declared before fitting.

## Recommended approach

1. **Install the [Drift-Diffusion Model skill](../../catalog/tools/drift-diffusion-model.html)** in Claude Code. It is methodology guidance, not a fitting engine: it walks an eight-stage protocol (plan → clean → specify → estimate → check convergence → compare models → posterior-predictive → recover parameters) and picks a fitting tool for you based on trial counts.

2. **Add the fitting engine** (see [Dependencies](#dependencies)). PyDDM is the recommendation for maximum-likelihood fits of the full model; the skill will steer you to hierarchical Bayesian estimation instead if your per-subject trial counts are low (see [Alternatives](#alternatives-considered)).

3. **Declare the analysis before fitting it.** Have the assistant write `ddm_spec.md` alongside the code stating: the hypothesis in parameter terms ("the manipulation should change drift rate, not boundary"), the RT exclusion rule as literal bounds, which of the four parameters are free per condition and which are yoked, and the model-comparison criterion. This exists so the free-parameter set is a prediction rather than a result.

4. **Have the assistant write one versioned script:**

   ```
   Using the drift-diffusion-model skill, write me fit_ddm.py that reads
   data/trials.csv (columns: subject, condition, choice, correct, rt_ms)
   and, per subject:
   - drops RTs outside the bounds stated in ddm_spec.md, logging the
     count and proportion dropped per subject and condition
   - fits the model specified in ddm_spec.md with PyDDM, from 10 random
     starting points, keeping the best fit and recording the spread of
     final likelihoods across starts
   - fits the stated nested comparison model(s) and reports BIC for each
   - writes posterior-predictive overlays of simulated vs observed RT
     quantiles (0.1/0.3/0.5/0.7/0.9), per condition, for each subject
   Emit out/ddm_params.csv (one row per subject x condition), 
   out/model_comparison.csv, out/excluded_trials.csv, and
   out/ppc/sub-XX.png. Set and record a random seed. Every bound,
   starting-point count and parameter constraint is a named constant at
   the top of the file.
   ```

5. **Read the convergence spread and the quantile overlays before the group statistics.** If the 10 starts land on materially different likelihoods, the fit is not converged and the parameter table is noise. If the simulated RT quantiles miss the observed ones — especially the slow tail, which means fits matched only in the mean — the model is misspecified and no group contrast on its parameters is meaningful.

6. **Run the recovery check the skill's stage 8 asks for.** Simulate data from the fitted parameters at your actual trial count and design, refit with the *identical* procedure, and correlate true against recovered. Treat recovered-parameter correlations of |r| > 0.5 between parameters as an identifiability warning even when each parameter's own recovery looks fine — the classic case is boundary separation trading off against non-decision time. If you need this as a full study rather than a check, escalate to the dedicated skill named under [Alternatives](#alternatives-considered).

7. **Pin the environment and record provenance.** Emit a `requirements.txt` pinning `pyddm`, `numpy`, `scipy`, `pandas`, `matplotlib`; have the script write `out/provenance.json` with the PyDDM version, the exclusion bounds and counts, the free-parameter set, the number of starts and the random seed, the fit likelihoods and BICs, the input file `sha256`, the run date, and the model/agent identity. Optimizer runs are seed-sensitive, so recording the seed is what makes the table re-derivable — see the [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide.

The durable artifact is `ddm_spec.md` + `fit_ddm.py` + the pinned `requirements.txt` + the emitted parameter, comparison, exclusion and PPC outputs + `provenance.json`, under version control.

## Dependencies

Libraries this recipe's script installs and imports directly. Claude Code installs these into your project environment — they are not available in Claude.ai chat.

| Package | Registry | Pinned | License | Import | Source (fetched 2026-08-16) |
|---|---|---|---|---|---|
| pyddm | PyPI | `0.9.0` | MIT | `pyddm` | [Shinn et al., *eLife* 2020](https://doi.org/10.7554/eLife.56938) |

```
pip install pyddm==0.9.0
python3 -c "import pyddm"
```

Nothing is downloaded on first use. PyDDM is pure Python over NumPy/SciPy and supports multiprocessing for the fit; no compiler and no GPU. The skill itself pins no packages — the pin above is this recipe's, and it must match the `requirements.txt` the script emits.

## Why this assembly

Rung 2. The skill's value is entirely in the parts that are not code: choosing the variant, fixing versus freeing parameters, the convergence and posterior-predictive criteria, and insisting on the recovery check that unaided workflows skip. The arithmetic is one MIT library. Plain Claude Code can write a PyDDM fit in a few lines — that was never the hard part; the hard part is that a converged-looking fit of an unidentifiable model produces a clean parameter table and a publishable-looking group difference, with nothing in the output flagging the problem. There is no reason to escalate: this is a laptop-scale fit of a well-specified model with human-inspected diagnostics.

## Availability

Fully open. The Drift-Diffusion Model skill is community OSS (MIT, from the Awesome Cognitive and Neuroscience Skills collection); PyDDM is MIT. No subscription or institutional access beyond a current Claude plan. Two caveats worth knowing. The skill declares a required dependency on the collection's `research-literacy` skill — install both, or use the plugin marketplace install that brings the whole collection. And the collection's skills are **AI-generated and not individually expert-reviewed** (`review_status: ai-generated`): check the RT cutoffs and comparison criteria the skill proposes against the primary sources it cites before adopting them, which is also why step 3 of this recipe makes you write the exclusion rule down yourself.

## Compute requirements

Laptop, CPU only. A single-subject full-DDM maximum-likelihood fit over a few hundred trials is seconds to a couple of minutes depending on how many parameters are free; the multiplier is step 4's 10 random starting points and step 6's recovery simulations. A 40-subject dataset with 10 starts each is comfortably an overnight-free, coffee-length job — PyDDM's multiprocessor support makes it minutes on a modern multi-core laptop. 8 GB RAM is ample. The heavy step is the recovery study if you expand it to hundreds of ground-truth parameter sets: that is *N* × the per-fit cost and is the one thing here worth parallelizing or running on a workstation.

## Evidence

**Proposed** — no documented attempt at this exact Claude assembly (Drift-Diffusion Model skill driving PyDDM) is known. The method leg is strong and current:

- PyDDM is the published generalized-DDM framework for jointly fitting accuracy and RT, including non-standard variants like collapsing bounds and time-varying drift ([Shinn, Lam & Murray, *eLife* 2020](https://doi.org/10.7554/eLife.56938)).
- It is in active research use for exactly this decomposition: a 2026 study of six macaques on a transitive-inference transfer task used PyDDM to jointly fit accuracy and RT, and could attribute learning and transfer to drift-rate changes with little movement in the other parameters, and the eye-versus-reach RT difference almost entirely to non-decision time ([Munoz et al., *J. Cogn. Neurosci.* 2026](https://doi.org/10.1162/JOCN.a.2425)) — a worked example of the recipe's output being the scientific answer.
- The recovery and hierarchical-shrinkage concerns the recipe encodes are quantified in the HDDM paper, whose parameter-recovery studies show hierarchical Bayesian estimation outperforming both the χ²-quantile method and plain maximum likelihood when per-subject trial counts are low ([Wiecki, Sofer & Frank, *Front. Neuroinform.* 2013](https://doi.org/10.3389/fninf.2013.00014)).

The skill layer itself carries no benchmark, and its content is AI-generated (see **Availability**) — the recipe treats it as an ordering-and-checklist device over verified libraries, not as an authority on the thresholds.

## Alternatives considered

- **Hierarchical Bayesian estimation (HDDM) instead of PyDDM.** The right call when per-subject/condition trial counts are low enough that individual point estimates are unstable — hierarchical shrinkage buys real power there, and you get posterior uncertainty rather than point estimates. The cost is a heavier install (a working PyMC/Theano-class backend) and chain-mixing diagnostics in place of multi-start convergence. The skill will steer you here on trial counts; it is a substitution inside this recipe, not a different recipe.
- **EZ-diffusion.** Closed-form three-parameter summary, no software at all. Genuinely the right answer for a quick descriptive read on drift, boundary and non-decision time when you are not testing a parameter-specific hypothesis. Do not use it for model comparison.
- **Escalate the recovery study with the [Parameter Recovery Checker skill](../../catalog/tools/parameter-recovery-checker.html) (rung 3).** Reach for this when the identifiability question *is* the question — you are choosing between two model variants, or justifying a trial count for a new design. It expands step 6 into a full simulate-and-refit study with recovery quality bands, a parameter-correlation matrix and a model-recovery confusion matrix. Adding it to this recipe by default would put a second component in the path for every routine fit, which the simplicity ladder rules out.
- **Accuracy only, no RT model.** If your task has no meaningful RT (untimed, or RT not recorded), signal-detection decomposition into sensitivity and bias is the appropriate analysis and the DDM does not apply.

## See also

- [Drift-Diffusion Model (Claude Skill)](../../catalog/tools/drift-diffusion-model.html)
- [Parameter Recovery Checker (Claude Skill)](../../catalog/tools/parameter-recovery-checker.html)
- [Extract event-related potentials from EEG epochs](extract-event-related-potentials-from-eeg.html) — where the fitted trial-wise parameters go next as model-based EEG regressors.
- [Extract spectral features from resting-state EEG](extract-resting-state-eeg-spectral-features.html) — the other rung-2, laptop-scale neuroscience analysis recipe whose risk lives in undeclared analytic choices.

## Sources

- [Drift-Diffusion Model skill — `skills/drift-diffusion-model/SKILL.md`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/drift-diffusion-model/SKILL.md) — catalog `verification: works` 2026-08-03; read 2026-08-16 (this run).
- [`pyddm` on PyPI](https://pypi.org/project/pyddm/) — 0.9.0, MIT, import `pyddm`; fetched 2026-08-16 (this run).
- [Shinn, Lam & Murray, *eLife* 9:e56938 (2020), doi:10.7554/eLife.56938](https://doi.org/10.7554/eLife.56938) — PyDDM, a flexible framework for simulating and fitting generalized drift-diffusion models.
- [Munoz et al., *J. Cogn. Neurosci.* (2026), doi:10.1162/JOCN.a.2425](https://doi.org/10.1162/JOCN.a.2425) — PyDDM jointly fitting accuracy and RT in macaque transitive inference; verified 2026-08-16 (this run).
- [Wiecki, Sofer & Frank, *Front. Neuroinform.* 7:14 (2013), doi:10.3389/fninf.2013.00014](https://doi.org/10.3389/fninf.2013.00014) — HDDM and its parameter-recovery comparisons.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=fit-a-drift-diffusion-model-to-choice-rt-data&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffit-a-drift-diffusion-model-to-choice-rt-data.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
