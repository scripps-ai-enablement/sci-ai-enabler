---
title: Localize a fiber/probe implant tip in an Allen CCF subregion from 2D histology
parent: All recipes
grand_parent: Recipes
nav_order: 17
problem_class: Data analysis
subject_areas: [Neuroscience]
evidence_level: Proposed
complexity: Multi-tool harness
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-27
summary: Batch-register coronal histology with DeepSlice, detect each fiber tip, and read its Allen CCF subregion plus a hit/miss-vs-target verdict — a scripted QUINT replacement.
---

# Localize a fiber/probe implant tip in an Allen CCF subregion from 2D histology

Point Claude Code at a folder of coronal brain-section images with an intended target region; get back a committed script that predicts each section's cutting plane, detects the fiber/probe tip, maps it into Allen CCF space, and reports the subregion each tip lands in with a hit/miss verdict and a distance-to-boundary margin.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Neuroscience |
| **Evidence level** | Proposed |
| **Complexity** | Multi-tool harness |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

After an optogenetics or fiber-photometry experiment, you have to prove where the fiber actually sat. Standard practice is the QUINT workflow — DeepSlice or QuickNII to anchor each section to an atlas plane, VisuAlign for nonlinear correction, Nutil to quantify — a multi-program, GUI-driven chain that does not batch cleanly and leaves no re-runnable script behind. For a cohort of dozens of mice with several sections each, someone clicks through hundreds of images by hand, and the placement call ("tip in dorsal CA1, hit") is rarely captured as anything an auditor can re-run.

"Solved" for a *screening* pass looks like: hand over a folder of coronal sections plus the intended target acronym, get back a committed table with one row per section — predicted AP position, the CCF structure the tip pixel maps to, its acronym/full name and parent structures, a hit/miss verdict against the target, and a **distance-to-boundary margin** (how many microns the tip sits from the nearest structure edge) so a marginal call is visible rather than silently binarized. This is a screening verdict, not a publication-grade boundary claim (see Compute/Evidence).

## Recommended approach

Rung 3 — a three-component toolbelt driving two directly-imported dependencies plus one catalogued Claude Skill. The hard step is cutting-plane prediction for off-axis sections; do **not** substitute a naive affine warp onto a hand-picked coronal plate (see Alternatives).

1. **Install the [scikit-image skill](../../catalog/tools/scikit-image-processing.html)** for the per-section tip detection (install commands on the catalog page). Add the two Python dependencies below to your project environment (see [Dependencies](#dependencies)).

2. **Predict each section's cutting plane with DeepSlice.** DeepSlice reads the whole folder and emits one QuickNII-compatible JSON alignment (anchoring vectors `ox,oy,oz,ux,uy,uz,vx,vy,vz` per section) — this is what handles non-orthogonal planes that a fixed coronal plate cannot:

   ```
   Write predict_planes.py using DeepSlice (from DeepSlice import DSModel):
     model = DSModel("mouse")
     model.predict("./sections/", ensemble=True, section_numbers=True)
     model.propagate_angles()          # enforce a consistent cutting angle
     model.save_predictions("out/alignment")   # QuickNII-compatible JSON
   Log the DeepSlice version and the per-section anchoring vectors.
   ```

3. **Detect the fiber/probe tip per section with scikit-image.** The tip is the deepest point of the lesion/DiI track. Have the assistant write a detector (threshold the track channel, take the connected component, find its ventral-most / distal extremum) and require a human to confirm the detected pixel on an overlay before trusting downstream — tip detection is the step most likely to misfire on artefacts:

   ```
   In detect_tips.py, for each section: isolate the track channel,
   segment the track (Otsu/threshold + morphology), take the largest
   component, and record the tip pixel as its distal extremum along
   the insertion axis. Save an overlay PNG per section (tip marked)
   to out/overlays/ for human QC. Emit out/tips.csv: section, x_px, y_px.
   ```

4. **Map the tip pixel into CCF and read the subregion.** Apply the section's DeepSlice anchoring vectors to convert the tip pixel `(x,y)` into a CCF voxel `(ap,dv,ml)`, then look it up with brainglobe-atlasapi:

   ```
   In localize_tips.py:
     from brainglobe_atlasapi import BrainGlobeAtlas
     atlas = BrainGlobeAtlas("allen_mouse_25um")
     # map tip pixel -> CCF voxel via the section's anchoring vectors
     sid  = atlas.annotation[ap, dv, ml]                 # structure id
     row  = atlas.lookup_df.loc[atlas.lookup_df.id == sid]  # acronym, name
     ancestors = atlas.get_structure_ancestors(row.acronym)  # hierarchy roll-up
   For the distance-to-boundary margin, compute the shortest distance
   from the tip voxel to the nearest voxel of a *different* structure id
   in atlas.annotation, times the 25 um voxel size.
   ```

5. **Emit the verdict table.** For each section write: predicted AP, tip CCF voxel, structure id/acronym/name, its parent structures, a `hit` boolean (target acronym is the structure or one of its ancestors), and `margin_um` (distance to boundary). A tip whose `margin_um` is smaller than the plane-prediction AP error should be reported as *marginal*, not a clean hit/miss.

6. **Record provenance.** Have the scripts write `out/provenance.json`: DeepSlice version + model (`mouse`), the atlas name and BrainGlobe atlas version (`allen_mouse_25um`), the voxel size, the tip-detection threshold parameters, the input-folder `sha256` manifest, the run date, and the model/agent identity. See the [reproducibility guide](../../guide/advanced/reproducibility.html).

The durable artifact is `predict_planes.py` + `detect_tips.py` + `localize_tips.py` + the pinned `requirements.txt` + the emitted `alignment.json`, `tips.csv`, `placements.csv`, overlay PNGs, and `provenance.json` — all under version control. Re-running on the same folder reproduces the placement table (modulo DeepSlice ensemble stochasticity, which the provenance records).

## Dependencies

Libraries this recipe's scripts install and import directly. Claude Code installs these into your project environment — they are not available in Claude.ai chat. DeepSlice fetches its trained model weights on first use (the `DSModel("mouse")` call downloads them), so the first run needs network access and a few hundred MB of disk; the import check below proves the package imports, not that the weight download succeeded. DeepSlice is **GPL-3.0** (copyleft) — redistributing a modified pipeline carries its license obligations, though running it in-house does not.

| Package | Registry | Pinned | License | Import | Source (fetched 2026-07-27) |
|---|---|---|---|---|---|
| DeepSlice | PyPI | `1.2.8` | GPL-3.0-only | `DeepSlice` | [Carey et al., *Nat Commun* 2023](https://doi.org/10.1038/s41467-023-41645-4) |
| brainglobe-atlasapi | PyPI | `2.3.1` | BSD-3-Clause | `brainglobe_atlasapi` | [Claudi et al., *JOSS* 2020](https://doi.org/10.21105/joss.02668) |

```
pip install DeepSlice==1.2.8 brainglobe-atlasapi==2.3.1
python3 -c "import DeepSlice; import brainglobe_atlasapi"
```

## Why this assembly

Rung 3 (multi-tool harness). Two of the three components carry non-substitutable capability: DeepSlice is the only catalogued/pip-installable step that predicts a *cutting plane* (including off-axis sections) rather than assuming a fixed coronal plate, and brainglobe-atlasapi is the CCF voxel→structure lookup that turns a coordinate into a named subregion. scikit-image supplies the per-section tip detection. Rungs 1–2 fail: plain Claude Code cannot register a section to CCF without a plane model, and there is no single catalogued Skill/MCP that both predicts the plane and reads the subregion — the read-only `allenbrain-mcp` (Alpha) does neither. The escalation to rung 3 is forced by the task, not by preference; it is not rung 4 because no autonomous system targets implant localization and the problem is well-scoped.

## Availability

Fully open. brainglobe-atlasapi is BSD-3-Clause; the scikit-image skill and its library are BSD/OSS. DeepSlice is **GPL-3.0** — fine to run in-house, but if you redistribute a derived pipeline you inherit copyleft obligations; that is the strictest license in the stack and it keeps the recipe at `Fully open` (no subscription, no institutional gate). No account required. The recipe assumes mouse sections in the Allen CCF; DeepSlice ships a rat model too, but the brainglobe atlas name and the QC thresholds would need adjusting.

## Compute requirements

Laptop. DeepSlice inference is CPU-only and processes a folder of sections in seconds to a couple of minutes; brainglobe-atlasapi's `allen_mouse_25um` volume (~tens of MB) loads into a few hundred MB of RAM. No GPU. First run downloads DeepSlice weights and the BrainGlobe atlas (one-time, a few hundred MB total). The accuracy ceiling, not compute, is the constraint: DeepSlice reports a mean placement error on the order of a QuickNII-anchored human, but a single 2D section still inherits AP uncertainty from the plane prediction — so this is a screening tool. For a publication-grade boundary call, keep VisuAlign's human nonlinear correction in the loop or confirm marginal placements manually.

## Evidence

Proposed — no documented attempt at this exact three-component Claude Code assembly is known. The closest evidence is component-level and strong: DeepSlice is peer-reviewed and validated for batch coronal cutting-plane prediction, reporting alignment accuracy comparable to human QuickNII anchoring and explicitly designed for the non-orthogonal planes that defeat fixed-plate registration ([Carey et al., *Nat Commun* 2023](https://doi.org/10.1038/s41467-023-41645-4)); brainglobe-atlasapi is the peer-reviewed, field-standard programmatic interface to the Allen CCF annotation/structure hierarchy ([Claudi et al., *JOSS* 2020](https://doi.org/10.21105/joss.02668)). The QUINT chain this recipe scripts (DeepSlice/QuickNII → VisuAlign → Nutil) is the documented manual workflow for exactly this task ([Yates et al., *Front. Neuroinform.* 2019](https://doi.org/10.3389/fninf.2019.00075)); the recipe substitutes DeepSlice's automated plane prediction for the manual anchoring and reads the subregion programmatically, trading VisuAlign's human nonlinear correction for speed and re-runnability. Treat the human-confirmed overlays (step 3) and the distance-to-boundary margins as your confidence check until you validate against a hand-annotated subset.

## Alternatives considered

- **The full QUINT GUI workflow (DeepSlice/QuickNII + VisuAlign + Nutil).** The right call when you need a publication-grade boundary claim: VisuAlign's human nonlinear correction fixes tissue distortion this scripted screen does not, and Nutil quantifies labeled objects. Reach for it for the definitive placement figure; use this recipe to *triage* a cohort down to the sections that need that hand correction.
- **A naive affine warp onto a hand-picked coronal plate (e.g., via the [SimpleITK registration skill](../../catalog/tools/simpleitk-image-registration.html)).** Explicitly rejected: SimpleITK has no cutting-plane model and no Allen atlas, so warping an off-axis section onto a single hand-chosen plate is confidently wrong exactly where placement matters most (angled or oblique cuts). The plane prediction is the hard part and is why DeepSlice is load-bearing here.
- **`allenbrain-mcp` alone.** Read-only RMA/ontology/image queries (Alpha, no LICENSE); it cannot register a section or map a coordinate to a subregion, so it does not solve this problem.
- **An autonomous-science system.** None targets implant/probe localization; the problem is well-scoped and the escalation to rung 4 is unwarranted.

## See also

- [scikit-image (Claude Skill)](../../catalog/tools/scikit-image-processing.html) — the per-section fiber-tip detection component.
- [Sort spikes from a Neuropixels recording](sort-spikes-from-neuropixels-recording.html) — the electrophysiology counterpart to placement validation for probe experiments.
- [Register longitudinal medical scans](register-longitudinal-medical-scans.html) — the SimpleITK-based registration recipe, for the general 3D case this one deliberately does not use.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [Carey et al., "DeepSlice: rapid fully automatic registration of mouse brain imaging to a volumetric atlas," *Nat Commun* 2023](https://doi.org/10.1038/s41467-023-41645-4) — published 2023-09; verified 2026-07-27 (this run).
- [Claudi et al., "BrainGlobe Atlas API," *JOSS* 2020](https://doi.org/10.21105/joss.02668) — published 2020; verified 2026-07-27 (this run).
- [Yates et al., "QUINT: Workflow for Quantification and Spatial Analysis of Features in Histological Images," *Front. Neuroinform.* 2019](https://doi.org/10.3389/fninf.2019.00075) — published 2019; the manual workflow this recipe scripts.
- [DeepSlice on PyPI](https://pypi.org/project/DeepSlice/) — version 1.2.8, GPL-3.0-only; fetched 2026-07-27 (this run).
- [brainglobe-atlasapi on PyPI](https://pypi.org/project/brainglobe-atlasapi/) — version 2.3.1, BSD-3-Clause; fetched 2026-07-27 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=localize-implant-tip-in-brain-atlas-subregion&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Flocalize-implant-tip-in-brain-atlas-subregion.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
