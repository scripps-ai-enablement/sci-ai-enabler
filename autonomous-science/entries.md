# Autonomous AI scientist systems

> Named systems that perform hypothesis generation, experiment design, or analysis with meaningful autonomy. Manuscript writing is a downstream subcomponent, not a peer stage — writing-only systems are out of scope. See [`summary.md`](summary.md) for the landscape view and [`../COSCIENTIST_AGENT.md`](../COSCIENTIST_AGENT.md) for the curation rules.

_Last updated: 2026-05-20._

## Systems

### AI Scientist (Sakana)

- **Affiliation**: Sakana AI, with FLAIR (Oxford), University of British Columbia, Vector Institute ([Sakana AI](https://sakana.ai/))
- **First introduced**: 2024-08 (arXiv v1); v2 preprint 2025-04; published in Nature 2026-03
- **Lifecycle stages**: Multi-stage, Writing
- **Autonomy level**: Fully autonomous (within a fixed code-template starting point for v1; v2 removes the template requirement)
- **Domain focus**: Machine-learning research (diffusion modelling, transformer LMs, learning dynamics in v1; broader ML domains in v2)
- **Approach**: End-to-end LLM agent that generates research ideas, searches literature, writes/executes code, runs experiments, produces figures and a full LaTeX manuscript, and runs an Automated Reviewer (Area-Chair-style ensemble of five LLM reviews). v2 replaces v1's human-written code templates with a progressive agentic tree search managed by a dedicated experiment-manager agent.
- **Availability**: Open source (v1 code on GitHub; v2 codebase open-sourced alongside the preprint)
- **Validation**: v1 generated full ML papers at ~$15 per paper and reported papers exceeding a top-ML-conference acceptance threshold under the Automated Reviewer; v2 submitted three fully AI-generated manuscripts to an ICLR 2025 workshop, with one accepted at the "I Can't Believe It's Not Better" (ICBINB) workshop — the first AI-generated paper to pass human peer review. The Nature paper reports a scaling law tying paper quality to underlying foundation-model capability.
- **Notable results**: First end-to-end AI-generated paper to pass peer review (ICLR 2025 workshop, v2); Automated Reviewer reaches ~69% balanced accuracy on NeurIPS-style review tasks (v1).
- **Primary paper**: [Lu et al., "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery," arXiv:2408.06292](https://arxiv.org/abs/2408.06292); peer-reviewed version Lu et al., Nature 651, 914–919 (2026)
- **Other references**: [Yamada et al., "The AI Scientist-v2," arXiv:2504.08066](https://arxiv.org/abs/2504.08066); [Sakana AI Nature announcement](https://sakana.ai/ai-scientist-nature/); [Nature news, "How to build an AI scientist"](https://www.nature.com/articles/d41586-026-00899-w)
- **Code**: [AI-Scientist (v1)](https://github.com/SakanaAI/AI-Scientist) and [AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)
- **Local source files**: `sources/2408.06292v5.pdf`, `sources/2504.08066v1.pdf`
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### Biomni

- **Affiliation**: Stanford University (Snap group, Leskovec lab), with Genentech, Arc Institute, Princeton, University of Washington, UCSF ([Biomni](https://biomni.stanford.edu/))
- **First introduced**: 2025-05 (bioRxiv preprint 2025.05.30.656746)
- **Lifecycle stages**: Multi-stage (experiment design, analysis, hypothesis generation)
- **Autonomy level**: Semi-autonomous (closed-loop with checkpoints; LLM-generated code is executed with system privileges by default)
- **Domain focus**: Biomedicine (general purpose across 25 biomedical subfields)
- **Approach**: Two-component agent. **Biomni-E1** is an environment mined from tens of thousands of biomedical publications, exposing 150 specialized tools, 105 software packages, and 59 databases as a unified action space. **Biomni-A1** is an LLM agent that dynamically selects tools, plans tasks, and executes Python code that composes loops, parallelization, and conditional steps; an adaptive planning loop iteratively refines plans during execution.
- **Availability**: Open source (Apache-2.0 for Biomni itself; integrated tools/databases may carry separate licenses); free no-code web UI at biomni.stanford.edu
- **Validation**: On LAB-Bench, 74.4% accuracy on DbQA (vs. 74.7% human experts) and 81.9% on SeqQA (vs. 78.8% human experts); on a 52-question HLE subset spanning 14 biomedical subfields, 17.3% accuracy (reported as a 4× improvement over base LLMs in the paper). Real-world case studies: 10-step wearable-sensor pipeline analyzing 458 files and 227 nights of sleep data; multi-omics processing of >336,000 single-nucleus RNA-seq/ATAC-seq profiles.
- **Notable results**: Matched or exceeded expert performance on LAB-Bench DbQA/SeqQA; autonomously authored multi-stage bioinformatics pipelines with figures and reports across heterogeneous biomedical data types.
- **Primary paper**: [Huang et al., "Biomni: A General-Purpose Biomedical AI Agent," bioRxiv 2025.05.30.656746](https://doi.org/10.1101/2025.05.30.656746)
- **Other references**: [Biomni project page](https://biomni.stanford.edu/); [GitHub README and DETAILS.md](https://github.com/snap-stanford/Biomni)
- **Code**: [Repo](https://github.com/snap-stanford/Biomni)
- **Local source files**: `sources/biomni_paper.pdf`
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### ChemCrow

- **Affiliation**: EPFL / University of Rochester ([Bran et al.](https://www.nature.com/articles/s42256-024-00832-8))
- **First introduced**: 2023-04 (arXiv preprint; Nature Machine Intelligence 2024)
- **Lifecycle stages**: Experiment design, Analysis
- **Autonomy level**: Semi-autonomous (closed-loop with checkpoints)
- **Domain focus**: Chemistry (organic synthesis, reaction planning)
- **Approach**: GPT-4 driven agent that combines chain-of-thought reasoning with 18 expert-designed chemistry tools (retrosynthesis, molecule property lookup, web/literature search, reaction execution). The agent plans, calls tools, and integrates results to complete chemistry tasks.
- **Availability**: Open source
- **Validation**: Demonstrated on synthesis planning tasks (e.g., insect repellent, organocatalyst, novel chromophore); evaluated by expert chemists and an LLM grader against an unaugmented GPT-4 baseline.
- **Notable results**: Autonomously planned and executed syntheses; outperformed GPT-4 baseline on expert and automated chemistry evaluations per the Gao et al. Cell perspective citation.
- **Primary paper**: [Bran et al., "Augmenting large language models with chemistry tools," Nat. Mach. Intell. 2024](https://doi.org/10.1038/s42256-024-00832-8)
- **Other references**: [Gao et al., Cell Perspective 2024](https://doi.org/10.1016/j.cell.2024.09.022) (cites ChemCrow as a Level 1 agent example)
- **Code**: [Repo](https://github.com/ur-whitelab/chemcrow-public)
- **Local source files**: `sources/1-s2.0-S0092867424010705-main.pdf` (Cell perspective citing ChemCrow)
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### Co-Scientist (Google)

- **Affiliation**: Google Cloud AI Research / Google DeepMind / Google Research, with collaborators at Stanford, Imperial College London, and Houston Methodist ([Google Research](https://research.google/))
- **First introduced**: 2025-02 (initial blog announcement); peer-reviewed paper accepted 2026-05
- **Lifecycle stages**: Hypothesis, Experiment design
- **Autonomy level**: Semi-autonomous (scientist-in-the-loop collaborative paradigm)
- **Domain focus**: General; validated in biomedicine (drug repurposing, target discovery, antimicrobial resistance)
- **Approach**: Multi-agent system built on Gemini comprising specialized agents (Generation, Reflection, Ranking, Evolution, Proximity, Meta-review) coordinated via an asynchronous task framework. Uses self-play scientific debate for hypothesis generation, an Elo-style tournament to compare hypotheses, and an evolution loop to refine them by scaling test-time compute.
- **Availability**: Closed / API only — full source not public; experimental access program announced; Gemini foundation model accessible via Google APIs.
- **Validation**: Three biomedical case studies — drug repurposing for acute myeloid leukemia (AML) with in vitro confirmation; novel epigenetic targets for liver fibrosis confirmed in human hepatic organoids; recapitulation of a then-unpublished bacterial gene-transfer mechanism in antimicrobial resistance discovered independently by collaborators at Imperial College.
- **Notable results**: Identified novel single-agent and combination repurposing candidates for AML showing selective cytotoxicity at clinically relevant concentrations; ranked epigenetic targets with anti-fibrotic activity in organoids; independently recapitulated an unpublished AMR gene-transfer mechanism.
- **Primary paper**: [Gottweis et al., "Accelerating scientific discovery with Co-Scientist," Nature 2026](https://doi.org/10.1038/s41586-026-10644-y)
- **Other references**: [Nature news on AI agents in science (AI Index 2026)](https://doi.org/10.1038/d41586-026-01199-z); [arXiv preprint, "Towards an AI co-scientist," 2502.18864](https://arxiv.org/abs/2502.18864)
- **Code**: Not released (pseudocode and system prompts provided in supplementary notes)
- **Local source files**: `sources/s41586-026-10644-y_reference.pdf`
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### Coscientist (CMU)

- **Affiliation**: Carnegie Mellon University, Gomes Lab ([Boiko et al.](https://www.nature.com/articles/s41586-023-06792-0))
- **First introduced**: 2023-12 (Nature)
- **Lifecycle stages**: Experiment design, Analysis
- **Autonomy level**: Fully autonomous (within a closed-loop chemistry workstation)
- **Domain focus**: Chemistry (catalysis, palladium-catalyzed cross-couplings)
- **Approach**: GPT-4 acts as a planner that orchestrates web search, documentation retrieval, Python code execution, and Symbolic Lab Language (SLL) commands sent to a physical robotic platform. The agent autonomously plans, generates SLL, transfers code to the device, and executes experiments.
- **Availability**: Code on request (per Boiko et al. supplementary)
- **Validation**: Wet-lab execution of optimized palladium-catalyzed Suzuki and Sonogashira cross-couplings on a physical platform.
- **Notable results**: Designed and executed cross-coupling reaction optimizations end-to-end with no human intervention on the experimental loop.
- **Primary paper**: [Boiko et al., "Autonomous chemical research with large language models," Nature 624, 570–578 (2023)](https://doi.org/10.1038/s41586-023-06792-0)
- **Other references**: [Gao et al., Cell Perspective 2024](https://doi.org/10.1016/j.cell.2024.09.022) (single-LLM-multi-role case study)
- **Code**: [Repo](https://github.com/gomesgroup/coscientist)
- **Local source files**: `sources/1-s2.0-S0092867424010705-main.pdf` (Cell perspective citing Coscientist)
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### CRISPR-GPT

- **Affiliation**: Stanford University (Cong lab), Princeton, UC Berkeley, Google DeepMind ([Qu et al.](https://doi.org/10.1038/s41551-025-01463-z))
- **First introduced**: 2024-04 (arXiv v1); peer-reviewed version in Nature Biomedical Engineering 2026-02
- **Lifecycle stages**: Experiment design, Analysis
- **Autonomy level**: Assistive (human-in-the-loop; user-proxy agent operates autonomously but user oversight is encouraged)
- **Domain focus**: Biology (CRISPR-Cas gene editing — knockout, base editing, prime editing, epigenetic editing)
- **Approach**: Multi-agent LLM system with four roles — a Planner agent decomposes user requests into a chain of state-machine tasks; a Task Executor manages workflow; a User-Proxy agent mediates user interaction; Tool Providers wrap external tools/databases/web search via APIs. The system implements 22 individual gene-editing tasks (sgRNA design, off-target prediction, delivery selection, protocol drafting, validation assay design) across Meta, Auto, and QA modes.
- **Availability**: Closed (no full code release pending US regulatory clarity on AI in biology); welcome page on GitHub
- **Validation**: Real-world case study of non-expert researchers using CRISPR-GPT to plan and execute gene-editing experiments from scratch, as reported in the Nature Biomedical Engineering paper.
- **Notable results**: First LLM agent system reported to span the full CRISPR experimental-design workflow across four editing modalities; demonstrated to help non-experts plan and execute real gene-editing experiments.
- **Primary paper**: [Qu et al., "CRISPR-GPT for agentic automation of gene-editing experiments," Nat. Biomed. Eng. 10, 245–258 (2026)](https://doi.org/10.1038/s41551-025-01463-z)
- **Other references**: [arXiv:2404.18021](https://arxiv.org/abs/2404.18021)
- **Code**: [Welcome page](https://github.com/cong-lab/crispr-gpt-pub); full codebase withheld pending regulatory clarity
- **Local source files**: `sources/2404.18021v2.pdf`
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### NovelSeek

- **Affiliation**: Shanghai Artificial Intelligence Laboratory ([NovelSeek Team](https://alpha-innovator.github.io/NovelSeek-project-page))
- **First introduced**: 2025-05 (arXiv:2505.16938)
- **Lifecycle stages**: Multi-stage
- **Autonomy level**: Semi-autonomous (closed-loop with optional human expert interaction)
- **Domain focus**: General (reaction yield, transcription/enhancer prediction, molecular dynamics, time-series forecasting, power flow estimation, semantic segmentation, etc. — 12 AI-for-Science tasks)
- **Approach**: Multi-agent framework spanning a Survey agent (literature search), Code Review agent (analyzes baseline repositories), Idea Innovation agent (proposes and self-evolves research ideas), and Planning & Execution agent (turns ideas into experiments and handles errors). Designed as an end-to-end loop from hypothesis to verification.
- **Availability**: Open source (code and baselines released)
- **Validation**: Reports improvements on 12 AI-for-Science benchmark tasks against published baselines, e.g. reaction yield prediction 27.6 → 35.4 in 12 hours; enhancer activity prediction (DeepSTARR baseline) 0.52 → 0.79 in 4 hours; 2D semantic segmentation 78.8 → 81.0 in ~30 hours. Compared head-to-head to AI Scientist-v2 on 2D image classification and point-cloud autonomous-driving idea-generation tasks via 5 human reviewers averaging 20 ideas/task.
- **Notable results**: Time-bounded performance gains across 12 heterogeneous AI4Science tasks; reported novelty preference over AI Scientist-v2 on the head-to-head idea-quality study.
- **Primary paper**: [NovelSeek Team, "NovelSeek: When Agent Becomes the Scientist — Building Closed-Loop System from Hypothesis to Verification," arXiv:2505.16938](https://arxiv.org/abs/2505.16938)
- **Other references**: [Project page](https://alpha-innovator.github.io/NovelSeek-project-page); [HuggingFace](https://huggingface.co/U4R/NovelSeek)
- **Code**: [Repo](https://github.com/Alpha-Innovator/NovelSeek)
- **Local source files**: `sources/2505.16938v1.pdf`
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### Robin (FutureHouse)

- **Affiliation**: FutureHouse, with collaborators at the University of Oxford and Fordham University ([FutureHouse](https://www.futurehouse.org/))
- **First introduced**: 2025-05 (preprint); peer-reviewed paper accepted 2026-05
- **Lifecycle stages**: Multi-stage (hypothesis generation + experiment design + analysis; lab-in-the-loop)
- **Autonomy level**: Semi-autonomous (closed-loop with checkpoints; humans run wet-lab experiments)
- **Domain focus**: Biology / therapeutics
- **Approach**: Multi-agent Jupyter notebook built on the FutureHouse Aviary framework. Combines PaperQA2-based literature search agents (Crow for concise, Falcon for deep summaries) with Finch, a Jupyter-native data analysis agent that runs analyses across multiple independent trajectories and produces consensus conclusions.
- **Availability**: Open source (code) + closed agent platform (FutureHouse-hosted Crow / Falcon / Finch endpoints)
- **Validation**: Wet-lab study on dry age-related macular degeneration (dAMD) — Robin proposed enhancement of retinal pigment epithelium phagocytosis as a strategy, selected drug candidates, analyzed RNA-seq follow-up, and produced all hypotheses, analyses, and figures in the main text.
- **Notable results**: Identified ripasudil (a clinically used ROCK inhibitor) as a novel dAMD candidate confirmed in vitro; identified KL001 as a second hit; proposed and analyzed an RNA-seq follow-up that revealed ABCA1 upregulation as a candidate mechanism/target.
- **Primary paper**: [Ghareeb et al., "A multi-agent system for automating scientific discovery," Nature 2026](https://doi.org/10.1038/s41586-026-10652-y)
- **Other references**: [Narayanan et al., "Aviary: training language agents on challenging scientific tasks," arXiv (2024)](https://arxiv.org/abs/2412.21154)
- **Code**: [Robin repo](https://github.com/Future-House/robin) and [Finch repo](https://github.com/Future-House/finch)
- **Local source files**: `sources/s41586-026-10652-y_reference.pdf`
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### Talk2QSP

- **Affiliation**: Sanofi and bmedx ([Sanofi](https://www.sanofi.com/))
- **First introduced**: 2026-05 (bioRxiv preprint v2)
- **Lifecycle stages**: Experiment design
- **Autonomy level**: Assistive (human-in-the-loop, dynamic HITL strategy)
- **Domain focus**: Quantitative Systems Pharmacology (QSP) / kinetic ODE modelling
- **Approach**: Agent-based framework that converts unstructured literature descriptions of clinical or preclinical scenarios into executable QSP/SBML model interventions. Combines semantic grounding of model entities, an LLM Scenario Extractor, and a dual-agent Scenario Mapper that issues discrete verifiable "work orders"; humans resolve biological ambiguities interactively.
- **Availability**: Closed (no public access announced in the preprint)
- **Validation**: Seven subject-matter-expert-curated literature scenarios applied across four ODE/QSP models; all selected scenarios resolved into correct executable parameter changes, including multi-dose interventions, unit conversions, no-op scenarios, and ambiguity-triggered HITL cases.
- **Notable results**: 7/7 SME-curated scenarios resolved correctly; outperformed standalone SBML-reasoning LLM calls and prior agentic efforts on processed SBML data (per preprint claim).
- **Primary paper**: [Kazemeini et al., "Talk2QSP: Deriving Executable Scenarios from Unstructured Literature via Human-in-the-Loop Agents," bioRxiv 2026.05.06.723244](https://doi.org/10.64898/2026.05.06.723244)
- **Other references**: _None._
- **Code**: Not released
- **Local source files**: `sources/2026.05.06.723244v2.full.pdf`
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

## Recently surfaced

- **AI Scientist (Sakana)** (added 2026-05-20) — end-to-end LLM agent that produced the first AI-generated paper to pass peer review (ICLR 2025 workshop, v2); Nature 2026.
- **Biomni** (added 2026-05-20) — Stanford general-purpose biomedical agent matching expert humans on LAB-Bench DbQA/SeqQA.
- **CRISPR-GPT** (added 2026-05-20) — multi-agent gene-editing experiment designer published in Nat. Biomed. Eng. 2026.
- **NovelSeek** (added 2026-05-20) — closed-loop multi-agent system reporting time-bounded gains on 12 AI-for-Science tasks.
- **Robin (FutureHouse)** (added 2026-05-20) — first published multi-agent system to close the hypothesize/analyze loop in experimental biology with in vitro validation.

## Flagged for review

_None._

## Deferred — next-run priority

- **Virtual Lab (Stanford / CZ Biohub)** — Nature 2025 multi-agent system that designed nanobodies against SARS-CoV-2 variants; bioRxiv PDF blocked by Cloudflare this run, defer to next attempt via Nature PDF or paper-search-mcp fallback.
- **MARS (multi-agent + robot materials lab)** — 19-agent / 16-tool hierarchical RAG system reported January 2026 for closed-loop materials discovery (perovskite nanocrystals, water-stable composites); locate the underlying primary paper next run.
- **BORA** — Digital Discovery Feb 2026 LLM + Bayesian optimisation hybrid (o3, o4-mini, gpt-5, gemini-2.5-flash) benchmarked on 10D photocatalytic H₂ evolution and 7D pétanque simulation; archive primary paper.
- **Agent Laboratory / AutoGen / BabyAGI / GPT Researcher / MOOSE-Chem2 / SciAgents / SciMON** — eight open-source frameworks evaluated in the bioRxiv January 2026 critical evaluation (10.64898/2026.01.05.697809); archive the evaluation paper and decide per-system inclusion.
- **STORM (Stanford)** — referenced in the agent landscape; primary paper not yet in `sources/`.
- **FutureHouse Aviary framework** — underpins Robin; the Aviary arXiv paper itself is worth archiving as a separate entry if Aviary is judged a discrete system rather than a framework.
- **AutoBa** — multi-omic analysis agent cited by Gao et al.; primary paper to be archived.
