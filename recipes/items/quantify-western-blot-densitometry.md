---
title: Quantify a western blot from a scanned image
parent: All recipes
grand_parent: Recipes
nav_order: 21
problem_class: Data analysis
subject_areas: [Molecular and Cellular Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-25
summary: Use the Western Blot Quantification skill to detect bands, normalize target to a loading control, aggregate replicates, and emit a committed densitometry table.
---

# Quantify a western blot from a scanned image

Hand Claude Code a scanned blot image and get back per-lane band intensities, a target-over-loading-control normalized value for every lane, replicate-level statistics, and a QC overlay — produced by the [Western Blot Quantification skill](../../catalog/tools/western-blot-quantification.html) and saved as a re-runnable script.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Molecular and Cellular Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Densitometry of western blots is one of the most common — and most quietly irreproducible — quantitative steps in cell biology. A postdoc scores a knockdown or a phospho-signal by drawing rectangles in ImageJ, subtracting a background band she picks by eye, dividing by a GAPDH lane, and pasting the numbers into a spreadsheet. Every one of those choices (ROI placement, background model, which loading control, how replicates are combined) is a degree of freedom that changes the fold-change, and none of it is captured anywhere the reviewer can see. Housekeeping-protein normalization is itself a known bias: β-actin, GAPDH, and tubulin are not constant across injury, disease, or hormone state.

"Solved" looks like: point at the blot image, get back one tidy table with a row per lane (lane, target raw intensity, loading-control raw intensity, normalized ratio), replicate-aggregated fold-changes with SD/SEM, and a verification image showing exactly which pixels each band ROI covered — all produced by a committed script that re-runs identically on the next blot, so the number in the figure is auditable rather than eyeballed once.

## Recommended approach

1. **Install the [Western Blot Quantification skill](../../catalog/tools/western-blot-quantification.html).** It ships in the [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) collection — clone once and load as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm it appears under `/plugin` → Installed. The skill runs its Python locally — no upload.

2. **Stage the image and record the lane map.** Save the raw scan (uncropped, unadjusted TIFF/PNG — never a JPEG a journal compressed) in one folder. Write down, per lane: the sample/condition, which bands are the target, and which are the loading control. Prefer a **total-protein** loading control (stain-free or REVERT) over a single housekeeping protein where you have it — it is materially more accurate and reproducible (see Evidence).

3. **Generate a committed quantification script.** Have Claude write the analysis to a file rather than eyeballing ROIs interactively, so the same detection and normalization apply to every blot:

   ```
   Use the Western Blot Quantification skill on ./blots/blot01.tif.
   Write a script quantify_blot.py that:
     - uses analyze_pixel_distribution / find_roi_from_image to detect
       the target and loading-control band ROIs per lane,
     - subtracts local background and integrates band intensity,
     - normalizes each lane's target to its loading control, then to
       the control lane, emitting one row per lane to blot01_quant.csv
       (lane, condition, target_raw, loading_raw, normalized_ratio),
     - aggregates biological replicates (mean, SD, SEM, fold-change vs
       control) into replicate_summary.csv,
     - saves a verification overlay (roi_overlay.png) showing every ROI,
     - records skill commit, package versions, the image sha256, the
       normalization method, and background model in provenance.json.
   Then summarize replicate_summary.csv.
   ```

   Pin the environment (`requirements.txt` / `environment.yml`) with the exact package versions, and commit `quantify_blot.py`, the pinned env, the raw image, and `provenance.json`. The recorded ROI method, background model, and normalization choice are what make the fold-change reproducible — see the [reproducibility guide](../../guide/advanced/reproducibility.html).

4. **QC the ROI overlay before you trust the numbers.** Open `roi_overlay.png` and check the two failure modes that silently corrupt densitometry: an ROI that clips a saturated band (integrated intensity plateaus — the signal is out of linear range, re-scan at lower exposure) and a background window that overlaps a neighboring band. If either appears, adjust the detection threshold or background window in the script and re-run — never hand-edit `blot01_quant.csv`.

5. **Hand off downstream.** `replicate_summary.csv` is the artifact: feed it to your statistics (report the test and n) and cite the committed script and `provenance.json` in the methods. The per-lane table is the audit trail for any reviewer who asks how a band became a number.

## Why this assembly

Rung 2 of the simplicity ladder. Plain Claude Code (rung 1) can write ad-hoc densitometry code, but it has no encoded convention for band ROI detection, background subtraction, or the two-step target-to-loading-control normalization — so every run drifts exactly where reproducibility matters. The skill encodes that workflow (`analyze_pixel_distribution`/`find_roi_from_image` for detection, loading-control-then-target normalization, replicate aggregation) and emits a verification grid, which is a real gain over rung 1. There is nothing to escalate to at rung 3/4: this is a single, well-bounded image-to-table task. The one judgment call the recipe surfaces explicitly is the loading control (prefer total-protein), because that is the dominant bias in the published literature.

## Availability

Fully open. The Western Blot Quantification skill is part of the community SciAgent-Skills collection (CC BY 4.0); it installs its own Python dependencies and runs locally with no account, API key, or image upload. TIFF/PNG and CSV are open formats.

## Compute requirements

Laptop-sufficient. Band detection and integration on a single scanned blot (a few megapixels) run in seconds on a laptop CPU — no GPU. A folder of dozens of blots is laptop-scale as a loop. The only "heavy" resource is disk for keeping uncompressed raw scans under version control.

## Evidence

Reported. The quantitative core — integrated-density band quantification normalized to a loading control, with total-protein normalization preferred over a single housekeeping protein — is field-standard and directly evidenced. A stain-free total-protein control reduced variability enough to cut the samples needed for significance by >50% versus actin/tubulin ([Maloy et al., *Anal. Biochem.* 2022](https://pubmed.ncbi.nlm.nih.gov/35931182/)); REVERT total-protein stain gave a wider linear range and better gel-to-gel consistency than GAPDH/actin/tubulin in brain homogenates ([Kirshner & Gibbs, *Mol. Cell. Endocrinol.* 2018](https://pubmed.ncbi.nlm.nih.gov/29396126/)); and titration-based WB further removes housekeeping-normalization bias using regression-curve quantification ([Maestri et al., *PLOS ONE* 2025](https://pubmed.ncbi.nlm.nih.gov/40504814/)). The skill's two-step normalization and replicate aggregation follow this practice.

No head-to-head benchmark of the *agent-driven* assembly versus a hand-run ImageJ densitometry exists — the skill buys a local, committed, reproducible run with a verification overlay, not a new measurement method. That gap is why this recipe is `Reported`, not `Validated`.

## Alternatives considered

- **ImageJ/Fiji gel-analysis GUI (rung 0–1).** The classic path: draw lanes, plot profiles, measure peaks by hand. Reach for it for a one-off blot where interactive curation is faster than scripting. The skill is worth it when you want the ROIs, background model, and normalization pinned and re-runnable across every blot in a paper.
- **scikit-image by hand (rung 1–2).** [scikit-image](../../catalog/tools/scikit-image-processing.html) can do the thresholding/regionprops that underlie band detection, but you then re-implement ROI logic and the two-step normalization yourself. The skill encodes that; drop to scikit-image only for a non-standard blot geometry the skill can't detect.
- **[Segment and quantify cells in a microscopy image](segment-and-quantify-cells-in-microscopy.html).** Different problem — instance segmentation of cells, not lane/band densitometry. Cross-referenced because both are committed image-to-table cell-biology quantifications.

## See also

- [Western Blot Quantification (Claude Skill)](../../catalog/tools/western-blot-quantification.html)
- [scikit-image (Claude Skill)](../../catalog/tools/scikit-image-processing.html) — classical image processing and regionprops.
- [Segment and quantify cells in a microscopy image](segment-and-quantify-cells-in-microscopy.html) — the microscopy-image counterpart.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [Maloy et al., "Stain-Free total-protein normalization enhances the reproducibility of Western blot data," *Anal. Biochem.* 2022](https://pubmed.ncbi.nlm.nih.gov/35931182/) — published 2022; verified 2026-07-25 (this run).
- [Kirshner & Gibbs, "Use of the REVERT total protein stain as a loading control…," *Mol. Cell. Endocrinol.* 2018](https://pubmed.ncbi.nlm.nih.gov/29396126/) — published 2018; verified 2026-07-25 (this run).
- [Maestri et al., "Titration-WB: A methodology for accurate quantitative protein determination…," *PLOS ONE* 2025](https://pubmed.ncbi.nlm.nih.gov/40504814/) — published 2025; verified 2026-07-25 (this run).
- [`jaechang-hits/SciAgent-Skills` (`skills/lab-automation/western-blot-quantification/SKILL.md`)](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/lab-automation/western-blot-quantification/SKILL.md) — skill source; verified 2026-07-25 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=quantify-western-blot-densitometry&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fquantify-western-blot-densitometry.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
