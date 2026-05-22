---
title: BIDS (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-05-22
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

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install bids@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/bids ~/.claude/skills/
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

- [`scientific-skills/bids/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/bids/SKILL.md)
- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [BIDS specification](https://bids-specification.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=bids&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbids.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
