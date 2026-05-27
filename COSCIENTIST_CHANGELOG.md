---
title: AI scientist updates
parent: Updates
nav_order: 3
permalink: /updates/ai-scientists.html
---

# AI scientist updates

Reverse-chronological log of changes to the [AI scientists tracker](autonomous-science/). Newest at the top.

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
