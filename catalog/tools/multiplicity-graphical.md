---
title: Multiplicity and Graphical Procedures (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-09
summary: "Build the multiplicity strategy for confirmatory trials — graphical Bretz-Maurer-Hommel procedures, gatekeeping and Holm/Hochberg/Hommel — with gMCP and FDA 2022 guidance"
verification: works
verified_on: 2026-08-13
reviewed_on: 2026-08-13
security: cleared
security_on: 2026-08-13
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.2k stars, no external credentials"
---

# Multiplicity and Graphical Procedures (bioSkills)

A Claude Code skill for designing the multiplicity strategy of a confirmatory trial: allocating α across primary, key-secondary and subgroup families, and choosing a procedure that actually controls the familywise error rate under the dependence you have.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — `gMCP`, `graphicalMCP`, `gatekeeping`, `multcomp`, `multxpert` (R) and `statsmodels` (Python) are separately installed OSS. |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (R, with a Python fallback), not as an MCP tool |
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
  cp -r bioSkills/clinical-biostatistics/multiplicity-graphical ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the R packages on first use, e.g. `install.packages(c("gMCP", "graphicalMCP", "multcomp"))`; the Python route needs `pip install "statsmodels>=0.14"` for `multipletests`. `gMCP` 0.8.16+ and `graphicalMCP` 0.2+ are the versions the skill targets.

## What it does

Walks a decision tree from the trial's claim structure to a specific procedure:

1. **Confirmatory or exploratory?** A regulatory claim requires FWER control. Exploratory work can use FDR (Benjamini–Hochberg) — the skill treats mixing the two up as the primary error.
2. **Is there a strict clinical priority ordering?** If yes, fixed-sequence (serial gatekeeping) or a chain graph.
3. **How many endpoints, and what dependence?**
   - ≤ 3 endpoints, dependence unknown → **Holm** (universally valid)
   - ≤ 3 endpoints, positive correlation established → **Hochberg** or **Hommel**, after verifying PRDS
   - ≥ 4 endpoints with a primary / key-secondary / subgroup hierarchy → **graphical procedure** via `gMCP`
   - Multiple distinct families → **parallel or serial gatekeeping**
4. **Can endpoints move in opposite directions?** (LDL vs HDL, efficacy vs safety) → **Holm only** — PRDS fails and Hochberg is anti-conservative there.

Underlying theory the skill implements: the closed-testing principle (Marcus–Peritz–Gabriel, with Goeman 2021 admissibility), Bretz–Maurer–Hommel graphical procedures, and gatekeeping in parallel, serial and mixed forms.

Calibration numbers it carries:

| Threshold | Value | Source |
|---|---|---|
| Bonferroni power loss at ~10 tests under positive dependence | 30–50% | Sarkar 1998 (PRDS) |
| Hommel gain over Hochberg under PRDS | 1–3% | Hommel 1988, *Biometrika* |
| Subgroup α budget | ≤ 20% of total | Dane 2019, EFSPI white paper |
| Confirmatory FWER level | α = 0.05 (two-sided) | Convention |

**Primary use cases**: allocating α across multiple primary endpoints, designing a key-secondary testing hierarchy, choosing between Holm and Hochberg.

## Notes

**Hochberg's validity is conditional, and the check is the point.** Hochberg and Hommel require positive regression dependence on subsets (PRDS); when it does not hold the Type-I error is inflated, and the skill's rule is to revert to Holm (Sarkar 2008, *Ann Stat*). The opposite-direction endpoint case is the standard counterexample.

Regulatory anchor: the **FDA Multiple Endpoints in Clinical Trials final guidance (October 2022)**. The graph — nodes, weights and α-propagation edges — belongs in the SAP before unblinding; a graph fitted after seeing the data controls nothing.

FWER and FDR are not interchangeable knobs. FDR is the right target for a screening analysis with many hypotheses; it does not support a regulatory claim on a single endpoint.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-clinical-biostatistics-multiplicity-graphical`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/multiplicity-graphical`. Upstream directory: `clinical-biostatistics/multiplicity-graphical`.

Related: [Subgroup Analysis](subgroup-analysis.html) (which spends the ≤ 20% subgroup α budget defined here), [Power and Sample Size](power-and-sample-size.html) (a split α changes n), [Adaptive Designs](adaptive-designs.html) (interim looks consume α through a spending function, on top of the endpoint split), [Trial Reporting](trial-reporting.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-biostatistics/multiplicity-graphical/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/multiplicity-graphical/SKILL.md)
- [FDA Multiple Endpoints in Clinical Trials: Guidance for Industry (2022)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/multiple-endpoints-clinical-trials-guidance-industry)
- [`gMCP` on CRAN](https://cran.r-project.org/package=gMCP)
- [`graphicalMCP` on CRAN](https://cran.r-project.org/package=graphicalMCP)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=multiplicity-graphical&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmultiplicity-graphical.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
