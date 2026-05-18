# Translational Medicine

> AI ecosystem components bridging discovery and clinical application — clinical-trial tooling, biomarker discovery, patient stratification, real-world evidence, EHR-aware agents, and regulatory-document assistants.

_Last updated: 2026-05-18_

## Entries

### Anthropic PubMed Connector

- **Type**: MCP server (hosted)
- **Supplier**: Anthropic ([claude.com](https://claude.com/))
- **Availability**: GA (within Claude.ai and Claude Code; beta MCP HTTP endpoint)
- **Pricing**: Included with Claude plans; no extra cost beyond model usage
- **Capabilities**: Read-only — PubMed and PubMed Central search; access to NCBI E-utilities; related NCBI databases (Gene, Protein, Nucleotide) discoverable via Claude
- **Primary use cases**: Literature search, systematic review scaffolding, MeSH-aware Boolean query refinement
- **Benchmarks**: None published
- **Installation**: Claude Code: `/plugin marketplace add anthropics/life-sciences` then `/plugin install pubmed@life-sciences`; API: connect to `https://pubmed.mcp.claude.com/mcp` with beta header `mcp-client-2025-11-20`
- **Integration notes**: NCBI rate limits apply server-side; updated daily from PubMed; surfaced as part of the broader Claude for Life Sciences launch (Oct 2025)
- **Sources**: [Anthropic tutorial](https://claude.com/resources/tutorials/using-the-pubmed-connector-in-claude), [Claude for Life Sciences coverage](https://www.cnbc.com/2025/10/20/anthropic-claude-life-sciences-research-ai.html)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### BioMCP

- **Type**: MCP server
- **Supplier**: GenomOncology ([biomcp.org](https://biomcp.org/))
- **Availability**: GA
- **Pricing**: Free / OSS (MIT); optional API keys (NCBI, OpenFDA, NCI CTS, OncoKB, AlphaGenome) raise rate limits or unlock private sources
- **Capabilities**: Read-only — unified MCP access to ClinicalTrials.gov, PubMed, MyVariant.info, OpenFDA, NCI CTS, and related biomedical sources
- **Primary use cases**: Trial discovery, variant lookup, drug adverse-event review, biomedical Q&A for agents
- **Benchmarks**: None published
- **Installation**: `uv tool install biomcp-cli` (or `pip install biomcp-cli`); Claude Desktop/Cursor config via `uv run --with biomcp-python biomcp run`
- **Integration notes**: 21 individual tools (trial_searcher, trial_getter, etc.); supports both ClinicalTrials.gov default and NCI CTS source; can ship an agent skill via `biomcp skill install`
- **Sources**: [biomcp.org](https://biomcp.org/), [GitHub topic](https://mcpservers.org/servers/genomoncology/biomcp), [ClinicalTrials.gov source page](https://biomcp.org/sources/clinicaltrials-gov/)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

### Claude for Life Sciences

- **Type**: Hosted service (model + integration suite)
- **Supplier**: Anthropic ([anthropic.com](https://www.anthropic.com/))
- **Availability**: GA (launched October 2025)
- **Pricing**: Available via Claude.com plans and AWS Marketplace; enterprise pricing not publicly disclosed
- **Capabilities**: Read/Write — Claude Sonnet 4.5-class model with life-science-tuned protocol understanding, integrations to Benchling, PubMed, 10x Genomics, Synapse.org, and others
- **Primary use cases**: Literature review, hypothesis generation, lab-data summarisation, regulatory document drafting
- **Benchmarks**: Anthropic reports Novo Nordisk reducing clinical study documentation from >10 weeks to ~10 minutes (vendor case study, unverified independently)
- **Installation**: Available through Claude.com and AWS Marketplace; integrations enabled via MCP connectors
- **Integration notes**: Partners include Caylent, KPMG, Deloitte; integrations include Benchling lab informatics, Synapse.org, 10x Genomics
- **Sources**: [CNBC coverage](https://www.cnbc.com/2025/10/20/anthropic-claude-life-sciences-research-ai.html), [UPI coverage](https://www.upi.com/Science_News/2025/10/20/Anthropic-launches-Caude-Life-Sciences-reasearch-using-AI/5701760979687/)
- **First catalogued**: 2026-05-18
- **Last verified**: 2026-05-18

## Flagged for review

_None._

## Recently surfaced

- **Anthropic PubMed Connector** (added 2026-05-18) — official MCP server for NCBI literature.
- **BioMCP** (added 2026-05-18) — multi-source biomedical MCP server (GenomOncology).
- **Claude for Life Sciences** (added 2026-05-18) — Anthropic's life-science model + integrations bundle.
