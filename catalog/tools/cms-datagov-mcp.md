---
title: CMS data.gov MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Clarify Health
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-07-26
summary: MIT-licensed MCP server over data.cms.gov — search, query, and export CMS public datasets (provider enrollment, hospital quality, spending) for healthcare analytics.
verification: works
verified_on: 2026-07-27
verification_note: "clarifyhealth/cms-datagov-mcp-server resolves and package.json bin cms-datagov-mcp-server maps to build/index.js confirming the npm-link launch; clone-and-build so not smoke-tested"
security: caution
security_on: 2026-07-27
security_note: "provenance matches clarifyhealth, MIT, no OSV advisories, but single-maintainer (1 star) and stale (pushed 2025-12-02)"
---

# CMS data.gov MCP Server

Community MCP server that gives Claude direct access to the Centers for Medicare & Medicaid Services (CMS) public data catalog at data.cms.gov — provider enrollment, hospital quality metrics, spending, and other datasets — for healthcare analytics workflows.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [Clarify Health](https://github.com/clarifyhealth/cms-datagov-mcp-server) |
| **Availability** | GA — published as `@clarify/cms-datagov-mcp-server` |
| **Pricing** | Free / OSS (MIT). No API key — data.cms.gov is public |
| **Capabilities** | Read-only — dataset search, filtered queries (≤ 5,000 rows), and CSV export links |
| **Verified** | works · 2026-07-27 — repo resolves; package.json bin cms-datagov-mcp-server confirms the launch |
| **Security** | caution · 2026-07-27 — provenance matches clarifyhealth, MIT, no OSV advisories, single-maintainer + stale (2025-12) |

## How to install

This server runs over stdio, so Claude Code / Claude Desktop launch the process themselves — there is no long-lived service to keep running. It is distributed from source (not published as a directly-runnable npm bin), so clone and build first.

- **Clone and build** (Node.js 18+):

  ```
  git clone https://github.com/clarifyhealth/cms-datagov-mcp-server
  cd cms-datagov-mcp-server
  npm install
  npm run build
  npm link
  ```

  (`npm link` puts the `cms-datagov-mcp-server` binary on your PATH; alternatively skip `npm link` and reference the built entry point at `$(pwd)/build/index.js` in the snippets below — replace `$(pwd)` with the absolute path of your clone.)

- **Claude Code** — register the linked binary:

  ```
  claude mcp add --transport stdio cms-datagov -- cms-datagov-mcp-server
  ```

  (If you did not run `npm link`, use `claude mcp add --transport stdio cms-datagov -- node /path/to/cms-datagov-mcp-server/build/index.js`, replacing `/path/to/…` with the absolute path of your clone — e.g., `$(pwd)/build/index.js` if you're still inside it from the build step.)

- **Claude Desktop** — add to `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "cms-datagov": {
        "command": "cms-datagov-mcp-server",
        "args": [],
        "env": {}
      }
    }
  }
  ```

  (If you did not run `npm link`, set `"command": "node"` and `"args": ["/path/to/cms-datagov-mcp-server/build/index.js"]` with the absolute path of your clone.) Restart Claude Desktop after editing the config.

## What it does

Exposes five tools plus resource templates over the data.cms.gov API (`https://data.cms.gov/data-api/v1`):

- **cms_search_datasets** — find CMS datasets by keyword.
- **cms_get_dataset** — detailed dataset metadata.
- **cms_query_dataset** — query a dataset with filters (up to 5,000 rows).
- **cms_get_dataset_stats** — row counts and column info.
- **cms_get_csv_link** — CSV download URL for bulk export.

Resource templates `cms://datasets`, `cms://dataset/{id}`, and `cms://csv/{id}` let Claude browse the catalog and pull dataset metadata or export links directly.

**Primary use cases**: Provider-enrollment and hospital-quality analysis, CMS dataset discovery, healthcare-analytics data pulls (e.g., joint-replacement / LEJR cohorts), CSV export for downstream tooling.

## Notes

stdio transport; public data, no authentication. Query results are capped at 5,000 rows per call — use `cms_get_csv_link` for bulk export. Community single-maintainer package — review the source before use.

Distinct from the Anthropic [CMS Coverage MCP](cms-coverage.html), which serves Medicare **coverage-policy** documents (Local and National Coverage Determinations) for prior-auth and appeals; this server serves the broader **data.cms.gov statistical datasets** (provider, quality, spending).

## Sources

- [`clarifyhealth/cms-datagov-mcp-server`](https://github.com/clarifyhealth/cms-datagov-mcp-server)
- [data.cms.gov API](https://data.cms.gov/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cms-datagov-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcms-datagov-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
