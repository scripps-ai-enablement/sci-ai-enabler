---
title: Curator state
parent: Catalog
nav_exclude: true
---

# Curator state

## Recently surfaced

- **NPI Registry MCP (Anthropic Healthcare)** (added 2026-05-30) — Anthropic-published MCP server over the CMS NPPES NPI Registry API v2.1; validate, look up, and search US healthcare providers by NPI. Fourth Anthropic Healthcare MCP catalogued, completing the `cms-coverage` / `icd-10-codes` / `pubmed` set.
- **OpenNeuro MCP** (added 2026-05-29) — Community MCP server (QuentinCody) wrapping the OpenNeuro GraphQL API; hosted Cloudflare Workers SSE endpoint, MIT + Academic Citation Requirement license. Complements the Neurosift Tools MCP (DANDI + NWB) by covering OpenNeuro's MRI / MEG / EEG / iEEG / ECoG archive.
- **Cellxgene Census (Claude Skill)** (added 2026-05-28) — K-Dense skill for querying the CZ CELLxGENE Discover census (50M+ cells, 1,000+ datasets) via TileDB-SOMA, with AnnData / Scanpy integration for reference-atlas construction.
- **scVelo (Claude Skill)** (added 2026-05-28) — K-Dense skill driving scVelo for RNA-velocity analysis (steady-state / stochastic / dynamical models, latent time, driver-gene identification).
- **Arboreto (Claude Skill)** (added 2026-05-28) — K-Dense skill for gene-regulatory-network inference with GRNBoost2 / GENIE3, distributed via Dask; standard upstream step for pySCENIC.

## Flagged for review

- **allenbrain-mcp** — upstream license unset; flagged 2026-05-20 before any redistribution.
- **biorxiv@life-sciences** / **clinical-trials@life-sciences** plugins — flagged 2026-05-28; published in the `anthropics/life-sciences` marketplace per upstream commit `e96556b` but the backing `mcp.deepsense.ai` MCP host returns NXDOMAIN. No catalog entry created until the endpoint is restored.

## Deferred — next-run priority

- **Cortellis Plugin (`anthropics/life-sciences`)** — Clarivate Cortellis drug-pipeline / deals data; standalone marketplace entry beyond `adisinsight`.
- **Medidata Connector (`anthropics/life-sciences`)** — clinical-operations / EDC platform integration; announced Jan 2026 but install path still gated behind Medidata account onboarding.
- **Consensus Plugin (`anthropics/life-sciences`)** — Consensus.app evidence-search connector; verify install path.
- **biorxiv@life-sciences plugin** — `anthropics/life-sciences` marketplace entry currently DOA (`mcp.deepsense.ai` NXDOMAIN per upstream issue #42 / commit `e96556b`). Revisit when upstream restores the endpoint.
- **clinical-trials@life-sciences plugin** — same DOA status as biorxiv@life-sciences; distinct from both the `adisinsight` plugin (Springer Nature) and the `clinicaltrials-gov-mcp` community entry. Revisit when the endpoint is restored.
- **DeepChem (K-Dense Skill)** — deep-learning models for ADMET, virtual screening, and molecular property prediction; next Chemistry-focus pass.
- **TorchDrug / PyTDC / DiffDock / PyOpenMS / matchms / cobrapy (K-Dense Skills)** — remaining chemistry-stack siblings, surface incrementally.
- **Retrosynthesis MCP** — no Claude-installable wrapper for AiZynthFinder / ASKCOS / IBM RXN located 2026-05-25; revisit on next Chemistry-focus pass.
- **OpenClaw Medical Skills Library** — 869-skill MIT-licensed collection; treat each individual skill (pharmacovigilance, adverse-event detection, PyHealth) as a separate entry.
- **Ensembl MCP servers** (`munch-group/ensembl-mcp`, `effieklimi/ensembl-mcp-server`) — both early-stage; revisit when one stabilises.
- **UCSC Genome MCP** (`hlydecker/ucsc-genome-mcp`) — 12 tools over the UCSC Genome Browser API.
- **NCBI Datasets MCP** (`Augmented-Nature/NCBI-Datasets-MCP-Server`) — 31 tools over the NCBI Datasets API.
- **OpenFDA MCP** (`Augmented-Nature/OpenFDA-MCP-Server`, `ythalorossy/openfda`) — standalone OpenFDA wrappers.
- **Azure FHIR MCP** (`erikhoward/azure-fhir-mcp-server`) — Azure Health Data Services FHIR adapter.
- **AACT Clinical Trials MCP** (`navisbio/aact_mcp`) — SQL-over-PostgreSQL alternative to the ClinicalTrials.gov v2 API; complementary to the v2-API MCP surfaced 2026-05-23.
- **Augmented-Nature ChEMBL-MCP-Server** — 22-tool community alternative to the official Anthropic ChEMBL connector; useful for users without marketplace access. Deferred because the first-party connector now covers the same surface.
- **easysolutions906 Healthcare MCP** (`@easysolutions906/mcp-healthcare`) — 10-tool community bundle covering ICD-10, NPI, NDC, and DEA in a single server; complementary to the four discrete Anthropic Healthcare MCPs. Revisit on next Translational pass if users want a single-install alternative.
- **IEDB MCP wrapper** — no Claude-installable wrapper for the IEDB Query API located on the 2026-05-26 Immunology pass; the IEDB API exposes ~2.2M epitopes and is a natural MCP candidate. Revisit on next Immunology-focus pass.
- **BCR/TCR repertoire MCP** — no dedicated MCP server for immcantation / VDJdb / McPAS-TCR identified on the 2026-05-26 sweep; awesome-vdj catalogs upstream libraries but no Claude wrapper yet.
- **Adaptyv (K-Dense Skill)** — wraps NetSolP / SoluProt / SolubleMPNN / ESM / ipTM / pSAE for antibody affinity maturation and developability prep; strong Immunology candidate, surface incrementally.
- **MDAnalysis (K-Dense Skill)** — standalone trajectory-analysis sibling to the new `molecular-dynamics` skill; may warrant its own entry once the K-Dense catalog confirms whether `mdanalysis` is a distinct `SKILL.md` directory or only the analysis half of `molecular-dynamics`.
- **Cryo-EM MCP / Skill** — no Claude-installable wrapper for RELION / cryoSPARC / CTFFIND located on the 2026-05-27 Structural pass; revisit on next Integrative Structural and Computational Biology pass.
- **RFdiffusion / ProteinMPNN Claude Skill** — protein-design model wrappers; not yet packaged as a Claude Skill or MCP server on the 2026-05-27 sweep.
- **BioPython / Bioservices (K-Dense Skills)** — confirmed present in K-Dense `scientific-skills/`; both span all life-science domains, useful as next-run Molecular & Cellular Biology additions if cellxgene/scvelo/arboreto are not enough coverage.
- **Aeon / TimesFM (K-Dense Skills)** — time-series forecasting siblings noted in K-Dense docs; only narrowly biomedical (e.g., longitudinal-clinical-data forecasting), revisit if a Translational pass needs more candidates.
- **NeuroClaw** (`CUHK-AIM-Group/NeuroClaw`) — 81-skill neuroimaging library (BIDS, FreeSurfer, FSL, fMRIPrep, CONN, DIPY, QSIPrep, MNE, nilearn integrations; sMRI / fMRI / DWI / EEG / ADNI / HCP / UKB pipelines; arXiv 2604.24696). Repo README explicitly positions `skills/`, `materials/`, `USER.md`, `SOUL.md` as installable into Claude Code, but a copy-pasteable `~/.claude/skills/` snippet is not published upstream and the license file's terms could not be confirmed via WebSearch on 2026-05-29. Strong neuroscience candidate — revisit on next Neuroscience-focus pass once upstream documents an exact Claude Code install command or ships a `marketplace.json`.
- **K-Dense `scientific-skills/` → `skills/` path migration** — search results indicate K-Dense moved skill directories from `scientific-skills/<name>/` to `skills/<name>/` as of v2.43.0 to match the Agent Skills CLI layout, but both paths still appear in upstream search indexes. Verify on next K-Dense pass and update existing K-Dense skill pages (`bids`, `neurokit2`, `neuropixels-analysis`, `scanpy`, `anndata`, `pydeseq2`, `scvi-tools`, etc.) if the old path no longer resolves.

## User requests (open)

_None._

## User requests (closed this run)

_None._
