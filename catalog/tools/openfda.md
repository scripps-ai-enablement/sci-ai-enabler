---
title: OpenFDA MCP Server (ythalorossy)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Ythalo Saldanha
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-06-06
summary: MIT-licensed npm MCP server over the openFDA drug API — adverse events, safety/labeling, manufacturer lookups, and NDC resolution.
---

# OpenFDA MCP Server (ythalorossy)

Community MCP server that queries the U.S. FDA's public openFDA drug API — adverse-event reports, drug safety/labeling, manufacturer lookups, and National Drug Code (NDC) resolution.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Ythalo Saldanha](https://github.com/ythalorossy/openfda) |
| **Availability** | GA — published to npm as `@ythalorossy/openfda` |
| **Pricing** | Free / OSS (MIT). Requires a free openFDA API key; key raises the rate limit from 1,000 to 120,000 requests/hour |
| **Capabilities** | Read-only — openFDA drug-endpoint queries |

## How to install

This server runs over stdio, so Claude Code / Claude Desktop launch the process themselves — there is no long-lived service to keep running. Obtain a free key first at [open.fda.gov/apis/authentication](https://open.fda.gov/apis/authentication/).

- **Claude Code** — register the npm package directly (no separate install step; `npx` fetches it):

  ```
  claude mcp add-json openfda '{"command":"npx","args":["-y","@ythalorossy/openfda"],"env":{"OPENFDA_API_KEY":"your_api_key_here"}}'
  ```

  (Replace `your_api_key_here` with the key from the openFDA authentication page above.)

- **Claude Desktop** — add to `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "openfda": {
        "command": "npx",
        "args": ["-y", "@ythalorossy/openfda"],
        "env": { "OPENFDA_API_KEY": "your_api_key_here" },
        "timeout": 60000
      }
    }
  }
  ```

  Restart Claude Desktop after editing the config.

## What it does

Exposes seven tools over the openFDA drug endpoints:

- **get-drug-by-name** — look up a drug by brand name.
- **get-drug-by-generic-name** — look up a drug by generic (active-ingredient) name.
- **get-drug-adverse-events** — adverse-event / side-effect reports for a drug (FAERS), by brand or generic name.
- **get-drugs-by-manufacturer** — all drugs for a given manufacturer.
- **get-drug-safety-info** — warnings, contraindications, interactions, and precautions.
- **get-drug-by-ndc** — resolve a National Drug Code, with format normalisation and validation.
- **get-drug-by-product-ndc** — resolve a product-level NDC.

**Primary use cases**: Drug-safety and adverse-event review, label/warning lookup, manufacturer and NDC resolution for pharmacovigilance and repurposing workflows.

## Notes

stdio transport. Drug-endpoint coverage only (no device or food endpoints). The openFDA API key is required at startup via the `OPENFDA_API_KEY` env var; store it in your client config rather than committing it to a file. For a broader, multi-source biomedical server that also wraps openFDA adverse events alongside PubMed / ClinicalTrials.gov / MyVariant, see [BioMCP](biomcp.html).

## Sources

- [`ythalorossy/openfda`](https://github.com/ythalorossy/openfda)
- [npm `@ythalorossy/openfda`](https://www.npmjs.com/package/@ythalorossy/openfda)
- [openFDA API authentication / rate limits](https://open.fda.gov/apis/authentication/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=openfda&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fopenfda.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
