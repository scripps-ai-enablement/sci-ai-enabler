---
title: BORA
parent: Systems
grand_parent: AI scientists
nav_order: 13
affiliation: University of Liverpool — Department of Chemistry and Leverhulme Research Centre for Functional Materials Design (Cooper lab), with the Department of Computer Science
lifecycle_stages: [Experiment design, Hypothesis]
autonomy: Semi-autonomous
domain: Chemistry / materials (general black-box optimization; demonstrated on photocatalytic hydrogen evolution)
availability: Open source
last_verified: 2026-05-30
---

# BORA

Language-Based Bayesian Optimization Research Assistant that couples an LLM with standard Bayesian optimization to inject literature-grounded domain knowledge and dynamic hypothesis generation into closed-loop experimental campaigns.

| | |
|---|---|
| **Affiliation** | University of Liverpool — Department of Chemistry / Leverhulme Research Centre for Functional Materials Design (Cooper lab), with Department of Computer Science |
| **First introduced** | 2025-01 (arXiv:2501.16224); accepted to IJCAI 2025 |
| **Lifecycle stages** | Experiment design (closed-loop BO), Hypothesis (LLM-generated proposals refined during the run) |
| **Autonomy level** | Semi-autonomous — runs without per-iteration human input but is initialised from a user-supplied Experiment Card and optionally accepts free-text hypotheses |
| **Domain focus** | Chemistry / materials (demonstrated on 10D photocatalytic hydrogen evolution); framework is domain-agnostic and also validated on solar-energy production, sugar-beet yield, and a pétanque-game model |
| **Availability** | Open source — [Ablatif6c/bora-the-explorer](https://github.com/Ablatif6c/bora-the-explorer) |

## Approach

BORA is a hybrid BO–LLM framework operating under a single Gaussian Process surrogate whose parameters update as new points are sampled by either path. At each step, an adaptive heuristic policy picks one of three actions based on the GP's mean uncertainty over a fixed set of monitoring points and a plateau detector over recent BO best-so-far values:

- **a₁ Vanilla BO** — maximise an Expected Improvement acquisition function over a Matérn-kernel GP and append the suggested point.
- **a₂ LLM comments and suggests n_LLM points** — when GP uncertainty is high, the LLM is given the full data set and prior comments, returns a structured JSON Comment with named hypotheses (rationale, confidence, candidate input), and proposes new search points.
- **a₃ LLM comments and selects n_LBO of n_BO BO candidates** — when uncertainty is intermediate, the LLM picks the most promising subset of acquisition-function candidates aligned with its hypotheses.

A trust mechanism tracks a rolling intervention score over the most recent three LLM interventions and adapts the plateau-duration threshold so the LLM is invoked more frequently when its past suggestions have helped and less frequently when they have not. The user-supplied Experiment Card describes the black-box function, input/target variables, and constraints; the LLM uses it to warm-start the optimisation with n_init initial samples derived from in-context reasoning.

## Validation

Benchmarked against Random Search, BayesOpt (vanilla BO), TuRBO, ColaBO, HypBO, and LAEA on three synthetic functions (Branin 2D, Levy 10D, Ackley 15D, anonymised in prompts to prevent name leakage) and four real scientific tasks (Solar Energy Production 4D, Pétanque 7D, Sugar Beet Production 8D, Hydrogen Production 10D, the last using the dataset and bespoke discrete-constrained implementation from Cissé et al. 2024). Implementations use GPT-4o-mini for cost-effectiveness; 10 seeds × 105 samples per task.

## Notable results

- On the 10D Hydrogen Production photocatalysis benchmark, BORA achieves a **47% reduction in cumulative regret** versus ColaBO; sign test versus HypBO gives p = 0.02 (Bonferroni-corrected, 95% confidence), and BORA outscores ColaBO in 5 of 6 tasks (p = 0.20).
- LLM-warm-started initial sampling near critical points (edges, centres, symmetric coordinates) substantially accelerates convergence on Levy and other near-symmetric functions; on the 7D Pétanque task, BORA gains a +35 score advantage early from trajectory-aware initial hypotheses.
- Ablation with LLM-only (action a₂) on Hydrogen Production and Ackley confirms the hybrid policy outperforms pure-LLM optimisation in late stages; the authors note stochastic divergence of LLM reasoning across identical prompts as a limitation.

## Primary paper

[Cissé et al., "Language-Based Bayesian Optimization Research Assistant (BORA)," arXiv:2501.16224 (IJCAI 2025)](https://arxiv.org/abs/2501.16224).

## Other references

_None yet._

## Code

[Ablatif6c/bora-the-explorer](https://github.com/Ablatif6c/bora-the-explorer).
