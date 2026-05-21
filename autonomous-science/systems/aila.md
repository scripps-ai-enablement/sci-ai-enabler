---
title: AILA
parent: Systems
grand_parent: AI scientists
nav_order: 3
affiliation: Indian Institute of Technology Delhi, with Aalborg University, Leibniz Institute of Photonic Technology, and University of Jena
lifecycle_stages: [Experiment design, Analysis]
autonomy: Semi-autonomous
domain: Materials / scanning-probe microscopy
availability: Open source
last_verified: 2026-05-21
---

# AILA

Multi-agent LLM framework that autonomously operates an atomic force microscope, paired with AFMBench, a 100-task evaluation suite spanning experimental design through results analysis.

| | |
|---|---|
| **Affiliation** | Indian Institute of Technology Delhi (M3RG group), with collaborators at Aalborg University, the Leibniz Institute of Photonic Technology, and the University of Jena ([M3RG-IITD](https://github.com/M3RG-IITD)) |
| **First introduced** | 2025-09 (*Nature Communications* 16:9104) |
| **Lifecycle stages** | Experiment design + Analysis (AFM workflow planning, instrument control, data interpretation) |
| **Autonomy level** | Semi-autonomous (natural-language goals from the user; agents plan, execute, and analyze) |
| **Domain focus** | Materials science / scanning-probe microscopy |
| **Availability** | Open source — [M3RG-IITD/AILA](https://github.com/M3RG-IITD/AILA) under CC BY 4.0 |

## Approach

An LLM-powered planner sits at the core and dispatches tasks to specialized agents. Two domain agents anchor the system: an AFM Handler Agent that performs calibration, mode selection, scan-parameter selection, and instrument control via tool calls, and a Data Handler Agent that performs baseline correction, feature detection, and mechanical-property analysis on AFM outputs. The architecture is modular so additional instruments and analytical tools can be wired in.

Alongside AILA the authors release **AFMBench**, a 100-task benchmark covering experimental workflow design, multi-tool coordination, decision-making, open-ended experiments, and data analysis. They evaluate GPT-4o, GPT-3.5, Claude-3.5-Sonnet, and Llama-3.3 in both single-agent and multi-agent configurations.

## Validation

AFMBench is the primary harness. Five real-world experiments validate AILA end-to-end: identification and analysis of an indentation mark on glass (including indenter-type inference), detection of graphene flakes on silicon and layer counting, automated microscope calibration, high-resolution imaging of graphene step edges, and load-dependent friction characterization on HOPG.

## Notable results

- Multi-agent configurations significantly outperform single-agent ones on AFMBench; sensitivity to prompt formatting persists in both.
- Materials-science question-answering proficiency does not transfer to laboratory operation — models that score well on materials QA can fail at instrument control.
- Documents an "agent sleepwalking" failure mode in which agents deviate from supplied instructions, with explicit safety implications for self-driving laboratories.

## Primary paper

[Mandal et al., "Evaluating large language model agents for automation of atomic force microscopy," *Nature Communications* 16:9104 (2025)](https://doi.org/10.1038/s41467-025-64105-7).

## Other references

_None yet._

## Code

[M3RG-IITD/AILA](https://github.com/M3RG-IITD/AILA) — includes AFMBench tasks and AILA implementation.
