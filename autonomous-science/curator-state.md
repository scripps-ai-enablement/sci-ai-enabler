---
title: Curator state
parent: AI scientists
nav_exclude: true
---

# Curator state

## Recently surfaced

- **MLEvolve** (added 2026-06-05) — Shanghai AI Laboratory / East China Normal University LLM-based self-evolving multi-agent framework for end-to-end ML-algorithm discovery. Progressive Monte Carlo Graph Search (cross-branch reference edges + entropy-inspired exploration→exploitation schedule), Retrospective Memory (cold-start knowledge base + dynamic global experience store), and Hierarchical Planning with Adaptive Code Generation (Planner/Coder split, full-rewrite/stepwise/diff modes). Reports 65.3% average medal rate on the full 75-task MLE-Bench under a 12-hour budget (state-of-the-art) and best on 11/15 AlphaEvolve math-optimization tasks. Open source at github.com/InternScience/MLEvolve.
- **CatDT** (added 2026-06-05) — HKUST self-evolving multi-agent system that constructs an autonomous, condition-aware digital twin of a working heterogeneous catalyst (eight agents, 27 tools) in 5–30 min on a single GPU. UniMech finds dominant reaction pathways at >10³× lower cost than exhaustive enumeration; a memory-augmented reinforcement loop lifts barrier-calculation success from 41% to 84% across 600 catalytic surfaces. Validated on seven gas–solid benchmarks (every prediction within 0.5–2× experimental values); independently discovers a Ni@ZrO₂ SMSI candidate for propane dehydrogenation rivaling Pt benchmarks.
- **CategoryScienceClaw** (added 2026-06-05) — MIT (Buehler lab) self-revising discovery framework that adds a category-theoretic, proof-carrying layer to the underlying ScienceClaw agentic execution substrate. Two instantiations: Builder/Breaker (protein-mechanics MDL-gated world-model revision; accepts mode-conditioned compliance with a 54.3-bit MDL gain) and CategoryScienceClaw (fiber-network mechanics worked example with AIC gate accepting an orientation-tensor anisotropic stiffness surrogate over an isotropic fiber-count descriptor). Code at github.com/lamm-mit/scienceclaw and the categoryscienceclaw-mechanics branch.
- **AgentPLM** (added 2026-06-05) — Bedford College, London with Saarland University agentic protein language model that interleaves autoregressive sequence generation with tool calls (ESMFold, FoldX, AutoDock Vina) under Reasoning-Augmented Decoding, trained end-to-end via Contrastive Agent Policy Optimisation (a trajectory-level extension of DPO) to learn when oracle feedback is informative. ICML 2026. Reports 2.79× improvement in antibody top-10% hit rate and +34% normalised k_cat/K_M on enzyme design.
- **AutoSci** (added 2026-06-02) — Peking University (PKUDAIR) memory-centric agentic system for the full scientific research lifecycle. Four modules (SciMem schema-governed memory, SciFlow harness-based five-stage executor with 30+ skills, SciDAG DAG-shaped multi-agent operators, SciEvolve versioned self-evolution) and a Trust Guard on all memory writes. Two end-to-end case studies in GPU kernel optimization (6.3/10 automated ICLR-review) and biomedical drug discovery (5.8/10). Open source at github.com/skyllwt/AutoSci.

## Flagged for review

_None._

## Deferred — next-run priority

- **CORAL** (arXiv:2604.01658, Apr 2026) — Multi-agent evolutionary discovery framework from MIT/NUS/Singapore-MIT. PDF archived at `sources/2604.01658v1.pdf`; reported on Anthropic's kernel-engineering task and Polyominoes packing, not strictly natural-science hypothesis generation. Add when a more science-leaning evaluation surfaces.
- **AIDO.Harness** (bioRxiv 2026.04.20.719735) — Autonomous ML-model construction for biomedical tasks, framed as POMDP. Not downloaded; revisit next pass.
- **SAGA** (arXiv:2512.21782) — Goal-evolving autonomous discovery agent. Not downloaded; verify scope.
- **Virtual Lab** (Stanford / CZ Biohub, *Nature* 2025) — referenced in Kosmos and AgenticSciML papers; PDF blocked by Cloudflare on prior run.
- **ScienceClaw × Infinite** (arXiv:2603.14312, Mar 2026) — Underlying agentic execution substrate cited as foundation by the new CategoryScienceClaw paper. Currently captured as a reference inside the CategoryScienceClaw entry; consider promoting to its own page when a more complete characterization is available.
