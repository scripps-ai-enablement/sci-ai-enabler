# Autonomous AI scientists

> Agents that semi- or fully-autonomously perform the core work of science — hypothesis generation, experiment design, and data analysis. Manuscript writing is a subcomponent (a downstream capability), not the focus.

_Last updated: 2026-05-20._

## What "autonomous AI scientist" means

An autonomous AI scientist is a named software system that takes meaningful initiative across one or more of three primary stages: (1) **hypothesis generation** — proposing novel, testable scientific claims rather than retrieving existing ones; (2) **experiment design** — choosing experiments that discriminate between hypotheses or optimizing protocols and parameters; and (3) **analysis** — autonomously interpreting experimental data, fitting models, and drawing inferences. "Autonomy" here is a spectrum — from assistive (human-in-the-loop) through semi-autonomous (closed-loop with checkpoints) to fully autonomous (closed loop without intervention). Manuscript writing, when present, is treated as a downstream capability of a system that already does scientific reasoning; systems whose only function is to draft text are out of scope. Closing the full loop — hypothesize, design, analyze — is the explicit ambition described in the Gao et al. Cell perspective ([2024](https://doi.org/10.1016/j.cell.2024.09.022)).

## The landscape today

Two systems with peer-reviewed primary papers anchor the landscape in 2026:

- [**Co-Scientist**](entries.md#co-scientist-google) (Google), a Gemini-based multi-agent reasoning engine that emphasizes the hypothesis stage. Co-Scientist combines a generation/reflection/ranking/evolution agent ensemble with a self-play scientific debate and Elo-style hypothesis tournaments, scaling test-time compute to refine ideas. Validation spans three biomedical case studies including drug repurposing for AML, novel epigenetic targets for liver fibrosis (confirmed in human hepatic organoids), and independent recapitulation of a then-unpublished antimicrobial-resistance gene-transfer mechanism. Code is not released; access is by experimental program ([Gottweis et al., Nature 2026](https://doi.org/10.1038/s41586-026-10644-y)).
- [**Robin**](entries.md#robin-futurehouse) (FutureHouse), the first published multi-agent system to integrate hypothesis generation with experimental data analysis in a single lab-in-the-loop workflow. Built on the Aviary framework, Robin orchestrates PaperQA2-based literature agents (Crow, Falcon) with the Jupyter-native Finch analysis agent across multiple parallel trajectories. Applied to dry age-related macular degeneration, Robin identified ripasudil and KL001 as in vitro hits and proposed/analyzed a follow-up RNA-seq experiment that surfaced ABCA1 as a candidate mechanism. Code is open at GitHub ([Ghareeb et al., Nature 2026](https://doi.org/10.1038/s41586-026-10652-y)).

Chemistry remains the most loop-closed domain. [**Coscientist**](entries.md#coscientist-cmu) (CMU, Boiko et al., Nature 2023) demonstrated a GPT-4 planner orchestrating Python, web search, and Symbolic Lab Language commands to autonomously execute palladium-catalyzed cross-couplings on a physical robotic platform. [**ChemCrow**](entries.md#chemcrow) (EPFL/Rochester, Bran et al., Nat. Mach. Intell. 2024) augments GPT-4 with 18 expert-curated chemistry tools for synthesis planning and reaction reasoning.

At the assistive end, [**Talk2QSP**](entries.md#talk2qsp) (Sanofi/bmedx, bioRxiv 2026) is a domain-specific experiment-design helper that maps unstructured literature descriptions onto executable Quantitative Systems Pharmacology models with a dynamic human-in-the-loop strategy.

Multiple named systems frequently cited in coverage — Sakana's AI Scientist, Stanford STORM, FutureHouse Aviary as a framework, AutoBa, CRISPR-GPT — are deferred pending primary sources in `sources/`.

## How these systems are evaluated

Evaluation is uneven. The strongest results in the current corpus are **wet-lab validations**: Co-Scientist's in vitro AML repurposing hits and organoid-confirmed liver-fibrosis targets; Robin's ripasudil/KL001 in vitro confirmations in retinal pigment epithelium phagocytosis assays; CMU Coscientist's executed cross-couplings on a physical platform. Co-Scientist also reports head-to-head comparisons against human experts and against frontier LLM baselines. Talk2QSP reports SME-curated scenario resolution (7/7 correct on its internal benchmark). The Nature news coverage of the AI Index Report 2026 notes the emergence of agent-specific benchmarks such as **PaperArena**, on which the best LLM-powered agent reached 39% accuracy — and reports that the best AI agents score roughly half as well as human PhD specialists on multistep scientific workflows ([Nature news, April 2026](https://doi.org/10.1038/d41586-026-01199-z)). Other benchmarks named in the broader landscape (LAB-Bench, MLE-Bench, ScienceAgentBench, SciCode, BixBench) are not directly evidenced in the archived sources and should be added with citations on future runs.

## Open problems

- **Hallucination of references.** Robin's ablations show that removing PaperQA2-based agents (Crow/Falcon) leads to a dramatic rise in hallucinated citations, underscoring how literature grounding is load-bearing for scientific agents.
- **Reproducibility of analyses.** Robin runs analysis across eight Finch trajectories and takes a consensus to dampen run-to-run variability; the Gao et al. perspective explicitly calls out reproducibility and rigorous peer review of agentic research as open challenges.
- **Originality vs retrieval.** The Gao et al. perspective argues that current foundation models, trained on existing data, may struggle to produce hypotheses outside their training distribution — a structural limit on hypothesis-generation claims.
- **Evaluation gaps.** Few head-to-head studies compare named systems on shared benchmarks; the AI Index Report 2026 notes that even the best agents lag human PhDs by ~2× on multistep tasks.
- **Safety and dual-use.** Co-Scientist's authors cite "safety implications of unmonitored autonomous agentic use of such capable AI systems" as a reason for not releasing source. Robin notes RLHF and platform-level controls aimed at preventing generation of malicious biological protocols. Gao et al. flag misuse, over-reliance, and identification of hazardous substances as risks scaling with autonomy.

## Sources

- [Gottweis et al., "Accelerating scientific discovery with Co-Scientist," Nature](https://doi.org/10.1038/s41586-026-10644-y) — accepted 2026-05-11; verified 2026-05-20 (this run).
- [Ghareeb et al., "A multi-agent system for automating scientific discovery" (Robin), Nature](https://doi.org/10.1038/s41586-026-10652-y) — accepted 2026-05-12; verified 2026-05-20 (this run).
- [Kazemeini et al., "Talk2QSP," bioRxiv 2026.05.06.723244](https://doi.org/10.64898/2026.05.06.723244) — posted 2026-05-15; verified 2026-05-20 (this run).
- [Gao et al., "Empowering biomedical discovery with AI agents," Cell 187 (2024)](https://doi.org/10.1016/j.cell.2024.09.022) — published 2024-10-31; verified 2026-05-20 (this run).
- [Nature news, "Human scientists beat the best AI agents…" (AI Index Report 2026 coverage)](https://doi.org/10.1038/d41586-026-01199-z) — Nature vol. 652, 23 April 2026; verified 2026-05-20 (this run).
- [Boiko et al., "Autonomous chemical research with large language models," Nature 624 (2023)](https://doi.org/10.1038/s41586-023-06792-0) — referenced via Gao et al. perspective; verified 2026-05-20 (this run).
- [Bran et al., "Augmenting large language models with chemistry tools," Nat. Mach. Intell. (2024)](https://doi.org/10.1038/s42256-024-00832-8) — referenced via Gao et al. perspective; verified 2026-05-20 (this run).
