# Entries

> Canonical content for every Claude-installable life-science component in the catalog. Each entry is tagged with the categories it applies to via a `Categories` field. Browse by research area via the category pages, or scan this file directly.

_Last updated: 2026-05-20_

## Entries

### 10x Genomics Cloud MCP

- **Categories**: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine
- **Type**: MCP server
- **Supplier**: 10x Genomics ([10xgenomics.com](https://www.10xgenomics.com/))
- **Availability**: GA — available from Oct 20, 2025
- **Pricing**: Free plugin; requires a paid 10x Genomics Cloud account with active analysis data
- **Capabilities**: Read/Write — query and trigger single-cell, immune-profiling, and spatial-transcriptomics analyses stored in 10x Genomics Cloud
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install 10x-genomics@life-sciences`, then `/plugin` → Configure with 10x Cloud access token)
  - Claude Desktop (MCPB extension distributed by 10x Genomics; configure with the same 10x Cloud access token)
- **Tools / resources exposed**: project and analysis listing, reference and annotation-model lookup, analysis output retrieval, project-file inspection for 10x Cloud Analysis runs
- **Primary use cases**: Conversational orchestration of 10x Cloud single-cell / Visium / Xenium analyses, retrieval of analysis outputs, prompt-based pipeline configuration
- **Integration notes**: Local MCPB binary hosted by 10x Genomics, not bundled in `anthropics/life-sciences`; auth via 10x Cloud access token from Security settings; requires existing cloud projects to be useful
- **Sources**: [10x Genomics Cloud MCP docs](https://www.10xgenomics.com/support/software/cloud-analysis/latest/tutorials/cloud-mcp-server-code), [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences), [DeepWiki: 10x Genomics Cloud](https://deepwiki.com/anthropics/life-sciences/3.7-10x-genomics-cloud)
- **First catalogued**: 2026-05-19
- **Last verified**: 2026-05-19

### Anthropic PubMed Connector

- **Categories**: All
- **Type**: MCP server
- **Supplier**: Anthropic ([claude.com](https://claude.com/))
- **Availability**: GA (Claude.ai / Claude Code); Beta MCP HTTP endpoint
- **Pricing**: Free / OSS — included with Claude plans; no extra cost beyond model usage
- **Capabilities**: Read-only — PubMed and PubMed Central search via NCBI E-utilities; related NCBI databases (Gene, Protein, Nucleotide) discoverable via Claude
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install pubmed@life-sciences`)
  - Claude Code (direct mcp add: `claude mcp add --transport http pubmed https://pubmed.mcp.claude.com/mcp` with beta header `mcp-client-2025-11-20`)
  - Claude.ai (Healthcare connector — toggle in Settings → Connectors)
- **Tools / resources exposed**: PubMed/PMC search, article metadata retrieval; related NCBI E-utilities databases (Gene, Protein, Nucleotide) discoverable through Claude
- **Primary use cases**: Literature search, systematic review scaffolding, MeSH-aware Boolean query refinement
- **Integration notes**: Anthropic-managed hosted HTTP transport; NCBI rate limits apply server-side; updated daily from PubMed; surfaced as part of the Claude for Life Sciences launch (Oct 2025)
- **Sources**: [Anthropic tutorial](https://claude.com/resources/tutorials/using-the-pubmed-connector-in-claude), [Claude for Life Sciences coverage](https://www.cnbc.com/2025/10/20/anthropic-claude-life-sciences-research-ai.html)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-19

### BioMCP

- **Categories**: All
- **Type**: MCP server
- **Supplier**: GenomOncology ([biomcp.org](https://biomcp.org/))
- **Availability**: GA
- **Pricing**: Free / OSS (MIT); optional API keys (NCBI, OpenFDA, NCI CTS, OncoKB, AlphaGenome) raise rate limits or unlock private sources
- **Capabilities**: Read-only — unified MCP access to ClinicalTrials.gov, PubMed, MyVariant.info, OpenFDA, NCI CTS, and related biomedical sources
- **Available in**:
  - Claude Code (direct mcp add via uv: `uv tool install biomcp-cli` then add `uv run --with biomcp-python biomcp run` as an MCP server)
  - Claude Desktop (manual mcp_config.json entry running `biomcp run` via uv or pip-installed CLI)
- **Tools / resources exposed**: ~21 tools including `trial_searcher`, `trial_getter`, plus PubMed search, MyVariant.info variant lookup, OpenFDA adverse-event queries
- **Primary use cases**: Clinical trial discovery, variant lookup, drug adverse-event review, biomedical Q&A for agents
- **Integration notes**: stdio transport; supports both ClinicalTrials.gov default and NCI CTS source; ships an agent skill via `biomcp skill install`
- **Sources**: [biomcp.org](https://biomcp.org/), [mcpservers.org listing](https://mcpservers.org/servers/genomoncology/biomcp), [ClinicalTrials.gov source page](https://biomcp.org/sources/clinicaltrials-gov/)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-19

### BioRender Connector

- **Categories**: All
- **Type**: MCP server
- **Supplier**: BioRender ([biorender.com](https://www.biorender.com/))
- **Availability**: GA — launched Oct 23, 2025 alongside the Claude for Life Sciences partnership
- **Pricing**: Freemium — Free and Individual plans access a limited icon/template set; Premium / Team plans access the full BioRender library
- **Capabilities**: Read/Write — search BioRender's icon and template library and request scientific-figure suggestions for slides, papers, posters, and grants
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install biorender@life-sciences`)
  - Claude.ai (BioRender connector — toggle in Settings → Connectors; sign in with BioRender credentials)
- **Tools / resources exposed**: scientific-icon search, template search, figure recommendations across the 50,000+ vetted BioRender icon library
- **Primary use cases**: Building scientific figures, generating slide-deck illustrations, sourcing curated templates for grants and publications
- **Integration notes**: Remote MCP server hosted by BioRender; OAuth login required; access scope depends on BioRender subscription tier
- **Sources**: [Anthropic tutorial](https://claude.com/resources/tutorials/using-the-biorender-connector-in-claude), [BioRender × Anthropic partnership announcement (BusinessWire, 2025-10-23)](https://www.businesswire.com/news/home/20251023858531/en/BioRender-and-Anthropic-Partner-To-Bring-Scientific-Illustrations-to-Claude-For-Life-Sciences), [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences)
- **First catalogued**: 2026-05-19
- **Last verified**: 2026-05-19

### instrument-data-to-allotrope (Claude Skill)

- **Categories**: Chemistry, Drug Repurposing and Discovery, Immunology and Microbiology, Molecular and Cellular Biology, Translational Medicine
- **Type**: Claude Skill
- **Supplier**: Anthropic ([anthropics/life-sciences](https://github.com/anthropics/life-sciences))
- **Availability**: GA — distributed via `anthropics/life-sciences` marketplace alongside Claude for Life Sciences (Oct 2025)
- **Pricing**: Free / OSS
- **Capabilities**: Read/Write — parses lab-instrument output (PDF, CSV, Excel, TXT) and writes Allotrope Simple Model (ASM) JSON, flattened 2D CSV, and exportable Python parser code
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install instrument-data-to-allotrope@life-sciences`)
  - Claude.ai (Settings → Capabilities → Skills → Upload skill, using the skill bundle from the `anthropics/life-sciences` repo)
- **Tools / resources exposed**: instrument auto-detection, native parsing via the `allotropy` library with flexible/PDF-table fallback, ASM JSON emission, flattened-CSV emission, ASM validation with strict mode, exportable Python parser code
- **Primary use cases**: Standardising 40+ instrument types (cell counters, spectrophotometers, plate readers, qPCR, chromatography) for LIMS ingestion, data-lake loading, and downstream analysis
- **Integration notes**: Depends on `pip install allotropy`; falls back to a flexible parser or PDF table extraction when native parsing fails, with reduced metadata completeness reported; also bundled in the Anthropic `bio-research` plugin
- **Sources**: [Skill listing (playbooks)](https://playbooks.com/skills/anthropics/life-sciences/instrument-data-to-allotrope), [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences), [Allotrope ASM overview](https://www.allotrope.org/asm)
- **First catalogued**: 2026-05-19
- **Last verified**: 2026-05-19

### nextflow-development (Claude Skill)

- **Categories**: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine
- **Type**: Claude Skill
- **Supplier**: Anthropic ([anthropics/life-sciences](https://github.com/anthropics/life-sciences))
- **Availability**: GA — distributed via `anthropics/life-sciences` marketplace alongside Claude for Life Sciences (Oct 2025); positioned by Anthropic as a prototype/educational example
- **Pricing**: Free / OSS
- **Capabilities**: Read/Write — configures and runs nf-core pipelines on local FASTQ inputs or public GEO/SRA accessions; writes pipeline outputs to a user-specified directory
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install nextflow-development@life-sciences`)
  - Claude.ai (Settings → Capabilities → Skills → Upload skill, using the skill bundle from the `anthropics/life-sciences` repo)
- **Tools / resources exposed**: `SKILL.md` instructions for nf-core `rnaseq` (v3.22.2), `sarek` (v3.7.1), and `atacseq` (v2.1.2) — including the standard `-profile test,docker` smoke commands and pointers to expand support to other nf-core pipelines
- **Primary use cases**: Bench-scientist orchestration of bulk RNA-seq, germline/somatic variant calling, and ATAC-seq analyses without bespoke bioinformatics tooling
- **Integration notes**: Requires Nextflow and Docker (or another supported container engine) on the host; users are responsible for compute capacity and result validation — Anthropic flags it as not production-ready without domain validation
- **Sources**: [Skill listing (agent-skills.md)](https://agent-skills.md/skills/anthropics/life-sciences/nextflow-development), [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences), [nf-core pipelines](https://nf-co.re/pipelines)
- **First catalogued**: 2026-05-19
- **Last verified**: 2026-05-19

### Scholar Gateway Connector (Wiley)

- **Categories**: All
- **Type**: MCP server
- **Supplier**: Wiley ([wiley.com](https://www.wiley.com/))
- **Availability**: Beta — released alongside the Claude for Life Sciences launch (Oct 2025)
- **Pricing**: Free / OSS — requires a free Scholar Gateway account
- **Capabilities**: Read-only — search Wiley's Scholar Gateway corpus and retrieve scholarly article metadata, abstracts, and DOI-linked content
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install wiley-scholar-gateway@life-sciences`; sign in with Scholar Gateway credentials when prompted)
  - Claude.ai (Scholar Gateway connector — toggle in Settings → Connectors; sign in with Scholar Gateway credentials)
- **Tools / resources exposed**: scholarly-article search, publication metadata retrieval, full-text/DOI-linked access for Wiley-indexed content (3M+ articles across STEM, including 300+ Life Sciences journals covering 900,000+ research articles)
- **Primary use cases**: Literature search grounded in peer-reviewed sources, citation-verifiable Q&A, supplementing PubMed with Wiley-published journal content
- **Integration notes**: Remote MCP server hosted at `connector.scholargateway.ai/mcp`; HTTP transport; OAuth login flow on first use; access scope tied to Scholar Gateway account
- **Sources**: [Anthropic tutorial](https://claude.com/resources/tutorials/using-the-scholar-gateway-connector-in-claude), [DeepWiki: Wiley Scholar Gateway](https://deepwiki.com/anthropics/life-sciences/3.5-wiley-scholar-gateway), [Wiley AI Gateway press release (2025)](https://newsroom.wiley.com/press-releases/press-release-details/2025/Wiley-Launches-Interoperable-Platform-to-Power-Scientific-Discovery-in-Worlds-Leading-AI-Technologies/default.aspx)
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### scientific-problem-selection (Claude Skill)

- **Categories**: All
- **Type**: Claude Skill
- **Supplier**: Anthropic ([anthropics/life-sciences](https://github.com/anthropics/life-sciences))
- **Availability**: GA — distributed via `anthropics/life-sciences` marketplace alongside Claude for Life Sciences (Oct 2025)
- **Pricing**: Free / OSS
- **Capabilities**: Read-only — guides Claude through a structured framework for evaluating research questions; does not write files unless the user asks Claude to summarise outputs to disk
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install scientific-problem-selection@life-sciences`)
  - Claude.ai (Settings → Capabilities → Skills → Upload skill, using the skill bundle from the `anthropics/life-sciences` repo)
- **Tools / resources exposed**: `SKILL.md` instructions encoding Fischbach & Walsh's *Cell* (2024) framework — covers project ideation, risk assessment, troubleshooting stuck projects, and strategic scientific planning
- **Primary use cases**: PI/postdoc project ideation, go/no-go decisions on lab projects, structured triage of competing research directions
- **Integration notes**: Pure prompt-based skill (no external services or runtime dependencies); applies to any life-science research planning conversation
- **Sources**: [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences), [Claude for Life Sciences announcement](https://www.anthropic.com/news/claude-for-life-sciences), [Fischbach & Walsh, *Cell* (2024)](https://www.cell.com/cell/fulltext/S0092-8674(24)00077-3)
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

### scvi-tools (Claude Skill)

- **Categories**: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine
- **Type**: Claude Skill
- **Supplier**: Anthropic ([anthropics/life-sciences](https://github.com/anthropics/life-sciences))
- **Availability**: GA — distributed via `anthropics/life-sciences` marketplace alongside Claude for Life Sciences (Oct 2025)
- **Pricing**: Free / OSS
- **Capabilities**: Read/Write — guides Claude through scvi-tools deep-learning workflows on AnnData single-cell inputs; writes trained model artifacts, latent representations, and normalized expression matrices
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install scvi-tools@life-sciences`)
  - Claude.ai (Settings → Capabilities → Skills → Upload skill, using the skill bundle from the `anthropics/life-sciences` repo)
- **Tools / resources exposed**: `SKILL.md` workflows for scVI / scANVI (batch correction, semi-supervised cell-type annotation), totalVI and MultiVI (CITE-seq, RNA+ATAC multi-modal integration), PeakVI and scBasset (chromatin accessibility), DestVI / Tangram / cell2location / Stereoscope (spatial deconvolution), contrastiveVI (perturbation), sysVI (cross-cohort batch correction), and veloVI (RNA velocity); model setup, training, and latent-extraction code patterns
- **Primary use cases**: Deep-learning-based batch integration, reference-mapped cell-type annotation, multi-modal CITE-seq / multiome analysis, spatial transcriptomics deconvolution
- **Integration notes**: Requires Python with `scvi-tools` (PyTorch + AnnData stack) installed locally; GPU recommended for larger datasets; expects raw-count layer (not log-normalized) when registering AnnData via `setup_anndata`
- **Sources**: [Anthropic tutorial](https://claude.com/resources/tutorials/how-to-use-the-scvi-tools-bioinformatics-skill-bundle-with-claude), [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences), [scvi-tools documentation](https://docs.scvi-tools.org/)
- **First catalogued**: 2026-05-19
- **Last verified**: 2026-05-19

### single-cell-rna-qc (Claude Skill)

- **Categories**: Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine
- **Type**: Claude Skill
- **Supplier**: Anthropic ([anthropics/life-sciences](https://github.com/anthropics/life-sciences))
- **Availability**: GA — first Anthropic-published scientific skill, released with Claude for Life Sciences (Oct 2025)
- **Pricing**: Free / OSS
- **Capabilities**: Read/Write — runs QC on `.h5ad` and 10x `.h5` single-cell files using scverse best practices; writes filtered matrices and QC plots
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install single-cell-rna-qc@life-sciences`)
  - Claude.ai (Settings → Capabilities → Skills → Upload skill, using the skill ZIP from the `anthropics/life-sciences` repo)
- **Tools / resources exposed**: `SKILL.md` instructions plus bundled scripts that perform MAD-based filtering on gene counts, total counts, and mitochondrial percentage, and emit standard QC visualizations
- **Primary use cases**: First-pass single-cell RNA-seq quality control, doublet/empty-droplet filtering, generating QC figures for downstream Scanpy / scvi-tools workflows
- **Integration notes**: Reads AnnData `.h5ad` or 10x Cell Ranger `.h5`; uses median-absolute-deviation thresholds in line with scverse guidance; auto-detects format
- **Sources**: [Skill source (SKILL.md)](https://github.com/anthropics/life-sciences/blob/main/single-cell-rna-qc/SKILL.md), [Anthropic tutorial](https://claude.com/resources/tutorials/how-to-use-the-single-cell-rna-qc-skill-with-claude), [Claude for Life Sciences announcement](https://www.anthropic.com/news/claude-for-life-sciences)
- **First catalogued**: 2026-05-19
- **Last verified**: 2026-05-19

### Synapse.org Connector

- **Categories**: All
- **Type**: MCP server
- **Supplier**: Sage Bionetworks ([synapse.org](https://www.synapse.org/))
- **Availability**: GA — released with the Claude for Life Sciences launch (Oct 2025)
- **Pricing**: Free / OSS — requires a free Synapse account; some datasets require governance approval
- **Capabilities**: Read-only — discover Synapse projects, browse data-asset structure, and retrieve metadata for authorised users across all of Synapse
- **Available in**:
  - Claude Code (plugin marketplace: `/plugin marketplace add anthropics/life-sciences` then `/plugin install synapse@life-sciences`)
  - Claude Code (direct mcp add: `claude mcp add --transport http synapse https://mcp.synapse.org/mcp`)
  - Claude.ai (Synapse.org connector — toggle in Settings → Connectors; OAuth2 sign-in with Synapse credentials)
- **Tools / resources exposed**: project discovery and listing, file/folder structure inspection, metadata retrieval for Synapse-hosted data assets, cross-project search subject to per-project access controls
- **Primary use cases**: Discovering biomedical datasets hosted on Synapse, retrieving project and file metadata, navigating consortium / DREAM-challenge data structures
- **Integration notes**: Remote MCP server hosted at `mcp.synapse.org/mcp`; HTTP transport; OAuth2 default (browser-based) — personal access tokens supported as alternative; data access governed by per-project controls (some require Synapse governance approval); Synapse Terms of Service restrict data redistribution, which may include third-party AI providers — review before connecting controlled datasets
- **Sources**: [Anthropic tutorial](https://claude.com/resources/tutorials/using-the-synapse-org-connector-in-claude), [anthropics/life-sciences marketplace](https://github.com/anthropics/life-sciences), [Synapse MCP server source](https://github.com/susheel/synapse-mcp)
- **First catalogued**: 2026-05-20
- **Last verified**: 2026-05-20

## Recently surfaced

- **Synapse.org Connector** (added 2026-05-20) — Sage Bionetworks remote MCP server / Claude.ai connector for discovery and metadata retrieval across Synapse-hosted biomedical data.
- **scientific-problem-selection (Claude Skill)** (added 2026-05-20) — Anthropic skill encoding Fischbach & Walsh's *Cell* (2024) framework for research project ideation, risk assessment, and troubleshooting.
- **Scholar Gateway Connector (Wiley)** (added 2026-05-20) — Wiley remote MCP server / Claude.ai connector providing peer-reviewed scholarly content (3M+ articles, 300+ Life Sciences journals).
- **scvi-tools (Claude Skill)** (added 2026-05-19) — Anthropic skill bundling deep-learning workflows for scVI, scANVI, totalVI, MultiVI, PeakVI, DestVI, veloVI, sysVI, and contrastiveVI on single-cell omics data.
- **nextflow-development (Claude Skill)** (added 2026-05-19) — Anthropic skill that runs nf-core `rnaseq`, `sarek`, and `atacseq` pipelines on local or GEO/SRA inputs.

## Flagged for review

_None._

## Deferred — next-run priority

Candidates observed during the most recent surfacing pass but not yet catalogued. Pick these up before re-querying other sources.

- **bio-research@anthropics/knowledge-work-plugins** — Anthropic umbrella plugin bundling 10 MCP servers and 6 analysis skills for life-science research; verify install path and complete tool inventory before cataloguing.
- **benchling@life-sciences** — Local MCPB connector for Benchling ELN/LIMS (named in the Anthropic Claude for Life Sciences launch alongside 10x Genomics); verify install path, auth, and exposed tools before cataloguing.
