---
title: Catalog updates
parent: Updates
nav_order: 1
permalink: /updates/catalog.html
---

# Catalog updates

Reverse-chronological log of changes to the [catalog]({{ '/catalog/' | relative_url }}). Newest at the top.

<!-- Curator appends new dated entries directly below this line. -->

Older entries live in [CHANGELOG_ARCHIVE.md](CHANGELOG_ARCHIVE.md).

## 2026-08-15

### Added
- **CAN-IMMUNE** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Translational Medicine) — hosted, keyless MCP server over the Li/Purcell Lab (Monash) cancer neoantigen catalogue: ~4.49M unique mutant peptides from COSMIC and DepMap/CCLE, 12 read-only tools, and MHC class I binding predicted with NetMHCpan-EL via the IEDB API. One-line install with `claude mcp add --transport http` ([repo](https://github.com/sanjaysgk/can-immune-mcp), [connector setup](https://canelib.erc.monash.edu/connector), [MCP Registry](https://registry.modelcontextprotocol.io/v0/servers?search=can-immune))
- **Blatant-Why (BY) Protein Design Agent** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology) — MIT Claude Code scaffold for antibody, nanobody, and de novo binder design campaigns: 19 skills, 13 `/by:…` commands, and 11 bundled MCP servers driving BoltzGen, PXDesign, and Protenix, with optional cloud or local GPU compute ([repo](https://github.com/001TMF/blatant-why), [npm](https://www.npmjs.com/package/blatant-why))

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- Manifest sweep found no uncatalogued entries: `anthropics/life-sciences` (21 plugins, all covered), `anthropics/claude-plugins-official` (no new life-science plugins), and Claude Science featured connectors and research skills (zero diff). Note the `anthropics/*` marketplace manifests now resolve only at `.claude-plugin/marketplace.json` — the repository-root path returns 404.

## 2026-08-15

### Added
- **ALKYL** (Categories: Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology) — MIT Claude Code plugin packaging 27 computational-chemistry skills (RDKit, docking, MD, quantum chemistry, free energy, generative design), 22 standalone RDKit scripts, and four keyless MCP servers. The page corrects the upstream README's placeholder clone URL, records that the repo ships no `marketplace.json` (so `/plugin marketplace add` will not resolve), and warns that skills stay in the clone rather than being copied to `~/.claude/skills/` — moving the clone breaks them ([repo](https://github.com/Kdevos12/ALKYL), [plugin.json](https://github.com/Kdevos12/ALKYL/blob/master/.claude-plugin/plugin.json))

### Updated
- **Cortellis Plugin** — `last_verified` refreshed to 2026-08-15. Clarivate press release still resolves; the Cortellis Regulatory Intelligence MCP announcement date (2026-03-10) and the dual Cortellis-CRI-plus-Claude subscription requirement both re-confirmed against the primary source, with no change to availability or pricing ([Clarivate](https://clarivate.com/news/clarivate-expands-access-to-trusted-regulatory-intelligence-within-claude/))

### Flagged
- **Owkin Pathology Explorer Connector** — owkin.com resolves but no longer names Pathology Explorer anywhere; the homepage now leads with the K Pro agent. The `owkin` entry is still present in the `anthropics/life-sciences` marketplace, so the install path stands and `last_verified` was deliberately not bumped. Next run should check the Owkin product pages directly to determine whether Pathology Explorer has been folded into K Pro

### Verified (no changes)
- 2 entries re-verified against primary sources (Owkin, Cortellis — the two oldest `last_verified` dates in the catalog). The `anthropics/life-sciences` marketplace manifest was re-fetched and all 15+ plugins it lists are already catalogued. Three Chemistry candidates were evaluated and deferred with reasons rather than catalogued: SYNTHIA Agentic AI (enterprise-only, no published MCP endpoint or install path), `ghutchis/chem-skill` (README clones a placeholder repo that does not exist; no documented skills-directory install), and `cyanheads/pubchem-mcp-server` (recorded as a candidate additional install path for the existing PubChem entry rather than a duplicate page).

## 2026-08-09

### Added
- **Drug Mechanism Research (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — traces a drug from primary target through off-target binding, pathway context, the FDA label's own mechanism language, and CPIC pharmacogenomics, on a four-tier evidence hierarchy; carries the nanomolar-is-primary / micromolar-is-off-target rule and the multi-target pathway-convergence rule ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-mechanism-research/SKILL.md))
- **Drug Regulatory Research (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — the catalog's first UNII / ATC-EPC / Orange Book exclusivity skill surface: 505(b)(1) vs 505(b)(2) vs ANDA pathways, AB-vs-BX therapeutic equivalence, NCE 5 y / ODE 7 y / PED +6 mo exclusivity durations, and the rule that generic entry needs both patent expiry *and* an approved ANDA ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-regulatory/SKILL.md))
- **Clinical Trial Matching (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — ranks trials across ClinicalTrials.gov, EU CTIS, and ISRCTN (a CT.gov-only search misses EU/UK trials) with T1–T4 evidence tiers and a decomposed 0–100 Trial Match Score; page states plainly that it produces a clinician's shortlist, not a clinical recommendation ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-clinical-trial-matching/SKILL.md))
- **Clinical Trial Design (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — six-dimension feasibility scoring (≥75 HIGH / 50–74 MODERATE / <50 LOW) weighted 30/25/20/15/10, with endpoint grades A–D; upstream is explicitly precedent-based rather than first-principles math, so the page routes real sample-size work to [Power and Sample Size](power-and-sample-size.html) and [Adaptive Designs](adaptive-designs.html) ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-clinical-trial-design/SKILL.md))
- **FDA MCP Server (OpenPharma)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — MIT MCP server over the FDA Orange Book and Purple Book plus openFDA, adding patent-cliff forecasting, AB-rated therapeutic equivalents, and biosimilar interchangeability — surfaces not covered by the catalogued openFDA servers ([openpharma-org/fda-mcp](https://github.com/openpharma-org/fda-mcp))

### Updated
- **FDA MCP Server (OpenPharma)** — deferred since 2026-07-26 on an unspecified license; the GitHub license API now returns **MIT** with a `LICENSE` file, clearing the blocker. Three install-path corrections recorded while cataloguing: **no npm package exists** (both `fda-mcp` and `@openpharma-org/fda-mcp-server` 404 on the registry, so the install is build-from-source), the upstream README's `/path/to/fda-mcp-server/…` registration path does not match the repository's own directory name `fda-mcp`, and the `node build/index.js` step is a one-shot verification rather than a service to leave running.

### Flagged
- _None._

### Verified (no changes)
- Manifest sweep: `anthropics/life-sciences/.claude-plugin/marketplace.json` re-read — every plugin returned is already catalogued; no new entries. `mims-harvard/ToolUniverse/skills/` listing re-fetched — the three IDE-packaging directories (`tooluniverse-antigravity-plugin`, `tooluniverse-claude-code-plugin`, `tooluniverse-codex-plugin`) recorded as distribution wrappers, not workflows, and left out of scope.

## 2026-08-09

### Added
- **CDISC Data Handling (bioSkills)** (Categories: Translational Medicine) — the catalog's first CDISC SDTM/ADaM surface: XPT parsing with `pyreadstat` 1.2+, ADSL/BDS/OCCDS/ADTTE derivation with traceability, TEAE windows by modality (28–30 d small molecules, 60–90 d biologics, indefinite for cell/gene therapy), Define-XML 2.1, Pinnacle 21 and CDISC CORE validation ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/cdisc-data-handling/SKILL.md))
- **Power and Sample Size (bioSkills)** (Categories: Translational Medicine) — superiority / non-inferiority / equivalence sizing with the FDA 2016 M1/M2 double discount, Schoenfeld vs Lakatos under non-proportional hazards, Schuirmann TOST at 80–125%, written to CONSORT 2025 item 16a ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/power-and-sample-size/SKILL.md))
- **Bayesian Trials (bioSkills)** (Categories: Translational Medicine) — BOIN/CRM/EWOC dose-finding, RBesT MAP priors with robust mixtures, EXNEX basket designs and platform-trial patterns, against FDA Bayesian devices (2010) and drugs-draft (Jan 2026) guidance ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/bayesian-trials/SKILL.md))
- **Multiplicity and Graphical Procedures (bioSkills)** (Categories: Translational Medicine) — Bretz–Maurer–Hommel graphical procedures via `gMCP`, gatekeeping, and a Holm/Hochberg/Hommel decision tree with the PRDS check, anchored to the FDA Multiple Endpoints final guidance (Oct 2022) ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/multiplicity-graphical/SKILL.md))
- **Subgroup Analysis (bioSkills)** (Categories: Translational Medicine) — interaction testing, RERI, STEPP/SIDES/causal forests and Bayesian shrinkage, assessed against the Sun *BMJ* 2012 11-criterion checklist and EMA 2019 ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/subgroup-analysis/SKILL.md))
- **Effect Measures (bioSkills)** (Categories: Translational Medicine) — OR/RR/RD/HR/NNT with Wilson, Newcombe, MOVER, Miettinen–Nurminen, profile-likelihood and Bender intervals, plus marginal-vs-conditional estimands per the FDA 2023 covariate-adjustment guidance ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/effect-measures/SKILL.md))

### Updated
- **Curator state** — the `GPTomics/bioSkills` `clinical-biostatistics/` category is now fully worked (9 of 12 catalogued, 3 declined on overlap with `scikit-survival.md` / `statsmodels.md`) and moves to diff-only maintenance.

### Flagged
- No new flags this run.

### Verified (no changes)
- Manifest sweep: `anthropics/life-sciences/.claude-plugin/marketplace.json` re-read; every plugin returned is already catalogued, no new entries.

## 2026-08-09

### Added
- **Neural Population Analysis Guide (Claude Skill)** (Categories: Neuroscience) — the catalog's first population-geometry surface: PCA / GPFA / dPCA / jPCA selection with per-method neuron and trial minima, soft normalization at 5 spikes/s instead of z-scoring, and dimensionality chosen by parallel analysis or cross-validation rather than a variance rule ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/neural-population-analysis-guide/SKILL.md))
- **Parameter Recovery Checker (Claude Skill)** (Categories: Neuroscience) — simulate-and-refit studies that test whether a cognitive model is identifiable before its fitted parameters are interpreted; recovery bands for *r*, bias, RMSE and Bayesian coverage, plus the |r| > 0.5 parameter-tradeoff cutoff and model-recovery confusion matrix ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/parameter-recovery-checker/SKILL.md))
- **Lesion-Symptom Mapping Guide (Claude Skill)** (Categories: Neuroscience, Translational Medicine) — VLSM, multivariate SVR-LSM, disconnection and lesion network mapping in patient cohorts, with N-gated method routing, per-voxel lesion-overlap floors, cost-function masking and permutation FWE at 5,000+ permutations ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/lesion-symptom-mapping-guide/SKILL.md))
- **NetNeuroTools Guide (Claude Skill)** (Categories: Neuroscience) — connectome analysis with `netneurotools` (BSD-3-Clause): consensus networks, communication metrics, consensus modularity, spatial statistics and the spatial-autocorrelation-preserving null models that make brain-network significance testing meaningful ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/netneurotools-guide/SKILL.md))
- **Pycortex Guide (Claude Skill)** (Categories: Neuroscience) — cortical surface visualization of fMRI data with pycortex (BSD-2-Clause): 2D flatmaps, interactive 3D WebGL viewers, volume-to-surface mapping and FreeSurfer/fMRIPrep integration; Linux/macOS only ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/pycortex-guide/SKILL.md))

### Updated
- **Curator state** — recorded a per-skill front-matter finding for the `awesome_cognitive_and_neuroscience_skills` collection: the `research-literacy` required-dependency block is not universal, so the single-skill copy path differs between the "Claude Code Agent" and "Claude (AI-assisted)" authored subsets. The latter also cite no papers, so their pages route readers to the wrapped library's documentation instead.

### Verified (no changes)
- `anthropics/life-sciences` marketplace re-read; every plugin listed is already catalogued. The collection's 50-directory skill listing was re-confirmed unchanged since the 2026-08-02 audit.

## 2026-08-08

### Added
- **TAD Detection (bioSkills)** (Categories: Molecular and Cellular Biology) — first 3D-genome entry in the catalog: cooltools diamond-window insulation scores, valley-prominence boundary strength, and the multi-scale window sweep ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/hi-c-analysis/tad-detection/SKILL.md))
- **Chromatin Loop Calling (bioSkills)** (Categories: Molecular and Cellular Biology) — cooltools `dots` / chromosight / Mustache loop calling with the depth fork that routes shallow maps to aggregate peak analysis instead ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/hi-c-analysis/loop-calling/SKILL.md))
- **A/B Compartment Analysis (bioSkills)** (Categories: Molecular and Cellular Biology) — per-chromosome-arm eigendecomposition with GC phasing so the active-compartment sign is not arbitrary ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/hi-c-analysis/compartment-analysis/SKILL.md))
- **Hashtag Demultiplexing (bioSkills)** (Categories: Molecular and Cellular Biology) — HTO / MULTI-seq / CellPlex sample assignment and cross-sample doublet calling across HTODemux, MULTIseqDemux, hashsolo, demuxEM and demuxmix ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/single-cell/hashing-demultiplexing/SKILL.md))
- **Metabolite Cell Communication (bioSkills)** (Categories: Molecular and Cellular Biology) — MEBOCOST enzyme-to-sensor scoring with scFEA / Compass / NeuronChat routing and explicit limits on the double inference involved ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/single-cell/metabolite-communication/SKILL.md))

### Verified (no changes)
- `anthropics/life-sciences` marketplace manifest re-read — all listed plugins already catalogued, no new entries.

## 2026-08-08

### Added
- **Covariation Analysis (bioSkills)** (Categories: Integrative Structural and Computational Biology, Molecular and Cellular Biology) — R-scape test of whether a proposed RNA secondary structure has evolutionary support, with the statistical-power check that makes a negative result meaningful; `bioconda::rscape` 2.0.4.a confirmed as the install path ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/rna-structure/covariation-analysis/SKILL.md))
- **ncRNA Search (bioSkills)** (Categories: Integrative Structural and Computational Biology, Molecular and Cellular Biology) — Infernal covariance-model search against Rfam with clan de-overlapping and GA/TC/NC threshold guidance; `bioconda::infernal` 1.1.5 confirmed ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/rna-structure/ncrna-search/SKILL.md))
- **RNA Structure Probing (bioSkills)** (Categories: Integrative Structural and Computational Biology, Molecular and Cellular Biology) — SHAPE-MaP/DMS-MaPseq processing with ShapeMapper2 into normalized reactivities used as soft folding restraints ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/rna-structure/structure-probing/SKILL.md))
- **Geometric Analysis (bioSkills)** (Categories: Integrative Structural and Computational Biology) — Bio.PDB measurement layer for static structures: distances, dihedrals, superposition/RMSD, radius of gyration, SASA ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/geometric-analysis/SKILL.md))

### Updated
- No existing entries changed (`link_recheck: no` this slot).

### Flagged
- None.

### Verified (no changes)
- `anthropics/life-sciences` marketplace manifest re-read; all listed plugins already catalogued, no new entries.

## 2026-08-08

### Added
- **Compensation and Transformation (bioSkills)** (Categories: Immunology and Microbiology, Molecular and Cellular Biology) — spillover compensation vs spectral unmixing, then logicle/arcsinh transforms in the correct order; arcsinh cofactor 5 for CyTOF vs ~150 for fluorescence ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/compensation-transformation/SKILL.md))
- **Cytometry QC (bioSkills)** (Categories: Immunology and Microbiology, Molecular and Cellular Biology) — margin removal, flowAI/PeacoQC/flowCut time-based anomaly cleaning, CyTOF `Event_length` and dead-cell checks, batch outlier flagging ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/cytometry-qc/SKILL.md))
- **Gating Analysis (bioSkills)** (Categories: Immunology and Microbiology, Molecular and Cellular Biology) — scripted hierarchical `GatingSet`s, openCyto templates, flowDensity thresholds, FlowJo round-trip via CytoML, FMO-not-isotype boundary rule ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/gating-analysis/SKILL.md))
- **Clustering and Phenotyping (bioSkills)** (Categories: Immunology and Microbiology, Molecular and Cellular Biology) — FlowSOM/PhenoGraph/CATALYST cell-type discovery with type-vs-state marker separation and display-only embeddings ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/clustering-phenotyping/SKILL.md))
- **Cytometry Differential Analysis (bioSkills)** (Categories: Immunology and Microbiology, Molecular and Cellular Biology) — diffcyt DA/DS testing with sample-as-unit aggregation, BH FDR, and compositional validation ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/flow-cytometry/differential-analysis/SKILL.md))

### Updated
- Curator state — `GPTomics/bioSkills` queue: `flow-cytometry/` directory listing confirmed (8 skills) and recorded as near-exhausted; `microbiome/` listing confirmed (6 skills, 3 uncatalogued); `imaging-mass-cytometry/` recorded as still unmined and next in line.

### Flagged
- None.

### Verified (no changes)
- `anthropics/life-sciences` marketplace manifest re-read — all plugins already catalogued; no new entries. `link_recheck: no` this slot, so no per-entry link/pricing re-verification was performed.

## 2026-08-08

### Added
- **ChemGraph** (Categories: Chemistry) — Argonne National Laboratory MCP server that runs real molecular simulations through ASE: `molecule_name_to_smiles`, `smiles_to_coordinate_file`, `run_ase`, `extract_output_json`, against xTB/TBLite, NWChem, ORCA, MACE, and UMA backends. Resolves the Chemistry candidate deferred 2026-08-01 — the repo is Apache-2.0 ([GitHub license API](https://api.github.com/repos/argonne-lcf/ChemGraph/license)), and reading [`server_utils.py`](https://github.com/argonne-lcf/ChemGraph/blob/main/src/chemgraph/mcp/server_utils.py) showed the server defaults to **stdio**, so a plain `claude mcp add --transport stdio` snippet works and the HTTP form is documented separately as a long-lived service ([`argonne-lcf/ChemGraph`](https://github.com/argonne-lcf/ChemGraph), [PyPI 0.6.0](https://pypi.org/project/chemgraph/))

### Updated
- **XTB MCP Server** — replaced the stale "ChemGraph … not yet catalogued pending license and tool-list confirmation" note with a live cross-link, framed as input preparation vs. execution
- **BioContextAI Knowledgebase MCP** — fixed a broken Docker install path: no image is published to a registry, so the page now shows the required `git clone` + `docker build` prerequisite and states the container is a long-lived service. Added a note that the hosted `biocontext-kb.fastmcp.app` endpoint is test-only and fair-use limited. Re-verified against the upstream README (Apache-2.0, active, not renamed); `last_verified` 2026-05-20 → 2026-08-08
- **AdisInsight Plugin**, **Scholar Gateway Connector (Wiley)** — install paths re-confirmed against `anthropics/life-sciences/.claude-plugin/marketplace.json`; pricing and availability unchanged; `last_verified` 2026-05-20 → 2026-08-08

### Verified (no changes)
- Manifest sweep: all plugins in the `anthropics/life-sciences` marketplace re-confirmed present and already catalogued; no new entries. 4 entries re-verified.

## 2026-08-02

### Added
- **ADMET Prediction (ToolUniverse Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery) — five-phase ADMET profiling that pairs ADMET-AI/SwissADME predictions with experimental PubChemTox data and grades every finding T1–T3, so readers can tell a measurement from a model output ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-admet-prediction/SKILL.md))
- **Dose-Response Analysis (ToolUniverse Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery, Molecular and Cellular Biology) — 4PL/Hill curve fitting for IC50/EC50 with explicit fit-quality gatekeeping (r² ≥ 0.95 to endorse a potency comparison; biphasic data rejected outright) ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-dose-response/SKILL.md))
- **Cell Line Profiling (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — ranks cancer cell lines for an experiment across Cellosaurus identity checks, DepMap dependencies, COSMIC/CCLE mutations, and PharmacoDB drug sensitivity ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-cell-line-profiling/SKILL.md))
- **Chemical Sourcing (ToolUniverse Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery) — vendor search across ZINC, Enamine, eMolecules, and Mcule with purity floors, per-mg price normalization, and a Tanimoto ≥ 0.7 purchasable-analog fallback ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-chemical-sourcing/SKILL.md))

### Deferred
- **Cicatriiz/healthcare-mcp-public** (MIT) — one server bundling FDA, PubMed, medRxiv, clinical trials, ICD-10, and DICOM metadata; deferred because five of those surfaces are already catalogued discretely and the repo has not been pushed since 2025-08-16.
- **cyanheads/pubchem-mcp-server** — should be folded into the existing PubChem entry as an alternative install path rather than duplicated, once its license and registration snippet are confirmed.
- **FDB MedProof MCP** — commercial medication-decision-support server (GA 2026-04); no public enable path or pricing published.

### Verified (no changes)
- `anthropics/life-sciences` marketplace re-swept — all 21 plugins already catalogued; no new entries.

## 2026-08-02

### Added
- **OMOPHub MCP Server** (Categories: Translational Medicine) — 11 tools over the OHDSI OMOP standardized vocabularies (SNOMED CT, ICD-10, RxNorm, LOINC, 100+ others): concept search, semantic search, cross-vocabulary mapping, hierarchy traversal, and FHIR coding resolution, without a local ATHENA load. MIT, npm `@omophub/omophub-mcp` 1.5.3, Node ≥ 20, free API key required ([source](https://github.com/OMOPHub/omophub-mcp))
- **pyomop** (Categories: Translational Medicine) — Python OMOP CDM toolkit that ships an MCP server: 8 tools for CDM schema inspection, validated SQL execution, and loading the OHDSI Eunomia demo dataset across SQLite/PostgreSQL/MySQL. GPL-3.0, PyPI 6.4.0, Python 3.11+ ([source](https://github.com/dermatologist/pyomop))
- **Adaptive Designs (bioSkills)** (Categories: Translational Medicine) — plans group-sequential (O'Brien–Fleming/Pocock/Lan–DeMets), sample-size re-estimation (Friede–Kieser, Cui–Hung–Wang, Mehta–Pocock promising zone), seamless Phase 2/3, enrichment and RAR trials with `rpact`/`gsDesign`, against FDA 2019 adaptive-designs and 2022 master-protocols guidance plus the ICH E20 Step 2b draft ([source](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/adaptive-designs/SKILL.md))
- **Missing Data Sensitivity (bioSkills)** (Categories: Translational Medicine) — ICH E9(R1) estimand-first missing-data workflow: MMRM with Kenward–Roger via `mmrm`, reference-based MI (J2R/CR/CIR/LMCF) via `rbmi`, Permutt tipping-point analysis, pattern-mixture restrictions, and Rubin's-vs-frequentist variance reconciliation ([source](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/missing-data-sensitivity/SKILL.md))
- **Trial Reporting (bioSkills)** (Categories: Translational Medicine) — CONSORT 2025 / SPIRIT 2025 / ICH E9(R1)-conformant statistical reporting: estimand attributes, ITT/FAS/PP/Safety populations, `tableone` Table 1 with SMD > 0.1 imbalance flagging, MMRM primary analysis, and Bretz–Maurer graphical multiplicity via `gMCP` ([source](https://github.com/GPTomics/bioSkills/blob/main/clinical-biostatistics/trial-reporting/SKILL.md))

### Updated
- No existing entries changed. Link/pricing recheck was not scheduled for this slot (`link_recheck: no`).

### Flagged
- No new flags this run.

### Verified (no changes)
- All 21 plugins in the `anthropics/life-sciences` marketplace manifest re-confirmed present and already catalogued.

## 2026-08-02

### Added
- **DeepLabCut (Claude Skill)** (Categories: Neuroscience) — markerless animal pose estimation: 9-stage project pipeline, SuperAnimal zero-shot models, multi-animal and 3D tracking ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/deeplabcut/SKILL.md))
- **Calcium Imaging Analysis Guide (Claude Skill)** (Categories: Neuroscience) — motion correction, CNMF/CNMF-E/Cellpose ROI extraction, neuropil correction, dF/F and spike inference with stated QC thresholds ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/calcium-imaging-analysis-guide/SKILL.md))
- **Drift-Diffusion Model (Claude Skill)** (Categories: Neuroscience) — selecting, fitting and validating DDMs of two-choice RT data with EZ-diffusion, fast-dm, PyDDM or HDDM ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/drift-diffusion-model/SKILL.md))
- **Optogenetics Protocol Designer (Claude Skill)** (Categories: Neuroscience) — opsin, wavelength, irradiance, pulse-protocol, fiber and control-condition selection for circuit manipulation experiments ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/optogenetics-protocol-designer/SKILL.md))
- **Signal Detection Analysis (Claude Skill)** (Categories: Neuroscience) — d′, criterion, β and c′ with the log-linear extreme-value correction and non-parametric alternatives ([SKILL.md](https://github.com/HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills/blob/master/skills/signal-detection-analysis/SKILL.md))

### Updated
- **`HaoxuanLiTHUAI/awesome_cognitive_and_neuroscience_skills`** — audit completed (deferred since 2026-07-12): repo-level MIT, default branch `master` (not `main`), Claude Code plugin marketplace install confirmed, 50 skill directories of which ~10 are meta. Every skill carries `review_status: ai-generated`, so all five new pages lead their Notes with a bolded verify-before-use caveat; most skills require the collection's `research-literacy` skill, which the single-skill install snippets now copy alongside.
- **HED-MCP** (deferred candidate) — re-checked: PyPI `hed-mcp` still returns 404, so it remains not installable.
- **NWB / NeuroConv MCP gap** — reconfirmed absent; recorded a name-collision warning that `mcp.science`'s `nemad` server is a materials database, not neuroscience.

### Flagged
- No new flags this run.

### Verified (no changes)
- All 21 plugins in `anthropics/life-sciences/.claude-plugin/marketplace.json` re-confirmed present and already catalogued (`link_recheck: no` this slot, so no per-page link/pricing recheck was run).

## 2026-08-01

### Added

- **Doublet Detection (bioSkills)** (Categories: Molecular and Cellular Biology) — Molecular and Cellular Biology directed pass. Flags multi-cell droplets in scRNA-seq with scDblFinder 1.16+, Scrublet (via scanpy 1.10+) and DoubletFinder before clustering: per-sample detection ahead of integration, expected rate ~0.8% per 1,000 recovered cells (`dbr.per1k = 0.008`), the total-lane-not-demultiplexed-subset rule for multiplexed pools, `modelHomotypic()` adjustment, and flag-and-inspect over blind deletion ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/single-cell/doublet-detection/SKILL.md))
- **CNV Inference (bioSkills)** (Categories: Molecular and Cellular Biology, Translational Medicine) — infers chromosome-scale copy-number alterations from tumor scRNA-seq to separate malignant from normal cells and call subclones, across inferCNV 1.18+ (reference-based), copyKAT 1.1+ / SCEVAN 1.0+ (reference-free) and Numbat 1.4+ (allele-aware); includes the droplet-vs-Smart-seq `cutoff` split (0.1 vs 1) and the lineage-marker/allele cross-check before a cell is labelled malignant ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/single-cell/cnv-inference/SKILL.md))
- **Perturb-seq Analysis (bioSkills)** (Categories: Molecular and Cellular Biology) — single-cell CRISPR screen analysis with Pertpy 0.9+, Mixscape escaper removal, SCEPTRE 0.10+ conditional resampling and E-distance effect sizes; encodes the rule that the replication unit is the transfection rather than the cell (pseudobulk over ≥2–3 replicates), plus Milo/scCODA compositional testing and a whole-perturbation-holdout check on perturbation-prediction foundation models ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/single-cell/perturb-seq/SKILL.md))
- **scATAC Analysis (bioSkills)** (Categories: Molecular and Cellular Biology) — single-cell ATAC-seq from fragment QC to motif deviations with Signac 1.13+/Seurat 5.0+, ArchR 1.0+ or SnapATAC2 2.x: TF-IDF/LSI with the depth-correlated first component diagnosed and dropped, per-cluster consensus peak merging, depth-covariate differential accessibility, and chromVAR scored against GC-matched backgrounds ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/single-cell/scatac-analysis/SKILL.md))
- **Lineage Tracing (bioSkills)** (Categories: Molecular and Cellular Biology) — reconstructs clonal phylogenies from CRISPR scars, LARRY/CellTag barcodes or mtDNA mutations using Cassiopeia 2.0+, Startle and CoSpar 0.3+, with cross-solver Robinson–Foulds / triplets-correct robustness checks and explicit homoplasy and dropout handling. The page installs Cassiopeia from GitHub, not PyPI: the `cassiopeia-lineage` distribution is still at 1.0.4 while the skill targets 2.0+ ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/single-cell/lineage-tracing/SKILL.md), [PyPI](https://pypi.org/project/cassiopeia-lineage/))

### Verified (no changes)

- Manifest sweep: all 18 plugins currently listed in [`anthropics/life-sciences`](https://raw.githubusercontent.com/anthropics/life-sciences/main/.claude-plugin/marketplace.json) re-confirmed present and already catalogued — no new entries. `biorxiv` and `clinical-trials` remain flagged (upstream `mcp.deepsense.ai` endpoint down).
- bioSkills `single-cell/` directory fully enumerated (17 skills). The 12 not catalogued this run were checked against existing pages; most overlap current coverage (Scanpy, AnnData, Single-cell RNA QC, CellTypist, popV, CellChat, LIANA, Harmony, MUON, MOFA+, scVelo, CellRank). `hashing-demultiplexing` and `metabolite-communication` recorded as the two genuinely-uncovered next-run candidates.

## 2026-08-01

### Added
- **Rosetta MCP Server** (Categories: Integrative Structural and Computational Biology) — MCP server exposing 18 tools over Rosetta, PyRosetta and Biotite: runs and validates RosettaScripts XML (including against the Rosetta XSD), scores structures with per-residue breakdown, fetches live mover/score-function docs, and translates protocols between the three APIs with design operations flagged as Rosetta-only. Node 14+ / Python 3.8+, stdio, configured through `PYTHON_BIN` and `ROSETTA_BIN`. Upstream documents Cursor only — the page carries constructed Claude Code and Claude Desktop equivalents, labelled as such ([repo](https://github.com/Arielbs/rosetta-mcp-server), [npm](https://www.npmjs.com/package/rosetta-mcp-server), [RosettaCommons write-up](https://rosettacommons.org/2025/10/20/rosetta-cursor-simplifying-protein-design-with-ai-assistance/))
- **Structure Validation (bioSkills)** (Categories: Integrative Structural and Computational Biology) — decides whether a model or one region of it is reliable enough to build on: resolution, the R-free-minus-R-work overfitting gap, within-structure B-factor z-scoring, MolProbity clashscore/Ramachandran/rotamer/cis-non-proline outliers via `phenix.molprobity`, pLDDT bands and PAE for predicted models, and cryo-EM global-vs-local resolution (FSC 0.143 vs 0.5) ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/structure-validation/SKILL.md))
- **Binding Site Detection (bioSkills)** (Categories: Drug Repurposing and Discovery, Integrative Structural and Computational Biology) — de novo pocket detection on apo structures with fpocket, P2Rank, CASTp and DoGSiteScorer, plus cryptic-pocket tracking over an MD ensemble with mdpocket; explicit that a geometric cavity is a hypothesis and that holo-trained druggability scores under-detect apo and shallow sites ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/binding-site-detection/SKILL.md))
- **Interface Analysis (bioSkills)** (Categories: Immunology and Microbiology, Integrative Structural and Computational Biology) — protein–protein and protein–ligand interface mapping with Bio.PDB: cutoff choice with stated rationale, `NeighborSearch` contacts, `ShrakeRupley` buried surface area, PDBePISA crystal-packing check, and the biological-assembly-not-asymmetric-unit rule ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/interface-analysis/SKILL.md))
- **Structure Preparation (bioSkills)** (Categories: Integrative Structural and Computational Biology) — makes a deposited or predicted structure docking-, MD- or electrostatics-ready with PDBFixer, `reduce`, PROPKA 3 and PDB2PQR: hydrogens, His tautomers and Asn/Gln/His flips, pKa-shifted protonation at a stated pH, missing atoms and short loops recorded as disorder hypotheses, and PQR output for Poisson–Boltzmann ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/structure-preparation/SKILL.md))

### Flagged
- **Rosetta MCP Server** — MIT is declared only in the npm package manifest; no `LICENSE` file is committed to the GitHub repo, so redistribution terms are marked `Unverified` inline. Separately, Rosetta and PyRosetta themselves require a University of Washington licence (free for academic use).

### Verified (no changes)
- All 21 `anthropics/life-sciences` marketplace plugins re-confirmed present and already catalogued; no new entries from the manifest sweep.
- Directed-pass negatives reconfirmed: no Claude-installable cryo-EM wrapper for RELION or cryoSPARC exists (the `cryosparc-tools` Python API remains unwrapped; `cryo-mcp` is an unrelated blockchain server), and no standalone TM-align / Foldseek / FoldMason alignment server — those algorithms reach Claude only through the existing Protein MCP Server and Foldseek entries.

## 2026-08-01

### Added
- **MetaPhlAn Profiling (bioSkills)** (Categories: Immunology and Microbiology) — MetaPhlAn 4 clade-specific marker profiling of shotgun metagenomes to species/SGB cell fractions, with `--index` pinning and unknown-fraction guidance ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/metaphlan-profiling/SKILL.md))
- **Functional Profiling (bioSkills)** (Categories: Immunology and Microbiology) — HUMAnN 3 tiered search for species-stratified gene-family and MetaCyc pathway abundances ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/functional-profiling/SKILL.md))
- **Strain Tracking (bioSkills)** (Categories: Immunology and Microbiology) — sub-species strain resolution and shared-strain testing with inStrain popANI, StrainPhlAn, MIDAS2, StrainGE and skani ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/strain-tracking/SKILL.md))
- **Immunogenicity Scoring (bioSkills)** (Categories: Immunology and Microbiology, Translational Medicine) — neoantigen/epitope ranking by likely T-cell response via NeoFox, PRIME2.0, BigMHC-IM and pVACtools tiering ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/immunogenicity-scoring/SKILL.md))
- **Differential Abundance (bioSkills)** (Categories: Immunology and Microbiology) — compositionally-aware microbiome differential-abundance testing with a required multi-tool consensus ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/microbiome/differential-abundance/SKILL.md))

### Verified (no changes)
- Manifest sweep: 21 `anthropics/life-sciences` marketplace plugins re-confirmed present and already catalogued.

## 2026-08-01

### Added
- **XTB MCP Server** (Categories: Chemistry) — MIT MCP server that builds, validates, and explains `xtb` semi-empirical quantum-chemistry input decks (GFN0/GFN1/GFN2/GFN-FF) across 10 tools covering optimizations, frequencies, scans, metadynamics, ONIOM QM/MM, and spectroscopy setups ([PhelanShao/xtb-mcp-server](https://github.com/PhelanShao/xtb-mcp-server))
- **Materials Project MCP Server** (Categories: General-Purpose Utilities) — MIT server in the `mcp.science` collection giving Claude 7 tools over the Materials Project crystal-structure database: formula search, CIF/POSCAR export, supercell and moiré-bilayer construction; launched with `uvx mcp-science materials-project` ([pathintegral-institute/mcp.science](https://github.com/pathintegral-institute/mcp.science))

### Updated
- **UniProt MCP Server** — `Pricing` corrected from "Free / OSS (MIT)" to "Free to use" with an inline `**Unverified —**` on redistribution: the committed `LICENSE` is a restrictive non-commercial grant while `package.json` and the README claim MIT. Notes now tell readers the server is fine to run (thin read-only client over the public UniProt REST API) but should not be vendored or redistributed until upstream resolves the conflict ([Augmented-Nature/UniProt-MCP-Server](https://github.com/Augmented-Nature/UniProt-MCP-Server))
- **BioMCP** — re-verified live: MIT, `biomcp-cli` on PyPI, `biomcp serve` launch command confirmed against [biomcp.org](https://biomcp.org/)

### Flagged
- **UniProt MCP Server** — self-contradictory upstream license (restrictive non-commercial `LICENSE` vs. MIT in `package.json`/README); last upstream push 2025-12-21

### Verified (no changes)
- 4 entries re-verified — Synapse.org Connector and scientific-problem-selection re-confirmed present in the `anthropics/life-sciences` marketplace manifest; all 21 plugins in that manifest re-checked and already catalogued.

## 2026-07-27 (user request #74)

Immediate-fulfillment run for @goodb's recipe-block chain (#74): the recipes curator blocked a QUINT-replacement implant-localization recipe on two uncatalogued components, `brainglobe-atlasapi` and `DeepSlice`. Both were verified as real, actively-maintained, and cleanly-licensed — but neither is catalogable: each is a **bare PyPI library with no Claude-installable Skill / MCP / plugin / connector**, the same out-of-scope bar applied to raw RDKit/Scanpy. Verified licenses banked for the moment a wrapper surfaces; recorded under Deferred. No page shipped.

### Declined
- **brainglobe-atlasapi** (BSD-3-Clause; [JOSS 2020](https://doi.org/10.21105/joss.02668)) and **DeepSlice** (MIT, © 2023 Harry Carey; [Carey et al., *Nat Commun* 2023](https://doi.org/10.1038/s41467-023-41645-4)) — out of scope as bare `pip install` libraries with no upstream `SKILL.md` or MCP wrapper (checked PyPI, both repos, and the NeuroClaw / SciAgent / K-Dense / bioSkills collections). Deferred; revisit if a community wrapper ships.

## 2026-07-26 (Drug Repurposing and Discovery slot)

Drug Repurposing and Discovery directed pass plus a manifest sweep. The `anthropics/life-sciences` `.claude-plugin/marketplace.json` (21 plugin entries) was re-fetched and diffed against the catalog — all entries already covered (medidata, consensus, cortellis, adisinsight all present; biorxiv@life-sciences / clinical-trials@life-sciences remain DOA per the standing flags). Drug-discovery seed queries (`DrugBank MCP server`, `drug repurposing agent MCP server`, `Open Targets standalone MCP`, `ADMET prediction Claude skill/MCP`) reconfirmed existing coverage (DrugBank, Open Targets, Inductive Bio ADMET) and surfaced two new verifiable, cleanly-licensed, installable servers.

### Added
- **ADMETlab MCP Server** (Categories: Chemistry, Drug Repurposing and Discovery) — Apache-2.0 self-hostable HTTP MCP server wrapping the ADMETlab 3.0 API (4 tools: molecule washing, SVG rendering, ADMET prediction, CSV retrieval); keyless free/self-hosted alternative to the enterprise-gated Inductive Bio connector ([GitHub](https://github.com/ToxMCP/admetlab-mcp)).
- **Drug Pipeline MCP Server** (Categories: Drug Repurposing and Discovery, Translational Medicine) — MIT server (PyPI `drug-pipeline-mcp`) aggregating ClinicalTrials.gov + openFDA + RxNorm + PubMed + EMA + DailyMed + Open Targets + MyChem.info into 6 source-traceable pipeline-intelligence tools; adds cross-source synthesis + EMA approval coverage beyond the discrete openFDA/ClinicalTrials.gov entries ([GitHub](https://github.com/DasClown/drug-pipeline-mcp)).

### Updated
- **DrugBank MCP Server** — `last_verified` bumped to 2026-07-26 (openpharma-org repo confirmed active, MIT, 17,430 drugs, npm/node install path unchanged) ([GitHub](https://github.com/openpharma-org/drugbank-mcp-server)).

### Verified (no changes)
- Manifest sweep confirmed no new `anthropics/life-sciences` life-science entries (21 plugins, all catalogued). Open Targets standalone MCP (`opentargets/open-targets-platform-mcp`) already cited on the flagged `open-targets.md`; Inductive Bio ADMET connector already covered.

## 2026-07-26 (Translational Medicine slot)

Translational Medicine directed pass plus a manifest sweep. The `anthropics/life-sciences` `.claude-plugin/marketplace.json` (18 plugin entries) and the Claude Science *Featured connectors + Research skills* list were re-fetched and diffed against the catalog — all entries already covered (biorxiv@life-sciences / clinical-trials@life-sciences remain DOA per the standing flags). Translational seed queries (`FHIR MCP server Claude`, `ClinicalTrials.gov MCP server`, `regulatory submission FDA 510k eCTD MCP/skill`, `OpenFDA drug adverse event MCP server`, `CMS Blue Button / Medicare claims MCP server`) surfaced two new verifiable, cleanly-licensed, installable servers; the FHIR and ClinicalTrials.gov candidates were already covered (`fhir-momentum`, `fhir-wso2`, `clinicaltrials-gov-mcp`).

### Added
- **OpenFDA MCP Server (cyanheads)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — Apache-2.0 npm server (`@cyanheads/openfda-mcp-server`) federating the full openFDA API across drugs, food, devices (510k/PMA), veterinary, shortages, and recalls (14 tools) with a public HTTP instance; fills the device-clearance gap that the deferred Augmented-Nature variant left open ([GitHub](https://github.com/cyanheads/openfda-mcp-server)).
- **CMS data.gov MCP Server** (Categories: Translational Medicine) — MIT server (`@clarify/cms-datagov-mcp-server`) over data.cms.gov statistical datasets (provider enrollment, hospital quality, spending); distinct from the Anthropic CMS Coverage policy MCP ([GitHub](https://github.com/clarifyhealth/cms-datagov-mcp-server)).

### Updated
- **OpenFDA MCP Server (ythalorossy)** — `last_verified` bumped to 2026-07-26 (npm `@ythalorossy/openfda` MIT + openFDA rate-limit facts re-confirmed); Notes now cross-link the broader cyanheads server ([npm](https://www.npmjs.com/package/@ythalorossy/openfda)).

### Flagged
- **openpharma-org/fda-mcp** and **openpharma-org/medicare-mcp** — deferred: no explicit upstream license (same bar as ChemCP / PLSDB). fda-mcp adds Orange Book / Purple Book patent-cliff + biosimilar intelligence; medicare-mcp adds CMS provider/prescriber/hospital-quality tools. Revisit once each declares a license.

## 2026-07-26 (Neuroscience slot)

Neuroscience directed pass plus a manifest sweep. The `anthropics/life-sciences` `.claude-plugin/marketplace.json` (18 plugin entries) was re-fetched and diffed against the catalog — all entries already covered. Neuroscience seed queries (`Allen Brain Atlas MCP server`, `Neurodata Without Borders NWB MCP server Claude skill`, `neuroscience MCP EEG spike sorting electrophysiology SKILL.md`, `DANDI archive / calcium imaging / connectome MCP`) surfaced no new *verifiable, installable* candidates — the neuroscience surface is heavily covered by the batch-ingested NeuroClaw (68 pages) and NeuroForge collections plus discrete `neurosift`, `allenbrain`, `openneuro`, `spikelab`, and `neuropixels-analysis` entries. The MCP Registry `brain` search returned only memory/business servers (no neuroscience). NeuroClaw README re-checked: still 86 skills, no upstream additions. No new entries this run.

### Updated
- **SpikeLab** — `last_verified` bumped to 2026-07-26; PyPI `spikelab` 0.1.2 (MIT, released 2026-05-29) and `braingeneers/SpikeLab` repo confirmed live, install paths and pricing unchanged ([PyPI](https://pypi.org/project/spikelab/)).
- **Neurosift Tools MCP** — `last_verified` bumped to 2026-07-26; `magland/neurosift-mcps` repo confirmed live (license still unset, already noted on page), plugin-marketplace and stdio install paths unchanged ([GitHub](https://github.com/magland/neurosift-mcps)).

### Verified (no changes)
- Manifest sweep confirmed no new `anthropics/life-sciences` life-science entries. Neuroscience directed pass reconfirmed standing deferrals: `bendichter/dandi-query-mcp` (boilerplate tools), `neuromechanist/hed-mcp` (not yet on PyPI), `brain-bbqs/NeuroMCP` (repo 404). `openneuro.md` left as verifier-flagged broken (repo/endpoint 404).

## 2026-07-25 (Molecular and Cellular Biology slot)

Molecular and Cellular Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` `.claude-plugin/marketplace.json` (18 plugin entries) and `anthropics/claude-plugins-official` were re-fetched and diffed against the catalog — all entries already covered (Boltz is the only life-science plugin in the official marketplace and is present as `boltz.md`). M&CB seed queries (`single-cell RNA-seq MCP server Scanpy Bioconductor`, `Ensembl Bioconductor CRISPR MCP server Claude skill`, `Geneformer/scGPT MCP server`, `CRISPR guide RNA design MCP server`) reconfirmed existing single-cell coverage (scanpy-mcp/scmcp/LIANA/decoupler/CellRank, CELLxGENE, scvi-tools) and the standing Geneformer/scGPT-wrapper and standalone-CRISPR-gRNA-design gaps; one new install path for an already-catalogued tool was surfaced.

### Updated
- **gget** — added the `longevity-genie/gget-mcp` MCP-server install path (MIT, PyPI `gget-mcp`, 13 keyless tools, `uvx --from gget-mcp@latest stdio`) as an alternative to the catalogued K-Dense/SciAgent skill packagings; Notes + Sources now distinguish the skill vs. MCP surfaces; `last_verified` bumped to 2026-07-25 ([GitHub](https://github.com/longevity-genie/gget-mcp)).

### Verified (no changes)
- Manifest sweep confirmed no new `anthropics/life-sciences` or `claude-plugins-official` life-science entries. `scanpy.md` (scmcphub family), `ensembl.md` (effieklimi + Pipeworx HTTP variant already noted), `cellxgene-census.md`, and `encode-toolkit.md` spot-checked and current; Geneformer/scGPT foundation-model wrapper and standalone CRISPR gRNA-design MCP/Skill gaps remain open (deferred).

## 2026-07-25 (Integrative Structural and Computational Biology slot)

Integrative Structural and Computational Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` `.claude-plugin/marketplace.json` (19 plugin entries) and the Claude Science featured-connectors/skills list were re-fetched and diffed against the catalog — all entries already covered (the featured connectors decompose to source-level pages already present; featured research skills — AlphaFold2, Boltz-2, Chai-1, ESMFold2, OpenFold3, ProteinMPNN/LigandMPNN/SolubleMPNN, DiffDock, ESM-2, Evo 2, Borzoi, scGPT, scvi-tools — all present). Structural seed queries (`RCSB PDB MCP server protein structure ChimeraX MCP`, `molecular dynamics MCP server GROMACS OpenMM cryo-EM Claude skill`) reconfirmed the standing cryo-EM-wrapper gap and existing GROMACS/OpenMM/PDB/PyMOL coverage; two genuinely-new installable structural-biology MCP servers were surfaced and catalogued.

### Added
- **Protein MCP Server** (Categories: Integrative Structural and Computational Biology) — keyless federated protein-structure engine over RCSB PDB + AlphaFold DB + 3D-Beacons + UniProt + InterPro + Foldseek; 7 tools for search, fetch, sequence/fold-homolog search, ligand tracking, TM-align/jFATCAT comparison, collection profiling, and annotation. Apache-2.0, npm `@cyanheads/protein-mcp-server` (stdio) plus a public HTTP instance ([GitHub](https://github.com/cyanheads/protein-mcp-server)).
- **ChimeraX MCP Server** (Categories: Integrative Structural and Computational Biology) — natural-language UCSF ChimeraX driver: 39 tools for structure open/edit/mutate/minimize, surface/cartoon/label visualization, distance/angle/RMSD/contact measurement, and selection; ChimeraX auto-launches. MIT, PyPI `chimerax-mcp` ([GitHub](https://github.com/mahynotch/chimerax-mcp)).

### Verified (no changes)
- Manifest sweep confirmed no new `anthropics/life-sciences` or Claude Science featured-connector/skill entries. `pdb.md` and `pymol.md` (structural neighbors) spot-checked and current; cryo-EM (RELION/cryoSPARC/CTFFIND) wrapper gap remains open (deferred).

## 2026-07-25 (Immunology and Microbiology slot)

Immunology and Microbiology directed pass plus a manifest sweep. The `anthropics/life-sciences` plugin directories and the Claude Science featured-connectors/skills list were re-checked against the catalog — all entries already covered (the Claude Science featured connectors decompose to sources already catalogued at source-level; featured research skills — AlphaFold2, Boltz-2, Chai-1, ESMFold2, OpenFold3, ProteinMPNN, DiffDock, ESM-2, Evo 2, Borzoi, scGPT, scvi-tools — all present). Five genuinely-new immunology/microbiology skills were drawn from the deferred `GPTomics/bioSkills` (MIT) queue and catalogued; each SKILL.md, its tool/database list, and the MIT license were verified against the upstream repo this run.

### Added
- **Repertoire Visualization (bioSkills)** (Categories: Immunology and Microbiology) — TCR/BCR figure skill: VDJtools + R circlize/iNEXT + Python networkx/rapidfuzz for V-J chord diagrams, spectratypes, clonal tracking, rarefaction/extrapolation, overlap heatmaps and similarity networks, with Morisita-Horn/Jaccard depth-robust metric guidance ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/repertoire-visualization/SKILL.md)).
- **Specificity Annotation (bioSkills)** (Categories: Immunology and Microbiology) — TCR/BCR antigen-specificity annotation (VDJdb/McPAS/IEDB+TCRMatch), clustering (tcrdist3/GLIPH2/GIANA/clusTCR), and generation-probability nulls (OLGA/IGoR/SONIA), treating matches as hypotheses ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/specificity-annotation/SKILL.md)).
- **VDJtools Analysis (bioSkills)** (Categories: Immunology and Microbiology) — repertoire diversity (Hill orders q=0/1/2), depth-normalized overlap, clonality, and V/J segment usage via VDJtools/immunarch ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/vdjtools-analysis/SKILL.md)).
- **Amplicon Processing (bioSkills)** (Categories: Immunology and Microbiology) — 16S/ITS ASV inference with DADA2: cutadapt primer removal, per-run error modeling, pair merging, chimera + decontam removal ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/microbiome/amplicon-processing/SKILL.md)).
- **Taxonomy Assignment (bioSkills)** (Categories: Immunology and Microbiology) — 16S/ITS/18S ASV classification via DADA2/DECIPHER IDTAXA/QIIME2 against SILVA/GTDB/Greengenes2/UNITE/PR2, with region-specific training and confidence-threshold guidance ([SKILL.md](https://github.com/GPTomics/bioSkills/blob/main/microbiome/taxonomy-assignment/SKILL.md)).

### Verified (no changes)
- Manifest sweep confirmed no new `anthropics/life-sciences` or Claude Science featured-connector/skill entries. bioSkills MIT `LICENSE` and the five new `SKILL.md` directories confirmed live upstream this run.

## 2026-07-25 (Chemistry slot)

Chemistry directed pass plus a manifest sweep. The `anthropics/life-sciences` `.claude-plugin/marketplace.json` (~17 entries) was re-fetched and diffed against the catalog — all entries already covered (pubmed, biorender, synapse, wiley-scholar-gateway, biorxiv, clinical-trials, chembl, owkin, open-targets, tooluniverse, and the local skills). Chemistry seed queries (`cheminformatics MCP server RDKit`, `MCP server SMILES publication reaction scheme mechanism`, `retrosynthesis MCP`, `Polaris drug discovery MCP`) reconfirmed existing RDKit coverage (`chemcp`, `rdkit-mcp`, `rdkit-skill`, `rdkit-agent`) and the standing retrosynthesis/Polaris gaps; one genuinely-new installable ChemDraw-CDXML MCP server was surfaced and catalogued.

### Added
- **CDXML Toolkit** (Categories: Chemistry) — MIT-licensed MCP server + Python toolkit (PyPI `cdxml-toolkit` v0.5.17) exposing 15 grounded chemistry tools for ChemDraw CDXML office automation: molecule/reaction rendering to publication-ready CDXML, structure extraction from images via DECIMER OCR, ELN/LCMS/NMR parsing, and PPTX/DOCX ChemDraw-OLE embed/extract. Windows + ChemDraw 2015+ required ([GitHub](https://github.com/leehiufung911/cdxml-toolkit), [PyPI](https://pypi.org/project/cdxml-toolkit/)).

### Verified (no changes)
- Manifest sweep confirmed no new `anthropics/life-sciences` entries; ChEMBL (`chembl.md`, last_verified 2026-07-15) spot-checked and current. Chemistry seed queries reconfirmed existing RDKit-based coverage; the OSS retrosynthesis-wrapper and Polaris-MCP gaps remain open (deferred).

