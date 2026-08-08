---
title: TourSynbio-Agent
parent: Systems
grand_parent: AI scientists
nav_order: 42
affiliation: Toursun Synbio, Shanghai (Chen, Liu, Shen) with City University of Hong Kong, Shanghai Jiao Tong University, and Johns Hopkins University
org_short: Toursun Synbio
lifecycle_stages: [Multi-stage]
validation_type: Mixed
autonomy: Assistive
domain: Biology (protein and enzyme engineering)
domain_group: Biology & medicine
availability: Unknown — no code-release statement in the primary paper
access: Unknown
tagline: Protein-engineering agent pairing a protein-specialized LLM with domain models, validated in dry and wet lab.
last_verified: 2026-08-08
---

# TourSynbio-Agent

Multi-agent protein-engineering framework that pairs TourSynbio-7B, a protein-specialized multimodal LLM, with domain deep-learning models, driving mutation prediction, folding, and design from a conversational interface and feeding into wet-lab enzyme campaigns.

| | |
|---|---|
| **Affiliation** | Toursun Synbio, Shanghai, with City University of Hong Kong, Shanghai Jiao Tong University, and Johns Hopkins University ([paper](https://arxiv.org/abs/2411.06029)) |
| **First introduced** | 2024-11 (validation paper arXiv:2411.06029, dated 2024-11-09; the framework itself was introduced in an earlier report) |
| **Lifecycle stages** | Multi-stage (variant hypothesis → screening-campaign design → analysis of measured activity data feeding the next round) |
| **Autonomy level** | Assistive — the user states the engineering goal in natural language and TourSynbio-7B routes it to a specialist agent; humans run the assays and decide each round |
| **Domain focus** | Protein engineering: cytochrome P450 selectivity, reductase catalytic efficiency, antibody/nanobody design |
| **Availability** | Unknown — the primary paper states no code-availability or repository information |

## Approach

TourSynbio-7B processes protein sequences directly as natural language, so no external protein encoder is needed, and it acts as the router: a natural-language request activates a specialist agent wrapping a domain model. The reported agents cover mutation-effect prediction (ESM-1v, with configurable scoring strategy and mutation-column offset), structure prediction (ESMFold, with PyMOL visualization and downloadable PDB output), and design (AntiFold over IMGT-standard PDB/CIF templates, with hyperparameter optimization ahead of sampling).

In the enzyme campaigns the same interface is used iteratively: the agent proposes variants, measured activity and selectivity data are returned, the prediction models are fine-tuned on that data, and a second round of multi-mutation variants is proposed. This makes the loop closed through a human wet lab rather than through robotics.

## Validation

Five case studies. Three dry-lab: mutation-effect prediction (H24 variant series, with H24M scoring highest at 7.85), protein folding (pLDDT 78.7 on the test sequence), and antibody design on PDB 6y1l (sequence recovery 0.9682, global score 1.0470, 14 mutations). Two wet-lab enzyme-engineering campaigns run as industrial projects. Earlier benchmarking of the underlying TourSynbio-7B model used ProteinLMBench. There is no head-to-head comparison against a non-agentic baseline workflow.

## Notable results

- **P450 steroid 19-hydroxylation**: 200 single-site mutation candidates generated in two weeks, three weeks of experimental validation, then 10 optimized variants carrying up to five mutations each. The best variant hit the target **70% improvement in product selectivity** while retaining catalytic activity; predictions correlated with measurements at r ≈ 0.7.
- **Reductase for alcohol conversion**: starting from wild-type plus 29 single-point variant measurements, the agent recommended 10 novel single-point mutations; the best gave a **3.7× enhancement in catalytic conversion rate**, again at r ≈ 0.7 prediction–measurement correlation.
- The authors present this as the first systematic validation of an LLM-based agent system in real-world protein engineering.

## Primary paper

[Chen, Liu, Wang, Shen, "Validation of an LLM-based Multi-Agent Framework for Protein Engineering in Dry Lab and Wet Lab," arXiv:2411.06029](https://arxiv.org/abs/2411.06029).

## Other references

_None yet._

## Code

Unknown — no repository is stated in the primary paper.
