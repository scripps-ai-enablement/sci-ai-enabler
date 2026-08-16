---
title: Design a group-sequential trial with interim looks
parent: All recipes
grand_parent: Recipes
nav_order: 8
problem_class: Experimental design
subject_areas: [Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-09
summary: Use the Adaptive Designs skill and rpact to fix boundaries, simulate operating characteristics, and pre-specify any sample-size re-estimation rule before enrolment.
---

# Design a group-sequential trial with interim looks

You want interim analyses so the trial can stop early for efficacy or futility — and possibly grow if the interim result is borderline. Fix the alpha-spending boundaries, simulate what the design actually does under effects you might really see, and write the adaptation rule into the protocol before the first patient enrols.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A fixed-sample trial commits everything up front: you pick an effect size, size for it, and find out at the end whether you guessed right. Interim looks buy you the option to stop early when the drug clearly works or clearly does not, and — with a sample-size re-estimation (SSR) rule — the option to add patients when the interim result is promising but underpowered. That option is why sponsors want adaptive designs, and it is also where the design goes wrong.

Three failure modes recur. First, the boundaries get chosen by reputation ("we'll use O'Brien–Fleming") rather than by what the spending function does to the maximum sample size and the stage-wise stopping probabilities. Second, the SSR rule is bolted on without simulating it: the promising-zone construction is intuitive and widely copied, but the region where extra patients buy the most power is not the region the standard rule triggers on, and in time-to-event trials the efficiency case for SSR over a plain group-sequential design largely evaporates. Third — the one that ends careers rather than trials — the adaptation rule is left vague in the protocol, so the decision at the interim looks like it was informed by the unblinded data, and the type I error argument collapses.

Solved looks like: a committed design script that regenerates the boundaries and the simulated operating characteristics from scratch, a pre-specified SSR rule (or a documented decision not to have one), and a Statistical Analysis Plan section that a reviewer can read without asking what would have happened in the cases that did not occur.

## Recommended approach

1. **Install the [Adaptive Designs skill](../../catalog/tools/adaptive-designs.html)** and the R packages it drives (`rpact`, `gsDesign`, `gsDesign2`, `simtrial`). Install paths are on the catalog page. Pin the versions now — boundary values are software output and you will be asked to reproduce them years later.

2. **Write down the fixed design first, and keep it.** Before any adaptation, ask the agent to size the conventional single-look trial for the same endpoint, effect size and power. This is the comparator every later claim is made against, and if the adaptive design does not beat it on expected sample size or expected power, you have found that out for the price of one function call.

   ```
   Use the adaptive-designs skill. Write design/00_fixed_reference.R:
   sample size for a two-arm trial, <endpoint type>, target effect <delta>,
   assumed SD/event rate <...>, two-sided alpha 0.025 (one-sided), power 0.90,
   allocation 1:1, expected dropout <x>%. Report n per arm and total.
   Do not add interim analyses yet.
   ```

3. **Choose the spending function by what it does, not by its name.** Have the agent tabulate two or three candidate designs side by side rather than returning one. The comparison that matters is the *inflation factor* (maximum n versus the fixed design), the boundary z-value at the first look, and the probability of stopping at each stage under both the null and the target alternative.

   ```
   Write design/01_boundaries.R using rpact. Compare, in one table:
   (a) O'Brien-Fleming-type alpha spending, (b) Pocock-type, (c) Lan-DeMets
   with a Kim-DeMets rho=2 spending function -- each with <k> looks at
   information fractions <...>, plus a non-binding futility boundary on
   the beta-spending scale. Emit results/boundary_comparison.csv with, per
   design: max n, inflation factor vs the fixed design, critical value and
   nominal alpha at each look, and cumulative stopping probability per
   stage under H0 and under the target alternative.
   ```

   Record whether the futility boundary is **binding or non-binding** as an explicit field. A binding boundary buys back alpha but obliges you to stop; teams routinely take the alpha and then cross it anyway, which invalidates the type I error control they claimed.

4. **Simulate the operating characteristics across an effect grid, not at the design point.** Boundary calculations answer "what happens if the true effect is exactly delta". That is the one scenario you can be sure of not being in. Ask for a simulation over a grid spanning the null, the minimum clinically important difference, and the optimistic value, and read the expected sample size row as carefully as the power row.

   ```
   Write design/02_operating_characteristics.R. Simulate each candidate
   design over a grid of true effects from 0 to <1.5x delta> in <n> steps,
   >= 10000 replicates, fixed RNG seed. Emit results/oc_grid.csv: per design
   and per true effect -- overall power, probability of stopping for
   efficacy at each look, probability of stopping for futility, expected
   total sample size, and expected study duration.
   ```

5. **Decide on sample-size re-estimation explicitly, and justify it against step 4.** SSR is an addition to a group-sequential design, not a substitute for one, and the default answer should be *no* unless the simulation shows a gain. If you do add it, pre-specify the rule completely — the zone boundaries, the target conditional power, the maximum multiple of the planned n, and the test statistic used at the final analysis (a weighted / combination test, or the unweighted statistic under an explicitly checked constraint).

   ```
   Extend the simulation to a promising-zone SSR variant of the chosen
   design: interim CP thresholds <...>, max sample size multiple <...>,
   final analysis via the Cui-Hung-Wang weighted statistic. Add rows to
   results/oc_grid.csv so the SSR and non-SSR designs are directly
   comparable on unconditional power, expected n, and expected n given
   the trial lands in the promising zone. Then state in one paragraph
   whether SSR is worth it here relative to simply adding a later look.
   ```

   For a **time-to-event** endpoint, treat the answer as presumptively no and require the simulation to overturn it (see **Evidence**). Also record whether extra events would be obtained by following the existing cohort or by enrolling more patients — those are different trials and they estimate different things when the hazard ratio is not constant.

6. **Write the pre-specification, and be concrete about what is fixed.** The SAP section must name the spending function and its parameter, the exact information fractions at which looks occur (and what happens if the actual information differs), the futility rule and its binding status, the SSR rule as a deterministic function of the interim statistic, the IDMC firewall — who sees unblinded data and who does not — and the estimator reported at the end. Adaptation biases the naive maximum-likelihood estimate; state that a bias-adjusted estimate and a repeated-confidence-interval will be reported alongside it, and generate both in the analysis script rather than promising them.

   ```
   Draft design/SAP_adaptive_section.md against the FDA 2019 Adaptive
   Designs guidance. Cover: design type and rationale, spending function
   and parameter, look schedule and the rule if actual information differs
   from plan, futility rule and binding status, the SSR rule as an explicit
   function, the combination test used at the final analysis, IDMC charter
   and firewall, and the estimation strategy (point estimate, bias-adjusted
   estimate, repeated confidence intervals). Flag every place where ICH E20
   is cited that E20 is still a draft at Step 2b, not final guidance.
   ```

7. **Commit the artifact and record provenance.** The deliverable is `design/00_fixed_reference.R`, `design/01_boundaries.R`, `design/02_operating_characteristics.R`, `design/SAP_adaptive_section.md`, the `results/*.csv` tables, and a pinned environment (`renv.lock`). Emit `provenance.json` with: R version and exact `rpact` / `gsDesign` / `simtrial` versions, the bioSkills commit SHA, the RNG seed and replicate count for every simulation, the assumed nuisance parameters (SD, control event rate, accrual and dropout) with their source, and the model id. Simulation results are stochastic; without the seed and replicate count the operating-characteristics table is a screenshot, not a result.

## Why this assembly

Rung 2. One skill, one endpoint, one design decision — the machinery is a mature R package and the value the skill adds is the *ordering and the pre-specification discipline*: fixed-design reference before adaptive design, boundary comparison before boundary choice, simulation before SSR, and an SAP section that names the estimator. Plain Claude Code will write plausible `rpact` calls from memory, but it does not by default produce the fixed-design comparator, does not simulate off the design point, and will cheerfully hand you a promising-zone rule without the weighted statistic that makes it valid. Nothing here needs a toolbelt: the inputs are a handful of numbers and the outputs are three tables. Escalation risk points the other way — toward designing something more adaptive than the trial can operationally support.

## Availability

Fully open. The skill is MIT (bioSkills). `rpact` 4.4.0 is **LGPL-3** and `gsDesign` is GPL-3, so a derived pipeline you redistribute carries copyleft obligations; check that before shipping the scripts inside a commercial product. Everything runs locally — no protocol assumptions or trial parameters leave the machine, which is what makes this usable on a confidential development plan. The commercial alternatives the skill names (East/EastHorizon, FACTS, ADDPLAN) are licensed products and are not installed. The *regulatory* gate is separate from the software one: a design intended for a marketing application will need sponsor-statistician sign-off and, in most cases, discussion with the regulator, and a laptop run is the specification for that conversation rather than a substitute for it.

## Compute requirements

Laptop. Boundary computation in `rpact` is effectively instantaneous. The cost is step 4: a 10,000-replicate simulation across a 10-point effect grid for three candidate designs is seconds to a couple of minutes for continuous or binary endpoints, and minutes to low tens of minutes for survival designs where each replicate simulates accrual, follow-up and event times. Run the grid coarse at 1,000 replicates while the design is still moving, then re-run at 10,000+ with the final seed for the numbers that go in the SAP — Monte-Carlo error on a stopping probability at 1,000 replicates is around one percentage point, which is enough to reorder two close designs.

## Evidence

Proposed. No documented attempt at running this assembly (Claude Code + the bioSkills Adaptive Designs skill) to design a trial is known, and no benchmark compares an agent-drafted adaptive design against a statistician-authored one. The statistical content is well established, and the specific gates above each trace to a published result:

- **The promising-zone rule triggers in the wrong place.** [Jennison & Turnbull, *Stat Med* (2015)](https://doi.org/10.1002/sim.6575) show that the greatest gains in power per additional observation lie *outside* the region defined by the Chen–DeMets–Lan condition that the Mehta–Pocock method uses, and that targeting a fixed conditional power produces very large increases over a narrow band of interim outcomes where moderate increases over a wider band would be more efficient. This is why step 5 requires simulation rather than adoption.
- **Optimal promising-zone rules exist, and the objective matters.** [Mehta, Bhingare, Liu & Senchaudhuri, *Stat Med* (2022)](https://doi.org/10.1002/sim.9339) derive optimal SSR decision rules and make explicit the tension between optimising unconditional and conditional power — the two objectives give different rules, so the SAP has to say which one it is.
- **For time-to-event endpoints the default should be no SSR.** [Freidlin & Korn, *Clinical Trials* (2017)](https://doi.org/10.1177/1740774517724746) show by simulation that, given the lack of an efficiency advantage over group-sequential designs, sample-size adjustment in the time-to-event setting lets interim information about the *shape* of the survival curves be used to enlarge the observed effect, and increases the probability of recommending an ineffective therapy when curves cross. Their conclusion is that such designs "remain unjustified" in that setting.
- **What must be written in the protocol is a known, delineable list.** [Shih, Li & Wang, *Contemp Clin Trials* (2016)](https://doi.org/10.1016/j.cct.2015.12.007) compare the likelihood, weighted, dual-test and promising-zone approaches, show that the dual test's sample-size rules *conflict* with the promising-zone rules, and set out explicitly what has to be specified in the protocol for the procedure to be valid versus what can be left implicit. Step 6's checklist follows that division.
- **The construction is still being extended, which is an argument for simulating your own case.** Recent work adapts promising-zone designs to delayed immunotherapy effects with a critical-value adjustment to control type I error inflation ([Li, Yan & Jiang, *J Biopharm Stat* (2025)](https://doi.org/10.1080/10543406.2024.2341674)) and to exact two-stage binary designs, where the promising-zone variant balances power against expected n better than the pure adaptive one ([Tang & Shan, *Stat Methods Med Res* (2026)](https://doi.org/10.1177/09622802251399914)).

The skill contributes the regulatory anchoring (FDA 2019 final guidance; ICH E20 flagged as draft) and the workflow ordering; it does not change the underlying statistics.

## Alternatives considered

- **Plain Claude Code with `rpact` directly.** Fine if you are a trial statistician who already runs the fixed-design comparator and simulates operating characteristics as a matter of habit — the skill mainly enforces what you would do anyway. Reach for the skill when the design has to be defended to a regulator by someone who did not build it.
- **A fixed-sample design.** Genuinely the right answer more often than the adaptive-design literature implies, especially for short-duration endpoints where an interim look arrives too late to save anything. Step 2 exists so that this stays a live option rather than a rhetorical one.
- **[Bayesian Trials skill](../../catalog/tools/bayesian-trials.html).** If the design question is a predictive-probability stopping rule, a borrowing prior, or a Bayesian dose-finding scheme rather than frequentist alpha spending, start there instead.
- **[Draft a Phase 2/3 clinical trial protocol](draft-phase23-clinical-trial-protocol.html).** The protocol document is a wider deliverable; this recipe produces the statistical design that goes inside it. Do the design first — retrofitting an adaptive design into a written protocol is how the pre-specification gets vague.
- **Commercial design software (East/EastHorizon, FACTS, ADDPLAN).** Standard in large sponsor organisations and often what a regulator has seen before. Use them where an internal SOP requires a validated design environment; the scripts from this recipe are still useful as the independent cross-check.

## See also

- [Adaptive Designs (bioSkills)](../../catalog/tools/adaptive-designs.html)
- [Bayesian Trials (bioSkills)](../../catalog/tools/bayesian-trials.html)
- [Design a Bayesian trial that borrows external control data](design-a-bayesian-trial-that-borrows-external-data.html) — the other-framework sibling: reach for it when the external information is the point rather than the interim looks.
- [Draft a Phase 2/3 clinical trial protocol](draft-phase23-clinical-trial-protocol.html)
- [Handle missing endpoint data in a confirmatory trial](handle-missing-endpoint-data-in-a-trial.html) — the analysis-stage sibling, where the estimand fixed at design time gets defended.
- [Fit a survival model to censored clinical outcomes](fit-survival-model-to-clinical-outcomes.html)
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [Jennison & Turnbull 2015 — pitfalls in adaptive sample size modification (Stat Med)](https://doi.org/10.1002/sim.6575) — published 2015; verified 2026-08-09 (this run).
- [Mehta, Bhingare, Liu & Senchaudhuri 2022 — optimal adaptive promising zone designs (Stat Med)](https://doi.org/10.1002/sim.9339) — published 2022; verified 2026-08-09 (this run).
- [Freidlin & Korn 2017 — sample size adjustment with time-to-event outcomes: a caution (Clinical Trials)](https://doi.org/10.1177/1740774517724746) — published 2017; verified 2026-08-09 (this run).
- [Shih, Li & Wang 2016 — flexible sample-size design methods compared (Contemp Clin Trials)](https://doi.org/10.1016/j.cct.2015.12.007) — published 2016; verified 2026-08-09 (this run).
- [Li, Yan & Jiang 2025 — adaptive promising zone design with delayed treatment effect (J Biopharm Stat)](https://doi.org/10.1080/10543406.2024.2341674) — published 2025; verified 2026-08-09 (this run).
- [Tang & Shan 2026 — adaptive SSR designs for two-stage binary trials (Stat Methods Med Res)](https://doi.org/10.1177/09622802251399914) — published 2026; verified 2026-08-09 (this run).
- [`rpact` on CRAN](https://cran.r-project.org/web/packages/rpact/index.html) — version 4.4.0, published 2026-03-04, LGPL-3; verified 2026-08-09 (this run).
- [FDA — Adaptive Designs for Clinical Trials of Drugs and Biologics (final guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adaptive-design-clinical-trials-drugs-and-biologics-guidance-industry) — final 2019-11-29.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=design-a-group-sequential-trial-with-interim-looks&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fdesign-a-group-sequential-trial-with-interim-looks.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
