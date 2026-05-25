---
title: Coscientist (CMU)
parent: Systems
grand_parent: AI scientists
nav_order: 15
affiliation: Carnegie Mellon University, Gomes Lab
lifecycle_stages: [Experiment design, Analysis]
autonomy: Fully autonomous
domain: Chemistry (catalysis, palladium-catalyzed cross-couplings)
availability: Code on request
last_verified: 2026-05-20
---

# Coscientist (CMU)

GPT-4 planner that orchestrates web search, documentation retrieval, Python code execution, and Symbolic Lab Language commands sent to a physical robotic chemistry platform. Fully autonomous on the experimental loop.

| | |
|---|---|
| **Affiliation** | Carnegie Mellon University, Gomes Lab ([Boiko et al.](https://www.nature.com/articles/s41586-023-06792-0)) |
| **First introduced** | 2023-12 (*Nature*) |
| **Lifecycle stages** | Experiment design, Analysis |
| **Autonomy level** | Fully autonomous (within a closed-loop chemistry workstation) |
| **Domain focus** | Chemistry (catalysis, palladium-catalyzed cross-couplings) |
| **Availability** | Code on request (per Boiko et al. supplementary) |

## Approach

GPT-4 acts as a planner that orchestrates web search, documentation retrieval, Python code execution, and Symbolic Lab Language (SLL) commands sent to a physical robotic platform. The agent autonomously plans, generates SLL, transfers code to the device, and executes experiments.

## Validation

Wet-lab execution of optimized palladium-catalyzed Suzuki and Sonogashira cross-couplings on a physical platform.

## Notable results

Designed and executed cross-coupling reaction optimizations end-to-end with no human intervention on the experimental loop.

## Primary paper

[Boiko et al., "Autonomous chemical research with large language models," *Nature* 624, 570–578 (2023)](https://doi.org/10.1038/s41586-023-06792-0).

## Other references

- [Gao et al., *Cell* Perspective 2024](https://doi.org/10.1016/j.cell.2024.09.022) (single-LLM-multi-role case study)

## Code

[Repository](https://github.com/gomesgroup/coscientist)
