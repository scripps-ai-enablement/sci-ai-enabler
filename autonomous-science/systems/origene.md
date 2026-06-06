---
title: OriGene
parent: Systems
grand_parent: AI scientists
nav_order: 60
affiliation: Global Institute of Future Technology, Shanghai Jiao Tong University, with Shanghai AI Laboratory, Fudan University and collaborators (GENTEL Lab; corresponding author Shuangjia Zheng)
org_short: SJTU
lifecycle_stages: [Hypothesis, Analysis]
validation_type: Wet-lab
autonomy: Semi-autonomous
domain: Biology & medicine (therapeutic target discovery / drug development)
domain_group: Biology & medicine
availability: Open source (GitHub; custom NOASSERTION license)
access: Open source
tagline: Self-evolving multi-agent "virtual disease biologist" that nominates mechanism-grounded drug targets.
last_verified: 2026-06-06
---

# OriGene

Self-evolving multi-agent system framed as a "virtual disease biologist" that autonomously generates and prioritizes mechanistically grounded therapeutic-target hypotheses by reasoning across genomics, protein networks, pharmacology, clinical records, and literature.

| | |
|---|---|
| **Affiliation** | Global Institute of Future Technology, Shanghai Jiao Tong University (GENTEL Lab) ([paper](https://www.biorxiv.org/content/10.1101/2025.06.03.657658v1)) |
| **First introduced** | 2025-06 (bioRxiv preprint, posted 2025-06-06) |
| **Lifecycle stages** | Hypothesis (generates and prioritizes target-discovery hypotheses), Analysis (interprets multi-omics, perturbation, and clinical data) |
| **Autonomy level** | Semi-autonomous — the self-evolving loop incorporates human and experimental feedback, and target validation is performed by humans in patient-derived models |
| **Domain focus** | Therapeutic target discovery and drug development |
| **Availability** | Open source — GitHub (custom/non-standard license) |

## Approach

OriGene is a self-evolving multi-agent system that integrates over 600 specialized tools and curated biomedical databases through a Model Context Protocol (MCP), enabling reasoning across genomics, transcriptomics, proteomics, protein networks, pharmacology, clinical records, and literature evidence. A knowledge-graph-based Tool RAG combined with an agent-selection mechanism drives dynamic, context-aware tool deployment, so that the system selects the appropriate tools and analytical protocols for each target-discovery query.

A self-evolving framework continuously assimilates human and experimental feedback to iteratively refine the system's core thinking templates, tool composition, and analytical protocols, with the stated aim of improving accuracy and adaptability over time. The system autonomously generates and prioritizes therapeutic-target hypotheses by analyzing functional interaction networks, disease ontologies, perturbation data, and literature-derived evidence.

## Validation

OriGene is evaluated on TRQA, an original benchmark of over 1,900 expert-level question-answer pairs spanning diverse diseases and target classes. TRQA splits into TRQA-lit (172 multiple-choice plus 1,108 short-answer items covering fundamental biology, disease biology, clinical medicine, and pharmacology) and TRQA-db (641 short-answer items on drug R&D pipelines and clinical trials). The authors report that OriGene outperforms human experts, leading research agents, and state-of-the-art LLMs on accuracy, recall, and robustness, particularly under data sparsity or noise.

Beyond the benchmark, OriGene nominated two previously underexplored therapeutic targets — GPR160 for liver cancer and ARG2 for colorectal cancer — both of which demonstrated significant anti-tumor activity in patient-derived organoid and tumor-fragment models mirroring human clinical exposures.

## Notable results

- Wet-lab validation of two agent-nominated targets (GPR160 in liver cancer; ARG2 in colorectal cancer) showing anti-tumor activity in patient-derived organoid and tumor-fragment models.
- Reported to outperform human experts and SOTA LLMs on the 1,921-pair TRQA expert benchmark, especially under data-sparse or noisy conditions.
- Integrates 600+ tools via MCP with a self-evolving feedback loop refining thinking templates, tool composition, and protocols over time.

## Primary paper

[Zhang et al., "OriGene: A Self-Evolving Virtual Disease Biologist Automating Therapeutic Target Discovery," bioRxiv 2025.06.03.657658](https://doi.org/10.1101/2025.06.03.657658).

## Other references

- [Project homepage](https://gentel-lab.github.io/OriGene-Homepage/)

## Code

[Repository](https://github.com/GENTEL-lab/OriGene) — open source under a custom (NOASSERTION) license.
