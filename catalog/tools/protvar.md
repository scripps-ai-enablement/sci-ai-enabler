---
title: ProtVar MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: EMBL-EBI (UniProt)
availability: Alpha
tool_categories: [Translational Medicine, Molecular and Cellular Biology, Integrative Structural and Computational Biology]
last_verified: 2026-08-19
summary: First-party EMBL-EBI MCP server over ProtVar — maps missense variants onto UniProt coordinates and returns AlphaMissense, EVE, ESM1b, popEVE, FoldX, pockets, interactions and population data keyed by accession and residue.
flagged: "upstream repo declares no LICENSE (as of 2026-08-19); hosted endpoint https://www.ebi.ac.uk/ProtVar/mcp is live but undocumented in the README, which lists only dev/int"
verification: works
verified_on: 2026-08-19
verification_note: "hosted https://www.ebi.ac.uk/ProtVar/mcp answered initialize (MCP 2025-06-18, serverInfo protvar-mcp 0.0.1) and tools/list (10 tools) this run; mapVariants returned the expected AlphaMissense values for P01008/P38484 test variants"
security: caution
security_on: 2026-08-19
security_note: "provenance matches EMBL-EBI (ebi-uniprot org, same org as protvar-be/protvar-fe) but the repo has no LICENSE (GitHub license null), 0 stars/0 forks, last push 2026-05-30, version 0.0.1-SNAPSHOT; read-only over public ProtVar data, no auth"
---

# ProtVar MCP Server

MCP server from the UniProt team at EMBL-EBI over [ProtVar](https://www.ebi.ac.uk/ProtVar/), which maps human missense variation onto **UniProt protein coordinates** and contextualises it with pathogenicity predictors, structural predictions and population data.

| | |
|---|---|
| **Type** | MCP server (remote, streamable HTTP, stateless) |
| **Supplier** | [EMBL-EBI / UniProt](https://www.ebi.ac.uk/ProtVar/) — first-party ([`ebi-uniprot/protvar-mcp`](https://github.com/ebi-uniprot/protvar-mcp)) |
| **Availability** | Alpha — `0.0.1-SNAPSHOT`, last push 2026-05-30; hosted endpoint live but not yet documented upstream |
| **Pricing** | **Unverified —** ProtVar and its data are freely accessible with no auth, but the MCP wrapper repo declares no LICENSE file, so redistribution terms are unstated |
| **Capabilities** | Read-only — variant mapping, annotation and prediction lookup |
| **Verified** | works · 2026-08-19 — hosted endpoint answered `initialize` + `tools/list` (10 tools); `mapVariants` returned expected AlphaMissense values |
| **Security** | caution · 2026-08-19 — EBI provenance, but no LICENSE, 0-star, `0.0.1-SNAPSHOT` |

## How to install

- **Claude Code** — remote MCP add against the hosted endpoint:
  ```
  claude mcp add --transport http protvar https://www.ebi.ac.uk/ProtVar/mcp
  ```
  Then run `/mcp` to confirm the server is connected. The README documents only the `wwwdev`/`wwwint` deployments, but the production path above answered MCP `initialize` and `tools/list` on 2026-08-19.
- **Claude.ai** — Settings → Connectors → **Add custom connector**, server URL `https://www.ebi.ac.uk/ProtVar/mcp`.
- **Claude Desktop** — no native HTTP transport, so proxy it in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "protvar": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://www.ebi.ac.uk/ProtVar/mcp"]
      }
    }
  }
  ```
- **Self-host (optional)** — Java 21 + Maven 3.9+; `mvn spring-boot:run -Dspring-boot.run.profiles=dev` serves `http://localhost:8081/ProtVar/mcp`. Note the shipped `dev`/`int` profiles target `wwwdev`/`wwwint`, not production.

## What it does

Ten read-only tools, all keyed by **UniProt accession + residue** rather than by genomic coordinate:

- `mapVariant` / `mapVariants` — map one or many variants to protein positions with full annotations. Accepts VCF, HGVS, rsID **or protein-level** notation (`P04637 R175H`); `mapVariants` takes a newline-delimited list, so a cohort is one call. Returns per-isoform records flagged `canonical`, each carrying `amScore` (AlphaMissense), `popEveScore`, CADD, the derived genomic coordinate, and a reference-residue check.
- `getFunction` — UniProt features (domains, sites) at a residue
- `getPopulation` — co-located variants, ClinVar/dbSNP xrefs, `clinicalSignificances`, allele frequencies
- `getStructure` — position within experimental and predicted structures
- `getFoldx` — FoldX ΔΔG stability predictions
- `getPockets` — predicted ligand-binding pockets near a residue
- `getInteractions` — predicted protein–protein interaction interfaces
- `searchVariants` — filter ProtVar variants by structural/functional criteria
- `semanticSearch` — natural-language search over ProtVar function descriptions

**Primary use cases**: missense-variant interpretation in protein coordinates; AlphaMissense/EVE/ESM1b pathogenicity lookup that is guaranteed to be for the accession you asked about; structural and interface context for a residue.

## Notes

**Why the accession keying matters.** AlphaMissense is defined per UniProt accession and residue. Reaching it through a *genomic* variant lookup instead can silently return a different transcript's residue or a different accession's score — one genomic record carries an annotation per transcript, and aggregators surface only one of them. `IFNGR2 p.T70N` matches two genomic records, one of which is canonically Thr149Asn; and for `SERPINC1` the first entry of dbNSFP's isoform-aligned array is the TrEMBL fragment `Q8TCE1`, not Swiss-Prot `P01008`. Because ProtVar answers per accession and flags the `canonical` isoform, it sidesteps both. It also validates the reference residue and says so — `P01008 220 R C` returns *"User input reference amino acid (Arg) does not match the UniProt sequence (Lys) at position 220"*.

Two things to code against: on a reference mismatch it still returns a **position-only** score, so check `messages` for `type: "WARN"` before trusting `amScore`; and `getPopulation`'s `clinicalSignificances` aggregates several sources, so keep only calls whose `sources` include ClinVar (an Ensembl-only call is not a ClinVar submission).

**REST alternative.** The same data is available without MCP at `https://www.ebi.ac.uk/ProtVar/api` ([Swagger UI](https://www.ebi.ac.uk/ProtVar/api/swagger-ui/index.html); the OpenAPI document is at `/ProtVar/api/docs`, not the springdoc default `/v3/api-docs`). A pinned pipeline may prefer the REST surface for re-runnability — that is what [Interpret variants that gain or lose glycosylation sites](../../recipes/items/interpret-glycosylation-altering-variants.html) does.

**License caveat**: [`ebi-uniprot/protvar-mcp`](https://github.com/ebi-uniprot/protvar-mcp) has no LICENSE file (GitHub `license` null as of 2026-08-19), so the wrapper's redistribution terms are unverified — hence `Unverified —` on Pricing rather than asserting Free / OSS. ProtVar itself is an EMBL-EBI service and AlphaMissense is CC BY 4.0.

## Sources

- [ProtVar](https://www.ebi.ac.uk/ProtVar/)
- [`ebi-uniprot/protvar-mcp`](https://github.com/ebi-uniprot/protvar-mcp) · [tool reference](https://github.com/ebi-uniprot/protvar-mcp/blob/main/docs/TOOLS.md)
- [ProtVar API Swagger UI](https://www.ebi.ac.uk/ProtVar/api/swagger-ui/index.html) · [`ebi-uniprot/protvar-be`](https://github.com/ebi-uniprot/protvar-be)
- [ProtVar: mapping and contextualizing human missense variation](https://doi.org/10.1093/nar/gkae413) (*Nucleic Acids Research*)
- [AlphaMissense data integration at EMBL-EBI](https://www.ebi.ac.uk/about/news/technology-and-innovation/alphamissense-data-integration/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=protvar&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fprotvar.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
