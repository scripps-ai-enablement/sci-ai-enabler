---
title: Gene Ontology MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Augmented Nature
availability: Beta
tool_categories: [All]
last_verified: 2026-07-17
claude_science: true
summary: Query GO terms, annotations, and enrichment inputs from the Gene Ontology; part of the Genes & Ontologies connector in Claude Science.
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "repo LICENSE is a restrictive personal non-commercial grant (GitHub NOASSERTION) not the OSS the page implied — fixed in-page; GO API is public read-only"
---

# Gene Ontology MCP Server

Exposes Gene Ontology terms and gene–function annotations to Claude via a community MCP server over the GO API.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Augmented Nature](https://github.com/Augmented-Nature/GeneOntology-MCP-Server) |
| **Availability** | Beta — community OSS |
| **Pricing** | GO data is Free / CC BY 4.0; the MCP wrapper code is under a restrictive personal, non-commercial license (no redistribution/modification/commercial use without permission) |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — wrapper repo LICENSE is a restrictive non-commercial grant (GitHub NOASSERTION); GO API public read-only |

## How to install

- **Claude Code / Desktop** — community MCP server ([Augmented Nature](https://github.com/Augmented-Nature/GeneOntology-MCP-Server), OSS):
  ```
  git clone https://github.com/Augmented-Nature/GeneOntology-MCP-Server
  cd GeneOntology-MCP-Server
  npm install && npm run build
  claude mcp add --transport stdio geneontology-server -- node /path/to/GeneOntology-MCP-Server/build/index.js
  ```
- **Claude Science** — also available as the *Genes & Ontologies* featured connector (Anthropic-hosted; enable in Claude Science).
- **Public API** — query directly at [api.geneontology.org](https://api.geneontology.org).

## What it does

Look up GO terms and hierarchy, retrieve gene-product annotations, and gather inputs for functional enrichment via the Gene Ontology API.

**Primary use cases**: GO term lookup, functional annotation, enrichment input retrieval

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Genes & Ontologies* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Community server over the public GO API (api.geneontology.org).

## Sources

- [Augmented-Nature/GeneOntology-MCP-Server](https://github.com/Augmented-Nature/GeneOntology-MCP-Server)
- [Gene Ontology](http://geneontology.org/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=gene-ontology&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgene-ontology.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
