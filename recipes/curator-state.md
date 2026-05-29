---
title: Curator state
parent: Recipes
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Compute HRV from an ECG recording** (added 2026-05-29) — rung-2 NeuroKit2 Claude skill recipe taking a single-lead ECG to time-/frequency-/non-linear HRV indices with quality-flagged epoching; second Neuroscience-primary recipe (joins the Neuropixels spike-sorting recipe) and the cookbook's first peripheral-signal recipe. `Proposed` evidence — NeuroKit2 itself is validated ([Makowski 2021 *Behavior Research Methods*](https://doi.org/10.3758/s13428-020-01516-y); [Pham 2021 *Sensors*](https://doi.org/10.3390/s21123998)) but no documented LLM-driven assembly exists. Closest analogue: [EEGAgent (Yan et al., arXiv:2511.09947, 2025-11-12)](https://arxiv.org/abs/2511.09947), AAAI-26-accepted, which uses an LLM to schedule EEG analysis tools (different modality, custom toolbox).
- **Assemble a tissue reference atlas from the CELLxGENE Census** (added 2026-05-28) — rung-2 cellxgene-census skill recipe pulling a versioned AnnData slice with the CZ-trained scVI embedding attached; first Molecular and Cellular Biology focus-day recipe to consume the Census; evidence anchored in the Census team's published `comp_bio_data_integration_scvi` notebook, the scvi-hub paper (Ergen 2025, *Nature Methods*), and the Sikkema 2023 integrated human lung atlas (*Nature Medicine*).
- **Infer a gene-regulatory network from single-cell RNA-seq** (added 2026-05-28) — rung-2 Arboreto skill recipe running GRNBoost2 on a QC'd / integrated AnnData with a TF-restricted regressor and seed-stabilised reruns; second Molecular and Cellular Biology focus-day recipe; evidence anchored in Moerman 2019 (*Bioinformatics*, GRNBoost2), van de Sande 2020 (*Nature Protocols*, SCENIC workflow), and Bravo González-Blas 2023 (*Nature Methods*, SCENIC+).
- **Triage an AlphaFold model for structure-based drug design** (added 2026-05-27) — rung-2 AlphaFold MCP recipe; first Integrative Structural and Computational Biology-primary recipe; `Proposed` evidence grounded in the EBI AlphaFold Protein Structure Database papers (Varadi 2022/2024), the AlphaFold-Multimer interface-pLDDT benchmark (Bryant 2022), and the Karelina 2023 *JCIM* assessment of AlphaFold for small-molecule docking.
- **Estimate pharmacokinetic properties of a small molecule** (added 2026-05-27) — answers user request #8; rung-3 RDKit + MedChem + ChEMBL assembly producing a descriptor / rule-based / analog-anchored PK card; `Proposed` evidence, closest analogues ChemCrow (Bran 2024) and PharmaBench (Niu 2024); flagged the absence of a Claude-installable ADMET predictor (ADMET-AI / AdmetLab / Deep-PK) as a Missing component.

## Flagged for review

_None._

## Deferred — next-run priority

- **Pseudobulk single-cell DE end-to-end** — natural composition of the QC + Scanpy pseudobulk + PyDESeq2 path; deferred because the Scanpy-MCP pseudobulk aggregation flow is mentioned but not yet documented as a focused end-to-end workflow.
- **Discover NWB recordings on DANDI and prepare them for sorting** — Neurosift Tools MCP + neuropixels-analysis skill; pairs with the spike-sorting recipe but distinct problem (discovery vs analysis). Defer to a future Neuroscience focus day.
- **Organise a raw DICOM dataset into a BIDS layout** — clean rung-2 fit for the [BIDS skill](../catalog/tools/bids.html) (DICOM→BIDS via HeuDiConv / dcm2bids, PyBIDS validation, BIDS-Apps prep). Considered for this Neuroscience focus day but deferred to keep the run within the recipe soft cap; revisit on the next Neuroscience pass.
- **Process resting-state EEG for spectral features end-to-end** — natural companion to the HRV recipe using the NeuroKit2 skill on EEG channels (bandpower, microstates, complexity measures). Defer to a future Neuroscience focus day; closest analogous LLM workflow is [EEGAgent](https://arxiv.org/abs/2511.09947) (Yan et al., AAAI-26).
- **Choose an integration method via scIB benchmarking** — companion to the integration recipe; needs a documented `scib-metrics` driver in the catalog before composing.
- **Draft a Phase 2/3 clinical-trial protocol from an indication brief** — the [`clinical-trial-protocol`](../catalog/tools/clinical-trial-protocol.html) Anthropic plugin is the obvious rung-2 fit. Defer to a future Translational Medicine focus day; expected `Reported`-class because Anthropic ships it as a sample skill rather than a benchmarked tool.
- **Look up adverse events for an approved drug via OpenFDA** — BioMCP exposes the OpenFDA API; small enough to be a clean rung-2 recipe.
- **Prepare an AlphaFold-Multimer model of a protein-protein complex for interface analysis** — natural companion to the AlphaFold triage recipe but blocked on co-folding / Multimer tooling not yet in `catalog/tools/`; revisit after the next Integrative Structural and Computational Biology pass.
- **RNA velocity / latent-time analysis with scVelo** — natural rung-2 follow-on to the new Census atlas and integration recipes; deferred because most published scVelo case studies require upstream velocyto / STARsolo / kallisto-bustools spliced-counts pipelines that aren't yet in the catalog (a CLI-only step before Claude takes over). Revisit after either the scVelo SKILL.md adds a worked example or a velocity-aware aligner skill is catalogued.
- **Drive pySCENIC end-to-end (motif filtering + AUCell)** — natural rung-3 toolbelt extension of the new GRN-inference recipe; deferred because pySCENIC (the cisTarget + AUCell stack downstream of Arboreto) is not yet wrapped as a Claude skill or MCP server. Surfaced as a Missing component note.

## Missing components

- **pySCENIC wrapper (cisTarget + AUCell)** — no Claude-installable component for the steps downstream of GRNBoost2 (motif filtering against cisTarget databases, per-cell regulon AUCell scoring). Would unlock a full SCENIC-pipeline recipe on top of the new GRN-inference recipe. Surfaced 2026-05-28.
- **ADMET-AI / AdmetLab 3.0 / Deep-PK wrapper** — none of the leading ML-based ADMET predictors ([Swanson et al., *Bioinformatics* 2024](https://doi.org/10.1093/bioinformatics/btae416); [Fu et al., *NAR* 2024](https://doi.org/10.1093/nar/gkae236)) has a Claude-installable wrapper (skill, MCP server, or plugin) in [`catalog/tools/`](../catalog/) today. Their inclusion would upgrade the *Estimate PK properties* recipe from descriptor-and-analog-anchored estimation to a defensible ML-prediction layer for endpoints (CYP isoform IC50, hERG IC50, microsomal clearance) that pure descriptors miss. Surfaced 2026-05-27.
- **DeepChem (K-Dense Skill)** — flagged in the catalog curator's state file as "next Chemistry-focus pass." Would also strengthen the PK-properties recipe and unlock a virtual-screen scoring recipe. Surfaced 2026-05-27.
- **Co-folding / AlphaFold-Multimer / Boltz-2 wrapper** — no Claude-installable component for protein-protein or protein-ligand co-folding currently in the catalog. Would unlock a complex-modelling companion to the AlphaFold triage recipe. Surfaced 2026-05-27.
- **MARRVEL-MCP** ([bioRxiv 2025-11-26](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1), [`hyunhwan-bcm/MARRVEL_MCP`](https://github.com/hyunhwan-bcm/MARRVEL_MCP/)) — rare-disease variant-interpretation MCP server with 39 tools and a published 95%-accuracy benchmark on 45 expert-curated tasks. Would strengthen the *Interpret a clinical variant* recipe from `Proposed` to `Reported` and open a Mendelian-disease-specific recipe. Surfaced 2026-05-23.

## User requests (open)

- [#12 @goodb 2026-05-27] (no trailer emitted; needs curator triage) title="[Recipe feedback]" label=claude:recipe-feedback — could not access the issue body from this run (no `gh` permission); leaving open for the next run with `gh` access.

## User requests (closed this run)

_None._
