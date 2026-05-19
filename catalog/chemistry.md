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

## Flagged for review

_None._

## Recently surfaced

- **Anthropic PubMed Connector** (added 2026-05-19) — Cross-cutting literature-search MCP/Connector added to this category as part of the multi-category backfill.
- **BioMCP** (added 2026-05-19) — Cross-cutting biomedical MCP (ClinicalTrials.gov, PubMed, MyVariant, OpenFDA) added to this category as part of the multi-category backfill.
