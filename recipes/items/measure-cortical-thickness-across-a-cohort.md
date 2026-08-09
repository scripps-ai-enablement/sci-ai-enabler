---
title: Measure cortical thickness and subcortical volumes across a cohort
parent: All recipes
grand_parent: Recipes
nav_order: 16
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: HPC or cloud cluster
last_verified: 2026-08-09
summary: Drive FreeSurfer recon-all over a T1w cohort with one pinned version, Euler-number QC, and a morphometry table that carries its quality covariate.
---

# Measure cortical thickness and subcortical volumes across a cohort

Turn a folder of T1-weighted scans into a per-subject × per-region thickness and volume table using the [FreeSurfer skill](../../catalog/tools/freesurfer-tool.html), with the two things that decide whether the table is publishable — one pinned FreeSurfer version for every subject, and a quality metric carried into the statistics — enforced by the script rather than remembered.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | HPC or cloud cluster |

## Problem

You have T1w scans for a cohort and a question of the form "is cortical thickness lower in the patient group" or "does hippocampal volume track this score". FreeSurfer's `recon-all` is the standard answer, and running it is not the hard part — the hard part is that the two commonest ways to get a wrong answer leave no trace in the output table.

The first is version drift. `recon-all` takes 6–12 hours per subject, so cohorts get processed in waves, across months, on whatever software module was loaded that day. Regional estimates are not comparable across FreeSurfer major versions: v5.0.0 differed from earlier releases by 8.8 ± 6.6% on volumes and 2.8 ± 1.3% on thickness ([Gronenschild et al. 2012](https://doi.org/10.1371/journal.pone.0038234)), and v7.1 cingulate thickness reaches only ICC 0.37–0.61 against v6.0/v5.3 ([Haddad et al. 2023](https://doi.org/10.1002/hbm.26147)). If controls were run in v7.1 and patients in v6.0, the group difference is partly software.

The second is scan quality. Motion-degraded scans yield systematically thinner cortex, and because motion correlates with age, diagnosis, and symptom severity, quality both inflates and obscures real associations ([Rosen et al. 2018](https://doi.org/10.1016/j.neuroimage.2017.12.059)). Solved looks like: a committed script, one version for every subject, an explicit QC gate, and a `morphometry.csv` that ships its own quality covariate.

## Recommended approach

1. **Install the [FreeSurfer skill](../../catalog/tools/freesurfer-tool.html)** (NeuroClaw), and obtain the free FreeSurfer `license.txt` by registering upstream — `recon-all` will not run without it. The [sMRI skill](../../catalog/tools/smri-skill.html) is the modality-layer planner that delegates to it; installing both is fine, but the FreeSurfer skill alone is what this recipe needs.

2. **Pin the version before you process a single subject.** Ask Claude Code to write `config.yaml` recording the FreeSurfer release string (`8.2.0`, `7.4.1`, whatever your site standardizes on), the container digest or module name, and the OS. Commit it. The rule the script enforces: every subject in the cohort is processed by that one build, and a mid-cohort upgrade means reprocessing everyone, not appending. Gronenschild et al. found workstation type and even macOS point release moved the numbers by roughly half the between-version amount, so "same version, different machine" is also a wave — record the host, and prefer a single container image over site modules.

3. **Confirm the inputs are BIDS-organized and consistent.** Point the run at a BIDS tree; if you are starting from scanner exports, use the [Organize raw DICOM into a BIDS layout](organize-raw-dicom-to-bids-layout.html) recipe first. Have the script abort — not warn — if T1w acquisition parameters (voxel size, sequence, field strength) differ across subjects without a `site`/`scanner` column existing in your `participants.tsv` to model it.

4. **Have Claude Code write `run_recon.py` (or a Nextflow/Slurm array wrapper) rather than running `recon-all` conversationally.** One subject per task, `SUBJECTS_DIR` fixed, stdout captured per subject, exit status recorded to `recon_status.csv`. This is the durable artifact; a chat transcript that ran 60 jobs is not re-runnable. See [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) for the pattern.

5. **Extract the Euler number and gate on it — before looking at any group difference.** After the runs finish, collect the total surface holes from each subject's `?h.orig.nofix` log into `qc.csv`. The Euler number tracks expert manual ratings closely and identifies human-rated "unusable" images at AUC 0.98–0.99 ([Rosen et al. 2018](https://doi.org/10.1016/j.neuroimage.2017.12.059)), which makes it the cheapest defensible automated gate. Two rules:
   - Set the exclusion threshold as a **recorded literal** in `config.yaml`, chosen before you see group labels, and write the excluded subject IDs to `excluded.csv` with their Euler values. Do not tune it afterwards.
   - Still eyeball the surfaces of borderline subjects. Thresholding attenuates but does not eliminate the quality effect ([Bedford et al. 2023](https://doi.org/10.1162/imag_a_00022)), so the gate is a filter, not a fix.

6. **Aggregate into one table that carries its own covariate.** Run `aparcstats2table` and `asegstats2table`, and have the script join them with `qc.csv` into `morphometry.csv` — one row per subject, columns for each Desikan-Killiany (or Destrieux) region plus `euler_lh`, `euler_rh`, and `estimated_total_intracranial_volume`. Keep thickness and surface area as **separate columns and separate analyses**: they are genetically and developmentally distinct measures, and Haddad et al. found their version-compatibility profiles differ, so a composite "cortical measure" hides both effects.

7. **Model quality explicitly, and eTIV for volumes.** In the statistics step, include the Euler number as a covariate rather than relying on the exclusion in step 5 alone — Bedford et al. showed that how you control for quality changes case-control conclusions in ABIDE. Subcortical volumes additionally need eTIV as a covariate or a proportional correction; thickness does not. Emit `results.csv` with both the quality-adjusted and unadjusted models, so the sensitivity of each finding to the QC choice is visible rather than buried.

8. **Record provenance.** Emit `provenance.json` with the FreeSurfer version string and container digest, the atlas/parcellation used, the Euler threshold literal, counts of subjects attempted / completed / excluded, the host OS, the model identity, and the run date. Commit `config.yaml`, `run_recon.py`, `morphometry.csv`, `qc.csv`, `excluded.csv`, and `provenance.json`.

## Why this assembly

Rung 2 — Claude Code plus one skill. Rung 1 fails on a specific mechanical point: `recon-all` is a multi-hour external binary with a licence file, a `SUBJECTS_DIR` convention, and a stats-table extraction step whose flags the model will approximate from training memory and get subtly wrong (wrong atlas, wrong measure keyword, silently empty columns). The skill supplies the current invocation. Nothing above rung 2 is needed: the value this recipe adds over "run FreeSurfer" is the version pin, the QC gate, and the covariate discipline, and all three are script logic Claude Code writes directly. A second component would only be justified for multi-site harmonization (see Alternatives).

## Availability

Fully open, and fully local — scans never leave your machine, so the recipe is usable on unpublished or IRB-restricted clinical cohorts. Two gates worth naming. FreeSurfer itself requires a **free registration to obtain `license.txt`**; the tools refuse to run without it, so do this before scheduling a cluster job array. The FreeSurfer software licence agreement governs use, and commercial use terms are not stated on the download page — read the agreement itself if you are not in an academic setting. The NeuroClaw skill wrapping it is MIT.

## Compute requirements

`HPC or cloud cluster` for a real cohort. `recon-all` is single-subject, largely single-threaded, and takes roughly **6–12 hours of wall clock per subject** on a current CPU core; it is CPU- and RAM-bound, not GPU-bound, so a GPU buys nothing for the classic pipeline. Budget ~1 core and 4–8 GB RAM per concurrent subject, and ~300–500 MB of output per subject in `SUBJECTS_DIR`.

The tiering is really about N. Ten subjects fit on a workstation overnight if you run 8 in parallel. Sixty subjects is a cluster array job or a multi-day serial run — and it is exactly that duration that creates the version-drift risk step 2 exists to close, because a queue that spans a site software upgrade will silently produce two waves. FreeSurfer 8.x offers faster deep-learning-based segmentation paths; if you use one, it becomes part of the version string you pin, not a detail.

## Evidence

`Proposed`. No published account is known of an LLM agent driving FreeSurfer over a cohort with this QC and provenance discipline, and the NeuroClaw skill is `verified: works` (the install path and invocation are current) rather than benchmarked end-to-end. What is unusually well quantified is every gate the recipe imposes:

- **Version pinning.** Thickness differed by 2.8 ± 1.3% and volumes by 8.8 ± 6.6% across FreeSurfer 4.3.1/4.5.0/5.0.0, with workstation type and macOS version contributing about half as much again; the authors' conclusion is a direct instruction not to update mid-study ([Gronenschild et al., *PLoS ONE* 2012](https://doi.org/10.1371/journal.pone.0038234)). The modern replication across v5.3/6.0/7.1 found cingulate thickness compatibility as low as ICC 0.37–0.61, pallidum and putamen volumes incompatible between v6.0 and v5.3, and — the load-bearing finding — **version differences in the results of downstream statistical analysis** of age associations in a quality-controlled sample ([Haddad et al., *Hum Brain Mapp* 2023](https://doi.org/10.1002/hbm.26147)).
- **The counterweight, stated honestly.** Absolute estimates shifting does not automatically invalidate a contrast: pairwise thickness differences of 1.6–5.8% across v4.1.0/4.5.0/5.1.0 had very little effect on detectable AD/MCI/control group differences or on entorhinal-thickness classification accuracy ([Chepkoech et al., *Hum Brain Mapp* 2016](https://doi.org/10.1002/hbm.23139)). Read together with Haddad: inter-subject stability within a version is good, which is precisely why processing one cohort with one version is sufficient — and why mixing versions across groups is not.
- **The Euler gate.** Euler number correlated with manual ratings across three datasets, identified "unusable" images at AUC 0.98–0.99, out-performed functional-timeseries proxies from the same session, and quality both inflated and obscured age associations in adolescence ([Rosen et al., *NeuroImage* 2018](https://doi.org/10.1016/j.neuroimage.2017.12.059)).
- **Why the gate is not sufficient.** Thresholding by QC score attenuates but does not eliminate the impact of quality on cortical estimates, and inadequate control for quality alters the results of autistic-vs-neurotypical comparisons in ABIDE ([Bedford et al., *Imaging Neuroscience* 2023](https://doi.org/10.1162/imag_a_00022)) — the reason step 7 covaries rather than only excludes.

## Alternatives considered

- **Multi-site cohorts.** If scans come from more than one scanner, this recipe is necessary but not sufficient: site effects on thickness are comparable to the effects people study. Add the [harmonization skill](../../catalog/tools/harmonization-tool.html) (ComBat-class) as a step between `morphometry.csv` and the statistics. Haddad et al. note that batch-effect correction may adjust for some inter-version effects when most sites ran one version, but that results vary when more sites are run with different versions — so harmonization is not a licence to skip step 2.
- **fMRIPrep / HCP-style pipelines.** If you also need functional preprocessing on the same subjects, run [fMRIPrep](../../catalog/tools/fmriprep-tool.html) or the [HCP pipeline](../../catalog/tools/hcppipeline-tool.html), both of which invoke FreeSurfer internally and can share its output. Reach for those when morphometry is a by-product; reach for this recipe when morphometry is the result.
- **Reuse a public derivative instead of processing.** For many questions the morphometry already exists — ADNI, ABCD, HCP, UK Biobank and others ship FreeSurfer outputs, and the catalogue has cohort skills for several ([ADNI](../../catalog/tools/adni-skill.html), [ABCD](../../catalog/tools/abcd-skill.html), [UK Biobank](../../catalog/tools/ukb-skill.html)). Check the release's FreeSurfer version before pooling it with your own runs; that comparison is exactly the mixed-version case the evidence warns against.

## See also

- [FreeSurfer (Claude Skill)](../../catalog/tools/freesurfer-tool.html)
- [Structural MRI (sMRI) skill](../../catalog/tools/smri-skill.html)
- [Harmonization skill](../../catalog/tools/harmonization-tool.html)
- [Organize raw DICOM into a BIDS layout](organize-raw-dicom-to-bids-layout.html) — the upstream recipe if you are starting from scanner exports.
- [Compute DTI scalar maps from diffusion MRI](compute-dti-scalar-maps-from-diffusion-mri.html) — the diffusion-side sibling.
- [Build a functional connectivity matrix from resting-state fMRI](build-functional-connectivity-matrix-from-fmri.html) — the functional-side sibling.

## Sources

- [Haddad et al., *Human Brain Mapping* 44(4) (2023), doi:10.1002/hbm.26147](https://doi.org/10.1002/hbm.26147) — published 2023; verified 2026-08-09 (this run).
- [Gronenschild et al., *PLoS ONE* 7(6):e38234 (2012), doi:10.1371/journal.pone.0038234](https://doi.org/10.1371/journal.pone.0038234) — published 2012; verified 2026-08-09 (this run).
- [Chepkoech et al., *Human Brain Mapping* 37(5):1831–1841 (2016), doi:10.1002/hbm.23139](https://doi.org/10.1002/hbm.23139) — published 2016; verified 2026-08-09 (this run).
- [Rosen et al., *NeuroImage* 169:407–418 (2018), doi:10.1016/j.neuroimage.2017.12.059](https://doi.org/10.1016/j.neuroimage.2017.12.059) — published 2018; verified 2026-08-09 (this run).
- [Bedford et al., *Imaging Neuroscience* (2023), doi:10.1162/imag_a_00022](https://doi.org/10.1162/imag_a_00022) — published 2023; verified 2026-08-09 (this run).
- [FreeSurfer Download and Install](https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall) — v8.2.0 released March 2026, v7.4.1 last v7 release, free `license.txt` required; fetched 2026-08-09 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=measure-cortical-thickness-across-a-cohort&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fmeasure-cortical-thickness-across-a-cohort.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
