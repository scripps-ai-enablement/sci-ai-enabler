---
title: Certus Drug Information MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Aditya Damerla (zesty-genius128)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-06-28
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "repo resolves MIT (GitHub API now reports canonical owner aditya-damerla128/Certus_server; old zesty-genius128 path redirects) but is stale (last push 2025-09-03) and single-maintainer/0-star; read-only openFDA, no advisories"
summary: MIT openFDA MCP server focused on drug shortages, recalls, labels, and adverse events — with a zero-install hosted endpoint and batch analysis across up to 25 drugs.
---

# Certus Drug Information MCP Server

MCP server giving Claude live access to U.S. FDA drug data via the openFDA APIs, with an emphasis on drug-shortage tracking, recalls, labeling, and adverse-event reporting.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Aditya Damerla (zesty-genius128)](https://github.com/zesty-genius128/Certus_server) |
| **Availability** | GA — runnable from source (Node.js 18+) or via the public hosted endpoint |
| **Pricing** | Free / OSS (MIT). No API key required; an optional free openFDA key raises rate limits |
| **Capabilities** | Read-only — openFDA drug-endpoint queries |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — MIT repo resolves (canonical aditya-damerla128/Certus_server; old owner path redirects) but stale 2025-09-03, single-maintainer; read-only openFDA, no advisories |

## How to install

This server is offered two ways: a **hosted** remote endpoint (zero install, proxied via `mcp-remote`) and a **local** stdio process you run from a clone.

- **Claude Code** — point at the hosted endpoint (zero install):

  ```
  claude mcp add --transport http certus https://certus.opensource.mieweb.org/mcp
  ```

- **Claude Desktop** — hosted endpoint via the `mcp-remote` proxy (Claude Desktop has no native HTTP transport). Add to `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "Certus": {
        "command": "npx",
        "args": ["mcp-remote", "https://certus.opensource.mieweb.org/mcp"]
      }
    }
  }
  ```

  Restart Claude Desktop after editing the config. Config file locations: macOS `~/Library/Application Support/Claude/claude_desktop_config.json`; Windows `%APPDATA%\Claude\claude_desktop_config.json`.

- **Local (self-host)** — clone, install, and run the stdio server:

  ```
  git clone https://github.com/zesty-genius128/Certus_server
  cd Certus_server
  npm install
  ```

  Then register it with Claude Code (stdio — Claude launches the process itself, so no separate long-running terminal is needed; replace `/path/to/Certus_server` with the absolute path of your clone — e.g., `$(pwd)` if you are still inside it from the previous step):

  ```
  claude mcp add --transport stdio certus -- node /path/to/Certus_server/official-mcp-server.js
  ```

  Or the equivalent Claude Desktop entry:

  ```json
  {
    "mcpServers": {
      "Certus": {
        "command": "node",
        "args": ["/path/to/Certus_server/official-mcp-server.js"],
        "env": { "OPENFDA_API_KEY": "your_api_key_here" }
      }
    }
  }
  ```

  (`OPENFDA_API_KEY` is optional — omit it to use the default rate limit, or get a free key at [open.fda.gov/apis/authentication](https://open.fda.gov/apis/authentication/).)

## What it does

Exposes eight tools over the openFDA drug endpoints:

- **search_drug_shortages** — query the FDA drug-shortage database by generic or brand name.
- **get_medication_profile** — combined FDA label and current shortage status for a drug.
- **search_drug_recalls** — FDA enforcement-database recall lookups.
- **get_drug_label_info** — FDA-approved prescribing information.
- **analyze_drug_shortage_trends** — historical shortage-pattern analysis (1–60 months).
- **search_adverse_events** — FAERS adverse-event reports.
- **search_serious_adverse_events** — FAERS reports filtered to serious outcomes (hospitalization, death, disability).
- **batch_drug_analysis** — assess shortages, recalls, and risk across up to 25 drugs in one call.

**Primary use cases**: drug-shortage monitoring, formulary risk assessment, recall and pharmacovigilance review, batch safety screening across a drug list.

## Notes

The hosted endpoint is convenient for evaluation; self-host for production or controlled-access workflows. The author notes a medical-safety caching policy — recalls and serious adverse events are fetched fresh on every call while other data is cached. Coverage is openFDA drug endpoints only (no device or food endpoints). For a drug-endpoint server with NDC resolution and manufacturer lookups, see [OpenFDA MCP Server (ythalorossy)](openfda.html); for a multi-source biomedical server, see [BioMCP](biomcp.html).

## Sources

- [`zesty-genius128/Certus_server`](https://github.com/zesty-genius128/Certus_server)
- [Certus hosted MCP endpoint](https://certus.opensource.mieweb.org/mcp)
- [openFDA API authentication / rate limits](https://open.fda.gov/apis/authentication/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=certus&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcertus.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
