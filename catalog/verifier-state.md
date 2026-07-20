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

- K-Dense skill batch 6 (bootstrap) — mostly works / cleared · 2026-07-20 — 12 more unstamped skills stamped against re-confirmed anchor `K-Dense-AI/scientific-agent-skills` (MIT, not archived, pushed 2026-07-15) with `skills/` contents-API confirming each subdir: `esm`, `diffdock` (also resolves upstream `gcorso/DiffDock` MIT), `geomaster`, `glycoengineering`, `hypogenic`, `hypothesis-generation`, `literature-review`, `peer-review`, `markitdown` (works/cleared); `pdf`, `docx`, `pptx` (works/**caution** — each `skills/<slug>/LICENSE.txt` is Anthropic PBC proprietary while the page claims Free/OSS, same xlsx pattern). Also refreshed `flowio`/`nextflow-development` notes: this cycle's smoke batch shows `npx skills add` passing (git ENOENT resolved).
- K-Dense skill batch 5 (bootstrap) — mostly works / cleared · 2026-07-20 — 12 more unstamped skills stamped against re-confirmed anchor `K-Dense-AI/scientific-agent-skills` (MIT, not archived, pushed 2026-07-15); each skill dir confirmed to resolve individually via contents API: `stable-baselines3`, `torchdrug`, `tiledbvcf`, `timesfm-forecasting` (cleared); `scientific-writing`, `scientific-brainstorming`, `scientific-critical-thinking`, `scientific-slides`, `scientific-visualization` (cleared, prompt-based); `xlsx` (caution — LICENSE.txt is Anthropic proprietary, not the page's Free/OSS); `scientific-schematics` (caution — ships user API key to external Google Gemini image services).
- `scientific-problem-selection` — works / caution · 2026-07-20 — Anthropic-supplied skill; `anthropics/life-sciences` resolves (not archived, pushed 2026-05-08) and plugin `scientific-problem-selection@life-sciences` documented; caution only because repo carries no top-level LICENSE.
- K-Dense skill batch 4 (bootstrap) — works / cleared · 2026-07-20 — 15 more unstamped skills stamped against re-confirmed anchor `K-Dense-AI/scientific-agent-skills` (MIT, not archived, pushed 2026-07-15): `pymoo`, `pydeseq2`, `pydicom`, `pyzotero`, `etetoolkit`, `histolab`, `pathml`, `geniml`, `matchms`, `molfeat`, `pytorch-lightning`, `pytdc`, `pylabrobot`, `lamindb`, `medchem`.
- `scvi-tools` — works / cleared · 2026-07-20 — Anthropic-supplied skill; `anthropics/life-sciences` repo resolves (not archived, pushed 2026-05-08) plus K-Dense alt `skills/scvi-tools` dir resolves; wraps BSD-3 scvi-tools, no OSV advisories.
- `rowan` — works / caution · 2026-07-20 — dual Skill+MCP; K-Dense `skills/rowan` dir resolves and `rowan-mcp` on PyPI (v2.3.2 MIT); caution because `k-yenko/rowan-mcp` repo has no LICENSE and the tool ships a user API key to an external cloud service.
- `phylogenetics`, `gtars`, `pyhealth` — works / caution · 2026-07-20 — K-Dense dirs resolve but each skill's own upstream library license is unstated.

## Flagged (broken or security)

- `pdf`, `docx`, `pptx` (K-Dense) — security `caution` · 2026-07-20 — each `skills/<slug>/LICENSE.txt` is Anthropic PBC proprietary ("© 2025 Anthropic, PBC. All rights reserved", no redistribution/derivatives) redistributed in the MIT K-Dense collection while the page claims Free/OSS ("Proprietary..txt has complete terms"). Same pattern as `xlsx`; curator should correct each `Pricing` line.

- `xlsx` (K-Dense) — security `caution` · 2026-07-20 — `skills/xlsx/LICENSE.txt` is Anthropic PBC proprietary ("all rights reserved", no redistribution/derivatives) yet the MIT K-Dense collection redistributes it and the page claims Free/OSS. Curator should correct the `Pricing` line.
- `scientific-schematics` (K-Dense) — security `caution` · 2026-07-20 — provenance/MIT clear, but the skill sends prompts plus a user API key to external Google Gemini ("Nano Banana 2" / Gemini 3.1 Pro) image services; note the external-service/credential dependency.
- `scientific-problem-selection` (Anthropic) — security `caution` · 2026-07-20 — plugin resolves in `anthropics/life-sciences` but repo has no top-level LICENSE; lift to cleared if a LICENSE lands.
- `uniprot` (Augmented-Nature) — security `caution` · 2026-07-20 — LICENSE file on the repo is restrictive non-commercial ("personal, non-commercial use only", no redistribution/modification) while `package.json` and the catalog page both claim MIT. Curator should reconcile the `Pricing` line; recheck if upstream relicenses.
- `rowan` — security `caution` · 2026-07-20 — `k-yenko/rowan-mcp` repo publishes no LICENSE (page already notes this) and the tool ships a user `ROWAN_API_KEY` to the external paid Rowan cloud; recheck if the MCP repo adds a LICENSE.
- `phylogenetics`, `gtars`, `pyhealth` — security `caution` · 2026-07-20 — K-Dense provenance clears but each skill's own upstream library license is unstated on the page; lift to cleared if a license is confirmed.
- Prior: `pymol`, `foldseek-structural-search` degraded but fixed in-page; scmcphub ecosystem on `caution` for staleness — recheck maintenance next cycle.

## Deferred — next-run priority

- All slugs from the prior deferred K-Dense list are now stamped (`rdkit-skill`, `scikit-bio`, `scikit-learn`, `seaborn`, `datamol`, `deepchem`, `deeptools`, `dask`, `esm`, `diffdock`, `geomaster`, `glycoengineering`, `hypogenic`, `hypothesis-generation`, `literature-review`, `peer-review`, `pdf`, `pptx`, `docx`, `markitdown`). Next bootstrap batches: pick remaining unstamped catalog entries with `supplier: K-Dense`; the anchor `skills/` contents API (fetched 2026-07-20) confirms these dirs exist for cross-checking — `arbor`, `arboreto`, `astropy`, `benchling-integration`, `bgpt-paper-search`, `bids`, `biopython`, `bioservices`, `bulk-rnaseq`, `citation-management`, `clinical-decision-support`, `clinical-reports`, `consciousness-council`, `database-lookup`, `depmap`, `dnanexus-integration`, `exa-search`, `fluidsim`, `generate-image`, `get-available-resources`, `ginkgo-cloud-lab`, `hugging-science`, `imaging-data-commons`, `infographics`, `matlab`, `molecular-dynamics`, `omero-integration`, `opentrons-integration`, `primekg`, `protocolsio-integration`, `pufferlib` — verify each catalog page is actually unstamped and each dir resolves individually before stamping. Watch for the Anthropic-proprietary LICENSE.txt pattern on any Anthropic-authored doc/util skills (like pdf/docx/pptx/xlsx).
- Note (correction): dirs `scipy`, `seurat`, `squidpy`, `spatialdata`, `sqlalchemy`, `survival-analysis`, `structural-biology`, `systems-biology`, `tensorflow`, `torch` are NOT present in the K-Dense `skills/` tree as of 2026-07-15 — do not stamp any such catalog entry against this anchor; resolve each against its own supplier instead.
- Curator handoff: `xlsx`, `pdf`, `docx`, `pptx` page `Pricing` lines falsely claim Free/OSS (each skill's upstream LICENSE.txt is Anthropic PBC proprietary) — verifier stamped security `caution`; curator owns the Pricing corrections.
- scmcphub ecosystem (`scanpy`, `cellrank-mcp`, `decoupler-mcp`, `liana-mcp`) — recheck for a maintenance bump or archival; currently ~13 months stale.
- `gromacs-mcp` — recheck upstream for a published LICENSE file; graded caution until then.
- `blast` (bio-mcp org) — recheck for a published LICENSE and a maintenance bump; caution until then.
- SciAgent-Skills entries (`bcftools-variant-manipulation`, `autodock-vina-docking`, …) — GitHub reports license NOASSERTION; recheck whether a recognized LICENSE lands to lift from caution.
- `chemcp` — recheck for a LICENSE file committed to the repo to reconcile the ISC npm metadata.

## Smoke-test queue

The `scripts/select_smoke_targets.py` selector is authoritative for what the quarantined smoke job
may install/boot (open, no-auth, no-cost Skills/MCP servers only). List slugs here to prioritize the
next run's smoke batch; leave empty to let the selector pick by age.

Note: the prior `spawn git ENOENT` sandbox failure is resolved — this run's smoke batch (8/8 pass)
shows `npx skills add K-Dense-AI/scientific-agent-skills` and `npx skills add
google-deepmind/science-skills/` both installing cleanly, so clone/CLI-based Skills can be re-queued.
Next smoke priorities:

- `scanpy` (`pip install scanpy-mcp`)
- `decoupler-mcp` (`pip install decoupler-mcp`)
- `liana-mcp` (`pip install liana-mcp`)
- `cellrank-mcp` (`pip install cellrank-mcp`)
- K-Dense CLI batch (`npx skills add K-Dense-AI/scientific-agent-skills`) — now confirmed installable in-sandbox; queue a few aging K-Dense slugs to capture real boot verdicts.
