---
title: Curator state
parent: Catalog
nav_exclude: true
---

# Curator state

## Recently surfaced

- **ChEMBL Connector** (added 2026-05-24) — Anthropic-packaged plugin and Claude.ai connector over EMBL-EBI's ChEMBL bioactive-compound database (compound, target, bioactivity, mechanism-of-action lookup).
- **ToolUniverse** (added 2026-05-24) — Harvard / MIT MCP server bundling 600+ vetted scientific tools across literature, chemistry, omics, and clinical trials; surfaced via `anthropics/life-sciences`.
- **Owkin Pathology Explorer Connector** (added 2026-05-24) — remote MCP connector exposing Owkin's H&E whole-slide image analysis agent for tumour-microenvironment profiling.
- **clinical-trial-protocol (Anthropic Healthcare Plugin)** (added 2026-05-23) — Anthropic skill for drafting FDA/NIH-compliant Phase 2/3 clinical-trial protocols via a four-step waypoint workflow.
- **CMS Coverage MCP** (added 2026-05-23) — Anthropic-published MCP over the CMS Local and National Coverage Determinations for Medicare prior-auth, appeals, and policy lookup.

## Flagged for review

- **allenbrain-mcp** — upstream license unset; flagged 2026-05-20 before any redistribution.

## Deferred — next-run priority

- **Cortellis Plugin (`anthropics/life-sciences`)** — Clarivate Cortellis drug-pipeline / deals data; standalone marketplace entry beyond `adisinsight`.
- **Medidata Connector (`anthropics/life-sciences`)** — clinical-operations / EDC platform integration; announced Jan 2026 but install path still gated behind Medidata account onboarding.
- **Consensus Plugin (`anthropics/life-sciences`)** — Consensus.app evidence-search connector; verify install path.
- **NPI Registry MCP (Anthropic Healthcare)** — Anthropic-published MCP for NPPES provider lookup; fourth healthcare-marketplace MCP from the 2026-05-23 run, still pending.
- **Cellxgene Census (K-Dense Skill)** — query CZ CELLxGENE Discover census (61M+ cells, 1000+ datasets) via TileDB-SOMA. Strong Molecular & Cellular Biology candidate.
- **scVelo (K-Dense Skill)** — RNA velocity analysis on single-cell data; next Thursday's Molecular & Cellular Biology pass.
- **Arboreto (K-Dense Skill)** — gene regulatory network inference (GRNBoost2, GENIE3) on single-cell expression.
- **OpenClaw Medical Skills Library** — 869-skill MIT-licensed collection; treat each individual skill (pharmacovigilance, adverse-event detection, PyHealth) as a separate entry.
- **Ensembl MCP servers** (`munch-group/ensembl-mcp`, `effieklimi/ensembl-mcp-server`) — both early-stage; revisit when one stabilises.
- **UCSC Genome MCP** (`hlydecker/ucsc-genome-mcp`) — 12 tools over the UCSC Genome Browser API.
- **NCBI Datasets MCP** (`Augmented-Nature/NCBI-Datasets-MCP-Server`) — 31 tools over the NCBI Datasets API.
- **OpenFDA MCP** (`Augmented-Nature/OpenFDA-MCP-Server`, `ythalorossy/openfda`) — standalone OpenFDA wrappers.
- **Azure FHIR MCP** (`erikhoward/azure-fhir-mcp-server`) — Azure Health Data Services FHIR adapter.
- **AACT Clinical Trials MCP** (`navisbio/aact_mcp`) — SQL-over-PostgreSQL alternative to the ClinicalTrials.gov v2 API; complementary to the v2-API MCP surfaced 2026-05-23.
- **Augmented-Nature ChEMBL-MCP-Server** — 22-tool community alternative to the official Anthropic ChEMBL connector; useful for users without marketplace access. Deferred because the first-party connector now covers the same surface.

## User requests (open)

_None._

## User requests (closed this run)

_None._
