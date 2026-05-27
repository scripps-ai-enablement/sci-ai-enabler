---
title: POISE
parent: Systems
grand_parent: AI scientists
nav_order: 33
affiliation: Fudan University (Xia, Zhang, Chen, Wu, Yuan, Xiao)
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Machine-learning research — reinforcement-learning algorithm discovery for LLMs
availability: Unknown
last_verified: 2026-05-25
---

# POISE

Closed-loop framework from Fudan that autonomously discovers improved policy-optimization algorithms for LLM reinforcement learning by proposing, implementing, verifying, evaluating, and reflecting on mechanism-level changes inside a genealogically linked archive.

| | |
|---|---|
| **Affiliation** | Shanghai Key Laboratory of Data Science, Fudan University ([paper](https://arxiv.org/abs/2603.23951)) |
| **First introduced** | 2026-03 (arXiv:2603.23951, dated 2026-03-25) |
| **Lifecycle stages** | Multi-stage — proposal generation → implementation/verification/evaluation → reflective analysis with archive update |
| **Autonomy level** | Semi-autonomous — humans configure the baseline algorithm, evaluation pipeline (VeRL recipe), and benchmark suite; POISE then runs the discovery loop |
| **Domain focus** | Reinforcement learning for language-model policy optimization; the discovery target is the optimization algorithm itself (loss design, advantage estimation, regularization) |
| **Availability** | Unknown — no public repository disclosed in the preprint |

## Approach

POISE formulates algorithm discovery as **Epistemic Evolutionary Search** over a feasible algorithm space Z. A genealogically linked archive M_t records each entry as (proposal z_i, implementation ρ_i, training trajectory τ_i, evaluation metrics y_i, natural-language reflection r_i). Three operators coordinate the loop around a standardized evaluation pipeline O(z) that executes training and returns (τ, y).

- **Proposal Operator (P).** Conditions on a selected parent entry and proposes N candidates using historical evidence, reflection, and external literature priors L. Lineage prioritization is an acquisition function balancing Pareto-frontier strength (`U_pareto`), normalized performance (`U_perf`), diversity (`U_div`), and a GP-UCB term `α_GP(d)` whose target is a discounted top-K descendant-gain — favoring nodes likely to yield stronger descendants rather than only currently-strong nodes. Proposal context is a tiered reference set (Pareto, complementary, exploratory) plus literature priors.
- **Reflective Analysis Operator (A).** Converts training dynamics and metrics into a mechanism-level diagnosis that becomes the next reflection r_{t+1}.
- **Archive Update Operator (U).** Updates the archive and lineage structure, selects anchors for subsequent evolution.

Phase II implements proposals under shared VeRL recipe interfaces and runs verification/consistency checks before training.

## Validation

Mathematical-reasoning experiments starting from a **GRPO** baseline (Shao et al. 2024). POISE evaluates 64 candidate algorithms and is compared against the GRPO starting point and recent component-level refinements (DAPO, SAPO, ASPO, GMPO) discussed in related work.

## Notable results

- Best discovered variant lifts **weighted Overall from 47.8 → 52.5 (+4.6)** and **AIME25 pass@32 from 26.7% → 43.3%** vs. the GRPO baseline.
- Mechanism discoveries include **analytic-variance scaling** and **validity masking**.
- Beyond producing stronger algorithms, lineage analysis surfaces interpretable design principles — **signal decoupling**, **conditional normalization**, and **correctness-first efficiency shaping** — for sparse-reward LM policy optimization.

## Primary paper

[Xia, Zhang, Chen, Wu, Yuan, Xiao, "From AI Assistant to AI Scientist: Autonomous Discovery of LLM-RL Algorithms with LLM Agents (POISE)," arXiv:2603.23951](https://arxiv.org/abs/2603.23951).

## Other references

_None yet._

## Code

Not released at preprint time.
