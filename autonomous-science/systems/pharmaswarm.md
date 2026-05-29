---
title: PharmaSwarm
parent: Systems
grand_parent: AI scientists
nav_order: 34
affiliation: Systems Pharmacology AI Research Center, University of Alabama at Birmingham (Song, Trotter, Chen)
lifecycle_stages: [Hypothesis, Analysis]
autonomy: Semi-autonomous
domain: Drug discovery (target identification, repurposing, lead compounds)
availability: Unknown
last_verified: 2026-05-25
---

# PharmaSwarm

Multi-agent LLM swarm for hypothesis-driven drug discovery that orchestrates specialized agents over omics, knowledge-graph, and literature data, with a central Evaluator LLM ranking proposed targets and compounds by plausibility, novelty, in-silico efficacy, and safety.

| | |
|---|---|
| **Affiliation** | Systems Pharmacology AI Research Center, University of Alabama at Birmingham ([paper](https://arxiv.org/abs/2504.17967)) |
| **First introduced** | 2025-04 (arXiv:2504.17967, dated 2025-04-24) |
| **Lifecycle stages** | Hypothesis (target / compound proposals), Analysis (mechanistic simulation, scoring, ranking) |
| **Autonomy level** | Semi-autonomous — closed-loop iteration is automated, but the system is described as an AI copilot with human review at each cycle's prioritized output |
| **Domain focus** | Drug discovery, including target identification, lead-compound suggestion, and repurposing |
| **Availability** | Unknown — paper describes the architecture and validation roadmap; no code release is referenced |

## Approach

PharmaSwarm is a three-layer architecture orchestrated via low-code workflow engines (n8n, Airflow, Prefect) or Kubernetes microservices (Argo Workflows / Kubeflow):

- **Data & Knowledge Layer.** The `getGPT` module assembles GWAS variants, DEGs, and known drug targets from Open Targets, Open Targets Genetics, and GEO. ChEMBL, DrugBank, KEGG, Reactome, the PAGER API, and a proprietary PharmAlchemy knowledge graph supply chemical, pathway, and network context. GeneTerrain Knowledge Maps (GTKMs) render expression and interaction topography.
- **LLM Agent Swarm Layer.** Three containerized agents access shared knowledge:
  - **Terrain2Drug** — omics-driven discovery, projects seed gene lists onto GTKMs, identifies network hubs.
  - **Paper2Drug** — LLM-templated literature mining for explicit and implicit target–compound pairs, validated by multi-hop traversals in PharmAlchemy.
  - **Market2Drug** — ingests FDA bulletins, ClinicalTrials.gov updates, financial feeds, and social-media sentiment to surface repurposing candidates.
- **Validation & Evaluation Layer.** A Pharmacological Efficacy and Toxicity Simulation (PETS) engine performs multiscale network propagation; an Interpretable Binding Affinity Map (iBAM) module cross-attends ESM2 protein embeddings and ChemBERTa molecular embeddings to produce affinity estimates and residue–substructure attention maps. A central **TxGemma-based Evaluator** scores proposals on empirical support, mechanistic coherence, novelty, safety, and interpretability, and sends structured feedback back to each agent for the next iteration.

A shared vector-database memory captures inter-agent context; agent submodels can be fine-tuned over time on accumulated validated insights.

## Validation

The paper is a design + retrospective work and does not report wet-lab validation. A four-tier validation pipeline is **proposed** but not executed in this preprint:

1. **Retrospective benchmarking** on classic discovery cases (idiopathic pulmonary fibrosis, triple-negative breast cancer) measured by Recall@K, Precision@K, Kendall's Tau, and MAP.
2. **Prospective in-silico assessment** with AutoDock Vina / Glide docking, 50–100 ns molecular dynamics, and ADMET prediction.
3. **Experimental evaluation** with SPR/ITC binding (Kd), cellular IC50 assays, kinase/receptor off-target panels, and rodent pilot studies.
4. **Expert user studies** measuring time-to-hypothesis and plausibility ratings versus conventional workflows.

An iBAM case study on the HSP90α–ligand complex is shown: predicted pKd 6.83 vs. experimental 6.05.

## Notable results

- Provides one of the first explicitly modular drug-discovery multi-agent designs combining omics analysis, knowledge-graph reasoning, market signals, and binding-affinity prediction under a single Evaluator-coordinated loop.
- Distinct from existing biomedical agentic systems in the catalogue (Robin, Biomni, CRISPR-GPT, PerTurboAgent) by targeting target/compound hypothesis generation across heterogeneous biomedical data.
- No wet-lab or prospective validation reported in this preprint — the four-tier pipeline is a roadmap.

## Primary paper

[Song, Trotter, Chen, "LLM Agent Swarm for Hypothesis-Driven Drug Discovery," arXiv:2504.17967](https://arxiv.org/abs/2504.17967).

## Other references

_None yet._

## Code

Not released at preprint time.
