---
title: SPARK
parent: Systems
grand_parent: AI scientists
nav_order: 27
affiliation: University Hospital Cologne and collaborators (Tolkach group)
lifecycle_stages: [Multi-stage]
autonomy: Fully autonomous
domain: Biology / cancer pathology
availability: Open source
last_verified: 2026-05-22
---

# SPARK

System of Pathology Agents for Research and Knowledge — an agentic framework that autonomously generates biologically driven concepts, codes them into analytical tools, and applies them to H&E and spatial-biology data across five cancer types.

| | |
|---|---|
| **Affiliation** | University Hospital Cologne, Martin Luther University Halle-Wittenberg, University Hospital Essen, University Hospital Giessen, and collaborators (corresponding: Yuri Tolkach) |
| **First introduced** | 2026-03 (accepted *Nature Medicine*; received 2025-09-02, accepted 2026-03-19) |
| **Lifecycle stages** | Multi-stage (idea generation, idea refinement, idea/parameter coding, parameter verification) |
| **Autonomy level** | Fully autonomous in the discovery loop, with an interactive module for clinician-driven queries |
| **Domain focus** | Computational cancer pathology — H&E whole-slide imaging and multiplexed spatial biology |
| **Availability** | Open source — code, parameters and results released ([GitHub](https://github.com/cpath-ukk/SPARK)) |

## Approach

Four linked modules use language as the universal interface between agents: an Idea Generation Agent (OpenAI o1 reasoning model, Jan–Feb 2025) proposes tumor-analysis concepts under varying creativity levels; an Idea Refinement Agent and Duplicate Detector filter and consolidate; an Idea Coding Agent (Claude Sonnet) converts concepts into executable Python parameters with up to three implementation attempts and Code Review feedback; and a Parameter Verification Agent screens for biases and instability. SPARK ingests routine H&E whole-slide images preprocessed by tissue segmentation and single-cell detection/classification across seven cell types (tumor, fibroblasts, macrophages, lymphocytes, neutrophils, eosinophils, plasma cells), then runs the agent-generated parameters case-wide and aggregates per-slide outputs to case level.

## Validation

Evaluated across 18 patient cohorts and more than 5,400 patients in five cancer types — lung adenocarcinoma, lung squamous cell carcinoma, colorectal, breast, and oropharyngeal squamous cell carcinoma — in both prognostic and predictive settings, plus a multiplexed spatial-biology breast-cancer dataset (n = 625). Parameters were correlated against histologic grade, pN stage, established biomarkers, and clinical follow-up.

## Notable results

- 99.2% of LLM-proposed parameters compiled to executable code; after quality filtering, 475 ideas yielded 1,115 non-redundant parameters from an initial 2,368 coded.
- Discovered parameters correlated with prognosis and predictive biomarkers across all five tumor types, and inferred patterns of tumor progression and temporal change from static H&E images.
- Open-source LLM alternatives (general and medical-domain) were shown to be viable substitutes for both idea generation and parameter coding.

## Primary paper

[Trost, Zhang, Aring et al., "An agentic framework for autonomous scientific discovery in cancer pathology" (SPARK), *Nature Medicine* (2026)](https://doi.org/10.1038/s41591-026-04357-y).

## Other references

_None yet._

## Code

[github.com/cpath-ukk/SPARK](https://github.com/cpath-ukk/SPARK) — full agentic pipeline and coded parameter library.
