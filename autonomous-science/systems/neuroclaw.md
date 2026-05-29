---
title: NeuroClaw
parent: Systems
grand_parent: AI scientists
nav_order: 29
affiliation: CUHK / Northwest University / Lehigh / MGH / Harvard Kempner Institute
lifecycle_stages: [Experiment design, Analysis]
autonomy: Semi-autonomous
domain: Biology (neuroimaging)
availability: Open source
last_verified: 2026-05-27
---

# NeuroClaw

Domain-specialized multi-agent research assistant for executable and reproducible neuroimaging research, operating directly on raw sMRI/fMRI/dMRI/EEG data with environment management and a three-tier skill hierarchy.

| | |
|---|---|
| **Affiliation** | The Chinese University of Hong Kong / Northwest University / Lehigh / Massachusetts General Hospital / Kempner Institute, Harvard ([project page](https://cuhk-aim-group.github.io/NeuroClaw/)) |
| **First introduced** | 2026-04 (arXiv:2604.24696) |
| **Lifecycle stages** | Experiment design, Analysis |
| **Autonomy level** | Semi-autonomous |
| **Domain focus** | Biology — neuroimaging (sMRI, fMRI, dMRI, EEG) |
| **Availability** | Open source |

## Approach

NeuroClaw organizes capabilities into a three-layer skill hierarchy: a **base layer** of atomic operations (DICOM-to-NIfTI conversion, metadata validation, single-command execution); a **subagent layer** of tool skills wrapping FSL, FreeSurfer, fMRIPrep, modality skills for fMRI/sMRI/dMRI/EEG, model skills for phenotype prediction and statistical analysis, and dataset skills for ADNI, HCP Young Adult, and UK Biobank; and an **interface layer** that interprets intent, routes to subagents, and maintains workflow continuity. Skill dependencies are a DAG, so multi-step plans are composed by traversal rather than re-interpreting a monolithic prompt.

The system works directly from raw multimodal neuroimaging data, conditioning planning on data organization, BIDS compliance, available modalities, and metadata. A reproducibility harness layers checkpointed execution, environment manifests, pinned Python / Docker environments, automated installers for neuroimaging toolchains, structured JSONL audit logs, expected-artifact / missing-file / NaN-Inf checks, and checksum-based artifact validation. Together these support a closed loop in which the agent proposes analysis actions from dataset semantics, executes tool-grounded steps, verifies artifacts and metrics, and revises subsequent actions.

## Validation

Evaluated on **NeuroBench**, a system-level benchmark of 100 hand-curated neuroimaging tasks (T001–T100) spanning sMRI, fMRI, dMRI, EEG across ADNI and HCP Young Adult, organized into basic utilities, core pipelines, advanced analysis, and multimodal integration. Each task has a specification with expected output artifacts and checkpoints. A fixed GPT-5.4 judge scores planning completeness (P), tool/skill usage reasonableness (R), and command/code correctness (C); aggregate score is `0.30 P + 0.40 R + 0.30 C`. Ten frontier multimodal LLMs were run with and without NeuroClaw skills.

## Notable results

- All ten base models improved when run inside NeuroClaw (average absolute gain **+4.74 points** on the 0–100 scale).
- **Claude-Opus-4.6** reached the top NeuroClaw score of **72.10%** (no-skills 69.12%); **Claude-Sonnet-4.6** 70.39% (+5.02); **GPT-5.4** 67.69% (+3.12).
- Largest absolute gains on weaker base models: **MiniMax-M2.7 +12.97** (normalized gain g = 0.1998) and **Qwen3-plus +7.73** (g = 0.1558).

## Primary paper

[Wang, He, Peng et al., "NeuroClaw Technical Report: Closed-Loop Agentic AI for Executable and Reproducible Neuroimaging Research," arXiv:2604.24696](https://arxiv.org/abs/2604.24696).

## Other references

- [Project page](https://cuhk-aim-group.github.io/NeuroClaw/index.html)

## Code

[Project homepage](https://cuhk-aim-group.github.io/NeuroClaw/index.html) — release status per project page.
