---
title: AnnData (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology, Neuroscience]
last_verified: 2026-05-21
summary: Claude skill teaching the AnnData annotated-data-matrix format used by Scanpy and scvi-tools for single-cell and other observation/feature matrices.
---

# AnnData (Claude Skill)

Claude skill that documents the AnnData object model — `X`, `obs`, `var`, `layers`, `obsm`, `varm`, `obsp`, `varp`, `uns`, and `raw` — and the read/write/subset/concatenate operations used in single-cell pipelines.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write — Claude executes AnnData via Python/Bash |

## How to install

- **Claude Code** — plugin marketplace:
  ```
  /plugin marketplace add K-Dense-AI/claude-scientific-skills
  /plugin install anndata@claude-scientific-skills
  ```
- **Claude Code / Claude Desktop** — manual clone of the source repo:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/scientific-skills/anndata ~/.claude/skills/
  pip install anndata
  ```

## What it does

`SKILL.md` with recipes for:

- AnnData object structure (`X`, `obs`, `var`, `layers`, `obsm`/`varm`, `obsp`/`varp`, `uns`, `raw`)
- Reading and writing `.h5ad`, `.zarr`, and 10x formats, including compression and backed mode
- Combining objects along observations or variables with flexible join strategies
- Subsetting, filtering, layer manipulation, and reorganization for downstream Scanpy / scvi-tools workflows

**Primary use cases**: Standardising single-cell input formats, joining multiple datasets, debugging Scanpy / scvi-tools pipelines that consume AnnData.

## Notes

AnnData itself is a Python library, not a Claude-installable component. This entry catalogs the K-Dense skill wrapper; the underlying library must still be `pip install`ed in the environment Claude executes in.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/anndata/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/anndata/SKILL.md)
- [AnnData documentation](https://anndata.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=anndata&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fanndata.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
