---
title: Dr.Sai
parent: Systems
grand_parent: AI scientists
nav_order: 12
affiliation: Institute of High Energy Physics (CAS), with University of Chinese Academy of Sciences, Jilin University, Lanzhou University, and Shanghai Jiao Tong University
lifecycle_stages: [Analysis, Experiment design]
autonomy: Semi-autonomous
domain: High-energy physics (BESIII collider experiment)
availability: Unknown
last_verified: 2026-05-21
---

# Dr.Sai

LLM-powered multi-agent system that performs autonomous end-to-end high-energy-physics data analysis on the BESIII detector, from event selection and kinematic fitting through statistical fitting and preliminary systematic uncertainty estimation.

| | |
|---|---|
| **Affiliation** | Institute of High Energy Physics, CAS, with University of Chinese Academy of Sciences, Jilin University, Lanzhou University, and Shanghai Jiao Tong University |
| **First introduced** | 2026-04 (arXiv:2604.22541) |
| **Lifecycle stages** | Analysis (event selection, kinematic fitting, signal extraction, systematic uncertainty estimation) + Experiment design (configuration-driven analysis-chain construction) |
| **Autonomy level** | Semi-autonomous — physicist defines a high-level physics goal in natural language; agents orchestrate the BESIII workflow without manual coding |
| **Domain focus** | High-energy physics — BESIII / BEPCII collider experiment |
| **Availability** | Unknown (no public repository disclosed in primary paper) |

## Approach

Built on the AutoGen framework with a Talker-Reasoner architecture. Six specialized agents — Host (router), Planner (task decomposition), Coder (code and parameter generation), Tester (remote execution), Calculator (branching-fraction computation), and Reflector (rationality validation) — coordinate through a daemon-based message manager that persists state across long-running cluster jobs (HTCondor). A specialized HEP-RAG module backed by LlamaIndex and Qdrant provides BESIII-specific corpora to the Coder agent. Two domain-narrowing mechanisms — configuration-driven code generation from standardized JSON templates and HepScript, a domain-specific language formalizing analysis logic — constrain the LLM action space. A Remote Worker bridges the agents to CERN ROOT, BOSS (BESIII Offline Software System), and a C++/Python/Shell execution environment. Backbone LLMs are Qwen3-max-2025-09-23 (complex reasoning, tool invocation) and DeepSeek-v3.1 (lightweight prompted tasks).

## Validation

Re-measured branching fractions across ten distinct J/ψ decay channels in the BESIII production-level environment. Results were in excellent agreement with Monte Carlo simulations and established physical benchmarks. A multi-dimensional performance evaluation found reflection mechanisms improved reliability, while precise tool/code synthesis and structural representation of domain expertise remained the primary bottlenecks.

## Notable results

- First named agentic AI scientist deployed inside a major collider collaboration (BESIII).
- Successfully managed full chains from event selection through statistical fitting and preliminary systematic uncertainty estimation without manual coding.
- Identified failure modes (tool-call mismatches, schema-noncompliant code generation) as bottlenecks for autonomous HEP analysis.

## Primary paper

[He et al., "Dr.Sai: An agentic AI for real-world physics analysis at BESIII," arXiv:2604.22541](https://arxiv.org/abs/2604.22541).

## Other references

_None yet._

## Code

Not released.
