---
title: UK Biobank (Brain) Pipeline (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: NeuroClaw
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-11
summary: "Analyze already available UK Biobank data for brain-related research, including neurological outcomes, cognitive phenotypes, brain MRI derived phenotypes, survival analysis, subgroup analysis, propensity score …"
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier CUHK-AIM-Group/NeuroClaw, MIT, not archived, no OSV advisories"
---

# UK Biobank (Brain) Pipeline (Claude Skill)

Analyze already available UK Biobank data for brain-related research, including neurological outcomes, cognitive phenotypes, brain MRI derived phenotypes, survival analysis, subgroup analysis, propensity score analysis, mediation analysis, sensitivity analysis, machine learning, visualization, or manuscript-ready summaries.

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
  cp -r NeuroClaw/skills/ukb-skill ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd NeuroClaw && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools.

## What it does

Use this skill whenever the user wants to analyze already available UK Biobank data for brain-related research, including neurological outcomes, cognitive phenotypes, brain MRI derived phenotypes, survival analysis, subgroup analysis, propensity score analysis, mediation analysis, sensitivity analysis, machine learning, visualization, or manuscript-ready summaries. This skill only covers post-extraction analysis and explicitly excludes RAP access and data download guidance.

**Primary use cases**: Analyze already available UK Biobank data for brain-related research, including neurological outcomes, cognitive phenotypes, brain MRI derived phenotypes, survival analysis, subgroup analysis, propensity score analysis, mediation analysis, sensitivity analysis, machine learning, visualization, or manuscript-ready summaries.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the NeuroClaw skill library — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: MIT. The skill directory upstream is `skills/ukb-skill`.

## Sources

- [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw)
- [`skills/ukb-skill/SKILL.md`](https://github.com/CUHK-AIM-Group/NeuroClaw/blob/main/skills/ukb-skill/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=ukb-skill&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fukb-skill.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
