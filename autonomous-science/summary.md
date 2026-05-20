# Autonomous AI scientists

> Agents that semi- or fully-autonomously perform the core work of science — hypothesis generation, experiment design, and data analysis. Manuscript writing is a subcomponent (a downstream capability), not the focus.

_Last updated: 2026-05-20._

## What "autonomous AI scientist" means

An autonomous AI scientist is a named software system that takes meaningful initiative across one or more of three primary stages: (1) **hypothesis generation** — proposing novel, testable scientific claims rather than retrieving existing ones; (2) **experiment design** — choosing experiments that discriminate between hypotheses or optimizing protocols and parameters; and (3) **analysis** — autonomously interpreting experimental data, fitting models, and drawing inferences. "Autonomy" here is a spectrum — from assistive (human-in-the-loop) through semi-autonomous (closed-loop with checkpoints) to fully autonomous (closed loop without intervention). Manuscript writing, when present, is treated as a downstream capability of a system that already does scientific reasoning; systems whose only function is to draft text are out of scope. Closing the full loop — hypothesize, design, analyze — is the explicit ambition described in the Gao et al. Cell perspective ([2024](https://doi.org/10.1016/j.cell.2024.09.022)).

## The landscape today

Two systems with peer-reviewed Nature papers anchor the wet-lab end of the landscape:

- [**Co-Scientist**](entries.md#co-scientist-google) (Google), a Gemini-based multi-agent reasoning engine focused on hypothesis generation, using a generation/reflection/ranking/evolution ensemble, self-play scientific debate, and Elo-style tournaments. Validated on three biomedical case studies (AML drug repurposing, liver-fibrosis target discovery in organoids, recapitulation of an unpublished AMR gene-transfer mechanism). Code unreleased ([Gottweis et al., Nature 2026](https://doi.org/10.1038/s41586-026-10644-y)).
- [**Robin**](entries.md#robin-futurehouse) (FutureHouse), the first multi-agent system to integrate hypothesis generation with experimental data analysis in a lab-in-the-loop workflow. Built on Aviary, Robin orchestrates PaperQA2 literature agents (Crow, Falcon) with the Jupyter-native Finch analysis agent. Applied to dry age-related macular degeneration, Robin identified ripasudil and KL001 as in vitro hits and proposed an RNA-seq follow-up implicating ABCA1 ([Ghareeb et al., Nature 2026](https://doi.org/10.1038/s41586-026-10652-y)).

The ML-research end is now anchored by [**AI Scientist**](entries.md#ai-scientist-sakana) (Sakana AI), an end-to-end loop that generates ideas, codes/runs experiments, writes a LaTeX manuscript, and reviews itself via an Automated Reviewer. AI Scientist-v2 produced the first AI-generated paper to pass human peer review at an ICLR 2025 workshop ([Lu et al., Nature 651, 914–919 (2026)](https://sakana.ai/ai-scientist-nature/); [v2 preprint arXiv:2504.08066](https://arxiv.org/abs/2504.08066)).

General-purpose biomedical agents are emerging. [**Biomni**](entries.md#biomni) (Stanford / Snap group, bioRxiv 2025) couples an environment of 150 tools / 105 packages / 59 databases (Biomni-E1) with a code-executing planner (Biomni-A1); on LAB-Bench it matches expert humans (74.4% DbQA, 81.9% SeqQA) and scores 17.3% on a 14-subfield HLE subset. [**CRISPR-GPT**](entries.md#crispr-gpt) (Stanford / Princeton, Nat. Biomed. Eng. 2026) is a four-agent planner spanning 22 gene-editing tasks across knockout, base, prime, and epigenetic editing; full code is withheld pending US regulatory clarity.

Chemistry remains the most loop-closed domain. [**Coscientist (CMU)**](entries.md#coscientist-cmu) and [**ChemCrow**](entries.md#chemcrow) cover autonomous synthesis planning and execution on physical and tool-augmented stacks respectively. At the assistive end, [**Talk2QSP**](entries.md#talk2qsp) (Sanofi/bmedx, bioRxiv 2026) maps literature scenarios onto executable QSP models with dynamic HITL.

[**NovelSeek**](entries.md#novelseek) (Shanghai AI Lab, arXiv:2505.16938) is a closed-loop multi-agent framework reporting time-bounded gains on 12 AI-for-Science tasks and a head-to-head idea-quality comparison against AI Scientist-v2.

Notable systems still deferred for next-run sourcing: **Virtual Lab** (Stanford / CZ Biohub, Nature 2025 — designed novel SARS-CoV-2 nanobodies), **MARS** (closed-loop materials discovery, Jan 2026), **BORA** (LLM + Bayesian optimisation, Digital Discovery Feb 2026), and **STORM**, **Aviary**, and **AutoBa**.

## How these systems are evaluated

Evaluation now spans three regimes. **Wet-lab validations** remain the strongest evidence: Co-Scientist's in vitro AML hits and organoid-confirmed fibrosis targets; Robin's ripasudil/KL001 confirmations; CMU Coscientist's robotic cross-couplings; CRISPR-GPT's non-expert case study. **Standardised benchmarks** have grown: Biomni reports LAB-Bench DbQA/SeqQA and HLE numbers against human-expert baselines; the AI Index 2026 coverage notes PaperArena (best agent 39%) and that the best AI agents score roughly half as well as human PhDs on multistep tasks ([Nature news, April 2026](https://doi.org/10.1038/d41586-026-01199-z)). **Internal head-to-head studies** are appearing — NovelSeek vs. AI Scientist-v2 on idea novelty; Sakana's Automated Reviewer benchmarked against NeurIPS-scale human agreement (~69% balanced accuracy). MoSciBench, BixBench, MLE-Bench, ScienceAgentBench, and SciCode are referenced in the broader landscape but not yet evidenced in the archived corpus and should be added with citations on future runs.

## Open problems

- **Hallucination of references.** Robin's ablations show that removing PaperQA2-based agents (Crow/Falcon) dramatically increases hallucinated citations; the AI Scientist papers report similar inaccuracies in citations and figures.
- **Reproducibility of analyses.** Robin runs eight Finch trajectories and consensuses; Gao et al. flag reproducibility and rigorous peer review of agentic research as open challenges.
- **Originality vs retrieval.** Gao et al. argue current foundation models may struggle to produce hypotheses outside their training distribution — a structural limit on hypothesis-generation claims. Critical evaluations (bioRxiv Jan 2026, 10.64898/2026.01.05.697809) report that none of eight open-source frameworks completed a full research cycle end-to-end.
- **Code execution risk and dual use.** Biomni notes its agent executes LLM-generated code with full system privileges by default; CRISPR-GPT withholds full code pending regulatory clarity; Co-Scientist authors cite safety implications as a reason for not releasing source; Robin notes RLHF and platform-level controls against malicious protocol generation.
- **Evaluation gaps.** Few head-to-head studies share benchmarks across the systems above; the AI Index Report 2026 notes that even the best agents lag human PhDs by ~2× on multistep tasks.

## Sources

- [Gottweis et al., "Accelerating scientific discovery with Co-Scientist," Nature](https://doi.org/10.1038/s41586-026-10644-y) — accepted 2026-05-11; verified 2026-05-20 (this run).
- [Ghareeb et al., "A multi-agent system for automating scientific discovery" (Robin), Nature](https://doi.org/10.1038/s41586-026-10652-y) — accepted 2026-05-12; verified 2026-05-20 (this run).
- [Kazemeini et al., "Talk2QSP," bioRxiv 2026.05.06.723244](https://doi.org/10.64898/2026.05.06.723244) — posted 2026-05-15; verified 2026-05-20 (this run).
- [Gao et al., "Empowering biomedical discovery with AI agents," Cell 187 (2024)](https://doi.org/10.1016/j.cell.2024.09.022) — published 2024-10-31; verified 2026-05-20 (this run).
- [Nature news, "Human scientists beat the best AI agents…" (AI Index Report 2026 coverage)](https://doi.org/10.1038/d41586-026-01199-z) — Nature vol. 652, 23 April 2026; verified 2026-05-20 (this run).
- [Boiko et al., "Autonomous chemical research with large language models," Nature 624 (2023)](https://doi.org/10.1038/s41586-023-06792-0) — referenced via Gao et al. perspective; verified 2026-05-20 (this run).
- [Bran et al., "Augmenting large language models with chemistry tools," Nat. Mach. Intell. (2024)](https://doi.org/10.1038/s42256-024-00832-8) — referenced via Gao et al. perspective; verified 2026-05-20 (this run).
- [Lu et al., "The AI Scientist," arXiv:2408.06292 / Nature 651, 914–919 (2026)](https://arxiv.org/abs/2408.06292) — v5 archived 2026-05-20; verified 2026-05-20 (this run).
- [Yamada et al., "The AI Scientist-v2," arXiv:2504.08066](https://arxiv.org/abs/2504.08066) — posted 2025-04-11; verified 2026-05-20 (this run).
- [Huang et al., "Biomni: A General-Purpose Biomedical AI Agent," bioRxiv 2025.05.30.656746](https://doi.org/10.1101/2025.05.30.656746) — posted 2025-05-30; verified 2026-05-20 (this run).
- [Qu et al., "CRISPR-GPT for agentic automation of gene-editing experiments," Nat. Biomed. Eng. 10, 245–258 (2026)](https://doi.org/10.1038/s41551-025-01463-z) — published 2026-02; verified 2026-05-20 (this run).
- [NovelSeek Team, arXiv:2505.16938](https://arxiv.org/abs/2505.16938) — posted 2025-05-22; verified 2026-05-20 (this run).
