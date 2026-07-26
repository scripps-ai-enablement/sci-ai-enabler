---
title: Tile and stain-normalize a whole-slide image for ML
parent: All recipes
grand_parent: Recipes
nav_order: 27
problem_class: Data analysis
subject_areas: [Translational Medicine]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Workstation with GPU
last_verified: 2026-07-26
summary: Use the histolab skill to turn a gigapixel H&E slide into a tissue-masked, stain-normalized tile dataset with a committed, re-runnable script.
---

# Tile and stain-normalize a whole-slide image for ML

Hand Claude Code a whole-slide image (`.svs`/`.tiff`/`.ndpi`) and get back a folder of tissue-only, stain-normalized tiles plus a manifest — produced by the [histolab skill](../../catalog/tools/histolab.html) and saved as a re-runnable script, ready to feed a downstream classifier.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Translational Medicine |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Workstation with GPU |

## Problem

A computational-pathology project almost always starts the same way: you have a stack of gigapixel H&E whole-slide images (WSIs) and you need a tidy tile dataset before any model can train. That preprocessing is where projects quietly go wrong. Naive tiling scoops up huge amounts of background glass, pen marks, and blur; tile coordinates aren't recorded, so a prediction can't be traced back to a slide region; and H&E color varies so much scanner-to-scanner and lab-to-lab that a model trained on one site's stain collapses on another's. Re-implementing tissue detection, tile extraction, and stain normalization by hand — against the OpenSlide API — is fiddly and rarely reproducible across team members.

"Solved" looks like: point at a slide (or a folder of them), get back a folder of fixed-size, tissue-only, stain-normalized tiles, a manifest mapping every tile to its slide and (x, y) coordinate and magnification, and a committed script you can re-run on the next batch with identical settings — so the dataset a model trains on is auditable, not a one-off pile of PNGs.

## Recommended approach

1. **Install the [histolab skill](../../catalog/tools/histolab.html).** It ships in the K-Dense collection — install once and enable the skill:

   ```
   npx skills add K-Dense-AI/scientific-agent-skills
   ```

   Enable the `histolab` skill when prompted. Claude runs the skill's Python locally via Bash (it wraps the `histolab` package over an OpenSlide/`large_image` backend); install its declared dependencies on first use. Keep the WSIs on local disk — they are read from there, not uploaded.

2. **Inspect the slides and pick a working magnification.** WSIs are pyramidal; the level you tile at sets the effective microns-per-pixel and changes everything downstream. Confirm it before extracting:

   ```
   Use the histolab skill. Load my slides in ./slides/ and for each one
   report the available pyramid levels, the native magnification, and
   microns-per-pixel at each level. Recommend a tiling level that gives
   ~0.5 um/px (20x) and state which level that is per slide — do not tile
   yet.
   ```

3. **Generate a committed tiling + normalization script.** Have Claude write the pipeline to a file so the same settings apply to every batch, not an interactive one-off:

   ```
   Use the histolab skill to write a script tile_wsi.py that, for every
   slide in ./slides/:
     - detects tissue with histolab's tissue mask (drop background/pen),
     - extracts 256x256 tiles at the 20x level with a minimum
       tissue-percent threshold (e.g. 80%) using GridTiler,
     - applies Macenko (or Reinhard) stain normalization to a single
       committed reference tile (save the reference image),
     - writes tiles to tiles/<slide_id>/ and a manifest.csv with one row
       per tile: slide_id, tile_path, level, mpp, x, y, tissue_pct,
     - records histolab version, OpenSlide version, tile size, level,
       tissue threshold, normalizer + reference-tile sha256, and a sha256
       of each slide in provenance.json.
   Then report tiles per slide and total tile count.
   ```

   Pin the environment (`requirements.txt` or `environment.yml`) with exact `histolab` and `openslide-python` versions, and commit `tile_wsi.py`, the pinned env, the reference tile, and `provenance.json`. The recorded level, tissue threshold, and normalization reference are what make a tile dataset reproducible — see the [reproducibility guide](../../guide/advanced/reproducibility.html).

4. **QC the tiles before training on them.** Have Claude render a contact sheet of random tiles per slide and check the two failure modes that silently poison a dataset: background/pen/blur tiles that slipped past the tissue mask, and over-aggressive normalization that washed out real tissue color. If they appear, raise the tissue threshold, swap the reference tile, or change normalizer in the script and re-run — never hand-delete tiles from the output folder.

5. **Hand off downstream.** `manifest.csv` + the `tiles/` folder is the artifact: feed it to your model training, or to a slide-level aggregation (MIL) step. Because every tile row carries its slide and (x, y), a tile-level prediction can always be mapped back to a region on the original slide for review.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill wraps the entire WSI preprocessing stack (OpenSlide-backed slide reading, tissue masking, grid/score tiling, and Macenko/Reinhard stain normalization), so a single component takes you from a gigapixel slide to a committed tile dataset. Rung 1 (plain Claude Code) can't do this defensibly: handling the OpenSlide pyramid API, robust tissue detection, and stain normalization correctly is exactly what histolab encapsulates, and Claude can't reconstruct that reliably from prompt instructions alone. Rung 3+ adds nothing for the preprocessing task itself; the discipline this recipe enforces (fixed magnification, a committed normalization reference, a coordinate manifest) is prompt instruction plus the skill, not a second tool. Escalate only when you bolt a trained model and slide-level aggregation onto the front of the tiles — a separate, downstream recipe.

## Availability

Fully open. histolab is Apache-2.0; the K-Dense skill wrapper is community OSS. OpenSlide and the pretrained-free tissue/stain operators run locally — no account, no API key, no slide upload. The catch is your *data*: clinical WSIs are PHI-adjacent and usually live under an institutional data-use agreement or IRB approval. Nothing leaves your machine here (the skill runs locally), but the de-identification status of the slides and any downstream sharing are governed by your institution, not this recipe. Public WSIs (TCGA via the GDC, CAMELYON) carry their own open or registered-access terms.

## Compute requirements

Workstation with GPU is the comfortable tier, though the GPU is for the *downstream* model, not this step. The tiling itself is CPU- and I/O-bound: a single ~1–3 GB WSI tiled at 20x yields thousands to tens of thousands of tiles and takes minutes on a workstation; a cohort of hundreds of slides is an overnight batch and produces tens to hundreds of GB of tiles, so plan disk accordingly. RAM of 16–32 GB is ample (histolab streams tiles rather than loading the whole slide). Macenko/Reinhard normalization adds modest per-tile cost. Name the tiling step as the heavy one if you hit wall-clock limits — parallelize across slides.

## Evidence

Reported. histolab is the peer-reviewed, purpose-built library for exactly this task — reproducible digital-pathology preprocessing (tissue detection, tile extraction, scoring, augmentation, and stain normalization) over OpenSlide/`large_image` backends, with multiplatform automated testing as a design goal ([Marcolini, Bussola, Arbitrio, Amgad, Jurman & Furlanello, "histolab: A Python library for reproducible Digital Pathology preprocessing with automated testing," *SoftwareX* 20:101237, 2022](https://doi.org/10.1016/j.softx.2022.101237)). Tile-based preprocessing of this kind is the standard front end of published WSI deep-learning pipelines.

No head-to-head benchmark of the *agent-driven* assembly (Claude driving the histolab skill) versus a hand-written histolab script is published — the skill buys a local, committed, reproducible run, not a new method. That gap is why this recipe is `Reported`, not `Validated`.

## Alternatives considered

- **pathml (rung 2, heavier).** For multiplexed immunofluorescence, spatial proteomics, or an integrated deep-learning pipeline (not just tiling), [pathml](../../catalog/tools/pathml.html) is the richer toolkit and the histolab skill's own docs point there. Reach for pathml when you need more than H&E tile prep; stay on histolab for the lightweight, fast, "just give me clean tiles" case.
- **OpenSlide / DeepZoom by hand (rung 1).** Writing the tiling loop directly against OpenSlide is possible but reinvents tissue masking and stain normalization, and rarely ends up reproducible. Only worth it if you have an idiosyncratic slide format histolab's backends don't support.
- **Cellpose-based quantification (rung 2, different question).** If your goal is counting and measuring individual cells rather than building a tile dataset for a slide-level model, the [microscopy segmentation recipe](segment-and-quantify-cells-in-microscopy.html) is the right tool — it does instance segmentation, not WSI tiling.

## See also

- [histolab (Claude Skill)](../../catalog/tools/histolab.html) — WSI tile extraction, tissue detection, stain normalization.
- [pathml (Claude Skill)](../../catalog/tools/pathml.html) — heavier digital-pathology / multiplexed-imaging toolkit.
- [Segment and quantify cells in a microscopy image](segment-and-quantify-cells-in-microscopy.html) — the cell-level counterpart for non-WSI microscopy.
- [Segment an organ or tumor in a medical image with nnU-Net](segment-organ-or-tumor-in-medical-image.html) — the radiology-volume segmentation counterpart.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [Marcolini, Bussola, Arbitrio, Amgad, Jurman & Furlanello, "histolab: A Python library for reproducible Digital Pathology preprocessing with automated testing," *SoftwareX* 20:101237](https://doi.org/10.1016/j.softx.2022.101237) — published 2022; verified 2026-06-28 (this run).
- [`histolab/histolab` (GitHub)](https://github.com/histolab/histolab) — library source, Apache-2.0; verified 2026-06-28 (this run).
- [`K-Dense-AI/scientific-agent-skills` — histolab skill](https://github.com/K-Dense-AI/scientific-agent-skills) — skill source; verified 2026-06-28 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=tile-and-normalize-whole-slide-image&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ftile-and-normalize-whole-slide-image.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
