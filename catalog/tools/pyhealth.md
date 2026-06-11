---
title: PyHealth (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-06-04
summary: Build clinical/healthcare deep-learning pipelines with PyHealth — loading EHR/signal/imaging datasets (MIMIC-III/IV, eICU, OMOP, SleepEDF, ChestXray14, EHRShot), defining tasks (mortality, readmission, length-of-stay, drug recommendation, sleep …
---

# PyHealth (Claude Skill)

Build clinical/healthcare deep-learning pipelines with PyHealth — loading EHR/signal/imaging datasets (MIMIC-III/IV, eICU, OMOP, SleepEDF, ChestXray14, EHRShot), defining tasks (mortality, readmission, length-of-stay, drug recommendation, sleep staging, ICD coding, EEG events), instantiating models (Transformer, RETAIN, GAMENet, SafeDrug, MICRON, StageNet, AdaCare, CNN/RNN/MLP), training with the PyHealth Trainer, computing clinical metrics, and using medical code utilities (ICD/ATC/NDC/RxNorm lookup and cross-mapping).

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | Free / OSS — license not stated upstream |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/scientific-computing/pyhealth` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `pyhealth` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/pyhealth ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use.

## What it does

Build clinical/healthcare deep-learning pipelines with PyHealth — loading EHR/signal/imaging datasets (MIMIC-III/IV, eICU, OMOP, SleepEDF, ChestXray14, EHRShot), defining tasks (mortality, readmission, length-of-stay, drug recommendation, sleep staging, ICD coding, EEG events), instantiating models (Transformer, RETAIN, GAMENet, SafeDrug, MICRON, StageNet, AdaCare, CNN/RNN/MLP), training with the PyHealth Trainer, computing clinical metrics, and using medical code utilities (ICD/ATC/NDC/RxNorm lookup and cross-mapping). Use this skill whenever the user mentions PyHealth, MIMIC, eICU, OMOP, EHR modeling, clinical prediction, drug recommendation, sleep staging, medical code mapping, ICD/ATC codes, or any healthcare ML pipeline that fits the dataset → task → model → trainer → metrics pattern, even if "PyHealth" isn't named explicitly.

**Primary use cases**: Build clinical/healthcare deep-learning pipelines with PyHealth — loading EHR/signal/imaging datasets (MIMIC-III/IV, eICU, OMOP, SleepEDF, ChestXray14, EHRShot), defining tasks (mortality, readmission, length-of-stay, drug recommendation, sleep staging, ICD coding, EEG events), instantiating models (Transformer, RETAIN, GAMENet, SafeDrug, MICRON, StageNet, AdaCare, CNN/RNN/MLP), training with the PyHealth Trainer, computing clinical metrics, and using medical code utilities (ICD/ATC/NDC/RxNorm lookup and cross-mapping).

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: not stated upstream. The skill name to enable after install is `pyhealth`.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`skills/pyhealth/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/pyhealth/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pyhealth&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpyhealth.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
