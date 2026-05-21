---
title: AgenticSciML
parent: Systems
grand_parent: AI scientists
nav_order: 2
affiliation: Brown University (Karniadakis group, Division of Applied Mathematics)
lifecycle_stages: [Hypothesis, Experiment design]
autonomy: Semi-autonomous
domain: Scientific machine learning
availability: Code on request
last_verified: 2026-05-21
---

# AgenticSciML

Multi-agent system in which more than ten specialized LLM agents debate, retrieve, and evolutionarily refine scientific-machine-learning architectures and training procedures.

| | |
|---|---|
| **Affiliation** | Brown University, Division of Applied Mathematics ([Karniadakis lab](https://www.brown.edu/research/projects/crunch/)) |
| **First introduced** | 2025-11 (arXiv:2511.07262) |
| **Lifecycle stages** | Hypothesis (new SciML modeling strategies) + Experiment design (architectures, loss formulations, training procedures) |
| **Autonomy level** | Semi-autonomous (human supplies problem statement, requirements, evaluation criteria, and approves the evaluation contract; agents then run iterative tree expansion) |
| **Domain focus** | Scientific machine learning — physics-informed neural networks (PINNs), neural operators, PDE-constrained learning, inverse problems |
| **Availability** | Code on request — repository announced "available on GitHub upon publication" in the preprint |

## Approach

Three-phase pipeline. (1) The human user provides `Problem.md`, `Requirements.md`, `Evaluation.md`, and an optional `Data_config.json`. (2) A multi-modal data-analyst agent performs exploratory data analysis on the training set and writes a `data_analysis.md` for downstream text-only agents; an evaluator agent then writes a formal evaluation contract (`evaluate.py` and `guidelines.md`) that the human approves. (3) Specialized agents — knowledge retrievers, proposers, critics, engineers, debuggers, and a result-analyst — collaboratively expand a tree of candidate solutions through ensemble-guided evolutionary search. The best-scoring solution is always retained for mutation (exploitation), while additional parents are selected by majority vote of a diverse ensemble of selector agents (exploration). A persistent methodological memory stores prior solutions, ablations, and error analyses; structured debate forces proposers and critics to justify and revise modeling decisions.

## Validation

Benchmarked on PDE-constrained learning, operator learning, and inverse problems. The authors compare against single-agent LLM systems, automated PINN frameworks, and NAS / AutoML baselines.

## Notable results

- Reports up to four orders of magnitude error reduction over single-agent and human-designed baselines (sometimes 1000×) on physics-informed and operator-learning tasks.
- Discovers SciML strategies that do not appear in the curated knowledge base, including adaptive domain-decomposed PINNs for multi-scale PDEs, physics-informed operator-learning architectures with constraint-conditioned branches, and dynamically weighted loss schedules derived from residual-flow structure.

## Primary paper

[Jiang & Karniadakis, "AgenticSciML: Collaborative Multi-Agent Systems for Emergent Discovery in Scientific Machine Learning," arXiv:2511.07262](https://arxiv.org/abs/2511.07262).

## Other references

_None yet._

## Code

Not released at preprint time; the paper states code and experiment results will be available on GitHub upon publication.
