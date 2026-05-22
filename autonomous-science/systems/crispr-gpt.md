---
title: CRISPR-GPT
parent: Systems
grand_parent: AI scientists
nav_order: 10
affiliation: Stanford University (Cong lab), Princeton, UC Berkeley, Google DeepMind
lifecycle_stages: [Experiment design, Analysis]
autonomy: Assistive
domain: Biology (CRISPR-Cas gene editing)
availability: Closed
last_verified: 2026-05-20
---

# CRISPR-GPT

Four-agent LLM planner for CRISPR-Cas gene-editing experiments, spanning 22 individual tasks across knockout, base, prime, and epigenetic editing.

| | |
|---|---|
| **Affiliation** | Stanford University (Cong lab), Princeton, UC Berkeley, Google DeepMind ([Qu et al.](https://doi.org/10.1038/s41551-025-01463-z)) |
| **First introduced** | 2024-04 (arXiv v1); peer-reviewed version in *Nat. Biomed. Eng.* 2026-02 |
| **Lifecycle stages** | Experiment design, Analysis |
| **Autonomy level** | Assistive (human-in-the-loop; user-proxy agent operates autonomously but user oversight is encouraged) |
| **Domain focus** | Biology (CRISPR-Cas gene editing — knockout, base editing, prime editing, epigenetic editing) |
| **Availability** | Closed (no full code release pending US regulatory clarity on AI in biology); welcome page on GitHub |

## Approach

Multi-agent LLM system with four roles:

- **Planner** — decomposes user requests into a chain of state-machine tasks.
- **Task Executor** — manages workflow.
- **User-Proxy** — mediates user interaction.
- **Tool Providers** — wrap external tools, databases, and web search via APIs.

The system implements 22 individual gene-editing tasks (sgRNA design, off-target prediction, delivery selection, protocol drafting, validation assay design) across Meta, Auto, and QA modes.

## Validation

Real-world case study of non-expert researchers using CRISPR-GPT to plan and execute gene-editing experiments from scratch, as reported in the *Nature Biomedical Engineering* paper.

## Notable results

First LLM agent system reported to span the full CRISPR experimental-design workflow across four editing modalities. Demonstrated to help non-experts plan and execute real gene-editing experiments.

## Primary paper

[Qu et al., "CRISPR-GPT for agentic automation of gene-editing experiments," *Nat. Biomed. Eng.* 10, 245–258 (2026)](https://doi.org/10.1038/s41551-025-01463-z).

## Other references

- [arXiv:2404.18021](https://arxiv.org/abs/2404.18021)

## Code

[Welcome page](https://github.com/cong-lab/crispr-gpt-pub) — full codebase withheld pending regulatory clarity.
