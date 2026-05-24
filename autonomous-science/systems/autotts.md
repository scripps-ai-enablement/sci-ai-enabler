---
title: AutoTTS
parent: Systems
grand_parent: AI scientists
nav_order: 9
affiliation: UMD, UVA, WUSTL, UNC, Google, Meta
lifecycle_stages: [Hypothesis, Experiment design, Analysis]
autonomy: Semi-autonomous
domain: Machine learning (test-time scaling for LLM reasoning)
availability: Open source
last_verified: 2026-05-23
---

# AutoTTS

Environment-driven agentic framework that autonomously discovers test-time-scaling (TTS) controllers for LLM reasoning by searching over branch / continue / probe / prune / stop policies on pre-collected reasoning trajectories.

| | |
|---|---|
| **Affiliation** | University of Maryland, UVA, WUSTL, UNC, Google, Meta ([paper](https://arxiv.org/abs/2605.08083)) |
| **First introduced** | 2026-05 (arXiv:2605.08083, v2 2026-05-12) |
| **Lifecycle stages** | Hypothesis (propose controller candidates), Experiment design (evaluate in offline replay environment), Analysis (diagnose failure modes from execution traces) |
| **Autonomy level** | Semi-autonomous (human constructs the discovery environment — states, actions, feedback, objectives — then the explorer LLM searches autonomously) |
| **Domain focus** | LLM test-time scaling for mathematical reasoning |
| **Availability** | Open source — [github.com/zhengkid/AutoTTS](https://github.com/zhengkid/AutoTTS) |

## Approach

AutoTTS reframes test-time scaling from hand-crafted heuristics to automatic controller discovery. The width–depth TTS problem is formalized as controller synthesis over an offline replay environment: for each question, reasoning trajectories and intermediate probe signals are pre-collected so that candidate controllers — programs that decide when to BRANCH, CONTINUE, PROBE, PRUNE, or STOP — can be evaluated cheaply without repeated LLM calls.

The discovery loop has four stages: humans define the environment (states, actions, feedback, objectives); an explorer LLM proposes candidate controllers; controllers are evaluated in the replay environment under an accuracy–cost objective; the explorer receives scaling-curve feedback and fine-grained execution-trace feedback that exposes how each controller allocates computation, and uses accumulated history to refine future proposals. Two design choices keep the search tractable: **beta parameterization**, which exposes a single scalar trade-off parameter β per controller and derives internal hyperparameters deterministically from it (reducing overfitting to the search set), and execution-trace feedback that lets the explorer diagnose *why* a controller fails rather than only *that* it fails.

## Validation

Benchmarked on mathematical-reasoning datasets (including AIME25 with Qwen-1.7B as the base model). Discovered controllers are compared against strong manually designed TTS baselines — SC@64, ASC, ESC, ANSWER CONSISTENCY, ST-BON, PARALLEL PROBE — interpreted as hand-designed points within the width–depth space. The authors also test generalization to held-out benchmarks and different model scales.

## Notable results

- Discovered controllers improve the accuracy–cost Pareto frontier over hand-crafted baselines on math reasoning.
- Discovered strategies generalize to held-out benchmarks and to different model scales without re-discovery.
- Total discovery cost reported as **$39.9 and 160 minutes** for the full one-time search.

## Primary paper

[Zheng et al., "LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling," arXiv:2605.08083](https://arxiv.org/abs/2605.08083).

## Other references

_None yet._

## Code

[Repository](https://github.com/zhengkid/AutoTTS).
