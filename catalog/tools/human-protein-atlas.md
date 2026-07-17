---
title: Human Protein Atlas MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Augmented Nature
availability: GA
tool_categories: [Immunology and Microbiology, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-06-13
claude_science: true
summary: "Query the Human Protein Atlas — tissue/blood/brain expression, subcellular localization, cancer markers, and antibody validation/staining data."
---

# Human Protein Atlas MCP Server

Community MCP server wrapping the Human Protein Atlas, exposing protein expression, subcellular localization, cancer pathology, and antibody validation/staining data to Claude.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Augmented Nature](https://github.com/Augmented-Nature/ProteinAtlas-MCP-Server) (Moudather Chelbi) |
| **Availability** | GA |
| **Pricing** | Free / OSS (MIT). No API key required — queries the public proteinatlas.org. |
| **Capabilities** | Read-only — Human Protein Atlas queries |

## How to install

This server is not published to npm; install from source.

- **Prerequisite** — Node.js 18+ and git.
- **Clone and build:**

  ```
  git clone https://github.com/Augmented-Nature/ProteinAtlas-MCP-Server/
  cd ProteinAtlas-MCP-Server/proteinatlas-server
  npm install
  npm run build
  ```

  (The upstream README writes `cd proteinatlas-server`; the server lives in the `proteinatlas-server/` subdirectory of the cloned `ProteinAtlas-MCP-Server` repo — `cd` into that path. Confirm `build/index.js` exists after `npm run build`.)

- **Claude Code** — register the built server (replace `/path/to` with the absolute path of your clone — e.g., `$(pwd)/build/index.js` if you're still in `proteinatlas-server` from the previous step):

  ```
  claude mcp add --transport stdio proteinatlas -- node /path/to/ProteinAtlas-MCP-Server/proteinatlas-server/build/index.js
  ```

- **Claude Desktop** — add to `claude_desktop_config.json` (same absolute path):

  ```json
  {
    "mcpServers": {
      "proteinatlas": {
        "command": "node",
        "args": ["/path/to/ProteinAtlas-MCP-Server/proteinatlas-server/build/index.js"]
      }
    }
  }
  ```

  Both Claude Code and Claude Desktop launch the process themselves over stdio — you do not keep a server running in a separate terminal.

## What it does

Fourteen read-only tools over the Human Protein Atlas:

- **Search/retrieval** — `search_proteins`, `get_protein_info` (by gene symbol), `get_protein_by_ensembl`.
- **Expression** — `get_tissue_expression`, `search_by_tissue`, `get_blood_expression`, `get_brain_expression`.
- **Subcellular localization** — `get_subcellular_location`, `search_by_subcellular_location`.
- **Pathology/cancer** — `get_pathology_data`, `search_cancer_markers`.
- **Advanced** — `advanced_search` (multi-filter), `batch_protein_lookup` (up to 100 proteins), `compare_expression_profiles` (2–10 proteins).

Antibody validation and immunostaining data are returned through the protein-info and tissue-expression tools.

**Primary use cases**: Antibody validation lookup, tissue/single-cell expression profiling, cancer prognostic-marker discovery.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Protein Annotation* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

License is MIT. No API key or account required. The server queries the public Human Protein Atlas; respect HPA's data-usage terms for downstream redistribution. Tool list and install steps verified against the upstream README 2026-06-13.

## Sources

- [`Augmented-Nature/ProteinAtlas-MCP-Server`](https://github.com/Augmented-Nature/ProteinAtlas-MCP-Server)
- [Human Protein Atlas](https://www.proteinatlas.org)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=human-protein-atlas&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fhuman-protein-atlas.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
