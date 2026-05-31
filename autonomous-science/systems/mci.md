---
title: MCI
parent: Systems
grand_parent: AI scientists
nav_order: 47
affiliation: Korea Research Institute of Chemical Technology (KRICT) and KAIST
lifecycle_stages: [Hypothesis, Analysis]
autonomy: Fully autonomous
domain: General (symbolic equation discovery across deterministic, stochastic, and uncharacterized dynamical systems)
availability: Unknown
last_verified: 2026-05-31
---

# MCI

Machine Collective Intelligence — a multi-agent framework that integrates symbolism and metaheuristics to autonomously discover explainable governing equations from empirical observations.

| | |
|---|---|
| **Affiliation** | Korea Research Institute of Chemical Technology (KRICT) and Korea Advanced Institute of Science and Technology (KAIST) |
| **First introduced** | 2026-04 (arXiv:2604.27297) |
| **Lifecycle stages** | Hypothesis (symbolic-equation proposal), Analysis (fitting and selection across observation data) |
| **Autonomy level** | Fully autonomous within the symbolic-discovery loop |
| **Domain focus** | General — demonstrated on deterministic, stochastic, and previously uncharacterized dynamical systems |
| **Availability** | Unknown — no repository announced in the paper |

## Approach

MCI orchestrates a population of K LLM-based reasoning agents that evolve symbolic hypotheses through coordinated generation, evaluation, critique, and consolidation:

- **Knowledge representation as ASTs.** Each candidate equation is canonicalized as an abstract syntax tree; AST depth quantifies explainability (lower depth = more compact, more explainable).
- **Initialization.** Given a problem specification P (inputs/outputs) and an initial hypothesis H, each agent generates an initial equation parsed into an AST.
- **Complexity-aware evaluation.** Each AST is scored by a "discovery score" combining negative SSE on observations, an explainability term (inverse depth), and a memory term.
- **Critique and consolidation.** Agents iteratively share best experiences across the population via knowledge-propagation and accumulation schemes drawn from population-based metaheuristics, enabling exploration beyond any single agent's prior knowledge.

The framework explicitly integrates symbolism (logical, AST-based reasoning) with metaheuristics (exploration via population-based search), aiming to escape the reasoning boundary of any individual backbone LLM.

## Validation

Tested on scientific systems governed by deterministic, stochastic, and previously uncharacterized dynamics. Authors report recovery of underlying governing equations without hand-crafted domain knowledge and direct comparison to deep neural network baselines.

## Notable results

- Reduces extrapolation error by up to six orders of magnitude relative to deep neural networks on the studied systems.
- Compresses 0.5–1 million DNN parameters into 5–40 interpretable parameters in the recovered equations.
- Recovers governing equations across deterministic, stochastic, and uncharacterized regimes without domain-specific priors.

## Primary paper

[Na and Park, "Machine Collective Intelligence for Explainable Scientific Discovery," arXiv:2604.27297 (2026)](https://arxiv.org/abs/2604.27297).

## Other references

_None yet._

## Code

Unknown — no repository announced in the paper.
