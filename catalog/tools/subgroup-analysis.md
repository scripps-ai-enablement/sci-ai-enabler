---
title: Subgroup Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-09
summary: "Run subgroup and heterogeneous-treatment-effect analyses — interaction tests, RERI, causal forests, Bayesian shrinkage — against the Sun BMJ and EMA 2019 credibility criteria"
---

# Subgroup Analysis (bioSkills)

A Claude Code skill for analysing treatment effects across patient subgroups without over-claiming: interaction testing done properly, data-adaptive HTE methods where they are warranted, and a credibility framework applied to whatever comes out.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — `statsmodels`, `scipy`, `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `econml` (Python) and `grf`, `policytree`, `causalToolbox`, `personalized`, `SIDES`/`rsides`, `stepp`, `gMCP`, `partykit`, `RBesT`, `brms` (R) are separately installed OSS. |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python and R), not as an MCP tool |

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
  cp -r bioSkills/clinical-biostatistics/subgroup-analysis ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the Python side on first use with `pip install "statsmodels>=0.14" "scipy>=1.12" "numpy>=1.26" "pandas>=2.1" "matplotlib>=3.8" "scikit-learn>=1.4" econml`; causal-forest work needs R with `install.packages(c("grf", "policytree", "stepp"))`.

## What it does

Routes the question to a method, then subjects the answer to a credibility check.

| Scenario | Method |
|---|---|
| Pre-specified subgroup, confirmatory trial | Interaction term in a single model + graphical multiplicity (`gMCP`) — the EMA 2019 "assessment subgroup" |
| Stratified randomisation (site, region) | CMH, or logistic regression with strata as covariates; stratum-specific ORs in the forest plot |
| Many pre-specified subgroups | Bayesian shrinkage (Dixon–Simon, MAP, EXNEX) rather than independent stratum estimates |
| Exploratory discovery | STEPP, SIDES, causal forests, X- / R-learners — labelled as hypothesis-generating |
| Additive-scale interaction | RERI (> 0 synergism, = 0 no additive interaction, < 0 antagonism) |

Numbers it holds you to:

- **Detecting an interaction needs roughly 4× the sample size of the main effect** (Brookes 2004). This is why most subgroup analyses are underpowered by construction.
- **0.5σ** standardised effect as the "noteworthy heterogeneity" benchmark (Dane 2019, EFSPI).
- **≤ 20% of total α** for exploratory subgroups (EMA 2019).
- Minimum **n ≥ 5 per cell** for CMH to avoid sparse-data bias; Breslow–Day is unreliable with fewer than 5 strata.
- Bayesian shrinkage prior: `tau ~ HalfNormal(0, 0.1)` conservative, `HalfNormal(0, 0.5)` regulatory-tolerant, with a sensitivity sweep across 0.1–0.5 expected.
- EXNEX mixture weights default **0.5 / 0.5**, swept over 0.1–0.9.
- Causal-forest honest-split fraction typically **0.5**; tune with `tune.parameters = "all"`.

Credibility is assessed against the **Sun BMJ 2012 11-criterion checklist** and the **EMA 2019 subgroup guideline**.

**Primary use cases**: pre-specifying a subgroup strategy in an SAP, assessing whether an observed subgroup effect is credible, exploratory HTE discovery.

## Notes

**A subgroup-specific p-value is not evidence of a differential effect** — the interaction test is, and it is the comparison the skill insists on. Reporting "significant in men, not in women" without an interaction test is the classic failure this skill is built to prevent.

Ignoring the randomisation strata is a real cost, not a conservatism: Kahan–Morris 2012 show it biases standard errors upward and loses power, so stratified designs must be analysed as stratified.

Data-adaptive methods (causal forests, SIDES) find subgroups by searching, so their output is hypothesis-generating regardless of how the split is scored. The honest-splitting and cross-fitting machinery controls estimation bias within a discovered subgroup, not the selection itself.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-clinical-biostatistics-subgroup-analysis`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/subgroup-analysis`. Upstream directory: `clinical-biostatistics/subgroup-analysis`.

Related: [Multiplicity and Graphical Procedures](multiplicity-graphical.html) (defines the α budget this analysis spends), [Bayesian Trials](bayesian-trials.html) (the MAP/EXNEX shrinkage machinery), [Power and Sample Size](power-and-sample-size.html) (the 4× interaction penalty), [Trial Reporting](trial-reporting.html), [statsmodels](statsmodels.html), [scikit-learn](scikit-learn.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`clinical-biostatistics/subgroup-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/subgroup-analysis/SKILL.md)
- [EMA Guideline on the investigation of subgroups in confirmatory clinical trials (2019)](https://www.ema.europa.eu/en/investigation-subgroups-confirmatory-clinical-trials-scientific-guideline)
- [Sun et al., *BMJ* 2012;344:e1553 — credibility of subgroup analyses](https://doi.org/10.1136/bmj.e1553)
- [`grf` on CRAN](https://cran.r-project.org/package=grf)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=subgroup-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fsubgroup-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
