---
title: Landscape
parent: AI scientists
nav_order: 1
synthesis_reviewed: 2026-06-11
---

# The autonomous AI scientist landscape

An autonomous AI scientist is a named software system that takes meaningful initiative across one or more of three primary stages: **hypothesis generation** (proposing novel, testable scientific claims rather than retrieving existing ones), **experiment design** (choosing experiments that discriminate between hypotheses, optimizing protocols), and **analysis** (interpreting experimental data, fitting models, drawing inferences). Closing the full loop — hypothesize, design, analyze — is the explicit ambition described in the Gao et al. *Cell* perspective ([2024](https://doi.org/10.1016/j.cell.2024.09.022)).

{% assign systems = site.pages | where_exp: "p", "p.path contains 'autonomous-science/systems/'" | where_exp: "p", "p.domain_group" | sort: "title" %}

## How the landscape breaks down

Across the {{ systems | size }} systems tracked here, a few cross-cutting patterns matter more than any single entry:

- **Chemistry and materials are the most loop-closed.** These systems run genuine closed loops on physical hardware — CMU's Coscientist and MARS drive robotic synthesis, AMASE and MAD couple multiple characterization instruments to active-learning policies, and LEAP and CatDT pair domain-tuned models with wet-lab or microkinetic validation. This is where "autonomous" most fully means hands-on-the-apparatus.
- **Biology and medicine carry the strongest evidence.** Wet-lab and clinical validation — Co-Scientist's in vitro oncology hits, Robin's confirmed dry-AMD drug candidates, SPARK's prospective pathology study across 18 cohorts, CRISPR-GPT's non-expert gene-editing case study, OriGene's agent-nominated cancer targets confirmed in patient-derived organoid models — set the highest evidence tier in the field.
- **ML and scientific computing is a large, fast-moving cluster,** but mostly benchmark-validated rather than physically grounded. The recent design trend is architectural: self-improving systems that accumulate methodological memory across problems (GRAFT-ATHENA, EvoScientist, AutoSci, AutoScientists), and a turn toward *verifiability* — adversarial cross-model review (ARIS), evidence-chain auditing (ScientistOne), and numeric-registry gating (AutoResearchClaw).
- **Physical sciences and embodied systems are the newest frontier,** moving AI past simulators onto real apparatus: Qumus fabricates 2D-material devices, the Qiushi engine runs a free-space optical platform, Dr.Sai operates inside the BESIII collider collaboration, and BioProVLA runs wet-lab robotics on an ~$800 rig.
- **A long tail of single-domain pioneers** now spans mathematics (AI co-mathematician, Ax-Prover's formal Lean proving), symbolic equation discovery (MCI), spatial data science (NORA), plant science (Aleks), and scientific visualization (VIS Co-Scientist).

Evaluation is shifting from one-off demos toward **process-level scoring and verifiability audits**, and several shared failure modes — reference hallucination, reproducibility, originality-versus-retrieval — remain open. See [Evaluation and open problems](evaluation.html).

## All tracked systems

The full set is below, grouped by domain. Each row links to a per-system page with architecture, validation detail, headline metrics, and citation. **Loop stage** is the part of the scientific loop the system drives (`Multi-stage` = closes hypothesize → design → analyze); **Validation** is the strongest evidence tier it has demonstrated (`Wet-lab` > `Mixed` > `Benchmark` > `Design-only`).

{% assign group_order = "Biology & medicine|Chemistry & materials|ML & scientific computing|Physical sciences|Math & symbolic|General / multi-domain|Other" | split: "|" %}
{% for grp in group_order %}
{% assign rows = systems | where: "domain_group", grp %}
{% if rows.size > 0 %}
### {{ grp }} ({{ rows.size }})

| System | Org | What it is | Loop stage | Validation | Access |
|:---|:---|:---|:---|:---|:---|
{% for s in rows %}| [{{ s.title }}](systems/{{ s.name | replace: ".md", ".html" }}) | {{ s.org_short }} | {{ s.tagline }} | {{ s.lifecycle_stages | join: ", " }} | {{ s.validation_type }} | {{ s.access }} |
{% endfor %}
{% endif %}
{% endfor %}

{%- comment -%} Safety net: surface any system whose domain_group is outside the known set above, so a typo or a newly-introduced group never silently disappears from the table. {%- endcomment -%}
{% capture known_groups %}|{{ group_order | join: "|" }}|{% endcapture %}
{% assign orphan_count = 0 %}
{% for s in systems %}{% capture probe %}|{{ s.domain_group }}|{% endcapture %}{% unless known_groups contains probe %}{% assign orphan_count = orphan_count | plus: 1 %}{% endunless %}{% endfor %}
{% if orphan_count > 0 %}
### ⚠ Uncategorized ({{ orphan_count }})

These systems carry a `domain_group` outside the known set and are **not** shown above. Fix the system page's front-matter (use one of the seven controlled groups, or `Other`), or add the new group to the list in this page and in `COSCIENTIST_AGENT.md`.

| System | Org | What it is | Loop stage | Validation | Access |
|:---|:---|:---|:---|:---|:---|
{% for s in systems %}{% capture probe %}|{{ s.domain_group }}|{% endcapture %}{% unless known_groups contains probe %}| [{{ s.title }}](systems/{{ s.name | replace: ".md", ".html" }}) | {{ s.org_short }} | {{ s.tagline }} (unrecognized group `{{ s.domain_group }}`) | {{ s.lifecycle_stages | join: ", " }} | {{ s.validation_type }} | {{ s.access }} |
{% endunless %}{% endfor %}
{% endif %}

Other systems being tracked for inclusion: **Virtual Lab** (Stanford / CZ Biohub, *Nature* 2025 — designed novel SARS-CoV-2 nanobodies), **CORAL** (multi-agent evolutionary discovery, arXiv:2604.01658), **STORM**, **Aviary**, and **AutoBa**.

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
- [Qu et al., "BiomniBench: Process-level Evaluation of LLM Agents for Real-world Biomedical Research," *bioRxiv* 2026.05.12.724604](https://doi.org/10.64898/2026.05.12.724604)
- [Trost, Zhang, Aring et al., "An agentic framework for autonomous scientific discovery in cancer pathology" (SPARK), *Nature Medicine* (2026)](https://doi.org/10.1038/s41591-026-04357-y)
- [Lyu et al., "EvoScientist: Towards Multi-Agent Evolving AI Scientists for End-to-End Scientific Discovery," arXiv:2603.08127](https://arxiv.org/abs/2603.08127)
- [Weidener et al., "Rethinking the AI Scientist: Interactive Multi-Agent Workflows for Scientific Discovery" (Deep Research / BioAgents), arXiv:2601.12542](https://arxiv.org/abs/2601.12542)
- [Miyai et al., "Jr. AI Scientist and Its Risk Report," *TMLR* 2026; arXiv:2511.04583](https://arxiv.org/abs/2511.04583)
- [Yang, Li, Li, "ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration," arXiv:2605.03042](https://arxiv.org/abs/2605.03042)
- [Pepe et al., "Agentic Discovery of Neural Architectures: AIRA-Compose and AIRA-Design," arXiv:2605.15871](https://arxiv.org/abs/2605.15871)
- [Zheng et al., "LLMs Improving LLMs: Agentic Discovery for Test-Time Scaling" (AutoTTS), arXiv:2605.08083](https://arxiv.org/abs/2605.08083)
- [Xu & Borrett, "Beyond AI as Assistants: Toward Autonomous Discovery in Cosmology" (CMBEvolve / CosmoEvolve), arXiv:2605.14791](https://arxiv.org/abs/2605.14791)
- [Zheng et al., "AI co-mathematician: Accelerating mathematicians with agentic AI," arXiv:2605.06651](https://arxiv.org/abs/2605.06651)
- [Liu et al., "AutoResearchClaw: Self-Reinforcing Autonomous Research with Human-AI Collaboration," arXiv:2605.20025](https://arxiv.org/abs/2605.20025)
- [Du et al., "CVEvolve: Autonomous Algorithm Discovery for Unstructured Scientific Data Processing," arXiv:2605.11359](https://arxiv.org/abs/2605.11359)
- [Angelopoulos, Cahoon, Alterovitz, "From Prompts to Protocols: An AI Agent for Laboratory Automation" (EOS AI agent), arXiv:2605.16552](https://arxiv.org/abs/2605.16552)
- [Zhang, "Deep Researcher Agent: An Autonomous Framework for 24/7 Deep Learning Experimentation with Zero-Cost Monitoring," arXiv:2604.05854](https://arxiv.org/abs/2604.05854)
- [Xia, Zhang et al., "From AI Assistant to AI Scientist: Autonomous Discovery of LLM-RL Algorithms with LLM Agents (POISE)," arXiv:2603.23951](https://arxiv.org/abs/2603.23951)
- [Song, Trotter, Chen, "LLM Agent Swarm for Hypothesis-Driven Drug Discovery" (PharmaSwarm), arXiv:2504.17967](https://arxiv.org/abs/2504.17967)
- [Jin et al., "Aleks: AI powered Multi Agent System for Autonomous Scientific Discovery via Data-Driven Approaches in Plant Science," arXiv:2508.19383](https://arxiv.org/abs/2508.19383)
- [Hao, Lee, Wang, Scalia, Regev, "PerTurboAgent: An LLM-based Agent for Designing Iterative Perturb-Seq Experiments," PMLR v311 / bioRxiv 2025.05.25.656020](https://proceedings.mlr.press/v311/hao25b.html)
- [Zhu, Cai, Liu et al., "EvoMaster: A Foundational Agent Framework for Building Evolving Autonomous Scientific Agents at Scale," arXiv:2604.17406](https://arxiv.org/abs/2604.17406)
- [Wang, He, Peng et al., "NeuroClaw Technical Report: Closed-Loop Agentic AI for Executable and Reproducible Neuroimaging Research," arXiv:2604.24696](https://arxiv.org/abs/2604.24696)
- [Latent Labs Team, "Latent-Y: A Lab-Validated Autonomous Agent for De Novo Drug Design," arXiv:2603.29727](https://arxiv.org/abs/2603.29727)
- [Xu, Poussi, Zhong et al. (Qiu group), "PantheonOS: An Evolvable Multi-Agent Framework for Automatic Genomics Discovery," *bioRxiv* 2026.02.26.707870](https://doi.org/10.64898/2026.02.26.707870)
- [Zhang, Eckmann, Miao, Mahon, Zou, "The Virtual Biotech: A Multi-Agent AI Framework for Therapeutic Discovery and Development," *bioRxiv* 2026.02.23.707551](https://doi.org/10.64898/2026.02.23.707551)
- [Liu et al., "AMASE: Autonomous Materials Search Engine for Closed-Loop Phase-Mapping of Sn-Bi Thin Films," arXiv:2410.17430](https://arxiv.org/abs/2410.17430)
- [Hickman et al., "BORA: A Language-Based Bayesian Optimization Research Assistant," arXiv:2501.16224 / IJCAI 2025](https://arxiv.org/abs/2501.16224)
- [Deng et al., "Harnessing AtomisticSkills for Agentic Atomistic Research," arXiv:2605.24002](https://arxiv.org/abs/2605.24002)
- [Meng et al., "ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence," arXiv:2605.26340](https://arxiv.org/abs/2605.26340)
- [Zhou et al., "NORA: A Harness-Engineered Autonomous Research Agent for Spatial Data Science," arXiv:2605.02092](https://arxiv.org/abs/2605.02092)
- [Na & Park, "Machine Collective Intelligence for Explainable Scientific Discovery" (MCI), arXiv:2604.27297](https://arxiv.org/abs/2604.27297)
- [Du et al., "BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System for Biological Laboratory Manipulation," arXiv:2605.07306](https://arxiv.org/abs/2605.07306)
- [Wang, Chen, Gao et al., "LEAP: A closed-loop framework for perovskite precursor additive discovery," arXiv:2605.20242](https://arxiv.org/abs/2605.20242)
- [Gao, Fang, Zitnik, "AUTOSCIENTISTS: Self-Organizing Agent Teams for Long-Running Scientific Experimentation," arXiv:2605.28655](https://arxiv.org/abs/2605.28655)
- [Guo, Chawla, Wiest, Zhang, "AutoLLMResearch: Training Research Agents for Automating LLM Experiment Configuration," arXiv:2605.11518](https://arxiv.org/abs/2605.11518)
- [Qian, Xu, Xie et al., "AutoSci: A Memory-Centric Agentic System for the Full Scientific Research Lifecycle," arXiv:2605.31468](https://arxiv.org/abs/2605.31468)
- [Miao, Li, Ai, Tang, Wang, Bremer, Liu, "Toward AI VIS Co-Scientists: A General and End-to-End Agent Harness for Solving Complex Data Visualization Tasks," arXiv:2605.21825](https://arxiv.org/abs/2605.21825)
- [Bulanadi, Baxter, Biswas et al., "Beyond Scalar Objectives: Expert-Feedback-Driven Autonomous Experimentation for Scientific Discovery at the Nanoscale" (DKPL), arXiv:2605.21820](https://arxiv.org/abs/2605.21820)
- [Lee, Liang, Kim et al., "Real-time Multi-instrument Autonomous Discovery of Novel Phase-change Memory Materials" (MAD), arXiv:2605.18033](https://arxiv.org/abs/2605.18033)
- [Song, Zhang, Cheng, "Autonomous heterogeneous catalyst discovery with a self-evolving multi-agent digital twin" (CatDT), arXiv:2606.05050](https://arxiv.org/abs/2606.05050)
- [Wang & Buehler, "Self-Revising Discovery Systems for Science: A Categorical Framework for Agentic Artificial Intelligence" (CategoryScienceClaw), arXiv:2606.01444](https://arxiv.org/abs/2606.01444)
- [Rahman & Rahman, "AgentPLM: Agentic Protein Language Models with Reasoning-Augmented Decoding for Protein Sequence Design," arXiv:2606.02386 / ICML 2026](https://arxiv.org/abs/2606.02386)
- [Du, Yu, Liu, Shen, Chen et al., "Accelerating Scientific Discovery with Autonomous Goal-evolving Agents" (SAGA), arXiv:2512.21782](https://arxiv.org/abs/2512.21782)
- [Cong, Smerkous, Wang et al., "LabOS: The AI-XR Co-Scientist That Sees and Works With Humans," arXiv:2510.14861](https://arxiv.org/abs/2510.14861)
- [Lucente, Pascoli, Sala, Zandi, "DarkAgents: towards an agentic system for theoretical astroparticle physics," arXiv:2606.11157](https://arxiv.org/abs/2606.11157)
- [Éltető, Daw, Stachenfeld, Miller, "ATLAS: Active Theory Learning for Automated Science," arXiv:2606.12386](https://arxiv.org/abs/2606.12386)
