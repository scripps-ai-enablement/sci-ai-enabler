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

- K-Dense skill batch (bootstrap) — works / cleared · 2026-07-20 — 19 skills stamped against confirmed anchor `K-Dense-AI/scientific-agent-skills` (MIT, not archived, pushed 2026-07-15, LICENSE.md + SECURITY.md present, skills/ tree lists each dir): `astropy`, `cobrapy`, `deeptools`, `deepchem`, `aeon`, `arboreto`, `cirq`, `bioservices`, `bgpt-paper-search`, `bids`, `bulk-rnaseq`, `cellxgene-census`, `dask`, `database-lookup`, `benchling-integration`, `citation-management`, `clinical-decision-support`, `clinical-reports`, `consciousness-council`.
- `adaptyv` — works / caution · 2026-07-20 — K-Dense skill dir resolves; writes to a paid external Adaptyv wet-lab platform and handles ADAPTYV_API_KEY (in-silico half runs unauthenticated).
- `autoskill` — works / caution · 2026-07-20 — K-Dense skill dir resolves; observes user screen via a local screenpipe daemon (detection local, only redacted summaries reach LLM).
- `arxiv` — works / cleared · 2026-07-20 — blazickjp GitHub Apache-2.0 + PyPI arxiv-mcp-server v0.5.0, no OSV.
- `chembl` — works / cleared · 2026-07-20 — anthropics/life-sciences marketplace repo resolves and active, ChEMBL data EMBL-EBI.
- `clinicaltrials-gov-mcp` — works / cleared · 2026-07-20 — cyanheads Apache-2.0, npm clinicaltrialsgov-mcp-server v2.8.2, no OSV.
- `datamol` — works / cleared · 2026-07-20 — K-Dense-AI repo MIT + Datamol PyPI v0.12.5 Apache-2.0, no OSV.
- `bci-mcp` — works / caution · 2026-07-20 — smoke pass; PyPI+npm+GitHub v0.1.3 MIT, single-maintainer alpha.

## Flagged (broken or security)

_None this run._ (`pymol`, `foldseek-structural-search` degraded but fixed in-page; scmcphub ecosystem on `caution` for staleness — recheck maintenance next cycle.)

## Deferred — next-run priority

- scmcphub ecosystem (`scanpy`, `cellrank-mcp`, `decoupler-mcp`, `liana-mcp`) — recheck for a maintenance bump or archival; currently ~13 months stale.
- `gromacs-mcp` — recheck upstream for a published LICENSE file; graded caution until then.
- `blast` (bio-mcp org) — recheck for a published LICENSE and a maintenance bump; caution until then.
- SciAgent-Skills entries (`bcftools-variant-manipulation`, `autodock-vina-docking`, …) — GitHub reports license NOASSERTION; recheck whether a recognized LICENSE lands to lift from caution.
- `chemcp` — recheck for a LICENSE file committed to the repo to reconcile the ISC npm metadata.

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
