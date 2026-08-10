---
title: Cytometry QC (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Cleans flow, spectral and mass cytometry acquisitions — margin removal, time-based anomaly detection with flowAI/PeacoQC/flowCut, dead-cell and CyTOF checks, batch outlier flagging"
verification: works
verified_on: 2026-08-10
reviewed_on: 2026-08-10
security: cleared
security_on: 2026-08-10
security_note: "GPTomics/bioSkills MIT root confirmed, provenance matches, bundled Bioconductor packages open source"
---

# Cytometry QC (bioSkills)

A Claude Code skill that removes acquisition artifacts from flow, spectral and mass cytometry files before any gating or clustering — clogs, signal drift, boundary events and off-spec CyTOF acquisitions.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — flowAI, PeacoQC, flowCore, flowDensity and CATALYST are separately installed Bioconductor packages |
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
  cp -r bioSkills/flow-cytometry/cytometry-qc ~/.claude/skills/
  ```
  (run from inside the directory holding your clone — if you are still in `bioSkills/` from the previous step, use `cp -r flow-cytometry/cytometry-qc ~/.claude/skills/`, or replace `bioSkills/` with the absolute path of your clone). Install the Bioconductor packages when prompted on first use:
  ```
  R -e 'BiocManager::install(c("flowAI","PeacoQC","flowCore","flowDensity","CATALYST"))'
  ```

## What it does

Enforces a QC order that most hand-rolled pipelines get wrong, then applies the time-series cleaners:

- **Order of operations** — compensate/unmix → transform → margin removal (`RemoveMargins()`) → time-based QC → debris/doublet/dead-cell gating → batch normalization. Margins must precede any density-based step or the boundary pile-up creates spurious density ridges.
- **Time-based anomaly cleaning** — flowAI (1.32+), PeacoQC (1.12+), flowCut and flowClean, targeting clogs, bubbles and monotonic signal drift.
- **Mass cytometry checks** — `Event_length` window, bead-based sensitivity drift, retuning cadence.
- **Batch-level outlier flagging** — per-sample summaries compared across a run to catch a single bad acquisition before it reaches differential testing.

Stated thresholds and defaults:

| Parameter | Value |
|---|---|
| PeacoQC `MAD` | 6 (default; higher is less strict) |
| PeacoQC `IT_limit` | 0.55 (default; higher is less strict) |
| flowClean minimum events | ~30,000 — below this, CLR frequency tracking under-detects |
| CyTOF `Event_length` | 10–75 (confirm per instrument) |
| Dead-cell fraction | 10–30% is reported as a sample-handling flag, not auto-excluded |
| CyTOF retuning | daily, or per long run — sensitivity decays from cone fouling |

**Primary use cases**: pre-gating QC of FCS files, detecting clogs and signal drift, flagging outlier samples in a multi-batch immunophenotyping study.

## Notes

The time parameter is the master QC axis: a missing or mis-scaled `$TIMESTEP` keyword silently breaks every time-based tool, so the skill checks it first. Dead-cell percentage is treated as metadata about sample handling rather than a filter threshold.

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the R workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-flow-cytometry-cytometry-qc`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/cytometry-qc`. Upstream directory: `flow-cytometry/cytometry-qc`.

Sits first in the bioSkills flow-cytometry chain: [Compensation and Transformation](compensation-transformation.html) → this skill → [Gating Analysis](gating-analysis.html) → [Clustering and Phenotyping](clustering-phenotyping.html) → [Cytometry Differential Analysis](cytometry-differential-analysis.html). For reading and writing the FCS files themselves in Python, see [FlowIO](flowio.html).

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`flow-cytometry/cytometry-qc/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/cytometry-qc/SKILL.md)
- [PeacoQC (Bioconductor)](https://bioconductor.org/packages/PeacoQC/)
- [flowAI (Bioconductor)](https://bioconductor.org/packages/flowAI/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cytometry-qc&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcytometry-qc.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
