---
title: Ensembl MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: effieklimi
availability: GA
tool_categories: [Drug Repurposing and Discovery, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine]
last_verified: 2026-06-11
claude_science: true
summary: MCP server over the Ensembl REST API for gene/transcript lookup, sequence retrieval, variant consequences, comparative genomics, and assembly lift-over.
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "provenance matches effieklimi/ensembl-mcp-server MIT via GitHub API, read-only public Ensembl REST API no credentials, featured Claude Science Genomes connector"
---

# Ensembl MCP Server

An MCP server that exposes the Ensembl REST API so Claude can look up genes and transcripts, fetch sequences, interpret variants, and run comparative-genomics queries from natural language.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [effieklimi](https://github.com/effieklimi/ensembl-mcp-server) |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT). Ensembl REST API needs no key; the Smithery installer path requires a free Smithery key. |
| **Capabilities** | Read-only — queries the public Ensembl REST API |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — provenance matches effieklimi/ensembl-mcp-server, MIT, read-only public Ensembl REST API no credentials, featured Claude Science Genomes connector |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/genomics-bioinformatics/databases/ensembl-database` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
The server is a TypeScript project run over stdio; it is **not** published to npm as a standalone package, so install it via Smithery (upstream-recommended) or a local clone/build.

- **Either client — via Smithery** (upstream-recommended; requires a free Smithery key; replace `your-smithery-key` with the key from your Smithery dashboard):
  ```
  npx -y @smithery/cli@latest install @effieklimi/ensembl-mcp-server --client claude --key your-smithery-key
  ```
- **Local clone/build** (no npm package — build from source, then register the run script):
  ```
  git clone https://github.com/effieklimi/ensembl-mcp-server.git
  cd ensembl-mcp-server
  npm install
  npm run build
  claude mcp add --transport stdio ensembl -- npm run start --prefix /path/to/ensembl-mcp-server
  ```
- **Claude Desktop** — register the same local build in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "ensembl": { "command": "npm", "args": ["run", "start", "--prefix", "/path/to/ensembl-mcp-server"] }
    }
  }
  ```

Requires Node.js. No Ensembl account or API key is needed for the REST API itself.

## What it does

Ten tools spanning the Ensembl REST API:

- `ensembl_lookup` — ID/symbol translation, cross-references, variant recoding
- `ensembl_sequence` — DNA, RNA, and protein sequence retrieval
- `ensembl_feature_overlap` — genes/transcripts/regulatory elements overlapping a region
- `ensembl_mapping` — coordinate conversion and assembly lift-over
- `ensembl_variation` — variant lookup, VEP consequences, phenotype mapping
- `ensembl_compara` — comparative genomics, homology, gene trees
- `ensembl_regulatory` — regulatory features, binding matrices, annotations
- `ensembl_protein_features` — protein domains and functional sites
- `ensembl_ontotax` — ontology and taxonomy traversal
- `ensembl_meta` — server metadata, species lists, release info

**Primary use cases**: Gene/transcript annotation lookup, sequence retrieval, variant consequence prediction, cross-species homology, genome-coordinate lift-over.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Genomes* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Read-only wrapper over the public Ensembl REST API; no write operations. A separate hosted HTTP variant exists via the Pipeworx gateway (`claude mcp add --transport http ensembl https://gateway.pipeworx.io/ensembl/mcp`), and `Augmented-Nature/Ensembl-MCP-Server` is an alternative implementation. The `effieklimi/ensembl-mcp-server` project is not published to npm, so use the Smithery installer or the local clone/build above rather than an `npx` package fetch.

## Sources

- [`effieklimi/ensembl-mcp-server`](https://github.com/effieklimi/ensembl-mcp-server)
- [Ensembl REST API](https://rest.ensembl.org/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=ensembl&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fensembl.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
