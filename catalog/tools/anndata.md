---
title: AnnData (Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology, Neuroscience]
last_verified: 2026-06-04
verification: works
verified_on: 2026-07-29
verification_note: "repo and skills/anndata dir resolve on K-Dense-AI/scientific-agent-skills; PyPI anndata 0.13.2 pip-installs cleanly in the smoke sandbox"
security: cleared
security_on: 2026-07-29
security_note: "provenance matches supplier K-Dense-AI, MIT repo wrapping BSD-3-Clause anndata 0.13.2, maintained (pushed 2026-07-29), no OSV advisories"
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
| **Verified** | works · 2026-07-29 — smoke-tested: `pip install anndata` passes |
| **Security** | cleared · 2026-07-29 — provenance matches K-Dense-AI, MIT repo, maintained, no OSV advisories |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/genomics-bioinformatics/single-cell/anndata-data-structure` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add K-Dense-AI/scientific-agent-skills
  ```
  Installs the K-Dense collection; enable the `anndata` skill when prompted (also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone of the source repo:
  ```
  git clone https://github.com/K-Dense-AI/scientific-agent-skills
  cp -r scientific-agent-skills/skills/anndata ~/.claude/skills/
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
- [`skills/anndata/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/anndata/SKILL.md)
- [AnnData documentation](https://anndata.readthedocs.io/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=anndata&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fanndata.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
