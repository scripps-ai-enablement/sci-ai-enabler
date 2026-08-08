---
title: Chromatin Loop Calling (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-08
summary: "Call focal chromatin loops from Hi-C or Micro-C maps with cooltools dots, chromosight and Mustache, and validate them with aggregate peak analysis"
---

# Chromatin Loop Calling (bioSkills)

A Claude Code skill for finding corner-dot chromatin loops in a contact map — and, first, for deciding whether the map is deep enough to look for them at all.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — cooltools, chromosight and Mustache are installed separately (all open source) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python/CLI), not as an MCP tool |

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
  cp -r bioSkills/hi-c-analysis/loop-calling ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone, e.g. `/Users/you/repos/bioSkills`).
- **Prerequisites — the core Python stack** (required for `dots` and APA):
  ```
  pip install "cooler>=0.10" "cooltools>=0.7" "bioframe>=0.7"
  ```
- **Optional — chromosight 1.6+** (template-correlation calling, and the `quantify` step used for differential loops):
  ```
  pip install "chromosight>=1.6"
  ```
  Confirm with `chromosight --version`.
- **Optional — Mustache 1.3+** (scale-space multi-resolution detection). **Unverified —** the skill names Mustache 1.3+ but does not give an install command, and the PyPI distribution name was not confirmed this run; install from the upstream project ([`ay-lab/mustache`](https://github.com/ay-lab/mustache)) and check `mustache --help` before use. The cooltools and chromosight paths cover the workflow without it.

## What it does

Treats loop calling as a decision about data depth first and an algorithm choice second:

- **Depth assessment** — the critical fork. De-novo calling needs roughly **5–10 kb** resolution, which in practice means hundreds of millions to billions of valid pairs. Shallower maps are routed to APA on known anchors instead of de-novo calling.
- **De-novo calling** — `cooltools.dots()`, a HiCCUPS-style local-enrichment test using four background donut/neighbourhood models with lambda-chunked FDR.
- **Alternative callers** — chromosight (template correlation; also finds borders and stripes) and Mustache (scale-space blob detection).
- **Aggregate peak analysis** — `cooltools.pileup()` builds an APA pileup to confirm a loop set, or to test known CTCF/cohesin anchors in a map too shallow to call de novo.
- **Validation** — consensus across callers plus convergent-CTCF support, rather than trusting one caller's list.
- **Differential loops** — union anchor set across conditions, then `chromosight quantify` to score the same coordinates in every map.

**Primary use cases**: calling loops or dots from a cooler, deciding de-novo vs APA-on-known-anchors, comparing loops between conditions.

## Notes

The scoping rule to read before installing: for **protein-anchored** assays — HiChIP, PLAC-seq, PCHi-C — this skill explicitly routes you elsewhere (FitHiChIP or MAPS), because `dots` assumes an all-by-all Hi-C background model that those protocols violate. bioSkills ships a separate `hichip-plac-loops` skill for that case.

As with the other Hi-C skills, the input cooler must be **balanced**, and `.mcool` files must be addressed with a resolution-specific URI (`file.mcool::/resolutions/5000`) rather than the bare path. Expected-value computation and chromosome-arm regions come from cooltools and bioframe respectively, so arm definitions need chromosome names consistent with the cooler.

Differential loop analysis is deliberately structured as *quantify the union anchors in both maps*, not *intersect two independently-called lists* — independent calling near a detection threshold manufactures condition-specific loops that are really just borderline calls.

Upstream skill front-matter name is `bio-hi-c-analysis-loop-calling` (`tool_type: mixed`, `primary_tool: cooltools`); upstream directory `hi-c-analysis/loop-calling`. Pairs with [TAD Detection](tad-detection.html) (domain boundaries rather than focal dots), [A/B Compartment Analysis](compartment-analysis.html), [MACS3](macs3-peak-calling.html) and [HOMER](homer-motif-analysis.html) for the CTCF/cohesin ChIP-seq anchors used in APA, and [bedtools](bedtools-genomic-intervals.html) for anchor arithmetic.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`hi-c-analysis/loop-calling/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/hi-c-analysis/loop-calling/SKILL.md)
- [cooltools documentation](https://cooltools.readthedocs.io/)
- [chromosight](https://github.com/koszullab/chromosight)
- [Mustache (`ay-lab/mustache`)](https://github.com/ay-lab/mustache)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=loop-calling&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Floop-calling.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
