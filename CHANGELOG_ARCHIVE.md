---
title: Catalog updates archive
nav_exclude: true
---

# Catalog updates archive

Older entries rotated out of [CHANGELOG.md](CHANGELOG.md). Newest first, same format.
## 2026-07-05 (Drug Repurposing and Discovery slot)

Drug Repurposing and Discovery directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` marketplaces were re-fetched and diffed — no new in-scope plugins. The directed pass ran the Open Targets / DrugBank / ADMET seed queries: the official Open Targets MCP, DepMap, and Inductive Bio ADMET paths are already catalogued (Open Targets MCP still flagged for its non-compliant `initialize`), and three genuinely-new, verified ToolUniverse sibling drug-discovery agent skills surfaced from the upstream `SKILL.md` files.

### Added
- **Target Research (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — ToolUniverse agent skill profiling a target across nine parallel research paths (expression via GTEx/HPA, pathways, STRING interactions, gnomAD/ClinVar variants, DGIdb/ChEMBL druggability, PubMed) into a 15-section T1–T4 evidence-graded report. Apache-2.0; requires the ToolUniverse MCP server. ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-target-research/SKILL.md))
- **GWAS Drug Discovery (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — ToolUniverse agent skill turning GWAS loci into druggable targets and repurposing candidates: GWAS Catalog fine-mapping → Open Targets tractability/safety → composite prioritisation → ChEMBL/DGIdb drug matching → openFDA/trial safety. Apache-2.0; requires the ToolUniverse MCP server. ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-gwas-drug-discovery/SKILL.md))
- **Binder Discovery (ToolUniverse Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery, Integrative Structural and Computational Biology) — ToolUniverse agent skill running a 7-phase small-molecule discovery workflow: druggability → ChEMBL/BindingDB/PubChem ligand mining → PDB/AlphaFold structure → NVIDIA NIM DiffDock/Boltz-2 docking → GenMol/MolMIM expansion → ADMET-AI filtering → ranked shortlist. Apache-2.0; requires the ToolUniverse MCP server (NVIDIA NIM tools need NIM access configured). ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-binder-discovery/SKILL.md))

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` — no new in-scope plugins.

## 2026-07-05 (Translational Medicine slot)

Translational Medicine directed pass plus a manifest sweep. The `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` marketplaces were re-fetched and diffed — no new in-scope plugins (life-sciences entries all catalogued; `boltz` remains the only life-science entry in the official directory and is catalogued). The directed pass ran the FHIR-MCP and ToolUniverse pharmacovigilance/rare-disease seed queries: the Momentum, WSO2, and Anthropic FHIR paths are already catalogued, and two genuinely-new, verified ToolUniverse sibling agent skills surfaced from the upstream `SKILL.md` files.

### Added
- **Pharmacovigilance (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — ToolUniverse agent skill mining FAERS spontaneous reports (`FAERS_count_reactions_by_drug_event` / `_filter_serious_events` / `_stratify_by_demographics`), FDA labels (`DailyMed_*`, `OpenFDA_search_drug_labels`), and pharmacogenomics (`PharmGKB_search_drugs`, `CPIC_list_guidelines`), computing disproportionality signals (PRR/ROR/IC). Apache-2.0; requires the ToolUniverse MCP server. ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-pharmacovigilance/SKILL.md))
- **Rare Disease Diagnosis (ToolUniverse Claude Skill)** (Categories: Molecular and Cellular Biology, Translational Medicine) — ToolUniverse agent skill for phenotype-driven differential diagnosis: HPO term matching (`HPO_search_terms`) → Orphanet/OMIM/DisGeNET candidate diseases → MARRVEL/ClinGen/GTEx gene prioritization → ACMG variant interpretation (`FAVOR_annotate_variant`, `ClinVar_get_variant_details`, `gnomad_get_variant`, EVE/SpliceAI) → AlphaFold2/InterPro. Apache-2.0; requires the ToolUniverse MCP server. ([SKILL.md](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-rare-disease-diagnosis/SKILL.md))

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` — no new in-scope plugins.

## 2026-07-05 (Neuroscience slot)

Neuroscience directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace was re-fetched from `.claude-plugin/marketplace.json` and diffed — every entry (10x-genomics, pubmed, biorender, synapse, wiley-scholar-gateway, biorxiv, clinical-trials, chembl, owkin, open-targets, single-cell-rna-qc, instrument-data-to-allotrope, nextflow-development, scvi-tools, clinical-trial-protocol, scientific-problem-selection, tooluniverse) is already catalogued; `claude-plugins-official` remains dev/business tooling with only `boltz` in life-science scope (already catalogued). The directed pass ran the Allen Brain Atlas, NWB/DANDI, spike-sorting, and EEG/fMRI MCP seed queries and scanned the MCP Registry: `allenbrain-mcp` (flagged, license unset) and `neurosift` (DANDI/NWB) are already catalogued, `brain-bbqs/NeuroMCP` repo still 404s (stays deferred), and one genuinely new, verified installable tool surfaced — BCI-MCP.

### Added
- **BCI-MCP** (Categories: Neuroscience) — community MIT MCP server (PyPI/npm `bci-mcp` v0.1.3, 2026-06-24) streaming live EEG brain-state metrics (focus, calm, attention, band powers, signal quality) from OpenBCI/Muse/LSL devices, with a hardware-free `synthetic://` mode; 13 tools incl. neurofeedback and session recording. Stdio FastMCP server, `claude mcp add bci-mcp -- npx -y bci-mcp`. ([repo](https://github.com/enkhbold470/bci-mcp), [PyPI](https://pypi.org/project/bci-mcp/))

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) and `claude-plugins-official` — no new in-scope plugins.

## 2026-07-04 (Molecular and Cellular Biology slot)

Molecular and Cellular Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace was re-fetched from `.claude-plugin/marketplace.json` and diffed — every entry (10x-genomics, pubmed, biorender, synapse, wiley-scholar-gateway, biorxiv, clinical-trials, chembl, owkin, open-targets, single-cell-rna-qc, instrument-data-to-allotrope, nextflow-development, scvi-tools, clinical-trial-protocol, scientific-problem-selection, tooluniverse) is already catalogued; no new in-scope plugins. The directed pass ran the Scanpy MCP and CRISPR-design seed queries and scanned the `GoekeLab/awesome-genomic-skills` meta-list: most standalone entries were already catalogued (chatspatial, biomcp, gget, biocontextai, clair-variant-caller), and one genuinely new, verified tool surfaced — the official Seqera MCP.

### Added
- **Seqera MCP** (Categories: Molecular and Cellular Biology, Immunology and Microbiology, Integrative Structural and Computational Biology) — official hosted MCP server from Seqera Labs (the Nextflow team) at `https://mcp.seqera.io/mcp`; launches/manages Nextflow & nf-core pipelines, provisions Wave containers, and retrieves public SRA/ENA/GEO data. OAuth 2.1 or Seqera token auth; requires a Seqera Platform account (free Cloud/Community tier). ([docs](https://docs.seqera.io/platform-cloud/seqera-mcp/overview))

### Updated
- **Scanpy-MCP** — re-verified (v0.5.0, BSD-3-Clause, `pip install scanpy-mcp`, scmcphub org all current); `last_verified` bumped 2026-05-20 → 2026-07-04 and an `scmcp` orchestrator alternative-install note added (single server bundling Scanpy + LIANA+ + decoupleR + CellRank 2).

### Flagged
- _None._

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` (`.claude-plugin/marketplace.json`) — no new in-scope plugins.

## 2026-07-04 (Integrative Structural and Computational Biology slot)

Integrative Structural and Computational Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace (~17 plugins) was re-fetched from `.claude-plugin/marketplace.json` and diffed against the catalog — every entry is already catalogued, no new in-scope plugins; the `claude-plugins-official` directory was scanned and remains dev/business tooling with no life-science additions. The directed pass ran the RCSB PDB, cryo-EM (RELION/cryoSPARC), and GROMACS/OpenMM MD seed queries and scanned the MCP Registry and `punkpeye/awesome-mcp-servers`: cryo-EM (RELION/cryoSPARC/CTFFIND) remains unwrapped for Claude (reconfirmed absent, deferred), and the strong protein-structure MCPs (cyanheads, Augmented Nature, QuentinCody, RCSB official) are already folded into `pdb.md`. One genuinely new, distinct data-source entry surfaced: the first-party PDBe Europe MCP servers.

### Added
- **PDBe MCP Servers** (Categories: Integrative Structural and Computational Biology, Drug Repurposing and Discovery) — first-party PDBe (EMBL-EBI) MCP servers over the PDBe REST API, Solr search, and an optional Neo4j graph; Apache-2.0, PyPI `pdbe-mcp-server` v1.1.4, keyless for API/Search. Distinct from the RCSB-focused servers on `pdb.md` (separate wwPDB partner site, different APIs). ([repo](https://github.com/PDBeurope/pdbe-mcp-servers), [PyPI](https://pypi.org/project/pdbe-mcp-server/))

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` and `claude-plugins-official` — no new in-scope plugins.
- Structural-biology core pages (`pdb.md`, `alphafold.md`, `foldseek-structural-search.md`, `pymol.md`, `openmm-mcp.md`) all within the 30-day verification window; no re-verification due.
- Cryo-EM (RELION / cryoSPARC / CTFFIND) — reconfirmed no Claude-installable wrapper on the Structural pass; deferred note re-dated.

## 2026-07-04 (Immunology and Microbiology slot)

Immunology and Microbiology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace (~17 plugins) was re-fetched from `.claude-plugin/marketplace.json` and diffed against the catalog — every entry is already catalogued, no new in-scope plugins. The directed pass ran the IEDB, metagenomics/microbiome, antibody-design, and BCR/TCR/AIRR seed queries and scanned `punkpeye/awesome-mcp-servers`, the MCP Registry, and the K-Dense skills directory: the three standing Immunology gaps (a Claude-installable IEDB wrapper, a BCR/TCR/AIRR-seq skill, a discrete metagenomics/microbiome/AMR MCP) were all reconfirmed absent, and K-Dense has no new immunology skills. No new installable candidates warranted this run; the deferred-gap notes were re-dated in `curator-state.md`.

### Added
- _None._

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- **FlowIO** (`flowio.md`) — confirmed the K-Dense `flowio` `SKILL.md` still exists upstream and wraps the BSD-3 `flowio` FCS parser; `last_verified` bumped 2026-06-04 → 2026-07-04.
- Manifest sweep of `anthropics/life-sciences` — no new in-scope plugins.

## 2026-07-04 (Chemistry slot)

Chemistry directed pass plus a manifest sweep. The `anthropics/life-sciences` (~21 plugins) and `claude-plugins-official` marketplaces were diffed — no new in-scope marketplace plugins (all life-sciences entries already catalogued; Boltz present). The Chemistry seed queries surfaced Anthropic's **Claude Science** launch cohort (2026-06-30/07-01): four new Life Sciences directory connectors. Two were catalogued this run — **Inductive Bio** (ADMET prediction, the focus-category find) and **Revvity Signals AI** (ELN) — both vendor/enterprise-gated with no public MCP URL, so the install path is the directory toggle plus a provisioned account (marked `Unverified —` on exact endpoints). The other two (Helix GenoSphere, Biomni Lab) were deferred under the soft cap. The retrosynthesis-MCP gap was reconfirmed absent (no OSS AiZynthFinder/ASKCOS/IBM RXN wrapper).

### Added
- **Inductive Bio ADMET Connector** (Categories: Chemistry, Drug Repurposing and Discovery) — Claude.ai connector surfacing Inductive Bio's ADMET prediction models (Beacon-1 family; 1st of 370+ in the OpenADMET-ExpansionRx blind challenge) for in-conversation compound design ([source](https://www.prnewswire.com/news-releases/inductive-bio-joins-anthropics-connector-ecosystem-for-life-sciences-surfacing-state-of-the-art-admet-prediction-to-drug-discovery-scientists-through-claude-302813935.html))
- **Revvity Signals AI Connector** (Categories: All) — Claude.ai connector for natural-language access to the Revvity Signals electronic lab notebook and connected R&D data ([source](https://clpmag.com/lab-essentials/information-technology/middleware-software/revvity-connects-signals-research-platform-anthropic-claude/))

### Flagged
- _None._

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` and `claude-plugins-official` — no new in-scope plugins.

## 2026-06-28 (Drug Repurposing and Discovery slot)

Drug Repurposing and Discovery directed pass plus a manifest sweep. The `anthropics/life-sciences` (~21 plugins) and `claude-plugins-official` marketplaces were diffed against the catalog — no new in-scope marketplace plugins (all life-sciences entries already catalogued; Boltz also present). The directed pass (DrugBank, drug-repurposing, target-prioritization queries) confirmed DrugBank is already well-covered (community + official MCP on `drugbank.md`) and surfaced **SandboxAQ** as an Anthropic-official connector — but its drug-discovery models (AQPotency, AQCell) are still waitlist-gated "coming soon" and only its materials-science catalyst model is live, so it was deferred. Two ToolUniverse drug-discovery agent skills (a deferred next-run priority) were verified against their upstream `SKILL.md` and catalogued.

### Added
- **Drug-Drug Interaction (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — CYP/transporter PK + PD interaction assessment with 0-100 clinical risk scoring, over the ToolUniverse MCP server ([source](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-drug-interaction/SKILL.md))
- **Precision Oncology (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — maps a tumor molecular profile to matched FDA-approved/investigational therapies, resistance mechanisms, and clinical trials (CIViC/OncoKB/COSMIC/GDC/Open Targets) ([source](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-precision-oncology/SKILL.md))

### Flagged
- _None._

### Verified (no changes)
- DrugBank (community + official MCP), Open Targets, and ToolUniverse core/sibling entries reconfirmed against current sources; no field changes.

## 2026-06-28 (Translational Medicine slot)

Translational Medicine directed pass plus a manifest sweep. The `anthropics/life-sciences` (~21 plugins) and `claude-plugins-official` marketplaces and the official MCP Registry were diffed against the catalog — no new in-scope marketplace plugins (all life-sciences entries already catalogued). The Translational Medicine pass (FHIR, openFDA, ClinicalTrials.gov queries) surfaced one new installable component, **Certus** — an MIT openFDA MCP server centered on drug-shortage tracking, recalls, and adverse events, with a zero-install hosted endpoint. Existing FHIR servers (Momentum, WSO2), the ythalorossy openFDA server, and the cyanheads ClinicalTrials.gov server were reconfirmed.

### Added
- **Certus Drug Information MCP Server** (Categories: Drug Repurposing and Discovery, Translational Medicine) — MIT openFDA MCP with 8 tools for drug shortages, recalls, labels, FAERS adverse events, and batch analysis; hosted endpoint + local self-host ([source](https://github.com/zesty-genius128/Certus_server))

### Updated
- **ClinicalTrials.gov MCP Server (cyanheads)** — re-verified, still GA / Apache-2.0 with hosted + npx/bunx install paths intact; `last_verified` bumped to 2026-06-28

### Verified (no changes)
- 1 entry re-verified (cyanheads ClinicalTrials.gov MCP); existing FHIR and openFDA entries reconfirmed against current sources.

## 2026-06-28 (Neuroscience slot)

Neuroscience directed pass plus a manifest sweep. The `anthropics/life-sciences` (21 plugins) and `claude-plugins-official` marketplaces and the official MCP Registry diffed against catalog — no new in-scope marketplace plugins. The Neuroscience pass (NWB/DANDI, Allen Brain Atlas, spike-sorting, EEG queries) surfaced one new installable component, **SciTeX Dataset MCP** — a cross-archive (OpenNeuro/DANDI/PhysioNet/Zenodo) dataset-discovery MCP server, catalogued this run. Two further candidates were deferred for verification: **HED-MCP** (`neuromechanist/hed-mcp`, BIDS/HED sidecar automation — not yet released to PyPI) and **brain-bbqs/NeuroMCP** (in the MCP Registry but the GitHub repo 404s). Already-catalogued neuroscience coverage (Neurosift, SpikeInterface, MNE, Allen Brain, allenbrain-mcp) was reconfirmed.

### Added
- **SciTeX Dataset MCP** (Categories: Neuroscience) — MCP server giving Claude a unified read-only search across OpenNeuro, DANDI, PhysioNet, and Zenodo for BIDS/NWB neuroscience datasets; AGPL-3.0, `uv pip install "scitex[dataset]"` + `scitex mcp start` ([source](https://pypi.org/project/scitex/))

### Flagged
- _None._

### Verified (no changes)
- `anthropics/life-sciences` (21 plugins), `claude-plugins-official`, and the official MCP Registry (brain/neuroscience search) diffed against catalog — no new in-scope marketplace entries.

## 2026-06-27 (Molecular and Cellular Biology slot)

Molecular and Cellular Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` (21 plugins) and `claude-plugins-official` marketplaces hold no new in-scope life-science entries (Boltz/fiftyone already covered or general-purpose). The MCB pass surfaced the `GoekeLab/awesome-genomic-skills` meta-list and the MCPmed bioinformatics-MCP family (Briefings in Bioinformatics 2026, bbag076), yielding three additions: **ChatSpatial** (spatial-transcriptomics MCP), the **Clair** variant-caller skill, and the first-party **MCPmed GEO MCP** (folded into the existing `geo-database.md`). MCPmed's PLSDB MCP was deferred on an unspecified upstream license.

### Added
- **ChatSpatial** (Categories: Molecular and Cellular Biology) — MCP server for spatial transcriptomics: 20 tools over ~65 Scanpy/Squidpy methods (preprocessing, spatial domains, deconvolution, cell-cell communication, SVG detection, trajectory/RNA velocity, CNV); MIT, `pip install chatspatial` or Docker ([source](https://github.com/cafferychen777/ChatSpatial))
- **Clair Variant Caller (Claude Skill)** (Categories: Molecular and Cellular Biology) — agent skill for the Clair suite: Clair3 (germline), Clair3-RNA (long-read RNA), ClairS / ClairS-TO (somatic), Clair-Mosaic; `git clone` into a skills dir ([source](https://github.com/HKU-BAL/Clair-skills))

### Updated
- **NCBI GEO** (`geo-database.md`) — added the first-party **MCPmed `geo-mcp`** MCP server (BSD-3-Clause, `pip install geo-mcp`, 7 tools over NCBI E-utilities, stdio/HTTP) as Option A; page generalized from a SciAgent-skill-only entry to a dual skill+MCP entry per one-entry-per-data-source; `last_verified` 2026-06-11 → 2026-06-27 ([source](https://github.com/MCPmed/GEOmcp))

### Flagged
- _None._

### Verified (no changes)
- `anthropics/life-sciences` (21 plugins) and `claude-plugins-official` marketplace inventories diffed against catalog — no new in-scope entries.

## 2026-06-27 (Integrative Structural and Computational Biology slot)

Integrative Structural and Computational Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` (21 plugins) and `claude-plugins-official` marketplaces hold no new in-scope life-science entries since the Boltz catalog earlier this run. The Structural directed pass (`RCSB PDB MCP server` and related queries) surfaced the **official first-party RCSB PDB MCP server**, folded into the existing `pdb.md` as the recommended install option. Also catalogued the last two genuinely new-to-catalog skills from `google-deepmind/science-skills` — **PyMOL** (structural visualization) and **EMBL-EBI OLS** (ontology resolution) — which exhausts that collection. Cryo-EM (RELION / cryoSPARC / CTFFIND) remains without any Claude-installable wrapper.

### Added
- **PyMOL (Claude Skill)** (Categories: Integrative Structural and Computational Biology) — headless, GPU-free PyMOL for rendering, structure superposition + RMSD, pLDDT/B-factor coloring, and protein–ligand interaction views, producing publication-quality PNGs and editable `.pse` sessions ([source](https://github.com/google-deepmind/science-skills/blob/main/skills/pymol/SKILL.md))
- **EMBL-EBI OLS (Claude Skill)** (Categories: All) — resolve and navigate biomedical ontology terms (GO, MONDO, HP, CHEBI, CL, UBERON, EFO, …) across 250+ ontologies via the EMBL-EBI Ontology Lookup Service ([source](https://github.com/google-deepmind/science-skills/blob/main/skills/embl_ebi_ols/SKILL.md))

### Updated
- **PDB MCP Server** (`pdb.md`) — added the **official first-party `rcsb-mcp`** server (maintained by RCSB PDB, MIT, `uvx rcsb-mcp`, official MCP Registry `io.github.rcsb/rcsb-mcp`, 40+ tools across the RCSB Search/Data/Sequence-Coordinates APIs) as the recommended Option A ahead of the three community servers; `last_verified` 2026-06-13 → 2026-06-27 ([source](https://github.com/rcsb/rcsb-mcp))

### Verified (no changes)
- `anthropics/life-sciences` (21 plugins) and `claude-plugins-official` marketplace inventories diffed against catalog — no new in-scope entries.

## 2026-06-27 (Immunology and Microbiology slot)

Immunology and Microbiology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace inventory is unchanged from the catalogued set. The Immunology pass (IEDB, antibody/ANARCI, AIRR-seq/Immcantation, metagenomics, AMR queries) again found no genuinely new Claude-installable component — IEDB, Immcantation/airrflow, QIIME2/Kraken2/MetaPhlAn, and AMRFinderPlus all remain CLI/pipeline tools with no discrete MCP/Skill wrapper (gaps tracked in curator state). Instead, catalogued a previously-deferred, primary-source-verified structural-biology skill from `google-deepmind/science-skills`.

### Added
- **Foldseek Structural Search (Claude Skill)** (Categories: Integrative Structural and Computational Biology) — submit a 3D protein structure and find structurally similar proteins across AFDB/PDB100/SwissProt and more via the hosted Foldseek API; resolves the long-deferred Foldseek-search gap with a verifiable upstream `SKILL.md` ([source](https://github.com/google-deepmind/science-skills/blob/main/skills/foldseek_structural_search/SKILL.md))

### Verified (no changes)
- `anthropics/life-sciences` marketplace inventory diffed against catalog — no new entries.

## 2026-06-27 (Chemistry slot)

Chemistry directed pass plus a manifest sweep. The `anthropics/claude-plugins-official` marketplace surfaced a new in-scope life-science plugin, **Boltz**, catalogued this run. The Chemistry directed pass (RDKit, Polaris, docking queries) found no genuinely new installable tools — the chemistry surface (rdkit-mcp, rdkit-skill, chemcp, chemlint, molecule-mcp, covasyn, autodock/smina/diffdock, datamol, medchem, molfeat, matchms) is already covered; Polaris ships no Claude wrapper, and the AKT1-only MCP_Vina remains deferred.

### Added
- **Boltz (Claude Code Plugin)** (Categories: Chemistry, Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology) — skills driving the hosted Boltz API for structure/binding prediction, small-molecule and protein/antibody screening, and de novo binder design; `/plugin install boltz@claude-plugins-official` ([source](https://github.com/boltz-bio/boltz-api-skills))

### Updated
- **Molecule-MCP** — re-verified upstream (`chatmol/molecule-mcp`, MIT, install instructions unchanged); `last_verified` 2026-05-20 → 2026-06-27 ([source](https://github.com/chatmol/molecule-mcp))

### Flagged
- _None._

### Verified (no changes)
- `anthropics/life-sciences` marketplace re-checked against the catalogued set (no new entries; all plugins already catalogued).
- RDKit MCP (`rdkit-mcp.md`) spot-checked upstream during the directed pass; still current (verified 2026-06-13).

## 2026-06-21 (Drug Repurposing and Discovery slot)

Drug Repurposing and Discovery directed pass plus a manifest sweep. The `anthropics/life-sciences` raw `marketplace.json` URL 404s; repo content still matches the catalogued set (no new entries). The directed pass surfaced the DrugBank official hosted MCP (paid/gated — noted on the existing community page) and confirmed three deferred ToolUniverse drug-discovery sibling skills against their upstream `SKILL.md` files, which were catalogued.

### Added
- **Drug Research (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — 12-step comprehensive drug dossier (mechanism, ADMET, trials, FAERS, pharmacogenomics, approval history) over the ToolUniverse MCP ([source](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-research/SKILL.md))
- **Drug Target Validation (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — four-gate 0–100 target validation score with GO/NO-GO tiers ([source](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-target-validation/SKILL.md))
- **Drug Synergy (ToolUniverse Claude Skill)** (Categories: Drug Repurposing and Discovery) — Bliss/HSA/Loewe/ZIP/Chou-Talalay combination-synergy scoring over user-supplied effect data ([source](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-drug-synergy/SKILL.md))

### Updated
- **DrugBank MCP Server** — added note + source for DrugBank's official hosted MCP (`go.drugbank.com/mcp`, paid DrugBank OS gated); `last_verified` 2026-05-20 → 2026-06-21 ([source](https://go.drugbank.com/mcp))

### Flagged
- _None._

### Verified (no changes)
- `anthropics/life-sciences` marketplace re-checked against the catalogued set (no new entries).

## 2026-06-21 (Translational Medicine slot)

Translational Medicine directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set (no new entries; the raw `marketplace.json` URL 404s but the repo content matches existing pages). The directed pass surfaced two distinct, MIT-licensed clinical MCP servers not previously catalogued. The Augmented-Nature OpenFDA device superset was re-investigated and remains deferred (license + registration snippet still unverified).

### Added
- **Momentum FHIR MCP Server** (Categories: Translational Medicine) — MIT FHIR R4 MCP with full CRUD plus document ingestion/chunking and Pinecone-backed semantic search; distinct from the WSO2 CRUD bridge and Anthropic `fhir-developer` authoring plugin ([source](https://github.com/the-momentum/fhir-mcp-server))
- **Medical Terminologies MCP** (Categories: Translational Medicine) — MIT MCP exposing 31–37 tools across ICD-11, SNOMED CT, LOINC, RxNorm, MeSH, and ATC with cross-mapping; broader than the single-terminology Anthropic ICD-10 connector ([source](https://github.com/SidneyBissoli/medical-terminologies-mcp))

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- `anthropics/life-sciences` marketplace re-checked against the catalogued set (no new entries).
- **Augmented-Nature OpenFDA-MCP-Server** re-investigated (10-tool drug+device list + clone/build steps now confirmed) but kept deferred — license still "standard licensing terms" only and no copy-pasteable registration snippet.

## 2026-06-21 (Neuroscience slot)

Neuroscience directed pass plus a manifest sweep — no substantive additions. The `anthropics/life-sciences` marketplace matched the catalogued set (no new entries). The Neuroscience directed pass (Allen Brain Atlas / NWB / DANDI / spike-sorting / EEG-fMRI seed queries) surfaced only tools already catalogued (`allenbrain-mcp`, SpikeLab, Neuropixels-Analysis) or already deferred/declined (`bendichter/dandi-query-mcp` boilerplate, ABC Atlas / BrainGlobe / OpenNeuro have no Claude-installable wrapper). The NeuroClaw collection (focus-category source) was re-diffed: all 86 upstream skills match `scripts/neuroclaw_category_map.yaml` exactly — none added, none removed.

### Added
- _None._

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- **allenbrain-mcp** — upstream repo still live, no LICENSE added, install path and 10-tool list unchanged; `last_verified` bumped to 2026-06-21 (license flag stands).
- `anthropics/life-sciences` marketplace re-checked against the catalogued set (no new entries).
- NeuroClaw (`CUHK-AIM-Group/NeuroClaw`) re-diffed in diff-only mode — 86 skills, all accounted for in the category map.

## 2026-06-20 (Molecular and Cellular Biology slot)

Molecular & cellular-biology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set (no new entries). The directed pass surfaced a new first-party skill collection, **`google-deepmind/science-skills`** (Apache-2.0 code / CC-BY-4.0 docs, ~37 skills, Agent Skills spec). Most of its skills wrap databases already catalogued (ChEMBL, ClinVar, dbSNP, Ensembl, gnomAD, ENCODE, etc.), but three are genuinely new and central to molecular/cellular biology and were added: **AlphaGenome single-variant analysis**, the **GTEx expression database** skill, and the **UniBind TF binding-sites** skill. Remaining new-to-catalog skills from this collection (foldseek structural search, EMBL-EBI OLS) are deferred.

### Added
- **AlphaGenome Single-Variant Analysis** (Categories: Molecular and Cellular Biology) — Claude Skill wrapping the AlphaGenome API to predict non-coding variant effects on expression, chromatin accessibility, histone marks, splicing, and TF binding; Apache-2.0, API key required ([source](https://github.com/google-deepmind/science-skills/blob/main/skills/alphagenome_single_variant_analysis/SKILL.md)).
- **GTEx Expression Database** (Categories: Molecular and Cellular Biology) — Claude Skill over the GTEx Portal API for median TPM expression across 54 tissues and eQTLs; Apache-2.0, no key ([source](https://github.com/google-deepmind/science-skills/blob/main/skills/gtex_database/SKILL.md)).
- **UniBind TF Binding Sites** (Categories: Molecular and Cellular Biology) — Claude Skill over the UniBind REST API for experimentally validated TF binding sites (BED/FASTA download); Apache-2.0, no key ([source](https://github.com/google-deepmind/science-skills/blob/main/skills/unibind_database/SKILL.md)).

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- `anthropics/life-sciences` marketplace re-checked against the catalogued set (no new entries).

## 2026-06-20 (Integrative Structural and Computational Biology slot)

Structural & computational-biology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set (no new entries). The directed pass found no Claude-installable cryo-EM (RELION/cryoSPARC/CTFFIND) wrapper — that gap persists. It surfaced two molecular-dynamics MCP candidates: **OpenMM MCP Server** (`PhelanShao/openmm-mcp-server`, GPLv3) was added as a new page — a discrete stdio server that *runs* MD/DFT jobs via managed tool calls, distinct from the existing K-Dense `molecular-dynamics` skill — while `egtai/gmx-vmd-mcp` was deferred (placeholder clone URL, unenumerated tools, unconfirmed license). The PDB and AlphaFold MCP candidates from the seed queries are already comprehensively catalogued (`pdb.md` covers all three RCSB/PDB servers).

### Added
- **OpenMM MCP Server** (Categories: Integrative Structural and Computational Biology, Drug Repurposing and Discovery) — stdio MCP server that sets up and runs OpenMM molecular dynamics (protein/membrane templates, advanced sampling) and Abacus DFT jobs from natural language; GPLv3, clone + `pip install -r requirements.txt` ([source](https://github.com/PhelanShao/openmm-mcp-server)).

### Updated
- **AlphaFold MCP Server** — re-verified upstream repo, install path, EBI API, and ~21–25 tool count; `last_verified` 2026-05-20 → 2026-06-20.

### Flagged
- _None._

### Verified (no changes)
- AlphaFold MCP Server (>30-day) re-verified; `anthropics/life-sciences` marketplace re-checked against the catalogued set.

## 2026-06-20 (Immunology and Microbiology slot)

Immunology and Microbiology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set (no new entries). The directed pass found no Claude-installable wrapper for IEDB, Immcantation/AIRR (BCR/TCR) repertoire analysis, or a discrete metagenomics/microbiome server — those gaps persist (deferred items unchanged). It did surface the **Bio-MCP** organization's discrete per-tool MCP servers; **BLAST** (`bio-mcp/bio-mcp-blast`, MIT) wraps NCBI BLAST+ as an MCP server with a clear clone-and-install path and was added as a new page (tagged `All`, since similarity search is a cross-cutting primitive heavily used in microbiology/metagenomics). Acted on user request #42 (open-targets): its `.request-bodies/42.md` prefetch is now present and the report is credible.

### Added
- **BLAST (Bio-MCP)** (Categories: All) — MCP server wrapping NCBI BLAST+ (`blastn`/`blastp`/`makeblastdb` + async job tools) over stdio; MIT, clone + `pip install -e .` ([source](https://github.com/bio-mcp/bio-mcp-blast)).

### Updated
- **Open Targets Plugin** — added a dated field report to Notes documenting a server-side MCP `initialize`-handshake failure (`-32602` under protocolVersion 2025-06-18 and 2024-11-05; no tools register) with two workarounds (direct GraphQL API; ToolUniverse `OpenTargets_*` tools); flagged in front-matter (per user request #42).

### Flagged
- **Open Targets Plugin** — remote MCP endpoint `https://mcp.platform.opentargets.org/mcp` non-compliant on `initialize` as of 2026-06-15 (reachable but returns `-32602`).

### Verified (no changes)
- 6 stale (>30-day) `anthropics/life-sciences` entries re-verified against the live marketplace listing (PubMed, BioRender, scvi-tools, single-cell-rna-qc, nextflow-development, instrument-data-to-allotrope); `last_verified` bumped.

## 2026-06-20 (Chemistry slot)

Chemistry directed pass plus a manifest sweep. The official MCP Registry surfaced **CovaSyn Chemistry MCP** (`com.covasyn/chemistry`, v1.27.2, registered 2026-06-02) — a hosted streamable-HTTP server with 130+ deterministic tools spanning ADMET, docking, retrosynthesis, ICH M7 toxicology, NMR/MS, and biologics design. It is installable today (free tier + `npx @covasyn/mcp-client` stdio proxy / remote `https://mcp.covasyn.com/mcp`), so it was added as a new page; it closes the long-standing "no Claude-installable retrosynthesis/ADMET wrapper" gaps noted in the curator state. The RDKit (`rdkit-mcp`, `rdkit-skill`), ChEMBL, PubChem, ChemLint, and ChemCP seed-query hits are already catalogued; AiZynthFinder/ASKCOS still ship only REST APIs with no discrete MCP/Skill, and Polaris has no Claude wrapper. User request #42 (open-targets) could not be actioned this run — the `.request-bodies/42.md` prefetch was missing, so the entry stays open per protocol.

### Added
- **CovaSyn Chemistry MCP** (Categories: Chemistry, Drug Repurposing and Discovery) — hosted deterministic cheminformatics MCP (130+ tools: ADMET, docking, retrosynthesis, ICH M7, NMR/MS, biologics); freemium, `npx @covasyn/mcp-client` or remote `https://mcp.covasyn.com/mcp` ([source](https://github.com/oliverkraft93-ops/covasyn-mcp-examples)).

### Verified (no changes)
- Chemistry seed queries (RDKit, retrosynthesis, ChEMBL, Polaris, cheminformatics MCP) re-run; all installable hits already catalogued.

## 2026-06-14

Drug Repurposing and Discovery directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set (PubMed, BioRender, Synapse, Scholar Gateway, Consensus, Cortellis, AdisInsight, 10x Genomics Cloud, the four skills, plus the noted `medidata`/`tooluniverse` — all have pages). The directed pass confirmed the official **Open Targets MCP** and the **ToolUniverse** MCP server are already catalogued, but found that the ToolUniverse repo also ships ~68 discrete **agent skills** under `skills/` (installable via `npx skills add mims-harvard/ToolUniverse`) that are distinct from the MCP-server entry. Added the **Drug Repurposing** skill (`tooluniverse-drug-repurposing`) as a new page; deferred the sibling drug-discovery skills. DrugBank and ADMET seed queries surfaced only already-catalogued or non-installable targets.

### Added
- **Drug Repurposing (Claude Skill)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — ToolUniverse agent skill identifying repurposing candidates via target-, compound-, and disease-driven strategies with mechanism and feasibility scoring; `npx skills add mims-harvard/ToolUniverse` (requires the ToolUniverse MCP server) ([source](https://github.com/mims-harvard/ToolUniverse)).

### Verified (no changes)
- `anthropics/life-sciences` marketplace re-fetched; all 13 entries already catalogued. Official Open Targets MCP (`open-targets.md`) and ToolUniverse MCP server (`tooluniverse.md`) confirmed current.

## 2026-06-14

Translational Medicine directed pass plus a manifest sweep of `anthropics/life-sciences`. Re-fetching the marketplace showed the `medidata` plugin now publishes a concrete HTTP MCP install path (`medidata/.claude-plugin/plugin.json` → `https://mcp.imedidata.com/mcp`), so the long-deferred **Medidata Connector** was promoted to a full page. The remaining clinical entries in the marketplace (clinical-trials, clinical-trial-protocol, cortellis, adisinsight) already have pages. FHIR (`fhir-developer`, `fhir-wso2`), CMS coverage, OpenFDA, and ClinicalTrials.gov directed-pass targets all matched catalogued entries; no other new installable Translational Medicine tool surfaced this slot.

### Added
- **Medidata Connector** (Categories: Translational Medicine) — Medidata's hosted clinical-trial MCP: Platform Help (Knowledge Hub Q&A for Rave EDC / Data Connect / Clinical Data Studio) and Predictive Site Ranking (rank trial sites by predicted enrollment during protocol planning); `/plugin install medidata@life-sciences` or `claude mcp add --transport http medidata https://mcp.imedidata.com/mcp` ([source](https://github.com/anthropics/life-sciences)).

### Verified (no changes)
- `anthropics/life-sciences` marketplace re-fetched; aside from `medidata` all clinical/translational plugins already catalogued.

## 2026-06-14

Neuroscience directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set (15 plugins/skills/connectors already have pages; `medidata` and `tooluniverse` remain noted/deferred); `anthropics/claude-plugins-official` contains no life-science plugins. The Neuroscience pass surfaced **SpikeLab** (`braingeneers/SpikeLab`, MIT) — a suite of computational-neuroscience agent skills for MEA spike-train data including a Kilosort2/4/RT-Sort spike-sorter skill and an optional built-in MCP server — added as a new page. The Allen Brain Atlas (`allenbrain-mcp`, already flagged on license) and AIND data MCP queries matched catalogued entries. While re-verifying, found that **Neurosift Tools MCP** now ships a `.claude-plugin` marketplace, so its page gained a `/plugin install neurosift-tools@neurosift-mcps` path alongside the existing manual build. The `mne-neurophysiology-analysis` mcpmarket listing and `dandi-query-mcp` boilerplate remain without a verifiable real tool surface and stay deferred.

### Added
- **SpikeLab** (Categories: Neuroscience) — Braingeneers agent-skill suite for MEA spike-train analysis and spike sorting (Kilosort2/Kilosort4/RT-Sort); `pip install "spikelab[all]"` + copy `agent/skills/` into `~/.claude/skills/`, with an optional MCP server via the `mcp` extra ([source](https://github.com/braingeneers/SpikeLab)).

### Updated
- **Neurosift Tools MCP** — added a Claude Code plugin-marketplace install path (`/plugin marketplace add` + `/plugin install neurosift-tools@neurosift-mcps`) and a Claude Desktop stdio JSON snippet; `last_verified` bumped (repo confirmed active per upstream README).
- **AIND Data MCP** — re-verified (repo active, MIT, `uvx`/`uv tool install aind-data-mcp`); `last_verified` bumped, no field changes.

### Verified (no changes)
- 1 additional Neuroscience entry spot-checked.

## 2026-06-13

Molecular and Cellular Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set (the `medidata` plugin remains gated behind account onboarding; `clinical-trial-protocol-skill` is already a page); `anthropics/claude-plugins-official` contains no life-science plugins. The directed pass surfaced the scmcphub single-cell MCP ecosystem — the already-catalogued `scanpy-mcp` has three sibling servers not yet in the catalog: **LIANA-MCP** (cell-cell communication), **decoupler-MCP** (pathway / TF activity), and **CellRank-MCP** (cell-fate / trajectory). Each is a discrete `pip`-installable MCP following the same `<pkg> run` stdio pattern, so all three were added as their own entries. No Bioconductor MCP and no standalone CRISPR-design MCP/Skill with a verifiable primary source surfaced this pass.

### Added
- **LIANA-MCP** (Categories: Immunology and Microbiology, Molecular and Cellular Biology) — scmcphub MCP wrapping liana-py for cell-cell communication (multi-method ligand-receptor inference, rank aggregation, circle/dotplot); `pip install liana-mcp` → `liana-mcp run` ([source](https://github.com/scmcphub/liana-mcp)).
- **decoupler-MCP** (Categories: Immunology and Microbiology, Molecular and Cellular Biology) — scmcphub MCP wrapping decoupler for pathway (PROGENy) and transcription-factor (CollecTRI) activity inference; `pip install decoupler-mcp` → `decoupler-mcp run` ([source](https://github.com/scmcphub/decoupler-mcp)).
- **CellRank-MCP** (Categories: Molecular and Cellular Biology) — scmcphub MCP wrapping CellRank for cell-fate / trajectory modeling (kernels, GPCCA, terminal/initial states, fate probabilities); `pip install cellrank-mcp` → `cellrank-mcp run` ([source](https://github.com/scmcphub/cellrank-mcp)).

## 2026-06-13

Integrative Structural and Computational Biology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set (all 21 plugins/skills/connectors already have pages); `anthropics/claude-plugins-official` contains no life-science plugins. The Structural pass surfaced one genuinely-new structural-biology MCP — `cyanheads/protein-mcp-server` (Apache-2.0, in the official MCP Registry), which orchestrates RCSB PDB + PDBe + UniProt with structure-similarity and ligand-tracking tools — folded into the existing `pdb.md` page as a third install option (one entry per data source). The ChatMol GROMACS/PyMOL/ChimeraX MCP and the AlphaFold DB MCP that the seed queries surfaced are already catalogued. A Foldseek structure-search skill (mcpmarket) and cryo-EM (RELION/cryoSPARC/EMDB) wrappers remain without verifiable primary sources and were deferred.

### Added
- **PDB MCP Server** (Categories: Integrative Structural and Computational Biology, Drug Repurposing and Discovery) — added `cyanheads/protein-mcp-server` (Apache-2.0) as a third install option on the existing page: a multi-provider MCP orchestrating RCSB PDB + PDBe + UniProt with `protein_search_structures` / `protein_get_structure` / `protein_find_similar` / `protein_track_ligands` ([source](https://github.com/cyanheads/protein-mcp-server)).

### Verified (no changes)
- **AlphaFold MCP Server** — re-verified upstream repo active, LICENSE present, ~20+ tools, install path unchanged (`last_verified` left at 2026-05-20 pending the next full sweep).

## 2026-06-13

Immunology and Microbiology directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set — every in-scope plugin/skill/connector is already a page. The Immunology pass surfaced one genuinely-new installable MCP server (Human Protein Atlas, an antibody-based resource). IEDB, BCR/TCR-repertoire (Immcantation), and metagenomics (Kraken2/QIIME2/MetaPhlAn) still lack discrete Claude-installable wrappers — BioinfoMCP is a converter framework, not a discrete tool — and were re-deferred; BoltzGen (binder/antibody design) was deferred as an unverifiable wrapper over a model-weight artifact.

### Added
- **Human Protein Atlas MCP Server** (Categories: Immunology and Microbiology, Molecular and Cellular Biology, Translational Medicine) — MIT; `Augmented-Nature/ProteinAtlas-MCP-Server`, 14 read-only tools over the Human Protein Atlas (protein search, tissue/blood/brain expression, subcellular localization, cancer prognostic markers, batch lookup, antibody validation/staining); stdio, install from source ([source](https://github.com/Augmented-Nature/ProteinAtlas-MCP-Server)).

### Flagged
- _None this slot._

### Verified (no changes)
- No entries are older than 30 days; nothing required re-verification this slot.

## 2026-06-13

Chemistry directed pass plus a manifest sweep. The `anthropics/life-sciences` marketplace matched the catalogued set — every in-scope plugin/skill/connector is already a page. The Chemistry pass surfaced two genuinely-new installable cheminformatics MCP servers (ChemLint, ChemCP); MoziChem-MCP (chemical-engineering thermodynamics) and the still-missing retrosynthesis wrapper were deferred.

### Added
- **ChemLint** (Categories: Chemistry, Drug Repurposing and Discovery) — MIT; `molML/ChemLint` MCP server exposing 150+ molecular machine-learning tools (SMILES cleaning, descriptors/fingerprints, scaffolds, similarity/clustering, 33+ ML algorithms, stats, activity cliffs, dim-reduction); stdio, `uv`-launched ([source](https://github.com/molML/ChemLint)).
- **ChemCP** (Categories: Chemistry) — `scottmreed/ChemCP` MCP App rendering interactive 2D molecular structures from SMILES via RDKit.js with basic property readouts; npm install, stdio for Desktop / HTTP+tunnel for Claude.ai. License undeclared upstream — flagged ([source](https://github.com/scottmreed/ChemCP)).

### Updated
- **RDKit MCP Server (TandemAI)** — re-verified; source live, `last_verified` 2026-05-20 → 2026-06-13 (no field changes).

### Flagged
- **ChemCP** — no LICENSE file declared upstream; Free / OSS claim and redistribution terms marked `Unverified —` pending an explicit license.

### Verified (no changes)
- 1 entry re-verified (rdkit-mcp).

## 2026-06-11

Two threads this date: (1) the daily directed pass on **Molecular and Cellular Biology** (Thursday focus) plus a manifest sweep and one user-request action; and (2) a **batch ingest of two life-science skill collections** following the K-Dense precedent (2026-06-04). For the batch, the K-Dense-only ingester was generalised into a reusable, collection-parameterised pipeline — `scripts/ingest_collection.py` driven by `scripts/collections.yaml` (per-collection registry) + an auditable `scripts/<collection>_category_map.yaml` (include = CREATE a new page, augment = add this collection's install path to an existing page, skip = recorded out-of-scope). It handles flat and nested `skills/` layouts and idempotent augmentation (a `<!-- alt-install:<key> -->` sentinel). Catalog tool pages: 179 -> 338. The `anthropics/life-sciences` marketplace matched the catalogued set — every in-scope plugin/skill is already a page; `biorxiv`/`clinical-trials` stay flagged (`mcp.deepsense.ai` NXDOMAIN).

### Added
- **SciAgent-Skills** (`jaechang-hits/SciAgent-Skills`, 197 skills, CC BY 4.0, BixBench-evaluated) — **89 new pages**: genomics (BWA-MEM2, STAR, Salmon, SAMtools/BCFtools, GATK, CNVkit, SnpEff, PLINK2, DESeq2, featureCounts, GSEApy, fastp, MultiQC, BEDtools, CellTypist, Harmony, popV) and ~24 reference-database skills (ENCODE, ClinVar, dbSNP, gnomAD, COSMIC, cBioPortal, GWAS Catalog, ClinPGx, JASPAR, ReMap, RegulomeDB, QuickGO, Monarch, KEGG, Reactome, STRING, BRENDA, ARCHS4, GEO, NCBI Gene, UCSC, Mouse Phenome Database, **ZINC**, openFDA, DailyMed, DDInter, Open Targets, GtoPdb, UniChem, EMDB, HMDB, Metabolomics Workbench, PRIDE, InterPro, MaxQuant); docking & MD (AutoDock Vina, smina, MDAnalysis, MDTraj); bio-imaging (Cellpose, napari, OpenCV, PyImageJ, scikit-image, trackpy); plus SAR analysis, ViennaRNA, pLannotate, sgRNA design, HOMER, MACS3, CellChat, libSBML, MOFA+, muon, SpikeInterface, nnU-Net, SimpleITK, Snakemake, Plotly, OpenAlex, bioRxiv, USPTO. **93 existing pages** gained a SciAgent alternative install path (one entry per tool — incl. the Ensembl skill folded into the same-day `ensembl` MCP page). 15 out of scope — recorded in `scripts/sciagent_category_map.yaml`.
- **NeuroClaw** (`CUHK-AIM-Group/NeuroClaw`, 86 skills, MIT) — **68 new Neuroscience pages**: tool/modality wrappers (FreeSurfer, FSL, fMRIPrep, QSIPrep, CONN, DIPY, MNE-Python, Nilearn, NiBabel, dcm2niix, nii2dcm, NeuroHarmonize, WMH/ASL/PET/DWI/EEG/fMRI/sMRI/MEG, brain visualization), dataset pipelines (ADNI, UK Biobank, HCP-A/D/EP/YA, ABCD, ABIDE, ADHD-200, AIBL, AOMIC, BOLD5000, Cam-CAN, COBRE, HBN, IXI, NSD, OASIS, PNC, PPMI, REST-meta-MDD, SEED-IV/VIG, TCP, UCLA-CNP, NIFD, MND, MS-Challenge, DMT-HAR-MED), and phenotype-prediction model docs (BrainNetworkTransformer, BrainGNN, Com-BrainTF, IBGNN, LG-GNN, FM-APP, NeuroSTORM, GLM, ICA, K-means, SVM, SpaceNet, dictionary learning, detrending, filtering, hierarchical). 1 augment (`bids`). 17 skipped — recorded in `scripts/neuroclaw_category_map.yaml`.
- **Biomni** (Categories: All) — Stanford SNAP Lab general-purpose biomedical AI agent; Claude Code skill via `npx skills add … --skill biomni` driving the `biomni` PyPI package (~11GB data lake). Apache-2.0; some bundled tools more restrictive ([source](https://github.com/snap-stanford/Biomni)).
- **Ensembl MCP Server** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine) — MIT; npm `ensembl-mcp-server`, 10 read-only tools over the Ensembl REST API ([source](https://github.com/effieklimi/ensembl-mcp-server)). The SciAgent Ensembl REST skill was folded into this page as an alternative install path rather than created as a duplicate.

### Updated
- 93 existing tool pages augmented with a SciAgent (92) or NeuroClaw (1) alternative install path. AGENT.md community-collections table + batch-ingest note updated; `scripts/ingest_collection.py` + `scripts/collections.yaml` added; SciAgent and NeuroClaw moved to diff-only mode. `curator-state.md`: ZINC, Ensembl/UCSC MCP, and mne-neurophysiology deferred entries updated to reflect now-catalogued coverage.
- **10x Genomics Cloud MCP** — user field report (#26, "worked great") confirming the Claude Code plugin-marketplace install path; added a dated note in **Notes**, `last_verified` -> 2026-06-11.

### Flagged
- **OpenClaw-Medical-Skills** (`FreedomIntelligence/OpenClaw-Medical-Skills`) deferred on a **license contradiction** — README markets it as open-source, but there is no repo LICENSE file and 185 of 449 `SKILL.md` files carry an "All Rights Reserved … unauthorized copying strictly prohibited" proprietary header. Not ingested; see `curator-state.md`. Most of its life-science surface is already covered by the cleanly-licensed K-Dense/SciAgent ingests.

### Verified (no changes)
- `anthropics/life-sciences` marketplace diffed — no new plugins/skills. All 13 entries (PubMed, BioRender, Synapse, Scholar Gateway, Consensus, Cortellis, AdisInsight, 10x Genomics, single-cell-rna-qc, instrument-data-to-allotrope, nextflow-development, scvi-tools, scientific-problem-selection) already catalogued.

## 2026-06-09

Directed pass on **Immunology and Microbiology** (Tuesday focus) plus a manifest sweep. WebFetch was unavailable from the runner this entire run (every call returned a backend model 404 — `claude-3-5-haiku` not found), and all `raw.githubusercontent.com`/`github.com`/`api.github.com` `marketplace.json` fetches returned 404, so the marketplace diff and candidate verification leaned on corroborated WebSearch results only. The directed-pass seed queries (IEDB epitope MCP, antibody-design skill, BCR/TCR repertoire MCP, metagenomics/microbiome MCP) reconfirmed the three previously-logged gaps: no Claude-installable wrapper exists for IEDB's PostgREST Query API, for AIRR-seq tooling (Immcantation / nf-core/airrflow / immunarch / immuneML), or for metagenomics pipelines (QIIME2 / Kraken2 / MetaPhlAn). The `anthropics/life-sciences` marketplace contents matched the catalogued set (no new plugins), and a K-Dense diff via search showed the collection steady at ~140/142 skills with no net-new immunology/microbiology directories. No new candidate could be verified to the followable-verbatim install standard from a primary source, so no tool pages were created. No `last_verified` dates exceed the 30-day window (oldest is 2026-05-19, 21 days).

### Added
- _None._

### Updated
- _None._

### Flagged
- _None._

### Verified (no changes)
- Immunology/Microbiology-relevant entries reviewed against today's seed queries; install paths and capability descriptions remain accurate. IEDB, AIRR-seq (BCR/TCR repertoire), and metagenomics/microbiome confirmed still uncovered by any Claude-installable wrapper — deferral dates refreshed in `curator-state.md`.

## 2026-06-08

Directed pass on **Chemistry** (Monday focus) plus a manifest sweep. WebFetch was unavailable from the runner this entire run (every call returned a backend model 404 — `claude-3-5-haiku` not found), and all `raw.githubusercontent.com`/`api.github.com` `marketplace.json` fetches returned 404, so the marketplace diff and candidate verification leaned on corroborated WebSearch results only. Because no new candidate could be verified to the followable-verbatim install standard from a primary source this run, no new tool pages were created. The Chemistry surface is already broad (`rdkit-mcp`, `rdkit-skill`, `pubchem`, `chembl`, `datamol`, `molfeat`, `medchem`, `deepchem`, `diffdock`, `rowan`, `matchms`, `pytdc`, `torchdrug`, `molecule-mcp`, `pyopenms`). The directed-pass seed queries (RDKit MCP, retrosynthesis MCP, ChEMBL MCP, Polaris, PubChem MCP) surfaced one genuinely new install path — a hosted/typescript PubChem server (`cyanheads/pubchem-mcp-server`) with an 8-tool read-only surface and a public Streamable HTTP endpoint — which was folded into the existing `pubchem` entry per the one-entry-per-tool rule. Two Chemistry candidates were deferred: a **ZINC Database** Claude Code skill (`davila7/claude-code-templates`) whose exact install flag and SKILL.md tool list could not be verified with WebFetch down, and **retrosynthesis** wrappers (AiZynthFinder/ASKCOS/IBM RXN), still without a Claude-installable surface.

### Updated
- **PubChem MCP Server** — added the `cyanheads/pubchem-mcp-server` install paths (hosted Streamable HTTP `https://pubchem.caseyjhand.com/mcp` via `claude mcp add --transport http`; `mcp-remote` proxy for Claude Desktop; local `bunx` stdio) and documented its wider 8-tool surface — substructure/superstructure/2D-similarity search and GHS hazard classification — alongside the existing JackKuo666 server; `last_verified` 2026-05-20 → 2026-06-08 ([cyanheads/pubchem-mcp-server](https://github.com/cyanheads/pubchem-mcp-server), [npm](https://www.npmjs.com/package/@cyanheads/pubchem-mcp-server)).

### Flagged
- _None._

### Verified (no changes)
- Chemistry-tagged entries (`rdkit-mcp`, `chembl`, `datamol`, `molfeat`, `medchem`, `deepchem`, `diffdock`, `rowan`, `matchms`, `pytdc`, `torchdrug`) reviewed against today's seed queries — install paths and capability descriptions remain accurate. Retrosynthesis confirmed still uncovered by any Claude-installable wrapper.

## 2026-06-07

Directed pass on **Drug Repurposing and Discovery** (Sunday focus) plus a manifest sweep of `anthropics/life-sciences`. WebFetch and `curl` were both unavailable from the runner this run (WebFetch returned a backend model 404; raw `marketplace.json` fetch was not permitted), so the marketplace diff and candidate verification leaned on corroborated WebSearch results plus the Clarivate press release and the existing first-party plugin pattern (`adisinsight`, `open-targets`). Surfaced two first-party plugins from the deferred queue — **Cortellis** (Clarivate regulatory/pipeline intelligence) and **Consensus** (literature evidence synthesis) — both confirmed as `life-sciences` marketplace plugins with subscription/account gating. The directed-pass seed queries (Open Targets MCP, DrugBank MCP, drug-repurposing/target-prioritization MCP) surfaced only tools already catalogued (`open-targets`, `chembl`, `drugbank`, `pubchem`); no new standalone discovery MCP warranted an entry. No `last_verified` dates exceed the 30-day window (oldest is 2026-05-19, 19 days).

### Added
- **Cortellis Plugin** (Categories: Drug Repurposing and Discovery, Translational Medicine) — Clarivate Cortellis MCP plugin in `anthropics/life-sciences`; global drug-pipeline, clinical-trial, regulatory, safety, and deals intelligence; subscription-gated, free install ([anthropics/life-sciences](https://github.com/anthropics/life-sciences), [Clarivate](https://clarivate.com/news/clarivate-expands-access-to-trusted-regulatory-intelligence-within-claude/)).
- **Consensus Plugin** (Categories: All) — Consensus.app MCP plugin in `anthropics/life-sciences`; AI-powered scientific literature search and evidence synthesis; free Consensus account required ([anthropics/life-sciences](https://github.com/anthropics/life-sciences), [Consensus](https://consensus.app/)).

### Verified (no changes)
- 178 tool pages spot-checked for `last_verified` recency; all current within the 30-day window. Drug-discovery-tagged entries (`open-targets`, `chembl`, `drugbank`, `pubchem`, `adisinsight`, `owkin`) reviewed against today's seed queries — install paths and capability descriptions remain accurate.

## 2026-06-06

Directed pass on **Translational Medicine** (Saturday focus) plus a manifest sweep. WebFetch was unreliable this run (the `anthropics/life-sciences` raw `marketplace.json`, GitHub READMEs, npm, and the MCP Registry API all returned backend 404/403 to automated fetches), so candidate verification leaned on corroborated WebSearch results across the npm listing, Glama, and the author's own write-ups. Surfaced one fully-verifiable Translational entry from the deferred queue (`@ythalorossy/openfda`). The AACT Clinical Trials MCP (`navisbio`) was re-investigated but held back — its license is reported inconsistently (MIT vs GPLv3) and the canonical repo/package path is ambiguous (`aact_mcp` vs `mcp-server-aact`); deferred pending a primary-source license confirmation. No `last_verified` dates exceed the 30-day window (oldest is 2026-05-19, 18 days).

### Added
- **OpenFDA MCP Server (ythalorossy)** (Categories: Drug Repurposing and Discovery, Translational Medicine) — MIT-licensed npm MCP server (`@ythalorossy/openfda`) exposing 7 openFDA drug tools (adverse events, safety/labeling, manufacturer, NDC resolution); fully copy-pasteable `claude mcp add-json` and Claude Desktop install paths ([github](https://github.com/ythalorossy/openfda), [npm](https://www.npmjs.com/package/@ythalorossy/openfda)).

### Verified (no changes)
- 176 tool pages spot-checked for `last_verified` recency; all current within the 30-day window.

## 2026-06-05

Directed pass on **Neuroscience** (Friday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-06-04 — same 10-plugin set; `biorxiv@life-sciences` / `clinical-trials@life-sciences` remain DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). Directed-pass seed queries (Allen Brain Atlas MCP, NWB MCP, fMRI / fMRIPrep Claude skill, MNE-Python skill, spike sorting MCP, DANDI MCP) surfaced only candidates already catalogued — the credible Neuroscience surface is well covered: `allenbrain` (Allen Brain Atlas RMA MCP), `neurosift` (DANDI/OpenNeuro + NWB introspection + PyNWB docs search MCP), `openneuro` (OpenNeuro GraphQL MCP), `aind-data` (AIND Metadata MCP + NWB file access), `neurokit2` (Claude Skill — biosignals, with MNE integration in `references/eeg.md`), `neuropixels-analysis` (Claude Skill — Kilosort4 / SpykingCircus2 / Mountainsort5 spike-sorting pipeline incl. AI-assisted curation), and `bids` (Claude Skill — BIDS spec + fMRIPrep / MRIQC / QSIPrep BIDS-Apps). Two listings investigated and not added: an `mne-neurophysiology-analysis` MCP-market entry without a verifiable upstream GitHub source, and `bendichter/dandi-query-mcp` whose advertised tool surface is the boilerplate note-server template (create_note / summarize_notes), not a real DANDI wrapper — and DANDI semantic search is already covered by `neurosift`. No new entries this run; no `last_verified` dates older than 30 days (oldest is 2026-05-19, 17 days).

### Verified (no changes)
- 176 tool pages spot-checked for `last_verified` recency; all current within the 30-day window. The Neuroscience-tagged subset (7 pages) reviewed against today's seed queries — all install paths and capability descriptions remain accurate.

## 2026-06-04 — General-Purpose Utilities category

**Added an 8th catalog category, `General-Purpose Utilities`, and ingested the domain-agnostic remainder of the K-Dense collection into it.** Recipes assemble horizontal tooling (plotting, dataframes, ML/stats, scientific communication) alongside domain tools, so these belong in the catalog even though they aren't life-science-specific. The new category is a **cross-cutting utilities shelf**, not a research area: tools tagged `General-Purpose Utilities` appear only on the [utilities index](catalog/general-purpose-utilities.html), never on the seven research-area pages, and never carry the `All` tag. 68 previously-skipped K-Dense skills moved in (including `consciousness-council`, a multi-perspective deliberation utility); only 3 remain out of scope (`dhdna-profiler`, `market-research-reports`, `paperzilla` — novelty / business / product-locked, not reusable utilities). Catalog now totals 175 tool pages (after merging the concurrent daily curator run that had independently surfaced COBRApy / DiffDock / Adaptyv / DeepChem / PyTDC).

### Added
- **New category index** `catalog/general-purpose-utilities.html` (nav_order 8). `AGENT.md`, root `README.md`, and `catalog/README.md` updated to describe the seven research areas **plus** the utilities shelf; `RECIPE_AGENT.md` clarified that recipes use only the seven research-area subject areas (utilities are ingredients, not a problem domain).
- **67 General-Purpose Utilities skill pages** (K-Dense), including: data/compute — `polars`, `dask`, `vaex`, `zarr-python`, `networkx`, `modal`, `optimize-for-gpu`; viz/communication — `matplotlib`, `seaborn`, `scientific-visualization`, `scientific-schematics`, `scientific-writing`, `scientific-slides`, `latex-posters`/`pptx-posters`, `infographics`, `generate-image`, `markdown-mermaid-writing`, `markitdown`, `liteparse`, `pdf`/`docx`/`pptx`/`xlsx`, `citation-management`, `pyzotero`, `venue-templates`, `peer-review`, `scholar-evaluation`, `research-grants`; ML/stats — `scikit-learn`, `statsmodels`, `pymc`, `shap`, `umap-learn`, `sympy`, `pytorch-lightning`, `torch-geometric`, `transformers`, `stable-baselines3`, `pufferlib`, `pymoo`, `aeon`, `timesfm-forecasting`; literature/web — `paper`-style `exa-search`, `parallel-web`, `research-lookup`, `open-notebook`, `bgpt`-style; adjacent-domain science — `qiskit`, `cirq`, `pennylane`, `qutip`, `pymatgen`, `astropy`, `geopandas`, `geomaster`, `fluidsim`, `matlab`; misc utilities — `exploratory-data-analysis`, `statistical-analysis`, `hypogenic`, `hugging-science`, `autoskill`, `get-available-resources`, `what-if-oracle`, `usfiscaldata`, `consciousness-council`.

### Updated
- **`scripts/kdense_category_map.yaml`** — 66 entries moved from `skip` to `include` tagged `[General-Purpose Utilities]`, `parallel-web` added; `skip` trimmed to the 4 genuine non-utilities with reasons.
- **`scripts/ingest_kdense.py`** — `PRETTY` display-name map extended for the 67 utility skills.

### Verified (no changes)
- All 173 tool pages pass front-matter lint; the seven research-area card counts are unchanged (utilities are tagged on the shelf only and do not appear on research-area pages); every `General-Purpose Utilities` tool is tagged on the shelf alone.

## 2026-06-04

**One-time batch ingestion of the K-Dense `scientific-agent-skills` collection.** Rather than continue surfacing K-Dense skills one or two at a time under the ≤5/run soft cap (the `Deferred` queue had grown a long K-Dense backlog), this run ingests the whole life-science-relevant subset in a single auditable pass and switches the K-Dense source to diff-only mode for future runs. The collection has 143 skills; **69 are life-science-relevant** and are now catalogued (51 new pages + 18 existing K-Dense pages repaired). The remaining ~74 are general-purpose (quantum computing, materials science, generic ML/stats/viz, office-document and web-search tooling, infra) and are out of scope — enumerated with reasons in `scripts/kdense_category_map.yaml` so future runs don't re-evaluate them. Generated pages are schema-accurate but intentionally lean (built from each skill's `SKILL.md` front-matter via `scripts/ingest_kdense.py`); subsequent daily runs enrich them. Also fixes a real upstream breakage: K-Dense migrated `scientific-skills/<name>/` → `skills/<name>/` and replaced the (non-existent) `claude-scientific-skills` plugin marketplace with `npx skills add` — every existing K-Dense page carried broken install steps.

### Added
51 new K-Dense Claude Skill pages (source: [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)):
- **Chemistry / Drug discovery** — `deepchem`, `diffdock`, `matchms`, `pytdc`, `rowan`, `torchdrug`
- **Structural & computational biology** — `esm`, `pyopenms`, `adaptyv`
- **Molecular & cellular biology / genomics** — `biopython`, `bioservices`, `bulk-rnaseq`, `cobrapy`, `deeptools`, `etetoolkit`, `geniml`, `gtars`, `lamindb`, `pathway-enrichment`, `phylogenetics`, `polars-bio`, `pysam`, `tiledbvcf`, `primekg`
- **Lab platforms & data integrations** — `benchling-integration`, `dnanexus-integration`, `ginkgo-cloud-lab`, `labarchive-integration`, `latchbio-integration`, `omero-integration`, `opentrons-integration`, `protocolsio-integration`, `pylabrobot`
- **Translational medicine / clinical / imaging** — `clinical-decision-support`, `clinical-reports`, `treatment-plans`, `pyhealth`, `pydicom`, `histolab`, `pathml`, `imaging-data-commons`, `pacsomatic`, `scikit-survival`, `iso-13485-certification`
- **Cross-cutting (`All`)** — `database-lookup`, `paper-lookup`, `literature-review`, `bgpt-paper-search`, `hypothesis-generation`, `scientific-brainstorming`, `scientific-critical-thinking`

### Updated
- **Install-path migration fix on 18 existing K-Dense pages** — `anndata`, `arboreto`, `bids`, `cellxgene-census`, `datamol`, `depmap`, `flowio`, `gget`, `glycoengineering`, `medchem`, `molecular-dynamics`, `molfeat`, `neurokit2`, `neuropixels-analysis`, `pydeseq2`, `rdkit-skill`, `scikit-bio`, `scvelo`. Replaced the dead `claude-scientific-skills` plugin-marketplace block with `npx skills add K-Dense-AI/scientific-agent-skills`, migrated `scientific-skills/` → `skills/` clone paths, and bumped `last_verified`.
- **Three "one entry per tool" augments** — added the K-Dense skill as an alternative install path on `scanpy` (existing scmcphub MCP), `scvi-tools` (existing Anthropic skill), and `nextflow-development` (existing Anthropic skill) rather than creating duplicate pages.
- **`AGENT.md`** — K-Dense source switched to **diff-only mode**: fully ingested as of 2026-06-04; future runs diff `skills/` against catalogued K-Dense slugs and add only *new* skills / flag *removed* ones, instead of incrementally surfacing the backlog.
- **`catalog/curator-state.md`** — cleared the now-ingested K-Dense items from `Deferred`; `Recently surfaced` collapsed to a single batch line.
- **New pipeline files** — `scripts/kdense_category_map.yaml` (auditable scope filter + category map) and `scripts/ingest_kdense.py` (the generator/repairer), reusable for future collection batches (SciAgent-Skills, OpenClaw-Medical-Skills, NeuroClaw).

### Verified (no changes)
- All 106 tool pages pass front-matter lint (required fields, ≤25-word summaries, canonical categories, slug-matched feedback footers).
## 2026-06-04

Directed pass on **Molecular and Cellular Biology** (Thursday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-06-03 — same 10-plugin set (pubmed, biorender, synapse, wiley-scholar-gateway, 10x-genomics, single-cell-rna-qc, instrument-data-to-allotrope, nextflow-development, scvi-tools, scientific-problem-selection); `biorxiv@life-sciences` / `clinical-trials@life-sciences` remain DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). The directed pass surfaced **COBRApy (Claude Skill)** from the standing Deferred queue — the K-Dense skill wrapper around `opencobra/cobrapy`, the canonical Python library for constraint-based reconstruction and analysis of genome-scale metabolic models. COBRApy fills the metabolism slice that none of the existing Molecular and Cellular Biology entries cover: `scanpy` / `scvelo` / `arboreto` / `pydeseq2` / `scvi-tools` / `cellxgene-census` are transcriptomics, `gget` / `uniprot` are sequence/identifier resolvers, and `single-cell-rna-qc` is QC — none drive FBA / FVA / knockout screens / flux sampling on SBML models. One new entry, well under the 5-entry soft cap; no user-feedback issues in the open queue this run.

### Added
- **COBRApy (Claude Skill)** (Categories: Molecular and Cellular Biology, Chemistry, Drug Repurposing and Discovery) — K-Dense skill driving COBRApy for constraint-based metabolic modelling. Loads SBML / JSON / YAML genome-scale models; runs flux balance analysis (FBA, pFBA, geometric FBA), flux variability analysis (with loopless option and `fraction_of_optimum` control), single and double gene/reaction knockouts, Markov-chain flux sampling, production envelopes, and gapfilling. Solver backends pluggable via `model.solver` (GLPK default; CPLEX / Gurobi for large models). Skill is MIT-licensed (collection); COBRApy itself is GPL-2.0 — review for commercial use ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/cobrapy/SKILL.md), [`opencobra/cobrapy`](https://github.com/opencobra/cobrapy), [Ebrahim et al. *BMC Syst. Biol.* 2013](https://bmcsystbiol.biomedcentral.com/articles/10.1186/1752-0509-7-74), [Playbooks: cobrapy skill](https://playbooks.com/skills/k-dense-ai/claude-scientific-skills/cobrapy)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with the COBRApy addition (oldest of the prior five — `npi-registry` — rolled off; `diffdock`, `adaptyv`, `deepchem`, `pytdc` carried forward). Deferred queue: removed `cobrapy` from the `TorchDrug / PyOpenMS / matchms / cobrapy` chemistry-stack-siblings line (cobrapy now surfaced); annotated the residual line with promotion dates and what each remaining sibling covers (TorchDrug = protein representation learning; PyOpenMS = MS proteomics; matchms = MS/MS spectral matching).

### Verified (no changes)
- Existing Molecular and Cellular Biology entries (`scanpy` last_verified 2026-05-26, `anndata` 2026-05-26, `scvi-tools` 2026-05-22, `pydeseq2` 2026-05-21, `scvelo` 2026-05-28, `arboreto` 2026-05-28, `cellxgene-census` 2026-05-29, `single-cell-rna-qc` 2026-05-22, plus cross-cutting `All`-tagged tools `gget`, `uniprot`, `pubmed`, `biomcp`, `biocontextai`) all within the 30-day verification window — no scheduled re-verification needed this run.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no diff vs. 2026-06-03; `biorxiv` / `clinical-trials` plugins still DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). Deferred queue (Cortellis, Medidata, Consensus, Augmented-Nature ChEMBL, AACT, OpenFDA / Azure FHIR, NeuroClaw, MCP_Vina, TorchDrug / PyOpenMS / matchms, IEDB / Immcantation / metagenomics, Cryo-EM, RFdiffusion / ProteinMPNN, Rowan, Boltz / Protein Hunter) carries forward.

### User requests
- `## User requests (open)` was empty entering this run — nothing to action; section remains `_None._`.

## 2026-06-03

Directed pass on **Integrative Structural and Computational Biology** (Wednesday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-06-02 — same 10-plugin set (pubmed, biorender, synapse, wiley-scholar-gateway, 10x-genomics, single-cell-rna-qc, instrument-data-to-allotrope, nextflow-development, scvi-tools, scientific-problem-selection); `biorxiv@life-sciences` / `clinical-trials@life-sciences` remain DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). The directed pass surfaced **DiffDock (Claude Skill)** from the standing Deferred queue — the K-Dense skill wrapper around `gcorso/DiffDock`, a diffusion-generative docker that predicts protein–ligand binding poses from a PDB structure plus a ligand SMILES, without exhaustive grid search. DiffDock complements the existing Structural-bio set: `alphafold` and `pdb` supply the receptor structure, `molecular-dynamics` refines the predicted poses, `molecule-mcp` visualises them in PyMOL/ChimeraX, and `deepchem` / `medchem` / `pytdc` re-score with affinity models. The Structural-bio pass also re-checked Cryo-EM (RELION / cryoSPARC / CTFFIND), RFdiffusion / ProteinMPNN standalone wrappers, Rowan MCP (`k-yenko/rowan-mcp`), and the Boltz / Protein Hunter MCPs (`longevity-genie/protein_hunter_mcp`, `biomolecular-design-nexus/boltz_mcp`) — none have a copy-pasteable Claude-installable path today, all now in the Deferred queue with the date stamped 2026-06-03. One new entry, well under the 5-entry soft cap; no user-feedback issues in the open queue this run.

### Added
- **DiffDock (Claude Skill)** (Categories: Drug Repurposing and Discovery, Integrative Structural and Computational Biology) — K-Dense skill driving DiffDock for diffusion-based protein–ligand docking. Generates N diffusion-sampled binding poses (default 10–40) with per-pose confidence scores; bundled scripts (`prepare_batch_csv.py`, `analyze_results.py`, `setup_check.py`) and references (`confidence_and_limitations.md`, `parameters_reference.md`, `workflows_examples.md`) for virtual screening, lead optimisation, and blind docking against AlphaFold-predicted targets. Poses only — pair with GNINA / Vina / MM-GBSA / FEP for affinity. MIT-licensed skill, MIT-licensed model ([source](https://github.com/K-Dense-AI/claude-scientific-skills/blob/main/scientific-skills/diffdock/SKILL.md), [DiffDock — `gcorso/DiffDock`](https://github.com/gcorso/DiffDock), [Corso et al. *ICLR* 2023](https://arxiv.org/abs/2210.01776), [Playbooks: diffdock skill](https://playbooks.com/skills/k-dense-ai/claude-scientific-skills/diffdock)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with the DiffDock addition (oldest of the prior five — `openneuro` — rolled off; `adaptyv`, `deepchem`, `pytdc`, `npi-registry` carried forward). Deferred queue: removed `DiffDock` from the `TorchDrug / DiffDock / PyOpenMS / matchms / cobrapy` chemistry-stack-siblings line (DiffDock now surfaced); bumped the Cryo-EM and RFdiffusion / ProteinMPNN re-check dates to 2026-06-03 and noted that RFdiffusion / ProteinMPNN ship bundled inside `longevity-genie/protein_hunter_mcp`; added two new Structural-pass deferred lines — `Rowan MCP` (`k-yenko/rowan-mcp`) and `Boltz / Protein Hunter MCP`.

### Verified (no changes)
- Existing Integrative Structural and Computational Biology entries (`alphafold` last_verified 2026-05-19, `pdb` 2026-05-19, `molecular-dynamics` 2026-05-27, `molecule-mcp` 2026-05-20, plus the cross-cutting `All`-tagged tools `gget`, `uniprot`, `pubmed`, `biomcp`, `biocontextai`) all within the 30-day verification window — no scheduled re-verification needed this run.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no diff vs. 2026-06-02; `biorxiv` / `clinical-trials` plugins still DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). Deferred queue (Cortellis, Medidata, Consensus, Augmented-Nature ChEMBL, AACT, OpenFDA / Azure FHIR, NeuroClaw, MCP_Vina, TorchDrug / PyOpenMS / matchms / cobrapy, IEDB / Immcantation / metagenomics, Cryo-EM, RFdiffusion / ProteinMPNN, Rowan, Boltz / Protein Hunter) carries forward.

### User requests
- `## User requests (open)` was empty entering this run — nothing to action; section remains `_None._`.

## 2026-06-02

Directed pass on **Immunology and Microbiology** (Tuesday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-06-01 — same 10-plugin set (pubmed, biorender, synapse, wiley-scholar-gateway, 10x-genomics, single-cell-rna-qc, instrument-data-to-allotrope, nextflow-development, scvi-tools, scientific-problem-selection), and `biorxiv@life-sciences` / `clinical-trials@life-sciences` remain DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). The directed pass surfaced **Adaptyv (Claude Skill)** from the standing Deferred queue — the K-Dense skill that closes the design–build–test loop on the Adaptyv cloud lab, pre-screening sequences in silico (NetSolP / SoluProt / SolubleMPNN / ESM / ipTM / pSAE) and submitting them to wet-lab binding (BLI K_D / k_on / k_off), expression (E. coli / mammalian / yeast / insect), thermostability (DSF / CD), and enzyme-activity assays. Adaptyv is the first Immunology-tagged entry covering the actual antibody-design → wet-lab handoff (the existing `glycoengineering` entry covers glycan-shield analysis but not the design-build-test loop). The Immunology pass also re-checked the IEDB Query API, Immcantation / nf-core/airrflow, and metagenomics (QIIME2 / Kraken2 / MetaPhlAn): none have a Claude-installable wrapper as of today's WebSearch — all three remain in the Deferred queue with the date bumped to 2026-06-02. One new entry, well under the 5-entry soft cap; no user-feedback issues in the open queue this run.

### Added
- **Adaptyv (Claude Skill)** (Categories: Immunology and Microbiology, Drug Repurposing and Discovery, Integrative Structural and Computational Biology) — K-Dense skill wrapping the Adaptyv cloud-lab API for closed-loop protein and antibody design. In-silico pre-screening with NetSolP / SoluProt (solubility), SolubleMPNN (expression-aware redesign), ESM (sequence-likelihood scoring), ipTM (AlphaFold-Multimer interface stability), and pSAE (aggregation risk); wet-lab assay submission for binding (biolayer interferometry K_D / k_on / k_off), expression in four cell systems, thermostability (DSF / CD T_m), and enzyme activity. Supports batch submission and webhook callbacks; turnaround ~21 days; the skill writes to a wet lab so review submissions carefully. Published via the `K-Dense-AI/claude-scientific-skills` plugin marketplace ([source](https://github.com/K-Dense-AI/scientific-agent-skills), [`scientific-skills/adaptyv/reference/examples.md`](https://github.com/K-Dense-AI/claude-scientific-skills/blob/main/scientific-skills/adaptyv/reference/examples.md), [Adaptyv Bio](https://www.adaptyvbio.com/), [Playbooks: adaptyv skill](https://playbooks.com/skills/k-dense-ai/claude-scientific-skills/adaptyv)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with the Adaptyv addition (oldest of the prior five — `cellxgene-census` — rolled off; `deepchem`, `pytdc`, `npi-registry`, `openneuro` carried forward). Deferred queue: removed `Adaptyv (K-Dense Skill)` (surfaced this run); bumped the `IEDB MCP wrapper` and `BCR/TCR repertoire MCP` re-check dates to 2026-06-02 and expanded the latter to call out Immcantation 4.7.0-2026.01.21 / nf-core/airrflow / VDJdb / McPAS-TCR specifically; added a new `Metagenomics / microbiome MCP` deferred line (no Claude-installable wrapper for QIIME2 / Kraken2 / MetaPhlAn on the 2026-06-02 sweep).

### Verified (no changes)
- Existing Immunology and Microbiology entries (`glycoengineering` last_verified 2026-05-26, plus all `All`-tagged cross-cutting tools — `pubmed`, `uniprot`, `alphafold`, `pdb`, `gget`, `biomcp`, `anndata`, `scanpy`, `scvi-tools`, `scikit-bio`, `flowio`, `10x-genomics-cloud`, `pydeseq2`, `single-cell-rna-qc`, `nextflow-development`, `instrument-data-to-allotrope`, `cellxgene-census`) all within the 30-day verification window — no scheduled re-verification needed this run.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no diff vs. 2026-06-01; `biorxiv` / `clinical-trials` plugins still DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). Deferred queue (Cortellis, Medidata, Consensus, Augmented-Nature ChEMBL, AACT, OpenFDA / Azure FHIR, NeuroClaw, MCP_Vina, DiffDock / cobrapy / TorchDrug / PyOpenMS / matchms, IEDB / Immcantation / metagenomics) carries forward.

### User requests
- `## User requests (open)` was empty entering this run — nothing to action; section remains `_None._`.

## 2026-06-01

Directed pass on **Chemistry** (Monday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-05-31 — the DOA `biorxiv@life-sciences` / `clinical-trials@life-sciences` plugins (upstream issue #42, `mcp.deepsense.ai` NXDOMAIN) still un-restored; no other new plugins this week. The directed pass surfaced **DeepChem** from the standing Deferred queue — the K-Dense skill wrapper around the canonical molecular-machine-learning framework (`deepchem/deepchem`), providing GCN / GAT / MPNN / AttentiveFP graph neural nets, molecular featurization, and the MoleculeNet benchmark suite (Tox21, ClinTox, SIDER, BBBP, QM7/8/9, ESOL, FreeSolv, Lipophilicity). DeepChem complements the existing `rdkit-skill`, `medchem`, `datamol`, `molfeat`, and `pytdc` Chemistry entries by adding the model-training and MoleculeNet-benchmark layer that none of those cover (RDKit / MedChem are featurizers and filters; PyTDC is benchmark splits and oracles). The Chemistry pass also re-checked retrosynthesis and docking MCPs: **MCP_Vina** (`shogo-d-nakamura/MCP_Vina`) is a viable AutoDock Vina MCP server but currently supports only AKT1 as a target — added to Deferred rather than catalogued. AiZynthFinder / ASKCOS / IBM RXN still lack any Claude-installable wrapper as of today's WebSearch. One new entry, well under the 5-entry soft cap; no user-feedback issues in the open queue this run.

### Added
- **DeepChem (Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery) — K-Dense skill driving DeepChem for molecular machine learning. Provides graph neural networks (GCN, GAT, MPNN, AttentiveFP), molecular featurization (graphs, Morgan / circular fingerprints, 2D/3D descriptors), pre-trained molecular foundation models, and the MoleculeNet benchmark suite (50+ datasets across quantum-chemistry, physical-chemistry, biophysics, and physiology / toxicity). TensorFlow and PyTorch backends; integrates with RDKit ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/deepchem/SKILL.md), [DeepChem](https://deepchem.io/), [`deepchem/deepchem`](https://github.com/deepchem/deepchem), [MoleculeNet](https://moleculenet.org/), [Wu et al. *Chem. Sci.* 2018](https://pubs.rsc.org/en/content/articlelanding/2018/sc/c7sc02664a)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with the DeepChem addition (oldest of the prior five — `scvelo` — rolled off; `pytdc`, `npi-registry`, `openneuro`, `cellxgene-census` carried forward). Deferred queue updated: removed `DeepChem (K-Dense Skill)` (surfaced this run); annotated `TorchDrug / DiffDock / PyOpenMS / matchms / cobrapy` line to note the post-DeepChem residual; added `MCP_Vina` (AutoDock Vina MCP server, single-target AKT1) as a deferred Chemistry candidate.

### Verified (no changes)
- Existing Chemistry entries (`rdkit-skill` last_verified 2026-05-20, `rdkit-mcp` 2026-05-20, `chembl` 2026-05-30, `pubchem` 2026-05-20, `medchem` 2026-05-25, `datamol` 2026-05-25, `molfeat` 2026-05-25, `molecule-mcp` 2026-05-20, `drugbank` 2026-05-20, `pytdc` 2026-05-31, `instrument-data-to-allotrope` 2026-05-19) all within the 30-day verification window — no scheduled re-verification needed this run.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no diff vs. 2026-05-31; `biorxiv` / `clinical-trials` plugins still DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). Deferred queue (Cortellis, Medidata, Consensus, Augmented-Nature ChEMBL, AACT, OpenFDA / Azure FHIR / TorchDrug / DiffDock / PyOpenMS / matchms / cobrapy / MCP_Vina) carries forward.

### User requests
- `## User requests (open)` was empty entering this run — nothing to action; section remains `_None._`.

## 2026-05-31

Directed pass on **Drug Repurposing and Discovery** (Sunday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-05-30 — the DOA `biorxiv@life-sciences` / `clinical-trials@life-sciences` plugins (upstream issue #42, `mcp.deepsense.ai` NXDOMAIN) still un-restored; no other new plugins this week. The directed pass surfaced **PyTDC** from the standing Deferred queue — the K-Dense skill wrapper around Therapeutics Data Commons (Harvard `mims-harvard/TDC`), the canonical benchmark suite for ADMET, drug-target / drug-drug interactions, drug response, molecular generation, and retrosynthesis. PyTDC complements the existing `chembl`, `drugbank`, `open-targets`, `pubchem`, `medchem`, `datamol`, `molfeat`, and `rdkit-skill` Drug Repurposing entries by providing the labelled benchmark splits and generation oracles those upstream tools then featurize / model. One new entry, well under the 5-entry soft cap; no user-feedback issues in the open queue this run.

### Added
- **PyTDC (Claude Skill)** (Categories: Drug Repurposing and Discovery, Chemistry, Translational Medicine) — K-Dense skill driving the PyTDC Python client for Therapeutics Data Commons benchmarks: `single_pred` (ADMET, toxicity), `multi_pred` (DTI, DDI, drug response, PPI), and `generation` (de-novo molecules with 17+ oracles incl. QED / SA / DRD2 / GSK3B / JNK3, plus retrosynthesis and reaction yield). Bundled scripts (`load_and_split_data.py`, `benchmark_evaluation.py`, `molecular_generation.py`) plus `datasets.md` / `oracles.md` / `utilities.md` references ([source](https://github.com/K-Dense-AI/scientific-agent-skills), [TDC](https://tdcommons.ai/), [`mims-harvard/TDC`](https://github.com/mims-harvard/TDC), [Huang et al. NeurIPS 2021](https://arxiv.org/abs/2102.09548)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with the PyTDC addition (oldest of the prior five — `arboreto` — rolled off; `cellxgene-census`, `scvelo`, `openneuro`, `npi-registry` carried forward). Deferred queue updated: removed `PyTDC` from the `TorchDrug / PyTDC / DiffDock / PyOpenMS / matchms / cobrapy (K-Dense Skills)` chemistry-stack-siblings line (PyTDC now surfaced).

### Verified (no changes)
- Existing Drug Repurposing and Discovery entries (`open-targets` last_verified 2026-05-20, `drugbank` 2026-05-20, `chembl` 2026-05-30, `pubchem`, `medchem`, `datamol`, `molfeat`, `rdkit-skill`, `rdkit-mcp`, `molecule-mcp`, `adisinsight`, `owkin`, `depmap`) all within the 30-day verification window — no scheduled re-verification needed this run.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no diff vs. 2026-05-30; `biorxiv` / `clinical-trials` plugins still DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). Deferred queue (Cortellis, Medidata, Consensus, Augmented-Nature ChEMBL, AACT, OpenFDA / Azure FHIR / DeepChem / TorchDrug / DiffDock MCPs and skills) carries forward.

### User requests
- `## User requests (open)` was empty entering this run — nothing to action; section remains `_None._`.

## 2026-05-30

Directed pass on **Translational Medicine** (Saturday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-05-29 — the DOA `biorxiv@life-sciences` / `clinical-trials@life-sciences` plugins still un-restored, no other new plugins this week. The directed pass cleared **NPI Registry MCP** from the standing Deferred queue (third Anthropic Healthcare MCP-marketplace entry alongside `cms-coverage` and `icd-10-codes`, plus the existing `pubmed` connector — completes the four Healthcare-marketplace MCPs published with the Jan 2026 Claude for Healthcare launch). Two user-feedback issues processed: #17 with a structured `worked fine` trailer for `chembl`, and #15 a no-trailer migration smoke-test against the same tool. One new entry, well under the 5-entry soft cap; both user requests closed this run.

### Added
- **NPI Registry MCP (Anthropic Healthcare)** (Categories: Translational Medicine) — Anthropic-published MCP server over the CMS NPPES NPI Registry API v2.1 with `npi_validate` / `npi_lookup` / `npi_search` tools for US healthcare-provider credential verification, network construction, and clinical-trial-investigator validation. Pairs with the existing `cms-coverage`, `icd-10-codes`, and `prior-auth-review` entries for end-to-end prior-auth review workflows ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-npi-registry-connector-in-claude), [`anthropics/healthcare`](https://github.com/anthropics/healthcare), [CMS NPPES](https://npiregistry.cms.hhs.gov/)).

### Updated
- **`chembl`** — added a dated field-report note in Notes (`/plugin marketplace add anthropics/life-sciences` + `/plugin install chembl@life-sciences` reported working without modification per user feedback issue #17); `last_verified` bumped 2026-05-24 → 2026-05-30.
- **`catalog/curator-state.md`** — Recently surfaced refreshed with the NPI Registry addition (oldest of the prior five — `molecular-dynamics` — rolled off). Removed `NPI Registry MCP (Anthropic Healthcare)` from the Deferred queue (surfaced this run); added `easysolutions906 Healthcare MCP` (`@easysolutions906/mcp-healthcare` — 10-tool ICD-10 / NPI / NDC / DEA community bundle) to Deferred as a single-install alternative to the four discrete Anthropic Healthcare MCPs.

### Verified (no changes)
- Existing Translational Medicine entries (`fhir-developer`, `prior-auth-review`, `fhir-wso2`, `cms-coverage`, `icd-10-codes`, `clinical-trial-protocol`, `clinicaltrials-gov-mcp`) all within the 30-day verification window (oldest 2026-05-23) — no scheduled re-verification needed this run.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no diff vs. 2026-05-29; `biorxiv` / `clinical-trials` plugins still DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). Deferred queue (Cortellis, Medidata, Consensus, Augmented-Nature ChEMBL, AACT, OpenFDA / Azure FHIR MCPs) carries forward.

### User requests
- **#15** — `[Tool feedback] migration smoke test — chembl` with no `tool-feedback` trailer; closed this run with a note that the title-derived intent is a post-migration form-plumbing smoke test, no content action needed beyond the chembl refresh already driven by #17.
- **#17** — structured trailer `feedback-on=chembl | sentiment=worked fine`; closed this run by adding a field-report Notes line on the chembl page and refreshing `last_verified`.

## 2026-05-29

Directed pass on **Neuroscience** (Friday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-05-28 — no new neuro plugins shipped upstream this week; the `biorxiv@life-sciences` / `clinical-trials@life-sciences` DOA situation continues. Existing Neuroscience entries (`allenbrain`, `aind-data`, `neurosift`, `neurokit2`, `neuropixels-analysis`, `bids`) all within the 30-day verification window — no re-verification needed. Directed search turned up two strong candidates: **OpenNeuro MCP** (QuentinCody) — a hosted Cloudflare Workers SSE server wrapping the OpenNeuro GraphQL API, with a clean copy-pasteable install path documented upstream — and **NeuroClaw** (CUHK-AIM Group), an 81-skill neuroimaging library with FreeSurfer / FSL / fMRIPrep / MNE / nilearn / DIPY integrations. OpenNeuro MCP was added; NeuroClaw was deferred because the upstream README positions skills/ as Claude-Code-installable but does not publish a copy-pasteable `~/.claude/skills/` snippet and the license terms could not be confirmed under today's WebFetch reliability. One new entry, well under the 5-entry soft cap.

### Added
- **OpenNeuro MCP** (Categories: Neuroscience) — Community MCP server wrapping the OpenNeuro GraphQL API for MRI / MEG / EEG / iEEG / ECoG dataset, snapshot, and file-listing queries; hosted Cloudflare Workers SSE endpoint, MIT + Academic Citation Requirement license. Complements the Neurosift Tools MCP (DANDI + NWB) by covering OpenNeuro's archive ([source](https://github.com/QuentinCody/open-neuro-mcp-server), [OpenNeuro](https://openneuro.org/)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with this run's OpenNeuro MCP addition (oldest of the prior five rolled off). Deferred queue gained `NeuroClaw` (install path gap + license unconfirmed) and a watch item on the K-Dense v2.43.0 `scientific-skills/` → `skills/` path migration that may affect future K-Dense skill page edits.
- **Feedback-footer URL backfill** — five tool pages added on / since 2026-05-27 (`openneuro`, `cellxgene-census`, `molecular-dynamics`, `scvelo`, `arboreto`) still pointed their `Installed this tool?` feedback links at the pre-migration `goodb/sci-ai-enabler` org / `goodb.github.io` pages host. The org-rename commit (`4d703fe`) ran on a branch that forked before today's earlier catalog commit (`c102ee7`), so these five files were not rewritten by the migration. Rewrote both occurrences in each footer to `scripps-ai-enablement/sci-ai-enabler` and `scripps-ai-enablement.github.io` to restore the working feedback path. No content changes outside the footer URLs ([migration commit](https://github.com/scripps-ai-enablement/sci-ai-enabler/commit/4d703fe)).

### Verified (no changes)
- All Neuroscience catalog entries' `last_verified` is within the 30-day window (oldest 2026-05-20) — no scheduled re-verification needed this run.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no new neuro plugins; `biorxiv` / `clinical-trials` plugins still DOA per upstream issue #42 (`mcp.deepsense.ai` NXDOMAIN). Deferred queue (Cortellis, Medidata, Consensus, NPI Registry, Augmented-Nature ChEMBL, AACT, OpenFDA / Azure FHIR MCPs) carries forward.

### User requests
- **#11** — `[Tool feedback]` with no `tool-feedback` trailer; still unactionable from the curator runner (no `gh` CLI / GitHub-API auth in this environment). Closed this run with that note; inbound responder will re-surface if the issue is updated.

## 2026-05-28

Directed pass on **Molecular and Cellular Biology** (Thursday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-05-27 sweep among plugins our catalog already covers; an `e96556b` upstream commit and issue #42 indicate that **biorxiv@life-sciences** and **clinical-trials@life-sciences** plugins are now published in the marketplace but currently DOA (the `mcp.deepsense.ai` host returns NXDOMAIN) — held off from cataloguing pending Anthropic / DeepSense restoring the endpoint, and added to the Deferred queue. The directed pass surfaced three K-Dense single-cell skills from the standing Deferred queue — **Cellxgene Census**, **scVelo**, and **Arboreto** — which collectively round out the catalog's single-cell trajectory + GRN coverage that pairs with the existing `scanpy`, `anndata`, `scvi-tools`, and `pydeseq2` entries. Three new entries, well under the 5-entry soft cap.

### Added
- **Cellxgene Census (Claude Skill)** (Categories: Molecular and Cellular Biology, Immunology and Microbiology, Translational Medicine) — K-Dense skill for querying the CZ CELLxGENE Discover census (50M+ cells, 1,000+ datasets) via TileDB-SOMA, with AnnData / Scanpy integration for reference-atlas construction and meta-analyses ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/cellxgene-census/SKILL.md), [CELLxGENE Census docs](https://chanzuckerberg.github.io/cellxgene-census/)).
- **scVelo (Claude Skill)** (Categories: Molecular and Cellular Biology, Neuroscience) — K-Dense skill driving scVelo for RNA-velocity analysis: steady-state / stochastic / dynamical models, latent-time inference, driver-gene identification, and velocity-embedding projection on UMAP / t-SNE ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/scvelo/SKILL.md), [scVelo docs](https://scvelo.readthedocs.io/)).
- **Arboreto (Claude Skill)** (Categories: Molecular and Cellular Biology, Drug Repurposing and Discovery) — K-Dense skill for gene-regulatory-network inference with GRNBoost2 / GENIE3, scaled with Dask; standard upstream step for pySCENIC pipelines and regulator prioritisation ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/arboreto/SKILL.md), [Arboreto docs](https://arboreto.readthedocs.io/)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with this run's three additions; Deferred queue trimmed (removed `Cellxgene Census`, `scVelo`, `Arboreto`) and extended with the upstream-broken `biorxiv@life-sciences` and `clinical-trials@life-sciences` plugins.

### Flagged
- **biorxiv@life-sciences** and **clinical-trials@life-sciences** plugins — published in `anthropics/life-sciences` marketplace but the backing `mcp.deepsense.ai` MCP host returns NXDOMAIN as of upstream commit `e96556b` (2026-05-12). Not yet added to the catalog because there is no working install path to document. Watch upstream and revisit on next sweep.

### Verified (no changes)
- All catalog entries' `last_verified` is within the 30-day window (oldest 2026-05-19); no scheduled re-verification needed this run.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: catalogued plugins (PubMed, BioRender, Synapse, Wiley Scholar Gateway, 10x Genomics, AdisInsight, single-cell-rna-qc, instrument-data-to-allotrope, nextflow-development, scvi-tools, scientific-problem-selection) still present; other deferred-queue plugins (Cortellis, Medidata, Consensus, NPI Registry) carry forward.

### User requests
- **#11** — `[Tool feedback]` with no `tool-feedback` trailer; the curator runner cannot fetch issue bodies via the GitHub REST API or `gh` CLI in this environment (auth-gated), so the request stays in `## User requests (open)` for the next run that has issue-body fetch capability. Closed-this-run note records the access constraint.

## 2026-05-27

Directed pass on **Integrative Structural and Computational Biology** (Wednesday focus). Manifest sweep of `anthropics/life-sciences` re-confirmed no diff vs. 2026-05-26 — every plugin currently published there remains catalogued. The K-Dense `claude-scientific-skills` catalog was scanned for structural-biology skills not yet in the catalog; **Molecular Dynamics** (OpenMM + MDAnalysis) is the strongest fit and complements the existing `alphafold` / `pdb` / `molecule-mcp` entries by covering the simulation and trajectory-analysis layer that none of those cover. Focused searches for cryo-EM (RELION / cryoSPARC) and protein-design model (RFdiffusion / ProteinMPNN) Claude wrappers turned up nothing installable today — deferred for the next Structural-focus pass. One new entry this run, well under the 5-entry soft cap.

### Added
- **Molecular Dynamics (Claude Skill)** (Categories: Integrative Structural and Computational Biology, Drug Repurposing and Discovery) — K-Dense skill that sets up, runs, and analyzes molecular-dynamics simulations end-to-end via OpenMM and MDAnalysis (system prep, force-field assignment, NVT/NPT equilibration, production MD, RMSD / RMSF / contact-map / free-energy-surface analysis) ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/molecular-dynamics/SKILL.md), [K-Dense scientific-skills catalog](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/docs/scientific-skills.md)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with this run's Molecular Dynamics addition; Deferred queue gained `MDAnalysis (K-Dense Skill)` (pending confirmation of whether it ships as a distinct `SKILL.md`), `Cryo-EM MCP / Skill` (no Claude-installable wrapper located this pass), and `RFdiffusion / ProteinMPNN Claude Skill` (no wrapper located this pass).

### Verified (no changes)
- Existing Integrative Structural and Computational Biology entries (`alphafold`, `pdb`, `molecule-mcp`, `uniprot`) spot-checked against upstream — install paths, supplier links, and pricing claims still valid; no field drift.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no diff vs. 2026-05-26 sweep; deferred queue (Cortellis, Medidata, Consensus, NPI Registry, Augmented-Nature ChEMBL community alternative, AACT, OpenFDA / Azure FHIR MCPs) carries forward.

### User requests
- **#11** — `[Tool feedback]` with no `tool-feedback` trailer emitted by the responder; issue body not fetchable from the curator runner this run, left open in `## User requests (open)` for next-run triage.

## 2026-05-26

Directed pass on **Immunology and Microbiology** (Tuesday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-05-25 — every plugin currently published there is already catalogued. The K-Dense `claude-scientific-skills` directory was scanned for immunology-relevant skills not yet in the catalog; **Glycoengineering** is the strongest fit (therapeutic-antibody and vaccine design via N/O-glycosylation prediction and external glyco-tool orchestration) and is the single new entry this run. A focused look for IEDB and BCR/TCR repertoire MCP servers turned up no Claude-installable wrappers — deferred for the next Immunology pass. Well under the 5-entry soft cap, by design: the directed pass is meant to surface high-fit category entries, not pad the catalog.

### Added
- **Glycoengineering (Claude Skill)** (Categories: Immunology and Microbiology, Drug Repurposing and Discovery) — K-Dense skill that scans protein sequences for N-glycosylation sequons (N-X-S/T), predicts O-glycosylation hotspots, and orchestrates NetOGlyc / GlycoShield / GlycoWorkbench for therapeutic-antibody Fc engineering, vaccine-immunogen design, and biologics developability ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/glycoengineering/SKILL.md), [K-Dense scientific-skills catalog](https://github.com/K-Dense-AI/claude-scientific-skills/blob/main/docs/scientific-skills.md)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with this run's Glycoengineering addition; Deferred queue gained `IEDB MCP wrapper`, `BCR/TCR repertoire MCP`, and `Adaptyv (K-Dense Skill)` as Immunology-focus candidates carried forward.

### Verified (no changes)
- Existing Immunology and Microbiology entries (`scikit-bio`, `flowio`, `uniprot`, `gget`, `pydeseq2`, `nextflow-development`) spot-checked against upstream — install paths, supplier links, and pricing claims still valid; no field drift.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no diff vs. 2026-05-25 sweep; deferred queue (Cortellis, Medidata, Consensus, NPI Registry, Augmented-Nature ChEMBL community alternative) carries forward.

## 2026-05-25

Directed pass on **Chemistry** (Monday focus). Manifest sweep of `anthropics/life-sciences` shows no diff vs. 2026-05-24 — the marketplace's chemistry surface (`chembl`, `tooluniverse`, plus the broader `bio-research` bundle) is fully catalogued. The directed pass picked up three sibling cheminformatics skills from the K-Dense `claude-scientific-skills` marketplace that round out the existing `rdkit-skill` entry into the full RDKit-derived lead-optimisation stack documented in K-Dense's example workflows. Three new entries — at the soft cap minus two — with DeepChem and the remaining chemistry siblings (TorchDrug, PyTDC, DiffDock, PyOpenMS, matchms, cobrapy) carried forward on the deferred queue.

### Added
- **Datamol (Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery) — K-Dense skill wrapping the Datamol RDKit-built library for molecular standardization, tautomer / stereoisomer enumeration, featurization, and parallel processing on large compound libraries ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/datamol/SKILL.md), [Datamol](https://datamol.io/)).
- **Molfeat (Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery) — K-Dense skill wrapping Molfeat, a unified API over 100+ molecular featurizers spanning classical fingerprints (ECFP, MACCS), 2D/3D descriptors, molecular graphs, and pretrained chemical foundation-model embeddings (ChemBERTa, MolBERT, Uni-Mol) ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/molfeat/SKILL.md), [Molfeat docs](https://molfeat.datamol.io/)).
- **MedChem (Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery) — K-Dense skill wrapping MedChem — drug-likeness filters (Lipinski, Veber, Egan, Muegge), PAINS / BRENK structural alerts, complexity metrics, and synthetic-accessibility scoring for hit-list triage ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/medchem/SKILL.md), [MedChem docs](https://medchem.datamol.io/)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with this run's three Chemistry additions; Deferred queue gained DeepChem, the remaining K-Dense chemistry-stack siblings (TorchDrug, PyTDC, DiffDock, PyOpenMS, matchms, cobrapy) as a bundle line, and a Retrosynthesis MCP entry (no Claude-installable wrapper for AiZynthFinder / ASKCOS / IBM RXN located on this pass).

### Verified (no changes)
- Existing Chemistry pages (`rdkit-skill`, `rdkit-mcp`, `molecule-mcp`, `chembl`, `pubchem`) spot-checked against upstream — install paths, supplier links, and pricing claims still valid; no field drift.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no diff vs. 2026-05-24 sweep; deferred queue (Cortellis, Medidata, Consensus, NPI Registry, Augmented-Nature ChEMBL community alternative) carries forward.

## 2026-05-24

Directed pass on **Drug Repurposing and Discovery** (Sunday focus). The `anthropics/life-sciences` marketplace gained three first-party drug-discovery surfaces at J.P. Morgan 2026 — **ChEMBL**, **ToolUniverse**, and **Owkin Pathology Explorer** — none of which were yet catalogued; all three were already on the deferred queue. Three new entries this run, at the 5-entry soft cap minus two; Cortellis / Medidata / Consensus standalone plugin entries kept on the deferred queue pending direct install-path confirmation.

### Added
- **ChEMBL Connector** (Categories: Chemistry, Drug Repurposing and Discovery) — Anthropic-packaged plugin and Claude.ai connector over EMBL-EBI's ChEMBL bioactive-compound database; six tool calls covering compound search, target search, bioactivity, and mechanism-of-action ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-chembl-connector-in-claude), [marketplace](https://github.com/anthropics/life-sciences)).
- **ToolUniverse** (Categories: All) — Zitnik Lab / MIT Lincoln Laboratory MCP server bundling 600+ vetted scientific tools across literature, chemistry, omics, clinical trials, and knowledge graphs; installable directly via `uvx tooluniverse` or as a `life-sciences` marketplace plugin ([Claude Code setup guide](https://zitniklab.hms.harvard.edu/bioagent/guide/building_ai_scientists/claude_code.html), [PyPI](https://pypi.org/project/tooluniverse/), [arXiv:2509.23426](https://arxiv.org/abs/2509.23426)).
- **Owkin Pathology Explorer Connector** (Categories: Drug Repurposing and Discovery, Translational Medicine) — remote MCP connector exposing Owkin's H&E whole-slide image analysis agent for cell-type detection, tumour-microenvironment profiling, and cohort-level survival analysis on TCGA and partner cohorts ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-owkin-connector-in-claude), [Owkin press release](https://www.owkin.com/newsfeed/owkins-specialized-biological-ai-agent-pathology-explorer-launches-with-anthropics-claude-for-healthcare-and-life-sciences)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with this run's three Drug Repurposing additions; Deferred queue gained `Augmented-Nature ChEMBL-MCP-Server` (community alternative now superseded for marketplace users by the first-party ChEMBL connector) and broke the previously-bundled "Standalone `anthropics/life-sciences` plugins" line into per-plugin Deferred entries (Cortellis, Medidata, Consensus).

### Verified (no changes)
- Existing Drug Repurposing entries (`open-targets`, `drugbank`, `pubchem`, `pdb`, `alphafold`, `depmap`, `bio-research`) spot-checked against upstream — install paths and pricing claims still valid; no field drift.
- Manifest sweep of `anthropics/life-sciences` re-confirmed: the four previously-deferred plugins beyond ChEMBL / ToolUniverse / Owkin (Cortellis, Medidata, Consensus, plus `bio-research`-already-catalogued bundles) carry forward to the deferred queue.

## 2026-05-23

Directed pass on **Translational Medicine** (Saturday focus). Manifest sweep of `anthropics/healthcare/.claude-plugin/marketplace.json` (via web search of the release notes and README, since direct fetch is unavailable from the runner) surfaced three new Anthropic-published healthcare components beyond the two already catalogued (`fhir-developer`, `prior-auth-review`). A focused web search for ClinicalTrials.gov MCP servers identified `cyanheads/clinicaltrialsgov-mcp-server` as the highest-quality standalone option, with a hosted public instance and Apache-2.0 license. Four new entries this run — at the 5-entry soft cap minus one — with NPI Registry deferred to next run.

### Added
- **clinical-trial-protocol (Anthropic Healthcare Plugin)** (Categories: Translational Medicine, Drug Repurposing and Discovery) — Anthropic skill that drafts FDA/NIH-compliant Phase 2/3 clinical-trial protocols via a four-step waypoint workflow (regulatory classification → ClinicalTrials.gov landscape → sample-size calculation → protocol drafting) ([source](https://github.com/anthropics/healthcare), [tutorial](https://claude.com/resources/tutorials/how-to-use-the-clinical-trial-protocol-draft-generation-sample-skill-with-claude)).
- **CMS Coverage MCP (Anthropic Healthcare)** (Categories: Translational Medicine) — Anthropic-published MCP over the CMS Local and National Coverage Determinations for Medicare prior-auth, appeals, and policy lookup ([source](https://github.com/anthropics/healthcare), [announcement](https://www.anthropic.com/news/healthcare-life-sciences)).
- **ICD-10 Codes MCP (Anthropic Healthcare)** (Categories: Translational Medicine) — Anthropic-published MCP for ICD-10-CM and ICD-10-PCS diagnosis and procedure code lookup, sourced from CMS and CDC ([source](https://github.com/anthropics/healthcare)).
- **ClinicalTrials.gov MCP Server (cyanheads)** (Categories: Translational Medicine, Drug Repurposing and Discovery) — Apache-2.0 MCP over the ClinicalTrials.gov v2 API with full study retrieval, outcomes extraction, and patient-to-trial matching; hosted public instance at `clinicaltrials.caseyjhand.com/mcp` ([source](https://github.com/cyanheads/clinicaltrialsgov-mcp-server), [npm](https://www.npmjs.com/package/clinicaltrialsgov-mcp-server)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced refreshed with this run's four Translational Medicine additions; Deferred queue gained `NPI Registry MCP` (the fourth healthcare-marketplace MCP, held back to respect the entry cap) and `AACT Clinical Trials MCP` (SQL-over-PostgreSQL alternative to the ClinicalTrials.gov v2 API).

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences/marketplace.json` re-confirmed: no diff vs. 2026-05-22; existing Owkin / ChEMBL / Cortellis / ToolUniverse / Consensus / Medidata deferred items carry forward.
- Existing Translational Medicine pages (`fhir-developer`, `prior-auth-review`, `fhir-wso2`) spot-checked against upstream — install paths still valid; no field drift.

## 2026-05-22

Directed pass on **Neuroscience** (Friday focus). Three K-Dense scientific skills added — each is a distinct `SKILL.md` directory installable via the `K-Dense-AI/claude-scientific-skills` plugin marketplace or by manual clone of `K-Dense-AI/scientific-agent-skills`. Manifest sweep of `anthropics/life-sciences` shows no new plugin entries since 2026-05-21.

### Added
- **BIDS (Claude Skill)** (Categories: Neuroscience) — K-Dense skill for the Brain Imaging Data Structure standard: dataset creation, DICOM-to-BIDS conversion (HeuDiConv / dcm2bids / BIDScoin), PyBIDS `BIDSLayout` queries, validation against OpenNeuro / DANDI submission requirements, and BIDS-Apps integration ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/bids/SKILL.md)).
- **Neuropixels-Analysis (Claude Skill)** (Categories: Neuroscience) — K-Dense skill for end-to-end Neuropixels pipelines: SpikeGLX / Open Ephys / NWB loading, preprocessing, motion correction, and Kilosort4 / SpykingCircus2 / Mountainsort5 spike sorting via SpikeInterface ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/neuropixels-analysis/SKILL.md)).
- **NeuroKit2 (Claude Skill)** (Categories: Neuroscience, Translational Medicine) — K-Dense skill wrapping NeuroKit2 for ECG / EEG / EDA / RSP / PPG / EMG / EOG analysis, HRV, and multi-modal psychophysiology ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/neurokit2/SKILL.md)).

### Updated
- **`catalog/curator-state.md`** — Recently surfaced list refreshed with this run's three Neuroscience additions.

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences` re-confirmed: no new plugin entries since the 2026-05-21 sweep; deferred queue (Owkin, ChEMBL, Cortellis, ToolUniverse, Consensus, Medidata standalone plugins) retained for next run.

## 2026-05-21

Directed pass on **Molecular and Cellular Biology** (Thursday focus). Four K-Dense scientific skills added — each is a distinct `SKILL.md` directory installable via the `K-Dense-AI/claude-scientific-skills` plugin marketplace or by manual clone of `K-Dense-AI/scientific-agent-skills`. Also created `catalog/curator-state.md` per the new schema.

### Added
- **AnnData (Claude Skill)** (Categories: Immunology and Microbiology, Molecular and Cellular Biology, Neuroscience) — K-Dense skill teaching the AnnData annotated-data-matrix object model that underpins Scanpy and scvi-tools ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/anndata/SKILL.md)).
- **PyDESeq2 (Claude Skill)** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Molecular and Cellular Biology, Translational Medicine) — K-Dense skill for bulk RNA-seq differential expression via the Python reimplementation of DESeq2 ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/pydeseq2/SKILL.md)).
- **gget (Claude Skill)** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology) — K-Dense skill wrapping the gget unified query API over Ensembl, UniProt, NCBI, PDB, COSMIC, and 15+ other genomics databases ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/gget/SKILL.md)).
- **DepMap (Claude Skill)** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — K-Dense skill for Cancer Dependency Map CRISPR Chronos gene-effect, PRISM drug sensitivity, and OMICS data across hundreds of cancer cell lines ([source](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/depmap/SKILL.md)).

### Updated
- **`catalog/curator-state.md`** — created per the schema in `AGENT.md`; carries forward `allenbrain-mcp` flag and the prior Deferred queue, with Cellxgene Census / scVelo / Arboreto added as next-run Molecular & Cellular Biology candidates.

### Verified (no changes)
- Manifest sweep of `anthropics/life-sciences/marketplace.json` re-confirmed: existing entries (`pubmed`, `biorender`, `synapse`, `wiley-scholar-gateway`, `10x-genomics`, `single-cell-rna-qc`, `instrument-data-to-allotrope`, `nextflow-development`, `scvi-tools`, `scientific-problem-selection`, `open-targets`, `adisinsight`) all still present — no diff against the previously catalogued set.

## 2026-05-20 (topic-focused seeding pass)

A one-time directed sweep across all seven categories, seeded by per-category seed queries newly added to `AGENT.md`. Twenty new tool pages, organized by the day-of-week the rotating focus is now scheduled to revisit each category.

### Added — Chemistry (Mondays)
- **RDKit Cheminformatics Skill** (Categories: Chemistry) — K-Dense Claude skill providing RDKit recipes for SMILES parsing, descriptors, fingerprints, substructure search, reactions, and 2D/3D molecular generation ([source](https://github.com/K-Dense-AI/scientific-agent-skills)).
- **PubChem MCP Server** (Categories: Chemistry, Drug Repurposing and Discovery) — community MCP wrapping the PubChem compound database; complements bioactivity-focused ChEMBL ([source](https://github.com/JackKuo666/PubChem-MCP-Server)).
- **RDKit MCP Server (TandemAI)** (Categories: Chemistry, Drug Repurposing and Discovery) — full RDKit 2025.3.1 surface exposed as discrete MCP tools, for environments without local Python execution ([source](https://github.com/tandemai-inc/rdkit-mcp-server)).

### Added — Immunology and Microbiology (Tuesdays)
- **BioContextAI Knowledgebase MCP** (Categories: All) — read-only MCP unifying 14+ biomedical databases (Antibody Registry, UniProt, STRING, AlphaFold, KEGG, Open Targets, …) ([source](https://github.com/biocontext-ai/knowledgebase-mcp)).
- **scikit-bio (Claude Skill)** (Categories: Immunology and Microbiology, Molecular and Cellular Biology) — K-Dense skill for microbiome ecology, alpha/beta diversity, ordination, PERMANOVA, phylogenetics ([source](https://github.com/K-Dense-AI/scientific-agent-skills)).
- **FlowIO (Claude Skill)** (Categories: Immunology and Microbiology) — K-Dense skill parsing Flow Cytometry Standard (FCS v2–3.1) files for immunophenotyping pipelines ([source](https://github.com/K-Dense-AI/scientific-agent-skills)).

### Added — Integrative Structural and Computational Biology (Wednesdays)
- **PDB MCP Server** (Categories: Integrative Structural and Computational Biology, Drug Repurposing and Discovery) — Augmented Nature MCP wrapping the RCSB Protein Data Bank with UniProt cross-referencing and structure-quality lookups ([source](https://github.com/Augmented-Nature/PDB-MCP-Server)).
- **AlphaFold MCP Server** (Categories: Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Drug Repurposing and Discovery) — Augmented Nature MCP over the EBI AlphaFold Protein Structure Database; ~25 tools including pLDDT analysis and PyMOL/ChimeraX export ([source](https://github.com/Augmented-Nature/AlphaFold-MCP-Server)).
- **Molecule-MCP** (Categories: Chemistry, Integrative Structural and Computational Biology, Drug Repurposing and Discovery) — chatmol three-server bundle driving PyMOL, ChimeraX, and GROMACS MD simulations via natural language ([source](https://github.com/chatmol/molecule-mcp)).

### Added — Molecular and Cellular Biology (Thursdays)
- **Scanpy-MCP** (Categories: All) — MCP wrapping the full Scanpy workflow (IO, QC, normalization, PCA, clustering, DE, plotting) for natural-language single-cell analysis ([source](https://github.com/scmcphub/scanpy-mcp)).
- **UniProt MCP Server** (Categories: Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Drug Repurposing and Discovery) — Augmented Nature MCP with 26 tools over UniProt REST: domains, orthologs, PTMs, pathways, multi-format export ([source](https://github.com/Augmented-Nature/UniProt-MCP-Server)).

### Added — Neuroscience (Fridays)
- **Neurosift Tools MCP** (Categories: Neuroscience) — Flatiron Institute MCP for DANDI / OpenNeuro discovery, NWB introspection, and PyNWB docs semantic search ([source](https://github.com/magland/neurosift-mcps)).
- **allenbrain-mcp** (Categories: Neuroscience) — Alpha community wrapper exposing Allen Brain Atlas RMA queries, cell types, mouse connectivity, ontologies, and image / grid downloads ([source](https://github.com/maflot/allenbrain-mcp)). License unset upstream — flag for review before redistribution.
- **AIND Data MCP** (Categories: Neuroscience) — official Allen Institute for Neural Dynamics MCP for V2 metadata DocDB queries and NWB introspection ([source](https://github.com/AllenNeuralDynamics/aind-data-mcp)).

### Added — Translational Medicine (Saturdays)
- **WSO2 FHIR MCP Server** (Categories: Translational Medicine) — Apache-2.0 MCP for FHIR R4 CRUD against any EHR or sandbox FHIR API with SMART-on-FHIR auth ([source](https://github.com/wso2/fhir-mcp-server)).
- **fhir-developer (Anthropic Healthcare Plugin)** (Categories: Translational Medicine) — Anthropic Claude Code plugin for authoring FHIR R4 resources with LOINC, SNOMED, and RxNorm validation ([source](https://github.com/anthropics/healthcare)).
- **prior-auth-review (Anthropic Healthcare Plugin)** (Categories: Translational Medicine) — Anthropic plugin reviewing prior-authorization request documents against payer rules and surfacing gaps ([source](https://github.com/anthropics/healthcare)).

### Added — Drug Repurposing and Discovery (Sundays)
- **Open Targets Plugin** (Categories: Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine) — Anthropic-packaged plugin wrapping the official Open Targets MCP for target-disease associations and target-prioritisation ([source](https://github.com/anthropics/life-sciences)).
- **AdisInsight Plugin** (Categories: Drug Repurposing and Discovery, Translational Medicine) — Springer Nature commercial plugin for drug-development pipeline, clinical-trial, and deal intelligence ([source](https://github.com/anthropics/life-sciences/blob/main/adisinsight/.claude-plugin/plugin.json)).
- **DrugBank MCP Server** (Categories: Drug Repurposing and Discovery, Chemistry, Translational Medicine) — community MCP over a local DrugBank SQLite (17k+ drugs) with 16 query methods; requires user-supplied DrugBank XML license ([source](https://github.com/openpharma-org/drugbank-mcp-server)).

### Updated
- **`AGENT.md`** — added a Topic-focused rotation section with per-category seed queries and source pointers, plus a directed-pass procedure that runs alongside the existing manifest sweep on every daily run.
- **`.github/workflows/curate.yml`** — derives today's focus category from the UTC weekday and injects `focus_category:` into the run prompt.
- **All existing tool pages** — dropped explicit `nav_order` so the new and existing pages sort alphabetically together in the sidebar.

### Deferred — next-run priority
Catalog candidates from the directed-pass that warrant a follow-up entry but were not added in this seeding pass:

- **Standalone `anthropics/life-sciences` plugins** beyond Open Targets and AdisInsight: `owkin`, `chembl`, `cortellis`, `tooluniverse`, `consensus`, `medidata`. Each is a discrete `/plugin install <name>@life-sciences` target and deserves its own entry distinct from the bundled `bio-research` umbrella.
- **OpenClaw Medical Skills Library** — 869-skill MIT-licensed collection. Per the catalog rule, treat each individual skill (clinical-trial-design, pharmacovigilance, FHIR-developer, adverse-event detection, PyHealth) as a separate entry rather than the umbrella repo.
- **Ensembl MCP servers** (`munch-group/ensembl-mcp`, `effieklimi/ensembl-mcp-server`) — both early-stage; revisit when one of them stabilises.
- **UCSC Genome MCP** (`hlydecker/ucsc-genome-mcp`) — 12 tools over the UCSC Genome Browser API.
- **NCBI Datasets MCP** (`Augmented-Nature/NCBI-Datasets-MCP-Server`) — 31 tools over the NCBI Datasets API.
- **OpenFDA MCP** (`Augmented-Nature/OpenFDA-MCP-Server`, `ythalorossy/openfda`) — standalone OpenFDA wrappers; BioMCP already covers OpenFDA but the distinct install path may warrant a separate entry.
- **Azure FHIR MCP** (`erikhoward/azure-fhir-mcp-server`) — Azure Health Data Services-specific FHIR adapter.

## 2026-05-20

### Surface knowledge-work-plugins bio-research umbrella plugin

Cleared the top Deferred item — `bio-research@anthropics/knowledge-work-plugins` — using the plugin's GitHub README, the parent `knowledge-work-plugins` repo, and the DeepWiki marketplace breakdown as primary sources. It is a pan-life-sciences plugin (literature, single-cell, sequencing, drug discovery, strategy), so tagged `Categories: All` and added to every category index. Also dropped `benchling@life-sciences` from the Deferred list: it was removed from the `anthropics/life-sciences` marketplace because the plugin system does not support tenant-specific URLs (per the [Benchling DeepWiki page](https://deepwiki.com/anthropics/life-sciences/3.6-benchling)); Benchling remains reachable indirectly via the new bio-research umbrella.

### Added
- **bio-research (Claude Code Plugin)** (Categories: All) — Anthropic open-source umbrella plugin in `anthropics/knowledge-work-plugins` bundling 5 analysis skills (Literature Review, Single-Cell Analysis, Sequencing Pipeline, Drug Discovery, Research Strategy) and ~10 MCP connectors (PubMed, BioRender, bioRxiv, ClinicalTrials.gov, ChEMBL, Synapse, Wiley Scholar Gateway, Owkin, Open Targets, Benchling); install via `/plugin marketplace add anthropics/knowledge-work-plugins` then `/plugin install bio-research@knowledge-work-plugins`, then `/start` ([plugin README](https://github.com/anthropics/knowledge-work-plugins/tree/main/bio-research), [DeepWiki](https://deepwiki.com/anthropics/knowledge-work-plugins)).

### Updated
- **[catalog/entries.md]** — New bio-research entry inserted alphabetically between Anthropic PubMed Connector and BioMCP; Recently surfaced refreshed (5-item rolling window: dropped nextflow-development, added bio-research at top); Deferred reshaped to flag individual `knowledge-work-plugins` connectors (bioRxiv, ChEMBL, ClinicalTrials.gov, Owkin, Open Targets) and the K-Dense-AI scientific-skills collection as next-run targets.
- **[catalog/README.md]** — Distinct-tool count 11 → 12; per-category counts incremented by 1 across all seven indices (Chemistry 7 → 8; Structural/Computational and Neuroscience 10 → 11; Immunology, Molecular & Cellular, Drug Discovery, Translational 11 → 12). All-tagged-tool list updated to include bio-research.
- **[All seven category indices]** — One new `bio-research (Claude Code Plugin)` card added per index in the alphabetical slot between Anthropic PubMed Connector and BioMCP.
- **[Deferred list]** — Removed `bio-research@anthropics/knowledge-work-plugins` (surfaced this run); recorded `benchling@life-sciences` as dropped with rationale and DeepWiki citation; added individual bundled connectors and `K-Dense-AI/scientific-agent-skills` as next-run priorities.

### Flagged
- _None._

### Verified (no changes)
- 11 existing entries spot-checked (all carry `Last verified` between 2026-05-19 and 2026-05-20 from recent runs); no field drift on supplier links, availability, or install paths. The bio-research plugin's bundled PubMed/BioRender/Synapse/Wiley connectors corroborate the existing standalone entries for those tools.

## 2026-05-20

### Surface anthropics/life-sciences marketplace entries (batch 4)

Cleared all three remaining `*@life-sciences` candidates from the Deferred list — Synapse, Wiley Scholar Gateway, and scientific-problem-selection — using web search results that cite the `anthropics/life-sciences` marketplace, the Anthropic tutorials, and the DeepWiki marketplace breakdown as primary sources. All three are pan-life-sciences tools and tagged `Categories: All`, so each was added to every category index. Held at three new entries this run (within the soft cap of 5) since each `All`-tagged entry costs 1 entry-block write + 7 card edits = 8 file touches.

### Added
- **Scholar Gateway Connector (Wiley)** (Categories: All) — Wiley remote MCP server / Claude.ai connector providing peer-reviewed scholarly content across 3M+ articles (including 300+ Life Sciences journals covering 900,000+ research articles); hosted at `connector.scholargateway.ai/mcp`, Beta, free Scholar Gateway account required ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-scholar-gateway-connector-in-claude), [DeepWiki](https://deepwiki.com/anthropics/life-sciences/3.5-wiley-scholar-gateway), [Wiley press release](https://newsroom.wiley.com/press-releases/press-release-details/2025/Wiley-Launches-Interoperable-Platform-to-Power-Scientific-Discovery-in-Worlds-Leading-AI-Technologies/default.aspx)).
- **scientific-problem-selection (Claude Skill)** (Categories: All) — Anthropic skill encoding Fischbach & Walsh's *Cell* (2024) framework for project ideation, risk assessment, troubleshooting stuck projects, and strategic scientific planning ([marketplace](https://github.com/anthropics/life-sciences), [Claude for Life Sciences](https://www.anthropic.com/news/claude-for-life-sciences)).
- **Synapse.org Connector** (Categories: All) — Sage Bionetworks remote MCP server / Claude.ai connector at `mcp.synapse.org/mcp` for discovery, project structure, and metadata retrieval across Synapse-hosted biomedical data; OAuth2 default, free Synapse account required, per-project access controls apply ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-synapse-org-connector-in-claude), [marketplace](https://github.com/anthropics/life-sciences), [server source](https://github.com/susheel/synapse-mcp)).

### Updated
- **[catalog/entries.md]** — Three new entry blocks inserted alphabetically; Recently surfaced refreshed (5-item rolling window: dropped instrument-data-to-allotrope, BioRender Connector, 10x Genomics Cloud MCP; added Synapse, scientific-problem-selection, Scholar Gateway at top).
- **[catalog/README.md]** — Distinct-tool count 8 → 11; per-category counts incremented by 3 across all seven indices (Chemistry 4 → 7; Structural/Computational and Neuroscience 7 → 10; Immunology, Molecular & Cellular, Drug Discovery, Translational 8 → 11). All-tagged-tool list updated to include Scholar Gateway, Synapse, and scientific-problem-selection.
- **[All seven category indices]** — Three new cards added per index in their alphabetical slots, freshness timestamps bumped.
- **[Deferred list]** — Removed all three surfaced items; `bio-research@anthropics/knowledge-work-plugins` carries forward; added `benchling@life-sciences` (named in Anthropic launch coverage alongside 10x Genomics) as a new next-run priority.

### Flagged
- _None._

### Verified (no changes)
- 8 existing entries spot-checked (all `Last verified: 2026-05-19` from prior runs); no field drift on supplier links, availability, or install paths.

## 2026-05-19

### Surface anthropics/life-sciences marketplace entries (batch 3)

Cleared one more item from the Deferred list — `scvi-tools@life-sciences` — using the `anthropics/life-sciences` marketplace plus the Anthropic tutorial as primary sources. Held to one new entry this run because the tag list expands to six category-card edits (Chemistry excluded — scvi-tools is single-cell omics, not chemistry).

### Added
- **scvi-tools (Claude Skill)** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine) — Anthropic skill bundling deep-learning workflows for scVI, scANVI, totalVI, MultiVI, PeakVI, DestVI, contrastiveVI, sysVI, and veloVI; covers batch correction, semi-supervised cell-type annotation, multi-modal CITE-seq / multiome integration, spatial deconvolution, perturbation analysis, and RNA velocity ([Anthropic tutorial](https://claude.com/resources/tutorials/how-to-use-the-scvi-tools-bioinformatics-skill-bundle-with-claude), [marketplace](https://github.com/anthropics/life-sciences)).

### Updated
- **[catalog/entries.md]** — Promoted scvi-tools from the Deferred list; refreshed Recently surfaced (5-item rolling window: dropped single-cell-rna-qc, added scvi-tools at top).
- **[catalog/README.md]** — Distinct-tool count 7 → 8; per-category counts incremented for the six tagged categories (Immunology, Molecular & Cellular, Drug Discovery, Translational 7 → 8; Structural/Computational and Neuroscience 6 → 7). Chemistry unchanged at 4.
- **[Deferred list]** — Removed `scvi-tools@life-sciences`; remaining items (synapse, wiley-scholar-gateway, scientific-problem-selection, bio-research umbrella) carry forward.

### Flagged
- _None._

### Verified (no changes)
- 7 existing entries spot-checked (all `Last verified: 2026-05-19` from prior runs today); no field drift on supplier links or install paths.

## 2026-05-19

### Surface anthropics/life-sciences marketplace entries (batch 2)

Cleared two items from the previous run's Deferred list using the `anthropics/life-sciences` marketplace as the manifest-driven source. Stayed under the per-run surfacing cap (2 entries this run vs. soft cap of 5) because each new entry's tag list expands into 5–6 category-card edits.

### Added
- **instrument-data-to-allotrope (Claude Skill)** (Categories: Chemistry, Drug Repurposing and Discovery, Immunology and Microbiology, Molecular and Cellular Biology, Translational Medicine) — Anthropic skill that converts 40+ lab-instrument output formats (PDF, CSV, Excel, TXT) to Allotrope Simple Model JSON / flattened CSV via the `allotropy` library, with PDF-table fallback and ASM validation ([skill listing](https://playbooks.com/skills/anthropics/life-sciences/instrument-data-to-allotrope), [marketplace](https://github.com/anthropics/life-sciences)).
- **nextflow-development (Claude Skill)** (Categories: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine) — Anthropic prototype skill that runs nf-core `rnaseq` 3.22.2, `sarek` 3.7.1, and `atacseq` 2.1.2 on local FASTQ or GEO/SRA inputs ([skill listing](https://agent-skills.md/skills/anthropics/life-sciences/nextflow-development), [marketplace](https://github.com/anthropics/life-sciences)).

### Updated
- **[catalog/entries.md]** — Promoted both skills from the Deferred list; refreshed Recently surfaced to include them.
- **[catalog/README.md]** — Distinct-tool count 5 → 7; per-category counts incremented (Chemistry 3 → 4; Structural/Computational and Neuroscience 5 → 6; Immunology, Molecular & Cellular, Drug Discovery, and Translational 5 → 7).
- **[Deferred list]** — Removed the two surfaced items; added `bio-research@anthropics/knowledge-work-plugins` (umbrella plugin bundling 10 MCP servers + 6 skills) as a new next-run priority after it was named by both search results.

### Flagged
- _None._

### Verified (no changes)
- 5 existing entries spot-checked (all `Last verified: 2026-05-19` from yesterday's run); no field drift on supplier links or install paths.

## 2026-05-19

### Refactor: entries.md is canonical; category files become tag-filtered indices

Multi-category entries were previously duplicated as full blocks into every named category file. That hit the action's 600-second wall on expansion runs (each pan-life-sciences entry cost ~7 file writes plus drift detection) and forced an artificial "primary category" choice for genuinely cross-cutting tools like PubMed.

Refactored to a single source of truth:

- `catalog/entries.md` now holds every entry's full content block, alphabetically.
- Each `catalog/<area>.md` is a card-based index: brief summary per entry tagged with that category, linking back to `entries.md`.
- The `Categories` field is a tag list (comma-separated), with the literal value `All` allowed for tools applicable across every life-science domain. No notion of a "primary" category.
- Drift detection at run-start is no longer needed — single source of truth, no drift possible.
- Updates to a tool's pricing/availability/etc. are one write to `entries.md`. Card edits in indices are only needed when the card's surface text (name, type, supplier, availability, one-line summary) changes.

This refactor was performed locally rather than by the agent because it's a substantial content migration and the agent's per-run timeouts made it unsafe to run there. AGENT.md was rewritten in the same change to match the new storage model.

#### Removed
- Per-category duplicated copies of the 5 cross-cutting entries (Anthropic PubMed Connector, BioMCP, BioRender Connector, 10x Genomics Cloud MCP, single-cell-rna-qc) — superseded by `entries.md` as canonical store.

#### Added
- **catalog/entries.md** — canonical file with all 5 entries; PubMed / BioMCP / BioRender tagged `All`, 10x Genomics Cloud / single-cell-rna-qc tagged with their explicit 6-category subset.
- Card-based index in each category file linking back to canonical entries.

## 2026-05-19

### Surface anthropics/life-sciences marketplace entries (batch 1)

Drew from the `anthropics/life-sciences` marketplace manifest — the highest-yield, pre-validated source for Claude-installable life-science components. Added the three most impactful entries not yet catalogued and stopped at the per-run cap of 3.

#### Added
- **[Chemistry, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine, Drug Repurposing and Discovery] BioRender Connector** — Scientific-illustration MCP / Claude.ai connector launched alongside the Oct 23, 2025 Anthropic × BioRender partnership; relevant across every life-science domain because figure-building is universal ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-biorender-connector-in-claude), [BusinessWire announcement](https://www.businesswire.com/news/home/20251023858531/en/BioRender-and-Anthropic-Partner-To-Bring-Scientific-Illustrations-to-Claude-For-Life-Sciences)).
- **[Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine, Drug Repurposing and Discovery] 10x Genomics Cloud MCP** — Local MCPB extension distributed by 10x Genomics that lets Claude Code and Claude Desktop drive 10x Cloud single-cell / immune-profiling / Visium / Xenium analyses; available from Oct 20, 2025 ([10x docs](https://www.10xgenomics.com/support/software/cloud-analysis/latest/tutorials/cloud-mcp-server-code)).
- **[Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine, Drug Repurposing and Discovery] single-cell-rna-qc (Claude Skill)** — Anthropic's first published scientific skill; performs scverse MAD-based QC on `.h5ad` and 10x `.h5` inputs ([SKILL.md](https://github.com/anthropics/life-sciences/blob/main/single-cell-rna-qc/SKILL.md), [Anthropic tutorial](https://claude.com/resources/tutorials/how-to-use-the-single-cell-rna-qc-skill-with-claude)).

#### Updated
- **[catalog/README.md]** — Refreshed entry counts (Chemistry → 3, all other categories → 5; distinct tools → 5) and updated cross-cutting-tools example list.

#### Flagged
- _None._

#### Verified (no changes)
- _None — new-surfacing run._

### Deferred — next-run priority

The following candidates were observed in `anthropics/life-sciences` and adjacent sources during this run but deferred to remain within the 3-entry surfacing cap. Pick up next run before re-querying any source.

- **synapse@life-sciences** — Remote MCP server for Sage Bionetworks Synapse; needs verification of auth model and supplier-side docs.
- **wiley-scholar-gateway@life-sciences** — Remote MCP server for Wiley scholarly content; verify subscription/auth requirements.
- **instrument-data-to-allotrope@life-sciences** — Skill that converts lab-instrument data to Allotrope Simple Model; useful in Chemistry and Translational Medicine.
- **nextflow-development@life-sciences** — Skill for running nf-core pipelines (rnaseq, sarek, atacseq) on local or GEO/SRA inputs.
- **scvi-tools@life-sciences** — Skill packaging the scvi-tools deep-learning toolkit for single-cell omics.
- **scientific-problem-selection@life-sciences** — Skill encoding Fischbach & Walsh (Cell 2024) scientific-project framework.

## 2026-05-19

### Enable multi-category entries

Backfilled the new `Categories` field on every existing catalog entry and duplicated each entry block byte-identically into every category file it claims. Both currently-catalogued tools are cross-cutting biomedical research infrastructure and were assigned all seven categories.

#### Updated
- **[All categories] Anthropic PubMed Connector** — Added `Categories: Chemistry | Immunology and Microbiology | Integrative Structural and Computational Biology | Molecular and Cellular Biology | Neuroscience | Translational Medicine | Drug Repurposing and Discovery`. Entry block duplicated into the six non-Translational-Medicine category files.
- **[All categories] BioMCP** — Added `Categories: Chemistry | Immunology and Microbiology | Integrative Structural and Computational Biology | Molecular and Cellular Biology | Neuroscience | Translational Medicine | Drug Repurposing and Discovery` (reflecting that it bundles ClinicalTrials.gov, PubMed, MyVariant.info, and OpenFDA — all relevant to every life-science domain). Entry block duplicated into the six non-Translational-Medicine category files.
- **[catalog/README.md]** — Refreshed entry counts (each category now lists 2 entries; 2 distinct tools across the catalog) and clarified that cross-cutting entries are duplicated across files.
- **[AGENT.md]** — Removed the one-time multi-category backfill subsection now that the backfill has been executed.

#### Added
- **[Chemistry] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced` ([Tutorial](https://claude.com/resources/tutorials/using-the-pubmed-connector-in-claude)).
- **[Chemistry] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced` ([biomcp.org](https://biomcp.org/)).
- **[Immunology and Microbiology] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Immunology and Microbiology] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.
- **[Integrative Structural and Computational Biology] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Integrative Structural and Computational Biology] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.
- **[Molecular and Cellular Biology] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Molecular and Cellular Biology] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.
- **[Neuroscience] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Neuroscience] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.
- **[Drug Repurposing and Discovery] Anthropic PubMed Connector** — Cross-cutting literature search; added to this category's `Recently surfaced`.
- **[Drug Repurposing and Discovery] BioMCP** — Cross-cutting biomedical MCP; added to this category's `Recently surfaced`.

#### Flagged
- _None._

#### Verified (no changes)
- _None — backfill only._

## 2026-05-19

### Scope refocus to Claude-installable components

The catalog scope was narrowed to discrete, installable Claude components (Claude Skills, MCP servers, Claude Code Plugins, Claude.ai Connectors). General-purpose libraries, model weights distributed only as research artifacts, hosted SaaS without a Claude-installable wrapper, and bespoke LangChain-style agents are no longer in scope. The entry schema was migrated to add `Available in` (every supported install path) and `Tools / resources exposed`, and to drop the free-form `Benchmarks` and `Installation` fields. Surviving entries were re-keyed to the new schema; out-of-scope entries were removed (git history preserves them).

### Removed
- **[Chemistry] RDKit** — General-purpose cheminformatics library; no Claude Skill/MCP/Plugin/Connector wrapper.
- **[Chemistry] DeepChem** — General-purpose ML toolkit for chemistry; no Claude-installable wrapper.
- **[Chemistry] ChemCrow** — LangChain bespoke agent, not packaged as a Skill or Plugin.
- **[Structural and Computational Biology] AlphaFold 3** — Model weights + hosted server; no Claude-installable wrapper.
- **[Structural and Computational Biology] Boltz-1 / Boltz-2** — Model weights / research code; no Claude-installable wrapper.
- **[Structural and Computational Biology] Chai-1** — Model weights + hosted SaaS; no Claude-installable wrapper.
- **[Structural and Computational Biology] OpenFold / OpenFold3** — Research code reproductions; no Claude-installable wrapper.
- **[Structural and Computational Biology] ESM-2 / ESMFold** — Model weights distributed as research artifacts; no Claude-installable wrapper.
- **[Structural and Computational Biology] RFdiffusion** — Research-artifact model weights; no Claude-installable wrapper.
- **[Immunology and Microbiology] IgFold** — Research-artifact library; no Claude-installable wrapper.
- **[Molecular and Cellular Biology] Scanpy** — General-purpose single-cell library; no Claude-installable wrapper.
- **[Molecular and Cellular Biology] CZ CELLxGENE Discover Census** — Hosted dataset + client library; no Claude-installable wrapper.
- **[Neuroscience] DeepLabCut** — General-purpose pose-estimation library; no Claude-installable wrapper.
- **[Translational Medicine] Claude for Life Sciences** — Umbrella offering, not a discrete installable component.
- **[Drug Repurposing and Discovery] TxGNN** — Research-artifact model and code; no Claude-installable wrapper.

### Updated
- **[Translational Medicine] Anthropic PubMed Connector** — Re-keyed to new schema with explicit `Available in` (Claude Code plugin marketplace, direct `mcp add`, Claude.ai Healthcare connector) and `Tools / resources exposed`.
- **[Translational Medicine] BioMCP** — Re-keyed to new schema with explicit `Available in` (Claude Code via `uv`, Claude Desktop mcp_config.json) and `Tools / resources exposed`.
- **[AGENT.md]** — Removed the one-time scope-migration subsection now that it has been executed.
- **[catalog/README.md]** — Refreshed entry counts and timestamp; updated schema summary.

### Flagged
- _None._

### Verified (no changes)
- _None — scope migration only._

## 2026-05-18

First substantive curator run — seeded each category with established, primary-source-verifiable entries.

### Added
- **[Chemistry] RDKit** — Core BSD-3-Clause cheminformatics toolkit; latest release 2025.09.x ([GitHub](https://github.com/rdkit/rdkit), [Install docs](https://www.rdkit.org/docs/Install.html))
- **[Chemistry] DeepChem** — MIT-licensed deep-learning toolkit for chemistry and materials ([GitHub](https://github.com/deepchem/deepchem))
- **[Chemistry] ChemCrow** — LangChain chemistry agent (Bran et al., _Nature Machine Intelligence_ 2024) ([GitHub](https://github.com/ur-whitelab/chemcrow-public))
- **[Structural and Computational Biology] AlphaFold 3** — DeepMind biomolecular structure prediction; server GA, code under CC-BY-NC-SA 4.0 ([GitHub](https://github.com/google-deepmind/alphafold3))
- **[Structural and Computational Biology] Boltz-1 / Boltz-2** — MIT-licensed open structure + affinity models (MIT Jameel Clinic) ([GitHub](https://github.com/jwohlwend/boltz))
- **[Structural and Computational Biology] Chai-1** — Chai Discovery multimodal predictor with free web interface ([GitHub](https://github.com/chaidiscovery/chai-lab))
- **[Structural and Computational Biology] OpenFold / OpenFold3** — Apache-2.0 reproductions of AlphaFold 2/3 ([GitHub](https://github.com/aqlaboratory/openfold), [OpenFold3](https://github.com/aqlaboratory/openfold-3))
- **[Structural and Computational Biology] ESM-2 / ESMFold** — Meta FAIR protein language model + folding head ([GitHub](https://github.com/facebookresearch/esm))
- **[Structural and Computational Biology] RFdiffusion** — Baker Lab generative protein design; RFdiffusion3 released Dec 2025 ([GitHub](https://github.com/RosettaCommons/RFdiffusion), [IPD announcement](https://www.ipd.uw.edu/2025/12/rfdiffusion3-now-available/))
- **[Immunology and Microbiology] IgFold** — Gray Lab antibody structure prediction with AntiBERTy embeddings ([GitHub](https://github.com/Graylab/IgFold))
- **[Molecular and Cellular Biology] Scanpy** — scverse single-cell analysis toolkit, BSD-3-Clause, v1.12.1 ([GitHub](https://github.com/scverse/scanpy))
- **[Molecular and Cellular Biology] CZ CELLxGENE Discover Census** — CZI hosted single-cell corpus with Python/R APIs ([Docs](https://chanzuckerberg.github.io/cellxgene-census/))
- **[Neuroscience] DeepLabCut** — Mathis Labs markerless pose estimation; v3.0 PyTorch engine ([GitHub](https://github.com/DeepLabCut/DeepLabCut))
- **[Translational Medicine] Anthropic PubMed Connector** — Official MCP server for NCBI literature ([Tutorial](https://claude.com/resources/tutorials/using-the-pubmed-connector-in-claude))
- **[Translational Medicine] BioMCP** — GenomOncology MIT-licensed MCP server bundling ClinicalTrials.gov, PubMed, MyVariant, OpenFDA ([biomcp.org](https://biomcp.org/))
- **[Translational Medicine] Claude for Life Sciences** — Anthropic life-science offering launched Oct 2025 ([CNBC](https://www.cnbc.com/2025/10/20/anthropic-claude-life-sciences-research-ai.html))
- **[Drug Repurposing and Discovery] TxGNN** — Zitnik Lab zero-shot graph foundation model for drug repurposing (Huang et al., _Nature Medicine_ 2024) ([GitHub](https://github.com/mims-harvard/TxGNN))

### Updated
- **[catalog/README.md]** — Refreshed with current entry counts and freshness timestamp.

### Flagged
- _None._

### Verified (no changes)
- _None — first substantive run._
