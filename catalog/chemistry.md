# Chemistry

> Installable Claude components (Skills, MCP servers, Plugins, Connectors) focused on cheminformatics, computational chemistry, chemical structure handling, reaction prediction, retrosynthesis, and chemistry-aware language interfaces.

_Last updated: 2026-05-19_

## Entries

### Anthropic PubMed Connector

- **Categories**: Chemistry | Immunology and Microbiology | Integrative Structural and Computational Biology | Molecular and Cellular Biology | Neuroscience | Translational Medicine | Drug Repurposing and Discovery
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

- **Categories**: Chemistry | Immunology and Microbiology | Integrative Structural and Computational Biology | Molecular and Cellular Biology | Neuroscience | Translational Medicine | Drug Repurposing and Discovery
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

- **Categories**: Chemistry | Immunology and Microbiology | Integrative Structural and Computational Biology | Molecular and Cellular Biology | Neuroscience | Translational Medicine | Drug Repurposing and Discovery
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

## Flagged for review

_None._

## Recently surfaced

- **Anthropic PubMed Connector** (added 2026-05-19) — Cross-cutting literature-search MCP/Connector added to this category as part of the multi-category backfill.
- **BioMCP** (added 2026-05-19) — Cross-cutting biomedical MCP (ClinicalTrials.gov, PubMed, MyVariant, OpenFDA) added to this category as part of the multi-category backfill.
- **BioRender Connector** (added 2026-05-19) — Cross-cutting scientific-illustration MCP / Claude.ai connector; useful for chemistry-figure assembly. ([Anthropic tutorial](https://claude.com/resources/tutorials/using-the-biorender-connector-in-claude))
