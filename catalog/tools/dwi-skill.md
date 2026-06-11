---
title: Diffusion MRI (DWI) (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "Preprocess diffusion MRI / DWI data, compute diffusion metrics (FA/MD/AD/RD, etc.), extract ROI-wise diffusion features, or run tractography/connectome-related workflows"
---

# Diffusion MRI (DWI) (Claude Skill)

Preprocess diffusion MRI / DWI data, compute diffusion metrics (FA/MD/AD/RD, etc.), extract ROI-wise diffusion features, or run tractography/connectome-related workflows.

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
  cp -r NeuroClaw/skills/dwi-skill ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants to preprocess diffusion MRI / DWI data, compute diffusion metrics (FA/MD/AD/RD, etc.), extract ROI-wise diffusion features, or run tractography/connectome-related workflows. Triggers include: 'DWI', 'DTI', 'diffusion MRI', 'FA', 'MD', 'AD', 'RD', 'eddy', 'topup', 'QSIPrep', 'tractography', 'connectome', 'TBSS', 'white matter microstructure'. This is the NeuroClaw modality-layer interface: it plans WHAT to do and delegates execution to tool skills.

**Primary use cases**: 'DWI', 'DTI', 'diffusion MRI', 'FA', 'MD', 'AD', 'RD', 'eddy', 'topup', 'QSIPrep', 'tractography', 'connectome', 'TBSS', 'white matter microstructure'.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/dwi-skill`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/dwi-skill/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/dwi-skill/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=dwi-skill&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdwi-skill.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
