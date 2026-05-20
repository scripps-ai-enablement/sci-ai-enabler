# Autonomous AI scientist systems

> Named systems that perform hypothesis generation, experiment design, or analysis with meaningful autonomy. Manuscript writing is a downstream subcomponent, not a peer stage — writing-only systems are out of scope. See [`summary.md`](summary.md) for the landscape view and [`../COSCIENTIST_AGENT.md`](../COSCIENTIST_AGENT.md) for the curation rules.

_Last updated: 2026-05-20._

## Systems

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
- **Other references**: [Nature news on AI agents in science (AI Index 2026)](https://doi.org/10.1038/d41586-026-01199-z)
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

- **ChemCrow** (added 2026-05-20) — chemistry-tool-augmented GPT-4 agent for organic synthesis planning.
- **Co-Scientist (Google)** (added 2026-05-20) — Gemini-based multi-agent hypothesis engine validated in three biomedical case studies.
- **Coscientist (CMU)** (added 2026-05-20) — GPT-4 planner for autonomous chemistry on a physical robotic platform.
- **Robin (FutureHouse)** (added 2026-05-20) — first published multi-agent system to close the hypothesize/analyze loop in experimental biology with in vitro validation.
- **Talk2QSP** (added 2026-05-20) — human-in-the-loop agent that converts literature scenarios into executable QSP model interventions.

## Flagged for review

_None._

## Deferred — next-run priority

- **Sakana AI Scientist** — frequently cited in landscape coverage but no primary source archived this run.
- **STORM (Stanford)** — referenced in the agent landscape; primary paper not yet in `sources/`.
- **FutureHouse Aviary framework** — underpins Robin; the Aviary arXiv paper itself is worth archiving as a separate entry if Aviary is judged a discrete system rather than a framework.
- **AutoBa** — multi-omic analysis agent cited by Gao et al.; primary paper to be archived.
- **CRISPR-GPT** — biology agent referenced in the broader literature; archive primary source on next run.
