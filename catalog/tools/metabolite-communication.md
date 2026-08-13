---
title: Metabolite Cell Communication (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Infer metabolite-mediated cell-cell crosstalk from scRNA-seq by scoring enzyme-to-sensor pairs with MEBOCOST, with explicit limits on what the result supports"
verification: works
verified_on: 2026-08-13
reviewed_on: 2026-08-13
security: cleared
security_on: 2026-08-13
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.2k stars, no external credentials"
---

# Metabolite Cell Communication (bioSkills)

A Claude Code skill for the metabolic layer of cell–cell communication: scoring producing-enzyme against sensor expression to nominate metabolite-mediated crosstalk, while being blunt about how far that inference reaches.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — MEBOCOST and the alternative back-ends are installed separately (all open source) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python), not as an MCP tool |
| **Verified** | works · 2026-08-13 |
| **Security** | cleared · 2026-08-13 — GPTomics/bioSkills MIT, no external credentials |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "single-cell"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/single-cell/metabolite-communication ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites — the single-cell base stack**:
  ```
  pip install "scanpy>=1.10" "anndata>=0.10"
  ```
- **Prerequisite — MEBOCOST 1.0+** (the primary tool). **Unverified —** a PyPI distribution was not confirmed this run, so install from the upstream repository:
  ```
  pip install "git+https://github.com/zhengrongbin/MEBOCOST.git"
  ```
  Confirm with `pip show mebocost`. MEBOCOST also needs its species-matched enzyme/sensor **database and config files**, which ship with the repository — note the path to them, because `create_obj()` takes it as an argument.

The alternatives the skill routes to (scFEA, Compass, NeuronChat) are separate installs and are only needed if the decision rules below point at them.

## What it does

- **Data preparation** — expects a log-normalized AnnData with **gene symbols, not Ensembl IDs**, cell-type labels, and an optional condition column; ambient RNA should be removed first (SoupX, DecontX, or CellBender).
- **Object creation** — `mebocost.create_obj()` with a species-matched config and database path.
- **Inference** — `infer_commu()` scores sender→receiver metabolite pairs using label-permutation testing.
- **Filtering** — keep results at `permutation_test_fdr < 0.05`; transporter-based calls are separated out as lower-confidence.
- **Method routing** — MEBOCOST for enzyme-to-sensor crosstalk between cell types; **scFEA** for relative per-cell metabolic flux (support for metabolite reasoning, not communication itself); **Compass** for comparing metabolic state between conditions via flux-balance analysis — its output measures reaction favourability, not secretion, so it does not license a communication claim; **NeuronChat** for neural systems only (glutamate, GABA, dopamine, serotonin, neuropeptides).

Working parameters: `cutoff_prop = 0.15` (a gene expressed in fewer than 15% of a group is mostly dropout), `n_shuffle = 1000` for a stable permutation FDR, `min_cell_number = 10` to stop tiny groups inflating scores, and FDR rather than raw p-value for filtering.

**Primary use cases**: nominating metabolic crosstalk between cell types, predicting metabolite secretion and sensing, choosing among metabolic-communication methods.

## Notes

The skill's central warning is the reason to prefer it over running MEBOCOST unaided: metabolite-mediated communication is a **double inference**, and the most speculative layer of cell–cell communication analysis. The chain runs enzyme mRNA → protein → activity → flux → metabolite pool → secretion → sensing, and none of those arrows is measured by scRNA-seq. Validation means metabolomics, mass-spectrometry imaging, isotope tracing, or enzyme/sensor perturbation — not a second expression-based method agreeing with the first.

Three failure modes to watch. **Bidirectional transporters** annotated as "sensors" may export rather than import the metabolite, which is why transporter-based hits are downgraded. **Ambient RNA** inflates apparent enzyme expression in non-producing cell types, so decontaminate before inference. And a **species mismatch** — mouse data scored against the human enzyme/sensor database — returns almost nothing, which reads as a negative result rather than a configuration error.

Upstream skill front-matter name is `bio-single-cell-metabolite-communication` (`tool_type: python`, `primary_tool: MeboCost`); upstream directory `single-cell/metabolite-communication`. Pairs with [CellChat](cellchat-cell-communication.html) and [LIANA](liana-mcp.html) for the better-established ligand–receptor layer, [COBRApy](cobrapy.html) for constraint-based metabolic modelling, [scanpy](scanpy.html) / [AnnData](anndata.html) for the data objects, and [Metabolomics Workbench](metabolomics-workbench-database.html) or [HMDB](hmdb-database.html) when looking for the measured metabolite evidence the skill asks for.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`single-cell/metabolite-communication/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/single-cell/metabolite-communication/SKILL.md)
- [MEBOCOST (`zhengrongbin/MEBOCOST`)](https://github.com/zhengrongbin/MEBOCOST)
- [scFEA (`changwn/scFEA`)](https://github.com/changwn/scFEA)
- [Compass (`YosefLab/Compass`)](https://github.com/YosefLab/Compass)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=metabolite-communication&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmetabolite-communication.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
