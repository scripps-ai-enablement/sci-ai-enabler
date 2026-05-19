# Entries

> Canonical content for every Claude-installable life-science component in the catalog. Each entry is tagged with the categories it applies to via a `Categories` field. Browse by research area via the category pages, or scan this file directly.

_Last updated: 2026-05-19_

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

## Recently surfaced

- **BioRender Connector** (added 2026-05-19) — Scientific-illustration MCP / Claude.ai connector for slides, papers, and grants.
- **10x Genomics Cloud MCP** (added 2026-05-19) — Conversational interface to 10x Cloud single-cell, immune-profiling, and spatial analyses.
- **single-cell-rna-qc (Claude Skill)** (added 2026-05-19) — Anthropic's first scientific skill; scverse MAD-based QC for single-cell RNA-seq.

## Flagged for review

_None._

## Deferred — next-run priority

Candidates observed during the most recent surfacing pass but not yet catalogued. Pick these up before re-querying other sources.

- **synapse@life-sciences** — Remote MCP server for Sage Bionetworks Synapse; needs verification of auth model and supplier-side docs.
- **wiley-scholar-gateway@life-sciences** — Remote MCP server for Wiley scholarly content; verify subscription/auth requirements.
- **instrument-data-to-allotrope@life-sciences** — Skill that converts lab-instrument data to Allotrope Simple Model; useful in Chemistry and Translational Medicine.
- **nextflow-development@life-sciences** — Skill for running nf-core pipelines (rnaseq, sarek, atacseq) on local or GEO/SRA inputs.
- **scvi-tools@life-sciences** — Skill packaging the scvi-tools deep-learning toolkit for single-cell omics.
- **scientific-problem-selection@life-sciences** — Skill encoding Fischbach & Walsh (Cell 2024) scientific-project framework.
