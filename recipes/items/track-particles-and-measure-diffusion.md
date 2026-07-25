---
title: Track single particles and measure their diffusion coefficient
parent: All recipes
grand_parent: Recipes
nav_order: 46
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-25
summary: Use the trackpy skill to locate and link particles across video-microscopy frames, then compute MSD and diffusion coefficients into a committed trajectory table.
---

# Track single particles and measure their diffusion coefficient

Hand Claude Code a fluorescence or brightfield video-microscopy stack and get back linked particle trajectories, a mean-squared-displacement (MSD) curve, and per-track diffusion coefficients — produced by the [trackpy skill](../../catalog/tools/trackpy-particle-tracking.html) and saved as a re-runnable script.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Quantifying how fast a labeled molecule, vesicle, or bead moves — and whether that motion is free Brownian, confined, or directed — is a routine but fiddly single-particle-tracking (SPT) task. From a TIRF or spinning-disk movie you need to detect every spot in every frame at sub-pixel accuracy, link those detections into trajectories across frames (handling blinking, crossing tracks, and particles that enter or leave), drop tracks too short to trust, and only then fit MSD-vs-lag to extract a diffusion coefficient and classify the motion mode. Done by hand or with a one-off script, the linking parameters and the track-length cutoff are undocumented degrees of freedom that change the answer, and the trajectory table rarely survives in a form a reviewer can re-run.

"Solved" looks like: point at the image stack, get back a linked-trajectories table (particle id, frame, x, y), an ensemble and per-particle MSD, fitted diffusion coefficients with the motion mode, and a trajectory overlay — all from a committed script that re-runs identically, with the detection, linking, and cutoff parameters recorded so the diffusion coefficient in the figure is auditable.

## Recommended approach

1. **Install the [trackpy skill](../../catalog/tools/trackpy-particle-tracking.html).** It ships in the [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) collection — clone once and load as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm it appears under `/plugin` → Installed. The skill installs `trackpy` (+`pims`) and runs locally — no upload.

2. **Stage the movie and record the acquisition metadata.** Put the raw stack (TIFF stack, AVI, or an image series) in one folder. Write down the numbers the physics depends on: **pixel size** (µm/px), **frame interval** (s), the approximate particle **diameter in pixels** (must be odd for trackpy's feature finder), and the imaging modality (bright spots on dark for fluorescence; invert for dark-on-bright brightfield).

3. **Generate a committed tracking + diffusion script.** Have Claude write the analysis to a file rather than tuning parameters interactively, so the same detection and linking apply to every movie:

   ```
   Use the trackpy skill on ./movies/cell01.tif.
   Write a script track_and_diffuse.py that:
     - locates features per frame with tp.locate (diameter=<D> px,
       minmass set from the mass histogram), inverting if brightfield,
     - links into trajectories with tp.link (search_range=<R> px,
       memory=<M> frames) and drops tracks shorter than <L> frames
       with tp.filter_stubs,
     - converts to physical units using pixel_size=<µm/px> and
       frame_interval=<s>, then computes ensemble and per-particle MSD
       (tp.emsd / tp.imsd) and fits the linear regime for the diffusion
       coefficient D and the anomalous exponent alpha,
     - writes trajectories.csv (particle, frame, x, y), msd.csv, and
       diffusion.csv (particle, D_um2_s, alpha, n_frames),
     - saves a trajectory overlay (tracks_overlay.png),
     - records skill commit, trackpy/pims versions, pixel size, frame
       interval, diameter, search_range, memory, stub cutoff, and the
       stack sha256 in provenance.json.
   Then summarize diffusion.csv: median D and the alpha distribution.
   ```

   Pin the environment (`requirements.txt` / `environment.yml`) with the exact `trackpy`/`pims` versions, and commit `track_and_diffuse.py`, the pinned env, and `provenance.json`. The recorded pixel size, frame interval, and linking parameters are what make a diffusion coefficient reproducible — see the [reproducibility guide](../../guide/advanced/reproducibility.html).

4. **QC the linking before you trust D.** Overlay `tracks_overlay.png` on the movie and check the two failure modes that corrupt SPT: a `search_range` set too large (tracks jump between distinct particles) or too small (one particle splits into several short tracks). Also confirm the MSD is fit only in its linear regime — the tail is noisy because few particles survive to long lags. Adjust parameters in the script and re-run; never hand-edit `diffusion.csv`.

5. **Hand off downstream.** `diffusion.csv` and `msd.csv` are the artifacts: compare median D or the confined/Brownian/directed mode across conditions in your statistics, and cite the committed script and `provenance.json` in the methods.

## Why this assembly

Rung 2 of the simplicity ladder. Plain Claude Code (rung 1) can call generic image code, but robust sub-pixel detection, frame-to-frame linking with memory, and the MSD-to-diffusion fit are exactly what the mature `trackpy` implementation of the Crocker–Grier algorithm provides — the model won't reconstruct that reliably from prompt text, and the linking parameters are where reproducibility is won or lost. The skill wraps that library and adds a committed, provenance-tracked run with a trajectory overlay, a real gain over rung 1. There is nothing to escalate to at rung 3/4: this is one input type and one well-bounded video-to-table task. The judgment calls the recipe surfaces explicitly — diameter, `search_range`, and the MSD linear regime — are the ones that actually matter.

## Availability

Fully open. `trackpy` is BSD-3-Clause; the SciAgent-Skills wrapper is CC BY 4.0. The library installs locally and runs with no account, API key, or upload. TIFF/AVI and CSV are open formats.

## Compute requirements

Laptop-sufficient. Detection and linking on a typical few-hundred-frame movie run in seconds to a couple of minutes on a laptop CPU — no GPU. Memory scales with frame size and particle count; very long movies or dense fields are the cases where you batch or downsample. Trajectory tables and MSD outputs are small CSVs.

## Evidence

Reported. The quantitative core — locate particles, link into trajectories, fit MSD-vs-lag for a diffusion coefficient, and classify the motion mode — is the canonical SPT analysis. The MSD-plot approach to distinguishing stationary, Brownian, directed, and confined diffusion was established for membrane receptors labeled and tracked in live cells ([Kusumi, Sako & Yamamoto, *Biophys. J.* 1993](https://pubmed.ncbi.nlm.nih.gov/8298032/)) and remains the standard readout: quantitative MSD analysis of individually tracked proteins in supported bilayers ([Taylor et al., *Methods Mol. Biol.* 2019](https://pubmed.ncbi.nlm.nih.gov/31218627/)) and GFP-tagged membrane-protein diffusion mapping by TIRF ([Vu et al., *BBA Biomembranes* 2021](https://pubmed.ncbi.nlm.nih.gov/34352241/)) both extract D and the motion mode from exactly this chain. `trackpy` is a widely used implementation of the Crocker–Grier detection-and-linking algorithm the field standardized on.

No head-to-head benchmark of the *agent-driven* assembly versus a hand-written trackpy script exists — the skill buys a local, committed, reproducible run with a trajectory overlay, not a new tracking method. That gap is why this recipe is `Reported`, not `Validated`.

## Alternatives considered

- **TrackMate (Fiji) GUI (rung 0–1).** The interactive ImageJ/Fiji tracker is the simplest path for a one-off movie with human-in-the-loop curation of tracks. The trackpy skill is worth it when you want the detection/linking parameters and the MSD fit pinned and re-runnable across a whole dataset.
- **[Segment and quantify cells in a microscopy image](segment-and-quantify-cells-in-microscopy.html).** Reach for that when you need per-cell masks and morphology in a *static* image, not motion across frames. Cross-referenced because both are committed image-to-table cell-biology quantifications; a segmentation step can even seed the ROIs a tracking run operates within.
- **scikit-image by hand (rung 1–2).** [scikit-image](../../catalog/tools/scikit-image-processing.html) offers blob detection but no trajectory linking or MSD machinery — you'd re-implement the hard parts. Drop to it only for a detection geometry trackpy can't handle.

## See also

- [trackpy (Claude Skill)](../../catalog/tools/trackpy-particle-tracking.html)
- [scikit-image (Claude Skill)](../../catalog/tools/scikit-image-processing.html) — classical image processing and blob detection.
- [Segment and quantify cells in a microscopy image](segment-and-quantify-cells-in-microscopy.html) — the static-image counterpart.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [Kusumi, Sako & Yamamoto, "Confined lateral diffusion of membrane receptors as studied by single particle tracking," *Biophys. J.* 1993](https://pubmed.ncbi.nlm.nih.gov/8298032/) — published 1993; verified 2026-07-25 (this run).
- [Taylor, Poudel & Brozik, "A Guide to Tracking Single Membrane Proteins…," *Methods Mol. Biol.* 2019](https://pubmed.ncbi.nlm.nih.gov/31218627/) — published 2019; verified 2026-07-25 (this run).
- [Vu et al., "Evaluation of diffusion coefficient of P-glycoprotein molecules labeled with GFP…," *BBA Biomembranes* 2021](https://pubmed.ncbi.nlm.nih.gov/34352241/) — published 2021; verified 2026-07-25 (this run).
- [`jaechang-hits/SciAgent-Skills` (`skills/cell-biology/trackpy-particle-tracking/SKILL.md`)](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/cell-biology/trackpy-particle-tracking/SKILL.md) — skill source; verified 2026-07-25 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=track-particles-and-measure-diffusion&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftrack-particles-and-measure-diffusion.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
