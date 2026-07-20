---
title: HCP Pipelines (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "Perform high-quality, HCP-style preprocessing of multimodal MRI data (structural, functional, diffusion) using the official HCP Pipelines"
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier CUHK-AIM-Group/NeuroClaw, MIT, not archived, no OSV advisories"
---

# HCP Pipelines (Claude Skill)

Perform high-quality, HCP-style preprocessing of multimodal MRI data (structural, functional, diffusion) using the official HCP Pipelines.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [CUHK-AIM-Group](https://github.com/CUHK-AIM-Group/NeuroClaw) (community OSS, MIT) |
| **Availability** | GA — part of the NeuroClaw neuroimaging skill library |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches supplier CUHK-AIM-Group/NeuroClaw, MIT, no OSV advisories |

## How to install

- **Claude Code** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/CUHK-AIM-Group/NeuroClaw
  cp -r NeuroClaw/skills/hcppipeline-tool ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants to perform high-quality, HCP-style preprocessing of multimodal MRI data (structural, functional, diffusion) using the official HCP Pipelines. Triggers include: 'HCP pipeline', 'HCP preprocessing', 'hcp-fmri', 'hcp-dwi', 'hcp-structural', 'MSMAll', 'ICA-FIX', 'bedpostx', 'probtrackx', or any request to run the Human Connectome Project preprocessing pipelines.

**Primary use cases**: 'HCP pipeline', 'HCP preprocessing', 'hcp-fmri', 'hcp-dwi', 'hcp-structural', 'MSMAll', 'ICA-FIX', 'bedpostx', 'probtrackx', or any request to run the Human Connectome Project preprocessing pipelines.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/hcppipeline-tool`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/hcppipeline-tool/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/hcppipeline-tool/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=hcppipeline-tool&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fhcppipeline-tool.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
