---
title: Landscape
parent: AI scientists
nav_order: 1
---

# The autonomous AI scientist landscape

An autonomous AI scientist is a named software system that takes meaningful initiative across one or more of three primary stages: **hypothesis generation** (proposing novel, testable scientific claims rather than retrieving existing ones), **experiment design** (choosing experiments that discriminate between hypotheses, optimizing protocols), and **analysis** (interpreting experimental data, fitting models, drawing inferences). Closing the full loop — hypothesize, design, analyze — is the explicit ambition described in the Gao et al. *Cell* perspective ([2024](https://doi.org/10.1016/j.cell.2024.09.022)).

## Wet-lab and data-driven biology

Three systems with major peer-reviewed papers anchor the biology end of the landscape:

- [**Co-Scientist**](systems/co-scientist-google.html) (Google) — a Gemini-based multi-agent reasoning engine focused on hypothesis generation, using a generation/reflection/ranking/evolution ensemble with Elo-style tournaments. Validated on three biomedical case studies: AML drug repurposing, liver-fibrosis target discovery in organoids, and recapitulation of an unpublished AMR gene-transfer mechanism. Code unreleased ([Gottweis et al., *Nature* 2026](https://doi.org/10.1038/s41586-026-10644-y)).
- [**Robin**](systems/robin.html) (FutureHouse) — the first multi-agent system to integrate hypothesis generation with experimental data analysis in a lab-in-the-loop workflow. Built on the Aviary framework, Robin orchestrates PaperQA2 literature agents with the Jupyter-native Finch analysis agent. Applied to dry age-related macular degeneration, Robin identified ripasudil and KL001 as in vitro hits and proposed an RNA-seq follow-up implicating ABCA1 ([Ghareeb et al., *Nature* 2026](https://doi.org/10.1038/s41586-026-10652-y)).
- [**Kosmos**](systems/kosmos.html) (Edison Scientific, FutureHouse's commercial spinout) — direct successor to Robin. Runs up to 12-hour cycles of parallel data analysis, literature search, and hypothesis generation against a structured world model shared across ~200 agent rollouts; cites every statement back to code or primary literature. Independent expert review judged 79.4% of statements in Kosmos reports accurate; collaborators rated a 20-cycle run equivalent to ~6 months of their own work. Seven highlighted discoveries span metabolomics, materials science, neuroscience, and statistical genetics (three reproduce unseen preprints; four claimed novel) ([Mitchener et al., arXiv:2511.02824](https://arxiv.org/abs/2511.02824)).

## Machine-learning and scientific-computing research

[**AI Scientist**](systems/ai-scientist-sakana.html) (Sakana AI) is an end-to-end loop that generates ideas, codes and runs experiments, writes a LaTeX manuscript, and reviews itself via an Automated Reviewer. AI Scientist-v2 produced the first AI-generated paper to pass human peer review at an ICLR 2025 workshop ([Lu et al., *Nature* 651, 914–919 (2026)](https://sakana.ai/ai-scientist-nature/); [v2 preprint arXiv:2504.08066](https://arxiv.org/abs/2504.08066)).

[**AgenticSciML**](systems/agenticsciml.html) (Brown / Karniadakis group) targets scientific machine learning specifically. More than ten specialized agents — proposers, critics, engineers, retrievers, evaluators — collaborate through structured debate, retrieval-augmented method memory, and ensemble-guided evolutionary search to discover new PINN, neural-operator, and PDE-constrained learning strategies. Reports up to four orders of magnitude error reduction over single-agent and human-designed baselines, including adaptive domain-decomposed PINNs not present in the curated knowledge base ([Jiang & Karniadakis, arXiv:2511.07262](https://arxiv.org/abs/2511.07262)).

[**GRAFT-ATHENA**](systems/graft-athena.html) (Brown / Karniadakis follow-up) introduces a self-improving substrate that accumulates methodological experience across problems. GRAFT projects DAGs of solver attributes into factored decision trees with a deterministic metric embedding; each solved instance becomes a fingerprinted entry in a persistent memory, and nearest-neighbor retrieval supplies a reward-calibrated prior for new problems. Reaches near-machine-precision on PIML benchmarks, reconstructs Mach-10 hypersonic flow over the Apollo Command Module from a 1968 NASA report, recovers shear-thinning red-blood-cell rheology in dissipative particle dynamics, and autonomously designs a spectral PINN with exponential convergence ([Toscano et al., arXiv:2605.11117](https://arxiv.org/abs/2605.11117)).

[**AI CFD Scientist**](systems/ai-cfd-scientist.html) (RPI / Pan group) extends the AI-scientist loop from software-only ML into high-fidelity physical simulators. Running on OpenFOAM via Foam-Agent, three coupled pathways handle parameter sweeps, case-local C++ library compilation, and open-ended hypothesis search. A vision-language physics-verification gate inspects rendered flow fields before any result is accepted — it caught 14 of 16 silent failures missed by solver-level checks in a planted-failure ablation. The system autonomously discovered a Spalart–Allmaras runtime correction reducing lower-wall Cf RMSE against DNS by 7.89% on the periodic hill ([Somasekharan et al., arXiv:2605.06607](https://arxiv.org/abs/2605.06607)).

## General-purpose biomedical agents

- [**Biomni**](systems/biomni.html) (Stanford / Snap group) couples an environment of 150 tools, 105 packages, and 59 databases (Biomni-E1) with a code-executing planner (Biomni-A1). On LAB-Bench it matches expert humans (74.4% DbQA, 81.9% SeqQA) and scores 17.3% on a 14-subfield HLE subset.
- [**OpenScientist**](systems/openscientist.html) (Washington University in St. Louis) is an Apache-2.0 agentic co-scientist built on Claude Code with a public collection of biomedical Agent Skills. Evaluated by domain experts across four clinical case studies — Alzheimer's biomarkers (SEABIRD cohort, identified `%ptau217` as best predictor in 40 minutes), plasma proteomic survival, single-cell transcriptomics in neurofibrillary tangles, and multiple-myeloma hypothesis generation validated in an external cohort ([Roberts et al., *medRxiv* 2026.03.15.26348338](https://www.medrxiv.org/content/10.64898/2026.03.15.26348338v1)).
- [**CRISPR-GPT**](systems/crispr-gpt.html) (Stanford / Princeton) is a four-agent planner spanning 22 gene-editing tasks across knockout, base, prime, and epigenetic editing; full code is withheld pending US regulatory clarity ([Qu et al., *Nat. Biomed. Eng.* 2026](https://doi.org/10.1038/s41551-025-01463-z)).

## Chemistry and materials

Chemistry and materials remain the most loop-closed domains. [**Coscientist (CMU)**](systems/coscientist-cmu.html) and [**ChemCrow**](systems/chemcrow.html) cover autonomous synthesis planning and execution on physical and tool-augmented stacks respectively. [**MARS**](systems/mars.html) (SIAT, Chinese Academy of Sciences) extends that pattern to perovskite materials: a hierarchical 19-agent / 16-tool framework — Orchestrator, Scientist, Engineer, Executor, Analyst — paired with a robotic synthesis platform optimized perovskite nanocrystal synthesis within 10 iterations and designed a biomimetic "core-shell-corona" water-stable perovskite composite in 3.5 hours of system time, a claimed ~60× acceleration versus the conventional 4–6-month manual route ([Shi et al., *Matter* 9, 102577 (2026)](https://doi.org/10.1016/j.matt.2025.102577)). [**AILA**](systems/aila.html) (IIT Delhi) takes the same multi-agent recipe to atomic force microscopy and ships **AFMBench**, a 100-task evaluation suite that exposes failure modes including "agent sleepwalking" (deviation from supplied instructions) with explicit safety implications for self-driving labs ([Mandal et al., *Nat. Commun.* 16:9104 (2025)](https://doi.org/10.1038/s41467-025-64105-7)). At the assistive end, [**Talk2QSP**](systems/talk2qsp.html) (Sanofi/bmedx) maps literature scenarios onto executable quantitative systems pharmacology models with dynamic human-in-the-loop interaction.

## Embodied physical-sciences and high-energy systems

A fast-growing cluster of systems pushes autonomous AI past simulators into real lab hardware in physics-heavy domains:

- [**Qumus**](systems/qumus.html) (Princeton / Sanfeng Wu group) is an embodied multi-agent system that fabricates atomically thin 2D quantum materials inside a robotic minilab integrating Scotch-tape exfoliation, optical inspection, vdW stacking, and storage. Reports the first AI creation of graphene and the first AI fabrication of atomically thin field-effect transistors via vdW stacking, with autonomous error correction during multi-hour closed-loop runs ([Shi et al., arXiv:2605.18407](https://arxiv.org/abs/2605.18407)).
- [**Qiushi Discovery Engine**](systems/qiushi-discovery-engine.html) (Zhejiang University) couples a dual-layer multi-agent architecture and Meta-Trace memory to a free-space optical platform with >2M-pixel SLM control. In a 206-step open-ended study (3,242 LLM calls, 1,242 tool calls), it identified and experimentally validated "optical bilinear interaction" — a previously unreported physical mechanism structurally analogous to Transformer-style query–key compatibility ([Yang et al., arXiv:2604.27092](https://arxiv.org/abs/2604.27092)).
- [**Dr.Sai**](systems/dr-sai.html) (IHEP, Chinese Academy of Sciences) is the first named agentic AI scientist deployed inside a major collider collaboration. An AutoGen-based six-agent stack with HEP-RAG and a HepScript DSL translates natural-language physics goals into BESIII analysis chains using CERN ROOT and BOSS, validated by re-measuring branching fractions across ten J/ψ decay channels in agreement with established benchmarks ([He et al., arXiv:2604.22541](https://arxiv.org/abs/2604.22541)).

## Closed-loop multi-domain frameworks

[**NovelSeek**](systems/novelseek.html) (Shanghai AI Lab) is a closed-loop multi-agent framework reporting time-bounded gains on 12 AI-for-Science tasks and a head-to-head idea-quality comparison against AI Scientist-v2.

Other notable systems being tracked for inclusion: **Virtual Lab** (Stanford / CZ Biohub, *Nature* 2025 — designed novel SARS-CoV-2 nanobodies), **BORA** (LLM + Bayesian optimization, *Digital Discovery* February 2026), **CORAL** (multi-agent evolutionary discovery, arXiv 2604.01658), **STORM**, **Aviary**, and **AutoBa**.

## How these systems are evaluated

Evaluation now spans three regimes.

**Wet-lab and instrument-coupled validations** remain the strongest evidence: Co-Scientist's in vitro AML hits and organoid-confirmed fibrosis targets; Robin's ripasudil/KL001 confirmations; CMU Coscientist's robotic cross-couplings; CRISPR-GPT's non-expert case study; MARS's robotic perovskite synthesis loop; AILA's five real-world AFM experiments; Qumus's AI fabrication of graphene and vdW field-effect transistors; Qiushi Engine's autonomous discovery and experimental validation of optical bilinear interaction on a real optical platform; Dr.Sai's reproduction of ten J/ψ branching fractions in the BESIII production environment; and AI CFD Scientist's vision-gated discovery of a Spalart–Allmaras correction validated against DNS.

**Independent expert review of system reports** has emerged with Kosmos: scientist evaluators classified 102 statements drawn from three reports as Supported or Refuted, with 79.4% Supported. Collaborators independently rated a 20-cycle Kosmos run as equivalent to roughly six months of their own research time.

**Standardised benchmarks** have grown: Biomni reports LAB-Bench DbQA/SeqQA and HLE numbers against human-expert baselines; AI Index 2026 coverage notes PaperArena (best agent 39%) and that the best AI agents score roughly half as well as human PhDs on multistep tasks ([*Nature* news, April 2026](https://doi.org/10.1038/d41586-026-01199-z)).

**Internal head-to-head studies** are appearing: NovelSeek vs. AI Scientist-v2 on idea novelty; Sakana's Automated Reviewer benchmarked against NeurIPS-scale human agreement (~69% balanced accuracy). MoSciBench, BixBench, MLE-Bench, ScienceAgentBench, and SciCode are referenced in the broader landscape but not yet evidenced in primary citations here.

## Open problems

- **Hallucination of references.** Robin's ablations show that removing PaperQA2-based agents (Crow/Falcon) dramatically increases hallucinated citations; the AI Scientist papers report similar inaccuracies in citations and figures.
- **Reproducibility of analyses.** Robin runs eight Finch trajectories and consensuses; Gao et al. flag reproducibility and rigorous peer review of agentic research as open challenges.
- **Originality versus retrieval.** Gao et al. argue current foundation models may struggle to produce hypotheses outside their training distribution — a structural limit on hypothesis-generation claims. A *bioRxiv* critical evaluation (January 2026, 10.64898/2026.01.05.697809) reports that none of eight open-source frameworks completed a full research cycle end-to-end.
- **Code-execution risk and dual use.** Biomni notes its agent executes LLM-generated code with full system privileges by default; CRISPR-GPT withholds full code pending regulatory clarity; Co-Scientist authors cite safety implications as a reason for not releasing source; Robin notes RLHF and platform-level controls against malicious protocol generation. MARS isolates code execution in Docker.
- **Instruction adherence in lab settings.** AILA's AFMBench evaluation documents an "agent sleepwalking" failure mode in which agents deviate from supplied instructions, and finds that materials-science question-answering proficiency does not transfer to laboratory operation — a direct warning for self-driving-lab deployments.
- **Evaluation gaps.** Few head-to-head studies share benchmarks across the systems above; the AI Index Report 2026 notes that even the best agents lag human PhDs by ~2× on multistep tasks.

## Sources

- [Gottweis et al., "Accelerating scientific discovery with Co-Scientist," *Nature*](https://doi.org/10.1038/s41586-026-10644-y)
- [Ghareeb et al., "A multi-agent system for automating scientific discovery" (Robin), *Nature*](https://doi.org/10.1038/s41586-026-10652-y)
- [Kazemeini et al., "Talk2QSP," *bioRxiv* 2026.05.06.723244](https://doi.org/10.64898/2026.05.06.723244)
- [Gao et al., "Empowering biomedical discovery with AI agents," *Cell* 187 (2024)](https://doi.org/10.1016/j.cell.2024.09.022)
- [*Nature* news, "Human scientists beat the best AI agents…" (AI Index Report 2026 coverage)](https://doi.org/10.1038/d41586-026-01199-z)
- [Boiko et al., "Autonomous chemical research with large language models," *Nature* 624 (2023)](https://doi.org/10.1038/s41586-023-06792-0)
- [Bran et al., "Augmenting large language models with chemistry tools," *Nat. Mach. Intell.* (2024)](https://doi.org/10.1038/s42256-024-00832-8)
- [Lu et al., "The AI Scientist," arXiv:2408.06292 / *Nature* 651, 914–919 (2026)](https://arxiv.org/abs/2408.06292)
- [Yamada et al., "The AI Scientist-v2," arXiv:2504.08066](https://arxiv.org/abs/2504.08066)
- [Huang et al., "Biomni: A General-Purpose Biomedical AI Agent," *bioRxiv* 2025.05.30.656746](https://doi.org/10.1101/2025.05.30.656746)
- [Qu et al., "CRISPR-GPT for agentic automation of gene-editing experiments," *Nat. Biomed. Eng.* 10, 245–258 (2026)](https://doi.org/10.1038/s41551-025-01463-z)
- [Roberts et al., "OpenScientist: evaluating an open agentic AI co-scientist to accelerate biomedical discovery," *medRxiv* 2026.03.15.26348338](https://www.medrxiv.org/content/10.64898/2026.03.15.26348338v1)
- [NovelSeek Team, arXiv:2505.16938](https://arxiv.org/abs/2505.16938)
- [Mitchener et al., "Kosmos: An AI Scientist for Autonomous Discovery," arXiv:2511.02824](https://arxiv.org/abs/2511.02824)
- [Jiang & Karniadakis, "AgenticSciML," arXiv:2511.07262](https://arxiv.org/abs/2511.07262)
- [Mandal et al., "Evaluating large language model agents for automation of atomic force microscopy" (AILA / AFMBench), *Nat. Commun.* 16:9104 (2025)](https://doi.org/10.1038/s41467-025-64105-7)
- [Shi et al., "Knowledge-driven autonomous materials research via collaborative multi-agent and robotic system" (MARS), *Matter* 9, 102577 (2026)](https://doi.org/10.1016/j.matt.2025.102577)
- [Shi et al., "Qumus: Realization of An Embodied AI Quantum Material Experimentalist," arXiv:2605.18407](https://arxiv.org/abs/2605.18407)
- [Yang et al., "End-to-end autonomous scientific discovery on a real optical platform" (Qiushi Discovery Engine), arXiv:2604.27092](https://arxiv.org/abs/2604.27092)
- [He et al., "Dr.Sai: An agentic AI for real-world physics analysis at BESIII," arXiv:2604.22541](https://arxiv.org/abs/2604.22541)
- [Toscano et al., "GRAFT-ATHENA: Self-Improving Agentic Teams for Autonomous Discovery and Evolutionary Numerical Algorithms," arXiv:2605.11117](https://arxiv.org/abs/2605.11117)
- [Somasekharan et al., "AI CFD Scientist," arXiv:2605.06607](https://arxiv.org/abs/2605.06607)
