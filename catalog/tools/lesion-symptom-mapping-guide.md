---
title: Lesion-Symptom Mapping Guide (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Awesome Cognitive and Neuroscience Skills
availability: GA
tool_categories: [Neuroscience, Translational Medicine]
last_verified: 2026-08-09
summary: "Plan and run lesion-symptom mapping in patient cohorts — VLSM, multivariate SVR-LSM, disconnection and lesion network mapping"
verification: works
verified_on: 2026-08-10
reviewed_on: 2026-08-10
security: cleared
security_on: 2026-08-10
security_note: "repo-renamed flag confirmed genuine org transfer to NeuroAIHub this run, MIT, old URL still redirects live, same pattern as sibling skills"
---

# Lesion-Symptom Mapping Guide (Claude Skill)

Guides Claude through inferring brain–behaviour relationships from patient lesion data — segmenting and normalizing lesions, choosing between voxel-wise and multivariate mapping, and correcting for the spatial dependence that makes naive statistics wrong here.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Awesome Cognitive and Neuroscience Skills](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills) (community OSS, MIT) |
| **Availability** | GA — one of ~40 research skills in the collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — methodology guidance; Claude writes and runs the analysis code locally |
| **Verified** | works · 2026-08-10 |
| **Security** | cleared · 2026-08-10 — MIT, org transferred to NeuroAIHub (confirmed), old URL still redirects |

## How to install

- **Claude Code** — plugin marketplace (installs all skills in the collection):
  ```
  /plugin marketplace add HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  /plugin install awesome-cognitive-and-neuroscience-skills@awesome-cognitive-and-neuroscience-skills
  ```
  Restart Claude Code afterwards. The skills are description-activated — there is no slash command; ask a lesion-mapping question and Claude loads the skill.
- **Claude Code** — single-skill alternative. This skill declares a required dependency on the collection's `research-literacy` skill, so copy **both**:
  ```
  git clone https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  cp -r awesome_cognitive_and_neuroscience_skills/skills/lesion-symptom-mapping-guide ~/.claude/skills/
  cp -r awesome_cognitive_and_neuroscience_skills/skills/research-literacy ~/.claude/skills/
  ```
  (Project-scoped alternative: copy into `.claude/skills/` instead. The repo's default branch is `master`, not `main`.)
- **Underlying software** — the skill is method guidance, not an analysis engine, and it pins no versions. Most of the toolchain it names is MATLAB-based (NiiStat, VLSM2, the SVR-LSM toolbox); LESYMAP is R, BCBToolkit is a GUI/Python disconnection package, and registration runs through ANTs or FSL.

## What it does

Runs a five-stage protocol: research planning → lesion segmentation → registration → statistical analysis → validation.

**Method selection** by cohort size and question:

- N ≥ 50 with a continuous outcome → **VLSM** (mass-univariate voxel-wise)
- N ≥ 100 and distributed patterns expected → **SVR-LSM** (multivariate; the skill puts its own floor at N ≥ 80–100)
- N < 50 → ROI-based or descriptive analysis only, on the grounds that voxel-wise mapping is underpowered
- White-matter pathway questions → **disconnection analysis**
- Network-level questions → **lesion network mapping**

**Thresholds it enforces**: a voxel is tested only where lesion overlap reaches ≥ 10% of the sample (or N ≥ 10 patients), with ≥ 15% recommended; multiple comparisons are corrected by permutation-based FWE with 5,000+ permutations, thresholded at the 5th percentile of the maximum-statistic distribution.

**Segmentation and registration**: manual tracing is treated as the gold standard, with semi-automated (LINDA, `lesion_gnb`) and deep-learning alternatives; registration requires **cost-function masking**, and enantiomorphic normalization for large lesions.

**Primary use cases**: stroke and aphasia cohort studies, clinical neuropsychology, mapping post-surgical or traumatic deficits.

## Notes

**AI-generated content — verify before use.** All skills in this collection carry `review_status: ai-generated`, and the README states the content "has not been individually verified by human domain experts." This skill cites Bates et al. 2003, Kimberg et al. 2007, Foulon et al. 2018, Zhang et al. 2014, Boes et al. 2015 and Sperber 2020 — check the sample-size floors and overlap thresholds against those sources. No tool version numbers are pinned upstream.

**The correction choice is the load-bearing part.** Lesion voxels are spatially correlated and lesion anatomy is driven by vascular territory, so the skill states that lesion maps violate the independence assumptions behind FDR and parametric corrections. Permutation FWE is the recommended default, Benjamini-Hochberg FDR an acceptable alternative, Bonferroni "too conservative; almost never detects effects", and uncorrected results never acceptable for publication. Lesion volume is a mandatory covariate.

Related catalogued tools: [fMRIPrep](fmriprep-tool.html) and [Nilearn](nilearn-tool.html) for the preprocessing and image-handling layers, [FreeSurfer](freesurfer-tool.html) for anatomy, and [NetNeuroTools Guide](netneurotools-guide.html) for the network metrics and null models a lesion network mapping analysis feeds into.

## Sources

- [`HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills)
- [`skills/lesion-symptom-mapping-guide/SKILL.md`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/lesion-symptom-mapping-guide/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=lesion-symptom-mapping-guide&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Flesion-symptom-mapping-guide.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
