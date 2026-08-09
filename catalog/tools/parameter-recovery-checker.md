---
title: Parameter Recovery Checker (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Awesome Cognitive and Neuroscience Skills
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-08-09
summary: "Run parameter- and model-recovery simulations to check a cognitive model is identifiable before you interpret its fitted parameters"
---

# Parameter Recovery Checker (Claude Skill)

Guides Claude through a simulate-and-refit study that answers a question most modeling papers skip: can this model's parameters be recovered at all, or are the numbers you fitted an artifact of an unidentifiable model?

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Awesome Cognitive and Neuroscience Skills](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills) (community OSS, MIT) |
| **Availability** | GA — one of ~40 research skills in the collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — methodology guidance; Claude writes and runs the simulation and fitting code locally |

## How to install

- **Claude Code** — plugin marketplace (installs all skills in the collection):
  ```
  /plugin marketplace add HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  /plugin install awesome-cognitive-and-neuroscience-skills@awesome-cognitive-and-neuroscience-skills
  ```
  Restart Claude Code afterwards. The skills are description-activated — there is no slash command; ask about model identifiability or parameter recovery and Claude loads the skill.
- **Claude Code** — single-skill alternative. This skill declares a required dependency on the collection's `research-literacy` skill, so copy **both**:
  ```
  git clone https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  cp -r awesome_cognitive_and_neuroscience_skills/skills/parameter-recovery-checker ~/.claude/skills/
  cp -r awesome_cognitive_and_neuroscience_skills/skills/research-literacy ~/.claude/skills/
  ```
  (Project-scoped alternative: copy into `.claude/skills/` instead. The repo's default branch is `master`, not `main`.)
- **Underlying software** — the skill is method guidance and pins no packages; it drives whatever simulator and fitter your model already uses.

## What it does

Runs a nine-stage protocol: research planning → define the parameter space (100–1,000+ ground-truth sets via uniform grid, Latin hypercube, random uniform or prior-based sampling) → simulate data matching the real experimental design exactly → refit with the **identical** procedure used on real data, from 5–10 random starting points per dataset → evaluate recovery → check cross-parameter tradeoffs → model recovery → sample-size analysis → objective-function landscape inspection.

**Recovery quality bands** the skill applies:

| Metric | Good | Acceptable | Concerning |
|---|---|---|---|
| Pearson *r* (true vs. recovered) | > 0.9 | > 0.8 | < 0.7 |
| Bias | ~0 | < 10% of range | > 20% of range |
| Coverage of 95% CIs (Bayesian) | ~95% | 85–100% | < 80% |
| Model-recovery confusion-matrix diagonal | > 90% | — | < 70% |

**Tradeoff rule**: recovered parameters correlating at **|r| > 0.5** signal an identifiability problem even when each parameter's marginal recovery looks fine. The remedies offered are fixing one parameter to a theoretically motivated value, reparameterizing, collecting more data, or reporting the tradeoff and interpreting cautiously.

**Model recovery**: if one model is selected when data actually came from another more than 20% of the time, the skill treats the two as indistinguishable for that design.

**Primary use cases**: validating reinforcement-learning, drift-diffusion and Bayesian cognitive models before publication; determining the minimum trial count a design needs; diagnosing why two model variants cannot be told apart.

## Notes

**AI-generated content — verify before use.** All skills in this collection carry `review_status: ai-generated`, and the README states the content "has not been individually verified by human domain experts." This skill cites Heathcote et al. 2015, Wilson & Collins 2019, Wagenmakers et al. 2004 and Navarro 2019 — check the recovery thresholds against those sources.

**Explicit scope exclusion**: the skill addresses *identifiability only*. It does not assess whether a recoverable model is a valid account of cognition — the seventh of its seven listed pitfalls is precisely "confusing identifiability with validity."

Its 12-item reporting checklist expects the sampling strategy, ground-truth ranges, per-parameter *r*/bias/RMSE, recovered-vs-true scatter plots, the parameter correlation matrix, the model-recovery confusion matrix and recovery as a function of trial count.

Related catalogued skills in the same collection: [Drift-Diffusion Model](drift-diffusion-model.html), whose own eighth stage is a parameter-recovery check this skill expands into a full study, and [Neural Population Analysis Guide](neural-population-analysis-guide.html). For the fitting machinery see [PyMC](pymc.html) and [statsmodels](statsmodels.html).

## Sources

- [`HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills)
- [`skills/parameter-recovery-checker/SKILL.md`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/parameter-recovery-checker/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=parameter-recovery-checker&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fparameter-recovery-checker.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
