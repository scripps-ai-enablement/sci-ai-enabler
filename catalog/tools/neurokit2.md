---
title: NeuroKit2 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Neuroscience, Translational Medicine]
last_verified: 2026-05-22
summary: Claude skill for biosignal processing — ECG, EEG, EDA, RSP, PPG, EMG, and EOG analysis including HRV, event-related responses, and multi-modal physiological insights.
---

# NeuroKit2 (Claude Skill)

Claude skill wrapping the NeuroKit2 biosignal processing toolkit — analysis pipelines for cardiovascular, neural, electrodermal, respiratory, muscle, and eye-movement signals.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (wraps the MIT-licensed NeuroKit2 library) |
| **Availability** | GA — distributed with the K-Dense marketplace at v2.27.0 |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write — local computation on user-supplied physiological recordings |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install neurokit2@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/neurokit2 ~/.claude/skills/
  pip install neurokit2
  ```

## What it does

- ECG: R-peak detection, HRV (time / frequency / non-linear domain)
- EEG: bandpower, microstates, complexity measures
- EDA: skin-conductance response decomposition
- RSP: respiration rate, RSA
- PPG, EMG, EOG processing
- Multi-modal event-related analysis (`nk.events_find`, `nk.epochs_create`, `nk.events_plot`)
- Signal cleaning helpers usable upstream of fMRI connectivity analyses

**Primary use cases**: HRV studies, EEG feature extraction, biosignal QC, multi-modal psychophysiology, resting-state fMRI nuisance regression.

## Notes

Pure Python; pairs with the BIDS skill for organizing the raw signals beforehand. Cite Makowski et al. 2021 (Behavior Research Methods) when publishing.

## Sources

- [`scientific-skills/neurokit2/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/neurokit2/SKILL.md)
- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [NeuroKit2 docs](https://neuropsychology.github.io/NeuroKit/)

---

## Installed this tool?

[Share feedback](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=neurokit2&details=Filed+from+https%3A%2F%2Fgoodb.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fneurokit2.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
