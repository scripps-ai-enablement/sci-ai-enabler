---
title: SEED-VIG (EEG Vigilance) Pipeline (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "End-to-end workflow for the SEED-VIG (SJTU Emotion EEG Dataset - Vigilance) dataset, including EEG validation, preprocessing, feature extraction, and vigilance/fatigue detection"
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier CUHK-AIM-Group/NeuroClaw, MIT, not archived, no OSV advisories"
---

# SEED-VIG (EEG Vigilance) Pipeline (Claude Skill)

End-to-end workflow for the SEED-VIG (SJTU Emotion EEG Dataset - Vigilance) dataset, including EEG validation, preprocessing, feature extraction, and vigilance/fatigue detection.

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
  cp -r NeuroClaw/skills/seed-vig-skill ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants an end-to-end workflow for the SEED-VIG (SJTU Emotion EEG Dataset - Vigilance) dataset, including EEG validation, preprocessing, feature extraction, and vigilance/fatigue detection. Triggers include: 'SEED-VIG', 'SEEDVIG', 'vigilance EEG', 'fatigue detection', 'drowsiness EEG', 'process SEED-VIG', or any request to run the SEED-VIG pipeline.

**Primary use cases**: 'SEED-VIG', 'SEEDVIG', 'vigilance EEG', 'fatigue detection', 'drowsiness EEG', 'process SEED-VIG', or any request to run the SEED-VIG pipeline.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/seed-vig-skill`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/seed-vig-skill/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/seed-vig-skill/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=seed-vig-skill&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fseed-vig-skill.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
