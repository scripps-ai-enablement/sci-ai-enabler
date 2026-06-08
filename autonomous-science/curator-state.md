---
title: Curator state
parent: AI scientists
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Ax-Prover** (added 2026-06-08) — Axiomatic AI (with ICFO, MIT, ICREA) multi-agent Lean theorem-proving framework that equips general-purpose LLMs (Claude Sonnet 4/4.5) with Lean tools via MCP. Orchestrator/Prover/Verifier loop sketches, formalizes, and machine-verifies proofs across mathematics and quantum physics, running autonomously or collaboratively with experts. Top open-source model and third overall on PutnamBench (14%); 96% on the authors' new QuantumTheorems benchmark and 64% on AbstractAlgebra, outperforming specialized provers (DeepSeek-Prover, Kimina). Two cryptography case studies with domain experts. Open source (arXiv:2510.12787).
- **SAGA** (added 2026-06-07) — multi-institution (Cornell, OSU, Yale, EPFL, UC Berkeley, Northeastern, Broad Institute, Deep Principle, and others) bi-level Scientific Autonomous Goal-evolving Agent. Outer loop (Planner proposes objectives → Implementer compiles them into executable scoring functions → Optimizer searches candidates → Analyzer diagnoses failure modes) evolves the objective functions of a design problem; inner loop optimizes candidates under current objectives. Runs co-pilot/semi-pilot/autopilot. Validated across five domains (antibiotics, nanobodies, functional DNA, inorganic materials, chemical processes) with wet-lab hits: a structurally novel antibiotic (Tanimoto >0.7 from known antibiotics) active against E. coli with no human cytotoxicity, and three de novo PD-L1 nanobody binders (K_D 300–400 nM). Open source under MIT (github.com/btyu/SAGA).
- **OriGene** (added 2026-06-06) — Shanghai Jiao Tong University (GENTEL Lab) self-evolving multi-agent "virtual disease biologist" automating therapeutic-target discovery. Integrates 600+ tools via a Model Context Protocol with a knowledge-graph Tool RAG and a self-evolving feedback loop; reasons across genomics, protein networks, pharmacology, clinical records, and literature to generate and prioritize target hypotheses. Reported to outperform human experts and SOTA LLMs on the 1,921-pair TRQA benchmark; wet-lab validated two nominated targets (GPR160 for liver cancer, ARG2 for colorectal cancer) in patient-derived organoid and tumor-fragment models. Open source at github.com/GENTEL-lab/OriGene.
- **MLEvolve** (added 2026-06-05) — Shanghai AI Laboratory / East China Normal University LLM-based self-evolving multi-agent framework for end-to-end ML-algorithm discovery. Progressive Monte Carlo Graph Search (cross-branch reference edges + entropy-inspired exploration→exploitation schedule), Retrospective Memory (cold-start knowledge base + dynamic global experience store), and Hierarchical Planning with Adaptive Code Generation (Planner/Coder split, full-rewrite/stepwise/diff modes). Reports 65.3% average medal rate on the full 75-task MLE-Bench under a 12-hour budget (state-of-the-art) and best on 11/15 AlphaEvolve math-optimization tasks. Open source at github.com/InternScience/MLEvolve.
- **CatDT** (added 2026-06-05) — HKUST self-evolving multi-agent system that constructs an autonomous, condition-aware digital twin of a working heterogeneous catalyst (eight agents, 27 tools) in 5–30 min on a single GPU. UniMech finds dominant reaction pathways at >10³× lower cost than exhaustive enumeration; a memory-augmented reinforcement loop lifts barrier-calculation success from 41% to 84% across 600 catalytic surfaces. Validated on seven gas–solid benchmarks (every prediction within 0.5–2× experimental values); independently discovers a Ni@ZrO₂ SMSI candidate for propane dehydrogenation rivaling Pt benchmarks.

## Flagged for review

_None._

## Deferred — next-run priority

- **Numina-Lean-Agent** (arXiv:2601.14027, Jan 2026; Project Numina et al.) — PDF archived this run (`sources/2601.14027.pdf`/`.txt`) and logged in the manifest. Agentic Lean theorem-proving framework (Claude Code + Numina-Lean-MCP on Claude Opus 4.5) that solves given theorems (Putnam 2025 12/12; formalizes Brascamp–Lieb); released at github.com/project-numina/numina-lean-agent. Scope-edge case: a purer prover of stated theorems with no hypothesis generation, experiment design, or scientific data analysis — closer to a prover tool than an autonomous scientist. Add only if a stronger "does-science" case emerges.
- **AutoDiscovery** (Ai2 / AstaLabs) — surfaced as a secondary lead on 2026-06-06 but could not be investigated this run (WebFetch returned a model 404). Revisit next pass to confirm scope and gather a citable source.
- **CORAL** (arXiv:2604.01658, Apr 2026) — Multi-agent evolutionary discovery framework from MIT/NUS/Singapore-MIT. PDF archived at `sources/2604.01658v1.pdf`; reported on Anthropic's kernel-engineering task and Polyominoes packing, not strictly natural-science hypothesis generation. Add when a more science-leaning evaluation surfaces.
- **AIDO.Harness** (bioRxiv 2026.04.20.719735) — Autonomous ML-model construction for biomedical tasks, framed as POMDP. Not downloaded; revisit next pass.
- **Virtual Lab** (Stanford / CZ Biohub, *Nature* 2025) — referenced in Kosmos and AgenticSciML papers; PDF blocked by Cloudflare on prior run.
- **ScienceClaw × Infinite** (arXiv:2603.14312, Mar 2026) — Underlying agentic execution substrate cited as foundation by the new CategoryScienceClaw paper. Currently captured as a reference inside the CategoryScienceClaw entry; consider promoting to its own page when a more complete characterization is available.
