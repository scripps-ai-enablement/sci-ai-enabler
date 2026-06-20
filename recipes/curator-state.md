---
title: Curator state
parent: Recipes
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Predict RNA secondary structure and target-site accessibility** (added 2026-06-20) — rung-2 [ViennaRNA skill](../catalog/tools/viennarna-structure-prediction.html) recipe: RNA sequence → MFE fold + partition function (ensemble free energy, MFE frequency, diversity, centroid) → `RNAplfold` target-window accessibility (mean/min unpaired probability with a ≥0.5 / 0.2–0.5 / <0.2 rule of thumb) → optional `RNAduplex` guide-strand check → a parameter-pinned, ranked design card for siRNA/sgRNA/ASO design or riboswitch analysis. Integrative Structural and Computational Biology focus-day recipe; cookbook's first RNA-secondary-structure recipe, cross-linked to the protein-sequence ESM-scoring recipe. `Proposed` — no documented LLM-driven ViennaRNA assembly; grounded in [Lorenz et al., *Algorithms Mol. Biol.* 2011](https://doi.org/10.1186/1748-7188-6-26), [Gruber et al., *Methods Mol. Biol.* 2015](https://pubmed.ncbi.nlm.nih.gov/25577387/), with accessibility-predicts-efficacy as the design rationale.
- **Annotate a single bacterial genome assembly** (added 2026-06-20) — rung-2 [Bakta skill](../catalog/tools/bakta-genome-annotation.html) recipe: one assembled bacterial/archaeal genome → database-pinned annotation (CDS, rRNA/tRNA/ncRNA, CRISPR arrays, replicon features) → GFF3/GenBank/protein-FASTA → a feature-count sanity check, with replicon-completeness and database-version footguns surfaced and an optional CARD/VFDB AMR overlay noted. Immunology and Microbiology focus-day recipe; the single-isolate counterpart to the multi-genome [pan-genome recipe](items/compute-bacterial-pangenome-from-assemblies.html), kept rung-2 (not rung-3) because one genome is one tool. `Reported` — single-isolate Bakta annotation is the field-standard opening move in genome characterization ([Santhosh et al., *BMC Genomics* 2025](https://doi.org/10.1186/s12864-025-12363-6); [Schwengers et al., *Microb. Genom.* 2021](https://doi.org/10.1099/mgen.0.000685)).
- **Infer transcription-factor and pathway activities from expression** (added 2026-06-20) — rung-2 [decoupler-MCP](../catalog/tools/decoupler-mcp.html) recipe: load an annotated AnnData → `tf_activity` (CollecTRI/ULM) → `pathway_activity` (PROGENy/MLM) → between-condition ranked activity tables with a grounded summary and a positive-control check, consuming the object from the [scRNA-seq QC recipe](items/qc-single-cell-rna-seq.html). Immunology and Microbiology focus-day recipe; cookbook's first footprint/activity-inference recipe, kept distinct from over-representation enrichment and de-novo GRN inference. `Proposed` — no documented LLM-driven decoupler-MCP assembly; grounded in [Badia-i-Mompel et al., *Bioinform. Adv.* 2022](https://doi.org/10.1093/bioadv/vbac016), [Schubert et al., *Nat. Commun.* 2018 (PROGENy)](https://doi.org/10.1038/s41467-017-02391-6), [Müller-Dott et al., *NAR* 2023 (CollecTRI)](https://doi.org/10.1093/nar/gkad841).
- **Map a disease to its implicated genes and pathways** (added 2026-06-20) — rung-3 chain of two Reported recipes: [Open Targets target ranking](items/prioritize-targets-within-a-disease.html) (overall association score) → [gget/Enrichr functional enrichment](items/run-functional-enrichment-on-a-gene-list.html), with DisGeNET as a positive control and a grounded synthesis. Canonicalized from composition report #43 (knee OA, EFO_0004616). `Reported` — #43 documents the chain running end-to-end on a laptop in <1 min with the disease recovered as a DisGeNET positive control.
- **Screen a polypharmacy medication list for drug-drug interactions** (added 2026-06-14) — rung-2 [DDInter skill](../catalog/tools/ddinter-database.html) recipe: per-drug DDInter ID resolution → pairwise interaction queries → cited severity/mechanism/management table with explicit "clean" lines, plus an optional rung-3 [DailyMed](../catalog/tools/dailymed-database.html) + [ClinPGx](../catalog/tools/clinpgx-database.html) overlay on major pairs (phenoconversion bridge to the [PGx dosing recipe](items/build-pharmacogenomic-dosing-report.html)). Drug Repurposing and Discovery focus-day recipe; cookbook's first DDI-screening recipe. `Reported` — [Domián et al., *Explor. Res. Clin. Soc. Pharm.* 2025](https://pubmed.ncbi.nlm.nih.gov/41425735/) shows ungrounded LLMs over-flag/hallucinate DDIs (Copilot 1,813 vs a 204-interaction reference on 57 patients), so screening must be database-anchored; DDInter is the peer-reviewed reference ([Xiong et al., *NAR* 2022](https://doi.org/10.1093/nar/gkab880)).

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
