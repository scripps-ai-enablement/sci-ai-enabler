---
title: Recipes updates
parent: Updates
nav_order: 4
permalink: /updates/recipes.html
---

# Recipes updates

Reverse-chronological log of changes to the [recipes cookbook]({{ '/recipes/' | relative_url }}). Newest at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-06-21

### Added

- **Detect somatic copy-number variants from tumor sequencing** (Problem class: Data analysis; Evidence: Reported) — rung-2 [CNVkit skill](catalog/tools/cnvkit-copy-number.html) recipe taking tumor WES/targeted-panel BAMs through pooled-reference construction → coverage binning + bias correction → CBS segmentation → gene-level amplification/deletion calls (with stated log2 thresholds) → scatter/diagram QC plots and SEG/VCF export, with purity/ploidy and matched-normal caveats surfaced. Translational Medicine focus-day recipe; cookbook's first somatic-CNV recipe, paired with the [cBioPortal cohort recipe](recipes/items/profile-cancer-cohort-genomics-with-cbioportal.html) for cohort-level context. `Reported` — CNVkit is the field-standard engine for copy-number from targeted/exome data ([Talevich et al., *PLOS Comput. Biol.* 2016](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004873)); the Claude-skill assembly is not independently benchmarked.
- **Predict hospital readmission from EHR data** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [PyHealth skill](catalog/tools/pyhealth.html) recipe taking a credentialed EHR extract (MIMIC-IV/eICU/OMOP) through the dataset → 30-day-readmission task → RETAIN/Transformer sequence model → patient-level-split AUROC/AUPRC + calibration vs a logistic-regression baseline, with data-use-agreement and cross-institution-transfer caveats surfaced. Translational Medicine focus-day recipe; cookbook's first EHR clinical-prediction recipe, complementing the [survival-model recipe](recipes/items/fit-survival-model-to-clinical-outcomes.html). `Proposed` — no documented LLM-driven PyHealth assembly; grounded in [Yang et al., *KDD 2023*](https://dl.acm.org/doi/10.1145/3580305.3599178) and [PyHealth 2.0, arXiv:2601.16414 (2026)](https://arxiv.org/abs/2601.16414). `Institutional access` (PhysioNet credentialed datasets).
- **Segment an organ or tumor in a medical image with nnU-Net** (Problem class: Data analysis; Evidence: Reported) — rung-2 [nnU-Net skill](catalog/tools/nnunet-segmentation.html) recipe taking labeled CT/MRI volumes through dataset-fingerprint planning → auto-configured preprocessing/architecture → 5-fold cross-validated training → best-config selection → held-out mask prediction + volume QC, with the nnU-Net folder/`_0000` data contract and the GPU/multi-day-per-fold cost surfaced. Translational Medicine focus-day recipe; cookbook's first medical-image-segmentation recipe, chained off the [DICOM-to-BIDS recipe](recipes/items/organize-raw-dicom-to-bids-layout.html) upstream and feeding the [survival-model recipe](recipes/items/fit-survival-model-to-clinical-outcomes.html) downstream. `Reported` — nnU-Net is field-defining ([Isensee et al., *Nature Methods* 2021](https://www.nature.com/articles/s41592-020-01008-z): match/beat specialized solutions on 23 challenges, no manual tuning); the Claude-skill assembly is not independently benchmarked. `Workstation with GPU`.

### Verified (no changes)

- 4 Translational Medicine recipes spot-checked and refreshed to 2026-06-21 (`last_verified` bumped): interpret-clinical-variant, match-patient-to-clinical-trials, scan-adverse-events-for-drug-safety-signal, fit-survival-model-to-clinical-outcomes — all linked catalog pages resolve and source URLs current.

## 2026-06-20

### Added

- **Annotate cell types in a single-cell dataset** (Problem class: Data analysis; Evidence: Reported) — rung-2 [CellTypist skill](catalog/tools/celltypist-cell-annotation.html) recipe taking a QC'd/clustered AnnData through reference-model logistic-regression annotation with `majority_voting` over clusters → per-cell + per-cluster labels + confidence → a canonical-marker sanity check, with an optional rung-3 escalation to the [popV consensus skill](catalog/tools/popv-cell-annotation.html) (8 classifiers + agreement score) when single-method confidence is poor. Molecular and Cellular Biology focus-day recipe; cookbook's first cell-type-annotation recipe, chained off the [scRNA-seq QC recipe](recipes/items/qc-single-cell-rna-seq.html). `Reported` — CellTypist ([Domínguez Conde et al., *Science* 2022](https://www.science.org/doi/10.1126/science.abl5197)) and popV ([Ergen et al., *Nat. Genet.* 2024](https://www.nature.com/articles/s41588-024-01993-3)) are peer-reviewed; the Claude-skill assembly is not independently benchmarked.
- **Predict the regulatory effect of a non-coding variant** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 [AlphaGenome skill](catalog/tools/alphagenome.html) recipe taking a single `chr:pos:ref>alt` variant through tissue-ontology resolution → sequence-to-function scoring across expression / accessibility / histone marks / splicing / TF binding → ranked modalities + ISM motif logo + splicing-disruption analysis, with tissue choice surfaced as the key judgment call. Molecular and Cellular Biology focus-day recipe; cookbook's first non-coding/regulatory variant recipe, cross-linked to the coding-variant [clinical-variant recipe](recipes/items/interpret-clinical-variant.html). `Reported` — AlphaGenome is peer-reviewed ([*Nature* 2026](https://www.nature.com/articles/s41586-025-10014-0): matches/exceeds best external models on 25/26 variant-effect evaluations); `Subscription required` (signup-gated free research-preview API key).
- **Predict RNA secondary structure and target-site accessibility** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [ViennaRNA skill](catalog/tools/viennarna-structure-prediction.html) recipe taking an RNA sequence through MFE folding + partition function → centroid/ensemble metrics → `RNAplfold` target-window accessibility (mean/min unpaired probability) → optional `RNAduplex` guide-strand check → a ranked, parameter-pinned design card for siRNA/sgRNA/ASO design or riboswitch analysis. Integrative Structural and Computational Biology focus-day recipe; cookbook's first RNA-secondary-structure recipe. `Proposed` — no documented LLM-driven ViennaRNA assembly; grounded in [Lorenz et al., *Algorithms Mol. Biol.* 2011](https://doi.org/10.1186/1748-7188-6-26) and the established role of `RNAplfold` accessibility in reagent-efficacy prediction.
- **Infer transcription-factor and pathway activities from expression** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [decoupler-MCP](catalog/tools/decoupler-mcp.html) recipe taking an annotated AnnData through `tf_activity` (CollecTRI/ULM) and `pathway_activity` (PROGENy/MLM) footprint inference → between-condition ranked activity tables → a grounded summary with a positive-control check. Immunology and Microbiology focus-day recipe; cookbook's first footprint/activity-inference recipe, kept distinct from over-representation enrichment and de-novo GRN inference. `Proposed` — no documented LLM-driven decoupler-MCP assembly; grounded in [Badia-i-Mompel et al., *Bioinform. Adv.* 2022](https://doi.org/10.1093/bioadv/vbac016), [Schubert et al., *Nat. Commun.* 2018 (PROGENy)](https://doi.org/10.1038/s41467-017-02391-6), and [Müller-Dott et al., *NAR* 2023 (CollecTRI)](https://doi.org/10.1093/nar/gkad841).
- **Map a disease to its implicated genes and pathways** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-3 chain of two existing Reported recipes: [Open Targets target ranking](recipes/items/prioritize-targets-within-a-disease.html) (overall association score) → [gget/Enrichr functional enrichment](recipes/items/run-functional-enrichment-on-a-gene-list.html), with DisGeNET as a positive control and a grounded synthesis. Canonicalized from composition report [#43](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/43) (knee OA, EFO_0004616). `Reported` — #43 documents the chain running end-to-end on a laptop in under a minute with the disease recovered as a DisGeNET positive control.
- **Annotate a single bacterial genome assembly** (Problem class: Data analysis; Evidence: Reported) — rung-2 [Bakta skill](catalog/tools/bakta-genome-annotation.html) recipe taking one assembled bacterial/archaeal genome through database-pinned annotation (CDS, rRNA/tRNA/ncRNA, CRISPR arrays, replicon features) → GFF3/GenBank/protein-FASTA → a feature-count sanity check, with the replicon-completeness and database-version footguns surfaced and an optional CARD/VFDB AMR overlay noted. Immunology and Microbiology focus-day recipe; the single-isolate counterpart to the multi-genome [pan-genome recipe](recipes/items/compute-bacterial-pangenome-from-assemblies.html). `Reported` — single-isolate Bakta annotation is the field-standard opening move ([Santhosh et al., *BMC Genomics* 2025](https://doi.org/10.1186/s12864-025-12363-6); [Schwengers et al., *Microb. Genom.* 2021](https://doi.org/10.1099/mgen.0.000685)).

### Updated

- **Run functional enrichment on a gene list** — fixed the gget install block (per [#41](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/41)): removed the non-existent `K-Dense-AI/claude-scientific-skills` marketplace, replaced with the catalog's `npx skills add` + manual-HTTPS-clone paths; added a Field-reports note.
- **Prioritize targets within a disease via Open Targets** — added a known-issue note (per [#43](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/43)) that the hosted Open Targets MCP endpoint is failing its `initialize` handshake (JSON-RPC `-32602`); documented the direct GraphQL API and ToolUniverse `OpenTargets_*` tools as the working path, plus a Field-reports entry.

### Verified (no changes)

- 6 aging recipes spot-checked (linked catalog tools resolve and unflagged, canonical sources resolve), `last_verified` bumped to 2026-06-20: **Infer a gene-regulatory network from single-cell RNA-seq**, **Run first-pass QC on a single-cell RNA-seq dataset**, **Triage a stack of new preprints**, **Run bulk RNA-seq differential expression**, **Compute HRV from an ECG recording**, **Discover NWB recordings on DANDI**.

## 2026-06-14

### Added

- **Screen a polypharmacy medication list for drug-drug interactions** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 [DDInter skill](catalog/tools/ddinter-database.html) recipe taking a medication list through per-drug ID resolution → pairwise DDInter queries → a cited severity/mechanism/management table with explicit "clean" lines, plus an optional rung-3 [DailyMed](catalog/tools/dailymed-database.html) + [ClinPGx](catalog/tools/clinpgx-database.html) overlay on the major pairs. Drug Repurposing and Discovery focus-day recipe; cookbook's first DDI-screening recipe. `Reported` — [Domián et al., *Explor. Res. Clin. Soc. Pharm.* 2025](https://pubmed.ncbi.nlm.nih.gov/41425735/) documents that ungrounded LLMs over-flag/hallucinate DDIs (Copilot 1,813 vs a 204-interaction reference on 57 real patients), establishing that screening must be anchored to a curated DDI database — the assembly this recipe recommends.
- **Run a GWAS on case-control genotype data** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [PLINK2 skill](catalog/tools/plink2-gwas-analysis.html) recipe taking a PLINK/VCF genotype set through sample + variant QC (call rate, MAF, HWE-in-controls) → LD pruning → genotype PCA → PCA-adjusted logistic-regression `--glm` association with a lambda_GC inflation check, handing genome-wide-significant loci to the [GWAS Catalog skill](catalog/tools/gwas-database.html) for annotation. Translational Medicine focus-day recipe; cookbook's first GWAS recipe. `Proposed` — no documented LLM-driven PLINK2 assembly; grounded in [Chang et al., *GigaScience* 4:7 (2015)](https://doi.org/10.1186/s13742-015-0047-8) and the canonical QC tutorial ([Marees et al., *Int. J. Methods Psychiatr. Res.* 27:e1608 (2018)](https://doi.org/10.1002/mpr.1608)).
- **Build a pharmacogenomic dosing report from a patient's diplotypes** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-2 [ClinPGx skill](catalog/tools/clinpgx-database.html) recipe taking star-allele diplotypes plus a medication list through diplotype→metabolizer-phenotype translation (CPIC PostgREST API) → per-drug CPIC/DPWG dosing recommendation lookup → a cited drug|gene|phenotype|recommendation table, with explicit "no actionable guidance" flagging and a [DDInter](catalog/tools/ddinter-database.html) phenoconversion overlay noted. Translational Medicine focus-day recipe; cookbook's first pharmacogenomic-dosing recipe, distinct from the germline-pathogenicity [variant-interpretation recipe](recipes/items/interpret-clinical-variant.html). `Proposed` — no documented LLM-driven ClinPGx/CPIC assembly; grounded in the CPIC guideline corpus ([Amstutz et al., *Clin. Pharmacol. Ther.* 2018](https://doi.org/10.1002/cpt.911); [Molden & Jukić, *Front. Pharmacol.* 2021](https://doi.org/10.3389/fphar.2021.650750)).
- **Profile a cancer cohort's genomics with cBioPortal** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 [cBioPortal skill](catalog/tools/cbioportal-database.html) recipe taking a study + gene set through study/profile lookup → per-gene mutation+CNA alteration frequency and co-occurrence/mutual-exclusivity → TMB summary → a Kaplan-Meier overall-survival split by mutation status, with cohort-denominator caveats enforced. Translational Medicine focus-day recipe; cookbook's first cohort-level cancer-genomics recipe, cross-linked to the gene-centric [target dossier](recipes/items/build-target-dossier.html), single-variant [variant-interpretation](recipes/items/interpret-clinical-variant.html), and adjusted-modelling [survival recipe](recipes/items/fit-survival-model-to-clinical-outcomes.html). `Reported` — the cBioPortal-backed AI-HOPE conversational-agent family documents the assembly class ([AI-HOPE-WNT, *Front. Artif. Intell.* 2025](https://pubmed.ncbi.nlm.nih.gov/40860720/), recapitulating WNT-EOCRC survival p=0.0167/0.0007; [AI-HOPE-TP53, *Cancers* 2025](https://pubmed.ncbi.nlm.nih.gov/40940961/)).

### Verified (no changes)

- **Build a target dossier** and **Draft a Phase 2/3 clinical-trial protocol** — linked catalog tools and key sources re-checked, `last_verified` bumped to 2026-06-14.
- **Assemble a tissue reference atlas from the CELLxGENE Census** — linked catalog tools (cellxgene-census, scvi-tools, scanpy, anndata) and Census/scvi-hub sources re-checked, `last_verified` bumped to 2026-06-14.

## 2026-06-13

### Added

- **Infer cell-cell communication from single-cell RNA-seq** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [LIANA-MCP](catalog/tools/liana-mcp.html) recipe taking an annotated AnnData object through `ls_ccc_method` → multi-method `communicate` (CellPhoneDB/Connectome/NATMI/SingleCellSignalR) → `rank_aggregate` consensus ligand-receptor tetrads → `circle_plot`/`ccc_dotplot`, consuming the annotated object from the [scRNA-seq QC recipe](recipes/items/qc-single-cell-rna-seq.html). Molecular and Cellular Biology focus-day recipe; cookbook's first cell-cell-communication recipe. `Proposed` — no documented LLM-driven LIANA-MCP assembly; grounded in [Dimitrov et al., *Nat. Commun.* 13:3735 (2022)](https://doi.org/10.1038/s41467-022-30755-0), a 2026 consensus-LIANA application ([Wei et al., *PLOS ONE* 2026](https://doi.org/10.1371/journal.pone.0345045)), and the method-disagreement benchmark ([Xie et al., *Biomolecules* 13:1211 (2023)](https://doi.org/10.3390/biom13081211)).
- **Call peaks and find enriched motifs from ChIP-seq or ATAC-seq** (Problem class: Data analysis; Evidence: Proposed) — rung-3 toolbelt chaining the [MACS3 skill](catalog/tools/macs3-peak-calling.html) (`callpeak`, narrow/broad mode → narrowPeak BED) into the [HOMER skill](catalog/tools/homer-motif-analysis.html) (`annotatePeaks.pl` nearest-gene context + `findMotifsGenome.pl` de-novo/known motif enrichment). Molecular and Cellular Biology focus-day recipe; the binding-site/motif companion to the [deepTools signal-profiling recipe](recipes/items/profile-chipseq-atacseq-signal-around-features.html), which deliberately stops before peak calling. `Proposed` — no documented LLM-driven MACS3→HOMER assembly; grounded in the field-standard pipeline ([Zhang et al., *Genome Biol.* 9:R137 (2008)](https://doi.org/10.1186/gb-2008-9-9-r137); [Heinz et al., *Mol. Cell* 38:576 (2010)](https://doi.org/10.1016/j.molcel.2010.05.004)).
- **Analyze an existing MD trajectory for stability, flexibility, and contacts** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [MDAnalysis skill](catalog/tools/mdanalysis-trajectory.html) recipe taking a finished GROMACS/AMBER/NAMD trajectory through a load-and-sanity-check → aligned RMSD/RMSF/Rg → interface contact map + H-bond occupancy → backbone PCA battery, with the [MDTraj skill](catalog/tools/mdtraj-trajectory-analysis.html) as the DSSP/Ramachandran fallback. Integrative Structural and Computational Biology focus-day recipe; the post-simulation-analysis companion to the [GROMACS setup recipe](recipes/items/set-up-protein-md-simulation-in-gromacs.html). `Proposed` — no documented LLM-driven MDAnalysis-skill assembly; grounded in [Michaud-Agrawal et al., *J. Comput. Chem.* 32:2319 (2011)](https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.21787), [McGibbon et al., *Biophys. J.* 109:1528 (2015)](https://doi.org/10.1016/j.bpj.2015.08.015), and class-level agentic-MD evidence ([MDCrow, *Mach. Learn. Sci. Technol.* 2025](https://iopscience.iop.org/article/10.1088/2632-2153/ae4b07)).
- **Scan a therapeutic antibody for glycosylation sites** (Problem class: Experimental design; Evidence: Proposed) — rung-2 [Glycoengineering skill](catalog/tools/glycoengineering.html) recipe taking heavy/light-chain sequences through N-X-S/T sequon detection (flagging Fc Asn-297 vs unintended variable-domain sites) → O-glycosylation hotspot prediction → a parent-vs-variant sequon diff, with optional minimal site-knockout edit suggestions. Immunology and Microbiology focus-day recipe; cookbook's first antibody-developability / glycosylation recipe. `Proposed` — no documented LLM-driven glycoengineering-skill assembly; grounded in 2026 Fc-glycan/ADCC literature ([Shuang et al., *mAbs* 2026](https://doi.org/10.1080/19420862.2026.2657099); [Illés 2026](https://doi.org/10.18071/isz.79.0131)) and the galactosylation-as-CQA reference ([Klingler et al., *Biotechnol. Bioeng.* 2024](https://doi.org/10.1002/bit.28616)).
- **Compute a bacterial pan-genome from a set of genome assemblies** (Problem class: Data analysis; Evidence: Proposed) — rung-3 toolbelt chaining the [Bakta skill](catalog/tools/bakta-genome-annotation.html) (identical per-genome annotation → GFF3) into the [Roary skill](catalog/tools/roary-pangenome.html) (CD-HIT/BLAST/MCL clustering → core/soft-core/shell/cloud partition, `gene_presence_absence.csv`, and a `core_gene_alignment.aln` that feeds the [phylogenetics recipe](recipes/items/build-phylogenetic-tree-from-sequences.html)). Immunology and Microbiology focus-day recipe; cookbook's first comparative-genomics / pan-genome recipe. `Proposed` — no documented LLM-driven Bakta→Roary assembly; grounded in the field-standard pipeline ([Page et al., *Bioinformatics* 2015](https://doi.org/10.1093/bioinformatics/btv421); [Schwengers et al., *Microb. Genom.* 2021](https://doi.org/10.1099/mgen.0.000685)) and a 2025 27,884-genome application ([Sholeh et al., *Mol. Genet. Genomics* 2025](https://doi.org/10.1007/s00438-025-02265-3)).

### Verified (no changes)

- 35 recipes spot-checked; all `last_verified` dates within the 30-day window, no aging recipes due.

## 2026-06-11

### Added

- **Profile ChIP-seq or ATAC-seq signal around genomic features** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [deepTools skill](catalog/tools/deeptools.html) recipe taking aligned ChIP-seq/ATAC-seq BAMs through `bamCoverage` BPM-normalized bigWig generation → `multiBamSummary` + `plotCorrelation` replicate QC → `computeMatrix` + `plotHeatmap`/`plotProfile` TSS/peak-centered visualization, with upstream BAM handling via the [pysam skill](catalog/tools/pysam.html). Molecular and Cellular Biology focus-day recipe; cookbook's first ChIP-seq/ATAC-seq coverage-profiling recipe. `Proposed` — no documented LLM-driven deepTools workflow; grounded in [Ramírez et al., *NAR* 44:W160 (2016)](https://doi.org/10.1093/nar/gkw257) plus class-level [Biomni](autonomous-science/systems/biomni.html).
- **Predict gene-knockout phenotypes with flux balance analysis** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [COBRApy skill](catalog/tools/cobrapy.html) recipe taking a genome-scale SBML model through baseline FBA sanity-check → genome-wide `single_gene_deletion` essentiality ranking → focused `double_gene_deletion` synthetic-lethality screen, with an explicit growth-ratio essentiality threshold. Molecular and Cellular Biology focus-day recipe; cookbook's first constraint-based metabolic-modelling recipe. `Proposed` — no documented LLM-driven COBRApy workflow; grounded in [Ebrahim et al., *BMC Syst. Biol.* 7:74 (2013)](https://doi.org/10.1186/1752-0509-7-74) and [Orth et al., *Nat. Biotechnol.* 28:245 (2010)](https://doi.org/10.1038/nbt.1614), plus class-level [Biomni](autonomous-science/systems/biomni.html).

### Verified (no changes)

- 33 recipes spot-checked; all `last_verified` dates within the 30-day window, no aging recipes due.

## 2026-06-10

### Added

- **Score point mutations for functional impact with a protein language model** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [ESM skill](catalog/tools/esm.html) recipe taking a wild-type protein sequence (optionally fetched by UniProt accession via the [gget skill](catalog/tools/gget.html)) and a list of substitutions through masked-marginal log-likelihood-ratio scoring → a ranked tolerated/deleterious CSV, with a wt-marginal one-pass variant for full single-mutation landscapes. Integrative Structural and Computational Biology focus-day recipe; cookbook's first zero-shot variant-effect / protein-fitness recipe and the database-free complement to the [clinical-variant interpretation](recipes/items/interpret-clinical-variant.html) recipe. `Proposed` — no documented LLM-driven ESM-skill scoring assembly; grounded in the canonical zero-shot method [Meier et al., *NeurIPS* 2021](https://www.biorxiv.org/content/10.1101/2021.07.09.450648v1.full), the [ProteinGym benchmark](https://pmc.ncbi.nlm.nih.gov/articles/PMC10723403/), and 2025 directed-evolution use [Zhang et al., *Nat. Commun.* 2025](https://doi.org/10.1038/s41467-025-56751-8).

### Verified (no changes)

- 31 recipes spot-checked; all `last_verified` dates within the 30-day window, no aging recipes due.

## 2026-06-09

### Added

- **Build a phylogenetic tree from a set of sequences** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [Phylogenetics skill](catalog/tools/phylogenetics.html) recipe taking a FASTA of homologous sequences (viral genomes, microbial marker genes, protein families) through MAFFT `--auto` alignment → gap-column trimming → IQ-TREE 2 ModelFinder + ultrafast-bootstrap maximum-likelihood inference → midpoint/outgroup rooting → an ETE3-annotated tree figure, handing the Newick off to the [ETE Toolkit](catalog/tools/etetoolkit.html) and the [16S diversity](recipes/items/compute-16s-microbiome-diversity.html) recipe (which consumes the rooted tree for UniFrac). Immunology and Microbiology focus-day recipe; cookbook's first phylogenetics / tree-building recipe. `Proposed` — no documented LLM-driven phylogenetics workflow; grounded in the field-standard tool references [Katoh & Standley, *MBE* 30:772 (2013)](https://doi.org/10.1093/molbev/mst010), [Minh et al., *MBE* 37:1530 (2020)](https://doi.org/10.1093/molbev/msaa015), [Kalyaanamoorthy et al., *Nat. Methods* 14:587 (2017)](https://doi.org/10.1038/nmeth.4285), and [Hoang et al., *MBE* 35:518 (2018)](https://doi.org/10.1093/molbev/msx281), plus class-level [Biomni](https://doi.org/10.1101/2025.05.30.656746).

### Updated

- **Estimate pharmacokinetic properties of a small molecule** — promoted `Proposed` → `Reported` on the first field report (issue #12). A user ran the full three-layer assembly through to a finished PK card and captured it in a standalone `pk_card.py`, verified across caffeine, ibuprofen, quercetin, and terfenadine. Added a **Field reports** subsection under **Evidence** and refreshed `last_verified` to 2026-06-09.

### Verified (no changes)

- 3 recipes spot-checked (oldest `last_verified` first), all current; `last_verified` bumped to 2026-06-09: [Scan approved drugs for repurposing candidates against a disease](recipes/items/scan-drug-repurposing-candidates.html), [Profile a compound's polypharmacology from ChEMBL bioactivity data](recipes/items/profile-compound-polypharmacology.html), [Triage an AlphaFold model for structure-based drug design](recipes/items/triage-alphafold-model-for-docking.html). All linked catalog pages resolve and are unflagged; source DOIs stable.

### User requests

- **#12 @goodb** — resolved. This entry had been stuck open since 2026-05-27 because the responder emitted no machine-readable trailer, so the request content lived only in the GitHub issue body — which the sandboxed curator agent (no `gh`/shell) could not read, leaving it "un-actionable" on every retry. Fixed at the source: the `recipes.yml` / `curate.yml` workflows now pre-fetch open user-request issue bodies into `.request-bodies/<NN>.md` before the agent runs, the responder fallback now rebuilds a structured queue entry from the issue-form fields, and `RECIPE_AGENT.md` / `AGENT.md` point the agent at the pre-fetched files instead of a `gh issue view` it can't run.

## 2026-06-08

### Added

- **Identify an unknown compound from an MS/MS spectrum** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [matchms skill](catalog/tools/matchms.html) recipe taking experimental tandem-MS spectra plus a reference library (GNPS / MassBank / in-house `.msp`) through format import → peak cleaning and metadata harmonization → modified-cosine scoring with precursor-m/z gating → a ranked candidate-identity CSV, handing confirmed InChIKeys off to the [PubChem MCP](catalog/tools/pubchem.html) and the [polypharmacology](recipes/items/profile-compound-polypharmacology.html) recipe. Chemistry focus-day recipe; cookbook's first metabolomics / spectral-library-matching recipe. `Proposed` — no documented LLM-driven matchms workflow; grounded in the canonical library paper [Huber et al., *JOSS* 5(52):2411 (2020)](https://doi.org/10.21105/joss.02411) plus methodological anchors [Onoprishvili et al., *Bioinformatics* (2025)](https://doi.org/10.1093/bioinformatics/btaf081) (SimMS) and [Xing et al., *Anal. Chem.* (2025)](https://doi.org/10.1021/acs.analchem.5c02047) (enhanced reverse spectral search).

### Verified (no changes)

- Aging-recipe sweep: oldest `last_verified` is 2026-05-24 (15 days), within the 30-day window — no recipes due for re-verification this run.

### User requests

- **#12 (@goodb)** — still no `gh` permission to read the issue body from this run; left open for next-run retry.

## 2026-06-07

### Added

- **Enumerate analogs around a lead compound for SAR expansion** (Problem class: Hypothesis generation; Evidence: Proposed) — rung-2 [Datamol skill](catalog/tools/datamol.html) recipe taking a lead SMILES through standardization → tautomer / stereoisomer enumeration → single-point fragment-substitution scan → ECFP4 Tanimoto + QED scoring → a deduplicated SAR-expansion CSV, with explicit handoff to the [VS-hit-filtering](recipes/items/filter-virtual-screening-hits.html) developability gate and the [polypharmacology](recipes/items/profile-compound-polypharmacology.html) bioactivity lookup. Drug Repurposing and Discovery focus-day recipe; cookbook's first dedicated analog-enumeration / lead-optimisation recipe and the natural upstream of the existing hit-filtering recipe; cookbook's second `Hypothesis generation` recipe. `Proposed` — no documented LLM-driven Datamol enumeration workflow; closest grounding is the K-Dense rdkit→datamol→medchem [lead-optimisation workflow](https://github.com/K-Dense-AI/scientific-agent-skills) plus the underlying primitives [Rogers & Hahn, *JCIM* 50:742 (2010)](https://doi.org/10.1021/ci100050t) (ECFP/Tanimoto), [Bickerton et al., *Nat. Chem.* 4:90 (2012)](https://doi.org/10.1038/nchem.1243) (QED), and [Griffen et al., *J. Med. Chem.* 54:7739 (2011)](https://doi.org/10.1021/jm200452d) (matched molecular pairs).

### Updated

- Nav orders rebalanced to keep alphabetical title ordering after the new addition. "Enumerate analogs…" inserted at 10; everything from "Estimate pharmacokinetic properties" downward shifted +1 (Estimate → 11, Filter VS hits → 12, Infer GRN → 13, Integrate single-cell → 14, Interpret variant → 15, Match patient → 16, Organize DICOM → 17, Parse FCS → 18, Prioritize targets → 19, Profile polypharmacology → 20, Run bulk RNA-seq → 21, Run first-pass QC → 22, Run functional enrichment → 23, Scan repurposing → 24, Set up MD → 25, Sort spikes → 26, Triage preprints → 27, Triage AlphaFold → 28, Fit survival → 29, Scan adverse events → 30).

### Verified (no changes)

- 29 existing recipes spot-checked; none past the 30-day `last_verified` window (oldest is 2026-05-24, `profile-compound-polypharmacology`), so no re-verification was due this run.

## 2026-06-06

### Added

- **Fit a survival model to censored clinical outcomes** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [scikit-survival skill](catalog/tools/scikit-survival.html) recipe taking a tidy covariate table plus a `(time, event)` outcome through structured-`Surv` encoding → Kaplan-Meier + log-rank → Cox PH (with a proportional-hazards check) → Random Survival Forest → cross-validated Harrell's c-index → risk-group stratification. First Translational Medicine focus-day recipe of this run; cookbook's first dedicated time-to-event / prognosis recipe. `Proposed` — no documented end-to-end LLM-driven `sksurv` workflow; closest grounding is the library reference [Pölsterl, *JMLR* 21(212):1–6 (2020)](https://jmlr.org/papers/v21/20-729.html) and recent RSF-vs-nomogram prognosis studies [Zhang et al., *Transl. Cancer Res.* (2026)](https://doi.org/10.21037/tcr-2025-aw-2462) and [Liu et al., *Medicine* (2026)](https://doi.org/10.1097/MD.0000000000048757).
- **Scan adverse-event reports for a drug-safety signal** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-2 [OpenFDA MCP](catalog/tools/openfda.html) recipe taking a drug name through generic-name resolution → FAERS top-reaction ranking → structured label / warning pull → label-vs-FAERS cross-check → an honest "reports, not rates" framing. Second Translational Medicine focus-day recipe of this run; promoted from the `Deferred — next-run priority` list; cookbook's first pharmacovigilance recipe. `Proposed` — no documented attempt of this exact MCP assembly; openFDA/FAERS is the canonical public pharmacovigilance source and the server wraps it faithfully.

### Verified (no changes)

- 27 existing recipes spot-checked; none past the 30-day `last_verified` window (oldest is 2026-05-24), so no re-verification was due this run.

## 2026-06-05

### Added

- **Organize a raw DICOM dataset into a BIDS layout** (Problem class: Workflow automation; Evidence: Proposed) — rung-2 [BIDS Claude Skill](catalog/tools/bids.html) recipe taking a directory of vendor DICOMs through series-level inventory → HeuDiConv heuristic (or dcm2bids config) drafting → single-subject `--dry-run` audit → cohort conversion via `dcm2niix` → top-level `dataset_description.json` / `participants.tsv` / sidecar authoring → `bids-validator` triage → PyBIDS post-conversion query, with explicit `IntendedFor` cross-link logic for fieldmaps. First Neuroscience focus-day recipe of this run; promoted from the `Deferred — next-run priority` list. Cookbook's first imaging-side data-organization recipe — counterpart to the existing [Discover NWB recordings on DANDI](recipes/items/discover-nwb-recordings-on-dandi.html) electrophysiology discovery recipe. `Proposed` because no documented end-to-end LLM-driven DICOM→BIDS workflow exists in last-24-months peer-reviewed or preprint literature; closest component-level grounding is [Gorgolewski et al., *Sci. Data* 3:160044 (2016)](https://doi.org/10.1038/sdata.2016.44) and [Poldrack et al., *Imaging Neuroscience* 2:1–19 (2024)](https://doi.org/10.1162/imag_a_00103) (BIDS spec evolution); [Yarkoni et al., *JOSS* 4(40):1294 (2019)](https://doi.org/10.21105/joss.01294) (PyBIDS); [Zwiers, Moia, Oostenveld, *Front. Neuroinform.* 15:770608 (2022)](https://doi.org/10.3389/fninf.2021.770608) (BIDScoin); and [Wulms et al., *Sci. Data* 10:673 (2023)](https://doi.org/10.1038/s41597-023-02583-4) (BIDSconvertR).

### Updated

- Nav orders rebalanced to keep alphabetical title ordering after the new addition and to fix a stale collision between **Run first-pass QC** and **Run functional enrichment** (both stamped 20). "Organize a raw DICOM dataset…" inserted at 16; everything from "Parse FCS…" downward shifted by +1, with **Run first-pass QC** at 21 and **Run functional enrichment** at 22: **Parse FCS flow-cytometry files** → 17, **Prioritize targets** → 18, **Profile polypharmacology** → 19, **Run bulk RNA-seq DE** → 20, **Run first-pass QC** → 21, **Run functional enrichment** → 22, **Scan repurposing** → 23, **Set up protein MD** → 24, **Sort spikes** → 25, **Triage preprints** → 26, **Triage AlphaFold** → 27.

### Verified (no changes)

- No aging recipes due — every `last_verified` date is within the 30-day window. The verification floor sits at 2026-05-24 (`scan-drug-repurposing-candidates`); next aging boundary is 2026-06-23.

### User requests

- **#12 @goodb** — still cannot access the issue body (no `gh` permission for the repo in this run); leaving open in `recipes/curator-state.md` for the next run with `gh` access.

## 2026-06-04

### Added

- **Run functional enrichment on a gene list** (Problem class: Data analysis; Evidence: Reported) — rung-2 [gget skill](catalog/tools/gget.html) recipe taking a list of gene symbols through `gget enrichr` against GO BP, KEGG, Reactome, MSigDB Hallmark, and DisGeNET → per-library CSV → grounded natural-language summary with explicit verification pass against the saved tables and a random-gene negative-control step. First Molecular and Cellular Biology focus-day recipe of this run; the cookbook's first dedicated functional-enrichment / pathway-interpretation recipe and the natural downstream step after [bulk RNA-seq DE](recipes/items/run-bulk-rnaseq-differential-expression.html). `Reported` evidence anchored in [Wang et al., *GeneAgent*, *Nature Methods* 22:1677, 2025](https://doi.org/10.1038/s41592-025-02748-6) — self-verification against Enrichr and curated databases lifts ROUGE-L on MSigDB from 0.239±0.038 (GPT-4) to 0.310±0.047 (GeneAgent) across 1,106 gene sets, with 84% of 15,848 claims database-supported and 92% of self-verification decisions correct on a 132-claim expert-judged sample; complementary anchors [Hu et al., *Nat. Methods* 21:2353, 2024](https://doi.org/10.1038/s41592-024-02525-x) and [Joshi et al., *llm2geneset* (bioRxiv 2024-11-12)](https://doi.org/10.1101/2024.11.11.621189).

### Verified (no changes)

- 5 recipes spot-checked, `last_verified` bumped to 2026-06-04 — every linked catalog page resolves, every source URL still loads: [Sort spikes from a Neuropixels recording end-to-end](recipes/items/sort-spikes-from-neuropixels-recording.html), [Integrate multiple single-cell RNA-seq datasets across batches](recipes/items/integrate-single-cell-datasets.html), [Interpret a clinical variant from a natural-language query](recipes/items/interpret-clinical-variant.html), [Match a patient summary to recruiting clinical trials](recipes/items/match-patient-to-clinical-trials.html), [Filter a virtual screening hit list with drug-likeness rules and structural alerts](recipes/items/filter-virtual-screening-hits.html). Fixed one stale `.md` link → `.html` in the filter-virtual-screening recipe (RDKit-MCP cross-reference).

### User requests

- **#12 @goodb** — still cannot access the issue body (no `gh` permission in this run); leaving open in `recipes/curator-state.md` for the next run with `gh` access.

## 2026-06-03

### Added

- **Dock a ligand library into a target structure with DiffDock** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [DiffDock skill](catalog/tools/diffdock.html) recipe taking a PDB or AlphaFold target + ligand SMILES CSV through batch-CSV prep → diffusion sampling (20–40 samples/complex) → confidence-thresholded filtering (`> 0` trustworthy, −1.5–0 inspect, < −1.5 drop) → top-K SDF export, with explicit handoffs to [MedChem](catalog/tools/medchem.html) / [DeepChem](catalog/tools/deepchem.html) / [molecular-dynamics](catalog/tools/molecular-dynamics.html) downstream. First Integrative Structural and Computational Biology focus-day recipe of this run; cookbook's first dedicated docking recipe and natural downstream of the existing [AlphaFold triage](recipes/items/triage-alphafold-model-for-docking.html) recipe. `Proposed` because no documented end-to-end LLM-orchestrated DiffDock virtual screen exists; closest component-level evidence is [Corso et al., DiffDock-L (ICLR 2024, arXiv:2402.18396)](https://arxiv.org/abs/2402.18396) (38%→80% RMSD<2Å on top one-third by confidence), [Buttenschoen et al., PoseBusters (*Chem. Sci.* 15:3130, 2024)](https://doi.org/10.1039/D3SC04185A), and [Karelina et al., AF2-target docking (*JCIM* 63:6219, 2023)](https://doi.org/10.1021/acs.jcim.3c00601) (~21% RMSD<2Å on AF2 models, motivating the upstream-triage gate in step 2).

### Updated

- Nav orders rebalanced to keep alphabetical title ordering after the new addition. "Dock a ligand library…" inserted at 8; everything from "Draft Phase 2/3…" downward shifted by +1: **Draft Phase 2/3 clinical-trial protocol** → 9, **Estimate PK** → 10, **Filter virtual screening** → 11, **Infer GRN** → 12, **Integrate single-cell** → 13, **Interpret clinical variant** → 14, **Match patient to trials** → 15, **Parse FCS flow-cytometry files** → 16, **Prioritize targets** → 17, **Profile polypharmacology** → 18, **Run bulk RNA-seq DE** → 19, **Run first-pass QC** → 20, **Scan repurposing** → 21, **Set up protein MD** → 22, **Sort spikes** → 23, **Triage preprints** → 24, **Triage AlphaFold** → 25.

### Verified (no changes)

- No aging recipes due — every `last_verified` date is within the 30-day window. The recipe set's verification floor sits at 2026-05-22 (`integrate-single-cell-datasets`, `sort-spikes-from-neuropixels-recording`); next aging boundary is 2026-06-21.

### User requests

- **#12 @goodb** — still cannot access the issue body (no `gh` permission for the repo in this run); leaving the request open in `recipes/curator-state.md` for the next run with `gh` access.

## 2026-06-02

### Added

- **Compute 16S microbiome alpha/beta diversity from a BIOM table** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [scikit-bio skill](catalog/tools/scikit-bio.html) recipe taking a BIOM feature table + sample metadata + Newick tree through rarefaction → Shannon/Simpson/Faith's PD → weighted/unweighted UniFrac → PCoA → PERMANOVA with explicit grouping-column and permutation-count flags. First Immunology and Microbiology focus-day recipe of this run; cookbook's first dedicated microbiome / community-ecology recipe. `Proposed` because no documented end-to-end attempt of this exact assembly exists; closest class-level evidence is [Huang et al. *Biomni* (bioRxiv 2025.05.30.656746)](https://doi.org/10.1101/2025.05.30.656746) whose published benchmark includes microbiome disease-taxa bioinformatics across five datasets (HMP, MetaPhlAn2 human metagenomics, drinking-water OTU matrices) at ~4× over base-LLM accuracy.
- **Parse FCS flow-cytometry files for downstream immunophenotyping** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [FlowIO skill](catalog/tools/flowio.html) recipe taking a directory of vendor-emitted FCS 2.0/3.0/3.1 files through `FlowData` parsing → per-file metadata harvest → scatter/fluorescence/time channel categorisation → optional log/gain transforms → concatenated long-format events Parquet, with explicit failure surfacing for partial-acquisition files. Second Immunology and Microbiology focus-day recipe; cookbook's first cytometry / FCS recipe. `Proposed` because no documented end-to-end attempt of this exact assembly exists; closest class-level evidence is ["Enhancing Clinical Workflow Efficiency in Flow Cytometry Reporting with LLMs" (PMC13053331, *J. Clin. Immunol.* 2026)](https://pubmed.ncbi.nlm.nih.gov/?term=PMC13053331), which demonstrates pathologist-level accuracy of fine-tuned LLMs on the downstream report-generation step the parsed-events output feeds into.

### Updated

- Nav orders rebalanced to keep alphabetical title ordering after the two additions: **Assemble Census atlas** → 1, **Benchmark ADMET** → 2, **Build target dossier** → 3, **Compute 16S microbiome diversity** → 4 (new), **Compute HRV** → 5, **Convert instrument data** → 6, **Discover NWB on DANDI** → 7, **Draft Phase 2/3 clinical-trial protocol** → 8, **Estimate PK** → 9, **Filter virtual screening** → 10, **Infer GRN** → 11, **Integrate single-cell** → 12, **Interpret clinical variant** → 13, **Match patient to trials** → 14, **Parse FCS flow-cytometry files** → 15 (new), **Prioritize targets** → 16, **Profile polypharmacology** → 17, **Run bulk RNA-seq DE** → 18, **Run first-pass QC** → 19, **Scan repurposing** → 20, **Set up protein MD** → 21, **Sort spikes** → 22, **Triage preprints** → 23, **Triage AlphaFold** → 24.

### Verified (no changes)

- No aging recipes due — every `last_verified` date is within the 30-day window. The recipe set's verification floor sits at 2026-05-22 (`integrate-single-cell-datasets`, `sort-spikes-from-neuropixels-recording`); next aging boundary is 2026-06-21.

### User requests

- **#12** (`claude:recipe-feedback`) — remains in `## User requests (open)`; `gh` CLI is still not available in this run's environment so the issue body cannot be inspected. Retry next run with `gh` access.

## 2026-06-01

### Added

- **Convert raw analytical instrument data to Allotrope ASM JSON** (Problem class: Workflow automation; Evidence: Reported) — rung-2 [instrument-data-to-allotrope skill](catalog/tools/instrument-data-to-allotrope.html) recipe taking a vendor-format file (cell counter, plate reader, HPLC, MS, qPCR) through auto-detect → `allotropy` native parse → ASM JSON-LD + flattened CSV + exportable Python parser, with strict-validation of the raw-vs-derived split before LIMS / data-lake handoff. First Chemistry focus-day recipe of this run; cookbook's first workflow-automation recipe spanning the Anthropic life-sciences plugin family. Anchored in the [Claude for Life Sciences launch (October 2025)](https://www.anthropic.com/news/claude-for-life-sciences), the [Anthropic Vi-CELL tutorial](https://claude.com/resources/tutorials/getting-started-with-claude-for-life-sciences), and the underlying [`Benchling-Open-Source/allotropy`](https://github.com/Benchling-Open-Source/allotropy) reference parser.
- **Set up a protein molecular dynamics simulation in GROMACS from a PDB ID** (Problem class: Experimental design; Evidence: Proposed) — rung-2 [molecule-mcp](catalog/tools/molecule-mcp.html) recipe driving the GROMACS Copilot server end-to-end (topology → solvation → ion neutralisation → minimisation → NVT/NPT → 50 ns production → RMSD/RMSF/Rg) with explicit force-field / water-model / GPU-offload flags. Second Chemistry focus-day recipe; first cookbook entry exercising the GROMACS path of the molecule-mcp bundle. `Proposed` because no documented end-to-end attempt of this exact assembly exists; closest peer-reviewed class-level evidence is [MDCrow (Campbell et al., *Mach. Learn. Sci. Technol.* 2025, DOI:10.1088/2632-2153/ae4b07)](https://iopscience.iop.org/article/10.1088/2632-2153/ae4b07) — OpenMM rather than GROMACS but same architecture — plus GROMACS-supporting follow-ons [DynaMate (arXiv:2512.10034)](https://arxiv.org/abs/2512.10034) and [NAMD-Agent (arXiv:2507.07887)](https://arxiv.org/abs/2507.07887), and the [MDGym benchmark (arXiv:2605.08941)](https://arxiv.org/abs/2605.08941) as a reality check (Claude Code / Codex / OpenHands all solve <21% of easy GROMACS/LAMMPS tasks).

### Updated

- Nav orders rebalanced to restore strict alphabetical title ordering after the two additions and to correct two prior off-by-many drifts (Benchmark ADMET was at 20 instead of 2; Prioritize Targets was at 19 instead of 14): **Assemble Census atlas** → 1, **Benchmark ADMET** → 2, **Build target dossier** → 3, **Compute HRV** → 4, **Convert instrument data** → 5 (new), **Discover NWB on DANDI** → 6, **Draft a Phase 2/3 clinical-trial protocol** → 7, **Estimate PK** → 8, **Filter virtual screening** → 9, **Infer GRN** → 10, **Integrate single-cell** → 11, **Interpret clinical variant** → 12, **Match patient to trials** → 13, **Prioritize targets** → 14, **Profile polypharmacology** → 15, **Run bulk RNA-seq DE** → 16, **QC single-cell** → 17, **Scan repurposing** → 18, **Set up protein MD in GROMACS** → 19 (new), **Sort spikes** → 20, **Triage preprints** → 21, **Triage AlphaFold** → 22.
- `recipes/curator-state.md` — `## Missing components` entry for "DeepChem (K-Dense Skill)" removed; DeepChem is now catalogued at [`catalog/tools/deepchem.md`](catalog/tools/deepchem.html).

### Verified (no changes)

- No aging recipes due — every `last_verified` date is within the 30-day window. The recipe set's verification floor sits at 2026-05-22 (`integrate-single-cell-datasets`, `sort-spikes-from-neuropixels-recording`); next aging boundary is 2026-06-21.

### User requests

- **#12** (`claude:recipe-feedback`) — remains in `## User requests (open)`; `gh` CLI is still not available in this run's environment so the issue body cannot be inspected. Retry next run with `gh` access.

## 2026-05-31

### Added

- **Prioritize targets within a disease via Open Targets** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 [Open Targets plugin](catalog/tools/open-targets.html) recipe taking a disease (EFO/MONDO) to a ranked target shortlist across the four prioritisation pillars (precedence, tractability, doability, safety) with cited GraphQL fields per cell. First DR&D focus-day recipe of this run; complements the existing gene-in [Build a target dossier](recipes/items/build-target-dossier.html) and disease-in/drug-out [Scan approved drugs for repurposing candidates](recipes/items/scan-drug-repurposing-candidates.html) recipes. Anchored in [Buniello et al. *NAR* 53(D1):D1467–D1475 (2025)](https://doi.org/10.1093/nar/gkae1128) and [Minikel et al. *Nature* 629:624–629 (2024)](https://doi.org/10.1038/s41586-024-07316-0); closest LLM-driven application: [Zunzunegui Sanz et al. *bioRxiv* 2025-06-13](https://doi.org/10.1101/2025.06.13.659527) and [More et al. *npj Precision Oncology* 10:95 (2025)](https://doi.org/10.1038/s41698-025-01265-1).
- **Benchmark an ADMET property with PyTDC** (Problem class: Data analysis; Evidence: Reported) — rung-2 [PyTDC skill](catalog/tools/pytdc.html) recipe driving the official TDC `ADMET_Group` benchmark (frozen scaffold splits, canonical metric per task, 5-seed leaderboard row format) so a new model gets a directly comparable number. Second DR&D focus-day recipe; first cookbook entry that produces leaderboard-comparable ADMET metrics. Anchored in [Huang et al. *NeurIPS Datasets and Benchmarks* (2021)](https://arxiv.org/abs/2102.09548), the published TDC-2 framework [Velez-Arce et al. NeurIPS 2024](https://openreview.net/forum?id=kL8dlYp6IM), and recent LLM-driven workflows ([Hao et al. *Scientific Data* 11:864 (2024)](https://doi.org/10.1038/s41597-024-03793-0); [Yuan et al. arXiv:2406.06316 (2024)](https://arxiv.org/abs/2406.06316)).

### Verified (no changes)

- No aging recipes due — every `last_verified` date is within the 30-day window. The recipe set's verification floor sits at 2026-05-22 (`integrate-single-cell-datasets`, `sort-spikes-from-neuropixels-recording`); next aging boundary is 2026-06-21.

### User requests

- **#12** (`claude:recipe-feedback`) — remains in `## User requests (open)`; `gh` CLI is still not available in this run's environment so the issue body cannot be inspected. Retry next run with `gh` access.

## 2026-05-30

### Added

- **Draft a Phase 2/3 clinical-trial protocol from an indication brief** (Problem class: Manuscript prep; Evidence: Reported) — rung-2 [`clinical-trial-protocol`](catalog/tools/clinical-trial-protocol.html) Anthropic Healthcare plugin recipe that walks an indication / endpoint paragraph through the four-waypoint flow — regulatory classification, ClinicalTrials.gov competitive landscape, sample-size calculation, FDA/NIH-template drafting — emerging with a reviewable draft Phase 2/3 protocol scaffold. First Translational Medicine focus-day recipe of the new run; resolves a previously deferred candidate. Evidence anchored in the [Anthropic plugin tutorial](https://claude.com/resources/tutorials/how-to-use-the-clinical-trial-protocol-draft-generation-sample-skill-with-claude) (Claude for Healthcare launch, January 2026) and class-level validation in [Markey et al. *Clinical Trials* 2025](https://journals.sagepub.com/home/ctj) (80% content relevance, >99% terminology accuracy with RAG), [Shin et al. *Clinical Pharmacology & Therapeutics* 2026](https://ascpt.onlinelibrary.wiley.com/journal/15326535) (100% accuracy on disease/intervention/comparator extraction, 14/15 trials for sample-size identification), [Hauptman et al. *JMIR Dermatology* 2026](https://derma.jmir.org/), and [Maleki, *arXiv* 2404.05044 (2024)](https://arxiv.org/abs/2404.05044).

### Updated

- Nav orders rebalanced across the recipe set to keep alphabetical ordering after the addition: **Assemble Census atlas** → 1, **Build target dossier** → 2, **Compute HRV** → 3, **Discover NWB on DANDI** → 4, **Draft a Phase 2/3 clinical-trial protocol** → 5 (new), **Estimate PK** → 6, **Filter virtual screening** → 7, **Infer GRN** → 8, **Integrate single-cell** → 9, **Interpret clinical variant** → 10, **Match patient to trials** → 11, **Profile polypharmacology** → 12, **Run bulk RNA-seq DE** → 13, **QC single-cell** → 14, **Scan repurposing** → 15, **Sort spikes** → 16, **Triage preprints** → 17, **Triage AlphaFold** → 18.

### Verified (no changes)

- No aging recipes due — every `last_verified` date is within the 30-day window. The recipe set's verification floor sits at 2026-05-22 (`integrate-single-cell-datasets`, `sort-spikes-from-neuropixels-recording`); next aging boundary is 2026-06-21.

### User requests

- **#12** (`claude:recipe-feedback`) — remains in `## User requests (open)`; `gh` CLI is still not available in this run's environment so the issue body cannot be inspected. Retry next run with `gh` access.

## 2026-05-29 (second pass — Neuroscience directed)

### Added

- **Discover NWB recordings on DANDI and prepare them for sorting** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-3 [Neurosift Tools MCP](catalog/tools/neurosift.html) + [neuropixels-analysis skill](catalog/tools/neuropixels-analysis.html) toolbelt taking a semantic query about extracellular recordings to a filtered list of DANDI assets — Claude calls `dandi_semantic_search`, `dandi_search_by_neurodata_type`, `dandiset_assets`, and `nwb_file_info` over the public DANDI API, applies user-supplied hypothesis constraints (probe model, session duration, presence of a `Units` table), and emits `dandi download` / `pynwb` streaming snippets ready for the [Sort spikes from a Neuropixels recording](recipes/items/sort-spikes-from-neuropixels-recording.html) recipe. Third Neuroscience-primary recipe; resolves a previously deferred candidate. Evidence anchored in [Magland, Ly, Rübel, Dichter. *Scientific Data* 12:1988 (2025), doi:10.1038/s41597-025-06285-x](https://doi.org/10.1038/s41597-025-06285-x), which documents an LLM-driven agentic chat assistant and notebook-generation pipeline for DANDI exploration from the same Flatiron lab that ships the Neurosift Tools MCP; reviewed by neurophysiology specialists with most generated notebooks rated "very helpful." Canonical Neurosift citation: [Magland, Soules, Baker, Dichter. *JOSS* 9(97):6590 (2024), doi:10.21105/joss.06590](https://doi.org/10.21105/joss.06590).

### Updated

- Nav orders rebalanced across the recipe set to keep alphabetical ordering after the addition: **Assemble Census atlas** → 1, **Build target dossier** → 2, **Compute HRV** → 3, **Discover NWB on DANDI** → 4, **Estimate PK** → 5, **Filter virtual screening** → 6, **Infer GRN** → 7, **Integrate single-cell** → 8, **Interpret clinical variant** → 9, **Match patient to trials** → 10, **Profile polypharmacology** → 11, **Run bulk RNA-seq DE** → 12, **QC single-cell** → 13, **Scan repurposing** → 14, **Sort spikes** → 15, **Triage preprints** → 16, **Triage AlphaFold** → 17.

### Verified (no changes)

- No aging recipes this run — every `last_verified` date is within the 30-day window. The recipe set's verification floor sits at 2026-05-22 (`integrate-single-cell-datasets`, `sort-spikes-from-neuropixels-recording`); next aging boundary is 2026-06-21.

### User requests

- **#12** (`claude:recipe-feedback`) — remains in `## User requests (open)`; `gh` CLI still unavailable in this run's environment so the issue body cannot be inspected. Retry next run with `gh` access.

## 2026-05-29

### Added

- **Compute HRV from an ECG recording** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [NeuroKit2 Claude skill](catalog/tools/neurokit2.html) recipe taking a single-lead ECG to validated R-peaks plus time-domain, frequency-domain, and non-linear HRV indices, with `nk.signal_quality`-driven epoch exclusion. Second Neuroscience-primary recipe in the cookbook (joins the Neuropixels spike-sorting recipe). Component evidence: [Makowski et al. *Behavior Research Methods* 2021](https://doi.org/10.3758/s13428-020-01516-y) (NeuroKit2 reference) and [Pham et al. *Sensors* 2021](https://doi.org/10.3390/s21123998) (HRV indices tutorial). Closest LLM-orchestrated analogue: [EEGAgent (Yan et al., arXiv:2511.09947, 2025-11-12)](https://arxiv.org/abs/2511.09947), AAAI-26 — different signal modality and custom toolbox, not NeuroKit2.

### Updated

- Nav orders rebalanced across the recipe set to keep alphabetical ordering after the addition: **Assemble Census atlas** → 1, **Build target dossier** → 2, **Compute HRV** → 3, **Estimate PK** → 4, **Filter virtual screening** → 5, **Infer GRN** → 6, **Integrate single-cell** → 7, **Interpret clinical variant** → 8, **Match patient to trials** → 9, **Profile polypharmacology** → 10, **Run bulk RNA-seq DE** → 11, **QC single-cell** → 12, **Scan repurposing** → 13, **Sort spikes** → 14, **Triage preprints** → 15, **Triage AlphaFold** → 16.

### Verified (no changes)

- 4 recipes spot-checked at the 30-day boundary and bumped to `last_verified: 2026-05-29` — **Triage preprints**, **QC single-cell**, **Build target dossier**, **Run bulk RNA-seq DE**. All linked catalog tools (bio-research, pubmed, single-cell-rna-qc, pydeseq2, open-targets, uniprot, alphafold, depmap) remain present and unflagged.

### User requests

- **#12** (`claude:recipe-feedback`) — remains in `## User requests (open)`; `gh` CLI is not available in this run's environment so the issue body still cannot be inspected. Retry on the next run that has `gh` access.

## 2026-05-28

### Added

- **Assemble a tissue reference atlas from the CELLxGENE Census** (Problem class: Data analysis; Evidence: Reported) — rung-2 [cellxgene-census skill](catalog/tools/cellxgene-census.html) recipe pulling a versioned AnnData slice from the CZ CELLxGENE Discover Census with the CZ-trained scVI embedding attached for reference mapping. First Molecular and Cellular Biology focus-day recipe to consume the Census. Evidence anchored in the Census team's [`comp_bio_data_integration_scvi` notebook](https://chanzuckerberg.github.io/cellxgene-census/notebooks/analysis_demo/comp_bio_data_integration_scvi.html), the [scvi-hub paper](https://www.nature.com/articles/s41592-025-02799-9) (Ergen et al., *Nature Methods* 2025), and the [integrated human lung atlas](https://doi.org/10.1038/s41591-023-02327-2) (Sikkema et al., *Nature Medicine* 2023).
- **Infer a gene-regulatory network from single-cell RNA-seq** (Problem class: Data analysis; Evidence: Reported) — rung-2 [Arboreto skill](catalog/tools/arboreto.html) recipe running GRNBoost2 on a QC'd / integrated AnnData with a TF-restricted regressor and seed-stabilised reruns; produces the ranked TF–target edge table that pySCENIC consumes downstream. Evidence anchored in [Moerman et al. *Bioinformatics* 2019](https://doi.org/10.1093/bioinformatics/bty916) (GRNBoost2), [Van de Sande et al. *Nature Protocols* 2020](https://doi.org/10.1038/s41596-020-0336-2) (SCENIC workflow), and [Bravo González-Blas et al. *Nature Methods* 2023](https://doi.org/10.1038/s41592-023-01938-4) (SCENIC+).

### Updated

- Nav orders rebalanced across the recipe set to keep alphabetical ordering after the two additions: **Assemble Census atlas** → 1, **Build target dossier** → 2, **Estimate PK** → 3, **Filter virtual screening** → 4, **Infer GRN** → 5, **Integrate single-cell** → 6, **Interpret clinical variant** → 7, **Match patient to trials** → 8, **Profile polypharmacology** → 9, **Run bulk RNA-seq DE** → 10, **QC single-cell** → 11, **Scan repurposing** → 12, **Sort spikes** → 13, **Triage preprints** → 14, **Triage AlphaFold** → 15.

### Missing components flagged to the catalog curator

- **pySCENIC wrapper (cisTarget + AUCell)** — would unlock the full SCENIC pipeline downstream of the new GRN-inference recipe (motif filtering against cisTarget databases, per-cell regulon AUCell scoring).

### Verified (no changes)

- All 13 pre-existing recipes have `last_verified` within the 30-day window (oldest 2026-05-21); no aging verifications were due this run.

## 2026-05-27

### Added

- **Estimate pharmacokinetic properties of a small molecule** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-3 RDKit + MedChem + ChEMBL assembly producing a descriptor / rule-based / analog-anchored PK card for a single SMILES. Ships in response to user request [#8](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/8). Closest documented analogues: [ChemCrow](https://doi.org/10.1038/s42256-024-00832-8) (Bran et al., *Nature Machine Intelligence* 2024) and [PharmaBench](https://doi.org/10.1038/s41597-024-03731-0) (Niu et al., *Scientific Data* 2024).
- **Triage an AlphaFold model for structure-based drug design** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-2 [AlphaFold MCP](catalog/tools/alphafold.html) recipe producing a pLDDT-anchored go/refine/fall-back-to-PDB verdict on a UniProt accession. First Integrative Structural and Computational Biology-primary recipe. Evidence grounded in the EBI AlphaFold DB papers ([Varadi 2022](https://doi.org/10.1093/nar/gkab1061), [Varadi 2024](https://doi.org/10.1093/nar/gkad1011)), the interface-pLDDT benchmark ([Bryant 2022](https://doi.org/10.1038/s41467-022-28865-w)), and the AlphaFold-for-docking assessment ([Karelina 2023](https://doi.org/10.1021/acs.jcim.3c00601)).

### Updated

- Nav orders rebalanced across the recipe set to keep alphabetical ordering after the two additions: **Estimate PK properties** → 2, **Filter virtual screening hits** → 3, **Integrate single-cell datasets** → 4, **Interpret clinical variant** → 5, **Match patient to trials** → 6, **Profile polypharmacology** → 7, **Run bulk RNA-seq DE** → 8, **QC single-cell RNA-seq** → 9, **Scan repurposing candidates** → 10, **Sort spikes** → 11, **Triage preprints** → 12, **Triage AlphaFold model** → 13.

### Missing components flagged to the catalog curator

- **ADMET-AI / AdmetLab 3.0 / Deep-PK wrapper** — would let the new PK-properties recipe move from descriptor-and-analog estimation to defensible ML prediction for CYP / hERG / microsomal endpoints.
- **DeepChem (K-Dense Skill)** — already flagged in the catalog curator's state; would also strengthen the PK-properties recipe.
- **Co-folding / AlphaFold-Multimer / Boltz-2 wrapper** — would unlock a complex-modelling companion to the AlphaFold triage recipe.

### Verified (no changes)

- All recipes have `last_verified` within the 30-day window; no aging verifications were due this run.

## 2026-05-25

### Added

- **Filter a virtual screening hit list with drug-likeness rules and structural alerts** (Problem class: Data analysis; Evidence: Reported) — rung-2 [MedChem](catalog/tools/medchem.html) + [Datamol](catalog/tools/datamol.html) cascade for Lipinski → Veber → PAINS → BRENK triage of SMILES hit lists. First Chemistry-primary recipe in the cookbook. Evidence anchored in the K-Dense lead-optimisation workflow and the foundational filter papers ([Baell & Holloway PAINS 2010](https://doi.org/10.1021/jm901137j), [Brenk 2008](https://doi.org/10.1002/cmdc.200700139), [Lipinski 2001](https://doi.org/10.1016/S0169-409X(00)00129-0), [Veber 2002](https://doi.org/10.1021/jm020017n)).
- **Profile a compound's polypharmacology from ChEMBL bioactivity data** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 single-tool recipe over the [ChEMBL connector](catalog/tools/chembl.html). Second Chemistry-primary recipe and the compound-centric mirror of the existing target-dossier recipe. Evidence grounded in the [Anthropic ChEMBL Connector tutorial](https://claude.com/resources/tutorials/using-the-chembl-connector-in-claude) and the ChEMBL curation paper ([Mendez et al., *NAR* 2019](https://doi.org/10.1093/nar/gky1075)).

### Updated

- **Integrate multiple single-cell RNA-seq datasets across batches** — nav_order 2 → 3 for alphabetical position after the new Filter recipe.
- **Interpret a clinical variant from a natural-language query** — nav_order 3 → 4.
- **Match a patient summary to recruiting clinical trials** — nav_order 4 → 5.
- **Run bulk RNA-seq differential expression from a counts matrix** — nav_order 5 → 7 (after the new Profile recipe).
- **Run first-pass QC on a single-cell RNA-seq dataset** — nav_order 6 → 8.
- **Scan approved drugs for repurposing candidates against a disease** — nav_order 7 → 9.
- **Sort spikes from a Neuropixels recording end-to-end** — nav_order 8 → 10.
- **Triage a stack of new preprints in your field** — nav_order 9 → 11.

### Verified (no changes)

- 9 existing recipes spot-checked; all `last_verified` dates within the 30-day window, all linked catalog pages resolve.

## 2026-05-24

### Added

- **Scan approved drugs for repurposing candidates against a disease** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-3 toolbelt composing the [Open Targets plugin](catalog/tools/open-targets.html), [ChEMBL connector](catalog/tools/chembl.html), and [DrugBank MCP](catalog/tools/drugbank.html); first focused Drug Repurposing and Discovery recipe in the cookbook. Evidence anchors: [DeepDrug Alzheimer's repurposing graph](https://www.nature.com/articles/s41598-025-85947-7) (Li et al., *Scientific Reports* 2025), [Robin / ripasudil dAMD discovery](https://doi.org/10.1038/s41586-026-10652-y) (Ghareeb et al., *Nature* 2026), and [DREBIOP LLM-validation benchmark](https://www.biorxiv.org/content/10.1101/2025.06.13.659527v1) (Zunzunegui Sanz et al., *bioRxiv* 2025-06-13).

### Updated

- **Sort spikes from a Neuropixels recording end-to-end** — nav_order 7 → 8 for alphabetical position.
- **Triage a stack of new preprints in your field** — nav_order 8 → 9 for alphabetical position.

### Verified (no changes)

- 8 existing recipes spot-checked; all `last_verified` dates within the 30-day window, all linked catalog pages resolve.

## 2026-05-23

### Added

- **Match a patient summary to recruiting clinical trials** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 BioMCP / cyanheads-ClinicalTrials.gov-MCP recipe; first Translational-Medicine-focused recipe in the cookbook. Evidence grounded in TrialGPT ([Jin et al., *Nature Communications* 2024](https://www.nature.com/articles/s41467-024-53081-z), 87.3% criterion-matching accuracy).
- **Interpret a clinical variant from a natural-language query** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-2 BioMCP recipe; pairs with the trial-matching recipe for variant-driven enrollment. Closest analogous benchmark is MARRVEL-MCP ([bioRxiv 2025-11](https://www.biorxiv.org/content/10.1101/2025.11.26.690887v1)).

### Updated

- **Run bulk RNA-seq differential expression from a counts matrix** — nav_order 3 → 5 for alphabetical position after the two new TM recipes.
- **Run first-pass QC on a single-cell RNA-seq dataset** — nav_order 4 → 6 for alphabetical position.
- **Sort spikes from a Neuropixels recording end-to-end** — nav_order 5 → 7 for alphabetical position.
- **Triage a stack of new preprints in your field** — nav_order 6 → 8 for alphabetical position.

### Verified (no changes)

- 5 existing recipes spot-checked; all `last_verified` dates within the 30-day window, all linked catalog pages resolve.

## 2026-05-22

### Added

- **Integrate multiple single-cell RNA-seq datasets across batches** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping the Anthropic `scvi-tools` skill for scVI / scANVI batch integration; written in response to user request [#7](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/7); evidence grounded in Hrovatin 2025 and scIB-E 2025 ([source](https://claude.com/resources/tutorials/how-to-use-the-scvi-tools-bioinformatics-skill-bundle-with-claude)).
- **Sort spikes from a Neuropixels recording end-to-end** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping the K-Dense `neuropixels-analysis` skill (SpikeInterface + Kilosort4); first Neuroscience-only recipe in the cookbook ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/neuropixels-analysis/SKILL.md)).

### Updated

- **Run bulk RNA-seq differential expression from a counts matrix** — nav_order shifted 2 → 3 for alphabetical position.
- **Run first-pass QC on a single-cell RNA-seq dataset** — nav_order shifted 3 → 4 for alphabetical position.
- **Triage a stack of new preprints in your field** — nav_order shifted 4 → 6 for alphabetical position.

### Verified (no changes)

- 4 existing recipes spot-checked (all linked catalog pages resolve; `last_verified` 2026-05-21 still within the 30-day window so no bumps).

## 2026-05-21

### Added

- **Run first-pass QC on a single-cell RNA-seq dataset** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping Anthropic's `single-cell-rna-qc` skill for canonical scverse MAD-based filtering of 10x `.h5` / AnnData `.h5ad` inputs ([source](https://claude.com/resources/tutorials/how-to-use-the-single-cell-rna-qc-skill-with-claude)).
- **Run bulk RNA-seq differential expression from a counts matrix** (Problem class: Data analysis; Evidence: Reported) — rung-2 recipe wrapping the K-Dense PyDESeq2 skill for negative-binomial GLM differential expression, including pseudobulk single-cell handoff guidance ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/pydeseq2/SKILL.md)).
- **Build a target dossier from gene name to structure to cancer dependency** (Problem class: Knowledge synthesis; Evidence: Proposed) — first rung-3 toolbelt recipe composing Open Targets, UniProt, AlphaFold, and DepMap into a one-page target dossier; first `Proposed`-evidence entry in the cookbook ([closest analogue](https://doi.org/10.1101/2025.05.30.656746)).

### Updated

- **Triage a stack of new preprints in your field** — nav_order shifted from 1 to 4 to reflect alphabetical ordering after the three new Mol/Cell Bio additions; no content changes.

### Verified (no changes)

- 1 recipe spot-checked, current (`triage-new-preprints`, last_verified 2026-05-21).

## 2026-05-21 (initial seed)

### Added

- **Section bootstrap** — `recipes/` section created with landing page, landscape page, and the all-recipes index; `recipes/curator-state.md` initialized; `RECIPES_CHANGELOG.md` (this file) created. Curator prompt and daily workflow added at `RECIPE_AGENT.md` and `.github/workflows/recipes.yml`.
- **Triage a stack of new preprints in your field** (Problem class: Literature triage; Evidence: Reported) — first seed recipe demonstrating the schema and the lowest rung of the simplicity ladder (Claude Code alone + bioRxiv MCP) ([source](https://github.com/biorxiv/biorxiv-mcp)).
