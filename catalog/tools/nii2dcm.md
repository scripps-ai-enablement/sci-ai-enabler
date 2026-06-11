---
title: nii2dcm (NIfTI → DICOM) (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "Convert NIfTI files (.nii or .nii.gz) to DICOM format, create DICOM series from processed neuroimaging results, write segmentation/registration/analysis outputs back to DICOM for PACS …"
---

# nii2dcm (NIfTI → DICOM) (Claude Skill)

Convert NIfTI files (.nii or .nii.gz) to DICOM format, create DICOM series from processed neuroimaging results, write segmentation/registration/analysis outputs back to DICOM for PACS compatibility or clinical viewer comparison, or transfer metadata from reference DICOM files.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [CUHK-AIM-Group](https://github.com/CUHK-AIM-Group/NeuroClaw) (community OSS, MIT) |
| **Availability** | GA — part of the NeuroClaw neuroimaging skill library |
| **Pricing** | Free / OSS (BSD 3-Clause (original nii2dcm). See https://github.com/tomaroberts/nii2dcm/blob/main/LICENSE for complete terms) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

- **Claude Code** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/CUHK-AIM-Group/NeuroClaw
  cp -r NeuroClaw/skills/nii2dcm ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants to convert NIfTI files (.nii or .nii.gz) to DICOM format, create DICOM series from processed neuroimaging results, write segmentation/registration/analysis outputs back to DICOM for PACS compatibility or clinical viewer comparison, or transfer metadata from reference DICOM files. Triggers include: mentions of 'NIfTI to DICOM', 'nii to dcm', 'convert nii.gz to DICOM', 'dicomify segmentation', 'nii2dcm', 'bring results back to DICOM', 'create DICOM from NIfTI', 'nii to dicom series', or any request to take post-processed neuroimaging results (segmentation, registration, bias field correction, synthesis, etc.) and store/view them alongside original patient DICOM data. Also use when modality-specific metadata (especially MR, SVR) or preservation of patient/study information from a reference DICOM is needed. Do NOT use for the reverse conversion (DICOM to NIfTI), non-medical imaging file conversions, or any clinical diagnostic or treatment-related workflows.

**Primary use cases**: mentions of 'NIfTI to DICOM', 'nii to dcm', 'convert nii.gz to DICOM', 'dicomify segmentation', 'nii2dcm', 'bring results back to DICOM', 'create DICOM from NIfTI', 'nii to dicom series', or any request to take post-processed neuroimaging results (segmentation, registration, bias field correction, synthesis, etc.) and store/view them alongside original patient DICOM data.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: BSD 3-Clause (original nii2dcm). See https://github.com/tomaroberts/nii2dcm/blob/main/LICENSE for complete terms. The skill directory upstream is `skills/nii2dcm`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/nii2dcm/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/nii2dcm/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=nii2dcm&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fnii2dcm.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
