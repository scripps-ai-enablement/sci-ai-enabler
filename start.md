---
title: Start here
nav_order: 1
permalink: /start/
description: "Install the Composer plugin in Claude Code or Cowork and try it on a real problem."
---

# Start here: the Composer

Don't know which of the cataloged components you need? Install the **[Composer](catalog/tools/composer.md)** plugin, describe your problem in plain language, and it composes a grounded, runnable solution from everything in this resource — reusing a curated [recipe]({{ '/recipes/' | relative_url }}) when one fits, assembling the simplest set of tools when it doesn't, and recommending a pre-built [autonomous system]({{ '/autonomous-science/' | relative_url }}) when that's the right call. It never invents a tool, always shows the evidence / availability / compute trade-offs, and offers to install the pieces and run them for you.

## 1. Install it (once)

**What you need:** [Claude Code](https://code.claude.com/) (or Cowork), signed in to your Anthropic account. That's it. The Composer is a Claude Code / Cowork plugin — it runs where you assemble pipelines, **not** in Claude.ai chat (chat uses [Connectors](guide/connectors.md) instead).

**You do not need to clone this repository or be in any particular folder.** The `scripps-ai-enablement/sci-ai-enabler` shorthand below tells Claude Code to fetch the marketplace straight from GitHub (it keeps its own copy internally). The repo is public, so no tokens, SSH keys, or git setup are involved.

Open **any** Claude Code or Cowork session, in any directory, and run these two commands (type them at the prompt exactly as written, including the leading `/`):

```
/plugin marketplace add scripps-ai-enablement/sci-ai-enabler
/plugin install composer@sci-ai-enabler
```

- The first command registers this repository as a [plugin marketplace](guide/marketplaces.md).
- The second installs the Composer from it. If Claude Code asks whether to install for **this project** or your **user account**, choose **user** so `/composer:compose` is available in every project.
- Confirm it worked: run `/plugin` and check that **composer** is listed (or type `/composer:` and see the command autocomplete).

Later, as the catalog grows, refresh your copy with `/plugin marketplace update sci-ai-enabler`.

## 2. Use it

Invoke it explicitly with the slash command, or just describe your problem in chat and the skill triggers on intent:

```
/composer:compose <describe what you're trying to do>
```

## Try it — paste any of these
{: #try-it }

Each prompt exercises a different path through the Composer. Run them as-is to see how it behaves. Some will offer to install additional components and run the workflow on your data — the Composer always asks before installing or changing anything.

- `/composer:compose I have a stack of new single-cell preprints and need to triage them`
  — *reuses a curated recipe* and offers to run it against your field right away.
- `/composer:compose rank microglial scRNA-seq preprints by relevance to neuroinflammation`
  — *matches on meaning across research areas*, even though the wording spans Neuroscience and Molecular & Cellular Biology.
- `/composer:compose convert a folder of vendor instrument CSVs into a tidy long-format table`
  — *walks the simplicity ladder*, recommending the cheapest assembly that solves it.
- `/composer:compose I want an agent to go from a disease hypothesis through experiment design to analysis end to end`
  — *recommends a pre-built autonomous system* (e.g. Robin, OpenScientist, or Biomni) with the evidence behind it.
- `/composer:compose predict crystal packing for a small molecule from its SMILES`
  — *tells you honestly when nothing in the catalog fits* rather than inventing a tool, and offers to file the gap so a recipe gets written.

## If something doesn't work

See the [Composer's troubleshooting table](catalog/tools/composer.md#troubleshooting) for the common install hiccups — a missing `@sci-ai-enabler` suffix, an outdated Claude Code, a stale marketplace copy, or the namespaced `/composer:compose` command.

## Prefer to browse first?

- [Recipes]({{ '/recipes/' | relative_url }}) — concrete problem → solution pairings, if you'd rather start from a worked example.
- [Guide]({{ '/guide/' | relative_url }}) — what Skills, MCP servers, Plugins, and Connectors are, if the terms are new.
- [Catalog]({{ '/catalog/' | relative_url }}) — every installable component, by research area.
- [Autonomous AI scientists]({{ '/autonomous-science/' | relative_url }}) — the frontier of systems that take real initiative.
