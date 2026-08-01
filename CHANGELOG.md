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

## 2026-07-19 (Drug Repurposing and Discovery slot)

Drug Repurposing and Discovery directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `anthropics/claude-plugins-official` marketplaces were re-fetched and diffed against the catalog — all life-science entries already covered. The Claude Science featured-connectors/skills list was re-checked (no new source-level additions). Seed queries (`DrugBank MCP server`, `drug repurposing agent MCP`) reconfirmed existing coverage (`drugbank.md` already carries the `openpharma-org` MCP + official hosted MCP + SciAgent paths). Four genuinely-new drug-discovery skills were drawn from the deferred `mims-harvard/ToolUniverse/skills/` queue and catalogued.

### Added
- **Small Molecule Discovery (ToolUniverse Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery) — 6-phase compound workflow (identity → analog search → ChEMBL/BindingDB bioactivity → SwissADME/ADMET-AI drug-likeness → SwissTargetPrediction → eMolecules/Enamine sourcing) ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-small-molecule-discovery/SKILL.md)).
- **Chemical Safety (ToolUniverse Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery, Translational Medicine) — 8-phase toxicology pipeline (ADMET-AI + CTD + PubChemTox + AOPWiki + STITCH + ChEMBL structural alerts + FDA/DrugBank) with Critical/High/Medium/Low risk grading ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-chemical-safety/SKILL.md)).
- **Cancer Genomics TCGA (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — 6-phase TCGA/GDC cohort analysis (clinical → somatic mutations → Progenetix CNV → GDC survival → OncoKB variant interpretation) ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-cancer-genomics-tcga/SKILL.md)).
- **Rare Disease Genomics (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — 9-phase Orphanet → HPO → causative genes → GenCC validity → ClinVar → epidemiology → trials → Europe PMC → report workflow with repurposing leads ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-rare-disease-genomics/SKILL.md)).

### Verified (no changes)
- **ToolUniverse** base page re-verified (skills directory + `uvx tooluniverse` install path confirmed against upstream; `last_verified` bumped to 2026-07-19). Manifest sweep confirmed no new `anthropics/life-sciences`, `anthropics/claude-plugins-official`, or Claude Science entries; DrugBank / drug-repurposing seed queries reconfirmed existing coverage.

## 2026-07-19 (Translational Medicine slot)

Translational Medicine directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`, ~19 entries) and `anthropics/claude-plugins-official` marketplaces were re-fetched and diffed against the catalog — all entries already covered. The Claude Science featured-connectors/skills list was re-checked (no new source-level additions). FHIR and ClinicalTrials.gov seed queries reconfirmed existing coverage (`fhir-wso2`, `fhir-momentum`, `clinicaltrials-gov-mcp`); the `AWS HealthLake MCP server` query surfaced one genuinely-new installable server. Also resolved the standing `anthropics/healthcare` deprecation flag by finishing the consolidated-plugin migration for the remaining pages.

### Added
- **AWS HealthLake MCP Server** (Categories: Translational Medicine) — Apache-2.0 MCP server (`awslabs/mcp`, PyPI `awslabs.healthlake-mcp-server`) exposing 11 tools over AWS HealthLake FHIR datastores: CRUD, advanced search, `patient_everything`, and bulk import/export jobs, with automatic datastore discovery and a `--readonly` safety flag; HIPAA-eligible on AWS ([GitHub](https://github.com/awslabs/mcp/tree/main/src/healthlake-mcp-server), [docs](https://awslabs.github.io/mcp/servers/healthlake-mcp-server), [AWS blog](https://aws.amazon.com/blogs/industries/building-healthcare-ai-agents-with-open-source-aws-healthlake-mcp-server/)).

### Updated
- **clinical-trial-protocol**, **fhir-developer** — install snippets now point at the consolidated `healthcare@healthcare` plugin (the standalone `@healthcare` plugin names are deprecated upstream per the re-fetched `anthropics/healthcare` marketplace.json).
- **CMS Coverage MCP**, **NPI Registry MCP** — install snippets migrated to `healthcare@healthcare` and given literal hosted HTTP endpoints (`https://hcls.mcp.claude.com/cms_coverage/mcp`, `.../npi_registry/mcp`) plus `claude mcp add --transport http` and Claude Desktop `mcp-remote` snippets, replacing the prior "adapt the snippet" placeholders ([`anthropics/healthcare` `.mcp.json`](https://github.com/anthropics/healthcare/blob/main/plugins/healthcare/.mcp.json)).

### Flagged
- **`anthropics/healthcare` deprecation** — un-flagged (resolved). All affected pages now reference the consolidated `healthcare@healthcare` plugin; `pubmed.md` needs no change (it installs via the separate, non-deprecated `pubmed@life-sciences` marketplace path).

### Verified (no changes)
- 4 healthcare-plugin entries re-verified against upstream marketplace/`.mcp.json` (`last_verified` bumped to 2026-07-19); manifest sweep confirmed no new `anthropics/life-sciences`, `anthropics/claude-plugins-official`, or Claude Science entries; FHIR + ClinicalTrials.gov coverage reconfirmed.

## 2026-07-19 (Neuroscience slot)

Neuroscience directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`, ~19 entries) and `anthropics/claude-plugins-official` marketplaces were re-fetched and diffed against the catalog — all entries already covered (Boltz, PubMed, ChEMBL, Open Targets, etc.). Neuroscience seed queries reconfirmed existing coverage: allenbrain-mcp (`allenbrain`, flagged for license), the EEG/BCI MCP (`bci-mcp`), SpikeLab spike-sorting (`spikelab`), and DANDI (covered via `neurosift`; the `bendichter/dandi-query-mcp` remains boilerplate and deferred). The abc_atlas_access package is a bare PyPI install (out of scope). One genuinely-new installable plugin surfaced.

### Added
- **NeuroFlow** (Categories: Neuroscience) — MIT Claude Code plugin (`stanislavjiricek/neuroflow`, v0.2.20) providing 20+ phase-aware slash commands for an end-to-end neuroscience research project: ideation, funder-adaptive grant writing, experiment/tool building, data preprocessing/analysis (BIDS), computational brain modeling, and manuscript/poster drafting; bundles a literature-search MCP ([README](https://github.com/stanislavjiricek/neuroflow), [LICENSE](https://github.com/stanislavjiricek/neuroflow/blob/main/LICENSE)).

### Verified (no changes)
- Manifest sweep confirmed no new `anthropics/life-sciences` or `anthropics/claude-plugins-official` plugins; Allen Brain Atlas, EEG/BCI, SpikeLab, and DANDI neuroscience surfaces reconfirmed against existing coverage.

## 2026-07-18 (Molecular and Cellular Biology slot)

Molecular and Cellular Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace (`.claude-plugin/marketplace.json`, 19 entries) was re-fetched and diffed against the catalog — all entries already covered. Seed queries reconfirmed the Scanpy MCP family (`scanpy-mcp`/`scmcp`, already catalogued and cross-linked) and the Ensembl MCP surface. The RNA-seq/regulatory-genomics query surfaced one genuinely-new installable plugin.

### Added
- **ENCODE Toolkit** (Categories: Molecular and Cellular Biology) — AGPL-3.0 Claude Code plugin + MCP server (`ammawla/encode-toolkit`, PyPI v0.3.0) with 20 ENCODE Portal tools (search, batch download with MD5 verification, local experiment tracking) plus seven Nextflow reference pipelines (ChIP-seq, ATAC-seq, RNA-seq, WGBS, Hi-C, DNase-seq, CUT&RUN); distinct from the read-only ENCODE Claude Skill ([README](https://github.com/ammawla/encode-toolkit/blob/main/README.md), [PyPI](https://pypi.org/project/encode-toolkit/)).

### Verified (no changes)
- Manifest sweep confirmed no new `anthropics/life-sciences` plugins; Scanpy MCP family and stMCP (spatial-transcriptomics preprint — deferred, unverified repo/license) reconfirmed against existing coverage.

## 2026-07-18 (Integrative Structural and Computational Biology slot)

Integrative Structural and Computational Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` and `anthropics/claude-plugins-official` marketplaces were re-fetched and diffed against the catalog — all entries already covered. Structural seed queries confirmed the RCSB PDB, AlphaFold/ESMFold, and PyMOL surfaces are already comprehensively catalogued (`pdb`, `alphafold`, `esmfold`, `pymol`, `molecule-mcp`), and that no cryo-EM (RELION/cryoSPARC) MCP or Skill exists yet (still deferred). The MD seed query surfaced one genuinely-new hosted computational-chemistry engine.

### Added
- **NovoMCP** (Categories: Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology) — hosted computational-chemistry MCP from Quant NexusAI: free ADMET / molecular-profiling tier over a ~122M-compound layer plus a paid Novo Compute tier (GFN2-xTB QM, GPU GROMACS MD, AutoDock-GPU docking); research-preview access, proprietary SaaS ([NovoMCP docs](https://www.novomcp.com/docs/novo)).

### Verified (no changes)
- Manifest sweep confirmed no new life-sciences marketplace plugins; cryo-EM MCP/Skill and dedicated PDB/AlphaFold MCPs reconfirmed against existing coverage.

## 2026-07-18 (Immunology and Microbiology slot)

Immunology and Microbiology directed pass plus a manifest sweep. The `anthropics/life-sciences` and `anthropics/claude-plugins-official` marketplaces were re-fetched and diffed against the catalog — all entries already covered (the only life-science plugin in the official cross-domain marketplace is `boltz`, catalogued). Seed queries for a dedicated IEDB MCP and a metagenomics/microbiome MCP confirmed neither exists yet (still deferred). Five genuinely-new immunology / TCR-BCR skills were drawn from the deferred `GPTomics/bioSkills` queue (MIT license re-confirmed from the repo LICENSE this run).

### Added
- **Neoantigen Prediction (bioSkills)** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Translational Medicine) — pVACtools tumor-to-candidate neoantigen pipeline centering clonality/CCF, HLA LOH, expression, and predicted→presented→immunogenic validation tiers ([`immunoinformatics/neoantigen-prediction`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/neoantigen-prediction/SKILL.md)).
- **MHC Class II Prediction (bioSkills)** (Categories: Immunology and Microbiology) — CD4 T-cell epitope binding via NetMHCIIpan-4.3 + MixMHC2pred-2.0, with the class II reliability caveats ([`immunoinformatics/mhc-class-ii-prediction`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/mhc-class-ii-prediction/SKILL.md)).
- **scirpy Analysis (bioSkills)** (Categories: Immunology and Microbiology) — single-cell paired TCR/BCR + gene-expression repertoire analysis on the scirpy AIRR awkward-array model ([`tcr-bcr-analysis/scirpy-analysis`](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/scirpy-analysis/SKILL.md)).
- **MiXCR Analysis (bioSkills)** (Categories: Immunology and Microbiology) — MiXCR 4.7+ V(D)J alignment + clonotype assembly with chemistry-matched presets and AIRR export (MiXCR needs its own free academic license) ([`tcr-bcr-analysis/mixcr-analysis`](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/mixcr-analysis/SKILL.md)).
- **TCR-Epitope Binding (bioSkills)** (Categories: Immunology and Microbiology) — TCR specificity via clustering (tcrdist3/GLIPH2/clusTCR/GIANA) + VDJdb/IEDB/McPAS-TCR lookup, with honest supervised-prediction caveats ([`immunoinformatics/tcr-epitope-binding`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/tcr-epitope-binding/SKILL.md)).

### Verified (no changes)
- Manifest sweep confirmed no new life-sciences marketplace plugins; dedicated IEDB / metagenomics MCP servers reconfirmed absent.

## 2026-07-18 (Chemistry slot)

Chemistry directed pass plus a manifest sweep, and processed one open user request (#50). The `anthropics/life-sciences` marketplace was re-fetched (21 plugin directories) and diffed against the catalog — all entries already covered (biorxiv / clinical-trials plugins remain flagged DOA). The Chemistry seed queries surfaced a strong single-install cheminformatics MCP; ChEMBL/PubChem candidates were already catalogued.

### Added
- **LabMate MCP** (Categories: Chemistry, Drug Repurposing and Discovery) — one-install stdio MCP with 81 tools (retrosynthesis, forward/ADMET/pKa/NMR prediction, 202 named reactions, reagent calculators, compound + literature lookup); MIT, PyPI `labmate-mcp` v7.3.1 ([`JonasRackl/labmate-mcp`](https://github.com/JonasRackl/labmate-mcp)).
- **Proto-OKN MCP Server** (Categories: All) — natural-language access to 30+ NSF Proto-OKN scientific knowledge graphs (SPOKE biomedicine, BioBricks chemical safety, DREAM-KG, SAWGraph) via SPARQL, schema inspection, cross-graph bridging, and ChEBI/MONDO/GO ontology expansion; BSD-3, hosted connector; from user request [#50](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/50) ([`sbl-sdsc/mcp-proto-okn`](https://github.com/sbl-sdsc/mcp-proto-okn)).

### Verified (no changes)
- Chemistry-page entries spot-checked (`last_verified` all within 30 days); manifest sweep confirmed no new life-sciences marketplace plugins.

## 2026-07-17 (manual bulk addition)

Out-of-cycle manual import from a user request (@goodb): Anthropic's [Claude Science](https://claude.com/docs/claude-science/connectors-and-skills) **20 Featured connectors + 17 Research skills**, catalogued at source-level granularity (each connector decomposed into its underlying data sources). Introduced a searchable **Claude Science marker** — a `claude_science: true` front-matter flag that `scripts/build_index.py` turns into a `"Claude Science"` composer keyword, plus a bolded **Claude Science:** trust callout under each entry's Notes. **69 entries now carry the marker** (35 new + 34 annotated). Merged as [#56](https://github.com/scripps-ai-enablement/sci-ai-enabler/pull/56). Claude Science has since been added to the standing discovery sources in `AGENT.md` so future runs sweep it automatically.

### Added
- **12 Claude Science research skills** (upstream OSS repos documented for local runs; most are Claude-Science-only): **AlphaFold2**, **Chai-1**, **ESMFold**, **OpenFold3** (structure prediction; Categories: Integrative Structural and Computational Biology, Drug Repurposing and Discovery ± Molecular and Cellular Biology); **ProteinMPNN**, **LigandMPNN**, **SolubleMPNN** (protein sequence design; Integrative Structural and Computational Biology, Drug Repurposing and Discovery); **Borzoi**, **Evo 2** (sequence/genome models; Molecular and Cellular Biology); **scGPT** (single-cell foundation model; Immunology and Microbiology, Molecular and Cellular Biology); **Indication Dossier** (agent workflow; Drug Repurposing and Discovery, Translational Medicine); **Morning** (General-Purpose Utilities). ([Claude Science](https://claude.com/docs/claude-science/connectors-and-skills))
- **6 connector data sources with community/official MCP servers** — **cBioPortal** ([`cBioPortal/cbioportal-mcp`](https://github.com/cBioPortal/cbioportal-mcp)), **MyGene.info** (BioThings, [`longevity-genie/biothings-mcp`](https://github.com/longevity-genie/biothings-mcp)), **Gene Ontology** ([`Augmented-Nature/GeneOntology-MCP-Server`](https://github.com/Augmented-Nature/GeneOntology-MCP-Server)), **Ontology Lookup Service (OLS)** ([`seandavi/ols-mcp-server`](https://github.com/seandavi/ols-mcp-server)), **arXiv** ([`blazickjp/arxiv-mcp-server`](https://github.com/blazickjp/arxiv-mcp-server)), **ArrayExpress / BioStudies** ([`Augmented-Nature/BioStudies-MCP-Server`](https://github.com/Augmented-Nature/BioStudies-MCP-Server)). All install paths built and verified.
- **17 connector data sources as Claude.ai Connector entries** (Anthropic-hosted in Claude Science; each documents the provider's public API for outside-Claude-Science access): **Complex Portal**, **IntAct**, **ChEBI**, **Rhea**, **BindingDB**, **BioMart**, **ClinGen**, **CIViC**, **eQTL Catalogue**, **FinnGen**, **BioBank Japan**, **Ketcher** (EPAM sketcher), **Antibody Registry**, **Rfam**, **MGnify**, **MetaboLights**, **CELLxGENE CellGuide**.

### Updated
- **Claude Science marker added to 34 existing entries** (provenance annotation — no `last_verified` bump): `pdb`, `pdbe`, `alphafold`, `emdb-database`, `gnomad-database`, `clinvar-database`, `dbsnp-database`, `zinc-database`, `pubchem`, `openfda`, `fda-database`, `gtex-database`, `uniprot`, `reactome-database`, `ensembl`, `ucsc-genome-browser`, `gwas-database`, `openalex-database`, `geo-database`, `pride-database`, `interpro-database`, `string-database-ppi`, `encode-database`, `jaspar-database`, `unibind-database`, `research-grants`, `cellxgene-census`, `open-targets`, `human-protein-atlas`, `boltz`, `diffdock`, `esm`, `literature-review`, `scvi-tools`.
- **Open Targets Plugin** — the official MCP endpoint remains flagged (fails `initialize`); added the **verified-working** community [`Augmented-Nature/OpenTargets-MCP-Server`](https://github.com/Augmented-Nature/OpenTargets-MCP-Server) as an install path + workaround (built, passed the stdio handshake, 6 tools, live BRAF data on 2026-07-17). `last_verified` bumped to 2026-07-17.

## 2026-07-15 (Chemistry slot)

Chemistry directed pass plus a manifest sweep, and processed one open user request. The `anthropics/life-sciences` marketplace was re-fetched (21 plugin directories) and diffed against the catalog — all entries already covered. The Chemistry seed queries (RDKit / retrosynthesis / ChEMBL / PubChem MCP) surfaced only tools already catalogued (`rdkit-mcp` = `tandemai-inc/rdkit-mcp-server`; `rdkit-agent`, `chemcp`, `pubchem`, `chembl` all present; the Augmented-Nature ChEMBL variant stays deferred; no OSS retrosynthesis MCP wrapper has shipped) — no new Chemistry entry warranted.

### Added
- **GlyGen MCP Server** (Categories: All) — first-party remote MCP server over GlyGen's integrated glycan / glycoprotein / biomarker / disease knowledgebase; five read-only summary tools (`get_protein_summary`, `get_site_summary`, `get_glycan_summary`, `get_biomarker_summary`, `get_disease_summary`). Install via Claude.ai custom connector, `claude mcp add --transport http`, or Claude Desktop `mcp-remote` proxy at `https://mcp.glygen.org/mcp`. Beta; pricing Unverified (no upstream LICENSE). Surfaced from user request [#48](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/48). ([`glygener/glygen-mcp-server`](https://github.com/glygener/glygen-mcp-server), [GlyGen](https://www.glygen.org/))

### Flagged
- **GlyGen MCP Server** — `glygener/glygen-mcp-server` declares no LICENSE (GitHub license field null); pricing marked `Unverified —` inline rather than asserting Free / OSS.

### Updated
- **ChEMBL Connector** — re-verified against the `anthropics/life-sciences` marketplace (still listed); `last_verified` bumped 2026-05-30 → 2026-07-15.

### Verified (no changes)
- `anthropics/life-sciences` marketplace re-diffed against the catalog; all 21 plugin directories already covered.

## 2026-07-12 (Drug Repurposing and Discovery slot)

Drug Repurposing and Discovery directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` marketplaces were re-fetched and diffed — no new life-science plugins. The directed pass drew from the deferred **ToolUniverse sibling agent skills** queue (`mims-harvard/ToolUniverse/skills/`, Apache-2.0, 150+ skills sharing the `npx skills add mims-harvard/ToolUniverse` install path): four genuinely new drug-discovery / oncology / safety workflows were verified against their `SKILL.md` files and catalogued.

### Added
- **Cancer Variant Interpretation (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — eight-phase somatic-mutation interpretation (CIViC/OncoKB tiers, cBioPortal prevalence, OpenTargets/ChEMBL/DrugBank therapies, resistance mechanisms, ClinicalTrials.gov matching) producing an evidence-graded precision-oncology report. GA, Free / OSS. ([`skills/tooluniverse-cancer-variant-interpretation/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-cancer-variant-interpretation/SKILL.md))
- **Adverse Event Detection (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — nine-phase pharmacovigilance signal detection over openFDA FAERS with disproportionality statistics (PRR/ROR/IC, 95% CIs) and a 0–100 Safety Signal Score. GA, Free / OSS. ([`skills/tooluniverse-adverse-event-detection/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-adverse-event-detection/SKILL.md))
- **Immunotherapy Response Prediction (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Translational Medicine) — eleven-phase ICI response scoring integrating TMB, MSI, PD-L1, HLA, and immune gene expression into a 0–100 evidence-graded score. GA, Free / OSS. ([`skills/tooluniverse-immunotherapy-response-prediction/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-immunotherapy-response-prediction/SKILL.md))
- **Adverse Outcome Pathway (ToolUniverse Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery) — four-phase chemical hazard assessment mapping compounds to AOPs via AOPWiki, GHS/IARC classification, LD50 data, and CTD toxicogenomics. GA, Free / OSS. ([`skills/tooluniverse-adverse-outcome-pathway/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-adverse-outcome-pathway/SKILL.md))

### Verified (no changes)
- `anthropics/life-sciences` + `claude-plugins-official` marketplaces re-diffed against the catalog; all entries already covered.

## 2026-07-12 (Translational Medicine slot)

Translational Medicine directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`, 19 entries) and `claude-plugins-official` marketplaces were re-fetched and diffed — no new life-science plugins. The directed pass ran the FHIR / OpenFDA / ClinicalTrials.gov / regulatory-submission seed queries: the FHIR MCP surface (wso2, Momentum, LangCare) is already covered (`fhir-wso2.md`, `fhir-momentum.md`), but the Anthropic-official `anthropics/healthcare` repo has **consolidated** — the former standalone plugins are now deprecated in favor of a single `healthcare@healthcare` plugin that bundles 10 skills + 7 connected MCPs, three of whose skills are genuinely new to the catalog.

### Added
- **Fraud Detection (Anthropic Healthcare Plugin)** (Categories: Translational Medicine) — Claude skill screening Medicare/Medicaid claims for fraud, waste, and abuse via a three-tier deterministic-detection → model-adjudication → synthesis pipeline over a DuckDB claims corpus (NCCI MUE / OIG LEIE / CMS enrollment / PFS rulesets), with a "citation-or-zero" audit gate producing ranked SIU referrals. GA, Free / OSS. ([`anthropics/healthcare`](https://github.com/anthropics/healthcare), [`skills/fraud-detection/SKILL.md`](https://github.com/anthropics/healthcare/blob/main/plugins/healthcare/skills/fraud-detection/SKILL.md))
- **Procedure Coding (Anthropic Healthcare Plugin)** (Categories: Translational Medicine) — Claude skill converting a clinical encounter's documentation into claim-ready CPT and HCPCS Level II procedure codes (E/M, procedures, labs, imaging, drugs/devices), excluding planned-but-unperformed, bundled, and Category II codes. GA, Free / OSS. ([`anthropics/healthcare`](https://github.com/anthropics/healthcare), [`skills/procedure-coding/SKILL.md`](https://github.com/anthropics/healthcare/blob/main/plugins/healthcare/skills/procedure-coding/SKILL.md))
- **Clinical Note Extract (Anthropic Healthcare Plugin)** (Categories: Translational Medicine) — Claude skill extracting structured, validated records from unstructured clinical notes with span-level provenance, explicit `null_reason` handling, and deterministic validation — for auditable chart abstraction and registry building. GA, Free / OSS. ([`anthropics/healthcare`](https://github.com/anthropics/healthcare), [`skills/clinical-note-extract/SKILL.md`](https://github.com/anthropics/healthcare/blob/main/plugins/healthcare/skills/clinical-note-extract/SKILL.md))

### Updated
- **prior-auth-review** — install snippet now points at the consolidated `healthcare@healthcare` plugin (standalone `prior-auth-review@healthcare` deprecated upstream); skill invoked as `/healthcare:prior-auth`. `last_verified` bumped to 2026-07-12.
- **ICD-10 Codes MCP** — install now shows `healthcare@healthcare` plus the literal hosted HTTP endpoint (`https://hcls.mcp.claude.com/icd10_codes/mcp`), a direct `claude mcp add --transport http` form, and a Claude Desktop `mcp-remote` proxy snippet. `last_verified` bumped to 2026-07-12.

### Flagged
- **`anthropics/healthcare` standalone plugins** — `clinical-trial-protocol`, `prior-auth-review`, `fhir-developer`, `cms-coverage`, `npi-registry`, `pubmed`, `icd10-codes` are all marked "Deprecated — install healthcare@healthcare instead" upstream. `prior-auth-review.md` and `icd-10-codes.md` updated this run; `clinical-trial-protocol.md` / `fhir-developer.md` / `cms-coverage.md` / `npi-registry.md` / the `pubmed.md` Anthropic path queued for a future pass.

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` (19 plugins) + `claude-plugins-official` + MCP Registry — no new in-scope entries.
- FHIR MCP surface (`fhir-wso2.md`, `fhir-momentum.md`) and OpenFDA / ClinicalTrials.gov coverage confirmed current for the directed pass.

## 2026-07-12 (Neuroscience slot)

Neuroscience directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`, 19 entries) and `claude-plugins-official` marketplaces were re-fetched and diffed — no new in-scope plugins (all already catalogued; `boltz` unchanged). The directed pass ran the NWB/DANDI and EEG/fMRI seed queries: DANDI/Allen/NWB MCP surfaces are already covered (`neurosift`, `allenbrain`, `bci-mcp`), but the `InternScience/Awesome-Scientific-Skills` meta-list surfaced `HughYau/neuroforge-skills` (MIT, 5 skills over Brian2 / MNE-Python / Nilearn / SpikeInterface / pyNIBS). Two of the five are genuinely new to the catalog.

### Added
- **Brian2** (Categories: Neuroscience) — Claude Skill for building spiking neural network simulations with Brian2: equation-based `NeuronGroup` neuron models, `Synapses` with STDP-style plasticity, Poisson/`TimedArray` inputs, spike/state/rate monitors, Python vs. `cpp_standalone` execution, and multicompartment `SpatialNeuron` morphology. GA, MIT. ([`HughYau/neuroforge-skills`](https://github.com/HughYau/neuroforge-skills), [`skills/brian2/SKILL.md`](https://github.com/HughYau/neuroforge-skills/blob/main/skills/brian2/SKILL.md))
- **pyNIBS** (Categories: Neuroscience) — Claude Skill for TMS / non-invasive brain stimulation analysis with pyNIBS: subject/session and mesh/ROI HDF5 I/O, coil-placement and multichannel-current optimization, nonlinear MEP-to-E-field regression mapping, and experiment-import/QC utilities (SimNIBS integration). GA, MIT. ([`HughYau/neuroforge-skills`](https://github.com/HughYau/neuroforge-skills), [`skills/pynibs/SKILL.md`](https://github.com/HughYau/neuroforge-skills/blob/main/skills/pynibs/SKILL.md))

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` (19 plugins) + `claude-plugins-official` + MCP Registry — no new in-scope entries.
- NeuroForge's other three skills (MNE-Python, Nilearn, SpikeInterface) already covered by `mne-eeg-tool.md` / `nilearn-tool.md` / `spikeinterface-electrophysiology.md` — no duplicate created.

## 2026-07-11 (Molecular and Cellular Biology slot)

Molecular and Cellular Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` marketplaces were re-fetched and diffed — no new in-scope plugins (all 19 entries already catalogued). The directed pass ran the Ensembl / Geneformer / Bioconductor / CRISPR / single-cell seed queries: a single-install multi-database aggregator MCP (GWAS-MCP) surfaced as genuinely new; no dedicated Geneformer/scGPT single-cell-foundation-model wrapper exists yet (gap noted for future runs).

### Added
- **GWAS-MCP** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — single-install MCP server bundling 30+ tools across 14 biological databases (UniProt, Ensembl, ClinVar, GWAS Catalog, GTEx, STRING, InterPro, AlphaFold, PDB, KEGG, Open Targets, PharmGKB, OMIM) for a variant-to-target research workflow. GA, MIT, PyPI `gwas-mcp` v1.0.2. ([`zaeyasa/gwas-mcp`](https://github.com/zaeyasa/gwas-mcp))

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` (19 plugins) + MCP Registry — no new in-scope entries.
- `ensembl.md` — Augmented-Nature Ensembl variant already noted as alternative implementation; no change.

## 2026-07-11 (Integrative Structural and Computational Biology slot)

Integrative Structural and Computational Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` marketplaces were re-fetched and diffed — no new in-scope plugins (all entries, including `boltz`, already catalogued). The directed pass ran the GROMACS/MD and RCSB PDB seed queries: the RCSB PDB MCP surface (incl. `cyanheads/protein-mcp-server`) is already covered by `pdb.md`, but a Docker-packaged GROMACS MD-runner MCP surfaced that closes the long-tracked standalone-GROMACS gap.

### Added
- **GROMACS MCP Server** (Categories: Integrative Structural and Computational Biology) — Docker-based MCP server bundling GROMACS 2025.4, exposing six tools to run/monitor MD simulations and batch trajectory analysis from Claude with async job tracking. First followable GROMACS MD-runner MCP catalogued. Alpha; license marked `Unverified —` (no upstream LICENSE) and flagged. ([`MacromNex/gromacs_mcp`](https://github.com/MacromNex/gromacs_mcp))

### Flagged
- **GROMACS MCP Server** — no upstream LICENSE file (GitHub license field null); README's "LGPL (GROMACS)" is GROMACS's license, not the wrapper's. Catalogued with pricing `Unverified —` inline; revisit once a wrapper license is declared.

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` + `claude-plugins-official` — no new in-scope entries.
- `pdb.md` — RCSB PDB MCP surface (official `rcsb-mcp` + cyanheads/Augmented-Nature/QuentinCody community servers) confirmed still current for the directed pass.

## 2026-07-11 (Immunology and Microbiology slot)

Immunology and Microbiology directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` marketplaces were re-fetched and diffed — no new in-scope plugins (all entries already catalogued). The directed pass ran the IEDB epitope / antibody-design / metagenomics / BCR-TCR AIRR-seq seed queries: no standalone IEDB or antibody-design MCP wrapper exists yet, but the `GPTomics/bioSkills` collection (MIT; 561 skills across 63 root-level category directories) surfaced as a rich, cleanly-licensed source of immunology/microbiology skills. Five genuinely-new skills were catalogued under the per-run soft cap; the full collection is deferred for a one-time batch ingest.

### Added
- **Epitope Prediction (bioSkills)** (Categories: Immunology and Microbiology) — Claude Code skill predicting B-cell and T-cell epitopes for vaccine/epitope-mapping work with BepiPred-3.0, DiscoTope-3.0, the IEDB tools, and NetMHCpan/MHCflurry presentation predictors. Closes the long-tracked IEDB/epitope gap. MIT. ([`immunoinformatics/epitope-prediction/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/epitope-prediction/SKILL.md))
- **MHC Binding Prediction (bioSkills)** (Categories: Immunology and Microbiology) — Claude Code skill scoring peptide–MHC class I binding and natural presentation with MHCflurry, NetMHCpan-4.1, and MixMHCpred to nominate CD8 T-cell epitopes/neoantigens. MIT. ([`immunoinformatics/mhc-binding-prediction/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/immunoinformatics/mhc-binding-prediction/SKILL.md))
- **Immcantation BCR Analysis (bioSkills)** (Categories: Immunology and Microbiology) — Claude Code skill reconstructing B-cell clonal families, quantifying somatic hypermutation/selection, and building antibody lineage trees from AIRR-seq data with the Immcantation R suite (alakazam/shazam/scoper/dowser/tigger). Closes the BCR/AIRR-seq gap. MIT. ([`tcr-bcr-analysis/immcantation-analysis/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/tcr-bcr-analysis/immcantation-analysis/SKILL.md))
- **Kraken2 Metagenomic Classification (bioSkills)** (Categories: Immunology and Microbiology) — Claude Code skill classifying shotgun metagenomic reads with Kraken2 minimizer/LCA matching then re-estimating abundance with Bracken. MIT. ([`metagenomics/kraken-classification/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/kraken-classification/SKILL.md))
- **AMR / Resistome Detection (bioSkills)** (Categories: Immunology and Microbiology) — Claude Code skill profiling the antimicrobial-resistance gene content of shotgun metagenomes with RGI, AMR++/MEGARes, deepARG, GROOT, and AMRFinderPlus/ABRicate. Closes the metagenomics/AMR gap. MIT. ([`metagenomics/amr-detection/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/metagenomics/amr-detection/SKILL.md))

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` + `claude-plugins-official` — no new in-scope entries.

## 2026-07-11 (Chemistry slot)

Chemistry directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` marketplaces were re-fetched and diffed — no new in-scope plugins (all entries already catalogued). The directed pass ran the RDKit / retrosynthesis / ChEMBL seed queries: existing RDKit (TandemAI MCP, K-Dense skill), PubChem, ChEMBL, and ChemCP entries already cover the surface; one genuinely-new, verified RDKit tool surfaced.

### Added
- **RDKit Agent** (Categories: Chemistry, Drug Repurposing and Discovery) — agent-first cheminformatics CLI / Node library / MCP server / Claude skill powered by RDKit **WASM** (no Python runtime, Node ≥ 16). 20+ tools including SMILES validation/repair, notation conversion, descriptors, Tanimoto similarity, reaction SMIRKS application, atom mapping, and SVG/PNG rendering. MIT, npm `rdkit-agent` v0.1.1. Distinct from the Python-based TandemAI RDKit MCP and K-Dense RDKit skill already catalogued. ([`scottmreed/rdkit-agent`](https://github.com/scottmreed/rdkit-agent), [npm](https://registry.npmjs.org/rdkit-agent))

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` + `claude-plugins-official` — no new in-scope entries.

