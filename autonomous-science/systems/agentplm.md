---
title: AgentPLM
parent: Systems
grand_parent: AI scientists
nav_order: 58
affiliation: Bedford College (London) and Saarland University
lifecycle_stages: [Experiment design]
autonomy: Semi-autonomous
domain: Biology / protein engineering
availability: Closed
last_verified: 2026-06-05
---

# AgentPLM

Agentic protein language model that interleaves autoregressive sequence generation with tool calls (ESMFold, FoldX, AutoDock Vina) under Reasoning-Augmented Decoding, trained end-to-end via Contrastive Agent Policy Optimisation to learn when oracle feedback is informative.

| | |
|---|---|
| **Affiliation** | Bedford College, London (Sahil Rahman) and Saarland University (Maxx Richard Rahman) |
| **First introduced** | 2026-06 (arXiv preprint); accepted to ICML 2026 |
| **Lifecycle stages** | Experiment design (the agent decides which biophysical oracle to query during in-silico protein-sequence design) |
| **Autonomy level** | Semi-autonomous (policy-driven tool selection during decoding; no wet-lab loop) |
| **Domain focus** | Biology / computational protein engineering |
| **Availability** | Closed (no code release noted in the preprint) |

## Approach

Each design step is modelled as a decision in a Partially Observable Markov Decision Process over the joint space of partial sequences and retrieved biophysical context. Two contributions:

- **Reasoning-Augmented Decoding (RAD)** — interleaves autoregressive PLM generation with structured tool calls to ESMFold, FoldX, and AutoDock Vina, incorporating their outputs via a learned **Tool Context Encoder (TCE)** and **Trajectory Memory Buffer (TMB)** trained end-to-end on protein-engineering objectives.
- **Contrastive Agent Policy Optimisation (CAPO)** — a trajectory-level extension of direct preference optimisation that contrasts high-fitness trajectories with coherent oracle use against low-fitness or contradictory ones, teaching the model when oracle feedback is informative rather than merely imitating high-fitness sequences.

AgentPLM is initialised from the public ESM-2 650M checkpoint and trained in two phases (TCE/TMB only, then joint optimisation with layer-wise decay). Distinct from earlier ProtAgent, which freezes a GPT-4 backbone as a planner; AgentPLM trains the agent policy itself.

## Validation

Benchmark tasks spanning de novo enzyme design, antibody optimisation, thermostability, PPI interface design, and zero-shot fitness prediction, with standardised oracle APIs and controlled sequence-identity splits. The authors claim mechanistic evidence of **online error correction without explicit backtracking**.

## Notable results

- **2.79× improvement in antibody top-10% hit rate** over the strongest passive baseline.
- **+34% normalised k_cat/K_M** on enzyme design.
- Outperforms all baselines across the five benchmark tasks; authors attribute the gain to qualitatively different reasoning trajectories rather than additional compute.

## Primary paper

[Rahman & Rahman, "AgentPLM: Agentic Protein Language Models with Reasoning-Augmented Decoding for Protein Sequence Design," arXiv:2606.02386 (Jun 2026); ICML 2026](https://arxiv.org/abs/2606.02386).

## Other references

_None._

## Code

Not released.
