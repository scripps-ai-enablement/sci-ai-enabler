---
title: AutoLLMResearch
parent: Systems
grand_parent: AI scientists
nav_order: 51
affiliation: University of Notre Dame
lifecycle_stages: [Experiment design, Analysis]
autonomy: Semi-autonomous
domain: Machine learning (LLM experiment configuration)
availability: Open source
last_verified: 2026-06-01
---

# AutoLLMResearch

Agentic framework trained by reinforcement learning over a multi-fidelity LLM-experiment environment so it can extrapolate generalizable principles from cheap low-fidelity runs to efficient configuration of expensive scalable LLM experiments.

| | |
|---|---|
| **Affiliation** | University of Notre Dame — Taicheng Guo, Nitesh V. Chawla, Olaf Wiest, Xiangliang Zhang |
| **First introduced** | 2026-05 (arXiv:2605.11518) |
| **Lifecycle stages** | Experiment design + analysis (configuration of LLM training experiments: architecture, hyperparameters, RL GRPO tuning, data mixture) |
| **Autonomy level** | Semi-autonomous — agent proposes and reasons over configurations; environment supplies verifiable rewards |
| **Domain focus** | Machine-learning research — automating high-cost LLM experiment configuration |
| **Availability** | Open source — [taichengguo/AutoLLMResearch](https://github.com/taichengguo/AutoLLMResearch) |

## Approach

AutoLLMResearch targets a gap left by prior automated-research agents: configuring scalable LLM experiments where a single training run consumes hundreds of GPU hours and only a few trials are feasible. Two components anchor the framework. **LLMConfig-Gym** is a multi-fidelity environment covering four representative LLM experiment tasks — Model Architecture, Pretraining Hyperparameter, RL GRPO Tuning, and Data Mixture — backed by over **one million GPU hours of verifiable experiment outcomes** at multiple fidelity levels (e.g., ≤3B / 10B-token low-fidelity vs 7B / 20B-token high-fidelity). It supplies the agent with pre-computed rewards for each proposed configuration, enabling end-to-end multi-turn RL training.

The training pipeline formulates configuration research as a long-horizon Markov Decision Process and combines **Train/Test Experiment Curation**, **Trajectory Simulation**, **Policy Distillation**, and **Multi-turn Reinforcement Learning** to incentivize researcher-like cross-fidelity extrapolation. The agent must overcome two challenges absent in same-fidelity meta-learning: a **configuration space shift** (the training and target configuration spaces differ) and an **optimization landscape shift** (optimal configurations do not transfer monotonically across fidelities), so it must reason about fidelity-dependent trends rather than memorize.

## Validation

Extensive evaluation against diverse baselines on held-out experiments across four LLM configuration tasks and models up to 7B parameters or training tokens up to 20B. Comparators include traditional HPO tools, learned BO methods (OptFormer, MetaBO, NAP, FSBO), and LLM-prompting baselines (GPT-5, Gemini, O4-mini); only AutoLLMResearch supports cumulative experiential learning with a verifiable environment, configuration-space shift, and landscape shift.

## Notable results

- First systematic study (per the authors' knowledge) on automating expensive LLM experiment configuration via training (not just prompting) an agent.
- Reports cross-fidelity extrapolation that improves over the strongest baselines on held-out high-fidelity experiments; in-depth analysis includes natural-language explanations of the agent's cross-fidelity reasoning.
- LLMConfig-Gym released as a verifiable multi-fidelity benchmark with pre-collected outcomes across four LLM tasks.

## Primary paper

[Guo, Chawla, Wiest, Zhang, "AutoLLMResearch: Training Research Agents for Automating LLM Experiment Configuration — Learning from Cheap, Optimizing Expensive," arXiv:2605.11518 (2026)](https://arxiv.org/abs/2605.11518).

## Other references

_None yet._

## Code

[taichengguo/AutoLLMResearch](https://github.com/taichengguo/AutoLLMResearch) — released with the preprint.
