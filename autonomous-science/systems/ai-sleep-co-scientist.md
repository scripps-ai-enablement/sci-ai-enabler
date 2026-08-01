---
title: AI Sleep Co-Scientist
parent: Systems
grand_parent: AI scientists
nav_order: 5
affiliation: Stanford University (Biomedical Data Science, Computer Science, and Psychiatry — Rahul Thapa, Emmanuel Mignot, James Zou) with the Technical University of Denmark, the Danish Center for Sleep Medicine, Washington University School of Medicine Neurology, and Together AI
org_short: Stanford
lifecycle_stages: [Multi-stage]
validation_type: Wet-lab
autonomy: Semi-autonomous
domain: Sleep medicine — polysomnography, sleep physiology, and clinical epidemiology
domain_group: Biology & medicine
availability: Unknown — no code-release statement in the preprint; cohort access is governed per-dataset
access: Unknown
tagline: Expert-guided agent environment that mines ~124,000 polysomnography recordings, binding every result to executable code.
last_verified: 2026-08-01
---

# AI Sleep Co-Scientist

Expert-guided multi-agent research environment in which human scientists direct specialist agents for hypothesis development, signal preprocessing, and statistical analysis across roughly 124,000 polysomnography recordings, with every reported result linked to the executable code that produced it.

| | |
|---|---|
| **Affiliation** | Stanford University, with the Technical University of Denmark, the Danish Center for Sleep Medicine, Washington University School of Medicine, and Together AI |
| **First introduced** | 2026-07 (arXiv:2607.25175) |
| **Lifecycle stages** | Multi-stage (hypothesis development, signal preprocessing, statistical analysis) |
| **Autonomy level** | Semi-autonomous — human scientists direct the specialist agents and review intermediate outputs |
| **Domain focus** | Sleep physiology and sleep medicine — multimodal PSG across clinical and epidemiological cohorts |
| **Availability** | Unknown — no code release stated; cohort access governed per dataset (HSP v2.0 and SSC via the BIDMC Brain Data Science Portal, CDH via Stanford Medicine, BioSerenity proprietary) |

## Approach

The environment separates the work of a PSG study into specialist agents — hypothesis development, signal preprocessing, and statistical analysis — that human scientists direct and whose intermediate outputs they review. The design targets three costs that have kept large PSG archives underused: scale (hundreds of thousands of hours of continuously sampled signal per hypothesis), multimodal complexity (concurrent brain, autonomic, respiratory, and musculoskeletal channels sampled at up to hundreds of hertz, each demanding distinct clinical interpretation), and fragmentation (recordings accumulated under different montages and channel-naming conventions across institutions, requiring harmonization before joint analysis). Provenance is enforced structurally: each reported result is bound to the executable code that produced it, giving an auditable record of the research process rather than a narrative report.

## Validation

Five case studies across four clinical and epidemiological cohorts comprising approximately 124,000 PSG recordings and more than 50 TB of raw signal, spanning three directions: how sleep physiology relates to future disease, how it distinguishes clinical phenotypes, and how sleep is organized and regulated. Findings are reported with effect sizes and confidence intervals against incident-disease endpoints and against comparator model architectures rather than as demonstrations of agent capability.

## Notable results

- Diminished network-level physiological coupling during sleep was associated with incident Parkinson's disease (HR 1.48, 95% CI 1.31–1.67) and Alzheimer's disease (HR 1.38, 95% CI 1.25–1.53).
- A physiologically structured late-fusion sleep-age model outperformed an unconstrained early-fusion approach (MAE 7.06 vs 7.33 years in the Stanford Sleep Clinic cohort; 8.83 vs 9.52 years in the Human Sleep Project), and its age residual was associated with incident disease across multiple organ systems.
- Arousal dynamics characterized comorbid insomnia and sleep apnoea as an intermediate phenotype skewed toward obstructive sleep apnoea but distinguished from it by prolonged post-arousal wakefulness and more irregular arousal organization; transient-oscillation analysis identified a fast-sigma deficit and excess centrofrontal theta activity in narcolepsy type 1.

## Primary paper

[Thapa et al., "Agentic AI-enabled discovery across large-scale sleep physiology," arXiv:2607.25175](https://arxiv.org/abs/2607.25175).

## Other references

_None yet._

## Code

Unknown — no repository stated in the preprint.
