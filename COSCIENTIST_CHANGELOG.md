---
title: AI scientist updates
parent: Updates
nav_order: 3
permalink: /updates/ai-scientists.html
---

# AI scientist updates

Reverse-chronological log of changes to the [AI scientists tracker]({{ '/autonomous-science/' | relative_url }}). Newest at the top.

Older entries live in [COSCIENTIST_CHANGELOG_ARCHIVE.md](COSCIENTIST_CHANGELOG_ARCHIVE.md).

## 2026-08-01

### Added
- **AIMS** (Lifecycle: Multi-stage) — Stanford/SIMES uncertainty-aware AI experimentalist that operates a cryogenic microwave impedance microscope end to end on twisted bilayer MoSe2, cutting sample-navigation time from ~10 h to ~4 h and prioritizing a quantum-fluctuation-renormalized origin for the robust ν = 1/2 crystal ([arXiv:2607.16544](https://arxiv.org/abs/2607.16544))
- **AI Sleep Co-Scientist** (Lifecycle: Multi-stage) — Stanford expert-guided agent environment over ~124,000 polysomnography recordings, binding each result to executable code; incident Parkinson's HR 1.48 and Alzheimer's HR 1.38 from diminished network-level sleep coupling ([arXiv:2607.25175](https://arxiv.org/abs/2607.25175))
- **NAIS (NVAITC AI Scientist)** (Lifecycle: Multi-stage, Writing) — NVIDIA governed end-to-end research system keeping protected data inside institutional boundaries; agent-orchestrated hypertension GWAS on 286,422 individuals reproduced FGF5, ATP2B1, CNNM2, FTO, and GRB14 ([arXiv:2607.11084](https://arxiv.org/abs/2607.11084))
- **OmniQEC** (Lifecycle: Multi-stage) — NTU Singapore LLM-orchestrated quantum-error-correction discovery agent optimizing circuit-level logical error rate; beat the BB [[72,12,6]] and [[144,12,12]] codes at complete-implementation budgets of 98 and 240 physical qubits ([arXiv:2607.25865](https://arxiv.org/abs/2607.25865))
- **CogEEGAgent** (Lifecycle: Analysis) — Tohoku University cognitive-EEG agent separating LLM semantic authority from deterministic scientific authority; 39/40 routing accuracy vs 33 for a matched deterministic router, and held-out confirmation cut the null false-positive rate by 11.6 points to 4.9% ([arXiv:2607.25045](https://arxiv.org/abs/2607.25045))

### Updated
- **Landscape synthesis** — added AIMS to the embodied physical-sciences exemplars and noted that the verifiability turn has spread beyond the ML cluster (CogEEGAgent's held-out confirmation, NAIS's governed data broker); `synthesis_reviewed` bumped to 2026-08-01.

### Flagged
- _None._

### Verified (no changes)
- Aging-entry re-verification remains blocked in Phase B (no web tools); the 55-entry link/repo backlog stays logged under `Deferred — next-run priority` and `last_verified` was not bumped for those pages.

## 2026-07-25

No substantive updates — Phase A surfaced no new in-scope systems. Synthesis re-checked against the current grouping (`synthesis_reviewed` 2026-07-18, within the 30-day cadence; no systems added or removed) — all superlatives still hold, no refresh needed. The link/repo re-verification backlog (55+ entries past the 30-day window) remains deferred to Phase A, which alone has the web/MCP tools to confirm link liveness.

## 2026-07-18

### Added
- **CoDHy** (Lifecycle: Hypothesis) — Hannover Medical School (PLRI/CAIMed) with Sanford Burnham Prebys (Younis, Basak, Chavez, Ahmadi; arXiv:2603.00612). An interactive, human-in-the-loop AI co-scientist for biomarker-guided cancer drug-combination hypothesis generation. From a user-specified biomarker, cancer type, and PubMed scope it builds a task-specific Neo4j knowledge graph (structured databases — Reactome, CIViC, TCGA-GDC, ChEMBL, STRING, SynlethDB, DepMap, DrugBank, etc. — plus spaCy-extracted PubMed triples normalized via sentence-transformers), computes Node2Vec embeddings, and runs a hybrid Graph-RAG generation agent, a Llama-3.1-8B validation agent (novelty/plausibility/safety with targeted PubMed grounding → proceed/caution/reject), and a ranking agent (composite graph-evidence + safety score, optional DrugCombDB synergy). Benchmark-only across 7 frozen (biomarker, cancer type) scenarios: Full CoDHy highest exact novelty (35.71%) vs No-Node2Vec (28.57%) and LLM-only (10.71%), diversity 0.89, with a deliberately lower MRR (0.74) reflecting a discovery-over-retrieval bias. Assistive decision support; open source ([source](https://arxiv.org/abs/2603.00612)).

### Updated
- **`autonomous-science/summary.md`** — re-verified the synthesis against the current grouping (CoDHy joins the Biology & medicine hypothesis-generation cluster as a benchmark-validated system and tips no superlative — the "strongest evidence" claim still rests on wet-lab/clinical exemplars) and bumped `synthesis_reviewed` to 2026-07-18.
- **`sources/manifest.json`** — added the CoDHy preprint (arXiv:2603.00612) with its `.txt` sidecar.
- **`autonomous-science/curator-state.md`** — added CoDHy to `Recently surfaced` (trimmed to last 5).

### Flagged
_None._

### Verified (no changes)
- Synthesis re-reviewed against the freshly grouped table after adding CoDHy; all superlatives ("most loop-closed," "strongest evidence," "newest frontier") still hold. The link/repo re-verification backlog (55+ entries past the 30-day window) remains deferred to Phase A — Phase B has no web/MCP tools to confirm link liveness, so `last_verified` dates were not bumped.

## 2026-07-11

### Added
- **ARIA** (Lifecycle: Hypothesis, Analysis) — Johns Hopkins University (Clancy, Van Durme, Yuille groups; KDD '26). A causal-aware LLM framework for trustworthy materials discovery that diagnoses "contextual tunneling" in knowledge-graph-augmented LLMs and gates knowledge use on Process-Structure-Property (PSP) mechanistic completeness, routing each query through a three-tier cascade (direct causal reasoning over complete PSP chains → physics-filtered analogical transfer → parametric fallback). Grounded in a 2,839-relation PSP Causal Knowledge Graph with optional real-time literature enrichment; covers forward property prediction and inverse synthesis-protocol design. Benchmark-only validation on 149 expert-curated 2D-materials tasks: ARIA-FULL +50.6% over baseline on in-domain forward prediction, sustained out-of-domain inverse-design performance, and beats a Self-RAG baseline. Open source ([source](https://doi.org/10.1145/3770855.3818954)).

### Updated
- **`autonomous-science/summary.md`** — added ARIA's primary paper to the Sources list; re-verified the synthesis against the current grouping (ARIA fits the existing Chemistry & materials cluster as a benchmark-validated system and tips no superlative) and bumped `synthesis_reviewed` to 2026-07-11.
- **`autonomous-science/curator-state.md`** — added ARIA to `Recently surfaced` (trimmed to last 5).

### Flagged
_None._

### Verified (no changes)
- Synthesis re-reviewed against the freshly grouped table after adding ARIA; all superlatives ("most loop-closed," "strongest evidence," "newest frontier") still hold. The link/repo re-verification backlog (55+ entries past the 30-day window) remains deferred to Phase A — Phase B has no web/MCP tools to confirm link liveness, so `last_verified` dates were not bumped.

## 2026-07-04

No new systems surfaced — Phase A's seed queries (arXiv, bioRxiv, medRxiv via `papers` MCP, plus WebSearch fallback) returned only out-of-scope work and already-catalogued systems, so the handoff was `_None._`.

### Updated
- **`autonomous-science/curator-state.md`** — refreshed the link/repo re-verification backlog to the 55 entries now past the 30-day window (last_verified 2026-05-20 through 2026-06-02).

### Flagged
_None._

### Verified (no changes)
- 55 entries have crossed the 30-day re-verification window (last_verified 2026-05-20 through 2026-06-02). Phase B has no web/MCP tools to confirm primary-paper-link or code-repo liveness, so `last_verified` was intentionally not bumped; the backlog is logged under `Deferred — next-run priority` for the next Phase A to fetch. `summary.md` synthesis last reviewed 2026-06-27 (7 days ago) and no systems were added or removed this run, so it remains within the 30-day cadence — no re-verification required.

## 2026-06-27

### Added
- **ARTIQ-MCP (Duke trapped-ion agent)** (Lifecycle: Experiment design, Analysis) — Duke Quantum Center (Brown and Linke groups) with University of Maryland. An LLM agent (Claude Opus 4.8) that autonomously writes native ARTIQ control code and runs it on real trapped-ion quantum hardware behind a per-call hardware safety filter: a `safety-filter` MCP proxy issues a content-bound, single-use authorization token only after an AST denylist check plus isolated `dax.sim` simulation that traces every operation against preset per-device bounds (block-by-default on unmapped devices), or a human token for sensitive actions; an `artiq-mcp` server then forwards approved calls to the ARTIQ master over sipyco. Wet-lab validation on a co-trapped 40Ca+/40CaOH+ crystal (full agent-built calibration stack; cross-instrument 60 Hz magnetic-field-stabilization loop) plus interface-level portability on an independent 171Yb+ ARTIQ platform; safety filter red-teamed with 1932 adversarial scripts. Open source ([source](https://arxiv.org/abs/2606.27231)).

### Updated
- **`autonomous-science/summary.md`** — ARTIQ-MCP joins the existing "Physical sciences and embodied systems are the newest frontier" cluster (Qumus, Qiushi, Dr.Sai, BioProVLA, CALMS), tipping no superlative: Biology & medicine remains the largest group (17) and strongest-evidence tier; Chemistry & materials (14) remains the most loop-closed. No synthesis prose was rewritten; `synthesis_reviewed` bumped to 2026-06-27 after re-checking every superlative against the current 67-system grouping.
- **`autonomous-science/curator-state.md`** — added ARTIQ-MCP at the top of `Recently surfaced` (trimming Ax-Prover to keep the window at five); refreshed the link/repo re-verification backlog to the 37 entries now past the 30-day window.
- **`sources/manifest.json`** — ARTIQ-MCP (DOI 10.48550/arXiv.2606.27231) entry added by Phase A.

### Flagged
_None._

### Verified (no changes)
- 37 entries have crossed the 30-day re-verification window (last_verified 2026-05-20 through 2026-05-27). Phase B has no web/MCP tools to confirm primary-paper-link or code-repo liveness, so `last_verified` was intentionally not bumped; the backlog is logged under `Deferred — next-run priority` for the next Phase A to fetch.

## 2026-06-20

### Added
- **CALMS** (Lifecycle: Experiment design, Analysis) — Argonne National Laboratory (Center for Nanoscale Materials + Advanced Photon Source; Vriza, Prince, Zhou, Chan, Cherukara) AutoGen-based multi-agent framework that operates two real scientific user facilities — a Hard X-ray Nanoprobe (HXN) beamline and an N9 robotic thin-film station. Specialized agents (code writer, code critic, administrator, paper scraper, image explainer, teachability) orchestrate multistep workflows, interpret multimodal nano-diffraction/nano-fluorescence images, and learn on the job by storing human guidance as input–output pairs in a ChromaDB vector store (with a similarity threshold to skip redundant memories). Live demos: natural-language → correct 2D-scan commands and cross-modality scan-region selection at HXN (only o3 reliably reasoned across modalities with high positional precision), and end-to-end fabrication of a defect-free PEDOT:PSS thin film after the literature-scraper agent extracted coating parameters (90 °C, 1 mm/s) from a PDF — teachability markedly improved long-horizon sequential success. Open source ([source](https://arxiv.org/abs/2509.00098)).

### Updated
- **`autonomous-science/summary.md`** — added the CALMS primary-paper link to Sources. CALMS fits the existing "Chemistry and materials are the most loop-closed" / embodied-instrument pattern (alongside MARS, AMASE, MAD, Qumus) and tips no superlative (Biology & medicine remains the largest group and strongest-evidence tier), so no synthesis prose was rewritten; `synthesis_reviewed` last refreshed 2026-06-11, within the 30-day cadence.
- **`autonomous-science/curator-state.md`** — added CALMS at the top of `Recently surfaced` (trimming SAGA to keep the window at five); deferred BioMedAgent and logged the link/repo re-verification backlog.
- **`sources/manifest.json`** — CALMS (DOI 10.48550/arXiv.2509.00098) entry added by Phase A.

### Deferred
- **BioMedAgent / CAS** (Bu et al., *Nat. Biomed. Eng.*, doi:10.1038/s41551-026-01634-6, 2026) — named, benchmark-validated autonomous biomedical-analysis agent (CAS; BioMed-AQA, 327 tasks, ~77% success; generalizes to BixBench), in-scope as an analysis-stage system. Phase A located no openly downloadable PDF (closed access, no preprint), so Phase B could not ground a page; deferred until a citable open source is available ([source](https://doi.org/10.1038/s41551-026-01634-6)).

### Flagged
_None._

### Verified (no changes)
- 19 bootstrap entries crossed the 30-day window today (last_verified 2026-05-20/21). Phase B has no web/MCP tools to confirm link/repo liveness, so `last_verified` was intentionally not bumped; the backlog is logged under `Deferred — next-run priority` for the next Phase A to fetch.

## 2026-06-13

No new systems surfaced — seed queries (arXiv, bioRxiv, medRxiv via `papers` MCP, plus WebSearch fallback) returned only out-of-scope work and already-catalogued systems.

### Deferred
- **EurekAgent** (arXiv:2606.13662, Tsinghua + Zhipu AI) — metric-driven autonomous-discovery agent ("environment engineering"; open-sourced) with new SOTA on circle packing, an autocorrelation inequality, a TriMul kernel, and an MLE-Bench subset for ~$11 API cost. Scope-edge: an optimization/discovery substrate on math/kernel/ML benchmarks, not natural-science hypothesis generation, experiment design, or data analysis. PDF archived and logged in the manifest; deferred pending a more science-leaning case ([source](https://arxiv.org/abs/2606.13662)).

### Verified (no changes)
- All system pages remain inside the 30-day re-verification window (oldest verified 2026-05-20, 24 days ago); no spot-checks required. `summary.md` synthesis last reviewed 2026-06-11 (2 days ago), within cadence — no re-verification needed.

## 2026-06-11

### Added
- **ATLAS** (Lifecycle: Multi-stage) — Google DeepMind (Éltető, Daw, Stachenfeld, Miller; with Princeton/Columbia/UCL) "Active Theory Learning for Automated Science," an active-learning framework — not an LLM orchestration — that closes the hypothesis-generation ↔ experiment-design loop to discover interpretable mechanistic models of behavior. It iterates a Hypothesis Generator (an ensemble of sparse Disentangled RNNs whose latent-variable interactions form candidate computational graphs), an Experiment Optimizer (hill-climbs binary reward-matrix designs to maximize ensemble disagreement / expected information gain, BALD-style), and an Experiment Runner that executes the chosen design. Validation is in-silico (benchmark-tier): recovering Q-learning and Leaky Actor-Critic agents from bandit behavior, scored on behavioral, structural, and dynamical (bisimulation) similarity. **5–10× sample-efficiency gain over random experimentation, 8/8 correct computational-graph recovery in 100 experiments where baselines needed ~1,000, and matched or surpassed expert-designed experiments.** Adds a non-LLM, cognitive-science exemplar to the ML & scientific-computing cluster. No code released ([source](https://arxiv.org/abs/2606.12386)).

### Updated
- **`autonomous-science/summary.md`** — added the ATLAS primary-paper link to Sources; re-verified every synthesis claim against the current grouping and bumped `synthesis_reviewed` to 2026-06-11. ATLAS fits the existing "ML & scientific computing is a large, benchmark-validated cluster" pattern and tips no superlative (Biology & medicine remains the largest group and strongest-evidence tier), so no synthesis prose was rewritten.
- **`autonomous-science/curator-state.md`** — added ATLAS at the top of `Recently surfaced` (trimming OriGene to keep the window at five).
- **`sources/manifest.json`** — ATLAS (DOI 10.48550/arXiv.2606.12386) entry added by Phase A.

### Flagged
_None._

### Verified (no changes)
- All pre-existing system pages remain inside the 30-day re-verification window (oldest additions verified 2026-05-20, 22 days ago); no spot-checks required this run.

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

