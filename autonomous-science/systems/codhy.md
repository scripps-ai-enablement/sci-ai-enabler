---
title: CoDHy
parent: Systems
grand_parent: AI scientists
nav_order: 18
affiliation: Peter L. Reichertz Institute for Medical Informatics (PLRI), Hannover Medical School and Lower Saxony Center for AI and Causal Methods in Medicine (CAIMed), with Sanford Burnham Prebys Medical Discovery Institute (Younis, Basak, Chavez, Ahmadi)
org_short: Hannover Med. School
lifecycle_stages: [Hypothesis]
validation_type: Benchmark
autonomy: Assistive
domain: Biology & medicine (translational oncology; drug-combination hypothesis generation)
domain_group: Biology & medicine
availability: Open source — code on GitHub; demo models CC BY-NC-SA 4.0
access: Open source
tagline: Human-in-the-loop AI co-scientist that generates and ranks biomarker-guided cancer drug-combination hypotheses via knowledge-graph reasoning.
last_verified: 2026-07-18
---

# CoDHy

An interactive, human-in-the-loop AI co-scientist that generates, validates, and ranks biomarker-guided cancer drug-combination hypotheses via knowledge-graph reasoning grounded in retrievable biomedical evidence.

| | |
|---|---|
| **Affiliation** | Hannover Medical School (PLRI / CAIMed) with Sanford Burnham Prebys ([paper](https://arxiv.org/abs/2603.00612)) |
| **First introduced** | 2026-02 (arXiv preprint) |
| **Lifecycle stages** | Hypothesis (generates, validates, and ranks drug-combination hypotheses) |
| **Autonomy level** | Assistive — researcher-steerable web interface; positioned as decision support, not automated decision-making |
| **Domain focus** | Translational oncology (biomarker-guided drug combinations) |
| **Availability** | Open source — code on GitHub; demo models under CC BY-NC-SA 4.0 |

## Approach

CoDHy takes a user-specified focus biomarker, cancer type, and PubMed retrieval scope, then constructs a task-specific knowledge graph that integrates structured biomedical databases (Reactome, CIViC, TCGA-GDC, ClinicalTrials.gov, ChEMBL, STRING, SynlethDB, DepMap, DrugBank, and others) with entities and relations extracted from retrieved PubMed abstracts via spaCy NLP pipelines. Extracted relations are normalized against existing relation types using sentence-transformer cosine similarity to limit noisy graph growth, and the graph is stored in Neo4j AuraDB with a cache for reuse across runs.

Node2Vec embeddings enable similarity-based reasoning over the graph. A hypothesis-generation agent uses a hybrid Graph-RAG approach — retrieving a localized discovery subgraph of explicit interactions around the biomarker, then augmenting it with implicit signals from embedding similarity — to propose candidate drug combinations. A validation agent (Llama-3.1-8B-Instruct via the Hugging Face Inference API) assesses novelty, plausibility, feasibility, and safety, runs targeted PubMed searches for exact combinations, and assigns a proceed/caution/reject verdict. A ranking agent computes a composite score from a graph-evidence score plus the LLM safety score, optionally incorporating DrugCombDB synergy data. The demo is deployed on Hugging Face Spaces via Gradio.

## Validation

CoDHy is evaluated on seven frozen (biomarker, cancer type) scenarios (e.g., EGFR / Lung Squamous Cell Carcinoma), retrieving 50 PubMed abstracts and generating four hypotheses per scenario with a fixed Llama-3.1-8B model. Three variants are compared: Full CoDHy, an LLM-only prompting baseline, and a No-Node2Vec ablation. Evaluation is benchmark/in-silico only — no wet-lab testing of the proposed combinations.

Full CoDHy achieves the highest exact-novelty rate (35.71%) versus No-Node2Vec (28.57%) and LLM-only (10.71%), while maintaining high diversity (0.89) and competitive evidence coverage. On retrieval-style ranking metrics, LLM-only scores highest (MRR 0.93) by favoring already-published standard-of-care combinations, whereas Full CoDHy's lower MRR (0.74) reflects its deliberate bias toward biologically plausible but previously unpublished combinations — framed by the authors as a shift from a search-retrieval to a discovery-oriented paradigm.

## Notable results

- Highest exact novelty (35.71%) among tested variants while retaining diversity (0.89) across seven oncology scenarios.
- Distinguishes graph-supported from embedding-inferred hypotheses and attaches explicit PubMed evidence plus safety/toxicity verdicts to each candidate.
- Ablation shows both structured KG evidence and Node2Vec embedding inference contribute to balancing novelty, evidence grounding, and diversity.

## Primary paper

[Younis, Basak, Chavez, Ahmadi, "From Literature to Hypotheses: An AI Co-Scientist System for Biomarker-Guided Drug Combination Hypothesis Generation," arXiv:2603.00612 (2026)](https://arxiv.org/abs/2603.00612).

## Other references

- [Demo video](https://www.youtube.com/watch?v=Bjdp-7JJjPY)
- [Web demo (Hugging Face Spaces)](https://huggingface.co/spaces/suvinavabasak/CoDHy)

## Code

[Repository](https://github.com/baksho/CoDHy) — open source; demo models licensed CC BY-NC-SA 4.0 (non-commercial research).
