---
title: A/B Compartment Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Call A/B chromatin compartments from balanced Hi-C matrices with cooltools eigendecomposition, phased against GC or gene density so the A sign is not arbitrary"
verification: works
verified_on: 2026-08-10
reviewed_on: 2026-08-10
security: cleared
security_on: 2026-08-10
security_note: "GPTomics/bioSkills MIT root confirmed, provenance matches, cooltools open source"
---

# A/B Compartment Analysis (bioSkills)

A Claude Code skill for the megabase-scale layer of genome organization: eigenvector decomposition of a Hi-C matrix into active (A) and inactive (B) compartments, with the sign-orientation step that most ad-hoc scripts get wrong.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — cooltools is installed separately (open source) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python), not as an MCP tool |
| **Verified** | works · 2026-08-10 |
| **Security** | cleared · 2026-08-10 — MIT, provenance matches, cooltools open source |

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
  cp -r bioSkills/hi-c-analysis/compartment-analysis ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites — the Python Hi-C stack** (the skill drives these; they are not bundled):
  ```
  pip install "cooler>=0.10" "cooltools>=0.7" "bioframe>=0.7"
  ```
  Python 3.6+ per the skill; check with `pip show cooltools`. A genome FASTA is also needed for the GC phasing track.

## What it does

Runs the standard compartment pipeline with the corrections that make the output interpretable:

- **Data preparation** — loads a balanced cooler at **100 kb–1 Mb** resolution (250 kb is the typical choice), fetches centromeres and builds a per-chromosome-arm `view_df` via `bioframe.make_chromarms()` so the centromere gradient does not dominate the first eigenvector.
- **Phasing track** — computes GC content at the cooler's exact binning with `bioframe.frac_gc()` (gene density is the alternative).
- **Eigendecomposition** — `cooltools.eigs_cis()` per chromosome arm on the distance-normalized, Pearson-correlated cis matrix, with `sort_metric='pearsonr'` rather than eigenvalue ordering.
- **Orientation** — signs the eigenvector against the phasing track so that positive = A = active, instead of leaving the sign to the arbitrary output of the decomposition.

**Primary use cases**: calling A/B compartments from a cooler, generating a phased compartment (E1) track, comparing compartmentalization between conditions.

## Notes

Three requirements the skill treats as non-negotiable. The cooler must be **pre-balanced** (stored `weight` column). Multi-resolution `.mcool` files need a resolution-specific URI (`file.mcool::/resolutions/100000`), not the bare path. And chromosome naming must be consistent across the cooler, the FASTA used for GC, and the centromere annotation — a `chr1` vs `1` mismatch produces empty or misaligned output rather than an error.

The two substantive methodological choices are worth restating. **Per-arm rather than per-chromosome** decomposition exists because the centromere imposes a large-scale gradient that the first eigenvector will otherwise capture instead of compartmentalization. And **`sort_metric='pearsonr'`** is preferred over eigenvalue ordering because the largest-eigenvalue component is not reliably the compartment component; correlation with the phasing track is the better selection criterion. Without the phasing step, the sign of A and B is arbitrary and cross-condition or cross-chromosome comparisons are meaningless.

Compartments sit at a different scale from, and are orthogonal to, insulation-based domain boundaries — a compartment switch and a boundary change are separate claims. Upstream skill front-matter name is `bio-hi-c-analysis-compartment-analysis` (`tool_type: python`, `primary_tool: cooltools`); upstream directory `hi-c-analysis/compartment-analysis`. Pairs with [TAD Detection](tad-detection.html) (the sub-megabase insulation layer), [Chromatin Loop Calling](loop-calling.html), and [deepTools](deeptools.html) for correlating a compartment track against chromatin marks.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`hi-c-analysis/compartment-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/hi-c-analysis/compartment-analysis/SKILL.md)
- [cooltools documentation](https://cooltools.readthedocs.io/)
- [bioframe documentation](https://bioframe.readthedocs.io/)
- [cooler documentation](https://cooler.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=compartment-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcompartment-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
