---
title: Decision tree
parent: Guide
nav_order: 7
---

# Decision tree

> "I want to do X — which Claude component should I use?"

Use this table to find the right component type for a goal you have in mind.

| If you want to… | Reach for | Why |
|---|---|---|
| Search a database (PubMed, ClinicalTrials.gov, ChEMBL, …) from Claude | **MCP server** | Databases expose searchable APIs; MCP wraps them as tools Claude can call. |
| Add a one-click integration inside Claude.ai chat | **Connector** | Connectors are toggled from `claude.ai/directory/connectors` without install commands. Requires Pro/Team/Enterprise for unlimited custom connectors. |
| Give Claude Code a focused capability (e.g., "design a clinical trial protocol") | **Skill** | Skills load context and conventions for one task. The same `SKILL.md` works in Cowork and other Skill-compatible agents. |
| Automate desktop/office work (files, spreadsheets, slides) without writing code | **Claude Cowork** | Cowork is the non-developer counterpart to Claude Code; runs in a sandboxed desktop VM. |
| Bundle several skills + MCP servers + hooks into one installable unit | **Plugin** | Plugins are the distribution format that combines multiple component types. |
| Share components with your team via a single install command | **Marketplace** | Marketplaces let `/plugin install …` and `/plugin marketplace add …` pull from a curated `marketplace.json`. |
| Run a script automatically before/after Claude calls a tool | **Hook** ([advanced](advanced/hooks.md)) | Hooks fire on Claude Code events. Not user-facing capabilities. |
| Add a custom `/myCommand` to your project | **Slash command** ([advanced](advanced/slash-commands.md)) | Slash commands are user-defined entry points. They can wrap any of the above. |

## Not sure which surface you're using?

See [Claude surfaces](claude-surfaces.md). Skills, MCP servers, and Plugins work in **Claude Code** and **Cowork**; Connectors work in **Claude.ai** and **Desktop**. Some tools (e.g., PubMed) are available in multiple surfaces — the [catalog](../catalog/) entries enumerate every install path per tool.

## See also

- [Catalog of life-science components](../catalog/) — concrete examples for each row above.
