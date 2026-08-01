---
title: UniProt MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Augmented Nature
availability: GA
tool_categories: [Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Drug Repurposing and Discovery]
last_verified: 2026-08-01
flagged: "upstream license is self-contradictory — committed LICENSE is a restrictive non-commercial grant while package.json and the README claim MIT, as of 2026-08-01"
claude_science: true
verification: works
verified_on: 2026-07-29
verification_note: "GitHub repo resolves (redirects to Augmented-Nature-UniProt-MCP-Server); wraps the public UniProt REST API and needs no auth"
security: caution
security_on: 2026-07-29
security_note: "provenance matches supplier Augmented-Nature but committed LICENSE is restrictive non-commercial while package.json and page claim MIT; last push 2025-12-21 (~7mo stale)"
summary: MCP server giving Claude 26 tools over the UniProt REST API for protein search, domains, orthologs, PTMs, pathways, and multi-format export.
---

# UniProt MCP Server

MCP wrapper over the UniProt REST API — the standard protein-annotation layer linking sequence, structure, function, and cross-references to other databases.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Augmented Nature](https://github.com/Augmented-Nature/UniProt-MCP-Server) (community OSS) |
| **Availability** | GA |
| **Pricing** | Free to use — wraps the public UniProt REST API, no auth. **Unverified —** redistribution terms are contradictory upstream: the committed `LICENSE` file is a restrictive non-commercial grant while `package.json` and the README say MIT. |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-29 |
| **Security** | caution · 2026-07-29 — committed LICENSE is restrictive non-commercial while page/package.json claim MIT; ~7mo stale |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/proteomics-protein-engineering/uniprot-protein-database` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
```
git clone https://github.com/Augmented-Nature/UniProt-MCP-Server
cd UniProt-MCP-Server
npm install
npm run build
```

Then add to `claude_desktop_config.json` (replace `/path/to/UniProt-MCP-Server` with the absolute path of your clone — e.g., `/Users/you/repos/UniProt-MCP-Server`):

```json
{
  "mcpServers": {
    "uniprot": { "command": "node", "args": ["/path/to/UniProt-MCP-Server/build/index.js"] }
  }
}
```

For Claude Code, the equivalent registration is:

```
claude mcp add --transport stdio uniprot -- node /path/to/UniProt-MCP-Server/build/index.js
```

Docker alternative: `docker build -t uniprot-mcp-server . && docker run -i uniprot-mcp-server`.

## What it does

26 tools across:

- **Core protein analysis** — search, get by accession, sequence and feature retrieval.
- **Comparative / evolutionary** — orthologs, taxonomy, phylogeny.
- **Structure / function** — domain, PTM, active-site annotation; AlphaFold cross-references.
- **Biological context** — pathways, GO terms, subcellular localization.
- **Batch search** and cross-reference resolution.
- **Export** — FASTA, GFF, GenBank, EMBL, TSV, XML, JSON.

**Primary use cases**: Resolve gene-to-protein-to-domain context for a hit list; pull orthologs and PTMs; build cross-reference tables for a target panel.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Genes & Ontologies* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

stdio transport. No auth required — calls the public UniProt REST API. Complements ChEMBL (small molecules) and AlphaFold (3D) by covering the annotation layer.

Upstream licensing is inconsistent (see **Pricing** above) and the last push was 2025-12-21. Running the server is unproblematic — it is a thin read-only client over a public API — but do not vendor or redistribute the code until the terms are clarified. The SciAgent-Skills packaging above (CC BY 4.0) is a cleanly-licensed alternative route to the same UniProt REST surface.

## Sources

- [`Augmented-Nature/UniProt-MCP-Server`](https://github.com/Augmented-Nature/UniProt-MCP-Server)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=uniprot&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Funiprot.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
