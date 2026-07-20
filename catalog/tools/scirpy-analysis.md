---
title: scirpy Analysis (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Immunology and Microbiology]
last_verified: 2026-07-18
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches GPTomics/bioSkills, MIT, no OSV/GitHub advisories, read-only local scirpy/scanpy workflow with no credential requests"
summary: "Integrate single-cell paired TCR/BCR repertoires with gene expression using scirpy — chain-pairing QC, clonotype definition, clonal expansion, diversity, and VDJdb specificity"
---

# scirpy Analysis (bioSkills)

A Claude Code skill that analyzes single-cell paired TCR/BCR repertoires alongside gene expression in an AnnData/MuData object using scirpy.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python), not as an MCP tool |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches GPTomics/bioSkills, MIT, no advisories, read-only local scirpy workflow |

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
  cp -r bioSkills/tcr-bcr-analysis/scirpy-analysis ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). The skill declares its Python dependencies (scirpy, scanpy, mudata) in `SKILL.md`; install them when prompted on first use.

## What it does

Runs a full single-cell immune-repertoire pipeline with **scirpy** (v0.24+) integrated with **scanpy**/**mudata**:

- **Data ingestion** — loads 10x VDJ, AIRR TSV, dandelion, or BD Rhapsody formats and pairs receptor data with gene expression.
- **Quality control** — chain-pairing categorization and doublet detection via `chain_qc` (multichain doublets, orphan dropout, extra-VJ dual-TCR).
- **Clonotype definition** — receptor-specific strategies: exact CDR3-nt identity for TCR (`define_clonotypes`) versus nucleotide-distance clustering for BCR (`define_clonotype_clusters` with normalized Hamming + same V/J gene, because somatic hypermutation shatters identity clonotypes).
- **Clonal analysis** — expansion binning, alpha diversity, repertoire overlap across groups, and clonotype modularity.
- **Integration** — overlaying clonality onto the transcriptomic UMAP.

The skill works on the awkward-array AIRR model (`adata.obsm['airr']`, accessed via `get.airr` after `pp.index_chains`), not legacy per-chain obs columns, and covers tuning `receptor_arms`, `dual_ir`, and `within_group`.

**Primary use cases**: single-cell TCR/BCR clonotype analysis, clonal-expansion mapping onto transcriptomes, repertoire diversity and specificity annotation.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally via Bash/Python rather than as an MCP server. The upstream skill front-matter name is `bio-tcr-bcr-analysis-scirpy-analysis`; if you invoke it as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/scirpy-analysis`. Complements bulk-repertoire skills (`mixcr-analysis`, `immcantation-analysis`) and VDJdb specificity lookup. Upstream directory: `tcr-bcr-analysis/scirpy-analysis`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`tcr-bcr-analysis/scirpy-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/scirpy-analysis/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=scirpy-analysis&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fscirpy-analysis.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
