---
title: Curator state
parent: Recipes
nav_exclude: true
---

# Curator state

## Recently surfaced

- **Analyze an existing MD trajectory for stability, flexibility, and contacts** (added 2026-06-13) — rung-2 [MDAnalysis skill](../catalog/tools/mdanalysis-trajectory.html) recipe for post-simulation analysis of a finished GROMACS/AMBER/NAMD/CHARMM trajectory: load-and-sanity-check → `align.AlignTraj`-corrected RMSD/RMSF/Rg over a stated production window → interface residue-residue contact map + `HydrogenBondAnalysis` occupancy → backbone PCA (scree + PC1/PC2 projection), with the [MDTraj skill](../catalog/tools/mdtraj-trajectory-analysis.html) as the DSSP/Ramachandran fallback. Integrative Structural and Computational Biology focus-day recipe; the post-simulation-analysis companion (bidirectionally cross-linked) to the existing [GROMACS setup recipe](items/set-up-protein-md-simulation-in-gromacs.html), distinguished by serving users who already have a trajectory (any engine) and need contacts/H-bonds/PCA the Copilot's closing step doesn't cover. `Proposed` — no documented LLM-driven MDAnalysis-skill assembly; grounded in [Michaud-Agrawal et al., *J. Comput. Chem.* 32:2319 (2011)](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.21787), [McGibbon et al., *Biophys. J.* 109:1528 (2015)](https://doi.org/10.1016/j.bpj.2015.08.015), and class-level agentic-MD evidence ([MDCrow 2025](https://iopscience.iop.org/article/10.1088/2632-2153/ae4b07); MDGym 2026 as the autonomy caution).
- **Scan a therapeutic antibody for glycosylation sites** (added 2026-06-13) — rung-2 [Glycoengineering skill](../catalog/tools/glycoengineering.html) recipe: heavy/light-chain N-X-S/T sequon detection (Fc Asn-297 vs unintended variable-domain sites) → O-glycosylation hotspot prediction → parent-vs-variant sequon diff → optional minimal site-knockout edit suggestions, with handoff to the [ESM variant-scoring recipe](items/score-protein-variants-with-esm.html) for substitution tolerability and the [Adaptyv skill](../catalog/tools/adaptyv.html) for wet-lab validation. Immunology and Microbiology focus-day recipe; cookbook's first antibody-developability / glycosylation recipe. `Proposed` — no documented LLM-driven glycoengineering-skill assembly; grounded in 2026 Fc-glycan/ADCC literature ([Shuang et al., *mAbs* 2026](https://doi.org/10.1080/19420862.2026.2657099); [Illés 2026](https://doi.org/10.18071/isz.79.0131)) and [Klingler et al., *Biotechnol. Bioeng.* 2024](https://doi.org/10.1002/bit.28616).
- **Compute a bacterial pan-genome from a set of genome assemblies** (added 2026-06-13) — rung-3 toolbelt chaining the [Bakta skill](../catalog/tools/bakta-genome-annotation.html) (identical per-genome annotation → GFF3) into the [Roary skill](../catalog/tools/roary-pangenome.html) (CD-HIT/BLAST/MCL clustering → core/soft-core/shell/cloud partition, `gene_presence_absence.csv`, core-gene MAFFT alignment), with the `core_gene_alignment.aln` handing off to the [phylogenetics recipe](items/build-phylogenetic-tree-from-sequences.html). [Prokka skill](../catalog/tools/prokka-genome-annotation.html) noted as the legacy annotation alternative. Immunology and Microbiology focus-day recipe; cookbook's first comparative-genomics / pan-genome recipe. `Proposed` — no documented LLM-driven Bakta→Roary assembly; grounded in [Page et al., *Bioinformatics* 31:3691 (2015)](https://doi.org/10.1093/bioinformatics/btv421), [Schwengers et al., *Microb. Genom.* 7:000685 (2021)](https://doi.org/10.1099/mgen.0.000685), and a 2025 27,884-genome *A. baumannii* Prokka+Roary application [Sholeh et al., *Mol. Genet. Genomics* (2025)](https://doi.org/10.1007/s00438-025-02265-3).
- **Profile ChIP-seq or ATAC-seq signal around genomic features** (added 2026-06-11) — rung-2 [deepTools skill](../catalog/tools/deeptools.html) recipe taking aligned ChIP-seq/ATAC-seq BAMs through BPM-normalized `bamCoverage` bigWigs → `multiBamSummary`/`plotCorrelation` replicate QC → `computeMatrix` + `plotHeatmap`/`plotProfile` TSS/peak-centered visualization, with upstream BAM handling via [pysam](../catalog/tools/pysam.html). Molecular and Cellular Biology focus-day recipe; cookbook's first ChIP-seq/ATAC-seq coverage-profiling recipe. `Proposed` — no documented LLM-driven deepTools assembly; grounded in [Ramírez et al., *NAR* 44:W160 (2016)](https://doi.org/10.1093/nar/gkw257).
- **Predict gene-knockout phenotypes with flux balance analysis** (added 2026-06-11) — rung-2 [COBRApy skill](../catalog/tools/cobrapy.html) recipe taking a genome-scale SBML model through baseline FBA sanity-check → genome-wide `single_gene_deletion` essentiality ranking → focused `double_gene_deletion` synthetic-lethality screen with an explicit growth-ratio essentiality threshold. Molecular and Cellular Biology focus-day recipe; cookbook's first constraint-based metabolic-modelling recipe. `Proposed` — no documented LLM-driven COBRApy assembly; grounded in [Ebrahim et al., *BMC Syst. Biol.* 7:74 (2013)](https://doi.org/10.1186/1752-0509-7-74) and [Orth et al., *Nat. Biotechnol.* 28:245 (2010)](https://doi.org/10.1038/nbt.1614).

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
