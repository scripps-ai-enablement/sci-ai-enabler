---
title: Talk2QSP
parent: Systems
grand_parent: AI scientists
nav_order: 10
affiliation: Sanofi and bmedx
lifecycle_stages: [Experiment design]
autonomy: Assistive
domain: Quantitative Systems Pharmacology / kinetic ODE modelling
availability: Closed
last_verified: 2026-05-20
---

# Talk2QSP

Agent-based framework that converts unstructured literature descriptions of clinical or preclinical scenarios into executable QSP/SBML model interventions, with dynamic human-in-the-loop ambiguity resolution.

| | |
|---|---|
| **Affiliation** | Sanofi and bmedx ([Sanofi](https://www.sanofi.com/)) |
| **First introduced** | 2026-05 (bioRxiv preprint v2) |
| **Lifecycle stages** | Experiment design |
| **Autonomy level** | Assistive (human-in-the-loop, dynamic HITL strategy) |
| **Domain focus** | Quantitative Systems Pharmacology (QSP) / kinetic ODE modelling |
| **Availability** | Closed (no public access announced in the preprint) |

## Approach

Combines semantic grounding of model entities, an LLM Scenario Extractor, and a dual-agent Scenario Mapper that issues discrete verifiable "work orders". Humans resolve biological ambiguities interactively.

## Validation

Seven subject-matter-expert-curated literature scenarios applied across four ODE/QSP models. All selected scenarios resolved into correct executable parameter changes, including multi-dose interventions, unit conversions, no-op scenarios, and ambiguity-triggered HITL cases.

## Notable results

7/7 SME-curated scenarios resolved correctly. Outperformed standalone SBML-reasoning LLM calls and prior agentic efforts on processed SBML data (per preprint claim).

## Primary paper

[Kazemeini et al., "Talk2QSP: Deriving Executable Scenarios from Unstructured Literature via Human-in-the-Loop Agents," bioRxiv 2026.05.06.723244](https://doi.org/10.64898/2026.05.06.723244).

## Code

Not released.
