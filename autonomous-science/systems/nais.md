---
title: NAIS (NVAITC AI Scientist)
parent: Systems
grand_parent: AI scientists
nav_order: 31
affiliation: NVIDIA AI Technology Center (NVAITC) with China Medical University Hospital Taichung, China Medical University, Asia University, and the RIKEN Center for Integrative Medical Sciences
org_short: NVIDIA
lifecycle_stages: [Multi-stage, Writing]
validation_type: Wet-lab
autonomy: Semi-autonomous
domain: Biomedical research — statistical genetics and hospital-scale GWAS on protected genotype and EHR data
domain_group: Biology & medicine
availability: Unknown — no repository or release statement in the preprint
access: Unknown
tagline: Governed end-to-end agentic research system that runs biomedical workflows inside institutional privacy boundaries.
last_verified: 2026-08-01
---

# NAIS (NVAITC AI Scientist)

Governed end-to-end agentic research system that plans, routes, and orchestrates biomedical workflows while protected patient data stay inside institutional privacy boundaries, validated on a hospital-scale hypertension GWAS.

| | |
|---|---|
| **Affiliation** | NVIDIA AI Technology Center, with China Medical University Hospital (Taichung), China Medical University, Asia University, and RIKEN IMS |
| **First introduced** | 2026-07 (arXiv:2607.11084) |
| **Lifecycle stages** | Multi-stage (proposal review, execution planning, workflow orchestration, evidence generation) with manuscript drafting as a downstream step |
| **Autonomy level** | Semi-autonomous — scientist-in-the-loop oversight is architectural, not optional |
| **Domain focus** | Institutional biomedical research — GWAS on hospital-linked genotype and EHR data; drug-induced liver injury prediction as a secondary workflow |
| **Availability** | Unknown — no repository stated in the preprint |

## Approach

NAIS combines durable research state, proposal-level planning, agentic execution, brokered data access, reproducible workflow orchestration, evidence tracking, and scientist-in-the-loop oversight. The governance design is the contribution: rather than granting an agent unrestricted access to protected data, NAIS separates reasoning and orchestration from data governance. The agent submits approved actions through controlled interfaces, protected records remain inside institutional infrastructure, and only governed artifacts — aggregate summaries, quality-control metrics, plots, logs, and manuscript-oriented evidence — are returned. NemoClaw, the agentic execution component, plans cohort extraction, submits governed analysis specifications, orchestrates PLINK2 GWAS workflows through brokered Kubeflow execution, retrieves aggregate artifacts, and drafts manuscript sections.

## Validation

Primary validation is a real-world hypertension GWAS on hospital-linked genotype and EHR data from the China Medical University Hospital HiGenome Genomic Bank, covering 286,422 individuals under an aggregate-only data policy. Agent-derived phenotype labels were compared systematically against independently curated expert analyses. That comparison surfaced phenotype discrepancies — blood-pressure measurements, diagnosis codes, and medication records yield different hypertension labels — and drove iterative, team-directed refinement of the hypertension definition before the final run.

## Notable results

- After team-directed reconciliation, the agent-orchestrated GWAS reproduced established hypertension-associated loci including FGF5, ATP2B1, CNNM2, FTO, and GRB14, with the strongest signal at FGF5 reaching −log₁₀ p ≈ 70.
- Secondary demonstration beyond GWAS: a drug-induced liver injury prediction workflow reaching AUC 0.842 with a multimodal graph neural network.
- The human–AI review step is reported as necessary rather than incidental — unconstrained autonomy would have propagated the initial phenotype discrepancy into the association results.

## Primary paper

[Huang et al., "NVAITC AI Scientist: A Governed End-to-End Research System — A Hypertension GWAS Case Study," arXiv:2607.11084](https://arxiv.org/abs/2607.11084).

## Other references

_None yet._

## Code

Unknown — no repository stated in the preprint.
