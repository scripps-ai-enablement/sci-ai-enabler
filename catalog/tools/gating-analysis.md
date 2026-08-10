---
title: Gating Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Defines cytometry populations with manual or automated gates — hierarchical GatingSets, openCyto templates, flowDensity thresholds, and FlowJo round-tripping via CytoML"
verification: works
verified_on: 2026-08-10
reviewed_on: 2026-08-10
security: cleared
security_on: 2026-08-10
security_note: "GPTomics/bioSkills MIT root confirmed, provenance matches, bundled Bioconductor packages open source"
---

# Gating Analysis (bioSkills)

A Claude Code skill that builds reproducible, scripted gating hierarchies for flow and spectral cytometry instead of hand-drawn gates that cannot be re-run.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — flowWorkspace, openCyto, flowDensity, flowCore and CytoML are separately installed Bioconductor packages |
| **Capabilities** | Read/Write — Claude runs the skill's R workflow locally, not as an MCP tool |
| **Verified** | works · 2026-08-10 |
| **Security** | cleared · 2026-08-10 — MIT, provenance matches, bundled Bioconductor packages open source |

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
  cp -r bioSkills/flow-cytometry/gating-analysis ~/.claude/skills/
  ```
  (run from inside the directory holding your clone — if you are still in `bioSkills/` from the previous step, use `cp -r flow-cytometry/gating-analysis ~/.claude/skills/`, or replace `bioSkills/` with the absolute path of your clone). Install the Bioconductor packages when prompted on first use:
  ```
  R -e 'BiocManager::install(c("flowWorkspace","openCyto","flowDensity","flowCore","CytoML"))'
  ```

## What it does

Organizes gates as a hierarchical `GatingSet` so the whole hierarchy is code and can be re-applied across samples:

- **Gate sequence** — time filtering → debris removal on FSC/SSC → singlet detection on FSC-A vs FSC-H → viability gating → lineage classification. The order is a funnel; reordering bakes upstream artifacts into every downstream population.
- **Manual gates** — `rectangleGate`, `polygonGate`, quadrant and boolean gates added with `gs_pop_add()` and applied with `recompute()`.
- **Automated gating** — openCyto CSV gating templates (`mindensity`, `tailgate`, `quantileGate`, `gate_flowclust_2d`) or flowDensity's sequential data-driven bivariate density thresholds; flowClust for model-based gates.
- **FlowJo interoperability** — workspaces read and written via CytoML, so an existing manual hierarchy can be imported and then applied programmatically.
- **Statistics** — population counts and frequencies extracted with `gs_pop_get_stats()`.

Stated thresholds:

| Rule | Value |
|---|---|
| Events needed for a coefficient of variation < 15% | ~50–60 (Poisson floor for rare-event counting) |
| Cells to acquire for 1e-5 sensitivity | ~1e6 |
| Practical rare-event detection floor | 1e-4 to 1e-5 frequency |

**Primary use cases**: reproducible immunophenotyping hierarchies, automated gating across many samples, rare-event and MRD-style gating, importing and re-running FlowJo workspaces.

## Notes

**FMO controls, not isotype controls, set gate boundaries** — spreading error is what sets the positive/negative edge (Roederer 2001); isotype controls only address nonspecific binding and place the boundary incorrectly.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the R workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-flow-cytometry-gating-analysis`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/gating-analysis`. Upstream directory: `flow-cytometry/gating-analysis`.

Run after [Compensation and Transformation](compensation-transformation.html) and [Cytometry QC](cytometry-qc.html). For high-parameter panels where a manual hierarchy is impractical, use [Clustering and Phenotyping](clustering-phenotyping.html) instead; either route feeds [Cytometry Differential Analysis](cytometry-differential-analysis.html). For reading and writing FCS files in Python, see [FlowIO](flowio.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`flow-cytometry/gating-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/gating-analysis/SKILL.md)
- [openCyto (Bioconductor)](https://bioconductor.org/packages/openCyto/)
- [flowWorkspace (Bioconductor)](https://bioconductor.org/packages/flowWorkspace/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=gating-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgating-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
