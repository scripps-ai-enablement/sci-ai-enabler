---
title: EvoScientist
parent: Systems
grand_parent: AI scientists
nav_order: 17
affiliation: Huawei Technologies (with Vrije Universiteit Amsterdam)
lifecycle_stages: [Multi-stage]
autonomy: Fully autonomous
domain: General (evaluated on AI/ML research tasks)
availability: Open source (announced)
last_verified: 2026-05-22
---

# EvoScientist

Evolving multi-agent AI scientist framework whose three specialized agents share persistent ideation and experimentation memories that distill prior successes and failures into reusable strategies.

| | |
|---|---|
| **Affiliation** | Huawei Technologies Co., Ltd., with Vrije Universiteit Amsterdam (Lyu et al.) |
| **First introduced** | 2026-03 (arXiv:2603.08127) |
| **Lifecycle stages** | Multi-stage (idea generation, experiment implementation and execution) |
| **Autonomy level** | Fully autonomous (end-to-end scientific discovery loop) |
| **Domain focus** | General — evaluated on AI/ML research topics drawn from contemporary papers |
| **Availability** | Open source (paper states "Code is available on EvoScientist"; repo URL pending) |

## Approach

EvoScientist decomposes end-to-end scientific discovery into three specialized agents: a Researcher Agent (RA) that performs Idea Tree Search for scientific ideas and proposals, an Engineer Agent (EA) that performs Experiment Tree Search to generate, run, and report on executable code, and an Evolution Manager Agent (EMA) that distills interaction histories into two persistent memory modules — an ideation memory summarizing top-ranked research directions and recording previously failed ones, and an experimentation memory capturing effective data-processing and model-training strategies derived from code-search trajectories. Both RA and EA query their respective memories before each decision, so each new task starts from accumulated successes and failures rather than a static pipeline.

## Validation

Benchmarked on scientific idea generation, code generation, and end-to-end scientific discovery against seven state-of-the-art open-source and commercial systems, including Virtual Scientist, AI-Researcher, InternAgent (NovelSeek), and AI Scientist-v2. Idea generation was scored by both automatic LLM evaluation and human judges across novelty, feasibility, relevance, and clarity. Code execution was scored by success rate over multi-step experimental tree searches.

## Notable results

- Outperforms seven open-source and commercial AI-scientist baselines on idea generation across novelty, feasibility, relevance, and clarity (automatic + human evaluation).
- Substantially improves code-execution success rates through multi-agent evolution, with reported gains averaged across four head-to-head comparisons (InternAgent, AI Scientist-v2, Novix, AI-Researcher).
- Directly addresses the static-pipeline limitation of prior AI-scientist systems by treating interaction histories as a first-class learning signal.

## Primary paper

[Lyu et al., "EvoScientist: Towards Multi-Agent Evolving AI Scientists for End-to-End Scientific Discovery," arXiv:2603.08127 (2026)](https://arxiv.org/abs/2603.08127).

## Other references

_None yet._

## Code

Announced as open source in the paper ("Code is available on EvoScientist"). Repository URL to be confirmed at next verification pass.
