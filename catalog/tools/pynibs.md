---
title: pyNIBS (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroForge
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-07-12
summary: "Analyze non-invasive brain stimulation (TMS/NIBS) experiments in pyNIBS — mesh/ROI I/O, coil-placement optimization, and MEP-to-E-field regression mapping."
---

# pyNIBS (Claude Skill)

Guides Claude through transcranial magnetic stimulation (TMS) and non-invasive brain stimulation analysis with pyNIBS — managing subject/session data, optimizing coil placement, and mapping motor-evoked potentials onto cortical electric fields.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [NeuroForge](https://github.com/HughYau/neuroforge-skills) (community OSS, MIT) |
| **Availability** | GA — part of the NeuroForge neuroscience skill set |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude writes and runs pyNIBS Python locally (Bash), not as an MCP tool |

## How to install

- **Claude Code** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/HughYau/neuroforge-skills
  cp -r neuroforge-skills/skills/pynibs ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. The skill invokes pyNIBS in your Python environment — install it first:
  ```
  pip install pynibs
  ```
  (pyNIBS processes electric-field simulation outputs; a SimNIBS install is expected for generating the underlying field data.)

## What it does

Covers the pyNIBS TMS/NIBS analysis workflow across six domains:

- **Subject & session I/O** — in-memory containers and persistence for MRI/mesh/ROI metadata.
- **Mesh & ROI structures** — geometric containers with structural metadata for cortical regions of interest.
- **HDF5 data layout** — file I/O that splits geometry from field data.
- **Optimization** — coil-placement and multichannel-current scoring.
- **Regression & localization** — nonlinear, element-wise MEP-to-E-field mapping.
- **Experiment import & QC** — CSV ingestion, trial filtering, and navigator-data cleanup.

**Primary use cases**: TMS coil-placement optimization, cortical localization from motor-evoked potentials, NIBS electric-field analysis.

## Notes

Distributed as a `SKILL.md` plus `references/*.md` in the NeuroForge skill set — Claude executes pyNIBS locally via Bash/Python rather than as an MCP server. Upstream skill front-matter `name` is `pynibs`; the skill directory upstream is `skills/pynibs`. Upstream license: MIT. The README documents context-injection usage for other agents, but the copy-into-`~/.claude/skills/` path above is the standard Claude Code Agent Skills install.

## Sources

- [`HughYau/neuroforge-skills`](https://github.com/HughYau/neuroforge-skills)
- [`skills/pynibs/SKILL.md`](https://github.com/HughYau/neuroforge-skills/blob/main/skills/pynibs/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pynibs&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpynibs.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
