---
title: NetNeuroTools Guide (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Awesome Cognitive and Neuroscience Skills
availability: GA
tool_categories: [Neuroscience]
last_verified: 2026-08-09
summary: "Network neuroscience with netneurotools — consensus connectomes, graph metrics, modularity, spatial autocorrelation-preserving null models and permutation statistics"
---

# NetNeuroTools Guide (Claude Skill)

Guides Claude through connectome analysis with the Network Neuroscience Lab's `netneurotools` package — building consensus networks, computing communication and assortativity metrics, and testing them against null models that preserve degree, distance or spatial autocorrelation.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [Awesome Cognitive and Neuroscience Skills](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills) (community OSS, MIT) |
| **Availability** | GA — one of ~40 research skills in the collection |
| **Pricing** | Free / OSS (MIT) — `netneurotools` itself is BSD-3-Clause |
| **Capabilities** | Read/Write — methodology guidance; Claude writes and runs the analysis code locally |

## How to install

- **Claude Code** — plugin marketplace (installs all skills in the collection):
  ```
  /plugin marketplace add HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  /plugin install awesome-cognitive-and-neuroscience-skills@awesome-cognitive-and-neuroscience-skills
  ```
  Restart Claude Code afterwards. The skills are description-activated — there is no slash command; ask a connectome or brain-network question and Claude loads the skill.
- **Claude Code** — single-skill alternative:
  ```
  git clone https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills
  cp -r awesome_cognitive_and_neuroscience_skills/skills/netneurotools-guide ~/.claude/skills/
  ```
  (Project-scoped alternative: copy into `.claude/skills/` instead. The repo's default branch is `master`, not `main`. Unlike most skills in this collection, this one declares no `research-literacy` dependency — copy that directory too if you want the collection's shared literature conventions.)
- **Underlying software** — install the package the skill drives:
  ```
  pip install "netneurotools[pyvista]"
  ```
  The extra pulls PyVista for surface plotting; drop it if you only need metrics. Core dependencies are numpy ≥ 1.16, scipy ≥ 1.4.0, scikit-learn, matplotlib, nibabel ≥ 3.0.0, nilearn, `bctpy` and `neuromaps`.

## What it does

Walks the eight `netneurotools` submodules as a pipeline:

1. **`datasets`** — fetch templates, parcellations and reference connectomes.
2. **`networks`** — build group consensus connectivity and apply thresholding.
3. **`metrics`** — communication measures, assortativity and related graph statistics.
4. **`spatial`** — spatial autocorrelation statistics: Moran's I, Geary's C, Lee's L.
5. **`modularity`** — consensus community detection.
6. **`stats`** — permutation tests and dominance analysis.
7. **Null models** — randomizations and surrogates that preserve degree and/or distance.
8. **`plotting`** — cortical surface renderings and heatmaps.

**Parameter rules the skill states**: consensus modularity requires non-negative input, so zero out negative weights with `A[A < 0] = 0` before running Louvain; convert weights to distances for communication metrics via `D = -np.log(W / (np.max(W) + 1))`; and remember that a permutation p-value cannot go below `1 / (n_perm + 1)` — 1,000 permutations floors you at ~0.001, so report the permutation count alongside any p-value.

**Primary use cases**: structural and functional connectome analysis, brain-map correspondence testing against spatial nulls, community/module detection in parcellated networks.

## Notes

**AI-generated content — verify before use.** All skills in this collection carry `review_status: ai-generated`, and the README states the content "has not been individually verified by human domain experts." This skill's front-matter lists no cited papers — check its parameter guidance against the [netneurotools documentation](https://netneurotools.readthedocs.io/) before relying on it.

The null-model layer is the reason to reach for this package over a generic graph library: brain-network statistics compared against a plain random-graph null routinely produce significance that reflects spatial embedding rather than biology.

Related catalogued tools: [BrainNetworkTransformer](bnt.html) and [Com-BrainTF](combraintf.html) for deep-learning approaches to the same connectome matrices, [Nilearn](nilearn-tool.html) for constructing them from fMRI, [Pycortex Guide](pycortex-guide.html) for surface rendering, and [Lesion-Symptom Mapping Guide](lesion-symptom-mapping-guide.html) for the lesion-network case.

## Sources

- [`HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills)
- [`skills/netneurotools-guide/SKILL.md`](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/netneurotools-guide/SKILL.md)
- [netneurotools documentation](https://netneurotools.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=netneurotools-guide&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fnetneurotools-guide.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
