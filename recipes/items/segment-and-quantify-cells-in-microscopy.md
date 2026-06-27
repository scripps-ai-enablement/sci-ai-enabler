---
title: Segment and quantify cells in a microscopy image
parent: All recipes
grand_parent: Recipes
nav_order: 23
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-06-27
summary: Use the Cellpose skill to segment cells or nuclei in fluorescence/brightfield images and extract per-cell counts, areas, and intensities to a committed table.
---

# Segment and quantify cells in a microscopy image

Hand Claude Code a microscopy image (or a folder of them) and get back per-cell label masks plus a quantitative table — cell count, area, shape, and per-channel intensity for every object — produced by the [Cellpose skill](../../catalog/tools/cellpose-cell-segmentation.html) and saved as a re-runnable script.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Counting cells and measuring their morphology or marker intensity from microscopy is one of the most common quantitative tasks in cell biology — scoring a knockdown phenotype, quantifying nuclear translocation, measuring cell size across conditions. Manual counting in ImageJ is slow, subjective, and irreproducible across operators. Classic thresholding/watershed breaks down on touching cells, uneven illumination, and the varied staining you get across a real plate. The hard part is robust *instance* segmentation — separating each cell from its neighbors — without hand-tuning parameters per image or training a model.

"Solved" looks like: point at an image (or directory), get back a label mask per image and one tidy table with one row per cell (image, object id, area, centroid, mean intensity per channel), produced by a committed script you can re-run on the next plate with identical settings — so the count that lands in a figure is auditable, not a number a person eyeballed once.

## Recommended approach

1. **Install the [Cellpose skill](../../catalog/tools/cellpose-cell-segmentation.html).** It ships in the [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) collection — clone once and load as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm Cellpose appears under `/plugin` → Installed. The skill installs the `cellpose` Python package and runs locally — no upload.

2. **Stage the images and note the channels.** Put the images in one folder. Record, for each image: which channel holds the object to segment (the `cytoplasm`/membrane stain or the `nuclei` stain) and which channels are the markers you want to quantify. Pick the model up front — `nuclei` for DAPI/Hoechst, `cyto3` (the generalist) for whole cells/brightfield. Estimate a typical cell diameter in pixels; Cellpose uses it to set scale.

3. **Generate a committed segmentation + quantification script.** Have Claude write the analysis to a file rather than running it interactively, so the same parameters apply to every plate:

   ```
   Use the Cellpose skill to segment every image in ./images/.
   Write a script segment_and_quantify.py that:
     - runs Cellpose with model=cyto3 (or 'nuclei'), diameter=<D> px,
       channels=[<seg>, <nuc>], on each image,
     - saves the integer label mask per image (masks/<name>_masks.tif),
     - uses scikit-image regionprops to emit one row per cell to
       cells.csv: image, label, area, eccentricity, centroid_x,
       centroid_y, and mean intensity for each marker channel,
     - records cellpose version, model name, diameter, flow/cellprob
       thresholds, and a sha256 of each input image in provenance.json.
   Then summarize cells.csv: cells per image and median area per image.
   ```

   Pin the environment (`requirements.txt` or `environment.yml`) with the exact `cellpose` and `scikit-image` versions, and commit `segment_and_quantify.py`, the pinned env, and `provenance.json`. The recorded model name, diameter, and thresholds are what make a cell count reproducible — see the [reproducibility guide](../../guide/advanced/reproducibility.html).

4. **QC the masks before you trust the numbers.** Have Claude overlay a few masks on the source images and check for the two failure modes that quietly corrupt counts: over-merging (two touching cells fused into one label) and over-splitting (one cell broken into fragments). If they appear, adjust `diameter`, `flow_threshold`, or `cellprob_threshold` in the script and re-run — never hand-edit the output table.

5. **Hand off downstream.** `cells.csv` is the artifact: feed it to your statistics (compare median area or marker intensity across conditions) or to the relevant downstream recipe. The masks are reusable for tracking or co-localization.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill does the segmentation, and the same skill's environment carries `scikit-image` for the regionprops measurement, so no extra component is needed. Rung 1 (plain Claude Code) can't segment touching cells robustly: instance segmentation across varied staining is exactly what Cellpose's pretrained generalist models buy you, and the model can't reproduce that from prompt instructions alone. Rung 3+ is overkill — there is one input type and one well-bounded task. The only judgement call is model and diameter, which the recipe pins explicitly.

## Availability

Fully open. Cellpose is BSD-3-Clause; the SciAgent-Skills wrapper is CC BY 4.0. Pretrained models (`cyto3`, `nuclei`, `tissuenet`) download once and run locally — no account, no API key, no image upload. TIFF/PNG and CSV are open formats.

## Compute requirements

Laptop-sufficient. Cellpose runs on CPU; a typical 2D image (~1–4 megapixels) segments in seconds to a couple of minutes per image on a laptop CPU, faster with a CUDA GPU. The pretrained model weights are a one-time download of tens of MB. A plate of a few hundred images is laptop-scale as a loop; very large whole-slide images or 3D z-stacks are the cases where a GPU starts to matter — name that step if you hit it.

## Evidence

Reported. Cellpose is the field-standard generalist segmentation method — trained on >70,000 manually segmented objects across highly varied image types, it segments cells, membranes, and nuclei without retraining or per-image parameter tuning ([Stringer et al., *Nature Methods* 2021](https://www.nature.com/articles/s41592-020-01018-x)), with Cellpose3 adding one-click image restoration for noisy/blurry/undersampled inputs ([Stringer & Pachitariu, *Nature Methods* 2025](https://www.nature.com/articles/s41592-025-02595-5)). It is routinely the segmentation step in published quantification pipelines (e.g., single-cell/phagosome tracking via Cellpose + TrackMate, [Augenstreich et al., *Biol. Open* 2024](https://doi.org/10.1242/bio.060555)).

No head-to-head benchmark of the *agent-driven* assembly versus a hand-written Cellpose script is published — the skill buys a local, committed, reproducible run, not a new method. That gap is why this recipe is `Reported`, not `Validated`.

## Alternatives considered

- **scikit-image watershed (rung 1–2, simpler).** For well-separated, evenly-lit nuclei on a clean background, classic thresholding + watershed in [scikit-image](../../catalog/tools/scikit-image-processing.html) is lighter and fully transparent. Reach for it when cells don't touch and staining is uniform; reach for Cellpose the moment cells overlap or staining varies across the image.
- **Cellpose GUI (no skill).** The desktop Cellpose GUI is the simplest path for a one-off interactive segmentation and for human-in-the-loop curation. The skill is worth it when you want the run scripted, batched over many images, and committed with pinned parameters alongside the data.
- **nnU-Net (rung 2, different domain).** The [medical-image segmentation recipe](segment-organ-or-tumor-in-medical-image.html) targets 3D radiology volumes (CT/MRI) and requires labeled training data and a GPU. For cell/nucleus microscopy with no training labels, Cellpose's pretrained generalist models are the right tool.

## See also

- [Cellpose (Claude Skill)](../../catalog/tools/cellpose-cell-segmentation.html) — DL cell/nucleus segmentation.
- [scikit-image (Claude Skill)](../../catalog/tools/scikit-image-processing.html) — classical image processing and regionprops.
- [Segment an organ or tumor in a medical image with nnU-Net](segment-organ-or-tumor-in-medical-image.html) — the radiology-volume counterpart.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [Stringer, Wang, Michaelos & Pachitariu, "Cellpose: a generalist algorithm for cellular segmentation," *Nature Methods* 18:100–106](https://www.nature.com/articles/s41592-020-01018-x) — published 2021; verified 2026-06-27 (this run).
- [Stringer & Pachitariu, "Cellpose3: one-click image restoration for improved cellular segmentation," *Nature Methods*](https://www.nature.com/articles/s41592-025-02595-5) — published 2025; verified 2026-06-27 (this run).
- [Augenstreich et al., "da_Tracker," *Biol. Open* 13:bio060555](https://doi.org/10.1242/bio.060555) — Cellpose-based quantification pipeline; published 2024; verified 2026-06-27 (this run).
- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) — Cellpose skill source; verified 2026-06-27 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=segment-and-quantify-cells-in-microscopy&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fsegment-and-quantify-cells-in-microscopy.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
