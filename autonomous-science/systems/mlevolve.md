---
title: MLEvolve
parent: Systems
grand_parent: AI scientists
nav_order: 59
affiliation: Shanghai Artificial Intelligence Laboratory
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Machine learning (algorithm discovery)
availability: Open source
last_verified: 2026-06-05
---

# MLEvolve

LLM-based self-evolving multi-agent framework that autonomously discovers end-to-end machine-learning solutions by extending tree search to a Progressive Monte Carlo Graph Search and accumulating reusable experience in a Retrospective Memory.

| | |
|---|---|
| **Affiliation** | Shanghai Artificial Intelligence Laboratory, with East China Normal University ([paper](https://arxiv.org/abs/2606.06473)) |
| **First introduced** | 2026-06 (arXiv:2606.06473, dated 2026-06-04) |
| **Lifecycle stages** | Multi-stage (propose solution → execute code → evaluate → adapt strategy, within ML-algorithm research) |
| **Autonomy level** | Semi-autonomous (fixed 500-step / 12-hour budget per task; humans define the task, search space, and evaluation harness) |
| **Domain focus** | Machine-learning research — end-to-end MLE and mathematical algorithm optimization |
| **Availability** | Open source ([github.com/InternScience/MLEvolve](https://github.com/InternScience/MLEvolve)) |

## Approach

MLEvolve targets three limitations the authors identify in prior MLE agents: inter-branch information isolation, memoryless search, and lack of hierarchical control. It unifies three components.

- **Progressive Monte Carlo Graph Search (MCGS)** replaces tree search with a graph that adds cross-branch reference edges so successful strategies transfer across trajectories, and an entropy-inspired progressive schedule that steers the search from broad exploration toward focused exploitation over the run.
- **Retrospective Memory** pairs a cold-start domain knowledge base (domain priors) with a dynamic global memory of search records that automatically accumulates and retrieves task-specific experience during the search, rather than propagating scalar rewards alone.
- **Hierarchical Planning with Adaptive Code Generation** decouples a Planner (what/why to change) from a Coder (how), and selects among full-rewrite, stepwise, and diff-based editing modes according to the current search state.

## Validation

Evaluated on two benchmarks with Gemini-3.1-Pro-preview as the backbone (temperature 1.0; 500 expansion steps, 12-hour runtime per task on 21 vCPUs, 234 GB RAM, single NVIDIA H200): OpenAI's **MLE-Bench** (75 Kaggle tasks across low/medium/high complexity) and 15 open-ended mathematical optimization tasks from AlphaEvolve. Compared against proprietary agents (FM-Agent, MLE-STAR-Pro-1.5, MARS, MARS+, AIBuildAI) and open-source agents (AIDE, R&D-Agent, ML-Master, AIRA-Dojo, Leeroo, ML-Master 2.0). Component ablations on MLE-Bench Lite (22 tasks) show removing Progressive MCGS causes the largest medal-rate drop; removing Retrospective Memory drops medal rate by 13.64%.

## Notable results

- **65.3% average medal rate** and **34.7% gold medal rate** on the full 75-task MLE-Bench under a 12-hour budget (half the standard 24-hour runtime) — reported as state-of-the-art among compared agents, with **100% valid submission rate** and **76.0% above-median rate**.
- Per-complexity medal rates of **80.3% / 64.0% / 46.7%** on low / medium / high tasks.
- On the 15 AlphaEvolve mathematical optimization tasks, best result on **11 of 15** when compared against AlphaEvolve, AlphaEvolve-v2, SimpleTES, TTT-Discover, and OpenEvolve — evidence of cross-domain generalization.

## Primary paper

[Du et al., "MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery," arXiv:2606.06473](https://arxiv.org/abs/2606.06473).

## Other references

_None yet._

## Code

[Repository](https://github.com/InternScience/MLEvolve).
