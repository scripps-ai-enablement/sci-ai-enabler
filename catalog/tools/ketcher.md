---
title: Ketcher Chemistry (Claude Science Connector)
parent: All tools
grand_parent: Catalog
tool_type: Claude.ai Connector
supplier: EPAM Systems
availability: GA
tool_categories: [Chemistry]
last_verified: 2026-07-17
claude_science: true
summary: Interactive 2D molecule sketcher (Ketcher) for drawing/editing chemical structures; the Ketcher Chemistry connector in Claude Science.
---

# Ketcher Chemistry (Claude Science Connector)

Provides an interactive 2D chemical-structure sketcher based on EPAM's open-source Ketcher, offered inside Claude Science.

| | |
|---|---|
| **Type** | Claude.ai Connector |
| **Supplier** | [EPAM Systems](https://github.com/epam/ketcher) |
| **Availability** | GA — Anthropic-hosted connector (EPAM component) |
| **Pricing** | Free / OSS (Apache-2.0) |
| **Capabilities** | Read/Write — draw, edit, and export molecular structures (SMILES/MOL) |

## How to install

- **Claude Science** — enable the *Ketcher Chemistry* connector to sketch and edit structures interactively.
- **Standalone / embed** — Ketcher is an open-source JS component, not a data API:
  ```
  npm install ketcher-react ketcher-standalone
  ```
  See [epam/ketcher](https://github.com/epam/ketcher) to embed it in your own app.

## What it does

An interactive 2D molecule editor: draw and edit chemical structures and reactions, and export/import as SMILES, MOL/RXN, or other cheminformatics formats. It is a UI component rather than a queryable data source.

**Primary use cases**: Structure drawing, molecule editing, SMILES/MOL export for downstream tools

## Notes

**Claude Science:** Offered inside Anthropic's **Claude Science** via the *Ketcher Chemistry* featured connector. Its inclusion there is an independent signal of quality and trustworthiness for life-science research.

Ketcher is a JS UI component (npm `ketcher-react`), maintained by EPAM Systems. Unlike the other Claude Science chemistry sources, it is an editor, not a database.

## Sources

- [epam/ketcher](https://github.com/epam/ketcher)
- [Ketcher](https://lifescience.opensource.epam.com/ketcher/)
- [Anthropic — Claude Science: Connectors and skills](https://claude.com/docs/claude-science/connectors-and-skills)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=ketcher&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fketcher.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
