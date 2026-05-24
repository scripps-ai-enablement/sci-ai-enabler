---
title: GRAFT-ATHENA
parent: Systems
grand_parent: AI scientists
nav_order: 21
affiliation: Brown University (Karniadakis group, Division of Applied Mathematics)
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Scientific computing / scientific machine learning
availability: Code on request (planned GitHub release upon acceptance)
last_verified: 2026-05-21
---

# GRAFT-ATHENA

Self-improving agentic framework that accumulates methodological experience across scientific problems and autonomously expands its own action space for the evolutionary discovery of numerical algorithms.

| | |
|---|---|
| **Affiliation** | Brown University, Division of Applied Mathematics (Karniadakis group) |
| **First introduced** | 2026-05 (arXiv:2605.11117) |
| **Lifecycle stages** | Multi-stage (problem formalization + method selection + implementation + advisor critique + cross-problem memory) |
| **Autonomy level** | Semi-autonomous — user supplies a free-form problem; the system formalizes it, samples methods from its action tree, executes, scores outcomes, and accumulates experience |
| **Domain focus** | Scientific computing — PDE solvers (Nektar++, Trixi.jl, PIML), dissipative particle dynamics (LAMMPS), and scientific machine learning |
| **Availability** | Code on request — authors state the repository will be made publicly available on GitHub upon acceptance |

## Approach

GRAFT (Graph Reduction to Adaptive Factored Trees) projects directed acyclic graphs of solver attributes and cross-rules into factored decision trees with a deterministic embedding into a metric space. Each method is a single path through an action tree T_A and each problem a single path through a companion problem tree T_P; a persistent memory D records every solved instance with its observables and reward. This changes the policy footprint from exponential to linear in decision chains while certifying the factorization as an I-map of the policy. Multiple specialized teams coordinate on this substrate: Expansion and Construction teams ingest solver documentation to grow the action graph; a Formalization team audits equations, boundary data, reductions, and identifiability before encoding a problem as a fingerprint on T_P; a Strategy team samples methods from T_A conditioned on the fingerprint; an Implementation team realizes the choice as runnable code; and an Advisor scores the outcome, revises failed choices, or extends the action tree with new nodes mid-trial. Nearest-neighbor retrieval from D over fingerprint similarity supplies a reward-calibrated prior for each new problem.

## Validation

On four canonical physics-informed machine-learning benchmarks, GRAFT-ATHENA reaches near-machine-precision accuracy, surpassing human and prior agentic baselines including the predecessor ATHENA. On production solvers it reconstructed Mach-10 hypersonic flow over the Apollo Command Module from a 1968 NASA report (Nektar++/Trixi.jl) and recovered shear-thinning red-blood-cell rheology in dissipative particle dynamics (LAMMPS). The viscous Burgers case demonstrates transfer: the prior retrieves a Reynolds-number continuation from neighboring high-Re runs and improves on the earlier agentic trace even at moderate Re.

## Notable results

- Autonomously proposed regularization constraints for ill-posed inverse problems and persisted them as new nodes in the action graph.
- Designed a spectral PINN with exponential convergence — a new numerical method emerging from agentic exploration.
- Demonstrates monotonically accumulating methodological memory across problems (every iteration, success or failure, commits to D).

## Primary paper

[Toscano, Chai, and Karniadakis, "GRAFT-ATHENA: Self-Improving Agentic Teams for Autonomous Discovery and Evolutionary Numerical Algorithms," arXiv:2605.11117](https://arxiv.org/abs/2605.11117).

## Other references

_None yet._

## Code

Authors commit to a GitHub release upon acceptance; no public URL yet.
