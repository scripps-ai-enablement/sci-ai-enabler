---
title: Curator state
parent: Catalog
nav_exclude: true
---

# Curator state

## Recently surfaced

- **clinical-trial-protocol (Anthropic Healthcare Plugin)** (added 2026-05-23) — Anthropic skill for drafting FDA/NIH-compliant Phase 2/3 clinical-trial protocols via a four-step waypoint workflow.
- **CMS Coverage MCP** (added 2026-05-23) — Anthropic-published MCP over the CMS Local and National Coverage Determinations for Medicare prior-auth, appeals, and policy lookup.
- **ICD-10 Codes MCP** (added 2026-05-23) — Anthropic-published MCP for ICD-10-CM / ICD-10-PCS diagnosis and procedure code lookup, sourced from CMS and CDC.
- **ClinicalTrials.gov MCP Server (cyanheads)** (added 2026-05-23) — Apache-2.0 MCP over the ClinicalTrials.gov v2 API with full study retrieval, outcomes extraction, and patient-to-trial matching; hosted public instance available.
- **BIDS (Claude Skill)** (added 2026-05-22) — K-Dense skill for organizing, validating, and querying Brain Imaging Data Structure datasets across 11 BIDS modalities.

## Flagged for review

- **allenbrain-mcp** — upstream license unset; flagged 2026-05-20 before any redistribution.

## Deferred — next-run priority

- **NPI Registry MCP (Anthropic Healthcare)** — Anthropic-published MCP for NPPES provider lookup; the fourth healthcare-marketplace MCP from this run. Deferred to stay within the 5-entry soft cap.
- **Cellxgene Census (K-Dense Skill)** — query CZ CELLxGENE Discover census (61M+ cells, 1000+ datasets) via TileDB-SOMA. Strong Molecular & Cellular Biology candidate.
- **scVelo (K-Dense Skill)** — RNA velocity analysis on single-cell data; next Thursday's Molecular & Cellular Biology pass.
- **Arboreto (K-Dense Skill)** — gene regulatory network inference (GRNBoost2, GENIE3) on single-cell expression.
- **Standalone `anthropics/life-sciences` plugins** beyond Open Targets and AdisInsight: `owkin`, `chembl`, `cortellis`, `tooluniverse`, `consensus`, `medidata`.
- **OpenClaw Medical Skills Library** — 869-skill MIT-licensed collection; treat each individual skill (pharmacovigilance, adverse-event detection, PyHealth) as a separate entry.
- **Ensembl MCP servers** (`munch-group/ensembl-mcp`, `effieklimi/ensembl-mcp-server`) — both early-stage; revisit when one stabilises.
- **UCSC Genome MCP** (`hlydecker/ucsc-genome-mcp`) — 12 tools over the UCSC Genome Browser API.
- **NCBI Datasets MCP** (`Augmented-Nature/NCBI-Datasets-MCP-Server`) — 31 tools over the NCBI Datasets API.
- **OpenFDA MCP** (`Augmented-Nature/OpenFDA-MCP-Server`, `ythalorossy/openfda`) — standalone OpenFDA wrappers.
- **Azure FHIR MCP** (`erikhoward/azure-fhir-mcp-server`) — Azure Health Data Services FHIR adapter.
- **AACT Clinical Trials MCP** (`navisbio/aact_mcp`) — SQL-over-PostgreSQL alternative to the ClinicalTrials.gov v2 API; complementary to the v2-API MCP just surfaced.

## User requests (open)

_None._

## User requests (closed this run)

_None._
