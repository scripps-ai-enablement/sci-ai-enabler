---
title: mcptools (R)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Posit Software, PBC
availability: GA
tool_categories: [General-Purpose Utilities]
last_verified: 2026-08-15
verification: works
verified_on: 2026-08-17
reviewed_on: 2026-08-17
security: cleared
security_on: 2026-08-17
security_note: "raw LICENSE.md fetched this run is standard MIT (Posit Software PBC, 2025), resolving the license-unrecognized flag; provenance matches Posit, launch command confirmed verbatim against the package vignette"
summary: "Posit's CRAN package that turns a live R session into an MCP server, letting Claude run R and call your own R functions as tools."
---

# mcptools (R)

Posit's CRAN package that exposes R to Claude over MCP — either as a standalone server that runs R code, or as a bridge into an already-running interactive R session with your data loaded.

| | |
|---|---|
| **Type** | MCP server (R package; also an MCP *client* for R via ellmer) |
| **Supplier** | [Posit Software, PBC](https://posit-dev.github.io/mcptools/) — maintainer Simon Couch |
| **Availability** | GA — CRAN 1.0.1, published 2026-07-27 |
| **Pricing** | Free / OSS — MIT |
| **Capabilities** | Read/Write — runs R in your session; the exact surface is whatever tools you register |
| **Verified** | works · 2026-08-17 |
| **Security** | cleared · 2026-08-17 — MIT confirmed via raw LICENSE.md, provenance matches Posit, no advisories |

## How to install

1. **Install the package** from an R console:
   ```r
   install.packages("mcptools")
   ```
   R 4.1.0 or newer.

2. **Claude Code** — register the server:
   ```
   claude mcp add -s "user" r-mcptools -- Rscript -e "mcptools::mcp_server()"
   ```

3. **Claude Desktop** — add to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "r-mcptools": {
         "command": "Rscript",
         "args": ["-e", "mcptools::mcp_server()"]
       }
     }
   }
   ```
   Fully quit and relaunch Claude Desktop after editing. (**Unverified —** upstream documents only the `claude mcp add` form; this JSON is the direct equivalent of that command but is not shown in the package docs. On Windows, `Rscript` must be on `PATH` or given as an absolute path.)

4. **Optional — connect to your live R session.** Add this to your `.Rprofile` so interactive sessions announce themselves to the server:
   ```r
   if (interactive() && requireNamespace("mcptools", quietly = TRUE)) {
     mcptools::mcp_session()
   }
   ```
   The server then picks the session whose working directory matches its own, so a Claude Code instance launched inside a project connects to that project's R session automatically.

`mcp_server()` is launched by Claude over stdio — you do not run it yourself in a terminal.

## What it does

Out of the box `mcp_server()` exposes only session-plumbing tools — `list_r_sessions()` and `select_r_session()` — and deliberately nothing that touches your data. Useful capability comes from passing your own tools to the `tools` argument: any function wrapped with `ellmer::tool()` can be registered, including a general `run_r_code()` tool if you want the agent to execute arbitrary R.

Because it runs in a real R session, this is the practical route to driving Bioconductor from Claude — `DESeq2`, `SummarizedExperiment`, `limma`, `flowCore` and the rest have no MCP servers of their own.

**Primary use cases**: driving Bioconductor and R statistics workflows from Claude, letting Claude inspect objects in a live analysis session, exposing lab-specific R functions as agent tools.

## Notes

Registering a `run_r_code()`-style tool gives the model arbitrary code execution in your R session, with whatever filesystem and credential access that session has — the package docs frame this as an option "for the brave" rather than a default. Prefer narrowly-scoped `ellmer::tool()` wrappers for anything shared or automated.

`mcptools` is also an MCP *client*: R code using ellmer can pull tools from third-party MCP servers into a chat, which is the reverse direction from the server use described above.

Several catalogued R-based skills — [DESeq2 differential expression](deseq2-differential-expression.html), [cytometry QC](cytometry-qc.html), [gating analysis](gating-analysis.html), [clustering and phenotyping](clustering-phenotyping.html) — assume an R runtime is reachable. This package is the general-purpose way to provide one.

## Sources

- [mcptools on CRAN](https://cran.r-project.org/web/packages/mcptools/index.html)
- [R as an MCP server (package vignette)](https://posit-dev.github.io/mcptools/articles/server.html)
- [`posit-dev/mcptools`](https://github.com/posit-dev/mcptools)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=mcptools&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fmcptools.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
