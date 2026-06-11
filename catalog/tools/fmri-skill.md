---
title: fMRI Processing (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "Perform fMRI preprocessing, first-level analysis, ROI extraction, functional connectivity, effective connectivity, or atlas-based alignment to MNI152 space using either fMRIPrep, HCP-style pipelines, or CONN Toolbox"
---

# fMRI Processing (Claude Skill)

Perform fMRI preprocessing, first-level analysis, ROI extraction, functional connectivity, effective connectivity, or atlas-based alignment to MNI152 space using either fMRIPrep, HCP-style pipelines, or CONN Toolbox.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [CUHK-AIM-Group](https://github.com/CUHK-AIM-Group/NeuroClaw) (community OSS, MIT) |
| **Availability** | GA — part of the NeuroClaw neuroimaging skill library |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

- **Claude Code** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/CUHK-AIM-Group/NeuroClaw
  cp -r NeuroClaw/skills/fmri-skill ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants to perform fMRI preprocessing, first-level analysis, ROI extraction, functional connectivity, effective connectivity, or atlas-based alignment to MNI152 space using either fMRIPrep, HCP-style pipelines, or CONN Toolbox. Triggers include: 'fmri', 'fMRI analysis', 'functional connectivity', 'effective connectivity', 'ROI extraction', 'seed-based correlation', 'PPI', 'DCM', 'atlas alignment', 'MNI152', 'HCP pipeline', 'CONN toolbox', or any request involving BOLD data.

**Primary use cases**: 'fmri', 'fMRI analysis', 'functional connectivity', 'effective connectivity', 'ROI extraction', 'seed-based correlation', 'PPI', 'DCM', 'atlas alignment', 'MNI152', 'HCP pipeline', 'CONN toolbox', or any request involving BOLD data.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/fmri-skill`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/fmri-skill/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/fmri-skill/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=fmri-skill&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ffmri-skill.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
