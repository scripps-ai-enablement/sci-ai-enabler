---
title: Compute DTI scalar maps (FA/MD/AD/RD) from diffusion MRI
parent: All recipes
grand_parent: Recipes
nav_order: 5
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-26
summary: Use the DIPY skill in Claude Code to fit a diffusion tensor to a DWI volume and emit FA/MD/AD/RD maps plus ROI statistics, as a re-runnable script.
---

# Compute DTI scalar maps (FA/MD/AD/RD) from diffusion MRI

Hand Claude Code a diffusion-weighted MRI volume with its gradient tables; get back a brain-masked tensor fit and FA/MD/AD/RD scalar maps plus per-ROI statistics, captured as a version-controlled script with the mask, model, and provenance written down.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Turning a diffusion-weighted MRI acquisition into the four DTI scalar maps everyone reports — fractional anisotropy (FA), mean diffusivity (MD), axial diffusivity (AD), radial diffusivity (RD) — is a fixed sequence: load the 4D DWI with its `.bval`/`.bvec` gradient tables, build a `GradientTable`, generate a brain mask, fit the diffusion tensor per voxel, then derive the scalars and pull statistics inside anatomical ROIs. But each step hides a decision that silently biases the numbers. A gradient table with flipped or mis-scaled b-vectors produces plausible-looking but wrong FA; skipping the brain mask lets skull/noise voxels inflate MD; fitting with the wrong estimator (OLS vs weighted-LS vs RESTORE) changes the tail behavior in low-SNR regions. Every lab rebuilds this boilerplate. Solved looks like: hand the agent the DWI + gradient files and an ROI (or atlas label), get back committed code that emits the four NIfTI scalar maps, an ROI statistics table, and a record of the mask method, tensor-fit method, b-values used, and input hashes.

## Recommended approach

1. **Install the [DIPY skill](../../catalog/tools/dipy-tool.html)** in Claude Code (it wraps the concrete DIPY idioms for loading DWI + gradient tables, masking, tensor fitting, computing FA/MD/AD/RD, and extracting ROI statistics):

   ```
   git clone https://github.com/CUHK-AIM-Group/NeuroClaw
   cp -r NeuroClaw/skills/dipy-tool ~/.claude/skills/
   ```

   Verify DIPY is importable (`pip install dipy`). No GPU needed. Start from a preprocessed DWI (denoise/Gibbs/eddy/motion correction are upstream steps this recipe does not run).

2. **Have the assistant write a versioned pipeline script, not run steps interactively.** A minimal prompt:

   ```
   Using the dipy-tool skill, write me a script fit_dti.py that takes
   a preprocessed DWI (sub-01_dwi.nii.gz) with sub-01_dwi.bval and
   sub-01_dwi.bvec. The script must:
   - load the DWI and read the gradient table with
     dipy.io.gradients.read_bvals_bvecs -> gradient_table;
     print the b-value shells and the number of directions per shell
   - generate a brain mask with median_otsu (state numpass/median_radius)
   - fit the diffusion tensor with TensorModel (fit_method="WLS")
     inside the mask
   - compute FA, MD, AD, RD and save each as a NIfTI in out/
     (fa.nii.gz, md.nii.gz, ad.nii.gz, rd.nii.gz) preserving the
     affine/header
   - given an ROI mask NIfTI (or an atlas label + label id), report
     mean/std/median FA/MD/AD/RD inside the ROI to out/roi_stats.csv
   Surface the fit method, mask parameters, and b-value shell(s) used
   for the tensor as variables at the top of the file with comments.
   ```

3. **Pin the environment.** Ask the assistant to emit a `requirements.txt` (or `environment.yml`) pinning `dipy`, `nibabel`, `numpy`, `scipy`, `pandas`. Commit the script and the environment together.

4. **Sanity-check the tensor fit before trusting the scalars.** Have the assistant add a QC step: FA should sit in [0, 1] with white-matter values ~0.4–0.8 and CSF near 0; MD should be near free-water diffusivity (~3×10⁻³ mm²/s) in ventricles. Save an FA map overlay and a directionally-encoded color (DEC) FA figure so gross b-vector flips (mislabeled left–right tracts) are visible. A whole-brain FA that is uniformly high or a DEC map with anatomically wrong colors almost always means a bad gradient table.

5. **Record provenance.** Have the script write `out/provenance.json` capturing: DIPY version, the b-value shell(s) fed to the tensor (single-shell recommended; note if high-b volumes were dropped), the mask method and parameters, the tensor fit method (`WLS`/`OLS`/`RESTORE`), the ROI/atlas name and label id, the input DWI/bval/bvec `sha256`, the run date, and the model/agent identity. See the [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide for the pattern.

The durable artifact is `fit_dti.py` + the pinned environment + the emitted `fa/md/ad/rd.nii.gz`, `roi_stats.csv`, and `provenance.json` — all under version control. Re-running on the same inputs reproduces the maps.

## Why this assembly

Rung 2. The skill gives Claude the correct DIPY idioms and — critically — the step ordering (gradient table → mask → tensor fit → scalars → ROI stats) so the model does not reinvent the API or silently skip the mask. Plain Claude Code *can* write DIPY code, but the gradient-table construction and tensor-fit method are exactly where an unaided model tends to pick unstated defaults (or mis-handle multi-shell b-values) that produce wrong-but-plausible FA. There is no reason to escalate: single-subject DTI scalar-map computation is a well-defined, laptop-scale job with a human-in-the-loop QC check, not a problem that needs a multi-tool harness or an autonomous system.

## Availability

Fully open. The DIPY skill is community OSS (MIT, part of the NeuroClaw library); DIPY is BSD-licensed. No institutional access or subscription. Any current Claude plan works. This recipe starts from a preprocessed DWI — denoising, Gibbs-ringing removal, and eddy/motion correction (typically FSL `eddy` or an MRtrix/QSIPrep pipeline) are the upstream prerequisites, not covered here. The NeuroClaw skill assumes the collection's shared helpers; a standalone `pip install dipy nibabel` covers the tensor-fit path.

## Compute requirements

Laptop. A single-subject single-shell DWI (~30–60 directions, ~2 mm isotropic) masks and tensor-fits in well under a minute to a couple of minutes on a modern laptop CPU; DIPY's `TensorModel` is voxelwise and vectorized. RAM 8–16 GB is ample for one subject's 4D volume. Batch across many subjects by looping the same script — still CPU-only, still laptop-scale. `RESTORE` fitting (robust to outliers) is slower than `WLS` but still laptop-scale for one subject.

## Evidence

Reported. DIPY is the documented, field-standard open-source Python library for diffusion MRI analysis, including the tensor model and FA/MD/AD/RD derivation ([Garyfallidis et al., *Front. Neuroinform.* 2014](https://doi.org/10.3389/fninf.2014.00008)), and the load → mask → tensor-fit → scalar-map → ROI/tract statistics workflow this recipe encodes is the canonical DTI pipeline reused across current clinical and translational studies — e.g., a quantitative-susceptibility/DTI schizophrenia study reporting subcortical MD and white-matter FA ([Vano et al., *Mol. Psychiatry* 2026](https://pubmed.ncbi.nlm.nih.gov/40913112/)), a cerebral-small-vessel-disease/vascular-dementia study using voxel-based FA/MD analysis ([Lu et al., *J. Alzheimers Dis.* 2025](https://pubmed.ncbi.nlm.nih.gov/40899970/)), and a randomized breast-cancer-exercise trial using DTI FA/MD ([Koevoets et al., *Brain Imaging Behav.* 2025](https://pubmed.ncbi.nlm.nih.gov/39804457/)). The DIPY *skill* is the documented Claude assembly for driving these operations. No peer-reviewed head-to-head benchmark of this exact skill against a hand-written DIPY script is known; the recipe inherits the robust component-level evidence for DIPY and the well-established DTI methodology.

## Alternatives considered

- **Plain Claude Code + raw DIPY.** Fine for users fluent in the DIPY API who want no skill layer. The skill's value is encoding the step ordering and surfacing the gradient-table / mask / fit-method knobs so they don't get silently defaulted.
- **FSL `dtifit`, MRtrix3, or QSIPrep with no agent.** The right call for a lab standardized on one of those pipelines, or when you also need the upstream eddy/motion correction in the same tool. Reach for this recipe when you want the tensor fit captured as re-runnable, version-controlled Python you can vary the mask and fit method on across subjects.
- **Higher-order models (constrained spherical deconvolution, NODDI) or tractography.** If single-tensor DTI is too crude for your question — crossing fibers, tractometry along a bundle — that is a different (still DIPY-capable) workflow, not this one. DTI scalar maps are the first-pass, most-reported summary; escalate only if the question demands it.
- **An autonomous-science system.** None targets DTI scalar-map computation; the problem is too well-scoped to justify one.

## See also

- [DIPY (Claude Skill)](../../catalog/tools/dipy-tool.html)
- [Build a resting-state functional-connectivity matrix from preprocessed fMRI](build-functional-connectivity-matrix-from-fmri.html) — the analogous single-modality, laptop-scale, skill-driven neuroimaging recipe (fMRI rather than diffusion MRI).
- [Extract event-related potentials from EEG epochs](extract-event-related-potentials-from-eeg.html) — the EEG counterpart in the same NeuroClaw skill family.
- [Organize raw DICOM into a BIDS layout](organize-raw-dicom-to-bids-layout.html) — the upstream data-organization step for a diffusion MRI dataset.

## Sources

- [DIPY skill — `NeuroClaw/skills/dipy-tool/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/dipy-tool/SKILL.md) — catalog `last_verified` 2026-06-11; verified 2026-07-26 (this run).
- [Garyfallidis et al., *Front. Neuroinform.* 8:8 (2014), doi:10.3389/fninf.2014.00008](https://doi.org/10.3389/fninf.2014.00008) — Dipy, a library for the analysis of diffusion MRI data.
- [Vano et al., *Mol. Psychiatry* (2026), doi:10.1038/s41380-025-03195-7](https://pubmed.ncbi.nlm.nih.gov/40913112/) — QSM + DTI (subcortical MD, white-matter FA) in schizophrenia; verified 2026-07-26 (this run).
- [Lu et al., *J. Alzheimers Dis.* (2025), doi:10.1177/13872877251372953](https://pubmed.ncbi.nlm.nih.gov/40899970/) — voxel-based FA/MD analysis in cerebral small vessel disease; verified 2026-07-26 (this run).
- [Koevoets et al., *Brain Imaging Behav.* (2025), doi:10.1007/s11682-024-00965-9](https://pubmed.ncbi.nlm.nih.gov/39804457/) — DTI FA/MD in a randomized breast-cancer exercise trial; verified 2026-07-26 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=compute-dti-scalar-maps-from-diffusion-mri&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fcompute-dti-scalar-maps-from-diffusion-mri.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
