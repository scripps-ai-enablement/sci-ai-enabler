---
title: Neural Population Analysis Guide (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Awesome Cognitive and Neuroscience Skills
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-08-09
summary: "Choose and validate dimensionality-reduction methods for neural population recordings — PCA, GPFA, dPCA and jPCA — with principled dimensionality selection"
verification: works
verified_on: 2026-08-13
reviewed_on: 2026-08-13
security: cleared
security_on: 2026-08-13
security_note: "repo-renamed confirmed genuine org transfer to NeuroAIHub this run, MIT, no external credentials"
---

# Neural Population Analysis Guide (Claude Skill)

Guides Claude through latent-variable analysis of simultaneously recorded neural populations — picking between PCA, GPFA, dPCA and jPCA, normalizing spike rates correctly, and choosing the number of dimensions by cross-validation rather than a variance rule of thumb.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Awesome Cognitive and Neuroscience Skills](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills) (community OSS, MIT) |
| **Availability** | GA — one of ~40 research skills in the collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — methodology guidance; Claude writes and runs the analysis code locally |
| **Verified** | works · 2026-08-13 |
| **Security** | cleared · 2026-08-13 — genuine org transfer to NeuroAIHub confirmed, MIT, no external credentials |

## How to install

- **Claude Code** — plugin marketplace (installs all skills in the collection):
  ```
  /plugin marketplace add HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  /plugin install awesome-cognitive-and-neuroscience-skills@awesome-cognitive-and-neuroscience-skills
  ```
  Restart Claude Code afterwards. The skills are description-activated — there is no slash command; ask a population-analysis question and Claude loads the skill.
- **Claude Code** — single-skill alternative. This skill declares a required dependency on the collection's `research-literacy` skill, so copy **both**:
  ```
  git clone https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  cp -r awesome_cognitive_and_neuroscience_skills/skills/neural-population-analysis-guide ~/.claude/skills/
  cp -r awesome_cognitive_and_neuroscience_skills/skills/research-literacy ~/.claude/skills/
  ```
  (Project-scoped alternative: copy into `.claude/skills/` instead. The repo's default branch is `master`, not `main`.)
- **Underlying software** — the skill is method guidance, not an analysis engine. It names no pinned packages; install whichever implementation you select (for example `pip install elephant` for GPFA, the Kobak dPCA reference implementation, or scikit-learn for PCA).

## What it does

Runs a four-stage protocol — research planning, method selection, preprocessing and analysis, then validation and reporting.

**Method selection decision tree**:

- Dominant co-variation patterns across neurons → **PCA** (linear, static)
- Smooth single-trial latent trajectories → **GPFA** or factor analysis
- Variance attributable to specific task parameters → **dPCA** (demixes stimulus, decision and time)
- Rotational dynamics in motor-cortex-style data → **jPCA**
- Visualization only → t-SNE/UMAP, explicitly **not** for quantitative claims

**Recording requirements** the skill states per method: PCA needs 30+ neurons; GPFA needs 50–100 neurons, 20–50 ms bins and 50+ trials per condition; dPCA needs 20–30+ neurons and 20+ trials per condition.

**Dimensionality selection**: parallel analysis (compare eigenvalues against shuffled data) or cross-validated reconstruction error. GPFA latent count is chosen by leave-one-neuron-out cross-validated log-likelihood over 2–15 dimensions; dPCA regularization lambda is chosen on held-out trials.

**Primary use cases**: Neuropixels and multi-electrode array population dynamics, motor and decision-making trajectory analysis, task-variable demixing.

## Notes

**AI-generated content — verify before use.** All skills in this collection carry `review_status: ai-generated`, and the README states the content "has not been individually verified by human domain experts." This skill cites Cunningham & Yu 2014, Yu et al. 2009, Kobak et al. 2016, Churchland et al. 2012, King & Dehaene 2014 and Humphries 2021 — check the neuron/trial minima and normalization constants against those sources.

Two rules the skill treats as non-negotiable, both worth knowing before you install it:

- **Do not z-score firing rates.** Standard z-scoring inflates low-firing neurons into apparent structure. Use soft normalization — `(rate − mean) / (range + constant)` with a constant of **5 spikes/s** — or a square-root transform.
- **There is no 90% variance rule.** The skill explicitly rejects the standard data-science "keep enough PCs for 90% of variance" heuristic as meaningless for neural data; use parallel analysis or cross-validation instead.

Related catalogued skills in the same collection: [Parameter Recovery Checker](parameter-recovery-checker.html) for validating that a fitted latent model is identifiable, [Calcium Imaging Analysis Guide](calcium-imaging-analysis-guide.html) for the upstream extraction step when the population comes from imaging rather than electrophysiology, and [Drift-Diffusion Model](drift-diffusion-model.html) for the behavioural counterpart. For the recording-side pipeline see [SpikeInterface](spikeinterface-electrophysiology.html).

## Sources

- [`HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills)
- [`skills/neural-population-analysis-guide/SKILL.md`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/neural-population-analysis-guide/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=neural-population-analysis-guide&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fneural-population-analysis-guide.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
