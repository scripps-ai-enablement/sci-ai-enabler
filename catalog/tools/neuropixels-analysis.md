---
title: Neuropixels-Analysis (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-05-22
summary: Claude skill for end-to-end Neuropixels analysis — SpikeGLX/Open Ephys/NWB loading, preprocessing, motion correction, and Kilosort4/SpykingCircus2/Mountainsort5 spike sorting.
---

# Neuropixels-Analysis (Claude Skill)

Claude skill for high-density extracellular electrophysiology pipelines on Neuropixels probes, following SpikeInterface, Allen Institute, and International Brain Laboratory best practices.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — distributed with the K-Dense marketplace at v2.27.0 |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write — local computation on user-supplied recordings; GPU recommended for Kilosort4 |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install neuropixels-analysis@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/neuropixels-analysis ~/.claude/skills/
  ```

## What it does

- Loads recordings from SpikeGLX, Open Ephys, and NWB
- Preprocessing: highpass filtering, Neuropixels 1.0 phase-shift correction, bad-channel detection, common-average referencing
- Motion / drift estimation and correction (`kilosort_like` and `nonrigid_accurate` presets)
- Spike sorting integration: Kilosort4 (GPU), SpykingCircus2, Mountainsort5 (CPU)
- AI-assisted curation toward publication-ready single units

**Primary use cases**: Raw-to-curated-units pipelines on Neuropixels recordings, drift-corrected sorting on long sessions, cross-sorter comparison via SpikeInterface.

## Notes

Kilosort4 needs a CUDA-capable GPU; SpykingCircus2 and Mountainsort5 fall back to CPU. The skill assumes SpikeInterface installed in the environment.

## Sources

- [`scientific-skills/neuropixels-analysis/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/neuropixels-analysis/SKILL.md)
- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [SpikeInterface docs](https://spikeinterface.readthedocs.io/)
