---
title: ChemCrow
parent: Systems
grand_parent: AI scientists
nav_order: 11
affiliation: EPFL / University of Rochester
lifecycle_stages: [Experiment design, Analysis]
autonomy: Semi-autonomous
domain: Chemistry (organic synthesis, reaction planning)
availability: Open source
last_verified: 2026-05-20
---

# ChemCrow

GPT-4-driven chemistry agent combining chain-of-thought reasoning with 18 expert-designed chemistry tools (retrosynthesis, molecule property lookup, web/literature search, reaction execution).

| | |
|---|---|
| **Affiliation** | EPFL / University of Rochester ([Bran et al.](https://www.nature.com/articles/s42256-024-00832-8)) |
| **First introduced** | 2023-04 (arXiv preprint); *Nature Machine Intelligence* 2024 |
| **Lifecycle stages** | Experiment design, Analysis |
| **Autonomy level** | Semi-autonomous (closed-loop with checkpoints) |
| **Domain focus** | Chemistry (organic synthesis, reaction planning) |
| **Availability** | Open source |

## Approach

GPT-4 driven agent that combines chain-of-thought reasoning with 18 expert-designed chemistry tools. The agent plans, calls tools, and integrates results to complete chemistry tasks.

## Validation

Demonstrated on synthesis planning tasks (e.g., insect repellent, organocatalyst, novel chromophore). Evaluated by expert chemists and an LLM grader against an unaugmented GPT-4 baseline.

## Notable results

Autonomously planned and executed syntheses. Outperformed GPT-4 baseline on expert and automated chemistry evaluations per the Gao et al. *Cell* perspective citation.

## Primary paper

[Bran et al., "Augmenting large language models with chemistry tools," *Nat. Mach. Intell.* 2024](https://doi.org/10.1038/s42256-024-00832-8).

## Other references

- [Gao et al., *Cell* Perspective 2024](https://doi.org/10.1016/j.cell.2024.09.022) (cites ChemCrow as a Level 1 agent example)

## Code

[Repository](https://github.com/ur-whitelab/chemcrow-public)
