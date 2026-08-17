---
title: CAN-IMMUNE
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Li/Purcell Lab, Monash University
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Translational Medicine]
last_verified: 2026-08-15
verification: works
verified_on: 2026-08-17
reviewed_on: 2026-08-17
security: caution
security_on: 2026-08-17
security_note: "hosted endpoint answers 405/406 to a browser-shaped GET (expected, live); server code MIT but repo is new (2 commits, 0 stars) and underlying data is derived from COSMIC/DepMap under their own terms"
summary: Hosted MCP server over the CAN-IMMUNE cancer neoantigen database — mutant peptides, cell lines, tissues, and MHC-I binding predictions.
---

# CAN-IMMUNE

A hosted, read-only MCP server that queries CAN-IMMUNE, a cancer neoantigen catalogue of ~4.49 million unique mutant peptides annotated with cell line, tissue, cancer type, and predicted MHC class I binding.

| | |
|---|---|
| **Type** | MCP server (remote, Streamable HTTP) |
| **Supplier** | [Li/Purcell Lab, Monash University](https://canelib.erc.monash.edu.au/) |
| **Availability** | GA — v1.0.0 published to the MCP Registry 2026-08-10 as `io.github.sanjaysgk/can-immune`, status active |
| **Pricing** | Free / OSS (server code MIT); anonymous access at a light rate limit, higher quota after Google sign-in |
| **Capabilities** | Read-only — parameterized, row-capped, time-bounded queries; no writes |
| **Verified** | works · 2026-08-17 |
| **Security** | caution · 2026-08-17 — endpoint live (405/406 to browser GET), MIT server code, but new low-traffic repo over COSMIC/DepMap-derived data |

## How to install

- **Claude Code** — remote MCP add (no local install, no API key):
  ```
  claude mcp add --transport http canelib https://canelib.erc.monash.edu/mcp
  ```
- **Claude.ai** — **Settings → Connectors → Add custom connector**, paste `https://canelib.erc.monash.edu/mcp`, then **Connect**.
- **Claude Desktop** — Desktop has no native HTTP transport, so proxy the remote server through `mcp-remote` in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "canelib": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://canelib.erc.monash.edu/mcp"]
      }
    }
  }
  ```
  (**Unverified —** upstream documents Claude Code and Claude.ai only; the `mcp-remote` entry above is the standard Desktop proxy pattern for a Streamable-HTTP server, not a snippet published by the project.)

Nothing runs locally: the server is hosted by Monash, so there is no process to start or keep alive.

## What it does

Twelve read-only tools over the neoantigen catalogue:

- **Orientation** — `database_overview` (record counts and coverage), `list_tissues`, `list_cancer_types`.
- **Generic retrieval** — `search` and `fetch` (the pair ChatGPT-style connectors expect).
- **Genes** — `search_genes`, `get_gene`, `get_gene_mutations`.
- **Cell lines** — `search_cell_lines`, `get_cell_line`, `top_genes_in_cell_line`.
- **Immunology** — `get_mhc_binding`, returning predicted MHC class I binding for a mutant peptide against a cell line's HLA class I type.

Records are built from COSMIC and DepMap/CCLE mutations, with PubMed for literature context. Each mutation is represented as a 25-mer peptide centred on the mutated residue in both wild-type and mutant form, with anchor positions (2 and 9 of the relevant 9-mer window) surfaced; MHC-I binding is predicted with NetMHCpan (eluted-ligand mode) via the IEDB API. The database also reports which tissues and cell lines share an identical mutant peptide, so shared neoantigens can be prioritised over private ones.

**Primary use cases**: shared-neoantigen shortlisting for cancer vaccines, cell-line selection for immunopeptidomics experiments, HLA-aware triage of tumour mutations.

## Notes

Anonymous use is allowed at a light rate limit. Signing in with Google (OAuth 2.1) raises the quota — academic domains (`.edu`, `.edu.au`, `.ac.*`) get the highest tier, other verified emails a standard tier; the project states sign-in reads only the verified email address to set the rate and stores nothing further.

Two hostnames are in circulation: the MCP endpoint and connector documentation are served from `canelib.erc.monash.edu`, while the browsable database UI is at `canelib.erc.monash.edu.au`. Use the `.edu` form in the install command above, exactly as published.

The server code is MIT-licensed, but the underlying content is derived from COSMIC and DepMap/CCLE — check those sources' own terms before redistributing extracted data or using it commercially. MHC-I binding values are predictions, not measured immunogenicity; binding is necessary but not sufficient for a neoantigen to be immunogenic, so treat scores as a filter rather than a result. The repository is new (2 commits, 0 stars as of 2026-08-15) even though the hosted service and its Registry entry are live, and no database publication was locatable — the site asks that CAN-IMMUNE be cited but does not yet give a reference.

For prediction-side workflows rather than database lookup, see [MHC binding prediction](mhc-binding-prediction.html), [MHC class II prediction](mhc-class-ii-prediction.html), [epitope prediction](epitope-prediction.html), and [neoantigen prediction](neoantigen-prediction.html).

## Sources

- [`sanjaysgk/can-immune-mcp`](https://github.com/sanjaysgk/can-immune-mcp)
- [CAN-IMMUNE AI connector setup](https://canelib.erc.monash.edu/connector)
- [CAN-IMMUNE database](https://canelib.erc.monash.edu.au/)
- [MCP Registry entry — `io.github.sanjaysgk/can-immune`](https://registry.modelcontextprotocol.io/v0/servers?search=can-immune)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=can-immune&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcan-immune.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
