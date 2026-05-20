---
title: Landscape
parent: AI scientists
nav_order: 1
---

# The autonomous AI scientist landscape

An autonomous AI scientist is a named software system that takes meaningful initiative across one or more of three primary stages: **hypothesis generation** (proposing novel, testable scientific claims rather than retrieving existing ones), **experiment design** (choosing experiments that discriminate between hypotheses, optimizing protocols), and **analysis** (interpreting experimental data, fitting models, drawing inferences). Closing the full loop — hypothesize, design, analyze — is the explicit ambition described in the Gao et al. *Cell* perspective ([2024](https://doi.org/10.1016/j.cell.2024.09.022)).

## Wet-lab biology

Two systems with peer-reviewed *Nature* papers anchor the wet-lab end of the landscape:

- [**Co-Scientist**](systems/co-scientist-google.html) (Google) — a Gemini-based multi-agent reasoning engine focused on hypothesis generation, using a generation/reflection/ranking/evolution ensemble with Elo-style tournaments. Validated on three biomedical case studies: AML drug repurposing, liver-fibrosis target discovery in organoids, and recapitulation of an unpublished AMR gene-transfer mechanism. Code unreleased ([Gottweis et al., *Nature* 2026](https://doi.org/10.1038/s41586-026-10644-y)).
- [**Robin**](systems/robin.html) (FutureHouse) — the first multi-agent system to integrate hypothesis generation with experimental data analysis in a lab-in-the-loop workflow. Built on the Aviary framework, Robin orchestrates PaperQA2 literature agents with the Jupyter-native Finch analysis agent. Applied to dry age-related macular degeneration, Robin identified ripasudil and KL001 as in vitro hits and proposed an RNA-seq follow-up implicating ABCA1 ([Ghareeb et al., *Nature* 2026](https://doi.org/10.1038/s41586-026-10652-y)).

## Machine-learning research

[**AI Scientist**](systems/ai-scientist-sakana.html) (Sakana AI) is an end-to-end loop that generates ideas, codes and runs experiments, writes a LaTeX manuscript, and reviews itself via an Automated Reviewer. AI Scientist-v2 produced the first AI-generated paper to pass human peer review at an ICLR 2025 workshop ([Lu et al., *Nature* 651, 914–919 (2026)](https://sakana.ai/ai-scientist-nature/); [v2 preprint arXiv:2504.08066](https://arxiv.org/abs/2504.08066)).

## General-purpose biomedical agents

- [**Biomni**](systems/biomni.html) (Stanford / Snap group) couples an environment of 150 tools, 105 packages, and 59 databases (Biomni-E1) with a code-executing planner (Biomni-A1). On LAB-Bench it matches expert humans (74.4% DbQA, 81.9% SeqQA) and scores 17.3% on a 14-subfield HLE subset.
- [**OpenScientist**](systems/openscientist.html) (Washington University in St. Louis) is an Apache-2.0 agentic co-scientist built on Claude Code with a public collection of biomedical Agent Skills. Evaluated by domain experts across four clinical case studies — Alzheimer's biomarkers (SEABIRD cohort, identified `%ptau217` as best predictor in 40 minutes), plasma proteomic survival, single-cell transcriptomics in neurofibrillary tangles, and multiple-myeloma hypothesis generation validated in an external cohort ([Roberts et al., *medRxiv* 2026.03.15.26348338](https://www.medrxiv.org/content/10.64898/2026.03.15.26348338v1)).
- [**CRISPR-GPT**](systems/crispr-gpt.html) (Stanford / Princeton) is a four-agent planner spanning 22 gene-editing tasks across knockout, base, prime, and epigenetic editing; full code is withheld pending US regulatory clarity ([Qu et al., *Nat. Biomed. Eng.* 2026](https://doi.org/10.1038/s41551-025-01463-z)).

## Chemistry

Chemistry remains the most loop-closed domain. [**Coscientist (CMU)**](systems/coscientist-cmu.html) and [**ChemCrow**](systems/chemcrow.html) cover autonomous synthesis planning and execution on physical and tool-augmented stacks respectively. At the assistive end, [**Talk2QSP**](systems/talk2qsp.html) (Sanofi/bmedx) maps literature scenarios onto executable quantitative systems pharmacology models with dynamic human-in-the-loop interaction.

## Closed-loop multi-domain frameworks

[**NovelSeek**](systems/novelseek.html) (Shanghai AI Lab) is a closed-loop multi-agent framework reporting time-bounded gains on 12 AI-for-Science tasks and a head-to-head idea-quality comparison against AI Scientist-v2.

Other notable systems being tracked for inclusion: **Virtual Lab** (Stanford / CZ Biohub, *Nature* 2025 — designed novel SARS-CoV-2 nanobodies), **MARS** (closed-loop materials discovery, January 2026), **BORA** (LLM + Bayesian optimization, *Digital Discovery* February 2026), **STORM**, **Aviary**, and **AutoBa**.

## How these systems are evaluated

Evaluation now spans three regimes.

**Wet-lab validations** remain the strongest evidence: Co-Scientist's in vitro AML hits and organoid-confirmed fibrosis targets; Robin's ripasudil/KL001 confirmations; CMU Coscientist's robotic cross-couplings; CRISPR-GPT's non-expert case study.

**Standardised benchmarks** have grown: Biomni reports LAB-Bench DbQA/SeqQA and HLE numbers against human-expert baselines; AI Index 2026 coverage notes PaperArena (best agent 39%) and that the best AI agents score roughly half as well as human PhDs on multistep tasks ([*Nature* news, April 2026](https://doi.org/10.1038/d41586-026-01199-z)).

**Internal head-to-head studies** are appearing: NovelSeek vs. AI Scientist-v2 on idea novelty; Sakana's Automated Reviewer benchmarked against NeurIPS-scale human agreement (~69% balanced accuracy). MoSciBench, BixBench, MLE-Bench, ScienceAgentBench, and SciCode are referenced in the broader landscape but not yet evidenced in primary citations here.

## Open problems

- **Hallucination of references.** Robin's ablations show that removing PaperQA2-based agents (Crow/Falcon) dramatically increases hallucinated citations; the AI Scientist papers report similar inaccuracies in citations and figures.
- **Reproducibility of analyses.** Robin runs eight Finch trajectories and consensuses; Gao et al. flag reproducibility and rigorous peer review of agentic research as open challenges.
- **Originality versus retrieval.** Gao et al. argue current foundation models may struggle to produce hypotheses outside their training distribution — a structural limit on hypothesis-generation claims. A *bioRxiv* critical evaluation (January 2026, 10.64898/2026.01.05.697809) reports that none of eight open-source frameworks completed a full research cycle end-to-end.
- **Code-execution risk and dual use.** Biomni notes its agent executes LLM-generated code with full system privileges by default; CRISPR-GPT withholds full code pending regulatory clarity; Co-Scientist authors cite safety implications as a reason for not releasing source; Robin notes RLHF and platform-level controls against malicious protocol generation.
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
