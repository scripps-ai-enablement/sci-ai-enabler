---
title: Fit a dose-response curve and report a defensible IC50
parent: All recipes
grand_parent: Recipes
nav_order: 12
problem_class: Data analysis
subject_areas: [Chemistry, Drug Repurposing and Discovery, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-02
summary: Drive the ToolUniverse Dose-Response skill to fit 4PL curves to plate-assay data, gate them on fit quality, and emit IC50 with AUC and per-replicate spread.
---

# Fit a dose-response curve and report a defensible IC50

You have concentration-response readings off a plate and need a potency number you can defend in a figure caption. Drive the ToolUniverse Dose-Response skill to fit the four-parameter logistic model, refuse the curves that do not support an IC50, and write the result to a versioned table.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You ran an eight- or ten-point dilution series in triplicate — enzyme inhibition, cell viability, a receptor agonist titration — and the next step is an IC50 or EC50 per compound. The arithmetic is easy and that is the trap. A 4PL fit will return a confident IC50 for a curve that never reached its bottom plateau, for a biphasic curve where the model is simply wrong, and for a dataset where the three replicates disagree by half a log. It will also return a number that does not survive comparison with another lab's number for the same compound, because IC50 is the least portable of the available potency metrics.

"Solved" looks like: a per-compound potency table where every row carries its fit quality, its concentration units, and its replicate spread; a companion table of the curves that were *rejected* and why; a portable metric alongside IC50 for cross-study comparison; and a committed command file so the next plate gets analysed the same way rather than re-litigated in chat.

## Recommended approach

1. **Install the ToolUniverse MCP server, then the Dose-Response skill** ([catalog page](../../catalog/tools/tooluniverse-dose-response.html)). The skill is a reasoning layer over ToolUniverse tool calls, so register the server first:

   ```
   claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
   npx skills add mims-harvard/ToolUniverse
   ```

   The skill sets `disable-model-invocation: true`, so invoke it explicitly.

2. **Shape the input to one committed long-format CSV**, `doseresponse_input.csv`, one row per well:

   ```
   compound_id,replicate,plate,concentration,conc_units,response,response_scale
   AZ-114,1,P03,0.003,uM,98.4,percent_of_control
   AZ-114,1,P03,0.010,uM,94.1,percent_of_control
   ```

   Three rules the skill enforces and you should encode in the file rather than argue about later: concentrations go on a **linear** scale, not log — the fitter logs them itself; zero-concentration wells are dropped from the fit and kept as the control that defines 100%; and each series needs **at least four points spanning both the upper and lower plateaus**. Record what "control" meant (vehicle wells, untreated wells, a positive-control floor) as a column or in the commit message — a normalization you cannot reconstruct makes every downstream number unreproducible.

   Keep replicates as **separate rows**. Do not average them before fitting. Averaging first collapses exactly the inter-experiment variability you need to report.

3. **Commit the analysis as a parameterized command file**, `.claude/commands/fit-dose-response.md`, so every plate is analysed by the same text:

   ```markdown
   Use the dose-response skill on $ARGUMENTS (a long-format CSV:
   compound_id, replicate, plate, concentration, conc_units, response,
   response_scale).

   For each compound_id x replicate:
     1. Fit the 4PL/Hill model with DoseResponse_calculate_ic50.
        Concentrations are already linear; do not re-transform them.
     2. Emit one row to fit_params.csv: compound_id, replicate,
        n_points, ic50, ic50_ci_low, ic50_ci_high, conc_units,
        hill_slope, emax, emin, r_squared, plateau_reached
        (top/bottom/both/neither).
     3. Emit AUC over the FIXED concentration window given below,
        computed from the fitted curve, as auc_trunc in the same row.

   Send a curve to rejected_curves.csv with a reason string, and emit
   NO ic50 for it, when any of these holds:
     - the response is non-monotonic or biphasic (4PL does not apply)
     - r_squared < 0.90
     - neither plateau is reached

   Mark, but do not reject, rows with one plateau missing: set
   ic50_qualifier = "approximate, extrapolated".
   Flag hill_slope > 1.5 or < 0.5 in a hill_flag column.

   Then, per compound_id, write summary.csv with the geometric mean
   IC50 across replicates, the min and max, and n_replicates. Do not
   report a single pooled IC50 without the spread.

   State a potency comparison between two compounds ONLY if both reach
   r_squared >= 0.95 with concordant Hill slopes; otherwise say the
   comparison is not supported and stop.

   Cite only values present in fit_params.csv. Do not state an IC50
   you did not read back from a fit.

   Fixed AUC window: 0.01-30 uM.
   ```

   Run it as `/fit-dose-response doseresponse_input.csv`.

4. **Emit AUC over a fixed truncated window alongside IC50, not instead of it.** If your potency number will ever be compared against another platform, another screen, or a public pharmacogenomics resource, IC50 is the fragile metric: a survey of curve-fitting protocols across large pharmacogenomics screens found that **AUC derived from a sigmoidal fit over a truncated dose range** gave the strongest agreement between platforms, and also the best alignment across successive versions of the *same* platform ([Chen et al., *Bioinformatics* 2026](https://pubmed.ncbi.nlm.nih.gov/42286248/)). Fix the window once, write it into the command file, and never change it silently — a shifted window is a silently changed metric.

5. **Read the rejected table before the accepted one.** A biphasic curve is a finding, not a fit failure: dose-dependent stimulation before inhibition is real in resistance biology and a monotonic sigmoid discards it ([Zhang et al., *PLOS ONE* 2013](https://doi.org/10.1371/journal.pone.0069301)). A Hill slope near 2 with a good r² usually means cooperativity, aggregation, or a compound precipitating at the top concentrations — inspect the top-dose wells before you believe the potency.

6. **Plot every accepted curve and look at it.** Overlay the fitted sigmoid on the raw points per compound, with replicates in distinct markers. Use whatever plotting library your project already pins — this recipe adds no new dependency. A curve whose r² passes but whose points cluster in two dose bins is not a dose-response experiment; it is two doses with a line through them.

7. **Write `provenance.json` next to the outputs**: ToolUniverse version, the ToolUniverse repo commit SHA the skill came from, the sha256 of `doseresponse_input.csv`, the control definition and response scale, the fixed AUC window, the r² gate, the model id that ran the command, and the UTC date. Commit `.claude/commands/fit-dose-response.md`, `doseresponse_input.csv`, `fit_params.csv`, `rejected_curves.csv`, `summary.csv`, and `provenance.json` together — see [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html).

## Why this assembly

Rung 2 of the simplicity ladder. The 4PL fitter and the potency comparison ship as ToolUniverse tools, and the skill is the layer that applies the input contract and the quality gates — one skill plus its MCP server fully solves the problem, so stop here. Rung 1 (Claude Code alone) can write a `scipy.optimize.curve_fit` 4PL in a minute, and that is exactly the failure mode this recipe exists to prevent: an unguarded fitter returns an IC50 for a plateau-less curve and for biphasic data without complaint, and the gates are what make the number defensible. Rung 3 adds nothing — no second tool is needed to fit a sigmoid. If you need hierarchical Bayesian potency estimates with full posteriors across many experiments, that is a different statistical tool, not a bigger toolbelt (see Alternatives).

## Availability

Fully open. ToolUniverse is Apache-2.0 and the curve fitting is local computation over your own assay data — no external API is queried, no compound structure or assay result leaves the machine. There is no subscription, licence, or data-residency gate, which makes this usable on unpublished internal screening data.

## Compute requirements

Laptop. A 4PL fit over ten points is milliseconds; wall-clock is dominated by the skill's reasoning, not the arithmetic. No GPU. A plate of 96 series returns in a few minutes, essentially all of it model latency — if you are analysing hundreds of plates, batch by plate and checkpoint `fit_params.csv` incrementally rather than issuing one enormous request.

## Evidence

Proposed. No documented attempt of this specific Claude-driven ToolUniverse Dose-Response assembly on a real assay is known, and the skill's integrated workflow is not benchmarked end-to-end. The grounding is in the individual design decisions, each of which traces to a published result:

- **4PL/Hill as the model, IC50 with Hill coefficient as the report** is the field standard for concentration-effect data, and the point "best fit" values usually reported understate uncertainty — hierarchical Bayesian fitting of the same curves recovers parameter distributions and quantifies inter-experiment variability, which is why step 3 reports replicate spread rather than a single pooled number ([Johnstone et al., *Wellcome Open Research* 2016](https://doi.org/10.12688/wellcomeopenres.9945.2)).
- **Truncated-range AUC as the portable metric** is measured, not preference: across pharmacogenomics screens with differing platforms and metrics, sigmoid-fit AUC on a truncated dose window beat IC50, EC50, and full-range AUC for cross-platform agreement ([Chen et al., *Bioinformatics* 2026](https://pubmed.ncbi.nlm.nih.gov/42286248/)).
- **Rejecting non-monotonic data from 4PL** rather than fitting it anyway: traditional monotonic sigmoids fail on such data and discard observations of biological significance, demonstrated on HIV mutant resistance curves where nonparametric local-polynomial fits were needed instead ([Zhang et al., *PLOS ONE* 2013](https://doi.org/10.1371/journal.pone.0069301)).

The skill's own `SKILL.md` documents the same input contract (linear concentrations, zero-dose exclusion, four-point minimum spanning both plateaus), the same r² = 0.90 inspection trigger, and the same r² ≥ 0.95 plus concordant-slope bar for endorsing a potency comparison; the recipe adds the durable artifact and the AUC column.

## Alternatives considered

- **A hand-written 4PL in `scipy`, `drc` (R), or GraphPad Prism.** Same math, and Prism in particular is what most wet labs already use. Reach for them when you are inside an existing pipeline or a validated SOP. The skill's contribution is the input contract and the refusal rules; if you write your own, port the gates in step 3 or you will publish an extrapolated IC50 eventually.
- **Hierarchical Bayesian fitting (`PyHillFit`-class).** Choose this when the question is about *uncertainty* — propagating potency error into a downstream simulation, or separating within- from between-experiment variance across many replicates. It is the right tool for that and is not in `catalog/tools/`, so it is an external alternative rather than a recipe.
- **Nonparametric fitting for biphasic curves.** When step 5 rejects a curve as non-monotonic and the biphasic shape is the actual result, a local-polynomial or nonparametric IC50 estimate is the documented path ([Zhang et al. 2013](https://doi.org/10.1371/journal.pone.0069301)). No catalogued component covers it; do not force a 4PL.
- **Going straight to synergy scoring.** If you already have single-agent potency and the question is a two-drug combination, skip to [Score a drug-combination screen for synergy](score-drug-combination-synergy.html) — it needs the numbers this recipe produces.

## See also

- [Dose-Response Analysis (ToolUniverse Claude Skill)](../../catalog/tools/tooluniverse-dose-response.html)
- [ToolUniverse (MCP server)](../../catalog/tools/tooluniverse.html)
- [Score a drug-combination screen for synergy](score-drug-combination-synergy.html) — downstream consumer of single-agent potency.
- [Analyze the SAR of a compound series](analyze-sar-of-a-compound-series.html) — where a table of potencies goes next.
- [Train a QSAR model from assay data](train-qsar-model-from-assay-data.html) — the fit table as model training data.
- [Source purchasable compounds for a hit list](source-purchasable-compounds-for-a-hit-list.html) — the ≥ 98% purity grade this recipe's assays need.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse) — component facts deferred to the catalog page, `last_verified` 2026-08-02.
- [`skills/tooluniverse-dose-response/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-dose-response/SKILL.md) — via catalog page, verified 2026-08-02 (this run).
- [Chen AT, Kelly MR, Ideker T, Mattson NM. "Harmonization and integration of pharmacogenomics screens." *Bioinformatics* (2026)](https://pubmed.ncbi.nlm.nih.gov/42286248/) — published 2026; retrieved 2026-08-02 (this run).
- [Johnstone RH, Bardenet R, Gavaghan DJ, Mirams GR. "Hierarchical Bayesian inference for ion channel screening dose-response data." *Wellcome Open Research* (2016)](https://doi.org/10.12688/wellcomeopenres.9945.2) — published 2016; retrieved 2026-08-02 (this run).
- [Zhang H, Holden-Wiltse J, Wang J, Liang H. "A strategy to model nonmonotonic dose-response curve and estimate IC50." *PLOS ONE* 8(8):e69301 (2013)](https://doi.org/10.1371/journal.pone.0069301) — published 2013; retrieved 2026-08-02 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=fit-dose-response-curve-to-ic50&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffit-dose-response-curve-to-ic50.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
