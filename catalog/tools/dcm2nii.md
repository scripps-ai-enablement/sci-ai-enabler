---
title: dcm2niix (DICOM → NIfTI) (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "Convert DICOM files or folders to NIfTI format (.nii or .nii.gz), extract neuroimaging volumes from clinical DICOM series (MRI, CT, PET, etc.), prepare raw …"
---

# dcm2niix (DICOM → NIfTI) (Claude Skill)

Convert DICOM files or folders to NIfTI format (.nii or .nii.gz), extract neuroimaging volumes from clinical DICOM series (MRI, CT, PET, etc.), prepare raw DICOM data for research processing pipelines, anonymize while converting, or batch-convert multiple series/studies.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [CUHK-AIM-Group](https://github.com/CUHK-AIM-Group/NeuroClaw) (community OSS, MIT) |
| **Availability** | GA — part of the NeuroClaw neuroimaging skill library |
| **Pricing** | Free / OSS (BSD 3-Clause (original dcm2niix). See https://github.com/rordenlab/dcm2niix/blob/master/LICENSE for complete terms) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

- **Claude Code** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/CUHK-AIM-Group/NeuroClaw
  cp -r NeuroClaw/skills/dcm2nii ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants to convert DICOM files or folders to NIfTI format (.nii or .nii.gz), extract neuroimaging volumes from clinical DICOM series (MRI, CT, PET, etc.), prepare raw DICOM data for research processing pipelines, anonymize while converting, or batch-convert multiple series/studies. Triggers include: 'DICOM to NIfTI', 'dcm to nii', 'convert dicom to nii.gz', 'dcm2niix', 'extract nii from dicom', 'batch dicom to nifti', 'prepare dicom for freesurfer/fsl/spm', 'anonymized nifti conversion', or any request to transform clinical DICOM data into analysis-ready NIfTI format while preserving orientation, voxel spacing, slice timing (when available), and important metadata in the JSON sidecar.

**Primary use cases**: 'DICOM to NIfTI', 'dcm to nii', 'convert dicom to nii.gz', 'dcm2niix', 'extract nii from dicom', 'batch dicom to nifti', 'prepare dicom for freesurfer/fsl/spm', 'anonymized nifti conversion', or any request to transform clinical DICOM data into analysis-ready NIfTI format while preserving orientation, voxel spacing, slice timing (when available), and important metadata in the JSON sidecar.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: BSD 3-Clause (original dcm2niix). See https://github.com/rordenlab/dcm2niix/blob/master/LICENSE for complete terms. The skill directory upstream is `skills/dcm2nii`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/dcm2nii/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/dcm2nii/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=dcm2nii&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdcm2nii.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
