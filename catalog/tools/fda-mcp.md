---
title: FDA MCP Server (OpenPharma)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: OpenPharma
availability: Beta
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-08-09
summary: MIT MCP server over the FDA Orange Book, Purple Book, and openFDA — patent-cliff forecasting, therapeutic equivalents, and biosimilar interchangeability.
---

# FDA MCP Server (OpenPharma)

Community MCP server that puts the FDA **Orange Book** (small-molecule patents and exclusivity) and **Purple Book** (biologics and biosimilars) in front of Claude alongside openFDA, so loss-of-exclusivity and biosimilar-interchangeability questions can be answered without hand-searching the FDA portals.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [OpenPharma](https://github.com/openpharma-org/fda-mcp) |
| **Availability** | Beta — `package.json` declares v1.0.0, but **no npm package is published** (both `fda-mcp` and `@openpharma-org/fda-mcp-server` return 404 on the registry as of 2026-08-09), so installation is from source. Repo last pushed 2026-03-10 |
| **Pricing** | Free / OSS (MIT, `LICENSE` in repo root). No API key required |
| **Capabilities** | Read-only — queries public FDA datasets; downloads and caches Orange/Purple Book data locally |

## How to install

There is no published package, so build from source. Requires **Node.js ≥ 18**.

```
git clone https://github.com/openpharma-org/fda-mcp
cd fda-mcp
npm install
npm run build
```

That produces `build/index.js` (the `main` and `bin` entry point declared in `package.json`).

- **Claude Code** — register the built server over stdio:

  ```
  claude mcp add --transport stdio fda-mcp -- node /path/to/fda-mcp/build/index.js
  ```

  (replace `/path/to/fda-mcp` with the absolute path of your clone — e.g. `/Users/you/repos/fda-mcp`, or run `pwd` while still inside the directory from the previous step and paste that. The upstream README writes this path as `/path/to/fda-mcp-server/…`, which does not match the repository's own directory name — use `fda-mcp` unless you renamed the clone.)

- **Claude Desktop** — add to `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "fda-mcp": {
        "command": "node",
        "args": ["/path/to/fda-mcp/build/index.js"],
        "env": {}
      }
    }
  }
  ```

  (same absolute-path substitution; restart Claude Desktop after editing.)

- **Verify it starts** (optional): `node build/index.js` from the clone should boot and wait on stdio. Ctrl-C once it does — Claude Code and Claude Desktop launch the process themselves, so this is not a service to leave running.

On first use the server downloads and caches the Orange Book and Purple Book datasets, so the initial query is slow; subsequent lookups hit the local cache.

## What it does

Exposes a **single tool, `fda_info`**, dispatched by method:

- `lookup_drug` — general drug lookup across openFDA search types
- `search_orange_book` — brand and generic product search
- `get_therapeutic_equivalents` — AB-rated generic alternatives for a product
- `get_patent_exclusivity` — patents and exclusivity periods by NDA number
- `analyze_patent_cliff` — generic-entry forecasting / loss-of-exclusivity analysis
- `search_purple_book` — biological products and biosimilars
- `get_biosimilar_interchangeability` — interchangeability designations

Upstream reports coverage of 47,486 Orange Book drug products, 21,126 patents, and 2,444 exclusivity periods, plus 2,168 Purple Book biological products, with openFDA fields for adverse events, labels, recalls, and shortages.

**Primary use cases**: loss-of-exclusivity timing for a portfolio, finding AB-rated substitutes, biosimilar and interchangeability status, patent-cliff analysis for competitive intelligence.

## Notes

The distinguishing surface is **Orange Book patent/exclusivity and Purple Book biosimilar interchangeability** — neither is covered by the openFDA-only servers already catalogued. If you only need adverse events, labels, or recalls, [OpenFDA MCP Server (cyanheads)](openfda-mcp-server.html) installs in one command from npm and is more actively maintained.

Treat the patent-cliff output as a research aid, not a legal or commercial opinion: the Orange Book is the FDA's listing of patents a sponsor chose to submit, and generic entry additionally depends on ANDA approval, exclusivity codes, litigation, and settlements that no dataset here captures. Cached data ages between refreshes — confirm any date you plan to act on against the live FDA portal.

The single-tool-with-methods design means the model has to pick the right method string; if a query returns nothing useful, name the method explicitly in the prompt.

Complements [openFDA](openfda.html), [FDA drug databases](fda-database.html), [DailyMed](dailymed-database.html), and the [Drug Regulatory Research](tooluniverse-drug-regulatory.html) skill, which reasons over the same Orange Book records through ToolUniverse.

## Sources

- [`openpharma-org/fda-mcp`](https://github.com/openpharma-org/fda-mcp)
- [`openpharma-org/fda-mcp` LICENSE (MIT)](https://github.com/openpharma-org/fda-mcp/blob/main/LICENSE)
- [FDA Orange Book](https://www.accessdata.fda.gov/scripts/cder/ob/)
- [FDA Purple Book](https://purplebooksearch.fda.gov/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=fda-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ffda-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
