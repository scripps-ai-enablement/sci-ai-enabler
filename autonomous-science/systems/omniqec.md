---
title: OmniQEC
parent: Systems
grand_parent: AI scientists
nav_order: 33
affiliation: Nanyang Technological University Singapore (Yuxuan Du group, College of Computing and Data Science) with Tokyo University of Agriculture and Technology, Zhejiang University of Technology, City University of Hong Kong, and Hon Hai (Foxconn) Research Institute
org_short: NTU Singapore
lifecycle_stages: [Multi-stage]
validation_type: Benchmark
autonomy: Fully autonomous
domain: Quantum computing — fault-tolerant quantum error-correcting code design
domain_group: Physical sciences
availability: Unknown — no repository or release statement in the preprint
access: Unknown
tagline: LLM-orchestrated agent that designs quantum error-correcting codes from construction through decoder-level circuit evaluation.
last_verified: 2026-08-01
---

# OmniQEC

LLM-orchestrated discovery agent that designs practical quantum error-correcting codes by optimizing circuit-level logical error rate directly, rather than the algebraic code-level proxies that earlier automated searches ranked on.

| | |
|---|---|
| **Affiliation** | Nanyang Technological University Singapore, with Tokyo University of Agriculture and Technology, Zhejiang University of Technology, City University of Hong Kong, and Hon Hai (Foxconn) Research Institute |
| **First introduced** | 2026-07 (arXiv:2607.25865) |
| **Lifecycle stages** | Multi-stage (code generation, code-level screening, syndrome-extraction synthesis, decoder-based circuit evaluation) |
| **Autonomy level** | Fully autonomous — the user supplies a design objective; the orchestrator runs the generate–evaluate–refine loop |
| **Domain focus** | Fault-tolerant quantum computing — qLDPC code–circuit–decoder co-design |
| **Availability** | Unknown — the preprint states no repository |

## Approach

A user specifies a design objective: target code family, optimization criterion, physical-qubit budget, connectivity, native gate set, and available ancilla resources. An LLM-based orchestrator translates that into a structured discovery task, maintains a self-evolving discovery memory, and routes information across a dual-loop workflow. In the **fast loop** (seconds), a generative code-search agent proposes executable code-construction programs, which are converted into candidate codes and screened by a code-characterization module on validity, logical-qubit number `k`, code distance `d`, and a figure-of-merit proxy `kd²/n`. Promising candidates are promoted to the **slow loop** (minutes to hours), where a circuit-synthesis module compiles validated codes into optimized syndrome-extraction circuits and a circuit-evaluation module estimates circuit-level logical error rates by noisy sampling with configurable decoders (BP+OSD, BP+LSD, Relay-BP). Circuit-level evidence is returned to the orchestrator, written into discovery memory, and used to refine both candidate generation and search strategy. The workflow outputs a ranked package containing reproducible construction programs, discovered codes, compiled circuits, and decoding performance.

## Validation

Systematically evaluated under a fixed total physical-qubit budget `N`, optimizing circuit-level logical error rate over complete code implementations — including ancillas and the syndrome-extraction circuit, not just the code block. The sweep covers four qLDPC construction families (lifted product, bivariate bicycle, trivariate tricycle, generalized lifted product), three LLM backends (Claude, GPT, DeepSeek), and 14 total-physical-qubit budgets per backend.

## Notable results

- Discovered codes show steadily improving logical-error suppression as the physical-qubit budget grows.
- Outperformed the bivariate-bicycle [[72, 12, 6]] and [[144, 12, 12]] codes under complete-implementation budgets of 98 and 240 physical qubits respectively.
- Discovered codes are reported as hardware-friendly under connectivity and gate-set constraints, and are offered as independently useful constructions.

## Primary paper

[Yan et al., "OmniQEC: discovering practical quantum error-correcting codes by an AI scientist," arXiv:2607.25865](https://arxiv.org/abs/2607.25865).

## Other references

_None yet._

## Code

Not released — no repository stated in the preprint.
