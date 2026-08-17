---
title: PBMCpedia MCP
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: MCPmed
availability: Beta
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology]
last_verified: 2026-08-15
verification: works
verified_on: 2026-08-17
reviewed_on: 2026-08-17
security: caution
security_on: 2026-08-17
security_note: "MCPmed org confirmed not archived, BSD-3-Clause via GitHub license API; port and tool names confirmed against server.ts and README, but repo is stale (last push 2026-02-25) and low-traffic (0 stars)"
summary: "Query PBMCpedia's harmonized PBMC single-cell atlas — per-cell-type expression, DEGs, pathways and antibody chains — filtered by sex, age and disease."
---

# PBMCpedia MCP

Query [PBMCpedia](https://web.ccb.uni-saarland.de/pbmcpedia/), a harmonized peripheral-blood-mononuclear-cell scRNA-seq atlas, for gene expression, differential expression and pathway results by cell type, sex, age group and disease.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [MCPmed](https://github.com/MCPmed/PBMCpediaMCP) (Chair for Clinical Bioinformatics, Saarland University) |
| **Availability** | Beta — last upstream commit 2026-02-25 |
| **Pricing** | Free / OSS — BSD-3-Clause; the backing PBMCpedia web service is public and needs no API key |
| **Capabilities** | Read-only — six query tools against the public PBMCpedia API |
| **Verified** | works · 2026-08-17 |
| **Security** | caution · 2026-08-17 — BSD-3-Clause and provenance confirmed; repo stale (last push 2026-02-25) and low-traffic |

## How to install

Requires Node.js with npm (the server is TypeScript, built on the TypeScript MCP SDK). There is **no published npm package** — install from a clone.

1. **Clone and install dependencies:**
   ```
   git clone https://github.com/MCPmed/PBMCpediaMCP
   cd PBMCpediaMCP
   npm install
   ```

2. Pick **one** of the two transports below.

### Option A — stdio (Claude launches the server)

- **Claude Code:**
  ```
  claude mcp add --transport stdio pbmcpedia -- npm start -- --transport stdio
  ```
  Then open `~/.claude.json`, find the `pbmcpedia` entry, and add a `"cwd"` key pointing at your clone — `claude mcp add` has no `--cwd` flag, and without it `npm start` runs in the wrong directory and the server will not launch:
  ```json
  "pbmcpedia": {
    "type": "stdio",
    "command": "npm",
    "args": ["start", "--", "--transport", "stdio"],
    "cwd": "/path/to/PBMCpediaMCP"
  }
  ```
  (replace `/path/to/PBMCpediaMCP` with the absolute path of your clone — e.g. `/Users/you/repos/PBMCpediaMCP`, or the output of `pwd` if you are still inside it from step 1).

- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "pbmcpedia": {
        "command": "npm",
        "args": ["start", "--", "--transport", "stdio"],
        "cwd": "/path/to/PBMCpediaMCP"
      }
    }
  }
  ```
  Fully quit and relaunch Claude Desktop after editing.

With stdio, do **not** run the server yourself — Claude starts and stops the process.

### Option B — HTTP (you run the server)

Start it and leave it running in its own terminal:

```
npm start
```

Then, in Claude Code:

```
claude mcp add --transport http pbmcpedia http://localhost:3002/mcp
```

3002 is the default port in `server.ts`; if you override it, use your port. Claude Desktop has no native HTTP transport — use Option A there, or proxy through `mcp-remote`.

## What it does

Six tools, read from `server.ts` (the README does not enumerate them):

- `getMetaData` — cohort metadata, optionally summarized, filtered by `sex` and/or `disease`
- `getExpressionPerGene` — expression for named genes, at fine or broad cell-type granularity, paginated
- `getDEGs` — differentially expressed genes filtered by age group, sex, disease and cell type, with ordering and pagination
- `getDEperCellType` — differential expression for specific genes within a cell type
- `getPathways` — pathway results with the same cohort and cell-type filters
- `getAntibodyChains` — antibody chains for a given clone

**Primary use cases**: checking whether a gene is differentially expressed in a specific blood cell type in a given disease, sizing cohorts before an experiment, cross-referencing pathway signals across PBMC subsets.

## Notes

PBMCpedia harmonizes published PBMC scRNA-seq studies under a unified reference mapping and cell-type annotation, and includes TCR/BCR and CITE-seq surface-protein layers alongside gene expression — which is why the server exposes an antibody-chain tool next to the expression tools.

The upstream README documents the install and transport wiring but not the tool surface; the tool list above was read directly from the repository's `server.ts` on 2026-08-15 and may drift if upstream changes.

The repository is new and low-traffic (0 stars). It is one of a family of MCPmed servers over bioinformatics web resources — see also [NCBI GEO](geo-database.html), [Allen Brain Atlas](allenbrain.html) and [UCSC Cell Browser MCP](ucsc-cell-browser.html).

## Sources

- [`MCPmed/PBMCpediaMCP`](https://github.com/MCPmed/PBMCpediaMCP)
- [PBMCpedia web service](https://web.ccb.uni-saarland.de/pbmcpedia/)
- [PBMCpedia: a harmonized PBMC scRNA-seq database (*Nucleic Acids Research*)](https://doi.org/10.1093/nar/gkaf1245)
- [MCPmed (*Brief Bioinform* 2026;27(1):bbag076)](https://academic.oup.com/bib/article/27/1/bbag076/8495038)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pbmcpedia&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpbmcpedia.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
