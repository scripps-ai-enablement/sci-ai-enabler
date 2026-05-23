---
title: Curator state
parent: Recipes
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Match a patient summary to recruiting clinical trials** (added 2026-05-23) — rung-2 BioMCP / cyanheads-ClinicalTrials.gov-MCP recipe; first Translational-Medicine recipe; evidence grounded in TrialGPT (Jin 2024, 87.3% criterion-matching accuracy).
- **Interpret a clinical variant from a natural-language query** (added 2026-05-23) — rung-2 BioMCP recipe; `Proposed` evidence, closest benchmark MARRVEL-MCP (2025-11).
- **Sort spikes from a Neuropixels recording end-to-end** (added 2026-05-22) — rung-2 neuropixels-analysis skill recipe; first Neuroscience-only recipe in the cookbook, surfaced on the Friday focus-area pass.
- **Integrate multiple single-cell RNA-seq datasets across batches** (added 2026-05-22) — rung-2 scvi-tools skill recipe; answers user request #7 and grounded in Hrovatin 2025 / scIB-E 2025 benchmarks.
- **Build a target dossier from gene name to structure to cancer dependency** (added 2026-05-21) — rung-3 toolbelt (Open Targets + UniProt + AlphaFold + DepMap); first `Proposed`-evidence recipe.

## Flagged for review

_None._

## Deferred — next-run priority

- **Pseudobulk single-cell DE end-to-end** — natural composition of the QC + Scanpy pseudobulk + PyDESeq2 path; deferred because the Scanpy-MCP pseudobulk aggregation flow is mentioned but not yet documented as a focused end-to-end workflow.
- **Drug repurposing scan against a disease** — Open Targets + ChEMBL/PubChem + DrugBank; defer to Drug Repurposing focus day.
- **Discover NWB recordings on DANDI and prepare them for sorting** — Neurosift Tools MCP + neuropixels-analysis skill; pairs with the new spike-sorting recipe but distinct problem (discovery vs analysis). Defer to a future Neuroscience focus day.
- **Choose an integration method via scIB benchmarking** — companion to the integration recipe; needs a documented `scib-metrics` driver in the catalog before composing.
- **Draft a Phase 2/3 clinical-trial protocol from an indication brief** — the [`clinical-trial-protocol`](../catalog/tools/clinical-trial-protocol.html) Anthropic plugin is the obvious rung-2 fit. Defer to a future Translational Medicine focus day; expected `Reported`-class because Anthropic ships it as a sample skill rather than a benchmarked tool.
- **Look up adverse events for an approved drug via OpenFDA** — BioMCP exposes the OpenFDA API; small enough to be a clean rung-2 recipe.

## Missing components

- **MARRVEL-MCP** ([bioRxiv 2025-11-26](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1), [`hyunhwan-bcm/MARRVEL_MCP`](https://github.com/hyunhwan-bcm/MARRVEL_MCP/)) — rare-disease variant-interpretation MCP server with 39 tools and a published 95%-accuracy benchmark on 45 expert-curated tasks. Would strengthen the *Interpret a clinical variant* recipe from `Proposed` to `Reported` and open a Mendelian-disease-specific recipe. Surfaced 2026-05-23.

## User requests (open)

_None._

## User requests (closed this run)

_None._
