---
title: AlphaFold MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Augmented Nature
availability: GA
tool_categories: [Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Drug Repurposing and Discovery]
last_verified: 2026-06-20
claude_science: true
summary: MCP server exposing the EBI AlphaFold Protein Structure Database for structure retrieval, pLDDT analysis, comparison, and PyMOL/ChimeraX export.
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "repo LICENSE is a restrictive personal non-commercial grant (GitHub NOASSERTION) not the MIT the page claimed — fixed in-page; EBI AlphaFold API is public read-only"
---

# AlphaFold MCP Server

MCP wrapper over the EBI AlphaFold Protein Structure Database — predicted structures for any UniProt protein, with built-in confidence analysis and visualization export.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Augmented Nature](https://github.com/Augmented-Nature/AlphaFold-MCP-Server) (community OSS) |
| **Availability** | GA — active, ~25 tools |
| **Pricing** | Source under a restrictive personal, non-commercial license (no redistribution/modification/commercial use without permission); EBI AlphaFold DB is free for academic use |
| **Capabilities** | Read-only |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — repo LICENSE is a restrictive non-commercial grant (GitHub NOASSERTION) not MIT; EBI AlphaFold API public read-only |

## How to install

<!-- alt-install:sciagent -->
- **Also packaged in the SciAgent-Skills collection** ([jaechang-hits](https://github.com/jaechang-hits/SciAgent-Skills) (community OSS, CC BY 4.0)): clone [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) and run `/plugin install sciagent-skills` in Claude Code (or copy `skills/structural-biology-drug-discovery/alphafold-database-access` into `~/.claude/skills/`).
<!-- /alt-install:sciagent -->
```
git clone https://github.com/Augmented-Nature/AlphaFold-MCP-Server
cd AlphaFold-MCP-Server
npm install
npm run build
```

Then add to `claude_desktop_config.json` (replace `/path/to/AlphaFold-MCP-Server` with the absolute path of your clone — e.g., `/Users/you/repos/AlphaFold-MCP-Server`):

```json
{
  "mcpServers": {
    "alphafold-server": {
      "command": "node",
      "args": ["/path/to/AlphaFold-MCP-Server/build/index.js"]
    }
  }
}
```

For Claude Code, the equivalent registration is:

```
claude mcp add --transport stdio alphafold-server -- node /path/to/AlphaFold-MCP-Server/build/index.js
```

## What it does

About 25 tools across:

- **Retrieval**: `get_structure`, `download_structure` (PDB / CIF / BCIF / JSON by UniProt ID)
- **Confidence**: `get_confidence_scores`, `analyze_confidence_regions` (pLDDT)
- **Batch / comparative**: `batch_structure_info` (up to 50 proteins), `compare_structures`, `find_similar_structures`
- **Visualization export**: `export_for_pymol`, `export_for_chimerax`

**Primary use cases**: Pull AlphaFold predictions by UniProt for a target list, flag low-pLDDT regions before docking or modelling, prepare PyMOL / ChimeraX sessions for analysis.

## Notes

**Claude Science:** This resource is offered inside Anthropic's **Claude Science** via the *Structures & Interactions* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Node/stdio transport. No auth — hits `https://alphafold.ebi.ac.uk/api/`. Complements the PDB MCP server (experimental structures) by covering predictions.

## Sources

- [`Augmented-Nature/AlphaFold-MCP-Server`](https://github.com/Augmented-Nature/AlphaFold-MCP-Server)
- [mcpservers.org listing](https://mcpservers.org/servers/Augmented-Nature/AlphaFold-MCP-Server)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=alphafold&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Falphafold.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
