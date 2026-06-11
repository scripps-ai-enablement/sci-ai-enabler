---
title: ATLAS
parent: Systems
grand_parent: AI scientists
nav_order: 10
affiliation: Google DeepMind (Éltető, Daw, Stachenfeld, Miller; with Princeton, Columbia, and UCL affiliations)
org_short: DeepMind
lifecycle_stages: [Multi-stage]
validation_type: Benchmark
autonomy: Semi-autonomous
domain: Cognitive science (computational behavioral modeling)
domain_group: ML & scientific computing
availability: No code released as of 2026-06-11 (none stated in preprint)
access: Unknown
tagline: DeepMind active-learning loop that designs experiments to discover interpretable mechanistic models of behavior.
last_verified: 2026-06-11
---

# ATLAS

Google DeepMind active-learning framework that closes the hypothesis-generation ↔ experiment-design loop to discover interpretable mechanistic models of behavior in cognitive science.

| | |
|---|---|
| **Affiliation** | Google DeepMind, with Princeton / Columbia / UCL ([paper](https://arxiv.org/abs/2606.12386)) |
| **First introduced** | 2026-06 (arXiv:2606.12386, dated 2026-06-10) |
| **Lifecycle stages** | Multi-stage — iterates data-driven hypothesis generation, optimal experiment design, and analysis of the resulting behavioral data |
| **Autonomy level** | Semi-autonomous — automates the hypothesize→design→collect loop; the human researcher interprets the discovered interpretable models |
| **Domain focus** | Cognitive science / computational behavioral modeling (test case: recovering reinforcement-learning agents from behavior) |
| **Availability** | No code released as of 2026-06-11 (none stated in the preprint) |

## Approach

ATLAS (Active Theory Learning for Automated Science) is an active-learning framework rather than an LLM-orchestration system — distinguishing it from most of the catalogue. It runs iterative cycles of three components around a growing dataset:

- **Hypothesis Generator** — trains a fresh set of Disentangled RNNs (DisRNNs) on the current dataset, sweeping the complexity-penalty parameter and random seeds. DisRNNs use information bottlenecks to converge on sparse, interpretable latent ("cognitive") variables whose interactions form a hypothetical computational graph for the underlying mechanism. Varying the sparsity penalty maintains an ensemble of qualitatively distinct hypotheses, selected via an offset-softmax distribution over cross-validated likelihoods.
- **Experiment Optimizer** — searches over experiment designs (binary T×A reward matrices) to maximize expected information gain, approximated as disagreement among ensemble members (analogous to the BALD objective). Optimization uses hill-climbing with 128 random restarts.
- **Experiment Runner** — executes the optimized design against the ground-truth agent, appending the resulting trajectory to the dataset for the next cycle.

The design draws on Query-by-Committee active learning and optimal experimental design, but replaces a fixed model committee with structurally constrained neural networks whose internal diversity encodes distinct mechanistic hypotheses.

## Validation

In-silico evaluation on recovering two reinforcement-learning agents — a Q-learning agent and a Leaky Actor-Critic agent — from their behavior in two-armed bandit tasks. Eight independent ATLAS runs of 100 cycles each were compared against two open-loop baselines (i.i.d. random rewards and Gaussian random-walk rewards) and against fixed expert-designed experiments drawn from the literature. Discovered models were scored on three criteria: behavioral similarity (held-out likelihood), structural similarity (isomorphism of the recovered computational graph to ground truth), and dynamical similarity (bidirectional bisimulation error). No wet-lab or real-world data — validation is benchmark-tier.

## Notable results

- 5–10× improvement in sample efficiency across behavioral, structural, and computational-similarity metrics versus random experimentation.
- Recovered the correct computational graph for 8/8 seeds after 100 experiments for both agents, where random and expert-designed baselines needed ~1,000 experiments (and the expert baseline never reached it for Actor-Critic).
- Matched or surpassed expert-designed experiments, while producing designs with distinctive temporal structure unlike those researchers typically hand-craft; ablations show DisRNN ensembles yield more structured, informative designs than vanilla GRU ensembles.

## Primary paper

[Éltető, Daw, Stachenfeld, Miller, "ATLAS: Active Theory Learning for Automated Science," arXiv:2606.12386](https://arxiv.org/abs/2606.12386).

## Other references

_None yet._

## Code

Not released at preprint time.
