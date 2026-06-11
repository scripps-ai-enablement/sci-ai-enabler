---
title: Composer
parent: All tools
grand_parent: Catalog
tool_type: Plugin
supplier: Scripps AI Enablement
availability: Beta
tool_categories: [All]
last_verified: 2026-06-11
summary: Turns a plain-language scientific problem into a grounded, runnable Claude solution composed from this catalog, reusing recipes and recommending autonomous systems.
---

# Composer

A Claude Code / Cowork plugin that takes a plain-language scientific problem and composes a grounded, runnable solution from the components in this knowledge base — reusing a curated recipe when one fits, walking the simplicity ladder when it doesn't, and recommending a pre-built autonomous-science system when that is genuinely the right rung.

| | |
|---|---|
| **Type** | Plugin (bundles the `compose` skill + the `/compose` command + a bundled index) |
| **Supplier** | [Scripps AI Enablement](https://github.com/scripps-ai-enablement/sci-ai-enabler) |
| **Availability** | Beta (Claude Code and Cowork) |
| **Pricing** | Free / OSS — included with this repository; normal model-token usage applies |
| **Capabilities** | Problem classification, semantic recipe/tool/system matching, grounded assembly, install + first-run enactment, capture write-back |

## How to install

- **Claude Code / Cowork** — plugin marketplace:
  ```
  /plugin marketplace add scripps-ai-enablement/sci-ai-enabler
  /plugin install composer@sci-ai-enabler
  ```

Then run `/compose <your problem>` (or just describe the problem — the skill triggers on intent).

## What it does

Given a problem like *"I have a stack of new single-cell preprints and need to triage them"*, the Composer classifies it, searches the cookbook for a matching recipe, and either presents that recipe or composes the simplest grounded assembly of cataloged components — always carrying evidence, availability, and compute caveats. It then offers to actually install the components, leave a reusable project command behind, and run the workflow once against your data. When no grounded solution exists, it says so honestly and offers to file a request that feeds the daily curator loop.

**Primary use cases**: Choosing tools for a new task, assembling a multi-component workflow, deciding whether an autonomous system fits, and turning a one-off solution into a reusable command.

## Notes

Matches on *meaning* (each catalog entry's summary and keywords), not on the subject-area categories, which are non-mutually-exclusive Scripps departments. The bundled index is regenerated daily from the catalog, recipes, and autonomous-science tracker; run `/plugin marketplace update sci-ai-enabler` to refresh it. Composition reports are filed only with your confirmation, and an abstracted-text option is offered because this repository is public.

## Sources

- [sci-ai-enabler repository](https://github.com/scripps-ai-enablement/sci-ai-enabler) — verified 2026-06-11 (this run).
- [Plugins guide](../../guide/plugins.html) and [Marketplaces guide](../../guide/marketplaces.html) — install model.

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=composer&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcomposer.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
