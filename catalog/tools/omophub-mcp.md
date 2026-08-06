---
title: OMOPHub MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: OMOPHub
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-02
verification: degraded
verified_on: 2026-08-06
reviewed_on: 2026-08-06
verification_note: "install and registration commands confirmed against the upstream README this run (npx -y @omophub/omophub-mcp, OMOPHUB_API_KEY required); auth-gated so the server itself could not be smoke-tested without an account"
security: cleared
security_on: 2026-08-06
security_note: "provenance matches OMOPHub/omophub-mcp, MIT license confirmed in README, no OSV or GitHub advisories found for the npm package"
summary: "Search, map and navigate 10M+ OHDSI OMOP vocabulary concepts (SNOMED CT, ICD-10, RxNorm, LOINC) from Claude without loading ATHENA locally"
---

# OMOPHub MCP Server

An MCP server that puts the OHDSI OMOP standardized vocabularies — SNOMED CT, ICD-10, RxNorm, LOINC and 100+ others — behind Claude as searchable, mappable concepts, instead of requiring a multi-gigabyte ATHENA download and a local database.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [OMOPHub](https://github.com/OMOPHub/omophub-mcp) (open source, MIT) |
| **Availability** | GA — npm `@omophub/omophub-mcp` 1.5.3; repo last pushed 2026-07-28 |
| **Pricing** | Free / OSS (MIT) for the server. The backing API at `api.omophub.com` requires a free account and an API key; **Unverified —** the README documents an upgrade path for higher rate limits at `dashboard.omophub.com/billing` but does not state the free-tier limits or paid prices. |
| **Capabilities** | Read-only — vocabulary search, concept lookup, mapping and hierarchy traversal |
| **Verified** | degraded · 2026-08-06 — auth-gated (requires an OMOPHUB_API_KEY signup), so functionally unverifiable without an account; launch command confirmed current |
| **Security** | cleared · 2026-08-06 — provenance matches OMOPHub/omophub-mcp, MIT, no advisories |

## How to install

You need an API key first: sign up at [omophub.com](https://omophub.com), then create a key at `dashboard.omophub.com/api-keys`. Keys are prefixed `oh_`. Node.js **20 or newer** is required (`engines.node: >=20` in the published package).

- **Claude Code** — stdio via npx, with the key passed as an environment variable:
  ```
  claude mcp add omophub --env OMOPHUB_API_KEY=oh_your_key_here -- npx -y @omophub/omophub-mcp
  ```
  (The upstream README shows `claude mcp add omophub -- npx -y @omophub/omophub-mcp` without the key; the server will not authenticate unless `OMOPHUB_API_KEY` is set, so use the `--env` form above.)
- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "omophub": {
        "command": "npx",
        "args": ["-y", "@omophub/omophub-mcp"],
        "env": {
          "OMOPHUB_API_KEY": "oh_your_key_here"
        }
      }
    }
  }
  ```
- **Docker** (optional, HTTP on port 3100 — a long-lived service you keep running, not a one-shot):
  ```
  docker run -e OMOPHUB_API_KEY=oh_your_key_here -p 3100:3100 omophub/omophub-mcp
  ```
  then register it with `claude mcp add --transport http omophub http://localhost:3100/mcp`.
- **Claude Code** — HTTP without Docker, same long-lived-service caveat:
  ```
  npx -y @omophub/omophub-mcp --transport=http --port=3100 --api-key=oh_your_key_here
  ```

## What it does

Eleven tools over the OMOP vocabulary tables:

- **Search and lookup** — `search_concepts`, `get_concept`, `get_concept_by_code`, `semantic_search`, `find_similar_concepts`.
- **Mapping and navigation** — `map_concept` (cross-vocabulary mapping, e.g. ICD-10 → SNOMED CT standard concept), `get_hierarchy` (ancestor/descendant traversal), `explore_concept`.
- **FHIR** — `fhir_resolve` and `fhir_resolve_codeable_concept`, for turning FHIR codings into OMOP standard concepts.
- **Reference** — `list_vocabularies`, plus resources `omophub://vocabularies` and `omophub://vocabularies/{vocabulary_id}`.
- **Guided prompts** — `phenotype-concept-set` (build a concept set for a phenotype definition) and `code-lookup`.

**Primary use cases**: building OMOP concept sets for cohort/phenotype definitions, mapping source codes to standard concepts during ETL, resolving FHIR codings to OMOP.

## Notes

This is a vocabulary service, not a database query server — it answers "what concept is this code, and what does it map to", not "how many patients in my CDM have it". For querying an actual OMOP CDM instance from Claude, see [pyomop](pyomop.html). For a non-OMOP terminology server covering ICD-11, SNOMED CT, LOINC, RxNorm, MeSH and ATC, see [Medical Terminologies MCP](medical-terminologies-mcp.html).

A hosted endpoint exists at `https://mcp.omophub.com` but expects the key as a Bearer token in an `Authorization` header. The README notes that Claude Desktop's Custom Connectors UI only supports OAuth and cannot send custom headers, so the `npx` stdio path above is the recommended route for Desktop.

Vocabulary content itself carries the licenses of its sources — SNOMED CT in particular requires an affiliate license in non-member countries, and the OMOP wrapper does not change that.

## Sources

- [`OMOPHub/omophub-mcp`](https://github.com/OMOPHub/omophub-mcp)
- [`@omophub/omophub-mcp` on npm](https://www.npmjs.com/package/@omophub/omophub-mcp)
- [OHDSI OMOP Common Data Model](https://ohdsi.github.io/CommonDataModel/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=omophub-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fomophub-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
