---
title: AI scientist updates
parent: Updates
nav_order: 3
permalink: /updates/ai-scientists.html
---

# AI scientist updates

Reverse-chronological log of changes to the [AI scientists tracker](autonomous-science/). Newest at the top.

## 2026-06-10

### Added
- **DarkAgents** (Lifecycle: Multi-stage) — Università di Bologna / INFN language-driven multi-agent system for theoretical astroparticle physics (TAP), and the first end-to-end architecture targeting that domain. An orchestrator interprets a particle-physics model or looser "idea," selects a pipeline branch, writes an execution plan, and dispatches specialized sub-agents (proposal, librarian, critic, plus deterministic compute stages) that each emit a Markdown report and a fixed-schema JSON handoff it checks before proceeding; it pauses for human audit after each step by default but can run fully autonomous. All physical quantities come from deterministic human-validated code to curb hallucination, and the workflow is LLM-agnostic (Mistral, Anthropic/Claude Code, OpenAI/Codex, local Ollama). The first implementation, **DarkAgent-PT**, takes a classically scale-invariant model to a `PTArcade` MCMC fit of the NANOGrav nanohertz gravitational-wave background, then adds a constraint sub-agent and an assumption/prior-auditing sub-agent. Validation: reproduced human Bayesian posteriors across providers (Claude Code Opus 4.8 and Codex GPT-5.5 ran almost autonomously), **identified inconsistencies in some published fits and produced novel fits on the dissipative bulk-flow GW template**, and correctly rejected the sound-wave template where invalid; a noted failure mode is hallucinated references in the final report. Open source ([source](https://arxiv.org/abs/2606.11157)).

### Updated
- **`autonomous-science/summary.md`** — added the DarkAgents primary-paper link to Sources; re-verified every synthesis claim against the current grouping and bumped `synthesis_reviewed` to 2026-06-10. DarkAgents fits the existing "Physical sciences are the newest frontier" pattern (alongside Dr.Sai and CMBEvolve/CosmoEvolve as in-silico TAP/cosmology work, not embodied apparatus) and tips no superlative, so no synthesis prose was rewritten.
- **`autonomous-science/curator-state.md`** — added DarkAgents at the top of `Recently surfaced` (trimming MLEvolve to keep the window at five).
- **`sources/manifest.json`** — DarkAgents (DOI 10.48550/arXiv.2606.11157) entry added by Phase A.

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages remain inside the 30-day re-verification window (most recent additions verified 2026-06-05 through 2026-06-09); no spot-checks required this run.

## 2026-06-09

### Added
- **LabOS** (Lifecycle: Multi-stage) — Stanford / Princeton AI-XR co-scientist (with Oregon State, U. Washington, NVIDIA) that couples a self-evolving multi-agent digital-lab system with extended-reality smart glasses, a lab-specialized vision-language model, 3D/4D digital twins, and a cobot module to perceive, reason about, and assist in the physical laboratory. The dry-lab module extends the **STELLA** framework (Manager/Planner, Developer, Critic agents plus a Tool-Creation agent feeding a shared "Tool Ocean") for hypothesis generation, experiment design, and analysis; the wet-lab module streams egocentric video to **LabOS-VLM** (Qwen-VL post-trained via SFT + GRPO) for real-time action verification, error detection, and step guidance. Benchmarks: **~32% HLE: Biomedicine, 61% LAB-Bench: DBQA, 65% LAB-Bench: LitQA** (up to 8% over next-best), plus a new **LabSuperVision (LSV)** lab-video benchmark on which LabOS-VLM-235B exceeds 90% error-detection accuracy, beating Claude Opus-4.1, GPT-5, and Gemini 2.5 Pro. Wet-lab: agent-nominated **CEACAM6** confirmed as an NK-cell anti-tumor target in a physical killing assay; **ITSN1** identified as a cell-fusion regulator. Open source ([source](https://arxiv.org/abs/2510.14861)).

### Updated
- **`autonomous-science/summary.md`** — added the LabOS primary-paper link to Sources. LabOS fits the existing "Biology & medicine carry the strongest evidence" and embodied-systems patterns and tips no superlative; `synthesis_reviewed` was refreshed yesterday (2026-06-08, within the 30-day window), so no synthesis prose was rewritten.
- **`autonomous-science/curator-state.md`** — added LabOS at the top of `Recently surfaced` (trimming CatDT to keep the window at five).
- **`sources/manifest.json`** — LabOS (DOI 10.48550/arXiv.2510.14861) entry added by Phase A.

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages remain inside the 30-day re-verification window (oldest `last_verified` is 2026-05-20); no spot-checks required this run.

## 2026-06-08

### Added
- **Ax-Prover** (Lifecycle: Analysis) — Axiomatic AI (with ICFO, MIT, ICREA) multi-agent framework that equips general-purpose LLMs (Claude Sonnet 4/4.5) with Lean theorem-proving tools via the Model Context Protocol, generating formally verified proofs across mathematics and quantum physics either autonomously or in collaboration with domain experts. A role-specialized **Orchestrator / Prover / Verifier** loop sketches proofs, formalizes each step into Lean `have` statements, and machine-checks them with `lean-lsp-mcp` tools (goal inspection, Mathlib search via Loogle/Leansearch, diagnostics) — sidestepping the over-specialization and Mathlib-version brittleness of distilled prover models. Benchmarked at pass@1 against frontier-LLM and specialized-prover baselines: **top open-source model and third overall on PutnamBench (14%, 92/660 problems)**, **96% on the authors' new QuantumTheorems benchmark** (vs. 61% DeepSeek-Prover, 57% Kimina) and **64% on AbstractAlgebra**, plus two cryptography case studies (matrix branch-number definition; QKD entropy bound) formalized with domain experts. Open source ([source](https://arxiv.org/abs/2510.12787)).

### Updated
- **`autonomous-science/summary.md`** — added Ax-Prover to the "long tail of single-domain pioneers" mathematics exemplars (formal Lean proving alongside AI co-mathematician); re-verified every synthesis claim against the current grouping and bumped `synthesis_reviewed` to 2026-06-08. Ax-Prover fits the existing Math & symbolic pattern and tips no superlative, so no synthesis prose was rewritten.
- **`autonomous-science/curator-state.md`** — added Ax-Prover at the top of `Recently surfaced` (trimming CategoryScienceClaw to keep the window at five); recorded **Numina-Lean-Agent** (arXiv:2601.14027) under `Deferred — next-run priority` as a scope-edge pure theorem prover.
- **`sources/manifest.json`** — Ax-Prover (DOI 10.48550/arXiv.2510.12787) and the deferred Numina-Lean-Agent (DOI 10.48550/arXiv.2601.14027) entries added by Phase A.

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages remain inside the 30-day re-verification window (oldest `last_verified` is 2026-05-20); no spot-checks required this run.

## 2026-06-07

### Added
- **SAGA** (Lifecycle: Multi-stage) — Scientific Autonomous Goal-evolving Agent, a multi-institution collaboration (Cornell, Ohio State, Yale, Simon Fraser, EPFL, UC Berkeley, Northeastern, Broad Institute, MIT, Deep Principle, Georgia Tech, and others) whose distinctive contribution is **automating objective-function design** — evolving *what to optimize for* rather than treating objectives as fixed inputs. A **bi-level architecture** pairs an **outer loop** of four LLM agents — a **Planner** that proposes new objectives from the goal and current progress, an **Implementer** that compiles objectives into executable scoring functions (e.g., RDKit-based scorers), an **Optimizer** that searches candidate hypotheses under the current objectives, and an **Analyzer** that diagnoses optimization failure modes — with an **inner loop** that runs any optimization strategy (genetic algorithms, RL search) to evolve candidates. It runs in **co-pilot**, **semi-pilot**, and **autopilot** modes. Demonstrated across five design domains (antibiotics, nanobodies, functional DNA sequences, inorganic materials, chemical-process flowsheets) with genuine wet-lab validation: a **structurally novel antibiotic hit** (Tanimoto distance >0.7 from all known antibiotics) with experimentally confirmed activity against *E. coli* and no human cytotoxicity, and **three de novo PD-L1 nanobody binders** (K_D 300–400 nM) where the autonomously evolved composite scorer separated binders from non-binders (p = 0.03) but no single in-silico metric did. Open source under MIT ([source](https://arxiv.org/abs/2512.21782)).

### Updated
- **`autonomous-science/summary.md`** — appended the SAGA source citation; re-verified every synthesis claim against the current grouping and bumped `synthesis_reviewed` to 2026-06-07. SAGA fits the existing General/multi-domain and wet-lab-evidence patterns (an objective-evolving cousin of DKPL) and reinforces but does not tip any superlative, so no synthesis prose was rewritten.
- **`autonomous-science/curator-state.md`** — added SAGA at the top of `Recently surfaced` (trimming AgentPLM to keep the window at five) and removed the now-promoted SAGA entry from `Deferred — next-run priority`.
- **`sources/manifest.json`** — SAGA entry (DOI 10.48550/arXiv.2512.21782) added by Phase A.

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages remain inside the 30-day re-verification window; no spot-checks required this run.

## 2026-06-06

### Added
- **OriGene** (Lifecycle: Hypothesis, Analysis) — Shanghai Jiao Tong University (Global Institute of Future Technology, GENTEL Lab; corresponding author Shuangjia Zheng) self-evolving multi-agent system framed as a **"virtual disease biologist"** that autonomously generates and prioritizes mechanistically grounded **therapeutic-target hypotheses**. It integrates **600+ specialized tools** and curated biomedical databases through a **Model Context Protocol (MCP)**, reasoning across genomics, protein networks, pharmacology, clinical records, and literature; a **knowledge-graph-based Tool RAG** plus an agent-selection mechanism drives dynamic, context-aware tool deployment, and a **self-evolving feedback loop** iteratively refines the system's thinking templates, tool composition, and analytical protocols from human and experimental feedback. On **TRQA**, an original 1,921-pair expert benchmark (TRQA-lit: 172 multiple-choice + 1,108 short-answer; TRQA-db: 641 short-answer), OriGene is reported to outperform human experts, leading research agents, and SOTA LLMs on accuracy, recall, and robustness — particularly under data sparsity or noise. Critically, it nominated two previously underexplored targets — **GPR160 (liver cancer)** and **ARG2 (colorectal cancer)** — both of which showed significant **anti-tumor activity in patient-derived organoid and tumor-fragment models** mirroring human clinical exposures. Open source at github.com/GENTEL-lab/OriGene ([source](https://doi.org/10.1101/2025.06.03.657658)).

### Updated
- **`autonomous-science/summary.md`** — added OriGene to the "Biology and medicine carry the strongest evidence" exemplar list (agent-nominated cancer targets confirmed in patient-derived organoid models); bumped `synthesis_reviewed` to 2026-06-06 after re-verifying every synthesis claim against the current grouping (all still hold — OriGene reinforces, but does not tip, the biology-medicine evidence superlative).
- **`autonomous-science/curator-state.md`** — added OriGene at the top of `Recently surfaced` (trimming AutoSci to keep the window at five); added **AutoDiscovery** (Ai2 / AstaLabs) to `Deferred — next-run priority` as a secondary lead that could not be investigated this run.
- **`sources/manifest.json`** — OriGene entry (DOI 10.1101/2025.06.03.657658) added by Phase A; bioRxiv PDF/JATS Cloudflare-blocked, so the sidecar was assembled from the bioRxiv API abstract, project homepage, and GitHub repo metadata.

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 or later — inside the 30-day re-verification window. No spot-checks required this run.

## 2026-06-05

### Added
- **MLEvolve** (Lifecycle: Multi-stage) — Shanghai Artificial Intelligence Laboratory with East China Normal University LLM-based self-evolving multi-agent framework for **end-to-end machine-learning algorithm discovery**. It targets three limitations of prior MLE agents — inter-branch information isolation, memoryless search, and one-shot generation — through three components: **Progressive Monte Carlo Graph Search** (graph-based cross-branch reference edges plus an entropy-inspired schedule that shifts the search from broad exploration to focused exploitation over time), **Retrospective Memory** (a cold-start domain knowledge base paired with a dynamic global experience store that auto-accumulates and retrieves task-specific records, rather than propagating scalar rewards alone), and **Hierarchical Planning with Adaptive Code Generation** (a Planner/Coder split that selects among full-rewrite, stepwise, and diff editing modes by search state). With a Gemini-3.1-Pro-preview backbone (500 expansion steps, 12-hour runtime, single H200), it reports a **65.3% average medal rate** (34.7% gold, 100% valid submission, 76.0% above-median; 80.3/64.0/46.7% on low/medium/high complexity) on the full 75-task MLE-Bench under a 12-hour budget — half the standard 24-hour runtime — claimed state-of-the-art over open-source (AIDE, R&D-Agent, ML-Master, AIRA-Dojo, Leeroo, ML-Master 2.0) and proprietary (FM-Agent, MLE-STAR-Pro-1.5, MARS, MARS+, AIBuildAI) agents, and best on **11 of 15** AlphaEvolve mathematical-optimization tasks (vs AlphaEvolve, AlphaEvolve-v2, SimpleTES, TTT-Discover, OpenEvolve), evidence of cross-domain generalization. Ablations on MLE-Bench Lite show removing Progressive MCGS causes the largest medal-rate drop and removing Retrospective Memory drops medal rate by 13.64%. Open source at github.com/InternScience/MLEvolve ([source](https://arxiv.org/abs/2606.06473)).
- **CatDT** (Lifecycle: Multi-stage) — HKUST (IAS Center for AI for Scientific Discoveries) self-evolving multi-agent system that constructs an autonomous, condition-aware **digital twin of a working heterogeneous catalyst** from only a bulk crystal and a natural-language reaction description. Eight specialized agents and 27 scientific tools predict stable facets, reconstruct surfaces under operating conditions, enumerate and rank reaction pathways, locate transition states, and compute kinetics in **5–30 min on a single GPU**. Two innovations target the hardest steps: **UniMech** fuses agent-guided proposals with energy-cached graph search over autonomously constructed reaction networks, finding dominant pathways at **>10³× lower cost** than exhaustive enumeration; a **memory-augmented reinforcement loop** lifts barrier-calculation success from **41% to 84%** across 600 diverse catalytic surfaces. Validated on seven gas–solid benchmarks (stepped metals, single-atom catalysts, ordered intermetallics, vacancy-rich 2D sulfides, 2D carbides, SMSI interface) with every prediction within **0.5–2× experimental values** across four orders of magnitude. For propane dehydrogenation, CatDT independently discovered non-precious candidates rivaling Pt-based industrial benchmarks (Ni@ZrO₂ SMSI overlayer reaching simulated TOF of 1.63 s⁻¹ at ~100% selectivity). Code repository announced at github.com/AI4QC/catdt upon publication ([source](https://arxiv.org/abs/2606.05050)).
- **CategoryScienceClaw** (Lifecycle: Multi-stage) — MIT (Buehler lab) self-revising discovery framework that adds a **category-theoretic, proof-carrying layer** to the underlying ScienceClaw agentic execution substrate, so that **regime transitions** — schema changes admitting new evidence types — are machine-verifiable. Fixed-regime operation is modeled as an endofunctorial update on copresheaf states `Iₜ : Sb → Set`; discovery is a verified regime transition `u : Sb → Sb'` with left Kan extension `Lan_u Iₜ` transporting old artifacts and an explicit preservation map. Two instantiations: **Builder/Breaker** (protein-mechanics symbolic world model revised under a Minimum Description Length gate; accepted law expresses within-chain flexibility as mode-conditioned compliance, with a 54.3-bit MDL gain) and **CategoryScienceClaw** (typed skills, immutable artifacts, open needs, workflow mutation, gates, stress tests, and public discourse lifted into a proof-carrying knowledge–computation graph; fiber-network mechanics worked example records candidate models, rejected alternatives, an AIC gate, perturbation tests, and an accepted orientation-tensor anisotropic stiffness surrogate over an isotropic fiber-count descriptor). Code at github.com/lamm-mit/scienceclaw plus the categoryscienceclaw-mechanics branch and github.com/lamm-mit/BreakingTheWorld ([source](https://arxiv.org/abs/2606.01444)).
- **AgentPLM** (Lifecycle: Experiment design) — Bedford College, London (Sahil Rahman) and Saarland University (Maxx Richard Rahman) agentic protein language model that takes the agent loop inside the PLM rather than around it. **Reasoning-Augmented Decoding (RAD)** interleaves autoregressive sequence generation with tool calls to ESMFold, FoldX, and AutoDock Vina via a learned **Tool Context Encoder** and **Trajectory Memory Buffer** trained end-to-end; **Contrastive Agent Policy Optimisation (CAPO)**, a trajectory-level extension of DPO, contrasts high-fitness trajectories with coherent oracle use against low-fitness or contradictory ones to teach the policy when oracle feedback is informative rather than imitating high-fitness sequences. Initialised from ESM-2 650M and evaluated on de novo enzyme design, antibody optimisation, thermostability, PPI interface design, and zero-shot fitness prediction with standardised oracle APIs and controlled sequence-identity splits. AgentPLM reports a **2.79× improvement in antibody top-10% hit rate** and **+34% normalised k_cat/K_M** on enzyme design, with mechanistic evidence of online error correction without explicit backtracking; accepted to ICML 2026 ([source](https://arxiv.org/abs/2606.02386)).

### Updated
- **`autonomous-science/summary.md`** — added a CatDT + CategoryScienceClaw paragraph in the Chemistry and materials section (heterogeneous-catalyst digital twin with 0.5–2× experimental fidelity and discovered Ni@ZrO₂ propane-dehydrogenation candidate; categorical proof-carrying layer with mode-conditioned compliance law and fiber-network anisotropic stiffness surrogate); added an AgentPLM paragraph in the Wet-lab and data-driven biology section (agent-in-PLM with RAD + CAPO, 2.79× antibody hit-rate gain); added an MLEvolve paragraph in the Machine-learning section (Progressive MCGS + Retrospective Memory; 65.3% MLE-Bench medal rate, best on 11/15 AlphaEvolve math tasks). Appended four new source citations.
- **`autonomous-science/curator-state.md`** — added MLEvolve, CatDT, CategoryScienceClaw, and AgentPLM at the top of `Recently surfaced`; trimmed DKPL, MAD, LEAP, and VIS Co-Scientist to keep the window at five (AutoSci retained). Appended a `ScienceClaw × Infinite` deferred entry (arXiv:2603.14312) to revisit as a possible standalone page.
- **`sources/manifest.json`** — four new DOI entries added by Phase A (arXiv:2606.05050 CatDT, arXiv:2606.01444 CategoryScienceClaw, arXiv:2606.02386 AgentPLM, arXiv:2606.06473 MLEvolve).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 or later — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-06-02

### Added
- **AutoSci** (Lifecycle: Multi-stage, Writing) — Peking University (PKUDAIR) memory-centric agentic system for the full scientific research lifecycle. Four interlocking modules: **SciMem** (schema-governed persistent memory split into a typed Long-Term Knowledge graph — 10 typed entities, 20+ typed relations — and an Active Research workspace with explicit lifecycle states), **SciFlow** (a harness-based five-stage executor over Literature, Ideation, Experiment, Writing, and Rebuttal with 30+ research skills), **SciDAG** (9 reusable multi-agent operators plus stage-specific templates), and **SciEvolve** (3 evolution skills converting user, experimental, and review feedback into versioned updates to memory, skills, and templates). All memory writes pass through a **Trust Guard** combining deterministic schema linting and an independent reviewer agent (PASS / WARN / BLOCK). Two end-to-end case studies — GPU kernel optimization and biomedical drug discovery — produced paper-level artifacts scoring **6.3/10** and **5.8/10** under automated ICLR-style review. Code at github.com/skyllwt/AutoSci ([source](https://arxiv.org/abs/2605.31468)).
- **VIS Co-Scientist** (Lifecycle: Analysis) — Lawrence Livermore National Laboratory with Vanderbilt and Notre Dame end-to-end agentic harness that autonomously designs custom visualization applications (VIS Apps) given only a dataset and a high-level task description. A main code agent (OpenAI Codex) orchestrates specialized subagents through artifact-mediated handoffs: **Exploratory Data Analyzer** profiles the dataset, **Planner** translates tasks into concrete visual-encoding specifications, **Environment Builder** configures dependencies, **VIS Designer** implements complex views (3D volume rendering, progressive streaming, linked selections), and an **Evaluator** validates both mechanics and task completion via **Playwright-based browser inspection**. A hierarchical markdown-based memory layer captures lessons across sessions. Evaluated on IEEE SciVis Contests for **2021, 2023, 2024, and 2026** (climate science, materials discovery, sonar imaging, neuroscience, mantle convection), producing functional single-page VIS Apps with verified linked-view behavior. Open-source release pending internal code review at LLNL ([source](https://arxiv.org/abs/2605.21825)).
- **DKPL** (Lifecycle: Experiment design, Analysis) — Oak Ridge National Laboratory's Deep-Kernel Pairwise Learning replaces hand-engineered scalar Bayesian-optimization objectives — a well-known bottleneck of self-driving microscopy — with a latent utility function inferred from expert pairwise judgements. A neural feature extractor maps high-dimensional data (microscopy image patches) into a low-dimensional latent representation; a **pairwise Gaussian process** operates on the latent space, learns from "A is better than B" comparisons, supports **indifference judgements** and **confidence-weighted** feedback, and uses **Upper Confidence Bound** (default β = 5) to plan subsequent measurements. Demonstrated on band-excitation piezoresponse spectroscopy of PbTiO3 (known-ground-truth dataset) and then applied to ferroelectric domain-wall character: DKPL distinguished **high vs. low domain-wall angles in bismuth ferrite** and discovered **head-to-head and tail-to-tail domain-wall character in erbium manganite** — multidimensional polarization behaviors that resist scalar description ([source](https://arxiv.org/abs/2605.21820)).
- **MAD** (Lifecycle: Experiment design, Analysis) — University of Maryland / NIST Multi-instrument Autonomous Discovery framework coordinating multiple characterization instruments as cooperating agents over a shared probabilistic posterior. Two compositionally identical Mn-Sb-Te thin-film spreads (177 4×4 mm regions) run in parallel on an XRD diffractometer (crystalline state) and a contact probe station (amorphous state), connected to a central agent that performs joint inference using a **multi-output Gaussian process with a co-regionalization kernel**. Distinct acquisition functions drive structural phase mapping (NMF over diffraction patterns) and resistance optimization (amorphous-state R_amo, a phase-change-memory figure of merit). A single live run achieved phase mapping and materials optimization in **5 hours over 25 closed-loop iterations** — a **seven-fold speed-up** over autonomous experimentation with independent GPs and over conventional grid mapping, on the previously unexplored Mn-Sb-Te ternary system for phase-change memory ([source](https://arxiv.org/abs/2605.18033)).

### Updated
- **`autonomous-science/summary.md`** — added an AutoSci paragraph in the Machine-learning section (full-lifecycle memory-centric agentic system, 6.3/10 and 5.8/10 ICLR-style scores on two case studies); appended a combined MAD + DKPL paragraph in Chemistry and materials (seven-fold speed-up on Mn-Sb-Te closed-loop discovery; expert-pairwise replacement for scalar BO objectives in ferroelectric domain-wall imaging); added a new **Scientific visualization** section for VIS Co-Scientist (SciVis-contest validation across four years and five domains). Appended four new source citations.
- **`autonomous-science/curator-state.md`** — added AutoSci, VIS Co-Scientist, DKPL, and MAD at the top of `Recently surfaced`; trimmed AutoScientists, AutoLLMResearch, AtomisticSkills, and ScientistOne to keep the window at five (LEAP retained as the next-newest).
- **`sources/manifest.json`** — four new DOI entries added by Phase A (arXiv:2605.31468 AutoSci, arXiv:2605.21825 VIS Co-Scientist, arXiv:2605.21820 DKPL, arXiv:2605.18033 MAD).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 or later — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-06-01

### Added
- **LEAP** (Lifecycle: Multi-stage) — Renmin University of China expert-in-the-loop closed-loop framework that couples a domain-specialized LLM (**Perovskite-RL**, supervised fine-tuned and RL'd on the perovskite-additive literature) with Bayesian optimization for iterative perovskite precursor additive discovery. Perovskite-RL emits soft mechanistic descriptors along five interpretable axes (binding mode, interfacial shielding, hydrophobic protection, ion-interaction potential, electronic modulation) that combine with hard molecular features in a hybrid representation feeding a GP surrogate with EI acquisition. On a 32-question mechanism-consistency benchmark drawn from 16 unseen additive papers, Perovskite-RL scored **78.1%** vs 50.0% (gemini-3-flash), 46.9% (DeepSeek-V3.2), 43.8% (GPT-5), 37.5% (Qwen3-32B), 28.1% (llama-3.3-70b-instruct), with Holm-Bonferroni-adjusted McNemar p < 0.001 to < 0.05. Three rounds of expert-in-the-loop wet-lab validation in inverted ITO/NiOx/4PADCB/perovskite/C60/BCP/Ag devices (24 devices per condition) produced mean PCEs of **20.13 ± 0.25%** (6-CDQ) and **20.87 ± 0.25%** (2-CNA) vs 19.25 ± 0.28% control, with a champion 2-CNA PCE of **21.32%** (VOC 1.128 V, JSC 23.92 mA/cm², FF 0.790) ([source](https://arxiv.org/abs/2605.20242)).
- **AutoScientists** (Lifecycle: Multi-stage) — Harvard (Zitnik lab) decentralized team of long-running AI agents that self-organize into teams around competing hypotheses and coordinate only through a shared state (champion `p*`, experiment log, structured research forum, team-local queues and dead-end registries) — no central planner. Default config: 3 analyst + 6 experiment agents, all running Claude Code with Claude Sonnet 4.6 on H100 GPUs. Under matched compute budgets, AutoScientists improves over the strongest prior single-trajectory baseline (Autoresearch): on **BioML-Bench** (24 biomedical-ML tasks) it reaches **74.40% mean leaderboard percentile** vs 66.07% (+8.33 points), with drug-discovery 47.91% → 64.52%; on **GPT nanochat training optimization** it reaches val_bpb ≈ 0.978 in 34 experiments vs 65 for Autoresearch (1.9× fewer) and accepts 7 improvements from an AutoScientists champion (0.9777 → 0.9730) where Autoresearch accepts 0 over 100 experiments; on **ProteinGym** it lifts ACE2-Spike Spearman ρ from 0.747 to 0.840 (+12.5%) and the frozen recipe transfers across all 217 supervised-substitution assays for +6.5% average. Code at github.com/mims-harvard/AutoScientists; site at autoscientists.openscientist.ai ([source](https://arxiv.org/abs/2605.28655)).
- **AutoLLMResearch** (Lifecycle: Experiment design, Analysis) — University of Notre Dame agentic framework trained via reinforcement learning over a multi-fidelity LLM-experiment environment so it can extrapolate generalizable principles from cheap low-fidelity experiments to efficient configuration of expensive ones. **LLMConfig-Gym** packages over **one million GPU hours** of verifiable experiment outcomes across four LLM tasks (Model Architecture, Pretraining Hyperparameter, RL GRPO Tuning, Data Mixture); a structured pipeline (Train/Test Experiment Curation, Trajectory Simulation, Policy Distillation, Multi-turn RL) formulates configuration research as a long-horizon MDP and trains the agent to handle both configuration-space shifts (different config spaces across fidelities) and optimization-landscape shifts (non-monotonic transfer of optima) that defeat prior HPO and meta-learning. To the authors' knowledge, the first systematic study on automating expensive LLM experiment configuration. Code at github.com/taichengguo/AutoLLMResearch ([source](https://arxiv.org/abs/2605.11518)).

### Updated
- **`autonomous-science/summary.md`** — appended three paragraphs in the Machine-learning section covering AutoScientists (decentralized coordination, +8.33 points on BioML-Bench, 1.9× faster on GPT nanochat, +12.5% on ACE2-Spike) and AutoLLMResearch (RL-trained agent over LLMConfig-Gym, cross-fidelity extrapolation); appended a LEAP entry in the Chemistry and materials section (78.1% mechanism-consistency vs ≤50% baselines, wet-lab PCE 20.87% vs 19.25% control); added three new source citations.
- **`autonomous-science/curator-state.md`** — added LEAP, AutoScientists, and AutoLLMResearch at the top of `Recently surfaced`; trimmed NORA, MCI, and BioProVLA-Agent (all dated 2026-05-31) to keep the window at five.
- **`sources/manifest.json`** — three new DOI entries added by Phase A (arXiv:2605.20242 LEAP, arXiv:2605.28655 AutoScientists, arXiv:2605.11518 AutoLLMResearch).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 or later — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-31

### Added
- **AtomisticSkills** (Lifecycle: Multi-stage) — MIT (Gómez-Bombarelli and Coley groups) with Shell open-source agent harness that empowers general-purpose AI coding agents to conduct atomistic research across materials science, chemistry, and drug discovery. Hierarchically decomposes scientific workflows into an MCP tool box (FairChem, MatGL, MACE, Atomate2, ORCA, DiffCSP, MatterGen, …), a skill library of more than **100 curated skills** spanning 53 materials-science, 23 chemistry, 18 drug-discovery, 14 ML, and 11 general skills, plus research, skill, and workflow standards. Functional coverage validated against the literature and demonstrated across six campaigns: Li-ion solid-state electrolyte generative design, MOF CO2-capture screening, autonomous MLIP benchmarking and fine-tuning, multi-stage structure-based virtual screening for drugs, multimodal XRD pattern analysis, and Fe-oxide OER catalyst screening ([source](https://arxiv.org/abs/2605.24002)).
- **ScientistOne** (Lifecycle: Multi-stage, Writing) — Google Cloud AI Research end-to-end autonomous research system built around the **Chain-of-Evidence (CoE)** standard, which requires every citation, numerical, methodological, and conclusion claim to trace through a recorded chain to a grounding source. Three stages — Problem Investigator (reads up to 100 full-text PDFs per topic via scholarly databases), Parallel Explore-Exploit Discovery Engine (Solver agents iterate across branches with task-specific evaluators and best-run selection), and Paper Writer with Claim Verifier — produce provenance-bearing artifacts. A companion **CoE Integrity Audit** scoring 15 papers per system across five autonomous research systems on five ADRS frontier ML tasks finds every baseline fails at least one of Score Verification, Specification Violation, Reference Verification, or Method-Code Alignment (hallucinated reference rates up to 21%, score verification as low as 42%). ScientistOne reaches **0/337 hallucinated references, 12/12 score verification, and 14/15 method-code alignment** while matching or exceeding human expert solver performance, and generalizes to medical imaging, fine-grained recognition, 3D perception, and parameter-constrained LM with **state-of-the-art on Parameter Golf** and gold medals on MLE-Bench tasks where baselines fail entirely ([source](https://arxiv.org/abs/2605.26340)).
- **NORA** (Lifecycle: Multi-stage, Writing) — University of Tennessee, Knoxville (Bing Zhou) with Emory, Texas A&M, and TikTok — Night Owl Research Agent, a harness-engineered multi-agent autonomous research system purpose-built for **GIScience and spatial data science**. Skills-first architecture with **21 domain-specialized workflow skills**, **9 specialist sub-agents**, and custom MCP servers, including two novel skill units: a spatial analysis skill encoding decision frameworks for ESDA, spatial regression (OLS vs. GWR vs. MGWR), and diagnostics; and a spatial data download skill supporting reproducible acquisition from authoritative geospatial sources. Formalizes "harness engineering" with lifecycle hooks, safety gates, generator–evaluator separation, human-in-the-loop, and state persistence. Three IJGIS-targeted case studies evaluated by **6 domain specialists and 3 LLM reviewers across seven dimensions** — first catalogue entry for spatial data science / GIScience ([source](https://arxiv.org/abs/2605.02092)).
- **MCI** (Lifecycle: Hypothesis, Analysis) — KRICT / KAIST Machine Collective Intelligence, a multi-agent framework that integrates symbolism and metaheuristics for autonomous discovery of **explainable governing equations**. K LLM-based reasoning agents evolve symbolic hypotheses canonicalized as abstract syntax trees through coordinated generation, complexity-aware evaluation (negative SSE + inverse depth), critique, and consolidation; population-based metaheuristics propagate best experiences across agents to escape any single backbone LLM's reasoning boundary. Across deterministic, stochastic, and previously uncharacterized dynamical systems, MCI recovers the underlying governing equations without hand-crafted domain knowledge, **reduces extrapolation error by up to six orders of magnitude** versus deep neural networks, and compresses 0.5–1 M DNN parameters into **5–40 interpretable parameters** ([source](https://arxiv.org/abs/2604.27297)).
- **BioProVLA-Agent** (Lifecycle: Experiment design) — East China University of Science and Technology, with Ruijin Hospital (Shanghai Jiao Tong University School of Medicine) and Shihezi University — affordable, protocol-driven, vision-enhanced embodied multi-agent system using Vision-Language-Action (VLA) models for biological laboratory manipulation on a ~**US$800–850** hardware platform. A Tailored LLM Protocol Agent transforms unstructured natural-language protocols into verifiable subtask units; a VLM-RAG Verification Agent reasons over real-time visual observations, robot states, retrieved operation knowledge, and reference success/failure examples to assess task readiness and completion; and a VLA Embodied Agent executes verified subtasks via a lightweight VLA policy. **AugSmolVLA** introduces online visual augmentation during fine-tuning to handle transparent labware, specular reflections, illumination shifts, and overexposure. Evaluated on **15 atomic tasks, 6 composite workflows, and 3 bimanual tasks** (centrifuge-tube loading, tube sorting, waste disposal, cap twisting, liquid pouring), AugSmolVLA improves execution stability over ACT, X-VLA, and the original SmolVLA across normal and high-exposure settings ([source](https://arxiv.org/abs/2605.07306)).

### Updated
- **`autonomous-science/summary.md`** — appended sentences/paragraphs covering all five new systems: AtomisticSkills (Chemistry and materials section), ScientistOne (Machine-learning section, plus a new "Verifiability audits" paragraph in the evaluation section), and BioProVLA-Agent (Embodied physical-sciences section); added two new sections — **Symbolic equation discovery** (MCI) and **Spatial data science and GIScience** (NORA). Appended five new source citations.
- **`autonomous-science/curator-state.md`** — replaced the five-entry `Recently surfaced` window with AtomisticSkills, ScientistOne, NORA, MCI, and BioProVLA-Agent (all added 2026-05-31).
- **`sources/manifest.json`** — five new DOI entries added by Phase A (arXiv:2605.24002 AtomisticSkills, arXiv:2605.26340 ScientistOne, arXiv:2605.02092 NORA, arXiv:2604.27297 MCI, arXiv:2605.07306 BioProVLA-Agent).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 or later — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-30

### Added
- **AMASE** (Lifecycle: Multi-stage) — University of Maryland (Takeuchi lab) and NIST autonomous materials search engine that closes the loop on combinatorial thin-film phase mapping. A **Variable Generation Planning Controller** (LLM-driven) orchestrates Bayesian active learning over composition–temperature space, YOLO-based XRD peak detection, and CALPHAD-informed phase identification, with explicit end-point detection. On a Sn-Bi thin-film library, AMASE autonomously selected **66 XRD measurements at 11 temperatures in 8 h 22 min** and predicted a thin-film eutectic at **53.3 ± 2 at% Sn / 133.1 ± 1 °C** — agreeing within **3%** of independent dedicated experiments (55.5 ± 1.5 at% Sn, 133.2 ± 10 °C) and exposing a thin-film vs. bulk eutectic shift from the standard 59.5 at% Sn / 140.7 °C; a **~6× reduction** in measurements over uniform sampling. Data and code released with the manuscript ([source](https://arxiv.org/abs/2410.17430)).
- **BORA** (Lifecycle: Experiment design, Hypothesis) — University of Liverpool (Cooper lab) language-based Bayesian-optimization research assistant pairing a Matérn-kernel Gaussian process with GPT-4o-mini. Three actions — **a₁** vanilla BO, **a₂** LLM-only hypotheses, **a₃** LLM filtering of BO candidates — are governed by an adaptive heuristic policy with a **trust mechanism** that monitors LLM-suggested improvement and a structured **Experiment Card** that grounds the language model in problem context. On the 10-D Hydrogen Production benchmark BORA reduces cumulative regret by **47%** versus ColaBO, and a sign test versus HypBO across three synthetic and four real campaigns gives **p = 0.02**; ablations show both the LLM hypothesis action and the trust mechanism are load-bearing. IJCAI 2025; open source at github.com/Ablatif6c/bora-the-explorer ([source](https://arxiv.org/abs/2501.16224)).

### Updated
- **`autonomous-science/summary.md`** — added two sentences in the Chemistry and materials section covering AMASE (closed-loop Sn-Bi phase mapping with ~6× measurement reduction) and BORA (hybrid BO–LLM optimization with 47% cumulative-regret reduction); removed the BORA preview from the "Other notable systems being tracked for inclusion" line; appended two new source citations.
- **`autonomous-science/systems/`** — renumbered `nav_order` on 37 affected system pages to preserve alphabetical ordering after inserting **AMASE** (nav_order 5) and **BORA** (nav_order 13). AILA, AIRA, Aleks, ARIS, AutoResearchClaw, AutoTTS, Biomni shifted by +1 for AMASE; all entries from ChemCrow through Virtual Biotech shifted by +2 for both insertions.
- **`autonomous-science/curator-state.md`** — added AMASE and BORA at the top of `Recently surfaced`; trimmed EvoMaster and NeuroClaw (both 2026-05-27) to keep the window at five.

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 or later — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-29

### Added
- **Latent-Y** (Lifecycle: Multi-stage) — Latent Labs (London / San Francisco) lab-validated autonomous agent for de novo biologics design that executes complete antibody design campaigns from text prompts, covering literature review, target / epitope analysis, candidate generation via the Latent-X2 generative model, computational validation (iPTM, DockQ), and selection of lab-ready sequences; supports both fully autonomous and collaborative modes and can write custom generative code under bounded platform access (e.g. for cross-species TNFL9 reactivity). Across nine therapeutic targets, Latent-Y produced lab-confirmed nanobody binders against six (**67% target-level success rate**, per-target hit rates 1–28%), with single-digit nanomolar affinities (PRL 5.44 nM, IL-6 12.5 nM, IL-6R 517 nM) validated by five-point SPR, and a user study against PhD-level protein designers reports a **56× acceleration** of expert-led campaigns ([source](https://arxiv.org/abs/2603.29727)).
- **PantheonOS** (Lifecycle: Multi-stage) — Stanford (Qiu lab) evolvable, privacy-preserving multi-agent framework for end-to-end single-cell and multi-omics genomics analysis spanning RL-augmented gene panel design, raw FASTQ processing, multimodal data integration, and 3D spatial genomics reconstruction. **Pantheon-Evolve** enables agentic code evolution that autonomously rewrites the system's own batch-correction and gene-panel-design algorithms beyond manually designed baselines; an intelligent model-routing mechanism adaptively selects optimal virtual-cell models across heterogeneous tasks. Demonstrated biology includes 3D reconstruction of mouse embryonic-day-six expression revealing **asymmetric Cer1–Nodal inhibition** along the proximal–distal axis, integration of human fetal-heart single-cell multi-omics with whole-heart 3D MERFISH+ at post-conception week 12, and adaptive virtual-cell-model selection for cardiogenesis perturbation prediction. Open ecosystem at github.com/aristoteleo; project at pantheonos.stanford.edu ([source](https://doi.org/10.64898/2026.02.26.707870)).
- **The Virtual Biotech** (Lifecycle: Multi-stage) — Stanford (Zou lab) multi-agent AI framework that mirrors the structure of a human therapeutic research organization: a **Chief Scientific Officer** agent receives scientific queries and delegates to domain-specialized scientist agents (statistical genetics, functional genomics, pathways and interactions, chemoinformatics, disease biology, clinical data), integrating outputs through data-driven reasoning. Three reported translational case studies: (1) **>37,000 clinical-trialist agents** autonomously annotated outcomes from **55,984 clinical trials** and found drugs targeting cell-type-specific genes are **40% more likely to advance Phase I → II**, **48% more likely to reach Phase IV**, with **32% lower adverse event rates**; (2) end-to-end B7-H3 lung-cancer target evaluation proposing an ADC strategy; (3) re-analysis of a terminated OSMRβ ulcerative-colitis trial inferring failure mechanisms and proposing biomarker-guided enrollment strategies ([source](https://doi.org/10.64898/2026.02.23.707551)).

### Updated
- **`autonomous-science/summary.md`** — appended a paragraph in the wet-lab and data-driven biology section covering Latent-Y, The Virtual Biotech, and PantheonOS; added three new source citations.
- **`autonomous-science/systems/`** — renumbered `nav_order` on the 10 affected system pages (MARS → 28, NeuroClaw → 29, NovelSeek → 30, OpenScientist → 31, PerTurboAgent → 33, PharmaSwarm → 34, POISE → 35, Qiushi Discovery Engine → 36, Qumus → 37, Robin → 38, SPARK → 39, Talk2QSP → 40) to preserve alphabetical ordering after inserting Latent-Y (27), PantheonOS (32), and The Virtual Biotech (41).
- **`autonomous-science/curator-state.md`** — added Latent-Y, PantheonOS, and The Virtual Biotech at the top of `Recently surfaced`; trimmed Aleks, Deep Researcher Agent, and PerTurboAgent (each dated 2026-05-25) to keep the window at five.
- **`sources/manifest.json`** — three new DOI entries added by Phase A (arXiv:2603.29727 for Latent-Y, bioRxiv 2026.02.26.707870 for PantheonOS, bioRxiv 2026.02.23.707551 for The Virtual Biotech). Note: the two bioRxiv preprints were blocked by Cloudflare on the PDF fetch; the `.txt` sidecars are derived from the bioRxiv API metadata (title, authors, abstract, extended summary).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 through 2026-05-27 — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-27

### Added
- **EvoMaster** (Lifecycle: Multi-stage) — Shanghai Jiao Tong University / SciLand / DP Technology foundational evolving-agent framework engineered for Agentic Science at Scale. A three-layer execution architecture (Playground orchestration, Exp single-experiment lifecycle, Agent reasoning core) plus a context-managed `reason → tools → observe → self-critique` loop, an MCP-native Capability Layer with hierarchical skill loading, and YAML configuration manifests with JSON trajectory logging let developers build self-evolving scientific agents in ~100 lines of code. Underpins the **SciMaster** ecosystem (ML-Master, X-Master, Browse-Master, PhysMaster, EmboMaster). Reports state-of-the-art scores with GPT-5.4 against OpenClaw on four benchmarks: **HLE 41.1%** (+202%), **MLE-Bench Lite 75.8%** (+316%, 17/22 Kaggle medals), **BrowseComp 73.3%** (+159%), **FrontierScience 53.3%** (+191%); open source at github.com/sjtu-sai-agents/EvoMaster ([source](https://arxiv.org/abs/2604.17406)).
- **NeuroClaw** (Lifecycle: Experiment design, Analysis) — CUHK / Northwest University / Lehigh / Massachusetts General Hospital / Harvard Kempner Institute domain-specialized multi-agent research assistant for executable and reproducible neuroimaging research. Operates directly on raw sMRI / fMRI / dMRI / EEG data with BIDS-aware orchestration, ADNI / HCP Young Adult / UK Biobank dataset skills, and a harness layer with pinned Python / Docker environments, automated installers for FSL / FreeSurfer / fMRIPrep, expected-artifact / missing-file / NaN-Inf verification, and JSONL audit logs. A three-tier skill hierarchy (interface / subagent / base) with skill dependencies expressed as a DAG decomposes long workflows into reusable units. Companion **NeuroBench** (100 hand-curated tasks T001–T100, GPT-5.4 judge across planning completeness, tool-use reasonableness, code correctness) shows all ten frontier multimodal LLMs improve when run inside NeuroClaw — mean absolute gain **+4.74 points**, Claude-Opus-4.6 top at **72.10%**, MiniMax-M2.7 largest absolute gain **+12.97**; adds neuroimaging as a new domain ([source](https://arxiv.org/abs/2604.24696)).

### Updated
- **`autonomous-science/summary.md`** — added two paragraphs in the closed-loop multi-domain frameworks section covering EvoMaster (foundational SciMaster harness with cross-benchmark numbers) and NeuroClaw (domain-specialized neuroimaging entry with NeuroBench results); appended two new source citations.
- **`autonomous-science/systems/`** — renumbered `nav_order` on the 14 affected system pages (EvoScientist → 23, GRAFT-ATHENA → 24, Jr. AI Scientist → 25, Kosmos → 26, MARS → 27, NovelSeek → 29, OpenScientist → 30, PerTurboAgent → 31, PharmaSwarm → 32, POISE → 33, Qiushi Discovery Engine → 34, Qumus → 35, Robin → 36, SPARK → 37, Talk2QSP → 38) to preserve alphabetical ordering after inserting EvoMaster (22) and NeuroClaw (28).
- **`autonomous-science/curator-state.md`** — added EvoMaster and NeuroClaw at the top of `Recently surfaced`; trimmed the two oldest entries (PharmaSwarm, POISE) to keep the window at five.
- **`sources/manifest.json`** — two new DOI entries with `.txt` sidecars (added by Phase A): arXiv:2604.17406 (EvoMaster), arXiv:2604.24696 (NeuroClaw).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 through 2026-05-25 — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-25

### Added
- **Aleks** (Lifecycle: Multi-stage) — Cornell three-agent multi-agent system (Domain Scientist, Data Analyst, Machine Learning Engineer) that, given only a research question and a tabular dataset, autonomously formulates the problem, iterates ML modeling strategies, and converges on interpretable models. Grapevine red blotch disease case study over a multi-year vineyard grid; ablations show that removing the Domain Scientist agent or restricting shared memory to a single iteration degrades coherence. Adds plant science / agriculture as a new domain to the catalogue ([source](https://arxiv.org/abs/2508.19383)).
- **Deep Researcher Agent** (Lifecycle: Multi-stage) — University of Tokyo open-source 24/7 framework running LLM agents through a Think → Execute → Reflect loop with Zero-Cost Monitoring (OS-level process/GPU/log-tail checks during training), a Two-Tier Constant-Size Memory provably bounded at ~5,000 characters, and a Minimal-Toolset Leader-Worker architecture. Across 4 concurrent projects on 4 GPU servers logged 500+ autonomous cycles, 30+ days continuous operation, $0.08 LLM cost per 24-hour cycle, and 52% improvement over baseline in the best project from 200+ automated experiments; open source ([source](https://arxiv.org/abs/2604.05854)).
- **PerTurboAgent** (Lifecycle: Experiment design, Analysis) — Genentech/Tsinghua/Stanford (Regev lab) self-planning LLM agent for iterative Perturb-seq experiments. Multi-step planner at each round combines agent-based (predict/reflect/refine), data-driven (GSEA on control or perturbed cells), and model-driven (perturbation prediction, embeddings, phenotype scores) actions, with an Action Memory storing per-step (action, result) pairs to adapt the plan. Outperforms BioDiscoveryAgent, GeneDisco, DiscoBAX, and IterPert across eleven phenotypes from genome-scale Perturb-seq data with both closed- and open-source LLM backbones ([source](https://proceedings.mlr.press/v311/hao25b.html)).
- **PharmaSwarm** (Lifecycle: Hypothesis, Analysis) — UAB Systems Pharmacology AI Research Center three-layer LLM agent swarm for hypothesis-driven drug discovery (Terrain2Drug omics, Paper2Drug literature, Market2Drug repurposing signals) coordinated by a TxGemma-based Evaluator over Open Targets, ChEMBL, DrugBank, KEGG, PAGER, and a proprietary PharmAlchemy knowledge graph. Includes a Pharmacological Efficacy and Toxicity Simulation engine and an Interpretable Binding Affinity Map (iBAM) module cross-attending ESM2 and ChemBERTa embeddings. Design + retrospective preprint — no wet-lab validation reported; proposes a four-tier validation roadmap ([source](https://arxiv.org/abs/2504.17967)).
- **POISE** (Lifecycle: Multi-stage) — Fudan closed-loop framework for autonomous discovery of LLM-RL policy-optimization algorithms. Frames the problem as Epistemic Evolutionary Search over a genealogically linked archive storing (proposal, implementation, training trajectory, metrics, reflection); a lineage acquisition function combines Pareto-frontier strength, normalized performance, diversity, and a GP-UCB term targeting discounted top-K descendant-gain. Starting from GRPO, evaluated 64 candidates and discovered analytic-variance scaling and validity masking; best variant lifts weighted Overall from 47.8 → 52.5 and AIME25 pass@32 from 26.7% → 43.3% ([source](https://arxiv.org/abs/2603.23951)).

### Updated
- **`autonomous-science/summary.md`** — added a paragraph in the wet-lab/biology section covering PerTurboAgent and PharmaSwarm; added a paragraph in the ML/scientific-computing section covering Deep Researcher Agent and POISE; created a new "Plant science and agriculture" domain section for Aleks; appended five new source citations.
- **`autonomous-science/systems/`** — renumbered `nav_order` on the existing 25 affected system pages to preserve alphabetical ordering after inserting the five new entries.
- **`autonomous-science/curator-state.md`** — replaced `Recently surfaced` with the five new additions; removed the pre-existing "Deep Researcher Agent" item from `Deferred — next-run priority` (now added as a full system page).
- **`sources/manifest.json`** — five new DOI entries with `.txt` sidecars (added by Phase A).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 through 2026-05-24 — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-24

### Added
- **AutoResearchClaw** (Lifecycle: Multi-stage, Writing) — UNC-led 23-stage Discovery → Experimentation → Writing pipeline combining structured multi-agent debate (Innovator/Pragmatist/Contrarian, then Optimist/Skeptic/Methodologist), a self-healing executor with explicit Pivot/Refine decisions, a numeric registry that whitelists every reported value, seven human-in-the-loop intervention modes including a confidence-driven SmartPause, and a time-decayed cross-run lesson store. On ARC-Bench CoPilot scores 0.648 overall (vs. AI Scientist v2 0.419, AIDE-ML 0.511); end-to-end 87.5% paper-acceptance rate with 19 interventions; sandboxed domain agents extend to HEP-ph, systems biology, and statistics where ML-only baselines collapse to ≤ 0.09; open source ([source](https://arxiv.org/abs/2605.20025)).
- **CVEvolve** (Lifecycle: Analysis) — Argonne Advanced Photon Source agentic harness for autonomous discovery of analytical image-processing algorithms across synchrotron imaging (XRF registration, Bragg peak detection, polycrystalline diffraction segmentation). Generate/tune/evolve rounds use MAP-Elites-inspired lineage-aware stochastic sampling; an in-loop image viewer handles floating-point and TIFF inputs; a separate holdout-test agent runs without seeing development data. Best XRF registration candidate reaches average Euclidean error 0.12 vs. 0.98 (brute force) and 0.23 (OpenEvolve at 500 iterations); Bragg peak detection holdout F1 0.298 → 0.788 ([source](https://arxiv.org/abs/2605.11359)).
- **EOS AI agent** (Lifecycle: Experiment design, Analysis) — UNC-Chapel Hill MCP-based agentic layer on top of the Experiment Orchestration System for laboratory automation across chemistry, biology, and materials. Creates, validates, and submits YAML protocols and closed-loop Bayesian optimization campaigns from natural-language prompts; a visual graph editor is bidirectionally synced to the protocol YAML; 40+ MCP tools split into read-only (auto-executed) and mutating (user-approved) classes. 97% first-attempt protocol-generation success across 65 trials at mean $0.50 and 184 s wall-time on Claude Sonnet 4.6; correct standard-curve and solubility-screening protocols on first attempt on UBC's PurPOSE platform ([source](https://arxiv.org/abs/2605.16552)).

### Updated
- **`autonomous-science/summary.md`** — added a paragraph in the ML / scientific-computing section for AutoResearchClaw, inserted CVEvolve alongside AI CFD Scientist, added EOS AI agent to the chemistry/materials section, and appended three new source citations.
- **`autonomous-science/systems/`** — renumbered `nav_order` on the existing 21 affected system pages to preserve alphabetical ordering after inserting the three new entries.
- **`autonomous-science/curator-state.md`** — refreshed `Recently surfaced` with the three new additions plus the two most recent prior entries (AIRA, AutoTTS).
- **`sources/manifest.json`** — three new DOI entries with `.txt` sidecars (added by Phase A).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 through 2026-05-23 — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-23

### Added
- **AIRA (AIRA-Compose and AIRA-Design)** (Lifecycle: Multi-stage) — Meta FAIR dual-agent framework for autonomous foundation-model architecture discovery. AIRA-Compose deploys 11 agents over Attention/MLP/Mamba primitives under a 24-hour budget; AIRA-Design tasks up to 20 agents with writing novel attention mechanisms. Discovered 14 architectures (AIRAformers, AIRAhybrids); at 1B scale, AIRAformer-D and AIRAhybrid-D improve downstream accuracy by 2.4% and 3.8% over Llama 3.2 and scale 54–71% faster ([source](https://arxiv.org/abs/2605.15871)).
- **AutoTTS** (Lifecycle: Hypothesis, Experiment design, Analysis) — UMD/UVA/WUSTL/UNC/Google/Meta environment-driven agentic framework that discovers test-time-scaling controllers via controller synthesis over an offline replay environment with beta parameterization and execution-trace feedback; improves the accuracy–cost Pareto frontier on math reasoning with a one-time discovery cost of $39.9 / 160 minutes; open source ([source](https://arxiv.org/abs/2605.08083)).
- **CMBEvolve and CosmoEvolve** (Lifecycle: Multi-stage) — Cambridge cosmology pair of agentic systems. CMBEvolve performs LLM-guided code evolution via typed tree search with score backpropagation for tasks with explicit quantitative metrics; CosmoEvolve simulates a virtual research laboratory with a PI agent and student-scientist agents over a shared blackboard. CosmoEvolve autonomously produced beam-aware split-cross pseudo-Cℓ stability diagnostics and pair-/scale-dependent stability windows on ACT DR6 with no predefined objective ([source](https://arxiv.org/abs/2605.14791)).
- **AI co-mathematician** (Lifecycle: Multi-stage, Writing) — Google DeepMind agentic workbench for mathematics research built on Gemini. A project-coordinator agent and parallel workstreams coordinate ideation, literature search, computational exploration, theorem proving, and theory building; outputs center on a living "working paper" with explicit provenance, version history, and preservation of failed explorations. **48%** on FrontierMath Tier 4 (Epoch AI evaluation), reported in the paper as a new high score among AI systems on this tier; adds mathematics as a new domain to the catalogue ([source](https://arxiv.org/abs/2605.06651)).

### Updated
- **`autonomous-science/summary.md`** — added a paragraph in the ML / scientific-computing section covering AIRA (foundation-model architecture discovery) and AutoTTS (automated test-time-scaling controller discovery); created two new domain sections — "Mathematics" (AI co-mathematician with FrontierMath Tier 4 48%) and "Cosmology and astrophysics" (CMBEvolve / CosmoEvolve); appended four new source citations.
- **`autonomous-science/systems/`** — renumbered `nav_order` on the existing 24 system pages to preserve alphabetical ordering after inserting the four new entries.
- **`autonomous-science/curator-state.md`** — replaced `Recently surfaced` with the four new additions (SPARK retained as the fifth, dated 2026-05-22).
- **`sources/manifest.json`** — four new DOI entries with `.txt` sidecars (added by Phase A).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 through 2026-05-22 — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-22

### Added
- **SPARK** (Lifecycle: Multi-stage) — University Hospital Cologne System of Pathology Agents; first *Nature Medicine*-published agentic AI scientist for cancer pathology. Four-module pipeline (idea generation with OpenAI o1, refinement, parameter coding with Claude Sonnet, parameter verification) validated across 18 patient cohorts and >5,400 patients in five cancer types plus a 625-patient spatial-biology breast-cancer dataset; 99.2% of proposed parameters compiled, yielding 1,115 non-redundant prognostic/predictive parameters; open source ([source](https://doi.org/10.1038/s41591-026-04357-y)).
- **Deep Research (BioAgents)** (Lifecycle: Multi-stage) — bio.xyz open-source interactive multi-agent biomedical system with persistent world state across planning, data-analysis, literature, and novelty-detection agents; minute-scale cycles; state-of-the-art 48.8% on BixBench open response (exceeding K-Dense Analyst by 14.4 pts) and 64.4% on MCQ without refusal ([source](https://arxiv.org/abs/2601.12542)).
- **EvoScientist** (Lifecycle: Multi-stage) — Huawei multi-agent evolving AI scientist with a Researcher Agent, Engineer Agent, and Evolution Manager Agent sharing persistent ideation and experimentation memories distilled from prior interactions; outperforms seven open-source and commercial AI-scientist baselines (Virtual Scientist, AI-Researcher, InternAgent, AI Scientist-v2, and others) on idea generation across novelty, feasibility, relevance, and clarity, with notable gains in code-execution success rate ([source](https://arxiv.org/abs/2603.08127)).
- **Jr. AI Scientist** (Lifecycle: Multi-stage, Writing) — University of Tokyo baseline-paper-anchored autoresearch system published in *TMLR* (Feb 2026) with companion risk report; analyzes limitations of a supplied NeurIPS/IJCV/ICLR baseline paper, formulates improvement hypotheses, iterates experiments via modern coding agents, and writes a full manuscript; receives higher DeepReviewer scores than existing fully automated systems and was the basis for Agents4Science submissions ([source](https://arxiv.org/abs/2511.04583)).
- **ARIS** (Lifecycle: Multi-stage, Writing) — Shanghai Jiao Tong University and Shanghai Innovation Institute open-source autonomous research harness; pairs an executor model (e.g., Claude Code) with a reviewer model from a different family (e.g., GPT-5.4 xhigh) as a default cross-family configuration, treating independent assurance as a first-class workflow layer across five workflows (idea discovery, implement & deploy, auto-review, paper writing, rebuttal) ([source](https://arxiv.org/abs/2605.03042)).

### Updated
- **`autonomous-science/summary.md`** — promoted SPARK into the top-tier biology section as the fourth peer-reviewed anchor; added Deep Research (BioAgents) as the open-source interactive counterweight to batch-mode systems and surfaced its BixBench numbers in the benchmarks paragraph; introduced two new architectural patterns (EvoScientist's persistent ideation + experimentation memory; ARIS's cross-model adversarial executor/reviewer pairing) and Jr. AI Scientist's baseline-paper-anchored workflow into the ML/scientific-computing section; added Jr. AI Scientist risk-disclosure as a new open-problem item; expanded the wet-lab validations paragraph with SPARK's prospective pathology evaluation; appended five new source citations.
- **`autonomous-science/systems/`** — renumbered `nav_order` on the existing 19 system pages to preserve alphabetical ordering after inserting the five new entries.
- **`autonomous-science/curator-state.md`** — replaced `Recently surfaced` with the five new additions.
- **`sources/manifest.json`** — five new DOI entries with `.txt` sidecars (added by Phase A).

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 or 2026-05-21 — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-21 (BiomniBench incorporation)

### Updated
- **`autonomous-science/summary.md`** — added BiomniBench-DA under "Standardised benchmarks" with concrete cross-harness numbers (best Claude Code + Opus 4.7 = 73.3/100; harness gap 13.5 pts > model-generation gap 3.8 pts; weakest dimensions: method selection, biological interpretation, scientific reasoning). Updated "Evaluation gaps" open-problem item to note BiomniBench narrows the cross-system benchmarking gap for data-analysis tasks specifically. Appended source citation ([source](https://doi.org/10.64898/2026.05.12.724604)).
- **`autonomous-science/systems/biomni.md`** — added the BiomniBench paper under Other references with a one-line summary of the headline finding; bumped `last_verified`.
- **`sources/manifest.json`** — added DOI entry for `2026.05.12.724604v1.full.pdf` with `.txt` sidecar.
- **`autonomous-science/curator-state.md`** — noted BiomniBench under Recently surfaced (benchmark, not system entry per scope rules).

## 2026-05-21 (Phase B)

### Added
- **Qumus** (Lifecycle: Multi-stage) — Princeton/Sanfeng Wu embodied multi-agent AI quantum-materials experimentalist running in a robotic minilab; first AI creation of graphene and first AI fabrication of atomically thin field-effect transistors via vdW stacking ([source](https://arxiv.org/abs/2605.18407)).
- **Qiushi Discovery Engine** (Lifecycle: Multi-stage) — Zhejiang University dual-layer agentic system coupled to a real free-space optical platform; autonomously identified and experimentally validated "optical bilinear interaction" as a previously unreported physical mechanism in a 206-step open-ended study ([source](https://arxiv.org/abs/2604.27092)).
- **Dr.Sai** (Lifecycle: Analysis, Experiment design) — IHEP/CAS AutoGen-based six-agent system with HEP-RAG and a HepScript DSL that re-measured branching fractions across ten J/ψ decay channels in the BESIII production environment ([source](https://arxiv.org/abs/2604.22541)).
- **GRAFT-ATHENA** (Lifecycle: Multi-stage) — Brown/Karniadakis self-improving agentic framework over factored decision trees with a metric embedding and reward-calibrated nearest-neighbor priors; designs a spectral PINN with exponential convergence, reconstructs Mach-10 hypersonic flow over the Apollo Command Module from a 1968 NASA report, and recovers shear-thinning red-blood-cell rheology ([source](https://arxiv.org/abs/2605.11117)).
- **AI CFD Scientist** (Lifecycle: Multi-stage, Writing) — RPI/Pan group open-source AI scientist for CFD on OpenFOAM via Foam-Agent; vision-language physics-verification gate caught 14 of 16 silent failures missed by solver logs, and the system autonomously discovered a Spalart–Allmaras runtime correction that cut lower-wall Cf RMSE against DNS by 7.89% ([source](https://arxiv.org/abs/2605.06607)).

### Updated
- **`autonomous-science/summary.md`** — added GRAFT-ATHENA and AI CFD Scientist to the machine-learning and scientific-computing section; added a new "Embodied physical-sciences and high-energy systems" section covering Qumus, Qiushi Discovery Engine, and Dr.Sai; expanded the wet-lab/instrument-coupled evaluation paragraph with the new validations; appended six new source citations.
- **`autonomous-science/systems/`** — renumbered `nav_order` on the existing 14 system pages to preserve alphabetical ordering after inserting the five new entries.
- **`autonomous-science/curator-state.md`** — replaced `Recently surfaced` with the five new additions.

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages were `last_verified` on 2026-05-20 or 2026-05-21 — inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-21

### Added
- **Kosmos** (Lifecycle: Multi-stage, Writing) — Edison Scientific's AI scientist; 12-hour autonomous cycles of parallel data analysis, literature search, and hypothesis generation over a structured world model; 79.4% independent statement accuracy; seven highlighted discoveries across metabolomics, materials science, neuroscience, and statistical genetics ([source](https://arxiv.org/abs/2511.02824)).
- **AgenticSciML** (Lifecycle: Hypothesis, Experiment design) — Brown / Karniadakis 10+-agent system for emergent discovery in scientific machine learning; up to four orders of magnitude error reduction over single-agent and human baselines on PINN and operator-learning tasks ([source](https://arxiv.org/abs/2511.07262)).
- **AILA** (Lifecycle: Experiment design, Analysis) — IIT Delhi multi-agent LLM framework for atomic force microscopy, with the AFMBench 100-task evaluation suite; documents an "agent sleepwalking" failure mode with safety implications for SDLs ([source](https://doi.org/10.1038/s41467-025-64105-7)).
- **MARS** (Lifecycle: Multi-stage) — SIAT/CAS hierarchical 19-agent / 16-tool framework with robotic synthesis; optimized perovskite nanocrystal synthesis in 10 iterations and designed a water-stable perovskite composite in 3.5 h ([source](https://doi.org/10.1016/j.matt.2025.102577)).

### Updated
- **`autonomous-science/summary.md`** — promoted Kosmos into the top-tier biology section alongside Co-Scientist and Robin; added AgenticSciML under machine-learning research; rebuilt the chemistry section to chemistry-and-materials and folded in MARS and AILA; added independent-expert-review as a third evaluation regime; added an "instruction adherence in lab settings" open-problem item citing AILA's sleepwalking finding; appended four new source citations.
- **`autonomous-science/systems/`** — renumbered `nav_order` on the nine pre-existing system pages to preserve alphabetical ordering after inserting the four new entries.
- **`autonomous-science/curator-state.md`** — created (was missing); populated `Recently surfaced`, empty `Flagged for review`, and `Deferred — next-run priority` (CORAL, AIDO.Harness, SAGA, Deep Researcher Agent, Virtual Lab).

### Flagged
_None._

### Verified (no changes)
- All existing system pages were `last_verified: 2026-05-20` — one day old, inside the 30-day re-verification window. No spot-checks performed this run.

## 2026-05-20 (medRxiv source test)

### Added
- **OpenScientist** (Lifecycle: Multi-stage) — Washington University agentic AI co-scientist built on Claude Code; evaluated by domain experts across four clinical case studies (Alzheimer's biomarkers, plasma proteomics, single-cell neuroscience, multiple myeloma). Open source under Apache 2.0; code at [openscientist-io/openscientist](https://github.com/openscientist-io/openscientist); web UI at [openscientist.io](https://openscientist.io/) ([source](https://www.medrxiv.org/content/10.64898/2026.03.15.26348338v1)).

### Updated
- **Landscape** — added OpenScientist to the general-purpose biomedical agents section of `summary.md`.
- **Curation rules** — added the medRxiv API as an explicit fallback source alongside bioRxiv, and added a medRxiv-leaning seed query (`"agentic AI co-scientist" biomedical`) to surface clinical co-scientist work on future runs.

## 2026-05-20 (daily run)

### Added
- **AI Scientist (Sakana)** (Lifecycle: Multi-stage, Writing) — Nature 651, 914–919 (2026); v2 produced the first AI-generated peer-reviewed workshop paper ([source](https://arxiv.org/abs/2408.06292), [v2](https://arxiv.org/abs/2504.08066)).
- **Biomni** (Lifecycle: Multi-stage) — Stanford general-purpose biomedical agent; matches expert humans on LAB-Bench DbQA/SeqQA ([source](https://doi.org/10.1101/2025.05.30.656746)).
- **CRISPR-GPT** (Lifecycle: Experiment design, Analysis) — four-agent gene-editing planner across 22 tasks; Nat. Biomed. Eng. 10, 245–258 (2026) ([source](https://doi.org/10.1038/s41551-025-01463-z)).
- **NovelSeek** (Lifecycle: Multi-stage) — closed-loop multi-agent framework reporting time-bounded gains on 12 AI4Science tasks ([source](https://arxiv.org/abs/2505.16938)).

### Updated
- **`sources/manifest.json`** — added five new DOI-keyed entries (AI Scientist v1 arXiv, AI Scientist v2 arXiv, Biomni bioRxiv, NovelSeek arXiv, CRISPR-GPT arXiv) with `pdftotext` sidecars.
- **`autonomous-science/entries.md`** — added four new system blocks (alphabetised between existing entries); refreshed `Recently surfaced` to reflect the new additions; refreshed `Deferred — next-run priority` with Virtual Lab (PDF blocked by Cloudflare this run), MARS, BORA, and the bioRxiv Jan 2026 critical evaluation framework list.
- **`autonomous-science/summary.md`** — rewrote `The landscape today` and `How these systems are evaluated` to incorporate AI Scientist (Sakana), Biomni, CRISPR-GPT, and NovelSeek; added new `Open problems` items on code-execution risk and end-to-end-cycle failure modes; appended five new dated source citations.

### Flagged
_None._

### Verified (no changes)
- ChemCrow, Co-Scientist (Google), Coscientist (CMU), Robin (FutureHouse), Talk2QSP — all five bootstrap entries spot-checked; primary links resolve; `Last verified` left at 2026-05-20 (bootstrap date).

## 2026-05-20

### Added
- **Co-Scientist (Google)** (Lifecycle: Hypothesis, Experiment design) — bootstrap seed from archived Nature paper ([source](https://doi.org/10.1038/s41586-026-10644-y)).
- **Robin (FutureHouse)** (Lifecycle: Multi-stage) — bootstrap seed; first published multi-agent system to integrate hypothesis generation with experimental data analysis ([source](https://doi.org/10.1038/s41586-026-10652-y)).
- **Talk2QSP** (Lifecycle: Experiment design) — bootstrap seed from archived bioRxiv preprint ([source](https://doi.org/10.64898/2026.05.06.723244)).
- **Coscientist (CMU)** (Lifecycle: Experiment design, Analysis) — bootstrap seed grounded in the Gao et al. Cell perspective citation of Boiko et al. Nature 2023 ([source](https://doi.org/10.1016/j.cell.2024.09.022)).
- **ChemCrow** (Lifecycle: Experiment design, Analysis) — bootstrap seed grounded in the Gao et al. Cell perspective citation of Bran et al. Nat. Mach. Intell. 2024 ([source](https://doi.org/10.1016/j.cell.2024.09.022)).

### Updated
- **`sources/manifest.json`** — populated with five DOI-keyed entries for the bootstrap PDFs (Co-Scientist, Robin, Talk2QSP, Gao et al. Cell perspective, Nature news on AI Index 2026).
- **`autonomous-science/entries.md`** — rebuilt from `_pending first run_` placeholder to the five seed entries plus `Recently surfaced` and `Deferred — next-run priority` sections.
- **`autonomous-science/summary.md`** — rebuilt from `_pending first run_` placeholder with the bootstrap landscape view, evaluation summary, open-problem list, and dated source citations.

### Flagged
_None._

### Verified (no changes)
_None — bootstrap run; nothing pre-existed to spot-check._
