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

- K-Dense skill batch 3 (bootstrap) — works / cleared · 2026-07-20 — 8 more unstamped skills stamped against re-confirmed anchor `K-Dense-AI/scientific-agent-skills` (MIT, not archived, pushed 2026-07-15; each dir confirmed present in this-run `skills/` tree listing; `npx skills add` CLI shown working in this-run smoke batch): `shap`, `umap-learn`, `zarr-python`, `transformers`, `simpy`, `scvelo`, `torch-geometric`, `vaex`.
- `uniprot` (Augmented-Nature UniProt MCP Server) — works / caution · 2026-07-20 — repo resolves (redirects to `Augmented-Nature-UniProt-MCP-Server`), public UniProt REST API no-auth; committed LICENSE is restrictive non-commercial while package.json + page claim MIT, last push 2025-12-21 (~7mo stale).
- K-Dense skill batch 2 (bootstrap) — works / cleared · 2026-07-20 — 16 skills stamped against re-confirmed anchor `K-Dense-AI/scientific-agent-skills`: `matplotlib`, `networkx`, `statsmodels`, `sympy`, `polars`, `seaborn`, `scikit-learn`, `pysam`, `qiskit`, `pennylane`, `qutip`, `pymc`, `pymatgen`, `geopandas`, `neurokit2`, `pyopenms`.
- K-Dense skill batch (bootstrap) — works / cleared · 2026-07-20 — 19 skills stamped against confirmed anchor `K-Dense-AI/scientific-agent-skills`: `astropy`, `cobrapy`, `deeptools`, `deepchem`, `aeon`, `arboreto`, `cirq`, `bioservices`, `bgpt-paper-search`, `bids`, `bulk-rnaseq`, `cellxgene-census`, `dask`, `database-lookup`, `benchling-integration`, `citation-management`, `clinical-decision-support`, `clinical-reports`, `consciousness-council`.
- `adaptyv` — works / caution · 2026-07-20 — K-Dense skill dir resolves; writes to a paid external Adaptyv wet-lab platform and handles ADAPTYV_API_KEY (in-silico half runs unauthenticated).
- `autoskill` — works / caution · 2026-07-20 — K-Dense skill dir resolves; observes user screen via a local screenpipe daemon (detection local, only redacted summaries reach LLM).
- `bci-mcp` — works / caution · 2026-07-20 — smoke pass; PyPI+npm+GitHub v0.1.3 MIT, single-maintainer alpha.

## Flagged (broken or security)

- `uniprot` (Augmented-Nature) — security `caution` · 2026-07-20 — LICENSE file on the repo is restrictive non-commercial ("personal, non-commercial use only", no redistribution/modification) while `package.json` and the catalog page both claim MIT. Curator should reconcile the `Pricing` line; recheck if upstream relicenses.
- Prior: `pymol`, `foldseek-structural-search` degraded but fixed in-page; scmcphub ecosystem on `caution` for staleness — recheck maintenance next cycle.

## Deferred — next-run priority

- Remaining unstamped K-Dense skills confirmed present in this-run `skills/` tree listing — next bootstrap batches (same works/cleared pattern, anchor already re-confirmed 2026-07-15): `pymoo`, `pydeseq2`, `pydicom`, `pyzotero`, `phylogenetics`, `etetoolkit`, `histolab`, `pathml`, `geniml`, `gtars`, `matchms`, `molfeat`, `pytorch-lightning`, `pytdc`, `pyhealth`, `pylabrobot`, `lamindb`, `medchem`, `rowan`, `scvi-tools`, `stable-baselines3`, `torchdrug`, `tiledbvcf`, `timesfm-forecasting`, `xlsx`, plus the `scientific-*` writing/thinking skills.
- Note (correction): dirs `scipy`, `seurat`, `squidpy`, `spatialdata`, `sqlalchemy`, `survival-analysis`, `structural-biology`, `systems-biology`, `tensorflow`, `torch` are NOT present in the K-Dense `skills/` tree as of 2026-07-15 — do not stamp any such catalog entry against this anchor; resolve each against its own supplier instead.
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
