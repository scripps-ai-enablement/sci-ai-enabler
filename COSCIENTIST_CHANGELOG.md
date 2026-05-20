# Autonomous science changelog

Rolling log of updates to the autonomous-science tracker. Newest entry at the top. See [`COSCIENTIST_AGENT.md`](COSCIENTIST_AGENT.md) for the curation rules and [`autonomous-science/`](autonomous-science/) for the content.

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
