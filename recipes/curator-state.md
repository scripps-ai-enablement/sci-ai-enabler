---
title: Curator state
parent: Recipes
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Score a drug-combination screen for synergy** (added 2026-06-21) — rung-2 [ToolUniverse Drug Synergy skill](../catalog/tools/tooluniverse-drug-synergy.html) recipe: user-supplied single-agent + combination effect data (on one consistent scale) → model selection by data shape (`DrugSynergy_calculate_bliss`/`_hsa`/`_loewe`/`_zip`/`_ci`) → synergy score → synergy/additive/antagonism classification via the standard ±10 thresholds (CI < 1 inverse), with scale-mixing and dose-dependence footguns surfaced. Drug Repurposing and Discovery focus-day recipe; cookbook's first combination-synergy recipe, cross-linked to the [polypharmacology recipe](items/profile-compound-polypharmacology.html) and the [drug-repurposing scan recipe](items/scan-drug-repurposing-candidates.html). `Proposed` — no documented Claude-driven ToolUniverse synergy assembly; grounded in the field-standard reference models from [Ianevski et al., *Nucleic Acids Research* 2022 (SynergyFinder 3.0)](https://doi.org/10.1093/nar/gkac382) and the skill's `SKILL.md`. `Laptop`.
- **Segment an organ or tumor in a medical image with nnU-Net** (added 2026-06-21) — rung-2 [nnU-Net skill](../catalog/tools/nnunet-segmentation.html) recipe: labeled CT/MRI volumes → dataset-fingerprint planning → auto-configured preprocessing/architecture → 5-fold cross-validated training → best-config/ensemble selection → held-out mask prediction + per-case volume QC, with the nnU-Net `imagesTr`/`_0000` data contract and the ≥10 GB VRAM / multi-day-per-fold cost surfaced. Translational Medicine focus-day recipe; cookbook's first medical-image-segmentation recipe, chained off the [DICOM-to-BIDS recipe](items/organize-raw-dicom-to-bids-layout.html) (upstream) and feeding the [survival-model recipe](items/fit-survival-model-to-clinical-outcomes.html) (tumor volume → prognostic covariate). `Reported` — nnU-Net is field-defining ([Isensee et al., *Nature Methods* 2021](https://www.nature.com/articles/s41592-020-01008-z): matches/beats specialized solutions on 23 segmentation challenges with no manual tuning); the Claude-skill assembly is not independently benchmarked. `Workstation with GPU`.
- **Detect somatic copy-number variants from tumor sequencing** (added 2026-06-21) — rung-2 [CNVkit skill](../catalog/tools/cnvkit-copy-number.html) recipe: tumor WES/targeted-panel BAMs → pooled-reference build → coverage binning + GC/repeat bias correction → CBS segmentation → gene-level amp/del calls (stated log2 thresholds) → scatter/diagram QC plots + SEG/VCF export, with purity/ploidy and matched-normal footguns surfaced. Translational Medicine focus-day recipe; cookbook's first somatic-CNV recipe, paired with the [cBioPortal cohort recipe](items/profile-cancer-cohort-genomics-with-cbioportal.html). `Reported` — CNVkit is field-standard for capture-data copy number ([Talevich et al., *PLOS Comput. Biol.* 2016](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004873)); the Claude-skill assembly is not independently benchmarked.
- **Predict hospital readmission from EHR data** (added 2026-06-21) — rung-2 [PyHealth skill](../catalog/tools/pyhealth.html) recipe: credentialed EHR extract (MIMIC-IV/eICU/OMOP) → 30-day-readmission task → RETAIN/Transformer sequence model with patient-level split → AUROC/AUPRC + calibration vs a logistic-regression baseline, with DUA and cross-institution-transfer caveats surfaced. Translational Medicine focus-day recipe; cookbook's first EHR clinical-prediction recipe, complementing the [survival-model recipe](items/fit-survival-model-to-clinical-outcomes.html) (which PyHealth was previously only an alternative within). `Proposed` — no documented LLM-driven PyHealth assembly; grounded in [Yang et al., *KDD 2023*](https://dl.acm.org/doi/10.1145/3580305.3599178) and [PyHealth 2.0, arXiv:2601.16414](https://arxiv.org/abs/2601.16414). `Institutional access`.
- **Annotate cell types in a single-cell dataset** (added 2026-06-20) — rung-2 [CellTypist skill](../catalog/tools/celltypist-cell-annotation.html) recipe: QC'd/clustered AnnData → reference-model logistic-regression annotation with `majority_voting` over clusters → per-cell + per-cluster labels + confidence → a canonical-marker sanity check, with an optional rung-3 escalation to the [popV consensus skill](../catalog/tools/popv-cell-annotation.html) (8 classifiers + agreement score) when single-method confidence is poor; planning anchored by the [annotation-guide skill](../catalog/tools/single-cell-annotation-guide.html). Molecular and Cellular Biology focus-day recipe; cookbook's first cell-type-annotation recipe, chained off the [scRNA-seq QC recipe](items/qc-single-cell-rna-seq.html). `Reported` — CellTypist ([Domínguez Conde et al., *Science* 2022](https://www.science.org/doi/10.1126/science.abl5197)) and popV ([Ergen et al., *Nat. Genet.* 2024](https://www.nature.com/articles/s41588-024-01993-3)) are peer-reviewed; the Claude-skill assembly is not independently benchmarked.

## Flagged for review

_None._

## Deferred — next-run priority

- **Select the best experimental PDB structure for a target before docking** — rung-2 fit for the [PDB MCP server](../catalog/tools/pdb.html) (`search_by_uniprot` → resolution / R-free / chain coverage / ligand-bound vs apo / alternate-conformation pre-flight). Considered for this Integrative Structural and Computational Biology focus day but deferred because the AlphaFold-triage recipe already covers the optional PDB cross-check at one step; promoting it to its own recipe needs a clearer use case ("you have a PDB ID and want to know whether it's the right one"). Revisit on the next ISCB focus day.
- **Pseudobulk single-cell DE end-to-end** — natural composition of the QC + Scanpy pseudobulk + PyDESeq2 path; deferred because the Scanpy-MCP pseudobulk aggregation flow is mentioned but not yet documented as a focused end-to-end workflow.
- **Process resting-state EEG for spectral features end-to-end** — natural companion to the HRV recipe using the NeuroKit2 skill on EEG channels (bandpower, microstates, complexity measures). Defer to a future Neuroscience focus day; closest analogous LLM workflow is [EEGAgent](https://arxiv.org/abs/2511.09947) (Yan et al., AAAI-26).
- **Browse OpenNeuro for MRI/EEG/MEG datasets matching a task or modality** — clean rung-2 fit for the [OpenNeuro MCP](../catalog/tools/openneuro.html); GraphQL-driven dataset discovery (task name, modality, subject count, snapshot inspection) as the imaging counterpart to the existing DANDI/NWB recipe. Considered for this Neuroscience focus day but deferred to keep within the soft cap; revisit on the next Neuroscience pass.
- **Query the Allen Brain Atlas for cell-type / connectivity / expression context** — clean rung-2 fit for the [allenbrain-mcp](../catalog/tools/allenbrain.html) (Alpha) — RMA queries, mouse connectivity experiments, brain-structure ontologies, 3D expression grid download. Deferred because the upstream MCP is Alpha with no LICENSE file; revisit after upstream clarifies licensing.
- **Choose an integration method via scIB benchmarking** — companion to the integration recipe; needs a documented `scib-metrics` driver in the catalog before composing.
- **Prepare an AlphaFold-Multimer model of a protein-protein complex for interface analysis** — natural companion to the AlphaFold triage recipe but blocked on co-folding / Multimer tooling not yet in `catalog/tools/`; revisit after the next Integrative Structural and Computational Biology pass.
- **RNA velocity / latent-time analysis with scVelo** — natural rung-2 follow-on to the new Census atlas and integration recipes; deferred because most published scVelo case studies require upstream velocyto / STARsolo / kallisto-bustools spliced-counts pipelines that aren't yet in the catalog (a CLI-only step before Claude takes over). Revisit after either the scVelo SKILL.md adds a worked example or a velocity-aware aligner skill is catalogued.
- **Drive pySCENIC end-to-end (motif filtering + AUCell)** — natural rung-3 toolbelt extension of the new GRN-inference recipe; deferred because pySCENIC (the cisTarget + AUCell stack downstream of Arboreto) is not yet wrapped as a Claude skill or MCP server. Surfaced as a Missing component note.

## Missing components

- **Biobank-scale mixed-model GWAS wrapper (regenie / SAIGE / BOLT-LMM)** — the catalogued [PLINK2 skill](../catalog/tools/plink2-gwas-analysis.html) covers array/small-cohort fixed-effect GWAS (now the [case-control GWAS recipe](items/run-gwas-on-case-control-genotypes.html)), but cohorts of 100k+ samples with relatedness/structure need a linear mixed model to control inflation. No regenie/SAIGE/BOLT-LMM component is Claude-installable today. Would unlock a biobank-scale sibling recipe. Surfaced 2026-06-14.
- **pySCENIC wrapper (cisTarget + AUCell)** — no Claude-installable component for the steps downstream of GRNBoost2 (motif filtering against cisTarget databases, per-cell regulon AUCell scoring). Would unlock a full SCENIC-pipeline recipe on top of the new GRN-inference recipe. Surfaced 2026-05-28.
- **ADMET-AI / AdmetLab 3.0 / Deep-PK wrapper** — none of the leading ML-based ADMET predictors ([Swanson et al., *Bioinformatics* 2024](https://doi.org/10.1093/bioinformatics/btae416); [Fu et al., *NAR* 2024](https://doi.org/10.1093/nar/gkae236)) has a Claude-installable wrapper (skill, MCP server, or plugin) in [`catalog/tools/`](../catalog/) today. Their inclusion would upgrade the *Estimate PK properties* recipe from descriptor-and-analog-anchored estimation to a defensible ML-prediction layer for endpoints (CYP isoform IC50, hERG IC50, microsomal clearance) that pure descriptors miss. Surfaced 2026-05-27.
- **Co-folding / AlphaFold-Multimer / Boltz-2 wrapper** — no Claude-installable component for protein-protein or protein-ligand co-folding currently in the catalog. Would unlock a complex-modelling companion to the AlphaFold triage recipe. Surfaced 2026-05-27.
- **MARRVEL-MCP** ([bioRxiv 2025-11-26](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1), [`hyunhwan-bcm/MARRVEL_MCP`](https://github.com/hyunhwan-bcm/MARRVEL_MCP/)) — rare-disease variant-interpretation MCP server with 39 tools and a published 95%-accuracy benchmark on 45 expert-curated tasks. Would strengthen the *Interpret a clinical variant* recipe from `Proposed` to `Reported` and open a Mendelian-disease-specific recipe. Surfaced 2026-05-23.

## User requests (open)

_None._

## User requests (closed this run)

_None._

## Composition reports

Demand signal from the Composer plugin (`/composer:compose`). The responder routes
`report=composition` entries into `## User requests (open)` like any other request;
process them there each run (promote a success, write a recipe for a gap), then keep a
rolling tally here so the directed pass can prioritize the problem classes and subject
areas scientists actually compose against. Keep the last ~15 lines.

Format: `- YYYY-MM-DD outcome=<worked|gap|failed> problem_class=<…> → <what shipped / note>`

- 2026-06-20 outcome=worked problem_class=Knowledge synthesis → shipped new recipe map-disease-to-genes-and-pathways (Open Targets → gget/Enrichr chain); cascaded Open Targets MCP handshake breakage into prioritize-targets recipe (#43).
