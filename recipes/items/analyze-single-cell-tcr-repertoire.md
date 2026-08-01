---
title: Analyze a single-cell TCR repertoire alongside gene expression
parent: All recipes
grand_parent: Recipes
nav_order: 1
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-18
summary: Use the scirpy Analysis skill to QC paired single-cell TCR chains, define clonotypes, quantify clonal expansion, and overlay clonality on the transcriptomic UMAP.
---

# Analyze a single-cell TCR repertoire alongside gene expression

Hand Claude Code a 10x/AIRR single-cell VDJ dataset paired with its gene expression and get back chain-pairing QC, exact-CDR3 clonotypes, per-cluster clonal-expansion statistics, and clonality mapped onto the transcriptomic UMAP — as committed, re-runnable analysis rather than a one-off session.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You ran a single-cell experiment with paired 5' gene expression and VDJ (TCR) libraries — a tumor, an infection time course, an autoimmune lesion — and you want to connect T-cell *phenotype* to T-cell *clonality*. Which transcriptional states are clonally expanded? Do expanded clones sit in an exhausted or effector cluster? How diverse is the repertoire within each condition, and does it overlap across samples? Answering this means joining two modalities correctly, and the joins are where the errors hide.

The footguns are specific to single-cell receptor data: keeping multichain "doublets" and orphan-chain cells that should be filtered by chain-pairing QC; defining TCR clonotypes by nucleotide-distance clustering (correct for BCR, wrong for TCR, where exact CDR3-nt identity is the standard because T cells do not somatically hypermutate); reading legacy per-chain obs columns instead of the AIRR awkward-array model; and reporting expansion without normalizing for cells-per-sample. "Solved" looks like: point the agent at your data, get back `clonotypes.csv` (clonotype IDs, sizes, expansion bins), per-cluster/per-condition diversity and overlap tables, a UMAP colored by clonal expansion, and a provenance record naming the scirpy version and clonotype-definition parameters.

## Recommended approach

1. **Install the [scirpy Analysis skill](../../catalog/tools/scirpy-analysis.html).** Clone the bioSkills repo and copy the one skill (`cp -r bioSkills/tcr-bcr-analysis/scirpy-analysis ~/.claude/skills/`), following the catalog page. The skill drives scirpy (v0.24+) integrated with scanpy/mudata on the AIRR awkward-array model; install its Python dependencies (scirpy, scanpy, mudata) when prompted on first use.

2. **Fix your inputs.** You need the VDJ output (10x `filtered_contig_annotations.csv`, an AIRR TSV, or dandelion/BD Rhapsody format) and the matching QC'd, clustered gene-expression `.h5ad` (the output of the [single-cell QC recipe](qc-single-cell-rna-seq.html), ideally already [cell-type annotated](annotate-cell-types-in-single-cell-data.html)). The barcodes must match between modalities.

3. **Have the skill write a committed analysis script, not just answers.** A prompt:

   ```
   Use the scirpy-analysis skill to write me a Python script
   sc_tcr.py that, from filtered_contig_annotations.csv and the
   clustered gene-expression adata.h5ad:
     1. Loads VDJ with scirpy, runs pp.index_chains, and pairs it
        with the transcriptome into one AnnData/MuData on matching
        barcodes.
     2. Runs chain_qc and FILTERS multichain doublets and orphan
        cells; report how many cells were dropped and why.
     3. Defines TCR clonotypes by EXACT CDR3-nt identity
        (define_clonotypes) — not nucleotide-distance clustering;
        write clonotypes.csv (clonotype_id, size, expansion bin,
        dominant V/J).
     4. Computes clonal expansion, alpha diversity per cluster and
        per condition (normalized for cells per group), and
        repertoire overlap across samples; write the tables.
     5. Overlays clonal expansion onto the transcriptomic UMAP and
        saves the figure.
     6. Writes provenance.json: scirpy/scanpy/mudata versions, the
        clonotype-definition strategy and parameters (receptor_arms,
        dual_ir), input file sha256s, run date, and model id.
   Commit sc_tcr.py; do not paste the tables back as prose I can't
   audit.
   ```

   Pin the environment with a `requirements.txt` (scirpy, scanpy, mudata, awkward pinned to exact versions). Keep `sc_tcr.py`, the pinned environment, `clonotypes.csv`, the diversity/overlap tables, the UMAP figure, and `provenance.json` under version control alongside the inputs.

4. **Read the results critically.** Confirm the dropped-cell counts from `chain_qc` are a small, sane fraction — a large orphan-chain fraction usually signals a barcode mismatch between the two libraries, not real biology. Verify clonotypes were defined by exact CDR3-nt identity (the provenance record makes this auditable). Expanded clones concentrated in an exhausted/effector transcriptional cluster is the canonical tumor/infection signal; a flat, high-diversity repertoire with no expansion means either a naive population or too few captured cells.

5. **Hand off.** Because the scirpy version and clonotype parameters are pinned in `provenance.json`, re-running `sc_tcr.py` reproduces the clonotype partition and figures. The dominant expanded clonotypes and their CDR3 sequences are natural candidates for antigen-specificity follow-up — feed them to the [TCR-Epitope Binding skill](../../catalog/tools/tcr-epitope-binding.html) to cluster by specificity (tcrdist3/GLIPH2) and look up known antigens (VDJdb/IEDB/McPAS-TCR).

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill orchestrates the whole single-cell repertoire pipeline (modality pairing, chain-pairing QC, clonotype definition, expansion/diversity, UMAP overlay). Plain Claude Code (rung 1) could call scirpy directly, but the skill encodes the correct-usage decisions that determine validity: filtering multichain doublets, using exact CDR3-nt identity for TCR (not the BCR-style distance clustering), and working on the AIRR awkward-array model rather than legacy obs columns. Those are exactly the choices a first-time scirpy user gets wrong. Rung 3+ is unnecessary: VDJ-plus-expression in, clonotypes-and-figures out is a single well-bounded analysis.

## Availability

Fully open. The scirpy Analysis skill is MIT-licensed and scirpy/scanpy/mudata are free open-source academic software. All computation runs locally on your data — no account, no upload.

## Compute requirements

Laptop-sufficient. Chain QC, clonotype definition, and expansion/diversity scoring on a typical single-cell dataset (tens of thousands of T cells) run in minutes on CPU with 8–16 GB RAM. No GPU. The transcriptome side (neighbors/UMAP) is the heavier step, but it is usually already computed in the input `.h5ad` from the upstream QC recipe. Very large atlases (hundreds of thousands of cells) benefit from more RAM but stay CPU-only.

## Evidence

Reported. scirpy is the documented scverse-ecosystem standard for single-cell TCR/BCR repertoire analysis, published with a benchmark against alternative tools ([Sturm et al., *Bioinformatics* 2020](https://pubmed.ncbi.nlm.nih.gov/32614448/)). The exact workflow this recipe drives — loading VDJ, pairing with the transcriptome, chain QC, clonotype identification, expansion and diversity, and integration with scanpy for downstream analysis — is the subject of a 2025 methods-book protocol chapter that walks through it step by step on multi-modal scRNA/TCR data ([Plattner, Sturm & Rieder, *Methods Cell Biol.* 2025](https://pubmed.ncbi.nlm.nih.gov/41106935/)).

No head-to-head benchmark of the *agent-driven skill* versus a hand-written scirpy notebook is published — the skill buys correct usage (doublet filtering, TCR-appropriate clonotype definition, AIRR-model access) and a pinned provenance record, not a new method. scirpy is the validated component.

## Alternatives considered

- **Plain Claude Code, no skill (rung 1).** Feasible if you already run scirpy and know to filter chain-QC doublets and use exact CDR3-nt identity for TCR. The skill exists to prevent those exact errors, so prefer it unless you are an experienced repertoire analyst.
- **The [BCR clonal-lineage recipe](reconstruct-bcr-clonal-lineages.html) (Immcantation).** Reach for that when you have *B-cell* repertoires and the question is affinity maturation — it derives a data-driven SHM threshold and builds germline-rooted lineage trees. This recipe is the T-cell, transcriptome-integrated counterpart: TCRs don't hypermutate, so clonotypes are exact-identity and the interesting join is clonality-to-phenotype, not lineage trees. The bioSkills `mixcr-analysis` skill covers *bulk* repertoire extraction from raw reads, upstream of both.
- **Cell Ranger / scRepertoire for a quick clonotype tally.** Fine for a first count, but they don't give you scverse-native integration with your scanpy object or the same QC/diversity toolkit. Use this recipe when the transcriptome-clonality join is the point.

## See also

- [scirpy Analysis (bioSkills)](../../catalog/tools/scirpy-analysis.html) — the skill this recipe drives.
- [QC a single-cell RNA-seq dataset](qc-single-cell-rna-seq.html) — produces the clustered `.h5ad` this recipe pairs against.
- [Annotate cell types in a single-cell dataset](annotate-cell-types-in-single-cell-data.html) — label the transcriptional clusters before overlaying clonality.
- [Reconstruct B-cell clonal lineages from AIRR-seq](reconstruct-bcr-clonal-lineages.html) — the B-cell, lineage-tree counterpart.
- [TCR-Epitope Binding (bioSkills)](../../catalog/tools/tcr-epitope-binding.html) — downstream antigen-specificity clustering and database lookup on the expanded clonotypes.
- [Annotate TCR antigen specificity by clustering and database lookup](annotate-tcr-specificity-by-clustering.html) — the downstream recipe that drives that skill on this recipe's expanded clonotypes.

## Sources

- [Sturm et al., "Scirpy: a Scanpy extension for analyzing single-cell T-cell receptor-sequencing data," *Bioinformatics* 36:4817–4818](https://pubmed.ncbi.nlm.nih.gov/32614448/) — the tool and its benchmark; published 2020; verified 2026-07-18 (this run).
- [Plattner, Sturm & Rieder, "Analysis of single-cell TCR repertoires and gene expression from multi-modal scRNA-seq data," *Methods Cell Biol.* 2025](https://pubmed.ncbi.nlm.nih.gov/41106935/) — step-by-step scirpy multi-modal protocol; published 2025; verified 2026-07-18 (this run).
- [scirpy documentation](https://scirpy.scverse.org/) — the tool the skill drives; verified 2026-07-18 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=analyze-single-cell-tcr-repertoire&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fanalyze-single-cell-tcr-repertoire.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
