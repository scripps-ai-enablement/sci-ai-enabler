---
title: Curator state
parent: Catalog
nav_exclude: true
---

# Curator state

## Recently surfaced

- **K-Dense batch ingest** (2026-06-04) — one-time ingestion of the life-science-relevant subset of `K-Dense-AI/scientific-agent-skills` (69 of 143 skills: 51 new pages + 18 existing repaired). K-Dense is now in diff-only mode (see `AGENT.md`); scope decisions recorded in `scripts/kdense_category_map.yaml`. Also migrated all existing K-Dense pages off the dead `claude-scientific-skills` marketplace to `npx skills add` and the `skills/` path.
- **OpenNeuro MCP** (added 2026-05-29) — Community MCP server (QuentinCody) wrapping the OpenNeuro GraphQL API; hosted Cloudflare Workers SSE endpoint, MIT + Academic Citation Requirement license. Complements the Neurosift Tools MCP (DANDI + NWB) by covering OpenNeuro's MRI / MEG / EEG / iEEG / ECoG archive.

## Flagged for review

- **allenbrain-mcp** — upstream license unset; flagged 2026-05-20 before any redistribution.
- **biorxiv@life-sciences** / **clinical-trials@life-sciences** plugins — flagged 2026-05-28; published in the `anthropics/life-sciences` marketplace per upstream commit `e96556b` but the backing `mcp.deepsense.ai` MCP host returns NXDOMAIN. No catalog entry created until the endpoint is restored.

## Deferred — next-run priority

- **Cortellis Plugin (`anthropics/life-sciences`)** — Clarivate Cortellis drug-pipeline / deals data; standalone marketplace entry beyond `adisinsight`.
- **Medidata Connector (`anthropics/life-sciences`)** — clinical-operations / EDC platform integration; announced Jan 2026 but install path still gated behind Medidata account onboarding.
- **Consensus Plugin (`anthropics/life-sciences`)** — Consensus.app evidence-search connector; verify install path.
- **NPI Registry MCP (Anthropic Healthcare)** — Anthropic-published MCP for NPPES provider lookup; fourth healthcare-marketplace MCP from the 2026-05-23 run, still pending.
- **biorxiv@life-sciences plugin** — `anthropics/life-sciences` marketplace entry currently DOA (`mcp.deepsense.ai` NXDOMAIN per upstream issue #42 / commit `e96556b`). Revisit when upstream restores the endpoint.
- **clinical-trials@life-sciences plugin** — same DOA status as biorxiv@life-sciences; distinct from both the `adisinsight` plugin (Springer Nature) and the `clinicaltrials-gov-mcp` community entry. Revisit when the endpoint is restored.
- **Retrosynthesis MCP** — no Claude-installable wrapper for AiZynthFinder / ASKCOS / IBM RXN located 2026-05-25; revisit on next Chemistry-focus pass.
- **OpenClaw Medical Skills Library** — 869-skill MIT-licensed collection; batch-ingest the life-science-relevant subset using the K-Dense pipeline (`scripts/ingest_kdense.py` parameterised for this repo), with cross-collection dedup against existing entries (one entry per tool).
- **Ensembl MCP servers** (`munch-group/ensembl-mcp`, `effieklimi/ensembl-mcp-server`) — both early-stage; revisit when one stabilises.
- **UCSC Genome MCP** (`hlydecker/ucsc-genome-mcp`) — 12 tools over the UCSC Genome Browser API.
- **NCBI Datasets MCP** (`Augmented-Nature/NCBI-Datasets-MCP-Server`) — 31 tools over the NCBI Datasets API.
- **OpenFDA MCP** (`Augmented-Nature/OpenFDA-MCP-Server`, `ythalorossy/openfda`) — standalone OpenFDA wrappers.
- **Azure FHIR MCP** (`erikhoward/azure-fhir-mcp-server`) — Azure Health Data Services FHIR adapter.
- **AACT Clinical Trials MCP** (`navisbio/aact_mcp`) — SQL-over-PostgreSQL alternative to the ClinicalTrials.gov v2 API; complementary to the v2-API MCP surfaced 2026-05-23.
- **Augmented-Nature ChEMBL-MCP-Server** — 22-tool community alternative to the official Anthropic ChEMBL connector; useful for users without marketplace access. Deferred because the first-party connector now covers the same surface.
- **IEDB MCP wrapper** — no Claude-installable wrapper for the IEDB Query API located on the 2026-05-26 Immunology pass; the IEDB API exposes ~2.2M epitopes and is a natural MCP candidate. Revisit on next Immunology-focus pass.
- **BCR/TCR repertoire MCP** — no dedicated MCP server for immcantation / VDJdb / McPAS-TCR identified on the 2026-05-26 sweep; awesome-vdj catalogs upstream libraries but no Claude wrapper yet.
- **Cryo-EM MCP / Skill** — no Claude-installable wrapper for RELION / cryoSPARC / CTFFIND located on the 2026-05-27 Structural pass; revisit on next Integrative Structural and Computational Biology pass.
- **RFdiffusion / ProteinMPNN Claude Skill** — protein-design model wrappers; not yet packaged as a Claude Skill or MCP server on the 2026-05-27 sweep.
- **NeuroClaw** (`CUHK-AIM-Group/NeuroClaw`) — 81-skill neuroimaging library (BIDS, FreeSurfer, FSL, fMRIPrep, CONN, DIPY, QSIPrep, MNE, nilearn integrations; sMRI / fMRI / DWI / EEG / ADNI / HCP / UKB pipelines; arXiv 2604.24696). Repo README explicitly positions `skills/`, `materials/`, `USER.md`, `SOUL.md` as installable into Claude Code, but a copy-pasteable `~/.claude/skills/` snippet is not published upstream and the license file's terms could not be confirmed via WebSearch on 2026-05-29. Strong neuroscience candidate — batch-ingest the life-science-relevant subset via the K-Dense pipeline once upstream documents an exact Claude Code install command or ships a `marketplace.json`.

## User requests (open)

- [#15 @goodb 2026-05-29] (no trailer emitted; needs curator triage) title="[Tool feedback] migration smoke test — chembl" label=claude:tool-feedback

## User requests (closed this run)

_None._
