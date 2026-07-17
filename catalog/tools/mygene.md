---
title: MyGene.info MCP (BioThings)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: longevity-genie
availability: GA
tool_categories: [All]
last_verified: 2026-07-17
claude_science: true
summary: Gene annotation and ID conversion across species via MyGene.info/BioThings; the Genes & Ontologies connector in Claude Science.
---

# MyGene.info MCP (BioThings)

Resolves gene identifiers and annotations across species through MyGene.info via the BioThings MCP server.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [longevity-genie](https://github.com/longevity-genie/biothings-mcp) |
| **Availability** | GA — community OSS (PyPI) |
| **Pricing** | Free / OSS (data CC BY) |
| **Capabilities** | Read-only |

## How to install

- **Claude Code** — community MCP server ([longevity-genie/biothings-mcp](https://github.com/longevity-genie/biothings-mcp), OSS):
  ```
  claude mcp add biothings -- uvx biothings-mcp
  ```
  A hosted endpoint is also available at `https://biothings.longevity-genie.info/mcp`.
- **Claude Science** — also available as the *Genes & Ontologies* featured connector (Anthropic-hosted; enable in Claude Science).
- **Public API** — query directly at [mygene.info/v3](https://mygene.info/v3).

## What it does

Query gene annotations, symbol/alias resolution, and cross-database ID conversion (Entrez, Ensembl, UniProt, symbol) across species via MyGene.info; the same server also wraps other BioThings APIs.

**Primary use cases**: Gene ID conversion, gene annotation lookup, cross-species mapping

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Genes & Ontologies* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

MyGene.info is maintained by the Su/Wu Lab at Scripps Research. The BioThings MCP wraps MyGene and sibling BioThings services.

## Sources

- [longevity-genie/biothings-mcp](https://github.com/longevity-genie/biothings-mcp)
- [MyGene.info](https://mygene.info/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=mygene&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmygene.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
