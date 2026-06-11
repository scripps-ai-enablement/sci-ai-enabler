---
title: NiBabel (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "NeuroClaw needs concrete nibabel operations for neuroimaging files: loading and validating NIfTI images, inspecting shapes and affine matrices, saving derived images, converting voxel coordinates …"
---

# NiBabel (Claude Skill)

NeuroClaw needs concrete nibabel operations for neuroimaging files: loading and validating NIfTI images, inspecting shapes and affine matrices, saving derived images, converting voxel coordinates to MNI/world coordinates, or reading FreeSurfer geometry and annotation files.

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
  cp -r NeuroClaw/skills/nibabel-skill ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever NeuroClaw needs concrete nibabel operations for neuroimaging files: loading and validating NIfTI images, inspecting shapes and affine matrices, saving derived images, converting voxel coordinates to MNI/world coordinates, or reading FreeSurfer geometry and annotation files. Triggers include: 'nibabel', 'inspect NIfTI', 'read affine', 'save nifti', 'voxel to MNI', 'atlas coordinates', 'read FreeSurfer surface', 'read annot', or any request focused on low-level neuroimaging I/O rather than full preprocessing.

**Primary use cases**: 'nibabel', 'inspect NIfTI', 'read affine', 'save nifti', 'voxel to MNI', 'atlas coordinates', 'read FreeSurfer surface', 'read annot', or any request focused on low-level neuroimaging I/O rather than full preprocessing.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/nibabel-skill`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/nibabel-skill/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/nibabel-skill/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=nibabel-skill&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fnibabel-skill.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
