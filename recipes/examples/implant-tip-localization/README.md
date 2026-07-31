---
title: 'Reproducible example: implant-tip localization'
parent: All recipes
grand_parent: Recipes
nav_exclude: true
permalink: /recipes/examples/implant-tip-localization/
---

# Implant-tip localization — reference artifact

The durable artifact for [Localize a fiber/probe implant tip in an Allen CCF
subregion from 2D histology](../../items/localize-implant-tip-in-brain-atlas-subregion.md).

## Run the deterministic replay

```
python localize_tips.py --offline --target TGT --outdir results/demo
```

Standard library only. No network, no atlas download, no TensorFlow. Prints:

```
  section 1 (25,40) -> TGT margin=50.00um : hit
  section 1 (75,40) -> NBR margin=75.00um : miss
  section 1 (48,40) -> TGT margin=4.00um  : marginal
```

## Why the fixture exists

The step that quietly goes wrong in this workflow is mapping a section pixel into
atlas space. QuickNII/DeepSlice anchoring is a 9-vector
`[ox,oy,oz, ux,uy,uz, vx,vy,vz]`, and the transform is

```
atlas_coord = O + (x / width) * U + (y / height) * V
```

divided by `width`/`height` — **not** `width-1`. Get it wrong and you get
coordinates that look reasonable and are wrong, with no error raised. So
`fixtures/` carries a synthetic 8×8×8 atlas whose answer is checkable by hand:
structure `TGT` where `ap < 4`, `NBR` where `ap >= 4`, 25 µm voxels, and an
alignment where `ap = 8 * x / 100`. The third tip sits at `x=48` → `ap = 3.84`,
i.e. 0.16 voxels × 25 µm = **4 µm** from the boundary, which is inside the
plane-prediction AP error and therefore reported `marginal` rather than a clean
hit. That case is the point of the fixture.

The formula matches the canonical implementation in PyNutil
(`transform_to_atlas_space`, `PyNutil/processing/atlas_map.py`).

## The live run

```
pip install -r requirements.txt
python localize_tips.py --alignment out/alignment.json \
    --atlas allen_mouse_25um --tips tips.csv --target CA1 --outdir results/run
```

Read `requirements.txt` before you start: **Python 3.11–3.13 only**, and DeepSlice
is GPL-3.0-only.

In live mode prefer PyNutil's own `read_alignment` + `xy_to_coords` over the
formula reproduced here — it handles multi-section series, VisuAlign non-linear
deformation, and orientation conversion. The formula is inlined in this script
only so the offline replay needs no third-party package.

## Files

| Path | What |
|---|---|
| `localize_tips.py` | the analysis; `--offline` replays the fixture |
| `tips.csv` | input tip pixels (hit / miss / marginal) |
| `fixtures/mini_atlas.json` | synthetic 8×8×8 atlas, hand-checkable |
| `fixtures/alignment.json` | QuickNII-format alignment, one section |
| `requirements.txt` | pinned live environment + the Python-version constraint |

Outputs `placements.csv` and `provenance.json` (input/output hashes, atlas
orientation and resolution, the transform and its reference, the AP-error
threshold). No wall-clock value reaches the outputs — pass `--run-date` to record
a date explicitly — so reruns are byte-identical.
