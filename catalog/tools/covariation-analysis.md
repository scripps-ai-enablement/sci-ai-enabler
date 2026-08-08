---
title: Covariation Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Test whether a proposed RNA secondary structure is actually supported by evolutionary covariation, using R-scape and an explicit statistical-power check"
---

# Covariation Analysis (bioSkills)

A Claude Code skill that asks the question most RNA structure claims skip: does the alignment show compensatory substitutions above what phylogeny alone predicts — and does it even have the power to tell?

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — R-scape is installed separately (open source, Rivas Lab) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "rna-structure"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/rna-structure/covariation-analysis ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisite — R-scape 2.0+** (the skill drives it as a CLI; it is not bundled):
  ```
  conda install -c conda-forge -c bioconda rscape
  ```
  bioconda ships `rscape` 2.0.4.a (checked 2026-08-08), which satisfies the skill's 2.0+ requirement. Source tarballs are also published by the [Rivas Lab](http://eddylab.org/R-scape/). Confirm with `R-scape --version` before running the skill.

## What it does

Treats "this RNA has a conserved structure" as a hypothesis to be tested, not asserted:

- **Structure testing** (`-s`) — scores the base pairs of a proposed `#=GC SS_cons` structure against a phylogeny-aware null, and separately scores *alternative* pairs, so a rejected structure and a differently-paired structure are distinguishable outcomes.
- **Power analysis** — estimates the per-pair probability that covariation *could* have been detected given the alignment's diversity. This is the step that turns a negative result into a meaningful one.
- **De novo consensus** (`--cacofold`) — builds a covariation-supported structure when there is no trusted structure to test, suitable for seeding a covariance model or a restrained fold.
- **Outputs** — `<msa>.cov` (covarying pairs with position, score, E-value, substitutions, power), `<msa>.power`, `<msa>.sorted.cov`, and an R2R structure diagram as `.svg`/`.pdf`.

Working numbers carried by the skill: default E-value target **0.05**; a mean alignment power of roughly **10%** is the line between "cannot infer" and "rejects the structure"; alignments should be diverse — around **60% average pairwise identity** rather than 90–95% — and it is the number of *independent substitutions*, not the raw sequence count, that buys power.

**Primary use cases**: validating a conserved-structure claim before building on it, deciding whether an alignment can test structure at all, generating a covariation-supported consensus.

## Notes

Two rules do the real work here. First, a **low-power negative says nothing** — it is not evidence against the structure, and the skill refuses to report it as such. Second, a raw positive covariation score is not enough; only covariation *above the phylogenetic null* counts, which is the whole reason R-scape exists rather than a plain mutual-information calculation. The skill also draws a boundary readers often blur: covariation tests whether a structure is **conserved**, which is a different question from whether the transcript is real, expressed, or functional — that needs expression and functional evidence.

The canonical application is the negative result: R-scape found no covariation support for the proposed HOTAIR, Xist, and SRA lncRNA structures, and the skill uses that as its worked example of an adequately-powered rejection.

Input must be a deep, diverse Stockholm-format alignment carrying a `#=GC SS_cons` line. Upstream skill front-matter name is `bio-rna-structure-covariation-analysis`; upstream directory `rna-structure/covariation-analysis`. Pairs naturally with [ncRNA Search](ncrna-search.html) (a CaCoFold consensus can seed a covariance model), [ViennaRNA](viennarna-structure-prediction.html) (thermodynamic folding, which covariation validates rather than replaces), [RNA Structure Probing](structure-probing.html) (experimental rather than evolutionary evidence), and [Rfam](rfam.html) for curated family alignments to test against.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`rna-structure/covariation-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/rna-structure/covariation-analysis/SKILL.md)
- [R-scape (Rivas Lab)](http://eddylab.org/R-scape/)
- [Rivas, Clements & Eddy, *Nat Methods* 14:45–48 (2017)](https://doi.org/10.1038/nmeth.4066)
- [`bioconda::rscape`](https://anaconda.org/bioconda/rscape)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=covariation-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcovariation-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
