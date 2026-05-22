---
title: Curator state
parent: Recipes
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Sort spikes from a Neuropixels recording end-to-end** (added 2026-05-22) — rung-2 neuropixels-analysis skill recipe; first Neuroscience-only recipe in the cookbook, surfaced on the Friday focus-area pass.
- **Integrate multiple single-cell RNA-seq datasets across batches** (added 2026-05-22) — rung-2 scvi-tools skill recipe; answers user request #7 and grounded in Hrovatin 2025 / scIB-E 2025 benchmarks.
- **Build a target dossier from gene name to structure to cancer dependency** (added 2026-05-21) — rung-3 toolbelt (Open Targets + UniProt + AlphaFold + DepMap); first `Proposed`-evidence recipe.
- **Run bulk RNA-seq differential expression from a counts matrix** (added 2026-05-21) — rung-2 PyDESeq2 skill recipe; pairs with the scRNA-seq QC recipe for the transcriptomics arc.
- **Run first-pass QC on a single-cell RNA-seq dataset** (added 2026-05-21) — rung-2 single-cell-rna-qc skill recipe; canonical Mol/Cell Bio data-analysis entry point.

## Flagged for review

_None._

## Deferred — next-run priority

- **Pseudobulk single-cell DE end-to-end** — natural composition of the QC + Scanpy pseudobulk + PyDESeq2 path; deferred because the Scanpy-MCP pseudobulk aggregation flow is mentioned but not yet documented as a focused end-to-end workflow.
- **Variant interpretation for a clinical case** — BioMCP covers ClinicalTrials.gov + MyVariant + OpenFDA; defer to Translational Medicine focus day.
- **Drug repurposing scan against a disease** — Open Targets + ChEMBL/PubChem + DrugBank; defer to Drug Repurposing focus day.
- **Discover NWB recordings on DANDI and prepare them for sorting** — Neurosift Tools MCP + neuropixels-analysis skill; pairs with the new spike-sorting recipe but distinct problem (discovery vs analysis). Defer to a future Neuroscience focus day.
- **Choose an integration method via scIB benchmarking** — companion to the integration recipe; needs a documented `scib-metrics` driver in the catalog before composing.

## Missing components

_None._

## User requests (open)

_None._

## User requests (closed this run)

_None._
