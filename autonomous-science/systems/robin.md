---
title: Robin (FutureHouse)
parent: Systems
grand_parent: AI scientists
nav_order: 36
affiliation: FutureHouse, with University of Oxford and Fordham University
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Biology / therapeutics
availability: Open source + closed agent platform
last_verified: 2026-05-20
---

# Robin (FutureHouse)

First multi-agent system to integrate hypothesis generation with experimental data analysis in a lab-in-the-loop workflow. Built on the Aviary framework, validated wet-lab in dry age-related macular degeneration.

| | |
|---|---|
| **Affiliation** | FutureHouse, with collaborators at the University of Oxford and Fordham University ([FutureHouse](https://www.futurehouse.org/)) |
| **First introduced** | 2025-05 (preprint); peer-reviewed paper accepted 2026-05 |
| **Lifecycle stages** | Multi-stage (hypothesis generation + experiment design + analysis; lab-in-the-loop) |
| **Autonomy level** | Semi-autonomous (closed-loop with checkpoints; humans run wet-lab experiments) |
| **Domain focus** | Biology / therapeutics |
| **Availability** | Open source (code) + closed agent platform (FutureHouse-hosted Crow / Falcon / Finch endpoints) |

## Approach

Multi-agent Jupyter notebook built on the FutureHouse Aviary framework. Combines PaperQA2-based literature search agents (Crow for concise, Falcon for deep summaries) with Finch, a Jupyter-native data analysis agent that runs analyses across multiple independent trajectories and produces consensus conclusions.

## Validation

Wet-lab study on dry age-related macular degeneration (dAMD). Robin proposed enhancement of retinal pigment epithelium phagocytosis as a strategy, selected drug candidates, analyzed RNA-seq follow-up, and produced all hypotheses, analyses, and figures in the main text.

## Notable results

- Identified ripasudil (a clinically used ROCK inhibitor) as a novel dAMD candidate, confirmed in vitro.
- Identified KL001 as a second hit.
- Proposed and analyzed an RNA-seq follow-up that revealed ABCA1 upregulation as a candidate mechanism/target.

## Primary paper

[Ghareeb et al., "A multi-agent system for automating scientific discovery," *Nature* 2026](https://doi.org/10.1038/s41586-026-10652-y).

## Other references

- [Narayanan et al., "Aviary: training language agents on challenging scientific tasks," arXiv (2024)](https://arxiv.org/abs/2412.21154)

## Code

- [Robin repo](https://github.com/Future-House/robin)
- [Finch repo](https://github.com/Future-House/finch)
