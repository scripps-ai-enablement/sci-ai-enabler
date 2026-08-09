---
title: Recipes updates archive
nav_exclude: true
---

# Recipes updates archive

Older entries rotated out of [RECIPES_CHANGELOG.md](RECIPES_CHANGELOG.md). Newest first, same format.
## 2026-07-18 (Molecular and Cellular Biology directed pass)

### Added

- **Integrate multi-omics layers into interpretable factors with MOFA+** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [MOFA+ skill](catalog/tools/mofaplus-multi-omics.html) recipe: 2+ omics views on the same samples/cells ([muon](catalog/tools/muon-multiomics-singlecell.html)/MuData for single-cell multi-modal, AnnData dict for bulk) → per-view feature selection → build MOFA+ model → train (`mofapy2`, fixed factor count + seed) → per-factor per-view variance decomposition → factor–metadata association → top loadings per factor → committed `mofa_run.py` + pinned `requirements.txt` + `mofa_model.hdf5` + `variance_explained.csv`/`factor_metadata_assoc.csv`/`top_loadings_<view>.csv` + figure + `provenance.json` (mofapy2/muon versions, factor count + seed, per-view feature counts, input sha256s, run date, model id). Cross-modality factorization complement to the within-modality [scVI batch-integration recipe](recipes/items/integrate-single-cell-datasets.html); feeds the [functional-enrichment](recipes/items/run-functional-enrichment-on-a-gene-list.html) and [TF/pathway-activity](recipes/items/infer-tf-and-pathway-activities-from-expression.html) recipes (all cross-linked). `Proposed` — no documented Claude+MOFA+-skill attempt; grounded on the canonical method ([Argelaguet et al., *Genome Biology* 2020](https://doi.org/10.1186/s13059-020-02015-1)) and a current applied exemplar (12-factor MOFA+ decomposition of 667 TCGA gliomas validated across n=1685 without retraining; [Saleh et al., *Cancers* 2026](https://doi.org/10.3390/cancers18101652)). `Fully open`; `Laptop`.

### Updated

- **infer-gene-regulatory-network-from-scrnaseq** — fixed a broken feedback-footer URL (was pointing at the non-canonical `goodb.github.io`/`github.com/goodb` host; now `scripps-ai-enablement`); `last_verified` → 2026-07-18 (Arboreto/AnnData/Scanpy catalog pages resolve, method sources current).
- **assemble-reference-atlas-from-cellxgene-census**, **compute-hrv-from-ecg-recording** — fixed the same broken feedback-footer host (`goodb` → `scripps-ai-enablement`); no other changes.

### Verified (no changes)

- 4 additional MCB recipes spot-checked (oldest-first), all current; `last_verified` bumped to 2026-07-18: **run-bulk-rnaseq-differential-expression** ([PyDESeq2](catalog/tools/pydeseq2.html)), **run-functional-enrichment-on-a-gene-list** ([gget](catalog/tools/gget.html)), **infer-tf-and-pathway-activities-from-expression** ([decoupler-MCP](catalog/tools/decoupler-mcp.html)), **annotate-cell-types-in-single-cell-data** ([CellTypist](catalog/tools/celltypist-cell-annotation.html)/[popV](catalog/tools/popv-cell-annotation.html)) — all linked catalog pages resolve, sources current.

## 2026-07-18 (Integrative Structural and Computational Biology directed pass)

### Added

- **Design amino-acid sequences for a fixed protein backbone** (Problem class: Experimental design; Evidence: Reported) — rung-3 two-model toolbelt: [ProteinMPNN skill](catalog/tools/proteinmpnn.html) samples sequences for a target backbone `.pdb` (fixed catalytic/interface positions, temperature sweep) → [ESMFold skill](catalog/tools/esmfold.html) refolds every design → self-consistency gate (Cα-scRMSD < 2.0 Å AND mean pLDDT > 80) keeps only foldable candidates → ranked survivors → committed `.claude/commands/mpnn-design.md` + pinned skill envs + `designs/<name>_mpnn.fasta` + `results/<name>_selfconsistency.csv` + `provenance.json` (model/versions, sampling settings, cutoffs, backbone sha256, run date, model id). First recipe to compose the ProteinMPNN family; cross-links [LigandMPNN](catalog/tools/ligandmpnn.html)/[SolubleMPNN](catalog/tools/solublempnn.html) variants, [AlphaFold2](catalog/tools/alphafold2.html) as a stricter second gate, and the [score-protein-variants-with-esm](recipes/items/score-protein-variants-with-esm.html) sibling. `Reported` — ProteinMPNN is the validated field-standard inverse-folding model ([Dauparas et al., *Science* 2022](https://doi.org/10.1126/science.add2187)), the design→refold→filter self-consistency routine is standard practice ([Lin et al., *Science* 2023](https://doi.org/10.1126/science.ade2574)), and a ProteinMPNN redesign of a flavin-binding fluorescent protein was wet-lab confirmed ([Nikolaev et al., *Protein Sci.* 2024](https://pubmed.ncbi.nlm.nih.gov/38501498/)); the Claude-skill assembly is not separately benchmarked. `Fully open`; `Workstation with GPU`.

### Verified (no changes)

- 2 recipes spot-checked (oldest-first, ISCB-focused), all current; `last_verified` bumped to 2026-07-18: **predict-rna-secondary-structure-and-accessibility** ([ViennaRNA skill](catalog/tools/viennarna-structure-prediction.html) catalog page resolves; SciAgent-Skills repo live), **infer-protein-function-from-structure** ([Foldseek skill](catalog/tools/foldseek-structural-search.html) catalog page resolves; Foldseek Search web service still up).

## 2026-07-18 (Immunology and Microbiology directed pass)

### Added

- **Analyze a single-cell TCR repertoire alongside gene expression** (Problem class: Data analysis; Evidence: Reported) — rung-2 [scirpy Analysis skill](catalog/tools/scirpy-analysis.html) recipe: 10x/AIRR single-cell VDJ + matching clustered `.h5ad` → `pp.index_chains` + barcode-matched modality pairing → `chain_qc` filtering of multichain doublets/orphan cells → exact-CDR3-nt clonotype definition (TCR-appropriate, not BCR distance clustering) → clonal expansion + per-cluster/per-condition diversity + repertoire overlap → clonality overlaid on the transcriptomic UMAP → committed `sc_tcr.py` + pinned `requirements.txt` + `clonotypes.csv` + diversity/overlap tables + figure + `provenance.json` (scirpy/scanpy/mudata versions, clonotype strategy + params, input sha256s, run date, model id). T-cell, transcriptome-integrated counterpart to the B-cell [reconstruct-bcr-clonal-lineages](recipes/items/reconstruct-bcr-clonal-lineages.html) recipe; downstream of [qc-single-cell-rna-seq](recipes/items/qc-single-cell-rna-seq.html) and [annotate-cell-types-in-single-cell-data](recipes/items/annotate-cell-types-in-single-cell-data.html) (all cross-linked). `Reported` — scirpy is the scverse-standard single-cell TCR tool with a published benchmark ([Sturm et al., *Bioinformatics* 2020](https://pubmed.ncbi.nlm.nih.gov/32614448/)) and the exact multi-modal workflow is a 2025 methods protocol ([Plattner, Sturm & Rieder, *Methods Cell Biol.* 2025](https://pubmed.ncbi.nlm.nih.gov/41106935/)); the agent-driven skill assembly is not separately benchmarked. `Fully open`; `Laptop`.

### Verified (no changes)

- 3 recipes spot-checked (oldest-first), all current; `last_verified` bumped to 2026-07-18: **assemble-reference-atlas-from-cellxgene-census** (Census `2025-11-08` LTS still current; all catalog links resolve), **annotate-a-bacterial-genome** (Bakta/Prokka catalog pages resolve; canonical sources stable).

## 2026-07-18 (Chemistry directed pass; composition report #55)

### Added

- **Plan a synthetic route for a target molecule** (Problem class: Experimental design; Evidence: Reported) — rung-2 [CovaSyn MCP](catalog/tools/covasyn.html) recipe: target SMILES → optional [RDKit](catalog/tools/rdkit-skill.html)/[Datamol](catalog/tools/datamol.html) canonicalization → `covaplatform` retrosynthesis call (N routes, max depth) → per-step precursor + transform-class capture with buyable-leaf flags → route scoring (shorter, fully-buyable first) → committed `plan_route.py` + pinned `requirements.txt` + `routes.csv`/`route_summary.csv` + `provenance.json` (CovaSyn version, model/suite id, building-block catalog snapshot, request params, input sha256, run date, model id). Downstream make-check for [enumerate-analogs-around-a-lead](recipes/items/enumerate-analogs-around-a-lead.html) (cross-linked) and [filter-virtual-screening-hits](recipes/items/filter-virtual-screening-hits.html), with [ChemCrow](autonomous-science/systems/chemcrow.html) as the rung-4 execute-and-iterate alternative. `Reported` — agentic tool-grounded retrosynthesis is benchmarked near expert level ([LARC, Baker et al., *arXiv* 2508.11860, 2025](https://arxiv.org/abs/2508.11860): 72.9% on 48 constrained tasks; [ChemCrow, *Nat. Mach. Intell.* 2024](https://doi.org/10.1038/s42256-024-00832-8)); the exact Claude+CovaSyn pairing is not separately benchmarked. `Subscription required` (CovaSyn freemium, credit-metered, cloud SMILES submission); `Laptop`.

### Updated

- **Prioritize targets within a disease via Open Targets** — processed composition report [#55](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/55) (@goodb, `outcome=worked`); added an Alzheimer's-*prevention* field report (SORL1 lead via a prevention-tuned re-weighting of the pillar fields against MONDO_0004975) that reinforces the direct-GraphQL fallback when the hosted MCP is rate-limited; `last_verified` 2026-07-12 → 2026-07-18.

## 2026-07-16 (Translational Medicine scope; user request #52)

### Added

- **Interpret variants that gain or lose glycosylation sites** (Problem class: Knowledge synthesis; Evidence: Reported) — answers user request [#52](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/52) from the GlyGen team. Rung-3 two-MCP toolbelt: [GlyGen MCP](catalog/tools/glygen.html) `get_protein_summary`/`get_site_summary` for glycosite ground truth → Swiss-Prot numbering harmonization (the Asn135↔Asn167 antithrombin trap) → LOG/GOG classification (N-X-S/T sequon destroy/create) → [BioMCP](catalog/tools/biomcp.html) `variant_searcher`/`variant_getter` for ClinVar + AlphaMissense joins (GlyGen's own variants come from EBI/BioMuta, so these add coverage) → expression sanity-check → committed `glyco_variants.py` + pinned `requirements.txt` + `glyco_candidates.csv` + `provenance.json` (GlyGen release + endpoint, BioMCP version, ClinVar/AlphaMissense snapshot dates, input sha256, run date, model id) + optional IEEE-2791 BioCompute Object. Cross-linked to [interpret-clinical-variant](recipes/items/interpret-clinical-variant.html) and [scan-antibody-glycosylation-sites](recipes/items/scan-antibody-glycosylation-sites.html). `Reported` — the GlyGen team documents this exact use case and ships a `variants.ipynb` reference notebook (SERPINC1 LOG / IFNGR2 GOG worked examples; [Mazumder et al., *Research Square* 2026-07-01](https://www.researchsquare.com/article/rs-9982242/v1); [glygener/colab-notebooks](https://github.com/glygener/colab-notebooks)); the Claude-driven GlyGen-MCP+BioMCP assembly is not separately benchmarked. `Fully open` (GlyGen MCP Beta, wrapper repo no-LICENSE caveat); `Laptop`.

## 2026-07-12 (Drug Repurposing and Discovery directed pass)

### Added

- **Find drug-repurposing candidates by walking a biomedical knowledge graph** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-2 offline [PrimeKG skill](catalog/tools/primekg.html) recipe: resolve a disease node → `get_neighbors` for disease genes → one-hop `protein_protein` expansion → `drug_protein` candidate drugs → drop drugs already indicated for the disease → score by number of connecting genes (hop-weighted), captured as a committed `kg_repurpose.py` + pinned `requirements.txt` + `candidates.csv` + `provenance.json` (skill commit, PrimeKG data version, resolved node id, input sha256, run date, model id). Offline, no-license, graph-connectivity complement to the quantitative target-first [scan-drug-repurposing-candidates recipe](recipes/items/scan-drug-repurposing-candidates.html) (now cross-linked). `Proposed` — no documented attempt at the skill-driven graph-walk assembly; grounded on the same PrimeKG substrate that COMIC used to recover 21/30 recent FDA repurposing pairs (9.55% over SOTA; [Aamer et al., *BMC Bioinformatics* 2026](https://doi.org/10.1186/s12859-025-06337-4)) and CellAwareGNN reports AUPRC 0.826 on ([Zhang et al. 2026](https://pubmed.ncbi.nlm.nih.gov/42124589/)), with the honest caveat that the skill exposes neighbor lookups (interpretable heuristic), not a trained TxGNN-class predictor. `Fully open`; `Laptop`.

### Updated

- **Prioritize targets within a disease via Open Targets** — verified; `last_verified` 2026-06-20 → 2026-07-12 (linked catalog pages resolve and are unflagged; known-issue note on Open Targets MCP handshake still current).
- **Scan approved drugs for repurposing candidates against a disease** — verified; `last_verified` 2026-06-28 → 2026-07-12; added **See also** cross-link to the new knowledge-graph repurposing recipe.

## 2026-07-12 (Translational Medicine directed pass)

### Added

- **Triage GWAS lead SNPs to candidate drug targets** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 [GWAS-MCP](catalog/tools/gwas-mcp.html) recipe: a version-controlled `leads.csv` of rsIDs → per-variant `get_variant_info`/`annotate_snps` consequence + nearest gene → `get_eqtl_data` eQTL-implicated gene(s) → `query_gwas_catalog` co-reported traits → `get_drug_targets`/`search_open_targets` tractability + clinical precedent, captured as a committed `triage_gwas_leads.py` + pinned `requirements.txt` + `targets_triage.csv` + `provenance.json` (gwas-mcp version, per-database snapshot dates, input sha256, run date, model id). Variant-first complement to the disease-first [prioritize-targets recipe](recipes/items/prioritize-targets-within-a-disease.html) and upstream of [build-target-dossier](recipes/items/build-target-dossier.html); scoped to the lookup-and-annotate layer (colocalization/MR flagged out of scope). `Reported` — reproduces the lookup layer of a quantitatively validated GWAS→target workflow ([Lessard et al., *BMC Genomics* 2024](https://pubmed.ncbi.nlm.nih.gov/39563277/): approved-target enrichment RR 2.58 vs 1.75 nearest-gene, >85% MR-directionality match), resting on the genetic-support premise ([Nelson et al., *Nat. Genet.* 2015](https://pubmed.ncbi.nlm.nih.gov/26121088/); [King et al., *PLoS Genet.* 2019](https://pubmed.ncbi.nlm.nih.gov/31830040/)); the Claude+GWAS-MCP assembly is not separately benchmarked. `Fully open`; `Laptop`.

### Updated

- **Build a target dossier** — added a 2026-06 known-issue note to the Open Targets install step (hosted MCP endpoint fails the `initialize` handshake with JSON-RPC `-32602`, [#43](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/43)) with the direct-GraphQL / ToolUniverse workaround; `last_verified` → 2026-07-12.

### Verified (no changes)

- 5 aging recipes spot-checked, all current (`last_verified` → 2026-07-12): draft-phase23-clinical-trial-protocol, screen-polypharmacy-for-drug-interactions, profile-cancer-cohort-genomics-with-cbioportal, run-gwas-on-case-control-genotypes, compute-bacterial-pangenome-from-assemblies. Every linked catalog page resolves; source URLs load.

## 2026-07-12 (Neuroscience directed pass)

### Added

- **Extract event-related potentials from EEG epochs** (Problem class: Data analysis; Evidence: Reported) — rung-2 [MNE-Python (EEG) skill](catalog/tools/mne-eeg-tool.html) recipe: raw continuous EEG + event markers → montage/reference → band-pass + notch → ICA artifact removal → epoching → per-condition evoked averaging, captured as a committed `preprocess_erp.py` + pinned env + `*_ave.fif`/`erp_counts.csv` + `provenance.json` (MNE version, filter cutoffs, ICA method + dropped-component indices + seed, rejection threshold, per-condition kept/rejected counts, input sha256, run date, model id). Cookbook's first EEG-analysis recipe; sibling to the single-signal [HRV recipe](recipes/items/compute-hrv-from-ecg-recording.html), and can run on public EEG discovered via the [DANDI recipe](recipes/items/discover-nwb-recordings-on-dandi.html). `Reported` — MNE-Python is the field-standard M/EEG toolbox ([Gramfort et al., *Front. Neurosci.* 2013](https://doi.org/10.3389/fnins.2013.00267)) and the filter→ICA→epoch→average workflow is reused across recent reproducible-pipeline packages built on it ([EEG-Pype, *PLoS Comput. Biol.* 2026](https://doi.org/10.1371/journal.pcbi.1014043); [osl-ephys, *Front. Neurosci.* 2025](https://doi.org/10.3389/fnins.2025.1522675)); the agent-driven assembly is not separately benchmarked. `Fully open`; `Laptop`.

### Verified (no changes)

- 2 neuroscience recipes spot-checked, `last_verified` bumped to 2026-07-12: [Discover NWB recordings on DANDI](recipes/items/discover-nwb-recordings-on-dandi.html) (linked catalog tools + source DOIs resolve) and [Compute HRV from an ECG recording](recipes/items/compute-hrv-from-ecg-recording.html) (NeuroKit2 skill link current).

## 2026-07-11 (Molecular and Cellular Biology directed pass)

### Added

- **Quantify bulk RNA-seq FASTQ into a gene-level counts matrix** (Problem class: Data analysis; Evidence: Proposed) — rung-3 toolbelt: [fastp](catalog/tools/fastp-fastq-preprocessing.html) trim → [Salmon](catalog/tools/salmon-rna-quantification.html) decoy-aware quasi-mapping (`--gcBias --seqBias --validateMappings`) → tximport gene-level aggregation via `tx2gene` → committed `quantify_rnaseq.py` + pinned `requirements.txt` + fastp JSON QC + `counts.csv`/`coldata.csv` + `provenance.json` (transcriptome release, index flags, FASTQ sha256, tool versions, run date, model id). Fills the FASTQ→counts gap the [bulk RNA-seq DE recipe](recipes/items/run-bulk-rnaseq-differential-expression.html) assumed away, now cross-linked as its downstream companion; alignment-based alternative noted via [STAR](catalog/tools/star-rna-seq-aligner.html)+[featureCounts](catalog/tools/featurecounts-rna-counting.html). `Proposed` — grounded on Salmon bias/decoy-aware benchmarks ([Patro et al., *Nat. Methods* 2017](https://doi.org/10.1038/nmeth.4197); [Srivastava et al., *Genome Biol.* 2020](https://doi.org/10.1186/s13059-020-02151-8)) and tximport aggregation ([Soneson et al., *F1000Res* 2015](https://doi.org/10.12688/f1000research.7563.2)); the agent-orchestrated chain is not separately benchmarked. `Fully open`; `Laptop`.

### Updated

- **Run bulk RNA-seq differential expression from a counts matrix** — added upstream cross-link to the new FASTQ→counts recipe in **See also**.

### Verified (no changes)

- 2 recipes spot-checked (profile-chipseq-atacseq-signal-around-features, call-peaks-and-motifs-from-chipseq-atacseq), all current — linked deepTools/MACS3/HOMER catalog pages resolve and are unflagged, source repos and DOIs load; `last_verified` bumped to 2026-07-11.

## 2026-07-11 (Integrative Structural and Computational Biology directed pass)

### Added

- **Predict a protein–protein complex to map the binding interface** (Problem class: Hypothesis generation; Evidence: Reported) — rung-2 [Boltz plugin](catalog/tools/boltz.html) recipe: two partner FASTA sequences → `boltz-structure-and-binding` multi-chain co-folding (wide sampling) → local 5 Å inter-chain contact recomputation → committed `.claude/commands/predict-ppi-interface.md` + `interface_from_boltz.py` + pinned env + `interface.csv` (consensus interface residues) + `provenance.json` (plugin version, boltz-api job ids/date, model id, input sha256). General non-antibody PPI counterpart to the [antibody–antigen complex recipe](recipes/items/predict-antibody-antigen-complex.html); closes the long-deferred "AlphaFold-Multimer complex interface" candidate now that Boltz is catalogued. `Reported` — Boltz-2 matches AF3 on PDB 2024–2025 complexes ([Passaro et al., *bioRxiv* 2025](https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1)); AF-Multimer/AF3 are field-standard multimer baselines ([Hou et al., *Nat. Commun.* 2025](https://pubmed.ncbi.nlm.nih.gov/41261173/)); the Claude-plugin assembly is not separately benchmarked. `Subscription required` (hosted Boltz API); `Laptop`.

### Updated

- **Score point mutations for functional impact with a protein language model** — `last_verified` bumped to 2026-07-11; ESM/gget catalog pages resolve and are unflagged, sources still current.
- **Predict gene-knockout phenotypes with flux balance analysis** — `last_verified` bumped to 2026-07-11; COBRApy catalog page and Biomni system page resolve and are unflagged, sources still current.

### Verified (no changes)

- 2 additional recipes (ESM variant scoring, FBA knockout) spot-checked with the two above; linked catalog/system pages resolve.

## 2026-07-11 (Immunology and Microbiology directed pass)

### Added

- **Scan a protein for candidate CD8 T-cell epitopes** (Problem class: Experimental design; Evidence: Validated) — rung-2 [MHC Binding Prediction skill](catalog/tools/mhc-binding-prediction.html) recipe: antigen FASTA + HLA class I alleles → tile to 8–11-mers → MHCflurry (+optional NetMHCpan-4.1/MixMHCpred) presentation + `%Rank` scoring → committed `scan_epitopes.py` + pinned env + `epitopes.csv` + `provenance.json` (predictor versions/model release, allele list, input sha256, run date, model id). Cookbook's first MHC-I epitope recipe. `Validated` — NetMHCpan/MHCflurry captured >half of major epitopes in the top 277 of 767,788 candidates in a proteome-wide benchmark ([Paul et al., *PLoS Comput. Biol.* 2020](https://pubmed.ncbi.nlm.nih.gov/32453790/)); SOTA reconfirmed 2026 ([Mecklenbräuker et al., *Mol. Cell. Proteomics*](https://pubmed.ncbi.nlm.nih.gov/41903651/)). `Fully open`; `Laptop`.
- **Reconstruct B-cell clonal lineages from AIRR-seq** (Problem class: Data analysis; Evidence: Reported) — rung-2 [Immcantation BCR Analysis skill](catalog/tools/immcantation-analysis.html) recipe: AIRR rearrangement table → shazam data-derived clonal threshold → scoper clonal families → SHM/BASELINe selection → dowser germline-rooted lineage trees → committed `bcr_lineages.R` + pinned Immcantation env + `clones.tsv`/trees + `provenance.json` (package versions, IMGT germline release, derived threshold, input sha256, run date, model id). Cookbook's first BCR clonal-analysis recipe. `Reported` — Immcantation is the documented AIRR-seq clonal-analysis standard with an active supporting methods literature ([Abdollahi et al., *BMC Bioinformatics* 2023](https://pubmed.ncbi.nlm.nih.gov/36849917/); [Zhang et al., *Front. Immunol.* 2022](https://pubmed.ncbi.nlm.nih.gov/36618367/)); the agent-orchestrated assembly is not separately benchmarked. `Fully open`; `Laptop`.

### Updated

- **Scan a therapeutic antibody for glycosylation sites** — `last_verified` bumped to 2026-07-11; Glycoengineering/gget/Adaptyv catalog pages resolve and are unflagged, sources still current.
- **Infer cell-cell communication from single-cell RNA-seq** — `last_verified` bumped to 2026-07-11; LIANA-MCP catalog page resolves and is unflagged, sources still current.

### Flagged

- None.

### Verified (no changes)

- 2 recipes spot-checked (antibody-glycosylation, cell-cell communication), all current.

## 2026-07-11 (Chemistry directed pass)

### Added

- **Prepare the correct protonation state of a ligand before docking** (Problem class: Experimental design; Evidence: Proposed) — rung-2 [Rowan skill](catalog/tools/rowan.html) recipe: ligand SMILES → optional local [Datamol](catalog/tools/datamol.html) standardization → Rowan `submit_macropka_workflow` (pH 0–14) → dominant microspecies at pH 7.4 + governing macro-pKa → committed `prepare_protonation.py` + pinned env + `prepared_ligands.csv` + `provenance.json` (Rowan skill/workflow ids, pH, run date, input/output sha256, model id). Fills the ligand-prep gap upstream of the [DiffDock docking](recipes/items/dock-ligand-library-with-diffdock.html), [affinity-ranking](recipes/items/rank-compound-library-by-predicted-affinity.html), and [GROMACS MD](recipes/items/set-up-protein-md-simulation-in-gromacs.html) recipes, distinguished from the pH-blind standardization in the [enumerate-analogs recipe](recipes/items/enumerate-analogs-around-a-lead.html). `Proposed` — grounded on Rowan's documented pKa/macro-pKa workflows and the established impact of protonation/tautomeric state on docking enrichment ([Kim et al., *J. Comput. Aided Mol. Des.* 2013](https://doi.org/10.1007/s10822-013-9643-9)); the agent-orchestrated prep assembly is not separately benchmarked. `Fully open` (free Rowan tier; cloud submission — data-residency caveat); `Laptop`.

### Updated

- **Analyze an existing MD trajectory for stability, flexibility, and contacts** — `last_verified` bumped to 2026-07-11; linked MDAnalysis/MDTraj catalog pages resolve and are unflagged, sources still current.

### Flagged

- None.

### Verified (no changes)

- 1 recipe spot-checked (MD-trajectory analysis), current.

## 2026-07-05 (Drug Repurposing and Discovery directed pass)

### Added

- **Validate a drug target with a GO/NO-GO score before committing bench work** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-2 [Drug Target Validation skill](catalog/tools/tooluniverse-drug-target-validation.html) over the [ToolUniverse MCP](catalog/tools/tooluniverse.html): a gene + disease → four-gate scoring (disease association 30 / druggability 25 / safety 20 / clinical precedent 15 / validation evidence 10) → committed `.claude/commands/validate-target.md` slash command + `targets/validation_scores.csv` + per-target cited cards + `provenance.json` (tooluniverse version, skill tag, Open Targets/ChEMBL release labels, resolved accessions, run date, model id). Fills the single-target GO/NO-GO gap between the [prioritize-targets recipe](recipes/items/prioritize-targets-within-a-disease.html) (disease-in, ranked list) and the [target-dossier recipe](recipes/items/build-target-dossier.html) (gene-in, free-form). `Proposed` — grounded on the ToolUniverse ecosystem paper's hypercholesterolemia case study ([Gao et al., arXiv:2509.23426, 2025](https://arxiv.org/abs/2509.23426)) and the field-standard genetic-evidence/precedence-tractability-doability-safety framework ([Nelson et al., *Nat. Genet.* 2015](https://doi.org/10.1038/ng.3314); [Ochoa et al., *NAR* 2023](https://doi.org/10.1093/nar/gkac1046)); the composite-score assembly is not separately benchmarked. `Fully open`; `Laptop`.

### Verified (no changes)

- **Enumerate analogs around a lead compound for SAR expansion** — linked catalog pages (datamol, rdkit-skill) resolve and are unflagged; textbook cheminformatics sources current. Bumped `last_verified` to 2026-07-05.
- **Identify an unknown compound from an MS/MS spectrum** — linked catalog pages (matchms, pyopenms, pubchem) resolve and are unflagged; matchms/SimMS sources current. Bumped `last_verified` to 2026-07-05.
- **Estimate pharmacokinetic properties of a small molecule** — linked catalog pages (rdkit-skill, medchem, chembl) resolve and are unflagged; ChEMBL/ChemCrow/PharmaBench sources current. Bumped `last_verified` to 2026-07-05.
- **Triage an AlphaFold model for structure-based drug design** — linked catalog pages (alphafold, pdb, uniprot) resolve and are unflagged; AlphaFold DB / pLDDT-benchmark sources current. Bumped `last_verified` to 2026-07-05.

## 2026-07-05 (Translational Medicine directed pass)

### Added

- **Assemble a public cancer imaging cohort from NCI Imaging Data Commons** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 [Imaging Data Commons skill](catalog/tools/imaging-data-commons.html) recipe: cohort criteria (modality / body part / accompanying RTSTRUCT-SEG / license) → `idc-index` DuckDB metadata query → license-filtered series-level `cohort_manifest.csv` + committed `build_cohort.py` + pinned env + `provenance.json` (idc-index version, IDC release version, query date, manifest sha256, patient/series counts, model id) → manifest-based DICOM download. The medical-imaging counterpart to the [DANDI discovery recipe](recipes/items/discover-nwb-recordings-on-dandi.html) and [cellxgene-census atlas recipe](recipes/items/assemble-reference-atlas-from-cellxgene-census.html); the upstream cohort step feeding the [nnU-Net segmentation recipe](recipes/items/segment-organ-or-tumor-in-medical-image.html) via the [DICOM-to-BIDS recipe](recipes/items/organize-raw-dicom-to-bids-layout.html). Emphasizes the per-collection CC-BY/CC-NC license gate. `Reported` — IDC and its `idc-index` client are the documented public-cancer-imaging cohort tooling ([Fedorov et al., *RadioGraphics* 2023](https://doi.org/10.1148/rg.230180); [Fedorov et al., *Cancer Res.* 2021](https://doi.org/10.1158/0008-5472.CAN-21-0950)); the Claude-skill assembly is not separately benchmarked. `Fully open`; `Laptop`.
- **Extract structured variables from free-text clinical notes** (Problem class: Data analysis; Evidence: Validated) — rung-1 (Claude Code alone) recipe: a folder of de-identified clinical notes + a versioned `codebook.md` → per-cell extraction with `evidence_quote` and `found/negated/not_mentioned` status into `records.jsonl` → flattened `registry.csv` + committed `extract_registry.py` + pinned env + `provenance.json` (model id, codebook sha256, note count, gold-subset accuracy) + a clinician-abstracted gold-set accuracy check. Cookbook's first note-extraction recipe; the upstream step to the [harmonize-clinical-terms recipe](recipes/items/harmonize-clinical-terms-to-standard-codes.html) (extract → then map terms to codes) and cross-linked to the [readmission-prediction recipe](recipes/items/predict-hospital-readmission-from-ehr.html). `Validated` — Claude 3.5 Sonnet extracted structured binary variables from ILD clinic notes at 96.2% accuracy, matching three-physician consensus ([Chen et al., *J. Med. Internet Res.* 2026](https://pubmed.ncbi.nlm.nih.gov/42361337/)); oncologic-history extraction reached F1 = 0.983 ([Bhayana et al., *Radiology* 2025](https://pubmed.ncbi.nlm.nih.gov/39903072/)). `Fully open`; `Laptop`.

### Verified (no changes)

- **Match a patient summary to recruiting clinical trials** — linked catalog pages (biomcp, clinicaltrials-gov-mcp, clinical-trial-protocol) and the Biomni system page resolve and are unflagged; TrialGPT / MatchMiner-AI sources current. Bumped `last_verified` to 2026-07-05.
- **Build a pharmacogenomic dosing report from a patient's diplotypes** — linked catalog pages (clinpgx-database, ddinter-database) resolve and are unflagged; CPIC guideline sources current. Bumped `last_verified` to 2026-07-05.

## 2026-07-04 (Molecular and Cellular Biology directed pass, later slot)

### Added

- **Find selective genetic dependencies for a cancer context with DepMap** (Problem class: Hypothesis generation; Evidence: Reported) — rung-2 [DepMap skill](catalog/tools/depmap.html) recipe: a cancer context (lineage / driver mutation / fusion / expression state) → copy-number-corrected group contrast over the Chronos `CRISPRGeneEffect` matrix → pan-essential-filtered, FDR-corrected `dependencies.csv` (selective effect, p, fdr, copy_number_flag) + committed `find_dependencies.py` + pinned env + `provenance.json` (DepMap release label + matrix sha256s, context/background definition, thresholds, run date, model id). First recipe to use the catalogued DepMap skill as a standalone tool (context-in / genes-out); distinguished from the [target-dossier recipe](recipes/items/build-target-dossier.html) (gene-in, uses DepMap as one of four lookups) and the [prioritize-targets recipe](recipes/items/prioritize-targets-within-a-disease.html) (disease-in, Open Targets associations). Cross-linked to the [sgRNA-design recipe](recipes/items/design-crispr-sgrnas-for-a-gene-knockout.html) for validation. `Reported` — DepMap-mining for selective dependencies is routine, with recent peer-reviewed instances ([Schneider et al., *Cancer Res.* 2024](https://doi.org/10.1158/0008-5472.CAN-23-3560); [Phillips et al., *Nat. Commun.* 2025](https://doi.org/10.1038/s41467-024-55300-z); [Iyer et al., *EMBO J.* 2025](https://doi.org/10.1038/s44318-025-00526-w)); the Claude-skill assembly is not separately benchmarked. `Fully open`; `Laptop`.

## 2026-07-04 (Integrative Structural and Computational Biology directed pass)

### Added

- **Superpose two protein structures and quantify where they differ** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [PyMOL skill](catalog/tools/pymol.html) recipe: two coordinate files (AlphaFold model vs experimental PDB, or apo vs holo) → `cealign`/`super` superposition → global RMSD + per-residue Cα-deviation `perres.csv` + deviation-coloured overlay PNG + `.pse` session + committed `.claude/commands/superpose.md` + `uv`-pinned env + `provenance.json` (PyMOL version, method + cutoff, both input sha256s, chain selectors, aligned-atom count, RMSD, fetch date/accession, model id). First recipe to use the catalogued PyMOL skill; cross-linked to the [Foldseek function recipe](recipes/items/infer-protein-function-from-structure.html) (database-search counterpart) and the [AlphaFold triage recipe](recipes/items/triage-alphafold-model-for-docking.html) (confidence-side counterpart). `Proposed` — no LLM-driven superposition workflow is documented; grounded on peer-reviewed PyMOL `cealign` ([Shindyalov & Bourne, *Protein Eng.* 1998](https://doi.org/10.1093/protein/11.9.739)) and AlphaFold model-vs-experiment RMSD validation ([Jumper et al., *Nature* 2021](https://doi.org/10.1038/s41586-021-03819-2)). `Fully open`; `Laptop`.

### Verified (no changes)

- **Sort spikes from a Neuropixels recording end-to-end** — linked catalog pages (neuropixels-analysis, neurosift, aind-data) resolve and are unflagged; SpikeAgent/SpikeInterface sources current. Corrected the K-Dense SKILL.md source URL path (`scientific-skills/` → `skills/`) to match the catalog page. Bumped `last_verified` to 2026-07-04.
- **Organize a raw DICOM dataset into a BIDS layout** — linked catalog pages (bids, openneuro) resolve and are unflagged; BIDS-spec and component DOIs current. Bumped `last_verified` to 2026-07-04.

## 2026-07-04 (Immunology and Microbiology directed pass, later slot)

### Added

- **Identify a bacterial isolate from its 16S rRNA sequence** (Problem class: Data analysis; Evidence: Reported) — rung-2 [BLAST (Bio-MCP)](catalog/tools/blast.html) recipe: a colony-PCR Sanger 16S read (or assembled 16S contig) → `blastn` against a pinned curated 16S database (NCBI `16S_ribosomal_RNA`) → coverage-filtered, identity-ranked `hits.csv` with a threshold-based `assignment` column (98.7% species / 94.5% genus) + committed `identify_16s.py` + pinned env + `provenance.json` (BLAST+ version, 16S DB release + sha256, query sha256, cutoffs, run date, model id). Single-isolate identification counterpart to the community-level [16S diversity recipe](recipes/items/compute-16s-microbiome-diversity.html); cross-linked to the [resistome screen](recipes/items/screen-genome-for-resistance-and-virulence-genes.html) (same BLAST-MCP tool), the [bacterial-genome-annotation recipe](recipes/items/annotate-a-bacterial-genome.html) (consumes the genus hint), and the [phylogenetic-tree recipe](recipes/items/build-phylogenetic-tree-from-sequences.html). `Reported` — 98.7%/94.5% identity thresholds are the community standard ([Kim et al., *IJSEM* 2014](https://doi.org/10.1099/ijs.0.059774-0); [Yarza et al., *Nat. Rev. Microbiol.* 2014](https://doi.org/10.1038/nrmicro3330)); the BLAST-MCP assembly is not separately benchmarked. `Fully open`; `Laptop`.

### Verified (no changes)

- **Build a phylogenetic tree from a set of sequences** — linked catalog pages (phylogenetics, ETE Toolkit, Nextflow) and Biomni system page all resolve; sources current. Bumped `last_verified` to 2026-07-04.

## 2026-07-04 (Immunology and Microbiology directed pass)

### Added

- **Screen a bacterial genome for resistance and virulence genes** (Problem class: Data analysis; Evidence: Reported) — rung-2 [BLAST (Bio-MCP)](catalog/tools/blast.html) recipe: an annotated genome's protein FASTA → `makeblastdb` + `blastp` against pinned CARD and VFDB references → identity/coverage-filtered best-hit-per-database → `resistance_hits.csv` + `virulence_hits.csv` + committed `screen_resistome.py` + pinned env + `provenance.json` (BLAST+ version, CARD release, VFDB download date, FASTA sha256s, cutoffs, input sha256). Picks up the AMR/virulence step the [bacterial-genome-annotation recipe](recipes/items/annotate-a-bacterial-genome.html) explicitly punts to the CLI, cross-linked to it and the [pan-genome recipe](recipes/items/compute-bacterial-pangenome-from-assemblies.html). `Reported` — `blast+` AMR/virulence detection validated at >95% sensitivity/specificity on a 131-isolate reference collection ([Bogaerts et al., *Microb. Genom.* 2021](https://doi.org/10.1099/mgen.0.000531)); the BLAST-MCP assembly is not separately benchmarked. `Fully open`; `Laptop`.

### Flagged

- **Missing component: dedicated resistome caller (RGI / AMRFinderPlus)** — surfaced for the catalog curator; the new AMR recipe is homology-only (no point-mutation resistance models) until such a tool is Claude-installable.

### Verified (no changes)

- 3 recipes spot-checked, all current, `last_verified` bumped to 2026-07-04: [dock-ligand-library-with-diffdock](recipes/items/dock-ligand-library-with-diffdock.html), [integrate-single-cell-datasets](recipes/items/integrate-single-cell-datasets.html), [filter-virtual-screening-hits](recipes/items/filter-virtual-screening-hits.html) — all linked catalog pages resolve and are unflagged.

## 2026-06-28 (Drug Repurposing and Discovery directed pass)

### Added

- **Rank a compound library against a target by predicted binding affinity** (Problem class: Data analysis; Evidence: Reported) — rung-2 [Boltz plugin](catalog/tools/boltz.html) recipe driving the hosted `boltz-small-molecule-screen` skill: a target sequence/PDB + a SMILES library → MedChem/Datamol pre-filter ([upstream recipe](recipes/items/filter-virtual-screening-hits.html)) → structure-and-affinity screen on the hosted Boltz API (no local GPU) → `screen_ranked.csv` (affinity, binder probability, structure confidence) + committed `rank_screen.py` + `.claude/commands/boltz-affinity-screen.md` + pinned env + `provenance.json` (Boltz model id, job IDs, submission date, input sha256, target accession), ranking by the classifier score rather than fine affinity gaps. Cookbook's first GPU-free structure-based affinity-screening recipe, cross-linked to the [DiffDock recipe](recipes/items/dock-ligand-library-with-diffdock.html) (GPU pose-level counterpart) and the [virtual-screening hit filter](recipes/items/filter-virtual-screening-hits.html) (upstream). `Reported` — Boltz-2 approaches FEP accuracy (Pearson 0.62 on FEP+, doubles MF-PCBA average precision; [Passaro et al., bioRxiv 2025](https://www.biorxiv.org/content/10.1101/2025.06.14.659707v1)) but an independent eval ([Wan et al., arXiv:2603.05532, 2026](https://arxiv.org/abs/2603.05532)) finds it a good binder classifier yet weak quantitative ranker; the Claude-plugin assembly is not separately benchmarked. `Subscription required`; `Laptop`.

### Updated

- **Scan approved drugs for repurposing candidates against a disease** — spot-checked; all catalog/system links resolve, tags consistent; `last_verified` → 2026-06-28.
- **Profile a compound's polypharmacology from ChEMBL bioactivity data** — spot-checked; all catalog links resolve, tags consistent; `last_verified` → 2026-06-28.

### Verified (no changes)

- No recipes are over the 30-day `last_verified` window (oldest is 2026-06-03); spot-checked the oldest Drug Repurposing recipes, all current.

## 2026-06-28 (Translational Medicine directed pass)

### Added

- **Register longitudinal medical scans to a common frame** (Problem class: Data analysis; Evidence: Reported) — rung-2 [SimpleITK skill](catalog/tools/simpleitk-image-registration.html) recipe: a baseline + follow-up CT/MRI pair → `CenteredTransformInitializer` → two-stage rigid (Euler3D, Mattes MI, multi-resolution pyramid) → deformable (B-spline) registration → resampled `warped.nii.gz` + persisted `transform.tfm` + propagated label mask (nearest-neighbour, Dice reported) + committed `register_scans.py` + pinned env + `provenance.json` (SimpleITK version, transform/metric/optimizer settings, control-point spacing, input sha256s), with a checkerboard/difference-overlay QC step. Cookbook's first image-registration recipe, cross-linked to the [nnU-Net segmentation recipe](recipes/items/segment-organ-or-tumor-in-medical-image.html) (produces the masks it propagates), the [DICOM-to-BIDS recipe](recipes/items/organize-raw-dicom-to-bids-layout.html) (upstream conversion), and the [survival recipe](recipes/items/fit-survival-model-to-clinical-outcomes.html) (downstream). `Reported` — SimpleITK/ITK are peer-reviewed and field-standard ([Yaniv et al., *J. Digit. Imaging* 2018](https://doi.org/10.1007/s10278-017-0037-8)); the Claude-skill assembly is not independently benchmarked. `Fully open`; `Workstation with GPU`.
- **Tile and stain-normalize a whole-slide image for ML** (Problem class: Data analysis; Evidence: Reported) — rung-2 [histolab skill](catalog/tools/histolab.html) recipe: a gigapixel H&E WSI (or folder) → tissue masking → fixed-size tile extraction at a chosen magnification → Macenko/Reinhard stain normalization against a committed reference → a `tiles/` folder + `manifest.csv` (slide_id, tile_path, level, mpp, x, y, tissue_pct) + committed `tile_wsi.py` + pinned env + `provenance.json` (histolab/OpenSlide versions, tile size, level, tissue threshold, normalizer + reference sha256, slide sha256), with a contact-sheet QC step. Cookbook's first digital-pathology WSI-preprocessing recipe, cross-linked to the [pathml skill](catalog/tools/pathml.html) (heavier toolkit) and the [microscopy segmentation recipe](recipes/items/segment-and-quantify-cells-in-microscopy.html) (cell-level counterpart). `Reported` — histolab is the peer-reviewed reproducible-preprocessing library ([Marcolini et al., *SoftwareX* 2022](https://doi.org/10.1016/j.softx.2022.101237)); the Claude-skill assembly is not independently benchmarked. `Fully open`; `Workstation with GPU`.
- **Harmonize free-text clinical terms to standard codes** (Problem class: Knowledge synthesis; Evidence: Proposed) — rung-2 [Medical Terminologies MCP](catalog/tools/medical-terminologies-mcp.html) recipe: a column of free-text diagnoses/drugs/labs → grounded lookup against ICD-11/RxNorm/ATC/LOINC → ranked `candidates.csv` (all hits per term) → a curated `crosswalk.csv` (term, chosen code/system/concept, match_type, n_candidates) + committed `harmonize_terms.py` + pinned env + `provenance.json` (MCP version, per-service terminology release dates, run date, model id, input sha256), with an expert-review pass on `needs_review` rows. Cookbook's first clinical-terminology harmonization recipe, cross-linked to the [PyHealth skill](catalog/tools/pyhealth.html) (in-pipeline code utilities) and the [pharmacogenomic dosing report](recipes/items/build-pharmacogenomic-dosing-report.html) (closest documented LLM-driving-clinical-references workflow). `Proposed` — grounding rests on authoritative WHO/RxNorm/LOINC services; no documented attempt of this exact LLM+MCP assembly is known. `Fully open`; `Laptop`.

### Verified (no changes)

- No recipes are over the 30-day `last_verified` window (oldest is 2026-06-03); spot-checked the oldest, all current.

## 2026-06-27 (Molecular and Cellular Biology directed pass)

### Added

- **Segment and quantify cells in a microscopy image** (Problem class: Data analysis; Evidence: Reported) — rung-2 [Cellpose skill](catalog/tools/cellpose-cell-segmentation.html) recipe: a fluorescence/brightfield image (or folder) → pretrained generalist instance segmentation (`cyto3`/`nuclei`) → per-cell label masks + a tidy `cells.csv` (count, area, eccentricity, centroid, per-channel mean intensity via scikit-image `regionprops`), with a committed `segment_and_quantify.py` + pinned env + `provenance.json` (cellpose version, model, diameter, flow/cellprob thresholds, input sha256) and an explicit mask-QC step (over-merge/over-split). Cookbook's first cell-microscopy segmentation/quantification recipe, cross-linked to the [scikit-image skill](catalog/tools/scikit-image-processing.html) (classical fallback) and the [nnU-Net medical-image recipe](recipes/items/segment-organ-or-tumor-in-medical-image.html) (radiology counterpart). `Reported` — Cellpose is field-defining ([Stringer et al., *Nature Methods* 2021](https://www.nature.com/articles/s41592-020-01018-x); [Cellpose3, 2025](https://www.nature.com/articles/s41592-025-02595-5)); the Claude-skill assembly is not independently benchmarked. `Fully open`; `Laptop`.
- **Design CRISPR sgRNAs for a gene knockout** (Problem class: Experimental design; Evidence: Reported) — rung-2 [sgRNA Design skill](catalog/tools/sgrna-design-guide.html) recipe: a gene + genome build → tiered guide selection (validated Addgene libraries → CRISPick pre-computed picks → de novo Rule Set 2 / Azimuth on-target + CFD off-target scoring) → a committed `guides.csv` (sequence, PAM, exon, strand, on/off-target, source tier) + pinned env + `provenance.json` (genome build, skill + source DB versions), with a pre-order exon/PAM/off-target sanity check. Cookbook's first CRISPR guide-design recipe, cross-linked to the [plasmid-verification recipe](recipes/items/annotate-and-verify-a-plasmid-construct.html). `Reported` — scoring rests on the field-standard Rule Set 2 / CFD models ([Doench et al., *Nature Biotechnology* 2016](https://www.nature.com/articles/nbt.3437)); the Claude-skill assembly is not independently benchmarked. `Fully open`; `Laptop`.

## 2026-06-27 (Integrative Structural and Computational Biology directed pass)

### Added

- **Infer the function of an uncharacterized protein from its 3D structure** (Problem class: Knowledge synthesis; Evidence: Reported) — rung-2 [Foldseek Structural Search skill](catalog/tools/foldseek-structural-search.html) recipe: a `.pdb`/`.cif` coordinate file → hosted Foldseek search against annotated structure DBs (`afdb-swissprot`, `pdb100`, `afdb50`) → ranked hit table + a banded (STRONG/SUGGESTIVE/NO-CONFIDENT-HIT) function call read off the top hits' annotations, with a committed `.claude/commands/foldseek-function.md`, `uv`-pinned skill env, and `provenance.json` (Foldseek API date + DB version strings + input sha256). The structure-side fallback for when sequence search (BLAST/HMMER/InterPro) returns nothing; cookbook's first structural-homology / function-inference recipe, cross-linked to the [AlphaFold-triage recipe](recipes/items/triage-alphafold-model-for-docking.html) (structure-quality counterpart) and the [ESM variant-scoring recipe](recipes/items/score-protein-variants-with-esm.html). `Reported` — Foldseek is peer-reviewed and field-defining ([van Kempen et al., *Nature Biotechnology* 2023](https://doi.org/10.1038/s41587-023-01773-0): 4–5 orders of magnitude faster than DALI/TM-align at 86–133% of their sensitivity), and the skill is a maintained Google DeepMind release; the Claude-skill assembly is not independently benchmarked. `Fully open`; `Laptop`.

### Verified (no changes)

- All recipes within the 30-day `last_verified` window (oldest 2026-06-03); no aging verification due this run.

## 2026-06-27 (Immunology and Microbiology directed pass)

### Added

- **Annotate and verify an engineered plasmid construct** (Problem class: Experimental design; Evidence: Reported) — rung-2 [pLannotate skill](catalog/tools/plannotate-plasmid-annotation.html) recipe taking a plasmid FASTA/GenBank through a local BLAST run against curated genetic-parts databases (Addgene, fpbase, Swiss-Prot, Rfam) → an annotated GenBank + feature table + HTML map, with the *fragment* column surfaced as the construct-verification signal and a committed `annotate_plasmid.py` + pinned env + `provenance.json` (pLannotate DB version + input sha256). Immunology and Microbiology / Molecular and Cellular Biology focus-day recipe; cookbook's first engineered-plasmid recipe, cross-linked to the [bacterial-genome annotation recipe](recipes/items/annotate-a-bacterial-genome.html) (chromosomal counterpart) and explicitly contrasted with Prokka/Bakta, which don't recognize engineered parts. `Reported` — pLannotate is the established engineered-plasmid annotator ([McGuffie & Barrick, *Nucleic Acids Res.* 2021](https://doi.org/10.1093/nar/gkab374): annotates recombinant/synthetic/engineered elements and reports incomplete fragments that genome pipelines miss); the Claude-skill assembly is not independently benchmarked. `Fully open`; `Laptop`.

## 2026-06-27

### Added

- **Predict an antibody–antigen complex to map an epitope** (Problem class: Experimental design; Evidence: Reported) — rung-2 [Boltz plugin](catalog/tools/boltz.html) recipe taking antibody/nanobody chains + an antigen sequence through a hosted-API `boltz-structure-and-binding` co-fold with a deliberately *wide sample ensemble*, then a local 4.5 Å CDR-contact recomputation per model (committed `epitope_from_boltz.py` + pinned env + `provenance.json` capturing `boltz-api` job IDs and submission date) → a *consensus* epitope across the top models rather than trusting top-1 confidence. Immunology and Microbiology focus-day recipe; cookbook's first co-folding/complex-prediction recipe, cross-linked to the [AlphaFold-triage recipe](recipes/items/triage-alphafold-model-for-docking.html) (single-chain counterpart) and the [antibody-glycosylation recipe](recipes/items/scan-antibody-glycosylation-sites.html). `Reported` — Boltz-2/1x are independently benchmarked on Ab/VHH–antigen complexes ([Gupta et al., *Protein Science* 2026, SNAC-DB](https://doi.org/10.1002/pro.70655): success rates ≤25%, 1000-sample oracle 50.5% vs near-flat confidence ranking; [Ünsal et al., *Brief. Bioinform.* 2026, AntiConf](https://doi.org/10.1093/bib/bbag137)), but the Claude-plugin assembly is not independently benchmarked. `Subscription required` (hosted Boltz API); `Laptop`.

### Verified (no changes)

- 4 recipes spot-checked, all current (`last_verified` bumped to 2026-06-27): set-up-protein-md-simulation-in-gromacs, convert-instrument-data-to-allotrope-asm, compute-16s-microbiome-diversity, parse-fcs-flow-cytometry-files. All linked catalog/system pages resolve and are unflagged; source citations stable.

## 2026-06-21

### Added

- **Score a drug-combination screen for synergy** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [ToolUniverse Drug Synergy skill](catalog/tools/tooluniverse-drug-synergy.html) recipe taking user-supplied single-agent + combination effect data (on one consistent scale) through model selection by data shape (`DrugSynergy_calculate_bliss`/`_hsa`/`_loewe`/`_zip`/`_ci`) → synergy score → synergy/additive/antagonism classification via the standard ±10 thresholds (CI < 1 inverse), with scale-mixing and dose-dependence footguns surfaced. Drug Repurposing and Discovery focus-day recipe; cookbook's first combination-synergy recipe, cross-linked to the [polypharmacology recipe](recipes/items/profile-compound-polypharmacology.html) and the [drug-repurposing scan recipe](recipes/items/scan-drug-repurposing-candidates.html). `Proposed` — no documented Claude-driven ToolUniverse synergy assembly; grounded in the field-standard reference models from [Ianevski et al., *Nucleic Acids Research* 2022 (SynergyFinder 3.0)](https://doi.org/10.1093/nar/gkac382) and the skill's `SKILL.md`. `Laptop`.
- **Detect somatic copy-number variants from tumor sequencing** (Problem class: Data analysis; Evidence: Reported) — rung-2 [CNVkit skill](catalog/tools/cnvkit-copy-number.html) recipe taking tumor WES/targeted-panel BAMs through pooled-reference construction → coverage binning + bias correction → CBS segmentation → gene-level amplification/deletion calls (with stated log2 thresholds) → scatter/diagram QC plots and SEG/VCF export, with purity/ploidy and matched-normal caveats surfaced. Translational Medicine focus-day recipe; cookbook's first somatic-CNV recipe, paired with the [cBioPortal cohort recipe](recipes/items/profile-cancer-cohort-genomics-with-cbioportal.html) for cohort-level context. `Reported` — CNVkit is the field-standard engine for copy-number from targeted/exome data ([Talevich et al., *PLOS Comput. Biol.* 2016](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004873)); the Claude-skill assembly is not independently benchmarked.
- **Predict hospital readmission from EHR data** (Problem class: Data analysis; Evidence: Proposed) — rung-2 [PyHealth skill](catalog/tools/pyhealth.html) recipe taking a credentialed EHR extract (MIMIC-IV/eICU/OMOP) through the dataset → 30-day-readmission task → RETAIN/Transformer sequence model → patient-level-split AUROC/AUPRC + calibration vs a logistic-regression baseline, with data-use-agreement and cross-institution-transfer caveats surfaced. Translational Medicine focus-day recipe; cookbook's first EHR clinical-prediction recipe, complementing the [survival-model recipe](recipes/items/fit-survival-model-to-clinical-outcomes.html). `Proposed` — no documented LLM-driven PyHealth assembly; grounded in [Yang et al., *KDD 2023*](https://dl.acm.org/doi/10.1145/3580305.3599178) and [PyHealth 2.0, arXiv:2601.16414 (2026)](https://arxiv.org/abs/2601.16414). `Institutional access` (PhysioNet credentialed datasets).
- **Segment an organ or tumor in a medical image with nnU-Net** (Problem class: Data analysis; Evidence: Reported) — rung-2 [nnU-Net skill](catalog/tools/nnunet-segmentation.html) recipe taking labeled CT/MRI volumes through dataset-fingerprint planning → auto-configured preprocessing/architecture → 5-fold cross-validated training → best-config selection → held-out mask prediction + volume QC, with the nnU-Net folder/`_0000` data contract and the GPU/multi-day-per-fold cost surfaced. Translational Medicine focus-day recipe; cookbook's first medical-image-segmentation recipe, chained off the [DICOM-to-BIDS recipe](recipes/items/organize-raw-dicom-to-bids-layout.html) upstream and feeding the [survival-model recipe](recipes/items/fit-survival-model-to-clinical-outcomes.html) downstream. `Reported` — nnU-Net is field-defining ([Isensee et al., *Nature Methods* 2021](https://www.nature.com/articles/s41592-020-01008-z): match/beat specialized solutions on 23 challenges, no manual tuning); the Claude-skill assembly is not independently benchmarked. `Workstation with GPU`.

### Verified (no changes)

- 4 Translational Medicine recipes spot-checked and refreshed to 2026-06-21 (`last_verified` bumped): interpret-clinical-variant, match-patient-to-clinical-trials, scan-adverse-events-for-drug-safety-signal, fit-survival-model-to-clinical-outcomes — all linked catalog pages resolve and source URLs current.
- benchmark-admet-property-with-pytdc spot-checked and refreshed to 2026-06-21 — pytdc/molfeat/datamol catalog pages resolve, TDC ADMET_Group leaderboard URL loads (22 datasets incl. caco2_wang).

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
