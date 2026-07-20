---
title: Composer
parent: All tools
grand_parent: Catalog
tool_type: Plugin
supplier: Scripps AI Enablement
availability: Beta
tool_categories: [All]
last_verified: 2026-06-11
verification: works
verified_on: 2026-07-20
security: cleared
security_on: 2026-07-20
security_note: "first-party Scripps plugin; confirmed present as composer at ./composer in this repo's .claude-plugin/marketplace.json, so /plugin install composer@sci-ai-enabler is current; OSS in-repo"
summary: Turns a plain-language scientific problem into a grounded, runnable Claude solution composed from this catalog, reusing recipes and, for open-ended goals, assembling a multi-agent system from those same components.
---

# Composer

A Claude Code / Cowork plugin that takes a plain-language scientific problem and composes a grounded, runnable solution from the components in this knowledge base — reusing a curated recipe when one fits, walking the simplicity ladder when it doesn't, and, when a problem needs a full agentic loop, assembling that multi-agent system from cataloged components rather than pointing you at an external system it cannot run.

| | |
|---|---|
| **Type** | Plugin (bundles the `compose` skill + the `/composer:compose` command + a bundled index) |
| **Supplier** | [Scripps AI Enablement](https://github.com/scripps-ai-enablement/sci-ai-enabler) |
| **Availability** | Beta (Claude Code and Cowork) |
| **Pricing** | Free / OSS — included with this repository; normal model-token usage applies |
| **Capabilities** | Problem classification, semantic recipe/tool/system matching, grounded assembly, install + first-run enactment, capture write-back |
| **Verified** | works · 2026-07-20 |
| **Security** | cleared · 2026-07-20 — first-party plugin confirmed at ./composer in this repo's marketplace.json, install path current, OSS in-repo |

## How to install

No clone or local checkout needed — the `owner/repo` shorthand fetches this public marketplace straight from GitHub. In **any** Claude Code or Cowork session, in any directory, run:

```
/plugin marketplace add scripps-ai-enablement/sci-ai-enabler
/plugin install composer@sci-ai-enabler
```

If prompted for install scope, choose **user** to make the command available everywhere; confirm with `/plugin`. Then run `/composer:compose <your problem>` (or just describe the problem in chat — the skill triggers on intent). Refresh later with `/plugin marketplace update sci-ai-enabler`.

## What it does

Given a problem like *"I have a stack of new single-cell preprints and need to triage them"*, the Composer classifies it, searches the cookbook for a matching recipe, and either presents that recipe or composes the simplest grounded assembly of cataloged components — always carrying evidence, availability, and compute caveats. It then offers to actually install the components, leave a reusable project command behind, and run the workflow once against your data. When no grounded solution exists, it says so honestly and offers to file a request that feeds the daily curator loop.

**Primary use cases**: Choosing tools for a new task, assembling a multi-component workflow, composing a multi-agent system for an open-ended goal, and turning a one-off solution into a reusable command.

## Notes

Matches on *meaning* (each catalog entry's summary and keywords), not on the subject-area categories, which are non-mutually-exclusive Scripps departments. The bundled index is regenerated daily from the catalog and recipes; run `/plugin marketplace update sci-ai-enabler` to refresh it. The [AI-scientists tracker](../../autonomous-science/) is *not* part of the composer's grounding set — those are external systems it can't install; it composes equivalent systems from cataloged components instead. Composition reports are filed only with your confirmation, and an abstracted-text option is offered because this repository is public.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `/plugin install` says the plugin can't be found | Make sure you ran `/plugin marketplace add scripps-ai-enablement/sci-ai-enabler` first, and that you included the marketplace suffix: `composer@sci-ai-enabler`, not bare `composer`. |
| `/plugin marketplace add` fails, or `/plugin` isn't recognized at all | Your Claude Code is likely too old. Check with `claude --version` and update to the latest; the plugin/marketplace commands need a current release. |
| Marketplace add fails with "not found" after you'd added it before | Your local copy of the marketplace is stale. Run `/plugin marketplace update sci-ai-enabler` (or remove and re-add: `/plugin marketplace remove sci-ai-enabler` then add again). |
| `/composer:compose` returns "unknown command" | The command is namespaced by the plugin. Use `/composer:compose <problem>` (not bare `/compose`), or just describe your problem in chat — the skill triggers on intent. |
| Installed, but the command doesn't show up | Run `/plugin list` to confirm it's enabled; if it's disabled, `/plugin enable composer`. After editing plugin files locally, `/reload-plugins`. Check the install scope — if you installed it for one project, it won't appear in others (reinstall with **user** scope). |
| It recommends against an old tool, or misses a brand-new one | The bundled index reflects your last marketplace update. Run `/plugin marketplace update sci-ai-enabler` to pull the latest. |

This repository is public, so no tokens, SSH keys, or org access are needed to install.

## Sources

- [sci-ai-enabler repository](https://github.com/scripps-ai-enablement/sci-ai-enabler) — verified 2026-06-11 (this run).
- [Plugins guide](../../guide/plugins.html) and [Marketplaces guide](../../guide/marketplaces.html) — install model.

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=composer&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fcomposer.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
