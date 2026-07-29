---
title: WMH Segmentation (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
verification: works
verified_on: 2026-07-29
verification_note: "repo CUHK-AIM-Group/NeuroClaw resolves (MIT, pushed 2026-07-26, 76 stars) and the skills/wmh-segmentation dir install path is current; local nnU-Net orchestration, no network"
security: cleared
security_on: 2026-07-29
security_note: "provenance matches CUHK-AIM-Group/NeuroClaw, MIT skill code, no OSV/GitHub advisories, read-only local orchestration"
summary: "Perform automated white matter hyperintensity (WMH) segmentation on structural MRI data using the MARS-WMH nnU-Net model."
---

# WMH Segmentation (Claude Skill)

Perform automated white matter hyperintensity (WMH) segmentation on structural MRI data using the MARS-WMH nnU-Net model.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [CUHK-AIM-Group](https://github.com/CUHK-AIM-Group/NeuroClaw) (community OSS, MIT) |
| **Availability** | GA — part of the NeuroClaw neuroimaging skill library |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-29 |
| **Security** | cleared · 2026-07-29 — provenance matches CUHK-AIM-Group/NeuroClaw, MIT skill code, no advisories, read-only local orchestration |

## How to install

- **Claude Code** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/CUHK-AIM-Group/NeuroClaw
  cp -r NeuroClaw/skills/wmh-segmentation ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants to perform automated white matter hyperintensity (WMH) segmentation on structural MRI data using the MARS-WMH nnU-Net model. Requires one FLAIR and one T1w NIfTI image (no contrast). Triggers include: 'wmh', 'white matter hyperintensities', 'WMH segmentation', 'MARS-WMH', 'wmh-nnunet', 'segment FLAIR T1', 'white matter lesions', 'vascular WMH', 'mars wmh', or any request to run nnU-Net WMH segmentation on FLAIR+T1w pair.

**Primary use cases**: 'wmh', 'white matter hyperintensities', 'WMH segmentation', 'MARS-WMH', 'wmh-nnunet', 'segment FLAIR T1', 'white matter lesions', 'vascular WMH', 'mars wmh', or any request to run nnU-Net WMH segmentation on FLAIR+T1w pair.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/wmh-segmentation`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/wmh-segmentation/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/wmh-segmentation/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=wmh-segmentation&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fwmh-segmentation.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
