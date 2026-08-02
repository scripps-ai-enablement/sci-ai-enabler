---
title: Extract neuronal traces from a calcium imaging movie
parent: All recipes
grand_parent: Recipes
nav_order: 12
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-08-02
summary: Use the Calcium Imaging Analysis Guide skill to pick motion correction, ROI extraction, neuropil correction and dF/F for two-photon or miniscope data, captured as a re-runnable script.
---

# Extract neuronal traces from a calcium imaging movie

Hand Claude Code a raw two-photon or miniscope movie; get back a committed pipeline that motion-corrects, segments ROIs, neuropil-corrects, computes dF/F, and writes a QC table saying which ROIs you are allowed to believe.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

Every calcium-imaging lab faces the same five-decision chain — rigid or non-rigid motion correction, which ROI-extraction algorithm, whether and how hard to subtract neuropil, how to define the dF/F baseline, and whether to trust deconvolved spike estimates — and each decision depends on the preparation. A choice that is correct for anesthetized two-photon cortex is wrong for a one-photon miniscope in a freely moving mouse, where out-of-focus background dominates and CNMF's two-photon assumptions break.

The decisions are also load-bearing in a way that is invisible downstream. Neuropil contamination inflates apparent correlations between neighbouring cells; subtracting it after dF/F rather than before changes the amplitudes; a baseline percentile chosen for sparse activity distorts traces from a densely active population. By the time the data is a heatmap of dF/F traces, none of that is recoverable, and the parameters usually live in someone's notebook or a GUI session that was never saved. "Solved" means: a script that runs the chain end to end, a QC table that gates which ROIs enter the analysis, and a written record of every threshold and package version.

## Recommended approach

1. **Install the [Calcium Imaging Analysis Guide skill](../../catalog/tools/calcium-imaging-analysis-guide.html)** in Claude Code. Note the catalog page's install caveat: the single-skill path also needs the collection's `research-literacy` skill. The skill is *decision guidance*, not a runner — install the extraction package you settle on separately (Suite2p and Cellpose are pip-installable; CaImAn is conda/mamba only).

2. **State your preparation before asking for anything.** This is the step that makes the skill useful, because its rules branch on it:

   ```
   I have 30 min of one-photon miniscope video from a freely moving mouse,
   GCaMP6f, 20 Hz, 600x600 px, single plane, ~150 expected cells.
   Using the calcium-imaging-analysis-guide skill: which motion correction,
   which ROI extraction method, and which neuropil correction apply here,
   and what changes versus a head-fixed two-photon recording?
   Give me the reasoning, not just the settings.
   ```

   Expect the branch to matter: CNMF-E for one-photon/miniscope where background is the dominant problem, CNMF or sparse-NMF (or Cellpose segmentation) for two-photon; non-rigid correction for awake behaving animals, rigid for anesthetized; maximum shift capped around 10% of the field of view.

3. **Get the decisions written into a versioned script.** A minimal prompt:

   ```
   Write me extract_traces.py implementing the pipeline you just described,
   using suite2p, for data/session01.tif. It must:
   - motion-correct with the method and max-shift you recommended
   - extract ROIs, then compute F_corrected = F - R_NEUROPIL * F_neuropil
     BEFORE dF/F, with R_NEUROPIL as a named constant
   - compute dF/F with a rolling-percentile baseline; expose the percentile
     and the window length as named constants
   - write out/traces_dff.npy, out/roi_masks.npy, and out/roi_qc.csv with
     per-ROI SNR, skewness, spatial compactness and the classifier score
   - write out/rejected_rois.csv with a reason string per rejection —
     do not silently drop ROIs
   Surface every threshold as a constant at the top with a comment.
   ```

   `rejected_rois.csv` is not a diagnostic, it is part of the result: the count and the reason distribution tell you whether the segmentation was reasonable or whether you just threw away a third of your cells.

4. **Look at the ROI overlay before you look at the traces.** Have the script save the ROI footprints over the mean and max-projection images. Segmentation failures are obvious in that figure — merged neighbours, a ring of duplicate ROIs around one cell, processes segmented as somata — and invisible in a trace heatmap.

5. **Treat deconvolution as a separate, optional, clearly-labelled step.** If you want event times, run OASIS or CASCADE as an explicit stage writing a *different* file (`out/spike_rates.npy`), never overwriting dF/F. Label the output what it is: an estimated firing rate, not a spike train. If absolute rates matter, prefer a method trained on ground-truth paired recordings over a model-based deconvolution (see Evidence).

6. **Pin and record.** Emit a `requirements.txt` (or `environment.yml`, if CaImAn puts you on conda) pinning the extraction package, `numpy`, `scipy`, `scikit-image`; have the script write `out/provenance.json` with the package name and version, the motion-correction method and max shift, the ROI algorithm and its key parameters, `R_NEUROPIL`, the baseline percentile and window, every QC cutoff, ROI counts kept/rejected, the input `sha256`, the run date, and the model/agent identity. Follow the [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) pattern.

The durable artifact is `extract_traces.py` + the pinned environment + `traces_dff.npy`, `roi_qc.csv`, `rejected_rois.csv` and `provenance.json`, under version control. The raw movie stays out of git; its hash goes in the provenance record.

## Why this assembly

Rung 2. The hard part here is not writing Suite2p calls — Claude Code can do that unaided — it is knowing *which* branch of the pipeline your preparation is on, and that the neuropil subtraction goes before dF/F rather than after. The skill supplies exactly that decision logic with a stated rule per stage, which is why it earns its place over plain Claude Code.

It does not earn more than that. This is one movie, one pipeline, one figure check; there is no second tool to wire in and no autonomous system that targets calcium extraction.

## Availability

Fully open, with a licensing note. The skill is community OSS (MIT); the extraction packages are separately licensed and copyleft — Suite2p GPL-3.0, CaImAn GPL-2.0, Cellpose BSD-3-Clause. If you plan to redistribute a derived pipeline, check the obligation that attaches to whichever you chose. Everything runs locally; no data leaves the machine.

**Verify the skill's numbers before adopting them.** The catalog page flags that the collection's skills are AI-generated and not individually expert-reviewed. The thresholds it states — r ≈ 0.7 neuropil coefficient, 8th–20th percentile baseline over 30–60 s windows, SNR > 3, skewness > 0.5 — are plausible field-standard starting points, not values you should ship without checking against the cited sources and your own preparation. Sanity-check the neuropil coefficient in particular: it is the parameter most likely to be preparation-specific, and getting it wrong shifts every correlation in your dataset.

## Compute requirements

Workstation with GPU, but RAM and disk are usually the real limits, not VRAM. A 30-minute single-plane movie at 512×512 and 30 Hz is tens of GB in float32; Suite2p and CaImAn both chunk to stay within memory, but 32–64 GB RAM keeps the run comfortable and fast local NVMe matters more than the GPU. Expect motion correction and segmentation together to run in the tens of minutes to a couple of hours per session on a workstation, scaling with pixels × frames × planes.

A GPU is genuinely useful for Cellpose-based segmentation and for deep-learning spike inference, and is optional elsewhere. Multi-plane or multi-session registration multiplies both time and storage — batch across sessions with the same script rather than growing one job.

## Evidence

Proposed. No documented attempt at driving a calcium-imaging pipeline through this Claude skill is known, and the skill's own text is AI-generated. The methods it selects among are strongly validated individually:

- **ROI extraction reaches near-human accuracy.** CaImAn was benchmarked against a corpus of manual annotations from multiple labelers across nine mouse two-photon datasets and achieved near-human performance in detecting the locations of active neurons ([Giovannucci et al., *eLife* 2019](https://doi.org/10.7554/eLife.38173)). That paper is also the source of the one-photon/two-photon method split the skill encodes.
- **Deconvolution is a rate estimate, and ground-truth-trained methods beat model-based ones.** CASCADE was trained on a database of more than 35 recording hours from 298 neurons spanning indicators, cell types and SNRs in zebrafish and mice; it infers *absolute spike rates*, outperforms existing model-based algorithms, and retrains itself to match the sampling rate and noise level of unseen data ([Rupprecht et al., *Nat. Neurosci.* 2021](https://doi.org/10.1038/s41593-021-00895-5)). Later supervised networks report further gains on the same public ground-truth database at lower computational cost ([Zhou et al., *Cell Rep. Methods* 2023](https://doi.org/10.1016/j.crmeth.2023.100462)). This is why step 5 keeps deconvolution separate and labelled.
- **Downstream classifiers are mostly robust but not identically so.** In a synthetic-ground-truth comparison built from real two-photon hippocampal signals, most time-cell detection algorithms correctly classified over 80% of cells but differed in their true/false-positive balance and in sensitivity to noise, event width, timing imprecision and background activity ([Ananthamurthy & Bhalla, *eNeuro* 2023](https://doi.org/10.1523/ENEURO.0007-22.2023)) — an argument for recording the extraction parameters, since the analysis layer above inherits them.

## Alternatives considered

- **A GUI pipeline with no agent** — the Suite2p GUI, or a wrapper like [EZcalcium](https://doi.org/10.3389/fncir.2020.00025) built over NoRMCorre and CaImAn for labs without programming depth. The right call for a single exploratory dataset where you want to click through ROI curation. Reach for this recipe when the pipeline has to run identically over many sessions and be defensible later.
- **Plain Claude Code + Suite2p directly.** Fine if you already know which branch your preparation is on. You lose the stage-by-stage rule set, which is the whole value of the skill.
- **Manual ROI drawing in ImageJ.** Still defensible for small, sparse, high-SNR fields, and immune to segmentation artefacts. It does not scale past a handful of sessions and provides no neuropil model.
- **Skipping extraction entirely** — pixel-wise or field-average dF/F. Legitimate for bulk fiber-photometry-style questions where single-cell resolution is not the point, and much cheaper.

## See also

- [Calcium Imaging Analysis Guide (Claude Skill)](../../catalog/tools/calcium-imaging-analysis-guide.html)
- [Sort spikes from a Neuropixels recording](sort-spikes-from-neuropixels-recording.html) — the electrophysiological route to the same population-activity matrix, with a different set of failure modes.
- [Track animal pose in behavioral video](track-animal-pose-in-behavioral-video.html) — the behavioral covariate to regress these traces against.
- [Localize an implant tip to a brain atlas subregion](localize-implant-tip-in-brain-atlas-subregion.html) — establishing where a miniscope GRIN lens or fiber actually sat.

## Sources

- [Calcium Imaging Analysis Guide skill — `awesome_cognitive_and_neuroscience_skills/skills/calcium-imaging-analysis-guide/SKILL.md`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/calcium-imaging-analysis-guide/SKILL.md) — catalog `last_verified` 2026-08-02.
- [Giovannucci et al., *eLife* 8:e38173 (2019), doi:10.7554/eLife.38173](https://doi.org/10.7554/eLife.38173) — CaImAn, near-human ROI detection on nine annotated two-photon datasets; verified 2026-08-02 (this run).
- [Rupprecht et al., *Nat. Neurosci.* (2021), doi:10.1038/s41593-021-00895-5](https://doi.org/10.1038/s41593-021-00895-5) — CASCADE ground-truth database and spike inference; verified 2026-08-02 (this run).
- [Zhou et al., *Cell Rep. Methods* (2023), doi:10.1016/j.crmeth.2023.100462](https://doi.org/10.1016/j.crmeth.2023.100462) — ENS2 spike inference benchmark.
- [Ananthamurthy & Bhalla, *eNeuro* (2023), doi:10.1523/ENEURO.0007-22.2023](https://doi.org/10.1523/ENEURO.0007-22.2023) — synthetic ground truth for downstream time-cell detection.
- [Cantu et al., *Front. Neural Circuits* (2020), doi:10.3389/fncir.2020.00025](https://doi.org/10.3389/fncir.2020.00025) — EZcalcium, the GUI alternative.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=extract-calcium-traces-from-two-photon-video&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fextract-calcium-traces-from-two-photon-video.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
