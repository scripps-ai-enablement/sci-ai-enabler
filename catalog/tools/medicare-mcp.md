---
title: Medicare MCP Server (OpenPharma)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: OpenPharma
availability: Beta
tool_categories: [Translational Medicine]
last_verified: 2026-08-16
verification: works
verified_on: 2026-08-17
reviewed_on: 2026-08-17
security: cleared
security_on: 2026-08-17
security_note: "openpharma-org confirmed as org (not archived), MIT via GitHub license API; build/index.js bin entry and node launch command confirmed against package.json and README, same publisher already cleared for fda-mcp"
summary: MIT MCP server over public CMS Medicare data — provider and prescriber lookup, hospital quality and safety measures, Part B/D drug pricing and formularies.
---

# Medicare MCP Server (OpenPharma)

Community MCP server that exposes public CMS Medicare datasets — physician and prescriber utilization, hospital quality and safety measures, and Part B/Part D drug pricing — as a single keyless Claude tool.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [OpenPharma](https://github.com/openpharma-org/medicare-mcp) |
| **Availability** | Beta — `package.json` declares v0.3.0 and **no npm package is published** (both `medicare-mcp` and `@openpharma-org/medicare-mcp-server` return 404 on the registry as of 2026-08-16), so installation is from source |
| **Pricing** | Free / OSS (MIT, `LICENSE` in repo root, confirmed via the GitHub license API 2026-08-16). No API key required — CMS public APIs are keyless |
| **Capabilities** | Read-only — queries public CMS APIs (provider data, Socrata ASP pricing) |
| **Verified** | works · 2026-08-17 |
| **Security** | cleared · 2026-08-17 — MIT, provenance matches OpenPharma org, launch command confirmed against package.json/README |

## How to install

There is no published package, so build from source. `package.json` declares **Node.js ≥ 16** (use ≥ 18 in practice, as the MCP SDK targets it).

```
git clone https://github.com/openpharma-org/medicare-mcp
cd medicare-mcp
npm install
npm run build
```

That produces `build/index.js` (the `bin` entry point declared in `package.json`).

- **Claude Code** — register the built server over stdio:

  ```
  claude mcp add --transport stdio medicare-mcp -- node /path/to/medicare-mcp/build/index.js
  ```

  (replace `/path/to/medicare-mcp` with the absolute path of your clone — e.g. `/Users/you/repos/medicare-mcp`, or run `pwd` while still inside the directory from the previous step and paste that. The upstream README writes this path as `/path/to/medicare-mcp-server/…`, which does not match the repository's own directory name — use `medicare-mcp` unless you renamed the clone.)

- **Claude Desktop** — add to `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "medicare-mcp": {
        "command": "node",
        "args": ["/path/to/medicare-mcp/build/index.js"],
        "env": {}
      }
    }
  }
  ```

  (same absolute-path substitution; restart Claude Desktop after editing.)

- **Verify it starts** (optional): `node build/index.js` from the clone should boot and wait on stdio. Ctrl-C once it does — Claude Code and Claude Desktop launch the process themselves, so this is not a service to leave running.

## What it does

Exposes a **single tool, `medicare_info`**, dispatched by a `method` parameter. Upstream documents 17 methods in four groups:

- **Provider and prescriber utilization** — `search_providers` (physician and practitioner data, 2013–2023), `search_prescribers` (Part D prescribing patterns by drug or specialty), `search_hospitals` (inpatient utilization and payments).
- **Hospital quality and safety** — `get_hospital_star_rating`, `get_readmission_rates` (30-day, by condition), `get_hospital_infections` (CLABSI, CAUTI, SSI, *C. difficile*, MRSA), `get_mortality_rates`, `search_hospitals_by_quality`, `compare_hospitals`, `get_vbp_scores` (Value-Based Purchasing), `get_hcahps_scores` (patient experience).
- **Drug pricing** — `get_asp_pricing` (Part B average sales price), `get_asp_trend` (quarterly trends), `compare_asp_pricing`, `search_spending` (Part B/D spending trends).
- **Coverage** — `search_formulary` (Part D plan coverage with tier, prior-authorization and quantity limits), `get_formulary_trend`.

**Primary use cases**: real-world prescribing and utilization patterns, hospital quality benchmarking, Part B drug price trends, Part D formulary and access research.

## Notes

The repo is titled "Unofficial Medicare MCP Server" — it is a community wrapper, not a CMS product. Data is refreshed by CMS quarterly, so figures lag the current quarter; confirm any number you plan to publish against the source dataset.

Complements [CMS Data.gov MCP](cms-datagov-mcp.html), which browses the CMS dataset *catalog*, and [CMS Coverage](cms-coverage.html), which answers national/local coverage-determination questions. This server differs by shipping pre-shaped Medicare quality and pricing queries rather than generic dataset access. For FDA-side regulatory data from the same publisher, see [FDA MCP Server (OpenPharma)](fda-mcp.html).

The single-tool-with-methods design means the model has to pick the right method string; if a query returns nothing useful, name the method explicitly in the prompt.

Provider-level Medicare data identifies named clinicians and organizations. It is public, but treat downstream analyses with the care you would apply to any named-provider dataset.

## Sources

- [`openpharma-org/medicare-mcp`](https://github.com/openpharma-org/medicare-mcp)
- [`openpharma-org/medicare-mcp` license (MIT, GitHub API)](https://github.com/openpharma-org/medicare-mcp/blob/main/LICENSE)
- [CMS Provider Data Catalog](https://data.cms.gov/provider-data/)
- [Medicare Part B ASP drug pricing files](https://www.cms.gov/medicare/payment/part-b-drugs/asp-pricing-files)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=medicare-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmedicare-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
