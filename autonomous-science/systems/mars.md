---
title: MARS
parent: Systems
grand_parent: AI scientists
nav_order: 27
affiliation: Shenzhen Institutes of Advanced Technology (Chinese Academy of Sciences), with City University of Hong Kong, National University of Singapore, and Chongqing University of Posts and Telecommunications
lifecycle_stages: [Multi-stage]
autonomy: Fully autonomous
domain: Materials / chemistry (perovskites)
availability: Open source
last_verified: 2026-05-21
---

# MARS

Hierarchical multi-agent and robotic framework that pairs 19 LLM agents and 16 domain tools with a robotic synthesis platform to autonomously design, synthesize, and optimize perovskite materials.

| | |
|---|---|
| **Affiliation** | Materials Artificial Intelligence Center, Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences (Yu Xue-Feng group), with collaborators at CityU Hong Kong, NUS, and Chongqing University of Posts and Telecommunications |
| **First introduced** | 2026-02 (*Matter* 9, 102577) |
| **Lifecycle stages** | Multi-stage (literature review + materials design + synthesis planning + robotic execution + analysis) |
| **Autonomy level** | Fully autonomous within the perovskite synthesis loop; supports natural-language interaction and expert intervention via the orchestrator |
| **Domain focus** | Materials science / chemistry — perovskite nanocrystal synthesis and water-stable perovskite composites |
| **Availability** | Open source — [tangger2000/MARS](https://github.com/tangger2000/MARS) |

## Approach

Five functional groups mirror a human research team:

- **Orchestrator (G1)** — central coordinator; receives user requests, plans sub-tasks, dispatches work to administrator agents inside each group, and aggregates results.
- **Scientist (G2)** — handles literature review and design proposals using a hybrid retrieval-augmented generation strategy (GraphRAG over a customized knowledge base) intended to reduce LLM hallucination.
- **Engineer (G3)** — translates scientific proposals into executable protocols; a structural engineer emits standardized JSON schemas, a software engineer generates code, and a code reviewer checks for safety.
- **Executor (G4)** — drives a robotic workstation and mobile-robot controller to perform synthesis and characterization.
- **Analyst (G5)** — analyzes experimental results, generates refinement strategies, and feeds them back to the Orchestrator for the next iteration.

The system is built on Microsoft AutoGen with Selector Group Chat and Swarm coordination, runs GPT-4o as the foundation model, and isolates code execution in Docker containers.

## Validation

End-to-end experimental demonstration in perovskite nanocrystal chemistry. MARS optimized a synthesis protocol within 10 iterations and designed a biomimetic "core-shell-corona" structure for a water-stable perovskite composite in 3.5 hours of system time, compared with the 4–6 months the authors report for the conventional manual route — a claimed ~60× acceleration.

## Notable results

- Closed-loop perovskite synthesis optimization in 10 robotic iterations.
- Cross-domain knowledge integration produced a biomimetic perovskite composite design inspired by cell-membrane structure.
- Reports reproducibility and safety affordances via open-source release and sandboxed code execution.

## Primary paper

[Shi et al., "Knowledge-driven autonomous materials research via collaborative multi-agent and robotic system," *Matter* 9, 102577 (2026)](https://doi.org/10.1016/j.matt.2025.102577).

## Other references

_None yet._

## Code

[tangger2000/MARS](https://github.com/tangger2000/MARS) — core MARS implementation; built on [microsoft/autogen](https://github.com/microsoft/autogen).
