---
title: NovelSeek
parent: Systems
grand_parent: AI scientists
nav_order: 25
affiliation: Shanghai Artificial Intelligence Laboratory
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: General (12 AI-for-Science tasks)
availability: Open source
last_verified: 2026-05-20
---

# NovelSeek

Closed-loop multi-agent framework reporting time-bounded gains on 12 AI-for-Science tasks and a head-to-head idea-quality comparison against AI Scientist-v2.

| | |
|---|---|
| **Affiliation** | Shanghai Artificial Intelligence Laboratory ([NovelSeek Team](https://alpha-innovator.github.io/NovelSeek-project-page)) |
| **First introduced** | 2025-05 (arXiv:2505.16938) |
| **Lifecycle stages** | Multi-stage |
| **Autonomy level** | Semi-autonomous (closed-loop with optional human expert interaction) |
| **Domain focus** | General — reaction yield, transcription/enhancer prediction, molecular dynamics, time-series forecasting, power-flow estimation, semantic segmentation, etc. (12 AI-for-Science tasks) |
| **Availability** | Open source (code and baselines released) |

## Approach

Multi-agent framework spanning:

- **Survey agent** — literature search.
- **Code Review agent** — analyzes baseline repositories.
- **Idea Innovation agent** — proposes and self-evolves research ideas.
- **Planning & Execution agent** — turns ideas into experiments and handles errors.

Designed as an end-to-end loop from hypothesis to verification.

## Validation

Reports improvements on 12 AI-for-Science benchmark tasks against published baselines, e.g. reaction-yield prediction 27.6 → 35.4 in 12 hours; enhancer-activity prediction (DeepSTARR baseline) 0.52 → 0.79 in 4 hours; 2D semantic segmentation 78.8 → 81.0 in ~30 hours. Compared head-to-head with AI Scientist-v2 on 2D image classification and point-cloud autonomous-driving idea-generation tasks via 5 human reviewers averaging 20 ideas/task.

## Notable results

Time-bounded performance gains across 12 heterogeneous AI4Science tasks. Reported novelty preference over AI Scientist-v2 on the head-to-head idea-quality study.

## Primary paper

[NovelSeek Team, "NovelSeek: When Agent Becomes the Scientist — Building Closed-Loop System from Hypothesis to Verification," arXiv:2505.16938](https://arxiv.org/abs/2505.16938).

## Other references

- [Project page](https://alpha-innovator.github.io/NovelSeek-project-page)
- [HuggingFace](https://huggingface.co/U4R/NovelSeek)

## Code

[Repository](https://github.com/Alpha-Innovator/NovelSeek)
