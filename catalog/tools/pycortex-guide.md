---
title: Pycortex Guide (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Awesome Cognitive and Neuroscience Skills
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-08-09
summary: "Render fMRI data on cortical surfaces with pycortex — 2D flatmaps, interactive 3D WebGL viewers, volume-to-surface mapping and ROI management"
---

# Pycortex Guide (Claude Skill)

Guides Claude through cortical surface visualization of fMRI data with pycortex — importing FreeSurfer or fMRIPrep anatomy into the cortex database, wrapping volumes into surface-mappable objects, and producing flatmaps or interactive WebGL brain viewers.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Awesome Cognitive and Neuroscience Skills](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills) (community OSS, MIT) |
| **Availability** | GA — one of ~40 research skills in the collection |
| **Pricing** | Free / OSS (MIT) — pycortex itself is BSD-2-Clause |
| **Capabilities** | Read/Write — methodology guidance; Claude writes and runs the visualization code locally |

## How to install

- **Claude Code** — plugin marketplace (installs all skills in the collection):
  ```
  /plugin marketplace add HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  /plugin install awesome-cognitive-and-neuroscience-skills@awesome-cognitive-and-neuroscience-skills
  ```
  Restart Claude Code afterwards. The skills are description-activated — there is no slash command; ask about flatmaps or surface rendering and Claude loads the skill.
- **Claude Code** — single-skill alternative:
  ```
  git clone https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  cp -r awesome_cognitive_and_neuroscience_skills/skills/pycortex-guide ~/.claude/skills/
  ```
  (Project-scoped alternative: copy into `.claude/skills/` instead. The repo's default branch is `master`, not `main`. Unlike most skills in this collection, this one declares no `research-literacy` dependency.)
- **Underlying software** — install pycortex itself. Build prerequisites must go in first:
  ```
  pip install -U setuptools wheel numpy cython
  pip install -U pycortex
  pip install -U 'pycortex[headless]'   # only if rendering without a display
  ```
  Python 3.10+, **Linux or macOS only** — there is no Windows path. Pulls numpy, scipy, matplotlib, nibabel, h5py, tornado, shapely and lxml.

## What it does

Walks a four-stage workflow:

1. **Import anatomy** — bring a FreeSurfer or fMRIPrep subject into the pycortex database, with a transform (`xfmname`) relating functional volumes to that surface.
2. **Construct data objects** — wrap arrays as `Volume` (voxel space, needs a transform) or `Vertex` (already on the surface), with `cmap`, `vmin`, `vmax` and `subject` metadata; combine into a `Dataset`.
3. **Render** — 2D cortical flatmaps or a 3D interactive WebGL viewer, with `with_curvature` and `with_rois` overlays.
4. **Analyze surface geometry** — curvature, ROI boundaries, geodesic distance.

**Rules the skill enforces**: the data array's shape must match the transform's dimensions; the subject and transform must already exist in the database before you reference them; set `vmin`/`vmax` explicitly whenever you compare across subjects, since autoscaling silently changes the colour mapping; and save with `pack=True` if the dataset needs to be portable to another machine.

**Primary use cases**: retinotopy and encoding-model result figures, publication-quality cortical flatmaps, sharing an interactive brain viewer alongside a paper.

## Notes

**AI-generated content — verify before use.** All skills in this collection carry `review_status: ai-generated`, and the README states the content "has not been individually verified by human domain experts." This skill's front-matter lists no cited papers and pins no pycortex version — check its API guidance against the [pycortex documentation](https://gallantlab.org/pycortex/) before relying on it.

**Two platform limitations to know before you commit**: pycortex does not support Windows, and the WebGL viewer blocks execution when called from a plain script — run it from IPython/Jupyter, or pass `autoclose`, if the call sits inside a batch pipeline.

Related catalogued tools: [FreeSurfer](freesurfer-tool.html) and [fMRIPrep](fmriprep-tool.html) produce the surfaces this skill consumes; [Nilearn](nilearn-tool.html) covers the volumetric plotting case; [NetNeuroTools Guide](netneurotools-guide.html) has its own surface-plotting layer for parcellated network results.

## Sources

- [`HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills)
- [`skills/pycortex-guide/SKILL.md`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/pycortex-guide/SKILL.md)
- [pycortex documentation](https://gallantlab.org/pycortex/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pycortex-guide&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpycortex-guide.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
