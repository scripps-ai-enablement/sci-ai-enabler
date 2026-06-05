---
title: Curator state
parent: Catalog
nav_exclude: true
---

# Curator state

## Recently surfaced

- **General-Purpose Utilities category** (2026-06-04) — new 8th catalog category (cross-cutting utilities shelf, not a research area). 68 domain-agnostic K-Dense skills (plotting, dataframes, ML/stats, scientific communication, adjacent-domain science, multi-perspective deliberation) ingested into it; only 3 K-Dense skills remain out of scope.
- **K-Dense batch ingest** (2026-06-04) — one-time ingestion of the life-science-relevant subset of `K-Dense-AI/scientific-agent-skills`. K-Dense is now in diff-only mode (see `AGENT.md`); scope decisions recorded in `scripts/kdense_category_map.yaml`. Subsumes the incremental COBRApy / DiffDock / Adaptyv / DeepChem / PyTDC surfacings from the prior daily runs (those pages are retained with their richer hand-written content; the batch repaired their install paths). Also migrated all existing K-Dense pages off the dead `claude-scientific-skills` marketplace to `npx skills add` and the `skills/` path.
- **OpenNeuro MCP** (added 2026-05-29) — Community MCP server (QuentinCody) wrapping the OpenNeuro GraphQL API; hosted Cloudflare Workers SSE endpoint, MIT + Academic Citation Requirement license. Complements the Neurosift Tools MCP (DANDI + NWB) by covering OpenNeuro's MRI / MEG / EEG / iEEG / ECoG archive.

## Flagged for review

- **allenbrain-mcp** — upstream license unset; flagged 2026-05-20 before any redistribution.
- **biorxiv@life-sciences** / **clinical-trials@life-sciences** plugins — flagged 2026-05-28; published in the `anthropics/life-sciences` marketplace per upstream commit `e96556b` but the backing `mcp.deepsense.ai` MCP host returns NXDOMAIN. No catalog entry created until the endpoint is restored.

## Deferred — next-run priority

- **Cortellis Plugin (`anthropics/life-sciences`)** — Clarivate Cortellis drug-pipeline / deals data; standalone marketplace entry beyond `adisinsight`.
- **Medidata Connector (`anthropics/life-sciences`)** — clinical-operations / EDC platform integration; announced Jan 2026 but install path still gated behind Medidata account onboarding.
- **Consensus Plugin (`anthropics/life-sciences`)** — Consensus.app evidence-search connector; verify install path.
- **biorxiv@life-sciences plugin** — `anthropics/life-sciences` marketplace entry currently DOA (`mcp.deepsense.ai` NXDOMAIN per upstream issue #42 / commit `e96556b`). Revisit when upstream restores the endpoint.
- **clinical-trials@life-sciences plugin** — same DOA status as biorxiv@life-sciences; distinct from both the `adisinsight` plugin (Springer Nature) and the `clinicaltrials-gov-mcp` community entry. Revisit when the endpoint is restored.
- **Retrosynthesis MCP** — no Claude-installable wrapper for AiZynthFinder / ASKCOS / IBM RXN located on the 2026-05-25 or 2026-06-01 Chemistry passes; revisit on next Chemistry-focus pass.
- **MCP_Vina** (`shogo-d-nakamura/MCP_Vina`) — AutoDock Vina MCP server with `dock_molecule` / `get_available_targets` tools; currently single-target (AKT1 only) with `uv`-based local install. Surfaced on the 2026-06-01 Chemistry pass but deferred because the target list is too narrow to justify a catalog entry today; revisit once additional targets or a docking-grid-builder workflow lands upstream.
- **OpenClaw Medical Skills Library** — 869-skill MIT-licensed collection; batch-ingest the life-science-relevant subset using the K-Dense pipeline (`scripts/ingest_kdense.py` parameterised for this repo), with cross-collection dedup against existing entries (one entry per tool).
- **Ensembl MCP servers** (`munch-group/ensembl-mcp`, `effieklimi/ensembl-mcp-server`) — both early-stage; revisit when one stabilises.
- **UCSC Genome MCP** (`hlydecker/ucsc-genome-mcp`) — 12 tools over the UCSC Genome Browser API.
- **NCBI Datasets MCP** (`Augmented-Nature/NCBI-Datasets-MCP-Server`) — 31 tools over the NCBI Datasets API.
- **OpenFDA MCP** (`Augmented-Nature/OpenFDA-MCP-Server`, `ythalorossy/openfda`) — standalone OpenFDA wrappers.
- **Azure FHIR MCP** (`erikhoward/azure-fhir-mcp-server`) — Azure Health Data Services FHIR adapter.
- **AACT Clinical Trials MCP** (`navisbio/aact_mcp`) — SQL-over-PostgreSQL alternative to the ClinicalTrials.gov v2 API; complementary to the v2-API MCP surfaced 2026-05-23.
- **Augmented-Nature ChEMBL-MCP-Server** — 22-tool community alternative to the official Anthropic ChEMBL connector; useful for users without marketplace access. Deferred because the first-party connector now covers the same surface.
- **easysolutions906 Healthcare MCP** (`@easysolutions906/mcp-healthcare`) — 10-tool community bundle covering ICD-10, NPI, NDC, and DEA in a single server; complementary to the four discrete Anthropic Healthcare MCPs. Revisit on next Translational pass if users want a single-install alternative.
- **IEDB MCP wrapper** — no Claude-installable wrapper for the IEDB Query API located on the 2026-05-26 or 2026-06-02 Immunology passes; the IEDB API exposes ~2.2M epitopes and ~6.8M assays (Nucleic Acids Research 2024 update) and remains a natural MCP candidate. Revisit on next Immunology-focus pass.
- **BCR/TCR repertoire MCP / Immcantation skill** — no Claude-installable wrapper for Immcantation (Change-O / SHazaM / Alakazam / SCOPer / Dowser), nf-core/airrflow, VDJdb, or McPAS-TCR identified on the 2026-05-26 or 2026-06-02 sweeps. Immcantation 4.7.0-2026.01.21 and nf-core/airrflow are stable upstream — the gap is purely a missing skill/MCP wrapper. Revisit on next Immunology-focus pass.
- **Metagenomics / microbiome MCP** — no Claude-installable wrapper for QIIME2 / Kraken2 / MetaPhlAn located on the 2026-06-02 sweep. Revisit on next Immunology-focus pass.
- **MDAnalysis (K-Dense Skill)** — standalone trajectory-analysis sibling to the `molecular-dynamics` skill; may warrant its own entry only if the K-Dense collection ever ships a distinct `mdanalysis` `SKILL.md` directory (it currently does not — the trajectory analysis lives inside `molecular-dynamics`).
- **Cryo-EM MCP / Skill** — no Claude-installable wrapper for RELION / cryoSPARC / CTFFIND located on the 2026-05-27 or 2026-06-03 Structural passes; revisit on next Integrative Structural and Computational Biology pass.
- **RFdiffusion / ProteinMPNN Claude Skill** — protein-design model wrappers; standalone Claude Skill / MCP not located on the 2026-05-27 or 2026-06-03 sweeps. Both are bundled inside the `longevity-genie/protein_hunter_mcp` server (which also includes Boltz / Chai-lab / PyRosetta / LigandMPNN) — that server is a viable structural-biology entry once its install path is verified outside the longevity-genie organisation.
- **Rowan MCP** (`k-yenko/rowan-mcp`) — molecular-dynamics, docking (Vina, QVina2, Smina), protein cofolding, MSA via the Rowan computational-chemistry platform. Listed in punkpeye/awesome-mcp-servers; surfaced on the 2026-06-03 Structural pass but deferred pending install-path verification and pricing/auth confirmation. Note: the K-Dense **Rowan skill** is now catalogued (`rowan.md`); when this MCP is verified, fold it into that page as an alternative install path rather than creating a second entry.
- **Boltz / Protein Hunter MCP** (`longevity-genie/protein_hunter_mcp`, `biomolecular-design-nexus/boltz_mcp`) — Boltz2 structure / affinity prediction wrappers. Surfaced on the 2026-06-03 Structural pass but deferred — Boltz model weights are MIT but the protein_hunter_mcp install path requires `uv` + CUDA GPU and the upstream README does not yet publish a copy-pasteable `claude mcp add` snippet.
- **NeuroClaw** (`CUHK-AIM-Group/NeuroClaw`) — 81-skill neuroimaging library (BIDS, FreeSurfer, FSL, fMRIPrep, CONN, DIPY, QSIPrep, MNE, nilearn integrations; sMRI / fMRI / DWI / EEG / ADNI / HCP / UKB pipelines; arXiv 2604.24696). Repo README explicitly positions `skills/`, `materials/`, `USER.md`, `SOUL.md` as installable into Claude Code, but a copy-pasteable `~/.claude/skills/` snippet is not published upstream and the license file's terms could not be confirmed via WebSearch on 2026-05-29. Strong neuroscience candidate — batch-ingest the life-science-relevant subset via the K-Dense pipeline once upstream documents an exact Claude Code install command or ships a `marketplace.json`.

## User requests (open)

_None._

## User requests (closed this run)

_None._
