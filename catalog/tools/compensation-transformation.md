---
title: Compensation and Transformation (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Corrects fluorophore spillover or spectral overlap and applies logicle/arcsinh transforms — spillover-matrix estimation, AutoSpill, and cofactor choice for CyTOF vs fluorescence"
---

# Compensation and Transformation (bioSkills)

A Claude Code skill that gets the two steps every cytometry pipeline depends on right: removing spectral overlap between detectors, then applying a variance-stabilizing transform in the correct order.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — flowCore, flowStats, flowWorkspace and CATALYST are separately installed Bioconductor packages |
| **Capabilities** | Read/Write — Claude runs the skill's R workflow locally, not as an MCP tool |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "flow-cytometry"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/flow-cytometry/compensation-transformation ~/.claude/skills/
  ```
  (run from inside the directory holding your clone — if you are still in `bioSkills/` from the previous step, use `cp -r flow-cytometry/compensation-transformation ~/.claude/skills/`, or replace `bioSkills/` with the absolute path of your clone). Install the Bioconductor packages when prompted on first use:
  ```
  R -e 'BiocManager::install(c("flowCore","flowStats","flowWorkspace","CATALYST"))'
  ```

## What it does

Separates the linear correction step from the nonlinear display step, and enforces their order:

- **Compensation (linear, on untransformed data)** — matrix subtraction via `flowCore::compensate()` using the recorded `$SPILLOVER` keyword, or a matrix computed from single-stain controls with `flowStats::spillover()`; AutoSpill (robust regression plus iterative refinement) for panels above ~12 colors.
- **Spectral unmixing** — for full-spectrum instruments (Cytek Aurora, Sony ID7000) the correct operation is least-squares **unmixing** of an overdetermined system, not compensation.
- **Transformation (nonlinear, on compensated data)** — logicle/biexponential via `estimateLogicle()` for fluorescence, arcsinh for mass cytometry and computational pipelines, log₁₀ only as a legacy option on strictly positive data.
- **Spillover spreading matrix** — treated as the panel-design diagnostic: spreading error scales as √(signal intensity), so resolution of a dim marker is bounded by panel choice, not by better compensation.

Stated thresholds and rules:

| Threshold / rule | Value | Source cited upstream |
|---|---|---|
| Arcsinh cofactor, mass cytometry | **5** | Nowicka 2017, *F1000Research* 6:748 |
| Arcsinh cofactor, fluorescence | **~150** (per-channel via flowVS preferred) | CATALYST community convention |
| Compensation control brightness | ≥ sample brightness | Roederer 2001, *Cytometry* 45:194 |
| Spreading error scaling | ∝ √(signal intensity) | Nguyen 2013, *Cytometry A* 83:306 |
| Metal spillover, CyTOF | 1–4% (oxide and isotopic impurity are the real problems) | — |

**Primary use cases**: building a spillover matrix from single-stain controls, choosing logicle vs arcsinh, picking an arcsinh cofactor, distinguishing conventional compensation from spectral unmixing.

## Notes

**Load-bearing ordering rule**: compensate → transform, never the reverse. Compensation is a linear operation and is mathematically invalid after a nonlinear transform; `estimateLogicle()` must run on already-compensated data so its `w`/`a` parameters reflect post-compensation negative spread.

Two API traps the skill calls out: `estimateLogicle()` lives in **flowWorkspace**, not flowCore, and `flowCore::spillover()` returns a list (index `[[1]]`) while `flowStats::spillover()` returns the matrix directly.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the R workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-flow-cytometry-compensation-transformation`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/compensation-transformation`. Upstream directory: `flow-cytometry/compensation-transformation`.

First step of the bioSkills flow-cytometry chain, ahead of [Cytometry QC](cytometry-qc.html), [Gating Analysis](gating-analysis.html), [Clustering and Phenotyping](clustering-phenotyping.html) and [Cytometry Differential Analysis](cytometry-differential-analysis.html). For reading and writing the FCS files themselves in Python, see [FlowIO](flowio.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`flow-cytometry/compensation-transformation/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/compensation-transformation/SKILL.md)
- [flowCore (Bioconductor)](https://bioconductor.org/packages/flowCore/)
- [CATALYST (Bioconductor)](https://bioconductor.org/packages/CATALYST/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=compensation-transformation&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcompensation-transformation.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
