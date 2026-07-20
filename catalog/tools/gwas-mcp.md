---
title: GWAS-MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: ZaEyAsa
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-11
summary: Single-install MCP server exposing 30+ tools across 14 biological databases (UniProt, Ensembl, ClinVar, GWAS Catalog, STRING, AlphaFold, KEGG, Open Targets, OMIM) for variant-to-target research.
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "PyPI gwas-mcp 1.0.2 MIT resolves but GitHub reports canonical owner muslus/gwas-mcp (page cites zaeyasa) and it is single-maintainer/1-star, stale pushed 2026-02-09"
---

# GWAS-MCP

A single MCP server that bundles gene, variant, protein-interaction, structure, pathway, and drug-target lookups across 14 public biological databases, so Claude can run a variant-to-target research workflow without wiring up each source separately.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [ZaEyAsa](https://github.com/zaeyasa/gwas-mcp) |
| **Availability** | GA — PyPI `gwas-mcp` v1.0.2 (2026-02-09) |
| **Pricing** | Free / OSS (MIT) — wraps public database APIs; no key documented |
| **Capabilities** | Read-only — queries public REST APIs (UniProt, Ensembl, NCBI, ClinVar, GWAS Catalog, GTEx, STRING, InterPro, AlphaFold, PDB, KEGG, Open Targets, PharmGKB, OMIM) |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — PyPI gwas-mcp 1.0.2 MIT resolves but canonical owner is muslus/gwas-mcp, single-maintainer/stale |

## How to install

Requires Python 3.10+. Install the package first, then register the stdio server.

- **Install the package** (both clients need this):
  ```
  pip install gwas-mcp
  ```
- **Claude Code** — direct MCP add (stdio; Claude Code launches `python -m gwas_mcp.server` itself — do not run it separately):
  ```
  claude mcp add --transport stdio gwas-bioinformatics -- python -m gwas_mcp.server
  ```
- **Claude Desktop** — add to `claude_desktop_config.json` (locations: macOS `~/Library/Application Support/Claude/claude_desktop_config.json`, Linux `~/.config/Claude/claude_desktop_config.json`, Windows `%APPDATA%\Claude\claude_desktop_config.json`), then restart Claude Desktop:
  ```json
  {
    "mcpServers": {
      "gwas-bioinformatics": {
        "command": "python",
        "args": ["-m", "gwas_mcp.server"]
      }
    }
  }
  ```

No API key is documented for any of the wrapped databases. Responses are cached for one hour.

## What it does

30+ tools grouped into six areas:

- **Protein & gene** — `search_uniprot`, `get_protein_details`, `search_ncbi_gene`, `search_ensembl_gene`, `get_variant_info`, `get_interpro_domains`
- **Clinical & variants** — `search_clinvar`, `get_clinvar_variant`, `annotate_snps`, `query_gwas_catalog`, `get_eqtl_data`
- **Protein interactions** — `get_protein_interactions`, `get_interaction_network`, `get_functional_enrichment`
- **Structure & pathways** — `get_alphafold_structure`, `search_alphafold`, `search_pdb_structures`, `get_pdb_structure`, `search_kegg_pathway`, `get_kegg_pathway`, `get_gene_pathways`
- **Drug discovery** — `get_drug_targets`, `get_disease_associations`, `search_open_targets`, `search_pharmgkb`, `get_drug_gene_interactions`
- **Genetic diseases** — `search_omim`, `get_gene_diseases`

**Primary use cases**: GWAS variant annotation, variant-to-gene-to-target prioritization, gene/disease association lookup, cross-database evidence gathering.

## Notes

A convenience aggregator: each underlying database is also catalogued here as its own dedicated entry (Ensembl, ClinVar, GWAS Catalog, STRING, AlphaFold, KEGG, Open Targets, GtoPdb, UniProt). Use GWAS-MCP when you want one install covering the whole variant-to-target chain; use the individual entries when you need a single source's full feature surface. Read-only; smart caching (1-hour TTL) reduces repeated API calls. OMIM coverage is via public search endpoints, not the licensed OMIM API.

## Sources

- [`zaeyasa/gwas-mcp`](https://github.com/zaeyasa/gwas-mcp)
- [PyPI: gwas-mcp](https://pypi.org/project/gwas-mcp/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=gwas-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fgwas-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
