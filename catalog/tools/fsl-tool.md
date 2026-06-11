---
title: FSL (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "Process neuroimaging data with FSL (FMRIB Software Library), covering structural MRI, functional MRI (fMRI), and diffusion MRI (dMRI/DTI)"
---

# FSL (Claude Skill)

Process neuroimaging data with FSL (FMRIB Software Library), covering structural MRI, functional MRI (fMRI), and diffusion MRI (dMRI/DTI).

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
  cp -r NeuroClaw/skills/fsl-tool ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants to process neuroimaging data with FSL (FMRIB Software Library), covering structural MRI, functional MRI (fMRI), and diffusion MRI (dMRI/DTI). Triggers include: 'use FSL', 'FSL processing', 'fsl_anat', 'FEAT', 'MELODIC', 'eddy', 'bedpostx', 'probtrackx', 'BET', 'FAST', 'FLIRT', 'FNIRT', 'run FSL pipeline'. This skill is the NeuroClaw interface-layer wrapper for FSL: checks installation, generates execution plan with concrete shell commands, waits for explicit confirmation, then routes all commands through claw-shell.

**Primary use cases**: 'use FSL', 'FSL processing', 'fsl_anat', 'FEAT', 'MELODIC', 'eddy', 'bedpostx', 'probtrackx', 'BET', 'FAST', 'FLIRT', 'FNIRT', 'run FSL pipeline'.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/fsl-tool`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/fsl-tool/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/fsl-tool/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=fsl-tool&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ffsl-tool.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
