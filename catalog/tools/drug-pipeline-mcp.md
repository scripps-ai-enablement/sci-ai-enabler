---
title: Drug Pipeline MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: DasClown (community)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Translational Medicine]
last_verified: 2026-07-26
summary: MCP server aggregating clinical trials, FDA/EMA approvals, safety data, and labels into source-traceable drug pipeline intelligence — no predictions, every output cites its primary source.
verification: degraded
verified_on: 2026-07-27
verification_note: "GitHub repo resolves (MIT, pushed 2026-07-07) and the git-source install works, but PyPI drug-pipeline-mcp returned 404 this run so the documented pip/uvx launch does not resolve"
security: caution
security_on: 2026-07-27
security_note: "provenance matches DasClown, MIT, no OSV advisories, but community single-maintainer (3 stars) and not resolvable on PyPI despite the GA/PyPI claim"
flagged: PyPI drug-pipeline-mcp not resolvable — only the git-source install works this run
---

# Drug Pipeline MCP Server

An MCP server that synthesizes pharmaceutical R&D pipeline intelligence — clinical trials, FDA/EMA approvals, safety signals, and labels — into single answers where every fact traces back to a primary source (NCT ID, FDA application number, or PMID).

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [DasClown](https://github.com/DasClown/drug-pipeline-mcp) (community) |
| **Availability** | GA — published on PyPI (`drug-pipeline-mcp`) |
| **Pricing** | Free / OSS (MIT); all backing data sources are public and keyless |
| **Capabilities** | Read-only — aggregates public regulatory/trial/literature APIs |
| **Verified** | degraded · 2026-07-27 — repo resolves + git-source install works; PyPI drug-pipeline-mcp 404 so pip/uvx does not resolve |
| **Security** | caution · 2026-07-27 — provenance matches DasClown, MIT, no OSV advisories, single-maintainer + not on PyPI |

## How to install

No API key is needed — every backing source is publicly accessible. The server runs over stdio by default (Claude launches it on demand); an optional HTTP mode is available for remote use.

- **Prerequisite** — Python 3.10+ and Claude Code / Claude Desktop.

- **Install from PyPI:**
  ```
  pip install drug-pipeline-mcp
  ```
  (Or install the latest from source: `pip install git+https://github.com/DasClown/drug-pipeline-mcp.git`.)

- **Claude Code** — register over stdio:
  ```
  claude mcp add --transport stdio drug-pipeline -- uvx drug-pipeline-mcp
  ```
  (`uvx` fetches and runs the package in an isolated env; if you installed with `pip` instead, use `-- drug-pipeline` in place of `-- uvx drug-pipeline-mcp`.)

- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "drug-pipeline": {
        "command": "uvx",
        "args": ["drug-pipeline-mcp"]
      }
    }
  }
  ```
  (Equivalent to the Claude Code stdio registration; requires `uv`/`uvx` on your PATH. If you `pip install`ed the package instead, use `"command": "drug-pipeline"` with empty `"args"`.)

- **Claude Code / Desktop — optional HTTP mode** (long-lived server; keep it running):
  ```
  pip install "drug-pipeline-mcp[http]"
  drug-pipeline --http --port 8081
  ```
  Then `claude mcp add --transport http drug-pipeline http://127.0.0.1:8081/mcp` (Claude Code) or proxy via `mcp-remote` for Desktop.

## What it does

Exposes six tools spanning trials, approvals, safety, and labels:

- `search_trials` — clinical-trial discovery by condition/phase/status (ClinicalTrials.gov).
- `get_approvals` — FDA approval history with submission dates (Drugs@FDA).
- `get_safety_data` — FAERS adverse-event reports and reaction counts.
- `get_drug_label` — FDA prescribing information and contraindications (Drug Labeling / DailyMed).
- `get_eu_approvals` — EMA authorization status with orphan/biosimilar flags.
- `drug_pipeline` — composite aggregation across all sources for a single drug.

Backing sources include ClinicalTrials.gov, openFDA (Drugs@FDA, FAERS, Labeling, NDC, Enforcement), RxNorm, PubMed/NCBI, EMA daily XLSX, DailyMed, Open Targets, and MyChem.info. The project makes no ML predictions — it only structures verified primary sources.

**Primary use cases**: competitive pipeline landscaping (e.g., "what's in the pipeline for GLP-1 agonists?"), cross-region approval comparison (US vs EU), drug-safety signal review, repurposing-candidate scoping from trial/approval evidence.

## Notes

Because outputs are aggregated from live public APIs, latency and completeness depend on those upstream services. The composite `drug_pipeline` tool fans out across all sources and can be slower than the single-source tools. This server overlaps but does not duplicate the discrete [openFDA](openfda.html) / [OpenFDA MCP Server (cyanheads)](openfda-mcp-server.html) and [ClinicalTrials.gov MCP](clinicaltrials-gov-mcp.html) entries — its distinct value is the cross-source, source-traceable *pipeline* synthesis plus EMA approval coverage.

## Sources

- [`DasClown/drug-pipeline-mcp`](https://github.com/DasClown/drug-pipeline-mcp)
- [PyPI: `drug-pipeline-mcp`](https://pypi.org/project/drug-pipeline-mcp/)
- [Glama listing](https://glama.ai/mcp/servers/DasClown/drug-pipeline-mcp)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=drug-pipeline-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fdrug-pipeline-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
