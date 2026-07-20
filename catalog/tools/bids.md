---
title: BIDS (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-20
verification_note: "repo and skills/bids dir resolve on K-Dense-AI/scientific-agent-skills"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT collection, maintained (pushed 2026-07-15), no OSV advisories"
summary: Claude skill for organizing, validating, and querying Brain Imaging Data Structure datasets — MRI, EEG, MEG, iEEG, PET, microscopy, behavioral, and 35 BIDS entities.
---

# BIDS (Claude Skill)

Claude skill for the Brain Imaging Data Structure standard — dataset creation, validation, DICOM conversion, PyBIDS queries, and BIDS-Apps preparation across all 11 BIDS modalities.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — distributed with the K-Dense marketplace at v2.27.0 |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write — converts and reorganizes local neuroimaging data into BIDS layout |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches K-Dense-AI, MIT collection, maintained, no OSV advisories |

## How to install

<!-- alt-install:neuroclaw -->
- **Also packaged in the NeuroClaw skill library** ([CUHK-AIM-Group](https://github.com/CUHK-AIM-Group/NeuroClaw) (community OSS, MIT)): clone [`CUHK-AIM-Group/NeuroClaw`](https://github.com/CUHK-AIM-Group/NeuroClaw) and copy `skills/bids-organizer` into `~/.claude/skills/`.
<!-- /alt-install:neuroclaw -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `bids` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/bids ~/.claude/skills/
  ```

## What it does

- DICOM-to-BIDS conversion via HeuDiConv (ReproIn turnkey, map-into-reproin, custom heuristics), dcm2bids (config-file-based), and BIDScoin (GUI-based)
- PyBIDS `BIDSLayout` queries against organized datasets
- Sidecar / `participants.tsv` / `scans.tsv` / `events.tsv` authoring with metadata inheritance
- BIDS validation before repository submission (OpenNeuro, DANDI)
- BIDS-Apps invocation patterns (fMRIPrep, MRIQC, QSIPrep)
- Reference for the full 35-entity BIDS schema and the `beps.yml` extension proposals (including Neuropixels)

**Primary use cases**: Organize raw neuroscience data for sharing, validate BIDS compliance before submission, prepare datasets for BIDS-Apps preprocessing pipelines, query large BIDS cohorts programmatically.

## Notes

Covers the 11 current BIDS modalities — MRI (structural / functional / diffusion / perfusion), PET, microscopy, EEG, MEG, iEEG, EMG, NIRS, motion capture, behavioral, and MR spectroscopy. Pairs naturally with the Neuropixels-Analysis skill once the microelectrode-electrophysiology BEP lands.

## Sources

- [`skills/bids/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/bids/SKILL.md)
- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [BIDS specification](https://bids-specification.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=bids&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbids.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
