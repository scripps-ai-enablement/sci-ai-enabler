---
title: Curator state
parent: Recipes
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Profile a cancer cohort's genomics with cBioPortal** (added 2026-06-14) — rung-2 [cBioPortal skill](../catalog/tools/cbioportal-database.html) recipe: study/molecular-profile lookup → per-gene mutation+CNA alteration frequency + co-occurrence/mutual-exclusivity → TMB summary → Kaplan-Meier OS split by mutation status, with cohort-denominator caveats enforced. Translational Medicine focus-day recipe; cookbook's first cohort-level cancer-genomics recipe, cross-linked to the gene-centric [target dossier](items/build-target-dossier.html), single-variant [variant-interpretation](items/interpret-clinical-variant.html), and adjusted-modelling [survival recipe](items/fit-survival-model-to-clinical-outcomes.html). `Reported` — the cBioPortal-backed AI-HOPE conversational-agent family documents the assembly class ([AI-HOPE-WNT, *Front. Artif. Intell.* 2025](https://pubmed.ncbi.nlm.nih.gov/40860720/); [AI-HOPE-TP53, *Cancers* 2025](https://pubmed.ncbi.nlm.nih.gov/40940961/)).
- **Run a GWAS on case-control genotype data** (added 2026-06-14) — rung-2 [PLINK2 skill](../catalog/tools/plink2-gwas-analysis.html) recipe: sample QC (call rate, sex-check, het outliers) → variant QC (`--geno`/`--maf`/`--hwe` in controls) → LD prune → `--pca 10` → PCA-adjusted `--glm` logistic regression → lambda_GC check, then hand genome-wide-significant loci to the [GWAS Catalog skill](../catalog/tools/gwas-database.html) for prior-art annotation. Translational Medicine focus-day recipe; cookbook's first GWAS recipe. `Proposed` — grounded in [Chang et al., *GigaScience* 4:7 (2015)](https://doi.org/10.1186/s13742-015-0047-8) and [Marees et al., *Int. J. Methods Psychiatr. Res.* 27:e1608 (2018)](https://doi.org/10.1002/mpr.1608). Biobank-scale mixed-model path deferred — no regenie/SAIGE component catalogued (see Missing components).
- **Build a pharmacogenomic dosing report from a patient's diplotypes** (added 2026-06-14) — rung-2 [ClinPGx skill](../catalog/tools/clinpgx-database.html) recipe: diplotype→metabolizer-phenotype translation via the CPIC PostgREST API → per-drug CPIC/DPWG dosing lookup → cited drug|gene|phenotype|recommendation table, with explicit "no actionable guidance" flagging and a [DDInter](../catalog/tools/ddinter-database.html) phenoconversion overlay noted. Translational Medicine focus-day recipe; cookbook's first PGx-dosing recipe, kept distinct from the germline-pathogenicity [variant-interpretation recipe](items/interpret-clinical-variant.html). `Proposed` — grounded in the CPIC guideline corpus ([Amstutz et al., *Clin. Pharmacol. Ther.* 2018](https://doi.org/10.1002/cpt.911); [Molden & Jukić, *Front. Pharmacol.* 2021](https://doi.org/10.3389/fphar.2021.650750)).
- **Infer cell-cell communication from single-cell RNA-seq** (added 2026-06-13) — rung-2 [LIANA-MCP](../catalog/tools/liana-mcp.html) recipe: load an annotated AnnData → `ls_ccc_method` → multi-method `communicate` (CellPhoneDB/Connectome/NATMI/SingleCellSignalR) → `rank_aggregate` consensus ligand-receptor tetrads → `circle_plot`/`ccc_dotplot`, consuming the annotated object from the [scRNA-seq QC recipe](items/qc-single-cell-rna-seq.html). Molecular and Cellular Biology focus-day recipe; cookbook's first cell-cell-communication recipe. `Proposed` — no documented LLM-driven LIANA-MCP assembly; grounded in [Dimitrov et al., *Nat. Commun.* 13:3735 (2022)](https://doi.org/10.1038/s41467-022-30755-0), a 2026 consensus-LIANA application ([Wei et al., *PLOS ONE* 2026](https://doi.org/10.1371/journal.pone.0345045)), and the method-disagreement benchmark ([Xie et al., *Biomolecules* 13:1211 (2023)](https://doi.org/10.3390/biom13081211)).
- **Call peaks and find enriched motifs from ChIP-seq or ATAC-seq** (added 2026-06-13) — rung-3 toolbelt chaining the [MACS3 skill](../catalog/tools/macs3-peak-calling.html) (`callpeak`, narrow/broad mode → narrowPeak BED) into the [HOMER skill](../catalog/tools/homer-motif-analysis.html) (`annotatePeaks.pl` nearest-gene context + `findMotifsGenome.pl` de-novo/known motif enrichment), both from the SciAgent-Skills collection. Molecular and Cellular Biology focus-day recipe; the binding-site/motif companion to the existing [deepTools signal-profiling recipe](items/profile-chipseq-atacseq-signal-around-features.html) (bidirectionally cross-linked), which deliberately stops before peak calling. `Proposed` — no documented LLM-driven MACS3→HOMER assembly; grounded in [Zhang et al., *Genome Biol.* 9:R137 (2008)](https://doi.org/10.1186/gb-2008-9-9-r137) and [Heinz et al., *Mol. Cell* 38:576 (2010)](https://doi.org/10.1016/j.molcel.2010.05.004).

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

_None._
