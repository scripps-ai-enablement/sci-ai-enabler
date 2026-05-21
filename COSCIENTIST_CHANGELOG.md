---
title: AI scientist updates
parent: Updates
nav_order: 3
permalink: /updates/ai-scientists.html
---

# AI scientist updates

Reverse-chronological log of changes to the [AI scientists tracker](autonomous-science/). Newest at the top.

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
