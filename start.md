---
title: Start here
nav_order: 1
permalink: /start/
description: "Install the Composer plugin in Claude Code or Cowork and try it on a real problem."
---

# Start here: the Composer

Don't know which of the cataloged components you need? Install the **[Composer](catalog/tools/composer.md)** plugin, describe your problem in plain language, and it composes a grounded, runnable solution from everything in this resource — reusing a curated [recipe]({{ '/recipes/' | relative_url }}) when one fits, assembling the simplest set of tools when it doesn't, and — for open-ended goals — composing a full multi-agent system from those same components. It never invents a tool, always shows the evidence / availability / compute trade-offs, and offers to install the pieces and run them for you. (For a map of pre-built [autonomous systems]({{ '/autonomous-science/' | relative_url }}) like Robin or OpenScientist, see the AI-scientists tracker — those are informational; the Composer builds equivalents from cataloged parts rather than installing them.)

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

These span very different corners of science — structural biology, cheminformatics, clinical genomics, microbiology, drug discovery, functional genomics — and each exercises the Composer differently (reuse a curated recipe, assemble a multi-tool pipeline, compose a full multi-agent system, or say honestly that nothing fits). Run them as-is. Several will offer to install the pieces and run the workflow on your own data — the Composer always asks before installing or changing anything.

- `/composer:compose predict a protein's 3D structure from its sequence, then dock a candidate ligand against the pocket`
  — *chains curated recipes into a short structural pipeline* (structure prediction → model triage → docking) drawn from the catalog's structure and docking tools.
- `/composer:compose here's a SMILES string — profile its likely targets, on/off-target activity, and ADMET liabilities`
  — *matches on meaning* and assembles the cheminformatics stack (chemical databases + property predictors) without you naming any of them.
- `/composer:compose interpret the clinical significance of a coding variant, with the supporting evidence`
  — *drops straight onto a curated recipe* grounded in clinical-genomics knowledge bases, with the evidence / availability / compute caveats shown up front.
- `/composer:compose annotate a bacterial genome assembly and screen it for antimicrobial-resistance and virulence genes`
  — *walks the simplicity ladder* to the annotation and resistance-screening skills that close the gap — no heavier pipeline than needed.
- `/composer:compose build a dossier for a drug target: disease associations, tractability, known chemistry, and the clinical-trial landscape`
  — *assembles across research areas in one go*, naming each real source across human genetics, chemistry, and trials databases.
- `/composer:compose I have a differential-expression gene list from an RNA-seq run — tell me what pathways and diseases it points to`
  — *reuses a recipe and offers to run it on your list*, citing only terms that actually appear in the results.
- `/composer:compose I want an agent to take a disease hypothesis all the way through experiment design and data analysis`
  — *composes a multi-agent system from cataloged components* (the way this project's Crucible plugin was built), and points you to the [AI-scientists tracker](autonomous-science/) for prior art like Robin or OpenScientist — informational, not something it installs for you.
- `/composer:compose predict the solid-state crystal packing / polymorphs of a small molecule from its SMILES`
  — *tells you honestly when nothing in the catalog fits* rather than inventing a tool, and offers to file the gap so a recipe gets written.

## If something doesn't work

See the [Composer's troubleshooting table](catalog/tools/composer.md#troubleshooting) for the common install hiccups — a missing `@sci-ai-enabler` suffix, an outdated Claude Code, a stale marketplace copy, or the namespaced `/composer:compose` command.

## Prefer to browse first?

- [Recipes]({{ '/recipes/' | relative_url }}) — concrete problem → solution pairings, if you'd rather start from a worked example.
- [Guide]({{ '/guide/' | relative_url }}) — what Skills, MCP servers, Plugins, and Connectors are, if the terms are new.
- [Catalog]({{ '/catalog/' | relative_url }}) — every installable component, by research area.
- [Autonomous AI scientists]({{ '/autonomous-science/' | relative_url }}) — the frontier of systems that take real initiative.
