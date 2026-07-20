---
title: GlyGen MCP Server
parent: All tools
grand_parent: Catalog
nav_order: 1
tool_type: MCP server
supplier: GlyGen
availability: Beta
tool_categories: [All]
last_verified: 2026-07-15
summary: First-party remote MCP server over GlyGen's integrated glycan, glycoprotein, biomarker, and disease data — protein, site, glycan, biomarker, and disease summaries.
flagged: upstream repo declares no LICENSE (as of 2026-07-15)
verification: degraded
verified_on: 2026-07-20
verification_note: "self-host repo glygener/glygen-mcp-server resolves and is current (pushed 2026-07-15) but the hosted mcp.glygen.org/mcp endpoint returned 503 this run so boot is unverified"
security: caution
security_on: 2026-07-20
security_note: "provenance matches GlyGen (glygener) but the wrapper repo has no LICENSE (GitHub license null) and is single-maintainer/0-star; underlying GlyGen data is public read-only"
---

# GlyGen MCP Server

Remote MCP server maintained by the GlyGen project that exposes its integrated carbohydrate and glycoconjugate knowledgebase — glycans, glycoproteins, glycosylation sites, biomarkers, and disease associations — to Claude.

| | |
|---|---|
| **Type** | MCP server (remote, streamable HTTP) |
| **Supplier** | [GlyGen](https://www.glygen.org/) |
| **Availability** | Beta — remote endpoint live; source repo [`glygener/glygen-mcp-server`](https://github.com/glygener/glygen-mcp-server) last updated 2026-06-25 |
| **Pricing** | **Unverified —** GlyGen data is freely accessible, but the MCP wrapper repo declares no LICENSE file, so redistribution terms are unstated |
| **Capabilities** | Read-only — data lookup/summary queries |
| **Verified** | degraded · 2026-07-20 — self-host repo current but hosted endpoint returned 503 this run |
| **Security** | caution · 2026-07-20 — provenance matches GlyGen but wrapper repo has no LICENSE, single-maintainer |

## How to install

- **Claude.ai** — Settings → Connectors → **Add custom connector**. Name it `Glygen MCP Server`, server URL `https://mcp.glygen.org/mcp`. (Team/Enterprise: an admin adds it under Admin settings → Connectors.)
- **Claude Code** — direct remote MCP add:
  ```
  claude mcp add --transport http glygen https://mcp.glygen.org/mcp
  ```
  This is a long-lived hosted service — nothing to run locally. After adding, run `/mcp` to confirm the server is connected.
- **Claude Desktop** — Claude Desktop has no native HTTP transport, so register the remote endpoint through the `mcp-remote` proxy in `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "glygen": {
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://mcp.glygen.org/mcp"]
      }
    }
  }
  ```
  (Requires Node.js so `npx` is available.)
- **Self-host (optional)** — clone [`glygener/glygen-mcp-server`](https://github.com/glygener/glygen-mcp-server) and build the Docker container with `python3 create_mcp_container.py -s dev` (Linux VM; the README documents a `systemd` unit for persistence). Only needed if you want to run your own instance rather than use the hosted endpoint above.

## What it does

Five read-only summary tools over GlyGen's integrated datasets:

- `get_protein_summary` — glycoprotein record summary (keyed by UniProt accession)
- `get_site_summary` — glycosylation site details for a protein
- `get_glycan_summary` — glycan structure/composition record (GlyTouCan-linked)
- `get_biomarker_summary` — biomarker record summary
- `get_disease_summary` — disease association summary

GlyGen integrates and harmonizes carbohydrate/glycoconjugate data from UniProtKB, GlyTouCan, UniCarbKB, and other international sources.

**Primary use cases**: Glycan and glycoprotein lookup, glycosylation-site queries, glycan-disease/biomarker association retrieval.

## Notes

Remote streamable-HTTP endpoint (`https://mcp.glygen.org/mcp`); no API key documented. GlyGen also exposes a REST API (`api.glygen.org`) and a SPARQL endpoint (`sparql.glygen.org`) for programmatic access outside Claude.

**License caveat**: the `glygen-mcp-server` GitHub repo has no LICENSE file (the GitHub license field is null as of 2026-07-15), so the redistribution terms of the wrapper are unverified — pricing above reflects this rather than asserting Free / OSS. The underlying GlyGen data is publicly and freely accessible.

Surfaced from user request [#48](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/48) (@goodb). The request suggested the `General-Purpose Utilities` shelf, but GlyGen is a life-science data resource spanning glycochemistry, glycobiology, and biomarker/disease data, so it is tagged `All`.

## Sources

- [GlyGen](https://www.glygen.org/)
- [`glygener/glygen-mcp-server`](https://github.com/glygener/glygen-mcp-server)
- [GlyGen resources / APIs](https://www.glygen.org/resources/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=glygen&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fglygen.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
