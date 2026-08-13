---
title: TAD Detection (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Call TAD boundaries from balanced Hi-C matrices with cooltools insulation scores, including the window sweep and boundary-strength ranking"
verification: works
verified_on: 2026-08-13
reviewed_on: 2026-08-13
security: cleared
security_on: 2026-08-13
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.2k stars, no external credentials"
---

# TAD Detection (bioSkills)

A Claude Code skill for calling topologically associating domain boundaries from a Hi-C contact matrix, built around the diamond-window insulation score rather than a single hard domain partition.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — cooltools and HiCExplorer are installed separately (both open source) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python/Bash), not as an MCP tool |
| **Verified** | works · 2026-08-13 |
| **Security** | cleared · 2026-08-13 — GPTomics/bioSkills MIT, no external credentials |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "hi-c-analysis"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/hi-c-analysis/tad-detection ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites — the Python Hi-C stack** (the skill drives these; they are not bundled):
  ```
  pip install "cooler>=0.10" "cooltools>=0.7" "bioframe>=0.7"
  ```
- **Optional — HiCExplorer 3.7+** for the `hicFindTADs` alternative:
  ```
  conda install -c conda-forge -c bioconda hicexplorer
  ```
  Confirm with `hicFindTADs --version`. HiCExplorer pulls a large dependency tree; skip it if you only need the cooltools path.

## What it does

Produces a continuous insulation track and a ranked boundary list, not just a BED file of domains:

- **Insulation score** — `cooltools.insulation()` slides a diamond window along the diagonal of a balanced matrix and reports log2 insulation per bin, so a boundary is a *valley* whose depth is measurable.
- **Boundary strength** — valley prominence, returned as `boundary_strength_{W}` alongside Li/Otsu-thresholded `is_boundary_{W}` flags, giving a ranking rather than a binary call.
- **Multi-scale window sweep** — the skill sweeps a list of window sizes (roughly `[3×bin, 5×bin, 10×bin, …]`), from sub-TAD scale up to compartment-domain scale, because "TAD" is not a single-scale object.
- **Cross-condition comparison** — compares the differential insulation *score* between conditions instead of intersecting two domain partitions.
- **Boundary annotation** — supports CTCF-backed boundary annotation; overlap with other genomic features is routed to interval tooling, and domain rendering to the sibling Hi-C visualization skill.
- **HiCExplorer alternative** — `hicFindTADs` as a second implementation.

**Primary use cases**: calling domain boundaries from a cooler, choosing an insulation window size, ranking and comparing boundaries across conditions.

## Notes

Two input requirements will silently ruin a run if missed, and the skill states both. The cooler **must be balanced** (a stored `weight` column) — an unbalanced matrix returns all-NaN insulation, not an error. And a multi-resolution `.mcool` must be addressed with a single-resolution URI (`file.mcool::/resolutions/10000`), never the bare `.mcool` path. Balance first with `cooler balance` or `cooler.balance_cooler()`.

The conceptual point the skill leads with is that **the boundary is reproducible but the domain partition is not**: different callers and different windows agree far better on where insulation dips than on how to segment the genome into domains, which is why the recommended output is a scored boundary track and why cross-condition work compares scores rather than partitions. Insulation is also treated as orthogonal to compartmentalization — a boundary call says nothing about A/B state.

Note the cooltools API shifted around 0.5→0.7 and standardized on `view_df`/viewframe arguments; pin `cooltools>=0.7` or the documented call signatures will not match. Upstream skill front-matter name is `bio-hi-c-analysis-tad-detection` (`tool_type: mixed`, `primary_tool: cooltools`); upstream directory `hi-c-analysis/tad-detection`. Pairs with [Chromatin Loop Calling](loop-calling.html) (focal interactions rather than domain boundaries), [A/B Compartment Analysis](compartment-analysis.html) (the orthogonal megabase-scale layer), [bedtools](bedtools-genomic-intervals.html) for boundary-feature overlap, and [HOMER](homer-motif-analysis.html) / [JASPAR](jaspar-database.html) for CTCF motif orientation at boundaries.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`hi-c-analysis/tad-detection/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/hi-c-analysis/tad-detection/SKILL.md)
- [cooltools documentation](https://cooltools.readthedocs.io/)
- [cooler documentation](https://cooler.readthedocs.io/)
- [HiCExplorer documentation](https://hicexplorer.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tad-detection&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftad-detection.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
