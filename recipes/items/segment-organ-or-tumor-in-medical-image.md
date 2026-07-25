---
title: Segment an organ or tumor in a medical image with nnU-Net
parent: All recipes
grand_parent: Recipes
nav_order: 23
problem_class: Data analysis
subject_areas: [Translational Medicine]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-07-25
summary: Drive nnU-Net's self-configuring framework from Claude Code to train and run a voxel-accurate segmentation model for an organ or lesion in CT/MRI, with 5-fold cross-validated Dice.
---

# Segment an organ or tumor in a medical image with nnU-Net

Hand Claude Code a folder of labeled CT or MRI volumes; get back a self-configured nnU-Net model, 5-fold cross-validated Dice scores, and voxel masks on held-out scans — without hand-tuning a single architecture hyperparameter.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

Quantifying an organ volume, a tumor burden, or a lesion margin from a stack of CT or MRI volumes is a routine translational-imaging task, but building the segmentation model is not. Every dataset has its own voxel spacing, intensity distribution, class imbalance, and 2D-vs-3D geometry, and the "right" U-Net depth, patch size, batch size, normalization, and resampling target all follow from those properties. Get any of them wrong and Dice collapses. Teams burn weeks hand-tuning architectures that a principled rule set could have configured automatically. Solved looks like: point the agent at a labeled training set in the expected layout, get a model that auto-configures preprocessing and architecture from the dataset fingerprint, trains with 5-fold cross-validation, and predicts masks on new scans with an honest cross-validated Dice you can report.

## Recommended approach

1. **Install the [nnU-Net skill](../../catalog/tools/nnunet-segmentation.html)** so Claude Code has the nnU-Net pipeline idioms in context:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm it appears under `/plugin` → Installed. On first use the skill installs `nnunetv2` and its PyTorch dependency.

2. **Lay the data out in nnU-Net's expected structure.** One task folder with `imagesTr/`, `labelsTr/`, `imagesTs/`, and a `dataset.json`. Image files carry the `_0000` modality suffix (`liver_001_0000.nii.gz`); label files share the case ID without the suffix. If your data is still DICOM, run the [DICOM-to-BIDS recipe](organize-raw-dicom-to-bids-layout.html) or a `dcm2niix` pass first to get NIfTI.

3. **Fingerprint, plan, and preprocess.** Let the skill drive nnU-Net's auto-configuration:

   ```
   Use the nnunet-segmentation skill on Dataset501_Liver.
   1. Run nnUNetv2_plan_and_preprocess -d 501 --verify_dataset_integrity.
   2. Report the planned configuration: target spacing, patch size,
      batch size, network depth, and which configs (2d / 3d_fullres /
      3d_lowres / cascade) nnU-Net selected and why.
   3. Flag any dataset-integrity warnings (label gaps, geometry mismatch)
      before training.
   ```

4. **Train with 5-fold cross-validation.** Train the chosen configuration across all five folds; this is the heavy step (see Compute):

   ```
   Train nnUNetv2 for dataset 501, configuration 3d_fullres, all 5 folds.
   After training, run nnUNetv2_find_best_configuration to pick the best
   single config or ensemble, and report the mean foreground Dice per
   class with the per-fold spread.
   ```

5. **Predict on held-out scans and QC.** Run inference on `imagesTs/`, then have Claude overlay a few predicted masks on their source slices and sanity-check volumes against expected anatomy.

   ```
   Run nnUNetv2_predict on imagesTs with the best configuration. For three
   random cases, render an axial slice with the predicted mask overlaid,
   and tabulate the segmented volume (mL) per case and class.
   ```

6. **Hand off.** The trained model, the per-class Dice table, and the predicted masks drop into a radiomics pipeline, a tumor-burden longitudinal analysis, or a figure. Keep the `nnUNetv2` dataset ID and plans file so the model is reproducible.

## Why this assembly

Rung 2. nnU-Net *is* the self-configuring framework; the skill is a thin wrapper that pins the four-stage `plan_and_preprocess` → `train` → `find_best_configuration` → `predict` idiom and the brittle data-layout / `_0000` suffix conventions that trip up first-time users. Plain Claude Code (rung 1) can write `nnunetv2` commands from memory but routinely drifts on the dataset-folder contract and on whether the reported Dice is in-sample or the cross-validated number — exactly what the skill enforces. There is no need for a multi-tool harness: training and inference are one coherent task and a single skill is the right grain. The one heavy ingredient — a GPU — is hardware, not a second component.

## Availability

Fully open. nnU-Net is Apache-2.0; the SciAgent-Skills wrapper is Apache-2.0 / CC BY 4.0. Public benchmark datasets (Medical Segmentation Decathlon, KiTS, BraTS) are freely downloadable for method development. Clinical/PHI imaging carries its own IRB, de-identification, and data-residency constraints that are the user's to satisfy — keep the volumes local and do not upload PHI to any hosted endpoint.

## Compute requirements

Workstation with GPU. Training is the heavy step: nnU-Net's default `3d_fullres` trainer runs 1,000 epochs per fold and needs an NVIDIA GPU with **≥ 10–11 GB VRAM** (the planner shrinks patch/batch size to fit, but less than ~8 GB forces a degraded config). Expect roughly **half a day to two days of wall-clock per fold** on a single RTX 3090/4090-class card for a typical 3D dataset, so a full 5-fold run is multi-day on one GPU — parallelize folds across GPUs to compress it. Preprocessing is CPU/RAM-bound (tens of GB of disk for the preprocessed cache). Inference is light: seconds to a couple of minutes per volume on the same GPU. CPU-only training is impractical.

## Evidence

Reported. nnU-Net itself is peer-reviewed and field-defining: [Isensee et al., *Nature Methods* 18:203–211 (2021)](https://www.nature.com/articles/s41592-020-01008-z) showed the self-configuring framework matching or beating highly specialized solutions on 23 public segmentation challenges across CT, MRI, and electron microscopy, with no manual architecture tuning, and it remains the standard baseline against which new segmentation methods are measured (e.g., [Sun et al., *Front. Oncol.* 2026](https://doi.org/10.3389/fonc.2026.1676424) benchmarks a new liver-tumor model explicitly against nnU-Net). The nnU-Net skill ships in the BixBench-evaluated SciAgent-Skills collection. No published benchmark documents this *exact* Claude-skill-driven assembly versus a hand-run `nnUNetv2` pipeline; the skill changes *how* the four-stage pipeline is invoked, not the underlying method or its accuracy.

## Alternatives considered

- **Plain Claude Code, no skill (rung 1).** Works for users already fluent in `nnUNetv2`'s CLI and folder contract. Reach for the skill when you want the data-layout conventions and the cross-validated-Dice discipline pinned across runs and collaborators.
- **Classical / threshold segmentation.** For high-contrast, well-separated structures (bone on CT, a contrast-filled vessel), a thresholding or region-growing pass in SimpleITK is faster and needs no training data. Escalate to nnU-Net only when classical methods fail *and* you have annotated examples — that is exactly the skill's stated trigger.
- **A foundation segmentation model (MedSAM / SAM-Med).** Promptable, zero-shot segmentation avoids per-task training and suits interactive few-click masking. No Claude-installable wrapper for those is catalogued today; until one is, nnU-Net is the catalogued path and remains stronger for fully-automatic, high-accuracy organ/lesion delineation when labels exist.

## See also

- [nnU-Net (Claude Skill)](../../catalog/tools/nnunet-segmentation.html)
- [Organize a raw DICOM dataset into a BIDS layout](organize-raw-dicom-to-bids-layout.html) — the upstream conversion step when your imaging is still vendor DICOM.
- [Fit a survival model to censored clinical outcomes](fit-survival-model-to-clinical-outcomes.html) — the downstream step when a segmented tumor volume becomes a prognostic covariate.

## Sources

- [Isensee et al., "nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation," *Nature Methods* 18:203–211](https://www.nature.com/articles/s41592-020-01008-z) — published 2021-02 (online 2020-12-07); verified 2026-06-21 (this run).
- [`MIC-DKFZ/nnUNet` (upstream framework)](https://github.com/MIC-DKFZ/nnUNet) — verified 2026-06-21 (this run).
- [Sun et al., "Clinically oriented automatic 2D liver tumor segmentation," *Front. Oncol.* (2026)](https://doi.org/10.3389/fonc.2026.1676424) — published 2026-01; nnU-Net used as the field-standard baseline.
- [nnU-Net skill catalog page (this repo)](../../catalog/tools/nnunet-segmentation.html) — `last_verified` 2026-06-11.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=segment-organ-or-tumor-in-medical-image&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fsegment-organ-or-tumor-in-medical-image.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
