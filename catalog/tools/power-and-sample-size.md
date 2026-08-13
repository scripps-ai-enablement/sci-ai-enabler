---
title: Power and Sample Size (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-09
summary: "Size superiority, non-inferiority and equivalence trials for continuous, binary and survival endpoints, with FDA M1/M2 margin logic and CONSORT-ready justification"
verification: works
verified_on: 2026-08-13
reviewed_on: 2026-08-13
security: cleared
security_on: 2026-08-13
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.2k stars, no external credentials"
---

# Power and Sample Size (bioSkills)

A Claude Code skill for justifying trial size in a protocol or SAP — picking the right formula for the endpoint and design, setting a defensible non-inferiority margin, and writing the CONSORT item 16a justification.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — `statsmodels`, `scipy`, `numpy`, `pandas` and the R packages `pwr`, `gsDesign`, `gsDesign2`, `rpact`, `presize`, `npsurvSS`, `nph`, `simtrial`, `PowerTOST`, `clusterPower`, `ratesci`, `nlme` are separately installed OSS. The commercial alternatives (nQuery, PASS, East) are not installed. |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python and R), not as an MCP tool |
| **Verified** | works · 2026-08-13 |
| **Security** | cleared · 2026-08-13 — GPTomics/bioSkills MIT, no external credentials |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "clinical-biostatistics"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/clinical-biostatistics/power-and-sample-size ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the Python side on first use with `pip install "statsmodels>=0.14" "scipy>=1.12" "numpy>=1.26" "pandas>=2.1"`; survival and bioequivalence work additionally needs R with `install.packages(c("gsDesign", "rpact", "npsurvSS", "PowerTOST"))`.

## What it does

Covers continuous, binary and time-to-event endpoints across superiority, non-inferiority and equivalence framings, and drives `statsmodels` (primary) with R packages for the cases Python does not cover well:

- **Superiority sizing** — effect size on the Cohen scale (d = 0.2 small, 0.5 medium, 0.8 large) at two-sided α = 0.05, with the skill's rule that the design difference δ should be **≥ 1.5 × MCID**, because setting δ equal to the minimum clinically important difference leaves no margin for sampling variation (Norman 2003).
- **Non-inferiority margins** — the FDA 2016 M1/M2 framework at one-sided α = 0.025: **M2 ≤ 0.5 × historical M1** (the "double discount" that guards against biocreep) and **M2 ≤ 0.5 × MCID**, since the loss you are willing to accept must be smaller than a difference that would be clinically meaningful.
- **Survival endpoints** — Schoenfeld 1981 for the event-driven count under proportional hazards, and Lakatos 1988 or simulation when it does not hold. The skill flags that **Schoenfeld under-estimates by 20–50% under non-proportional hazards** (Lin 2020, NPH Working Group), which is the delayed-effect case typical of immuno-oncology.
- **Bioequivalence** — Schuirmann's two one-sided tests, targeting a **90% CI for the geometric mean ratio of C<sub>max</sub>/AUC inside (0.80, 1.25)** per the FDA 1992 guidance, via `PowerTOST`.
- **Inflation and design factors** — dropout inflation `n_final = n / (1 − q)` (q = 0.20 → multiply by 1.25); the stratified-randomisation efficiency gain `n / (1 − r²)` (Senn 2013); the cluster design effect `1 + (m − 1)·ICC`.
- **Adaptive interaction** — if the size may be re-estimated at an interim, unblinded SSR needs **Cui–Hung–Wang weighting** to hold the Type-I error, and the Mehta–Pocock promising zone is calibrated for a conditional power range of roughly **30–80%**.

**Primary use cases**: writing the sample-size section of a protocol or SAP, choosing a non-inferiority margin, sizing an event-driven survival trial.

## Notes

**MCID and δ are not the same number** and the skill treats conflating them as the headline error. The MCID is a property of the outcome measure; δ is a design choice that must sit above it.

The skill notes that applying a **continuity correction to binary comparisons wastes roughly 10% of the sample size** (D'Agostino 1988, *Am Stat* 42:198) and that modern computing makes exact or score-based intervals (`ratesci`, Miettinen–Nurminen) the better default.

Regulatory anchors cited: the **FDA 2016 non-inferiority guidance** (M1/M2), the **FDA 1992 bioequivalence guidance** (80–125%), and **CONSORT 2025 item 16a**, which is the reporting requirement this skill's output is written to satisfy.

A power calculation for a fixed design is a different problem from a group-sequential one — for interim looks, spending functions and sample-size re-estimation, use [Adaptive Designs](adaptive-designs.html), which drives the same `rpact`/`gsDesign` stack.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-clinical-biostatistics-power-sample-size`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/power-and-sample-size`. Upstream directory: `clinical-biostatistics/power-and-sample-size`.

Related: [Multiplicity and Graphical Procedures](multiplicity-graphical.html) (α is an input to this calculation, and splitting it changes n), [Subgroup Analysis](subgroup-analysis.html) (interaction tests need roughly 4× the main-effect sample size), [Trial Reporting](trial-reporting.html), [statsmodels](statsmodels.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-biostatistics/power-and-sample-size/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/power-and-sample-size/SKILL.md)
- [FDA Non-Inferiority Clinical Trials to Establish Effectiveness (2016)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/non-inferiority-clinical-trials)
- [`PowerTOST` on CRAN](https://cran.r-project.org/package=PowerTOST)
- [`rpact` on CRAN](https://cran.r-project.org/package=rpact)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=power-and-sample-size&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpower-and-sample-size.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
