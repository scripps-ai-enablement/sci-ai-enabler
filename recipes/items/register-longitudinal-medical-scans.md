---
title: Register longitudinal medical scans to a common frame
parent: All recipes
grand_parent: Recipes
nav_order: 21
problem_class: Data analysis
subject_areas: [Translational Medicine]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-06-28
summary: Drive SimpleITK from Claude Code to rigidly then deformably align a patient's baseline and follow-up CT/MRI, propagate contours, and emit a reproducible transform + warped volume.
---

# Register longitudinal medical scans to a common frame

Hand Claude Code two scans of the same patient at different timepoints; get back a committed registration script that aligns the follow-up to the baseline, propagates a contour, and records every transform parameter so the alignment can be re-run.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

Comparing a tumor, an organ, or a lesion across two scans — baseline vs. follow-up, pre- vs. post-treatment, planning CT vs. on-treatment CBCT — requires the two volumes to sit in the same coordinate frame first. Patients are positioned differently, breathe differently, and tissues deform between sessions, so a naive voxel-by-voxel subtraction is meaningless. The fix is image registration: a rigid (or affine) step to correct gross pose, then a deformable step to model soft-tissue change, after which a contour or dose map drawn on one scan can be warped onto the other. Done by hand in a GUI, this is slow, click-driven, and irreproducible — the transform parameters vanish when the window closes. Solved looks like: a committed script that reads the two volumes, runs the registration with recorded metric/optimizer settings, writes the resampled moving image and the transform file, and reports an overlap/quality metric you can defend.

## Recommended approach

1. **Install the [SimpleITK skill](../../catalog/tools/simpleitk-image-registration.html)** so Claude Code has the SimpleITK registration idioms in context:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm it appears under `/plugin` → Installed. On first use the skill installs `SimpleITK` and its dependencies.

2. **Get both scans into a registration-ready format.** SimpleITK reads DICOM series and NIfTI directly. If your data is still raw DICOM, run the [DICOM-to-BIDS recipe](organize-raw-dicom-to-bids-layout.html) or a `dcm2niix` pass first so each timepoint is a single `*.nii.gz` volume with correct spacing and orientation. Name the baseline `fixed.nii.gz` and the follow-up `moving.nii.gz`.

3. **Have Claude write the registration to a versioned script**, not an interactive session. Ask it to use the skill and emit `register_scans.py`:

   ```
   Use the simpleitk-image-registration skill to write register_scans.py that:
   1. Reads fixed.nii.gz and moving.nii.gz (sitk.ReadImage, cast to float32).
   2. Initializes with CenteredTransformInitializer (geometry mode).
   3. Stage 1 — rigid (Euler3DTransform): MattesMutualInformation (50 bins),
      regular-step gradient descent, 3-level multi-resolution pyramid
      (shrink 4/2/1, smoothing 2/1/0 mm).
   4. Stage 2 — deformable (BSplineTransform, ~8 mm control-point grid),
      initialized from the stage-1 result, LBFGSB optimizer.
   5. Resamples moving onto the fixed grid (linear), writes warped.nii.gz.
   6. Writes the composite transform to transform.tfm.
   7. Reports the final Mattes MI metric value and, if a moving-image label
      mask is supplied, propagates it (nearest-neighbour resample) and prints
      the Dice overlap against a fixed-image reference mask.
   Pin the environment in requirements.txt with the exact SimpleITK version.
   ```

4. **Run it and QC the alignment.** Have Claude execute the script, then render a checkerboard and a difference overlay of `fixed` vs. `warped` on a few slices and inspect for residual misalignment. Report the metric value and, where masks exist, the propagated-contour Dice.

   ```
   Run register_scans.py. For three representative slices, render a
   checkerboard composite of fixed vs. warped and a signed-difference map.
   Flag any slice where the deformable field looks implausible (folding,
   >2 cm displacement in rigid anatomy).
   ```

5. **Record provenance.** Have Claude write `provenance.json` capturing the SimpleITK version, the transform type/metric/optimizer settings, the control-point spacing, the input volume sha256s, the run date, and the model id. Commit `register_scans.py`, `requirements.txt`, `transform.tfm`, and `provenance.json` together — see the [reproducibility guide](../../guide/advanced/reproducibility.md). The transform file plus the pinned env reproduces the warped volume exactly; the warped volume and propagated contour drop straight into a longitudinal tumor-burden analysis or a dose-accumulation step.

## Why this assembly

Rung 2. SimpleITK *is* the registration engine; the skill pins the brittle two-stage rigid → B-spline idiom — the `CenteredTransformInitializer` mode, the multi-resolution pyramid schedule, the Mattes-MI bin count, and the nearest-neighbour rule for label propagation — that first-time users get wrong. Plain Claude Code (rung 1) can write SimpleITK from memory but routinely drifts on initializer geometry, mismatches resample interpolators (smearing a label mask with linear interpolation), and forgets to persist the transform, leaving an irreproducible one-off. There is no need for a multi-tool harness: a single image pair and one library is the right grain. The optional GPU is hardware, not a second component.

## Availability

Fully open. SimpleITK is Apache-2.0; the SciAgent-Skills wrapper is Apache-2.0 / CC BY 4.0. Public phantom and challenge datasets (Learn2Reg, the SimpleITK training data) are freely downloadable for method development. Clinical/PHI imaging carries its own IRB, de-identification, and data-residency constraints that are the user's to satisfy — keep the volumes local and do not upload PHI to any hosted endpoint.

## Compute requirements

Workstation with GPU. SimpleITK's CPU registration handles a single pair of typical CT/MRI volumes (~512×512×200) in **a few minutes per stage** on a multi-core workstation with **8–16 GB RAM**; the deformable B-spline stage dominates. A GPU is not strictly required for one pair, but batch registration of a cohort (tens to hundreds of pairs) benefits from parallelizing pairs across cores or a GPU-accelerated build, and is where the workstation tier is justified. Output is small: the warped volume matches the fixed-image size, and the transform file is kilobytes. Memory scales with volume size — very large micro-CT or whole-body volumes may need 32 GB+.

## Evidence

Reported. SimpleITK and its underlying ITK are peer-reviewed and field-standard for medical-image registration: [Yaniv et al., *J. Digit. Imaging* 31:290–303 (2018)](https://doi.org/10.1007/s10278-017-0037-8) documents the toolkit's reproducible-research registration workflows, and deformable registration of this kind is the routine basis for contour propagation and dose accumulation in current clinical-physics practice (e.g., [Solomou et al., *Phys. Imaging Radiat. Oncol.* (2026)](https://doi.org/10.1016/j.phro.2026.100954) on consensus dose-accumulation strategies built on image registration). The SimpleITK skill ships in the BixBench-evaluated SciAgent-Skills collection. No published benchmark documents this *exact* Claude-skill-driven assembly versus a hand-run SimpleITK script; the skill changes *how* the registration is authored, not the algorithm or its accuracy.

## Alternatives considered

- **Plain Claude Code, no skill (rung 1).** Works for users already fluent in SimpleITK's `ImageRegistrationMethod` API and the resample-interpolator rules. Reach for the skill when you want the two-stage idiom and the transform-persistence discipline pinned across runs and collaborators.
- **A dedicated registration package (ANTs, elastix, NiftyReg).** These offer battle-tested parameter presets and often better deformable accuracy for hard cases. None has a Claude-installable wrapper catalogued today; until one is, SimpleITK is the catalogued path and is sufficient for routine rigid+B-spline longitudinal alignment.
- **Learning-based deformable registration (VoxelMorph-class).** Faster at inference once trained and stronger on large deformations, but requires training data and a GPU pipeline. No Claude-installable wrapper is catalogued; escalate only when classical registration demonstrably fails on your anatomy.

## See also

- [SimpleITK (Claude Skill)](../../catalog/tools/simpleitk-image-registration.html)
- [Organize a raw DICOM dataset into a BIDS layout](organize-raw-dicom-to-bids-layout.html) — the upstream conversion step when your imaging is still vendor DICOM.
- [Segment an organ or tumor in a medical image with nnU-Net](segment-organ-or-tumor-in-medical-image.html) — produces the label masks this recipe propagates between timepoints.
- [Fit a survival model to censored clinical outcomes](fit-survival-model-to-clinical-outcomes.html) — the downstream step when a longitudinal volume change becomes a prognostic covariate.

## Sources

- [Yaniv et al., "SimpleITK Image-Analysis Notebooks: a Collaborative Environment for Education and Reproducible Research," *J. Digit. Imaging* 31:290–303](https://doi.org/10.1007/s10278-017-0037-8) — published 2018; verified 2026-06-28 (this run).
- [Solomou et al., "Comparative evaluation of dose accumulation strategies in the clinical reirradiation setting," *Phys. Imaging Radiat. Oncol.* (2026)](https://doi.org/10.1016/j.phro.2026.100954) — published 2026-01; registration-based contour/dose propagation as routine clinical practice.
- [`InsightSoftwareConsortium/SimpleITK`](https://github.com/InsightSoftwareConsortium/SimpleITK) — verified 2026-06-28 (this run).
- [SimpleITK skill catalog page (this repo)](../../catalog/tools/simpleitk-image-registration.html) — `last_verified` 2026-06-11.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=register-longitudinal-medical-scans&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fregister-longitudinal-medical-scans.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
