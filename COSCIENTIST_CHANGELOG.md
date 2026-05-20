---
title: AI scientist updates
parent: Updates
nav_order: 3
permalink: /updates/ai-scientists.html
---

# AI scientist updates

Reverse-chronological log of changes to the [AI scientists tracker](autonomous-science/). Newest at the top.

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
