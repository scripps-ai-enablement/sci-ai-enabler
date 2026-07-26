---
title: OpenFDA MCP Server (cyanheads)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: cyanheads
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-07-26
summary: Apache-2.0 MCP server federating the full openFDA API — drugs, food, devices (510k/PMA), veterinary, recalls, and shortages — with a public HTTP instance.
---

# OpenFDA MCP Server (cyanheads)

Community MCP server that queries the U.S. FDA's public openFDA API across drugs, food, devices, veterinary products, and recalls — a broader surface than drug-only wrappers, including 510(k)/PMA device clearances and drug-shortage records.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [cyanheads](https://github.com/cyanheads/openfda-mcp-server) |
| **Availability** | GA — published to npm as `@cyanheads/openfda-mcp-server`; public HTTP instance live |
| **Pricing** | Free / OSS (Apache-2.0). An openFDA API key is optional — free tier is 1,000 requests/day, a free key raises it to 120,000/day |
| **Capabilities** | Read-only — federated openFDA queries across drug/food/device/animal/recall endpoints |

## How to install

An openFDA API key is optional but recommended for the higher rate limit — get one free at [open.fda.gov/apis/authentication](https://open.fda.gov/apis/authentication/).

- **Claude Code** — public hosted HTTP instance (no local runtime, nothing to keep running):

  ```
  claude mcp add --transport http openfda-mcp https://openfda.caseyjhand.com/mcp
  ```

- **Claude Code** — local stdio via `bunx` (Bun v1.3.0+; Claude Code launches the process itself, so this is not a long-lived service):

  ```
  claude mcp add-json openfda-mcp '{"command":"bunx","args":["@cyanheads/openfda-mcp-server@latest"],"env":{"MCP_TRANSPORT_TYPE":"stdio","OPENFDA_API_KEY":"your_api_key_here"}}'
  ```

  (Omit the `OPENFDA_API_KEY` entry to run keyless at the lower rate limit. Substitute `npx -y @cyanheads/openfda-mcp-server@latest` for `bunx …` if you use Node instead of Bun.)

- **Claude Desktop** — Desktop has no native HTTP transport, so use the local stdio entry in `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "openfda-mcp-server": {
        "type": "stdio",
        "command": "bunx",
        "args": ["@cyanheads/openfda-mcp-server@latest"],
        "env": {
          "MCP_TRANSPORT_TYPE": "stdio",
          "OPENFDA_API_KEY": "your_api_key_here"
        }
      }
    }
  }
  ```

  To point Desktop at the public HTTP instance instead, use an `mcp-remote` proxy entry (`"command": "npx", "args": ["-y", "mcp-remote", "https://openfda.caseyjhand.com/mcp"]`). Restart Claude Desktop after editing the config.

## What it does

Exposes 14 tools over the openFDA endpoints:

- **openfda_drug_profile** — consolidated FDA profile for a single drug (replaces several chained lookups).
- **openfda_search_adverse_events** — adverse-event reports across drugs, food, and devices (FAERS and equivalents).
- **openfda_search_animal_events** — veterinary adverse-event reports.
- **openfda_search_drug_shortages** — FDA drug-shortage records.
- **openfda_search_tobacco_reports** — problem reports for tobacco / e-cigarette products.
- **openfda_search_recalls** — enforcement and recall actions.
- **openfda_get_drug_label** — FDA drug labeling / package inserts.
- **openfda_search_drug_approvals** — Drugs@FDA approvals.
- **openfda_search_device_clearances** — 510(k) and PMA device clearances.
- **openfda_lookup_ndc** — National Drug Code directory lookup.
- **openfda_count_values** / **openfda_describe_fields** — aggregate field values and list searchable fields for any endpoint.
- **openfda_dataframe_query** / **openfda_dataframe_describe** — opt-in SQL (DuckDB / DataCanvas) over staged result sets.

**Primary use cases**: Pharmacovigilance and adverse-event review, medical-device 510(k)/PMA clearance lookup, drug-shortage and recall monitoring, label/approval research.

## Notes

stdio and Streamable HTTP transports; a public instance runs at `https://openfda.caseyjhand.com/mcp`. Optional `OPENFDA_API_KEY` env var raises the rate limit; the opt-in DataCanvas SQL surface needs `CANVAS_PROVIDER_TYPE=duckdb`. Community single-maintainer package — review the source before use.

Distinct from the drug-only [OpenFDA MCP Server (ythalorossy)](openfda.html) (7 tools, drug endpoints only): this server adds device clearances (510k/PMA), food, veterinary, tobacco, shortage, and recall endpoints plus a hosted HTTP instance. For a broader multi-source biomedical server, see [BioMCP](biomcp.html).

## Sources

- [`cyanheads/openfda-mcp-server`](https://github.com/cyanheads/openfda-mcp-server)
- [npm `@cyanheads/openfda-mcp-server`](https://www.npmjs.com/package/@cyanheads/openfda-mcp-server)
- [openFDA API authentication / rate limits](https://open.fda.gov/apis/authentication/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=openfda-mcp-server&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fopenfda-mcp-server.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
