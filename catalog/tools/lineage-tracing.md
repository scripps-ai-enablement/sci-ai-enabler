---
title: Lineage Tracing (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-01
summary: "Reconstruct single-cell lineage trees from CRISPR scars, expressed barcodes or mtDNA mutations using Cassiopeia, Startle and CoSpar"
---

# Lineage Tracing (bioSkills)

A Claude Code skill that builds clonal phylogenies from single-cell lineage recorders — CRISPR/Cas9 scars, static expressed barcodes, or somatic mitochondrial mutations — and joins them to transcriptomic state.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — Cassiopeia, CoSpar, Startle and scanpy are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python), not as an MCP tool |

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
  cp -r bioSkills/single-cell/lineage-tracing ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the Python stack on first use:
  ```
  pip install "cospar>=0.3" "scanpy>=1.10" "numpy>=1.26"
  pip install git+https://github.com/YosefLab/Cassiopeia@master
  ```
  Cassiopeia must come from GitHub, not PyPI: the skill targets Cassiopeia 2.0+, but the PyPI distribution `cassiopeia-lineage` is still at 1.0.4 (checked 2026-08-01), so `pip install cassiopeia-lineage` gets you the older API.

## What it does

Five stages from recorder reads to a fate-annotated tree:

1. **Assay selection** — CRISPR/Cas9 scars, static expressed barcodes (LARRY, CellTag), combinatorial tags, or somatic mtDNA mutations, each with different resolution and dropout behaviour.
2. **Character matrix construction** — resolve UMIs, align reads, call alleles, and convert to phylogenetic characters.
3. **Solver selection and tree reconstruction** — Cassiopeia 2.0+ parsimony and distance solvers (VanillaGreedy, ILP, Hybrid, NeighborJoining) plus Startle for scar data with homoplasy.
4. **Robustness assessment** — compare topologies across solvers with Robinson–Foulds distance and triplets-correct scores, rather than trusting a single reconstruction.
5. **Clone–state integration** — CoSpar 0.3+ to map fate bias from paired clonal and transcriptomic data.

**Quality thresholds the skill applies** — drop cells below ~10 UMIs per cell (noise dominates allele calls); drop cells missing more than ~50% of characters (insufficient phylogenetic signal); count a character as informative only if its states appear in more than one cell; and require barcode library complexity far exceeding the founder population so collisions do not fabricate clones.

**Primary use cases**: developmental and tumor-progression phylogenies, clonal fate-bias analysis, mtDNA-based clone grouping in human samples.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-single-cell-lineage-tracing` (`tool_type: python`, `primary_tool: Cassiopeia`); if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/lineage-tracing`. Homoplasy — the same scar arising independently in unrelated cells — and allele dropout are the two failure modes the skill spends most of its guidance on, since both produce confidently wrong topologies. Distinct from expression-based pseudotime: [scVelo](scvelo.html) and [CellRank](cellrank-mcp.html) infer trajectories from RNA dynamics, whereas this skill uses a physical heritable recorder, and it treats a state-based fate call as something to be validated against clonal evidence rather than assumed. Upstream directory: `single-cell/lineage-tracing`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`single-cell/lineage-tracing/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/single-cell/lineage-tracing/SKILL.md)
- [`YosefLab/Cassiopeia`](https://github.com/YosefLab/Cassiopeia) · [`cassiopeia-lineage` on PyPI](https://pypi.org/project/cassiopeia-lineage/) · [`cospar` on PyPI](https://pypi.org/project/cospar/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=lineage-tracing&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Flineage-tracing.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
