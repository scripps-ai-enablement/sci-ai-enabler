---
title: cBioPortal MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: cBioPortal
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-07-17
claude_science: true
summary: Query cancer genomics studies, mutations, and clinical data from cBioPortal; also the Cancer Models connector in Claude Science.
---

# cBioPortal MCP Server

Exposes cBioPortal's cancer genomics studies — mutations, copy-number, and clinical attributes — to Claude via an official MCP server.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [cBioPortal](https://github.com/cBioPortal/cbioportal-mcp) |
| **Availability** | GA — official MCP server |
| **Pricing** | Free / OSS (data ODbL; some studies access-restricted) |
| **Capabilities** | Read-only |

## How to install

- **Claude Code / Desktop** — MCP server ([cBioPortal/cbioportal-mcp](https://github.com/cBioPortal/cbioportal-mcp), OSS):
  ```
  git clone https://github.com/cBioPortal/cbioportal-mcp
  cd cbioportal-mcp
  uv run cbioportal-mcp
  ```
  See [https://docs.cbioportal.org/ai-integrations/mcp/](https://docs.cbioportal.org/ai-integrations/mcp/) for setup.
- **Claude Science** — also available as the *Cancer Models* featured connector (Anthropic-hosted).
- **Public API** — [cbioportal.org/api](https://www.cbioportal.org/api).

## What it does

Search cancer studies, retrieve mutation / CNA / clinical profiles for genes and samples, and pull study metadata across the cBioPortal public instance and compatible deployments.

**Primary use cases**: Cancer genomics lookup, cohort/mutation queries, biomarker exploration

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Cancer Models* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Official server maintained by the cBioPortal project. Some studies carry access restrictions even though the portal is open (ODbL).

## Sources

- [cBioPortal/cbioportal-mcp](https://github.com/cBioPortal/cbioportal-mcp)
- [cBioPortal MCP docs](https://docs.cbioportal.org/ai-integrations/mcp/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=cbioportal&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcbioportal.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
