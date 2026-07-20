---
title: Verifier state
parent: Catalog
nav_exclude: true
---

# Verifier state

Working memory for the [Verifier agent](https://github.com/scripps-ai-enablement/sci-ai-enabler/blob/main/VERIFIER_AGENT.md).
It owns the `verification` / `security` stamps on catalog entries; the catalog curator
(`catalog/curator-state.md`) owns everything else.

## Recently verified

- `bci-mcp` — works / caution · 2026-07-20 — smoke pass; PyPI+npm+GitHub v0.1.3 MIT, single-maintainer alpha.
- `instrument-data-to-allotrope` — works / cleared · 2026-07-20 — smoke pass; life-sciences plugin path resolves, allotropy Benchling MIT.
- `flowio` / `rdkit-skill` / `scikit-bio` / `gget` / `biopython` / `anndata` — works / cleared · 2026-07-20 — K-Dense-AI repo MIT, skill dirs resolve, maintained; smoke clone failed only on sandbox missing git.
- `nextflow-development` — works / cleared · 2026-07-20 — anthropics/life-sciences dir resolves; K-Dense alt smoke clone failed on sandbox git.
- `pymol` / `foldseek-structural-search` — degraded / cleared · 2026-07-20 — fixed: removed stale scienceskillscommon copy line (404 in repo, not imported).
- `biomcp` — works / cleared · 2026-07-20 — biomcp-cli v0.8.25 + biomcp-python v0.7.3 MIT, GenomOncology.
- `scanpy` / `cellrank-mcp` / `decoupler-mcp` / `liana-mcp` — works / caution · 2026-07-20 — scmcphub PyPI v0.4.0/v0.5.0 present, no OSV, but repos unmaintained since 2025-06 (no LICENSE on several).

## Flagged (broken or security)

_None this run._ (`pymol`, `foldseek-structural-search` degraded but fixed in-page; scmcphub ecosystem on `caution` for staleness — recheck maintenance next cycle.)

## Deferred — next-run priority

- scmcphub ecosystem (`scanpy`, `cellrank-mcp`, `decoupler-mcp`, `liana-mcp`) — recheck for a maintenance bump or archival; currently ~13 months stale.
- `gromacs-mcp` — recheck upstream for a published LICENSE file; graded caution until then.

## Smoke-test queue

The `scripts/select_smoke_targets.py` selector is authoritative for what the quarantined smoke job
may install/boot (open, no-auth, no-cost Skills/MCP servers only). List slugs here to prioritize the
next run's smoke batch; leave empty to let the selector pick by age.

Note: this run's K-Dense / google-deepmind skill smoke jobs failed with `spawn git ENOENT` (sandbox
lacks `git`) — an environmental failure, not a tool fault. Fix the smoke image to include `git`
before re-queuing clone-based skills. PyPI-installable servers below don't need git:

- `scanpy` (`pip install scanpy-mcp`)
- `decoupler-mcp` (`pip install decoupler-mcp`)
- `liana-mcp` (`pip install liana-mcp`)
- `cellrank-mcp` (`pip install cellrank-mcp`)
