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
| Go from "I have problem X" to a grounded, runnable solution without first knowing which components exist | **The [Composer](../catalog/tools/composer.md) plugin** (`/composer:compose`) | It matches your problem against the whole catalog/recipes/systems index, assembles the simplest grounded solution, and offers to install and run it. |
| Search a database (PubMed, ClinicalTrials.gov, ChEMBL, …) from Claude | **MCP server** | Databases expose searchable APIs; MCP wraps them as tools Claude can call. |
| Add a one-click integration inside Claude.ai chat | **Connector** | Connectors are toggled from `claude.ai/directory/connectors` without install commands. Requires Pro/Team/Enterprise for unlimited custom connectors. |
| Give Claude Code a focused capability (e.g., "design a clinical trial protocol") | **Skill** | Skills load context and conventions for one task. The same `SKILL.md` works in Cowork and other Skill-compatible agents. |
| Run an analysis that needs a scientific library with no Claude wrapper (atlas lookup, instrument-file parsing, epitope prediction) | **Claude Code + a [recipe](../recipes/) that declares it as a dependency** | Claude Code has a shell, so `pip install` *is* the install path — no wrapper needed. The recipe carries the exact pin, the license, and the import to verify; see the [library index](../recipes/dependencies.md). Not available in Claude.ai chat, which has nowhere to install it. |
| Automate desktop/office work (files, spreadsheets, slides) without writing code | **Claude Cowork** | Cowork is the non-developer counterpart to Claude Code; runs in a sandboxed desktop VM. |
| Run a reproducible scientific analysis over curated databases (genomics, proteomics, cheminformatics) | **[Claude Science](surfaces/claude-science.md)** | A research workbench app that orchestrates 60+ skills and database connectors and keeps code + environment + provenance per figure. |
| Delegate tasks to Claude where your team already works, in Slack | **[Claude Tag](surfaces/claude-tag.md)** | Tag `@Claude` in a channel; one shared Claude works the task asynchronously with per-channel tools and memory (Enterprise/Team beta). |
| Bundle several skills + MCP servers + hooks into one installable unit | **Plugin** | Plugins are the distribution format that combines multiple component types. |
| Share components with your team via a single install command | **Marketplace** | Marketplaces let `/plugin install …` and `/plugin marketplace add …` pull from a curated `marketplace.json`. |
| Run a script automatically before/after Claude calls a tool | **Hook** ([advanced](advanced/hooks.md)) | Hooks fire on Claude Code events. Not user-facing capabilities. |
| Add a custom `/myCommand` to your project | **Slash command** ([advanced](advanced/slash-commands.md)) | Slash commands are user-defined entry points. They can wrap any of the above. |

## Not sure which surface you're using?

See [Claude surfaces](claude-surfaces.md). Skills, MCP servers, and Plugins work in **Claude Code** and **Cowork**; Connectors work in **Claude.ai** and **Desktop**. Some tools (e.g., PubMed) are available in multiple surfaces — the [catalog](../catalog/) entries enumerate every install path per tool.

## See also

- [Catalog of life-science components](../catalog/) — concrete examples for each row above.
