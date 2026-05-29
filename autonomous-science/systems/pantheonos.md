---
title: PantheonOS
parent: Systems
grand_parent: AI scientists
nav_order: 32
affiliation: Stanford (Department of Genetics, Qiu lab) and collaborators
lifecycle_stages: [Multi-stage]
autonomy: Semi-autonomous
domain: Biology / single-cell and spatial genomics
availability: Open source (ecosystem at github.com/aristoteleo); platform at pantheonos.stanford.edu
last_verified: 2026-05-29
---

# PantheonOS

Evolvable, privacy-preserving multi-agent framework for end-to-end single-cell and multi-omics genomics analysis, with an agentic code-evolution component that autonomously improves the system's own batch-correction and gene-panel-design algorithms.

| | |
|---|---|
| **Affiliation** | Department of Genetics, Stanford University (Qiu lab) and collaborators ([pantheonos.stanford.edu](https://pantheonos.stanford.edu)) |
| **First introduced** | 2026-02 (bioRxiv 10.64898/2026.02.26.707870, posted 27 February 2026) |
| **Lifecycle stages** | Multi-stage (RL-augmented gene panel design → raw FASTQ processing → multimodal data integration → 3D spatial genomics reconstruction; algorithm self-improvement via Pantheon-Evolve) |
| **Autonomy level** | Semi-autonomous (general-purpose multi-agent framework with customizable agent composition; analyses run end-to-end on user-supplied data) |
| **Domain focus** | Single-cell and spatial genomics; multi-omics integration |
| **Availability** | Open ecosystem at github.com/aristoteleo; project at pantheonos.stanford.edu |

## Approach

PantheonOS is an abstract, extensible multi-agent architecture that pairs general orchestration with deep domain specificity for biology. It supports end-to-end single-cell and multi-omics analysis spanning reinforcement-learning-augmented gene panel design, raw FASTQ processing, multimodal data integration, and three-dimensional spatial genomics reconstruction. Central to the framework, **Pantheon-Evolve** enables agentic code evolution: the system autonomously rewrites and improves state-of-the-art batch-correction algorithms and new RL-based gene-panel-design algorithms, reporting performance beyond manually designed baselines. An intelligent model-routing mechanism adaptively selects optimal virtual-cell models across heterogeneous tasks.

## Validation

Demonstrated across three biology case studies reported in the preprint: (1) automatic three-dimensional reconstruction of mouse embryonic-day-six (E6.0) spatial gene expression, resolving asymmetric Cer1 expression and paracrine Cer1–Nodal inhibition along the proximal–distal axis; (2) integration of human fetal heart single-cell multi-omics with whole-heart 3D MERFISH+ data at post-conception week 12, uncovering spatially resolved molecular programs underlying heart disease ontogeny; (3) adaptive virtual-cell-model selection that recovers minimal regulatory networks of cardiogenesis and predicts spatially resolved perturbation effects.

## Notable results

- Pantheon-Evolve reports autonomously improved batch-correction and RL-augmented gene-panel-selection algorithms exceeding manually designed baselines — a code-evolution loop, not just orchestration.
- First-cited demonstration of paracrine Cer1–Nodal inhibition driving robust proximal–distal axis formation in mouse E6.0 3D reconstructions.
- Multi-frequency / multi-modality integration of fetal-heart single-cell + whole-heart 3D MERFISH+ data, applied to disease-relevant molecular programs.

## Primary paper

[Xu, Poussi, Zhong, Zeng et al. (Qiu group), "PantheonOS: An Evolvable Multi-Agent Framework for Automatic Genomics Discovery," *bioRxiv* 2026.02.26.707870](https://doi.org/10.64898/2026.02.26.707870).

## Other references

- [PantheonOS project page (Stanford)](https://pantheonos.stanford.edu)

## Code

[Aristotelo ecosystem on GitHub](https://github.com/aristoteleo) — public ecosystem repositories supporting PantheonOS.
