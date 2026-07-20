---
title: NeuroKit2 (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Neuroscience, Translational Medicine]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-20
verification_note: "repo and skills/neurokit2 dir resolve on K-Dense-AI/scientific-agent-skills; smoke clone failed on sandbox missing git (environmental, not tool)"
security: cleared
security_on: 2026-07-20
security_note: "provenance matches supplier K-Dense-AI, MIT repo wrapping MIT NeuroKit2, maintained (pushed 2026-07-15), no OSV advisories"
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
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches K-Dense-AI, MIT repo, maintained, no OSV advisories |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/scientific-computing/neurokit2` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `neurokit2` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/neurokit2 ~/.claude/skills/
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

- [`skills/neurokit2/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/neurokit2/SKILL.md)
- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [NeuroKit2 docs](https://neuropsychology.github.io/NeuroKit/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=neurokit2&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fneurokit2.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
