---
title: Predict hospital readmission from EHR data
parent: All recipes
grand_parent: Recipes
nav_order: 38
problem_class: Data analysis
subject_areas: [Translational Medicine]
evidence_level: Proposed
complexity: One skill or MCP
availability: Institutional access
compute_requirements: Workstation with GPU
last_verified: 2026-06-21
summary: Use the PyHealth Claude Skill to build a 30-day readmission predictor on MIMIC/OMOP EHR data with a reproducible dataset → task → model → metrics pipeline.
---

# Predict hospital readmission from EHR data

Point Claude at a credentialed EHR dataset (MIMIC-IV, eICU, or an OMOP CDM export); get back a trained 30-day readmission model with held-out AUROC/AUPRC, calibration, and a reproducible five-stage pipeline — without hand-writing the cohort extraction, sequence encoding, and training loop.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Institutional access |
| **Compute** | Workstation with GPU |

## Problem

A clinical data scientist with access to a credentialed EHR dataset wants a defensible readmission risk model: take the admissions table, define a 30-day all-cause readmission label, encode each patient's diagnosis/procedure/medication history, train a sequence model, and report honest held-out discrimination and calibration. Doing this from scratch means writing brittle cohort SQL, deciding how to encode ICD/ATC code sequences, building a padded-sequence data loader, and wiring a training loop — every team reinvents it, and results rarely reproduce because the preprocessing is undocumented. PyHealth standardizes the whole thing into a dataset → task → model → trainer → metrics pipeline over harmonized EHR schemas. Solved looks like: name the dataset and the task, get a trained model with cross-validated AUROC/AUPRC and a calibration read, plus the exact pipeline so a reviewer can rerun it.

## Recommended approach

1. **Install the [PyHealth skill](../../catalog/tools/pyhealth.html)** from the K-Dense collection:

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   ```

   Enable the `pyhealth` skill when prompted. Claude runs the skill's Python locally via Bash; it declares its own dependencies (install on first use). Have your credentialed dataset already downloaded locally — PyHealth reads it from disk.

2. **Load the dataset and confirm the schema.** PyHealth's dataset classes (`MIMIC4Dataset`, `eICUDataset`, `OMOPDataset`) expect a specific table layout; let Claude confirm the parse before modeling:

   ```
   Use the pyhealth skill. Load my local MIMIC-IV v3 extract from
   /data/mimic4 with the MIMIC4Dataset class, including the
   diagnoses, procedures, and prescriptions tables. Report the number
   of patients, visits, and the available code vocabularies
   (ICD-10-CM, ICD-10-PCS, NDC), and confirm the parse before we
   define a task.
   ```

3. **Define the readmission task explicitly.** PyHealth ships a `readmission_prediction` task function with a configurable time window; pin the 30-day window and state the label definition:

   ```
   Define a 30-day all-cause readmission prediction task using
   PyHealth's readmission task function (time_window=30 days). Report
   the resulting sample count, the positive (readmitted) rate, and how
   index visits with insufficient lookback or in-hospital death are
   handled. State the exact label definition.
   ```

4. **Train a sequence model with an honest split.** Use a clinical sequence model (RETAIN is interpretable; Transformer is a strong baseline) and a patient-level split so no patient leaks across folds:

   ```
   Train a RETAIN model on the readmission task with a patient-level
   70/10/20 train/val/test split (no patient in more than one fold).
   Use the PyHealth Trainer with early stopping on validation AUPRC.
   Report training/validation curves and the chosen hyperparameters.
   ```

5. **Report discrimination, calibration, and a baseline.** A single AUROC is not enough; require AUPRC (the class is imbalanced), calibration, and a logistic-regression baseline so the deep model has to earn its complexity:

   ```
   On the held-out test set report AUROC, AUPRC, and a calibration
   curve (or Brier score) for RETAIN, and compare against a simple
   logistic-regression baseline on count-encoded codes. State whether
   the deep model beats the baseline on AUPRC and by how much.
   ```

6. **State the caveats.** Require the summary to note that readmission labels are sensitive to the lookback/death-handling choices, that performance does not transfer across institutions without recalibration, that the model is a research artifact (not a deployed clinical tool), and that any reporting must respect the dataset's data-use agreement. Save the pipeline script and metrics for review.

## Why this assembly

Rung 2 of the simplicity ladder. One Claude Skill wraps PyHealth's entire five-stage pipeline — harmonized dataset loaders, prebuilt clinical tasks, sequence models, a trainer, and clinical metrics — so a single component takes you from a credentialed EHR extract to a validated readmission model. Claude Code alone (rung 1) cannot do this defensibly: it would hand-roll cohort logic and a training loop ad hoc, with no standard task definition or reproducible preprocessing, and is prone to subtle label leakage. A rung-3 toolbelt adds nothing for the core task; the discipline this recipe enforces (patient-level splits, AUPRC, a baseline, calibration) is prompt instruction, not a second tool. Escalate to rung 3 only if you need to chain in external feature sources or deploy the model into a serving stack.

## Availability

Institutional access. The PyHealth skill is free OSS, but the datasets it targets are credentialed: MIMIC-IV and eICU require a [PhysioNet](https://physionet.org/) credentialed account with a completed data-use agreement and CITI human-subjects training; OMOP CDM extracts live behind your institution's data governance. No data leaves your machine — the skill runs locally — but you must hold the appropriate DUA and only report aggregate results permitted by it. Any current Claude plan suffices for the modeling side.

## Compute requirements

Workstation with GPU. Loading and tabulating MIMIC-IV (tens of thousands of patients, millions of events) needs several to tens of GB of RAM. Training a RETAIN/Transformer sequence model is GPU-accelerated: a single mid-range GPU (8–16 GB VRAM) trains a readmission model in minutes to low tens of minutes; CPU-only training is feasible but slow for the larger cohorts. The logistic-regression baseline is laptop-trivial. Disk: the raw credentialed extract dominates (tens of GB for full MIMIC-IV).

## Evidence

Proposed. No documented attempt is known of this exact assembly — Claude Code driving the PyHealth skill to build a readmission model. The closest evidence is component-level and strong: PyHealth is the peer-reviewed, widely-used standard library for exactly this dataset → task → model → metrics pattern ([Yang, Wu, Jiang, Lin, Gao, Danek & Sun, "PyHealth: A Deep Learning Toolkit for Healthcare Applications," *KDD 2023*](https://dl.acm.org/doi/10.1145/3580305.3599178)), and its successor [PyHealth 2.0 (arXiv 2026)](https://arxiv.org/abs/2601.16414) reports building predictive pipelines in as few as 7 lines of code across 15+ datasets, 20+ clinical tasks, and 25+ models, with up to 39× faster processing. Readmission prediction is one of PyHealth's built-in tasks with published baselines. The analogous documented LLM workflow is the [cBioPortal-backed AI-HOPE conversational-agent family](profile-cancer-cohort-genomics-with-cbioportal.html#evidence) — an LLM driving a domain library to produce validated clinical-data analyses — but no published source documents an LLM driving PyHealth specifically. Treat the deep model's gain over the logistic baseline (step 5) as the success criterion to confirm on your own cohort.

## Alternatives considered

- **[Fit a survival model to censored clinical outcomes](fit-survival-model-to-clinical-outcomes.html) (rung 2).** Reach for that when the outcome is *time-to-event* with censoring (time to readmission/death) rather than a fixed 30-day binary label, and when an interpretable, well-calibrated Cox or Random Survival Forest on a modest covariate table is what reviewers want. This recipe is for the binary classification framing on raw EHR code sequences where a deep sequence model can add value.
- **Classical ML in Claude Code (rung 1–2).** If you have already exported a flat patient-feature table, a plain scikit-learn gradient-boosting model in Claude Code may match a deep model and is simpler. PyHealth earns its place when you want to model the *sequence* of coded events without hand-engineering features.
- **Claude Code alone (rung 1).** Insufficient as a defensible pipeline — no standard task definition, high label-leakage risk, no reproducible preprocessing.

## See also

- [PyHealth (Claude Skill)](../../catalog/tools/pyhealth.html)
- [Fit a survival model to censored clinical outcomes](fit-survival-model-to-clinical-outcomes.html) — the time-to-event framing of clinical-outcome modeling.
- [Profile a cancer cohort's genomics with cBioPortal](profile-cancer-cohort-genomics-with-cbioportal.html) — the closest documented LLM-driving-a-clinical-library workflow.

## Sources

- [PyHealth skill (`SKILL.md`)](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/pyhealth/SKILL.md) — verified 2026-06-21 (this run).
- [Yang et al., "PyHealth: A Deep Learning Toolkit for Healthcare Applications," *KDD 2023*](https://dl.acm.org/doi/10.1145/3580305.3599178) — canonical PyHealth method paper; verified 2026-06-21 (this run).
- [PyHealth 2.0, arXiv:2601.16414 (2026)](https://arxiv.org/abs/2601.16414) — successor toolkit with expanded tasks/models; verified 2026-06-21 (this run).
- [PhysioNet — credentialed access for MIMIC-IV / eICU](https://physionet.org/) — data-use-agreement gate; verified 2026-06-21 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=predict-hospital-readmission-from-ehr&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fpredict-hospital-readmission-from-ehr.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
