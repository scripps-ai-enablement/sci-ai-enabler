---
title: Train a QSAR model from your own assay data and predict untested compounds
parent: All recipes
grand_parent: Recipes
nav_order: 27
problem_class: Data analysis
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-25
summary: Use the ChemLint MCP in Claude Code to clean an assay CSV, featurize, train and cross-validate a QSAR model with an applicability domain, then score an untested library.
---

# Train a QSAR model from your own assay data and predict untested compounds

Hand Claude Code a CSV of assayed analogs (`smiles` + a measured activity) and an untested library; get back a cross-validated, Y-randomization-checked QSAR model plus a scored shortlist that flags which predictions fall inside the model's applicability domain.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

A medicinal-chemistry program accumulates a few hundred to a few thousand compounds with measured activity (IC50, Ki, % inhibition) long before it has a good structure or a docking box. The recurring question is ligand-based, not structure-based: *given what we've measured, which untested compounds are worth making next?* The honest way to answer it is a QSAR model — featurize the assayed set, fit a regressor/classifier, and validate it properly (cross-validation, a held-out test split, Y-randomization to rule out chance correlation, and an applicability-domain check so you don't trust predictions on chemistry the model never saw).

Done by hand this is a notebook full of scikit-learn boilerplate that is easy to get subtly wrong: leaking the test set into feature selection, reporting a flattering R² with no Y-scramble control, or scoring library compounds that sit far outside the training space. Solved looks like: assay CSV in, a saved model + a validation report + a scored, AD-gated library out, with the descriptor set, algorithm, split seed, and cutoffs all recorded so the model can be re-fit and re-audited next quarter.

## Recommended approach

1. **Install the [ChemLint MCP](../../catalog/tools/chemlint.html)** (requires [`uv`](https://docs.astral.sh/uv/); the catalog page owns the verbatim `claude mcp add` command). It exposes 150+ cheminformatics-ML tools — cleaning, descriptors/fingerprints, 33+ ML algorithms with cross-validation and hyperparameter tuning, activity-cliff and outlier detection, and quality reporting — so the QSAR pipeline runs through tool calls instead of hand-written scikit-learn.

2. **Clean and QC the training set first.** A minimal prompt:

   ```
   Training data: data/assay.csv with columns id, smiles, ic50_nm.
   Using the ChemLint MCP:
     - Standardize/canonicalize every SMILES; drop and report rows
       that fail to parse or duplicate (keep the most potent on ties).
     - Convert ic50_nm to pIC50 = 9 - log10(ic50_nm); this is the
       regression target.
     - Run outlier and activity-cliff detection; list flagged pairs
       but do not drop them yet.
   Report rows in, rows surviving, and the pIC50 distribution.
   ```

3. **Featurize, then split before touching the test data.** Explicit prompt:

   ```
   Using ChemLint:
     - Compute ECFP4 (Morgan r=2, 2048 bit) fingerprints and, as a
       second representation, MACCS keys.
     - Make a scaffold-based train/test split (80/20) so analogs of
       the same core do not straddle the split; fix the random seed.
   ```

   A scaffold split is the honest test for lead-optimization QSAR — a random split lets near-identical analogs sit on both sides and inflates the score.

4. **Train, cross-validate, and run the chance-correlation control.** Explicit prompt:

   ```
   Using ChemLint, on the training split only:
     - Train Random Forest and gradient-boosting regressors on each
       fingerprint; 5-fold cross-validation, tune hyperparameters.
     - Report CV R2/RMSE and held-out test R2/RMSE per model.
     - Run Y-randomization (>=20 scrambles); the scrambled R2 must
       collapse toward 0 or the model is fitting noise.
   Pick the single best (representation, algorithm) by test RMSE.
   ```

5. **Score the untested library with an applicability-domain gate.** Explicit prompt:

   ```
   Using ChemLint on library/untested.csv (id, smiles):
     - Standardize and featurize with the winning representation.
     - Predict pIC50 with the saved best model.
     - Compute an applicability-domain flag (Tanimoto distance to the
       nearest training compound; in_domain = nearest >= 0.3 similarity).
     - Write predictions/scored_library.csv:
       id | smiles | pred_pIC50 | nearest_train_sim | in_domain.
     - Print the top-25 in-domain predictions, descending.
   ```

6. **Capture the durable artifact.** Have Claude write the whole run to a versioned `qsar_train.py` (load → clean → featurize → scaffold-split → train/CV/Y-scramble → save model → score library) with a pinned `requirements.txt`, and save the fitted model (`model.pkl`), the validation report, and `predictions/scored_library.csv`. Emit a `provenance.json` recording ChemLint commit, library versions (RDKit, scikit-learn), the descriptor set, algorithm, split seed, Y-scramble result, AD cutoff, input CSV sha256, run date, and model id. Keep all of it under version control — it is the audit trail for "why we made these next." Follow the [reproducibility guide](../../guide/advanced/reproducibility.html) for the artifact layout.

## Why this assembly

Rung 2 of the simplicity ladder. Every step — clean, featurize, split, train, cross-validate, Y-scramble, AD-gate, score — is a named ChemLint tool, so the whole QSAR pipeline runs from one skill with the validation controls baked in. Plain Claude Code (rung 1) can drive RDKit + scikit-learn directly, but then every run re-writes the split/CV/Y-randomization scaffolding by hand, which is exactly where QSAR pipelines leak the test set or skip the chance-correlation control. A multi-tool harness (rung 3) adds nothing: this is one library applied in sequence, no second data source to orchestrate. An autonomous system (rung 4) is unmotivated — there is no open-ended search here, only a fixed, auditable pipeline whose provenance the chemist needs to see.

## Availability

Fully open. [ChemLint](../../catalog/tools/chemlint.html) is MIT-licensed (molML/TU Eindhoven) and computes locally on the molecules you supply — no data leaves the machine, no subscription, no institutional access. RDKit (BSD-3) and scikit-learn (BSD-3) are its dependencies. Any current Claude plan supports the MCP install.

## Compute requirements

Laptop. Featurizing and training on a few thousand compounds with fingerprint descriptors and tree-based models runs in seconds to a couple of minutes on a single CPU core and fits in <4 GB RAM. Y-randomization multiplies training time by the scramble count (~20×) but each fit is cheap. Scoring a 10⁵-compound library is fingerprint-featurization-bound, still minutes on a laptop. No GPU needed; only deep-learning representations (which ChemLint also offers) would want one.

## Evidence

Proposed. No published benchmark of an LLM-driven ChemLint QSAR workflow is known. The pipeline it drives, however, is the field-standard method, and a current exemplar builds exactly this stack by hand: Alzahrani et al. ([*Mol. Divers.* 2026](https://pubmed.ncbi.nlm.nih.gov/41961390/)) trained a MACCS-fingerprint Random Forest QSAR for SMYD3 modulators with cross-validation, an explicit applicability domain, Y-randomization, and SHAP interpretability, then applied it to an external library scoring only in-domain compounds — the same clean→featurize→train→validate→AD-gate→score sequence this recipe automates. The multi-descriptor, multi-algorithm ML-QSAR pattern with recursive feature selection and applicability-domain / decoy validation is well established for ChEMBL-anchored repurposing (e.g. Kamboj et al., [*Comput. Struct. Biotechnol. J.* 2022](https://pubmed.ncbi.nlm.nih.gov/35832613/), Pearson r 0.80–0.92 in 10-fold CV). Each component (RDKit featurization, scikit-learn models, Y-scramble, Tanimoto AD) has independent validation; the Claude+ChemLint assembly does not. Treat every prediction as a prioritization hypothesis to confirm at the bench.

## Alternatives considered

- **Plain Claude Code, no MCP (rung 1).** Fine for a quick RandomForest sanity model on a clean CSV, but you re-write the scaffold-split / CV / Y-randomization / AD scaffolding each session — the exact places QSAR silently overfits. Reach for it only when you cannot install the MCP.
- **[Benchmark an ADMET property with PyTDC](benchmark-admet-property-with-pytdc.html).** Use that recipe when the endpoint is a *standard* ADMET property with an established public benchmark and you want to compare models against a leaderboard. This recipe is for a *bespoke* target/assay where the labels are your own measurements, not a public benchmark set.
- **[Analyze the SAR of a compound series](analyze-sar-of-a-compound-series.html).** That recipe explains *what drives* activity in an already-measured series (R-group decomposition, activity cliffs); this one *predicts* activity for compounds you have not measured. Run the SAR analysis first to understand the series, then this to score the next batch.
- **[Rank a compound library by predicted binding affinity](rank-compound-library-by-predicted-affinity.html).** That is structure-based (needs a target sequence/structure); reach for it when you have a target but little assay data. This QSAR path is the mirror image — lots of assay data, no structure needed.

## See also

- [ChemLint (MCP server)](../../catalog/tools/chemlint.html)
- [Benchmark an ADMET property with PyTDC](benchmark-admet-property-with-pytdc.html)
- [Analyze the SAR of a compound series](analyze-sar-of-a-compound-series.html)
- [Rank a compound library by predicted binding affinity](rank-compound-library-by-predicted-affinity.html)

## Sources

- [`molML/ChemLint`](https://github.com/molML/ChemLint) — verified 2026-07-25 (this run, via catalog page `last_verified` 2026-06-13 / verified 2026-07-20).
- [Alzahrani A.R. et al. — Predictive bioactivity modeling for SMYD3 modulators, *Mol. Divers.* 2026](https://pubmed.ncbi.nlm.nih.gov/41961390/) — published 2026-01; verified 2026-07-25 (this run).
- [Kamboj S. et al. — QSAR and machine learning for repurposed drugs against HCV, *Comput. Struct. Biotechnol. J.* 2022](https://pubmed.ncbi.nlm.nih.gov/35832613/) — published 2022; verified 2026-07-25 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=train-qsar-model-from-assay-data&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftrain-qsar-model-from-assay-data.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
