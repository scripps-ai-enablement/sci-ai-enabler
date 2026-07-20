---
title: MiXCR Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-18
summary: "Align V(D)J reads and assemble TCR/BCR clonotypes with MiXCR, driven by a chemistry-matched preset, exporting native or AIRR TSV for downstream repertoire analysis"
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "skill provenance matches GPTomics/bioSkills MIT and the tcr-bcr-analysis/mixcr-analysis directory is confirmed this run, but the required MiXCR binary is separately licensed (free academic/non-commercial only) so review MiLaboratories terms before commercial use"
---

# MiXCR Analysis (bioSkills)

A Claude Code skill that aligns raw immune-repertoire sequencing reads and assembles TCR/BCR clonotypes with MiXCR, choosing and auditing the correct chemistry-matched preset.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — MiXCR itself requires a separate license (free for academic/non-commercial use) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — skill provenance matches GPTomics/bioSkills, MIT, directory confirmed this run, but the required MiXCR binary is separately licensed (free academic/non-commercial only) |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "tcr-bcr-analysis"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/tcr-bcr-analysis/mixcr-analysis ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). The skill declares MiXCR (v4.7+) as its external dependency in `SKILL.md`; install and license it when prompted on first use.

## What it does

Runs the **MiXCR 4.7+** analysis pipeline for TCR/BCR repertoire profiling, aligning reads to V(D)J germline segments, collapsing molecules/cells by barcode, and assembling clonotypes keyed on CDR3 plus V and J genes:

- **Preset selection** matched to wet-lab chemistry — 5'RACE/template-switch vs multiplex-primer amplicon (rigid vs floating boundaries), RNA vs gDNA (`--rna`/`--dna`), bulk vs 10x single-cell, UMI vs no-UMI, and kit presets (Takara, NEBNext, QIAseq, BD, MiLaboratory).
- **Pipeline stages** — `align` → `refineTagsAndSort` → `assemblePartial` → `extend` → `assemble` → `assembleCells` → `export`.
- **Quantitation choices** — reads vs UMI vs cell denominator.
- **Export** — native MiXCR fields or AIRR rearrangement TSV (`exportAirr`) for downstream Immcantation/scirpy/VDJtools, plus alignment/chain-usage QC (`exportQc`).

**Primary use cases**: bulk and single-cell TCR/BCR clonotype assembly, preset auditing for a library chemistry, AIRR export for downstream repertoire analysis.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally via Bash/Python rather than as an MCP server. The upstream skill front-matter name is `bio-tcr-bcr-analysis-mixcr-analysis`; if you invoke it as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/mixcr-analysis`. **MiXCR requires its own license** — free for academic/non-commercial use, obtained from MiLaboratories; the skill's MIT license covers only the workflow instructions, not MiXCR itself. Downstream analysis of the AIRR export is handled by `immcantation-analysis` (bulk) or `scirpy-analysis` (single-cell). Upstream directory: `tcr-bcr-analysis/mixcr-analysis`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`tcr-bcr-analysis/mixcr-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/mixcr-analysis/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=mixcr-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmixcr-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
