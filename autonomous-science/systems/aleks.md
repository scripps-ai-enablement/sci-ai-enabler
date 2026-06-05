---
title: Aleks
parent: Systems
grand_parent: AI scientists
nav_order: 8
affiliation: Cornell University (Jin, Gunner, Carvajal Janke, Baruah, Gold, Jiang)
lifecycle_stages: [Multi-stage]
autonomy: Fully autonomous
domain: Plant science / agriculture
availability: Unknown
last_verified: 2026-05-25
---

# Aleks

Cornell multi-agent system that autonomously formulates a plant-science problem from a natural-language research question and dataset, iterates over machine-learning modeling strategies, and converges on interpretable models.

| | |
|---|---|
| **Affiliation** | Cornell University — School of ECE and Cornell AgriTech ([paper](https://arxiv.org/abs/2508.19383)) |
| **First introduced** | 2025-08 (arXiv:2508.19383, dated 2025-08-26) |
| **Lifecycle stages** | Multi-stage — autonomous problem formulation, modeling-strategy exploration, code generation, evaluation, and domain-grounded refinement |
| **Autonomy level** | Fully autonomous — once given a research question and dataset, Aleks runs to a budgeted iteration cap without human intervention; humans only supply the seed literature for the domain agent |
| **Domain focus** | Plant science (case study: grapevine red blotch disease); designed to extend to additional plant-science questions |
| **Availability** | Unknown — no repository disclosed in the preprint |

## Approach

Aleks couples three specialized LLM-powered agents through a shared memory hub:

- **Domain Scientist (DS) agent** — initialized with a semantic memory summarizing human-supplied research papers; assesses domain plausibility of proposed features and results, biases the loop toward fewer and more interpretable features, and accounts for asymmetric error costs.
- **Data Analyst (DA) agent** — has full access to the experimental history; proposes problem formulations (classification vs. regression), preprocessing steps, and feature-engineering moves; decides when to stop or iterate.
- **Machine Learning Engineer (MLE) agent** — generates and runs executable Python code under a scoped working-memory view; uses semantic memory of API documentation and runtime/efficiency constraints, and episodic memory of execution traces for error-driven self-repair.

A central shared memory stores every iteration as (suggestion, ML result, domain feedback) tuples. The DS agent sees the question, dataset, and current results; the DA agent sees full history; the MLE agent sees only the current task. The case study uses DeepSeek Chat as the underlying LLM and constrains the MLE to auto-sklearn for tabular modeling.

## Validation

Single-domain case study on grapevine red blotch disease (GRBD), using a multi-year 10 m × 10 m vineyard grid dataset with remote-sensing vegetation indices and partial vector-activity features. Four experiment configurations test (1) reproducibility across five independent runs with all three agents and full history; (2) ablation of the DS agent; (3) ablation of long-term memory (single-iteration history); (4) a leaderboard-style compressed-history design. The only human input is the question "predict GRBD-infected grapevines in 2023" (or 2024); all preprocessing, feature engineering, problem formulation, and metric selection are delegated to Aleks. Research budget set at 20 iterations.

## Notable results

- Aleks progressively identified biologically meaningful features and converged on interpretable models with robust performance on GRBD across multiple runs.
- Ablations show that removing the DS agent or restricting memory to a single iteration degrades coherence — confirming that domain knowledge and cross-iteration memory are both necessary for the system's reasoning.
- Adds plant science / agriculture as a new domain to the catalogue, alongside chemistry, biology, materials, physics, and ML.

## Primary paper

[Jin, Gunner, Carvajal Janke, Baruah, Gold, Jiang, "Aleks: AI powered Multi Agent System for Autonomous Scientific Discovery via Data-Driven Approaches in Plant Science," arXiv:2508.19383](https://arxiv.org/abs/2508.19383).

## Other references

_None yet._

## Code

Not released at preprint time.
