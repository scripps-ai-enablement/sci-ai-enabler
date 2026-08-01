---
title: Perturb-seq Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Molecular and Cellular Biology]
last_verified: 2026-08-01
summary: "Analyze single-cell CRISPR screens with Pertpy, Mixscape escaper removal, SCEPTRE calibrated testing and E-distance effect sizes"
---

# Perturb-seq Analysis (bioSkills)

A Claude Code skill for single-cell CRISPR screens (Perturb-seq / CROP-seq) that covers guide assignment, escaper removal, and statistically calibrated differential testing.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — Pertpy, scanpy, SCEPTRE, Seurat, scMAGeCK, DESeq2 and edgeR are separately installed OSS |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Python/R), not as an MCP tool |

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
  cp -r bioSkills/single-cell/perturb-seq ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install the Python stack on first use: `pip install "pertpy>=0.9" "scanpy>=1.10" "anndata>=0.10"`; SCEPTRE 0.10+ and the Seurat/scMAGeCK paths are R installs.

## What it does

Walks a CRISPR screen from raw guide counts to defensible effect sizes:

- **Guide assignment** — treats guide calling as a mixture problem and uses the mixture-model posterior by default; flat thresholds are reserved for sanity checks.
- **Escaper removal** — computes a Mixscape perturbation signature and a two-component knockout / non-perturbed classification, so cells that received a guide but show no transcriptional effect do not dilute the comparison.
- **Calibrated testing** — SCEPTRE conditional resampling, or pseudobulk DE with DESeq2/edgeR, instead of naive per-cell differential expression. The replication unit is the **transfection, not the cell**, so pseudobulk-per-replicate with ≥2–3 replicates is required.
- **Effect quantification** — E-distance computed in a fixed PCA embedding, giving a comparable magnitude across perturbations.
- **Compositional analysis** — Milo / scCODA differential abundance, separating a shift in cell-state proportions from a change in expression within a state.
- **Foundation-model validation** — whole-perturbation holdout plus DE-gene metrics measured against an additive baseline, to test whether a perturbation-prediction model actually beats the trivial predictor.
- **Design guidance** — low-MOI designs (~1 guide/cell) discard 70–90% of cells; high-MOI enables combinatorial perturbation designs.

**Primary use cases**: CRISPR screen differential expression, perturbation effect ranking, benchmarking perturbation-prediction models.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-single-cell-perturb-seq` (`tool_type: python`, `primary_tool: Pertpy`); if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/perturb-seq`. The skill's most consequential rule is the replication unit: treating cells as independent replicates inflates significance in essentially every Perturb-seq dataset, which is why SCEPTRE or pseudobulk is the default rather than a scanpy `rank_genes_groups` call. Guide-library design and sgRNA selection sit upstream in [sgRNA Design Guide](sgrna-design-guide.html); [Scanpy](scanpy.html) and [AnnData](anndata.html) provide the underlying data structures. Upstream directory: `single-cell/perturb-seq`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`single-cell/perturb-seq/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/single-cell/perturb-seq/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=perturb-seq&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fperturb-seq.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
