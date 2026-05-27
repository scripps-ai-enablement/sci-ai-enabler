---
title: Curator state
parent: Recipes
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Triage an AlphaFold model for structure-based drug design** (added 2026-05-27) — rung-2 AlphaFold MCP recipe; first Integrative Structural and Computational Biology-primary recipe; `Proposed` evidence grounded in the EBI AlphaFold Protein Structure Database papers (Varadi 2022/2024), the AlphaFold-Multimer interface-pLDDT benchmark (Bryant 2022), and the Karelina 2023 *JCIM* assessment of AlphaFold for small-molecule docking.
- **Estimate pharmacokinetic properties of a small molecule** (added 2026-05-27) — answers user request #8; rung-3 RDKit + MedChem + ChEMBL assembly producing a descriptor / rule-based / analog-anchored PK card; `Proposed` evidence, closest analogues ChemCrow (Bran 2024) and PharmaBench (Niu 2024); flagged the absence of a Claude-installable ADMET predictor (ADMET-AI / AdmetLab / Deep-PK) as a Missing component.
- **Filter a virtual screening hit list with drug-likeness rules and structural alerts** (added 2026-05-25) — rung-2 MedChem + Datamol cascade (Lipinski → Veber → PAINS → BRENK); first Chemistry-primary recipe; evidence anchored in the K-Dense lead-optimisation workflow and the foundational filter papers (Baell 2010, Brenk 2008, Lipinski 2001, Veber 2002).
- **Profile a compound's polypharmacology from ChEMBL bioactivity data** (added 2026-05-25) — rung-2 single-tool ChEMBL connector recipe; second Chemistry-primary recipe and compound-centric mirror of the existing target-dossier recipe; evidence grounded in the Anthropic ChEMBL Connector tutorial and Mendez 2019 (NAR).
- **Scan approved drugs for repurposing candidates against a disease** (added 2026-05-24) — rung-3 toolbelt (Open Targets + ChEMBL + DrugBank); first focused Drug Repurposing and Discovery recipe; evidence grounded in DeepDrug (Li 2025), Robin (Ghareeb 2026), and the DREBIOP LLM-validation benchmark (Zunzunegui Sanz 2025).

## Flagged for review

_None._

## Deferred — next-run priority

- **Pseudobulk single-cell DE end-to-end** — natural composition of the QC + Scanpy pseudobulk + PyDESeq2 path; deferred because the Scanpy-MCP pseudobulk aggregation flow is mentioned but not yet documented as a focused end-to-end workflow.
- **Discover NWB recordings on DANDI and prepare them for sorting** — Neurosift Tools MCP + neuropixels-analysis skill; pairs with the new spike-sorting recipe but distinct problem (discovery vs analysis). Defer to a future Neuroscience focus day.
- **Choose an integration method via scIB benchmarking** — companion to the integration recipe; needs a documented `scib-metrics` driver in the catalog before composing.
- **Draft a Phase 2/3 clinical-trial protocol from an indication brief** — the [`clinical-trial-protocol`](../catalog/tools/clinical-trial-protocol.html) Anthropic plugin is the obvious rung-2 fit. Defer to a future Translational Medicine focus day; expected `Reported`-class because Anthropic ships it as a sample skill rather than a benchmarked tool.
- **Look up adverse events for an approved drug via OpenFDA** — BioMCP exposes the OpenFDA API; small enough to be a clean rung-2 recipe.
- **Prepare an AlphaFold-Multimer model of a protein-protein complex for interface analysis** — natural companion to the new AlphaFold triage recipe but blocked on co-folding / Multimer tooling not yet in `catalog/tools/`; revisit after the next Integrative Structural and Computational Biology pass.

## Missing components

- **ADMET-AI / AdmetLab 3.0 / Deep-PK wrapper** — none of the leading ML-based ADMET predictors ([Swanson et al., *Bioinformatics* 2024](https://doi.org/10.1093/bioinformatics/btae416); [Fu et al., *NAR* 2024](https://doi.org/10.1093/nar/gkae236)) has a Claude-installable wrapper (skill, MCP server, or plugin) in [`catalog/tools/`](../catalog/) today. Their inclusion would upgrade the new *Estimate PK properties* recipe from descriptor-and-analog-anchored estimation to a defensible ML-prediction layer for endpoints (CYP isoform IC50, hERG IC50, microsomal clearance) that pure descriptors miss. Surfaced 2026-05-27.
- **DeepChem (K-Dense Skill)** — flagged in the catalog curator's state file as "next Chemistry-focus pass." Would also strengthen the PK-properties recipe and unlock a virtual-screen scoring recipe. Surfaced 2026-05-27.
- **Co-folding / AlphaFold-Multimer / Boltz-2 wrapper** — no Claude-installable component for protein-protein or protein-ligand co-folding currently in the catalog. Would unlock a complex-modelling companion to the new AlphaFold triage recipe. Surfaced 2026-05-27.
- **MARRVEL-MCP** ([bioRxiv 2025-11-26](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1), [`hyunhwan-bcm/MARRVEL_MCP`](https://github.com/hyunhwan-bcm/MARRVEL_MCP/)) — rare-disease variant-interpretation MCP server with 39 tools and a published 95%-accuracy benchmark on 45 expert-curated tasks. Would strengthen the *Interpret a clinical variant* recipe from `Proposed` to `Reported` and open a Mendelian-disease-specific recipe. Surfaced 2026-05-23.

## User requests (open)

_None._

## User requests (closed this run)

_None._
