---
title: Curator state
parent: Recipes
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Compute a bacterial pan-genome from a set of genome assemblies** (added 2026-06-13) — rung-3 toolbelt chaining the [Bakta skill](../catalog/tools/bakta-genome-annotation.html) (identical per-genome annotation → GFF3) into the [Roary skill](../catalog/tools/roary-pangenome.html) (CD-HIT/BLAST/MCL clustering → core/soft-core/shell/cloud partition, `gene_presence_absence.csv`, core-gene MAFFT alignment), with the `core_gene_alignment.aln` handing off to the [phylogenetics recipe](items/build-phylogenetic-tree-from-sequences.html). [Prokka skill](../catalog/tools/prokka-genome-annotation.html) noted as the legacy annotation alternative. Immunology and Microbiology focus-day recipe; cookbook's first comparative-genomics / pan-genome recipe. `Proposed` — no documented LLM-driven Bakta→Roary assembly; grounded in [Page et al., *Bioinformatics* 31:3691 (2015)](https://doi.org/10.1093/bioinformatics/btv421), [Schwengers et al., *Microb. Genom.* 7:000685 (2021)](https://doi.org/10.1099/mgen.0.000685), and a 2025 27,884-genome *A. baumannii* Prokka+Roary application [Sholeh et al., *Mol. Genet. Genomics* (2025)](https://doi.org/10.1007/s00438-025-02265-3).
- **Profile ChIP-seq or ATAC-seq signal around genomic features** (added 2026-06-11) — rung-2 [deepTools skill](../catalog/tools/deeptools.html) recipe taking aligned ChIP-seq/ATAC-seq BAMs through BPM-normalized `bamCoverage` bigWigs → `multiBamSummary`/`plotCorrelation` replicate QC → `computeMatrix` + `plotHeatmap`/`plotProfile` TSS/peak-centered visualization, with upstream BAM handling via [pysam](../catalog/tools/pysam.html). Molecular and Cellular Biology focus-day recipe; cookbook's first ChIP-seq/ATAC-seq coverage-profiling recipe. `Proposed` — no documented LLM-driven deepTools assembly; grounded in [Ramírez et al., *NAR* 44:W160 (2016)](https://doi.org/10.1093/nar/gkw257).
- **Predict gene-knockout phenotypes with flux balance analysis** (added 2026-06-11) — rung-2 [COBRApy skill](../catalog/tools/cobrapy.html) recipe taking a genome-scale SBML model through baseline FBA sanity-check → genome-wide `single_gene_deletion` essentiality ranking → focused `double_gene_deletion` synthetic-lethality screen with an explicit growth-ratio essentiality threshold. Molecular and Cellular Biology focus-day recipe; cookbook's first constraint-based metabolic-modelling recipe. `Proposed` — no documented LLM-driven COBRApy assembly; grounded in [Ebrahim et al., *BMC Syst. Biol.* 7:74 (2013)](https://doi.org/10.1186/1752-0509-7-74) and [Orth et al., *Nat. Biotechnol.* 28:245 (2010)](https://doi.org/10.1038/nbt.1614).
- **Score point mutations for functional impact with a protein language model** (added 2026-06-10) — rung-2 [ESM skill](../catalog/tools/esm.html) recipe taking a wild-type sequence (optionally fetched by UniProt accession via the [gget skill](../catalog/tools/gget.html)) and a substitution list through masked-marginal log-likelihood-ratio scoring → a ranked tolerated/deleterious CSV, with a wt-marginal one-pass variant for full single-mutation landscapes. Integrative Structural and Computational Biology focus-day recipe; cookbook's first zero-shot variant-effect / protein-fitness recipe and the database-free complement to the [clinical-variant interpretation](items/interpret-clinical-variant.html) recipe. `Proposed` — no documented LLM-driven ESM-skill scoring assembly; grounded in [Meier et al., *NeurIPS* 2021](https://www.biorxiv.org/content/10.1101/2021.07.09.450648v1.full), the [ProteinGym benchmark](https://pmc.ncbi.nlm.nih.gov/articles/PMC10723403/), and 2025 directed-evolution use [Zhang et al., *Nat. Commun.* 2025](https://doi.org/10.1038/s41467-025-56751-8).
- **Build a phylogenetic tree from a set of sequences** (added 2026-06-09) — rung-2 [Phylogenetics skill](../catalog/tools/phylogenetics.html) recipe taking a FASTA of homologous sequences through MAFFT `--auto` alignment → gap-column trimming → IQ-TREE 2 ModelFinder + ultrafast-bootstrap ML inference → midpoint/outgroup rooting → an ETE3-annotated tree figure, handing the Newick off to the [ETE Toolkit](../catalog/tools/etetoolkit.html) and the [16S diversity](items/compute-16s-microbiome-diversity.html) recipe (which consumes the rooted tree for UniFrac). Immunology and Microbiology focus-day recipe; cookbook's first phylogenetics / tree-building recipe (viral phylodynamics, microbial genomics, protein-family analysis). `Proposed` — no documented LLM-driven phylogenetics workflow; grounded in the field-standard tool references [Katoh & Standley, *MBE* 30:772 (2013)](https://doi.org/10.1093/molbev/mst010), [Minh et al., *MBE* 37:1530 (2020)](https://doi.org/10.1093/molbev/msaa015), [Kalyaanamoorthy et al., *Nat. Methods* 14:587 (2017)](https://doi.org/10.1038/nmeth.4285), [Hoang et al., *MBE* 35:518 (2018)](https://doi.org/10.1093/molbev/msx281), plus class-level [Biomni (bioRxiv 2025.05.30.656746)](https://doi.org/10.1101/2025.05.30.656746).

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
