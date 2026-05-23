---
title: AIRA (AIRA-Compose and AIRA-Design)
parent: Systems
grand_parent: AI scientists
nav_order: 6
affiliation: FAIR at Meta
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Machine learning (foundation-model architecture)
availability: Closed
last_verified: 2026-05-23
---

# AIRA (AIRA-Compose and AIRA-Design)

Pair of Meta FAIR LLM-agent frameworks that autonomously discover novel foundation-model architectures: AIRA-Compose searches a combinatorial space over computational primitives, and AIRA-Design writes low-level attention mechanisms and training scripts.

| | |
|---|---|
| **Affiliation** | FAIR at Meta ([paper](https://arxiv.org/abs/2605.15871)) |
| **First introduced** | 2026-05 (arXiv:2605.15871, dated 2026-05-18) |
| **Lifecycle stages** | Multi-stage (hypothesis → experiment design → analysis, within ML-architecture research) |
| **Autonomy level** | Semi-autonomous (fixed 24-hour compute budgets per search; humans define the design space, primitives, and evaluation harness) |
| **Domain focus** | Machine-learning research — foundation-model architecture and training |
| **Availability** | Closed — no public code or weights at preprint time |

## Approach

Two complementary agent frameworks targeting different abstraction layers.

- **AIRA-Compose** deploys an ensemble of 11 agents to navigate a combinatorial design space of fundamental computational primitives (Attention, MLP, Mamba) under a fixed 24-hour compute budget. Agents operate in two stages: iteratively designing and evaluating candidate architectures at the million-parameter scale, then extrapolating the top-performing designs to 350M, 1B, and 3B parameter scales for confirmation.
- **AIRA-Design** tasks up to 20 agents with directly writing novel attention mechanisms aimed at long-range dependencies, and implementing high-performing training scripts. Evaluation is performed on the Long Range Arena (LRA) benchmark and the Autoresearch benchmark.

The combined system is positioned by the authors as a step toward recursive self-improvement — LLM agents autonomously designing the next generation of foundation models rather than relying on hand-designed Transformer baselines.

## Validation

Validation is staged across model scales (M → 350M → 1B → 3B parameters) and against multiple baselines: Llama 3.2, Composer-found alternatives (a separate architecture-search baseline), and human state-of-the-art on LRA. Autoresearch is used as an external time-bounded discovery benchmark.

## Notable results

- AIRA-Compose discovered 14 novel architectures spanning two families (**AIRAformers**, Transformer-based; **AIRAhybrids**, Transformer-Mamba-based). At the 1B-parameter scale under a fixed token budget, agent-discovered top performers consistently outperform Llama 3.2 and Composer-found alternatives.
- AIRAformer-D and AIRAhybrid-D improve downstream-task accuracy by **2.4%** and **3.8%** over Llama 3.2. AIRAformer-C scales **54%** and **71%** faster than Llama 3.2 and the best Composer-found Transformer, respectively; AIRAhybrid-C scales **23%** and **37%** faster than modified Nemotron-2 and the best Composer-found hybrid.
- AIRA-Design's best agent-designed architectures reach within **2.3%** of human SOTA on LRA document matching and **2.6%** on text classification. On the Autoresearch benchmark, Greedy Opus 4.5 achieves **0.968 validation bits-per-byte**, surpassing the published minimum reference.

## Primary paper

[Pepe et al., "Agentic Discovery of Neural Architectures: AIRA-Compose and AIRA-Design," arXiv:2605.15871](https://arxiv.org/abs/2605.15871).

## Other references

_None yet._

## Code

Not released.
