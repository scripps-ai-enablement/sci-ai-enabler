---
title: SR-Scientist
parent: Systems
grand_parent: AI scientists
nav_order: 41
affiliation: Shanghai Jiao Tong University (Xia, Sun, Liu) with Shanghai Innovation Institute and GAIR
org_short: SJTU
lifecycle_stages: [Multi-stage]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Scientific equation discovery (symbolic regression) across chemistry, biology, physics, and materials science
domain_group: Math & symbolic
availability: Open source
access: Open source
tagline: Agentic equation discovery — the LLM writes analysis code, tests candidate equations, and iterates on feedback.
last_verified: 2026-08-08
---

# SR-Scientist

Equation-discovery framework that promotes the LLM from an equation proposer inside a search algorithm to an autonomous agent that writes code to analyze data, implements candidate equations, evaluates them, and refines them from experimental feedback.

| | |
|---|---|
| **Affiliation** | Shanghai Jiao Tong University with Shanghai Innovation Institute and GAIR ([paper](https://arxiv.org/abs/2510.11661)) |
| **First introduced** | 2025-10 (arXiv:2510.11661); v2 dated 2026-02-17, published at ICLR 2026 |
| **Lifecycle stages** | Multi-stage (hypothesize an equation → design and run its evaluation → analyze the residuals and revise) |
| **Autonomy level** | Semi-autonomous — the dataset and error target are human-specified; the agent then runs long-horizon optimization with minimal human-defined pipeline structure |
| **Domain focus** | Symbolic regression over chemistry, biology, physics, and materials-science problems |
| **Availability** | Open source ([github.com/GAIR-NLP/SR-Scientist](https://github.com/GAIR-NLP/SR-Scientist)) |

## Approach

Prior LLM-based symbolic regression embeds the model as a proposer inside genetic programming: the LLM emits candidate expressions and a fixed outer loop does the searching. SR-Scientist inverts that relationship. A code interpreter is wrapped as two tools — data analysis and equation evaluation — and the agent is instructed to drive the optimization itself, deciding when to inspect raw data, when to fit, and when to change functional form. A typical trajectory begins with the agent loading the dataset and printing rows to reason about sign and magnitude before proposing any expression.

Long-horizon operation is supported by an experience buffer that retains previously explored equations and fetches the top-*k* back into context, so later iterations build on earlier failures. The published configuration allows up to 25 turns per iteration over 40 iterations. The authors additionally build an end-to-end reinforcement-learning framework (on verl) to train the agent's behaviour rather than only prompting it.

## Validation

Evaluated on **LSR-Synth**, the synthetic partition of LLM-SRBench: 129 problems across chemistry (36), biology (24), physics (44), and materials science (25), each combining known terms with synthetic novel terms specifically to defeat memorization, and each verified by two subject-matter experts. LSR-Transform was deliberately excluded after the authors found nearly half its problems solved on the first iteration, indicating residual memorization. The primary metric is accuracy-to-tolerance (Acc<sub>0.01</sub> and Acc<sub>0.001</sub>) on held-out in-domain and out-of-domain test sets, with the worst 5% of predictions discarded; symbolic accuracy against the ground-truth expression is reported separately.

Baselines span non-LLM methods (GPLearn, E2E, NeSymReS, DSR, uDSR, PySR, each capped at 100,000 candidate equations) and LLM methods (LLM-SR, LaSR, capped at 1,000 LLM calls). Backbones tested include Qwen3-Coder-480B-A35B, GLM-4.5-Air, GPT-OSS-120B, GPT-OSS-20B, and Qwen3-Coder-30B-A3B; every experiment is repeated three times and averaged.

## Notable results

- Outperforms baseline symbolic-regression methods by an **absolute 6–35%** across the four scientific domains of LSR-Synth.
- Discovered equations generalize to out-of-domain test data and hold up under added noise, with symbolic accuracy reported alongside numerical fit.
- RL training on Qwen3-Coder-30B-A3B, with 1,024 synthesized training problems deduplicated against the benchmark by two authors independently, improves agent performance further.

## Primary paper

[Xia, Sun, Liu, "SR-Scientist: Scientific Equation Discovery With Agentic AI," ICLR 2026; arXiv:2510.11661](https://arxiv.org/abs/2510.11661).

## Other references

_None yet._

## Code

[github.com/GAIR-NLP/SR-Scientist](https://github.com/GAIR-NLP/SR-Scientist) — code and data.
