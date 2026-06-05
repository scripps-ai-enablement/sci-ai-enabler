---
title: LEAP
parent: Systems
grand_parent: AI scientists
nav_order: 49
affiliation: Renmin University of China (School of Physics; School of Chemistry and Life Resource)
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Materials / chemistry (perovskite solar cells)
availability: Unknown
last_verified: 2026-06-01
---

# LEAP

Expert-in-the-loop closed-loop framework that couples a domain-specialized LLM with Bayesian optimization for iterative perovskite precursor additive discovery.

| | |
|---|---|
| **Affiliation** | Renmin University of China (Ze-Feng Gao, Peng-Jie Guo, Cheng Mu, Zhong-Yi Lu) |
| **First introduced** | 2026-05 (arXiv:2605.20242) |
| **Lifecycle stages** | Multi-stage (literature mining + descriptor generation + experiment selection + analysis with expert feasibility review) |
| **Autonomy level** | Semi-autonomous — model-prioritized candidates are reviewed by domain experts before validation |
| **Domain focus** | Materials science / chemistry — perovskite solar cell precursor additives |
| **Availability** | Unknown (no public code link in the preprint) |

## Approach

LEAP (LLM-driven Exploration via Active Learning for Perovskites) builds a domain-specialized LLM, **Perovskite-RL**, by supervised fine-tuning and reinforcement learning on the perovskite-additive literature. Perovskite-RL evaluates candidate molecules and emits **soft mechanistic descriptors** along five interpretable axes — binding mode, interfacial shielding, hydrophobic protection, ion-interaction potential, and electronic modulation — derived through repeated probabilistic reasoning and aggregation. These soft descriptors are concatenated with deterministic hard molecular features to form a hybrid representation that feeds a Gaussian-process surrogate model with expected-improvement acquisition.

Each iteration runs four steps: Perovskite-RL re-generates soft descriptors under an updated reasoning context that includes the latest experimental observations; the GP surrogate is retrained on accumulated ∆PCE data; EI scores are recomputed; and prioritized candidates pass through expert review for chemical plausibility, precursor-solution compatibility, safety, cost, and device-fabrication feasibility before wet-lab validation. Device-level PCE, film quality, and defect-suppression readouts flow back into the dataset for the next round.

## Validation

On a 32-question mechanism-consistency benchmark drawn from 16 unseen additive papers, Perovskite-RL scored **78.1%** (25/32), outperforming general-purpose baselines (gemini-3-flash 50.0%, DeepSeek-V3.2 46.9%, GPT-5 43.8%, Qwen3-32B 37.5%, llama-3.3-70b-instruct 28.1%) with Holm-Bonferroni-adjusted McNemar p-values from <0.001 to <0.05. A retrospective representation ablation on 36 hot-start additives showed the hybrid LEAP descriptor space lifted Spearman correlation from 0.274 (hard-only) to 0.394 and top-20% overlap from 0.125 to 0.375.

Three rounds of expert-in-the-loop wet-lab validation in inverted ITO/NiOx/4PADCB/perovskite/C60/BCP/Ag devices tested one LEAP-prioritized additive per round (Boc-DCPy, 6-CDQ, 2-CNA), with 24 devices fabricated per condition.

## Notable results

- Mean device PCE 20.13 ± 0.25% (6-CDQ) and 20.87 ± 0.25% (2-CNA) vs 19.25 ± 0.28% for control; champion PCE 21.32% (2-CNA, VOC 1.128 V, JSC 23.92 mA/cm², FF 0.790).
- First-round candidate Boc-DCPy underperformed (16.76 ± 0.58%); the workflow recovered in subsequent rounds after feeding the negative result back into the surrogate and prompting context.
- Mechanism-consistency accuracy 78.1% vs ≤50% for general-purpose LLM baselines on unseen perovskite-additive papers.

## Primary paper

[Wang, Chen, Gao, Guo, Mu, Lu, "LEAP: A closed-loop framework for perovskite precursor additive discovery," arXiv:2605.20242 (2026)](https://arxiv.org/abs/2605.20242).

## Other references

_None yet._

## Code

Not released as of the preprint.
