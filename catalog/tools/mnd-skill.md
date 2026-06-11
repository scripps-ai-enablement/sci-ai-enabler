---
title: Motor Neuron Disease (MND) Pipeline (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "End-to-end workflow for the Motor Neuron Disease (MND) dataset from OpenNeuro ds005874, including BIDS validation, multimodal processing of rs-fMRI and task-fMRI, phenotype extraction, and …"
---

# Motor Neuron Disease (MND) Pipeline (Claude Skill)

End-to-end workflow for the Motor Neuron Disease (MND) dataset from OpenNeuro ds005874, including BIDS validation, multimodal processing of rs-fMRI and task-fMRI, phenotype extraction, and QC integration.

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
  cp -r NeuroClaw/skills/mnd-skill ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants an end-to-end workflow for the Motor Neuron Disease (MND) dataset from OpenNeuro ds005874, including BIDS validation, multimodal processing of rs-fMRI and task-fMRI, phenotype extraction, and QC integration. Triggers include: 'MND', 'Motor Neuron Disease', 'ALS', 'Amyotrophic Lateral Sclerosis', 'process MND data', 'MND fMRI', or any request to run the MND multimodal pipeline.

**Primary use cases**: 'MND', 'Motor Neuron Disease', 'ALS', 'Amyotrophic Lateral Sclerosis', 'process MND data', 'MND fMRI', or any request to run the MND multimodal pipeline.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/mnd-skill`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/mnd-skill/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/mnd-skill/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=mnd-skill&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmnd-skill.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
