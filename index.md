---
title: Home
nav_order: 0
description: "Installable Claude components, beginner guides, and a tracker of autonomous AI scientists for life-science research."
permalink: /
---

# Life Science AI Ecosystem

An information resource for scientists, engineers, and clinicians working at the intersection of AI and the life sciences.

## Start here: the Composer

Don't know which of the components below you need? Install the **[Composer](catalog/tools/composer.md)** plugin, describe your problem in plain language, and it composes a grounded, runnable solution from everything in this resource — reusing a curated recipe when one fits, assembling the simplest set of tools when it doesn't, and recommending a pre-built autonomous system when that's the right call. It never invents a tool, always shows the evidence/availability/compute trade-offs, and offers to install the pieces and run them for you.

### 1. Install it (once)

The Composer is a **Claude Code / Cowork plugin** — it runs where you assemble pipelines, not in Claude.ai chat (chat uses [Connectors](guide/connectors.md) instead). You'll need Claude Code (or Cowork) and an Anthropic account.

In a Claude Code or Cowork session, run:

```
/plugin marketplace add scripps-ai-enablement/sci-ai-enabler
/plugin install composer@sci-ai-enabler
```

That registers this repository as a [plugin marketplace](guide/marketplaces.md) and installs the Composer from it. To update later as the catalog grows, run `/plugin marketplace update sci-ai-enabler`.

### 2. Use it

Invoke it explicitly with the slash command, or just describe your problem in chat and the skill triggers on intent:

```
/composer:compose <describe what you're trying to do>
```

### 3. Try it — paste any of these

Each prompt exercises a different path through the Composer. Run them as-is to see how it behaves:

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

[About the Composer →](catalog/tools/composer.md){: .btn .btn-primary }
[New to plugins?](guide/plugins.md){: .btn }

Or browse the four sections directly, all kept current:

## [Catalog](catalog/) — what to install

Installable Claude components — Skills, MCP servers, Claude Code Plugins, and Claude.ai Connectors — that target life-science work. Browse by research area or by tool.

[Browse the catalog →](catalog/){: .btn .btn-primary }
[See all tools](catalog/tools/){: .btn }

## [Guide](guide/) — how the pieces fit together

Short, beginner-facing pages explaining Claude's component model: Skills, MCP servers, Plugins, Marketplaces, Connectors, and a decision tree for "I want to do X — which one?"

[Read the guide →](guide/){: .btn .btn-primary }

## [Autonomous AI scientists](autonomous-science/) — what's working in the lab

A tracker of named AI systems that take meaningful initiative in hypothesis generation, experiment design, or analysis — Google's Co-Scientist, FutureHouse's Robin, Stanford's Biomni, Sakana's AI Scientist, and others.

[See the landscape →](autonomous-science/){: .btn .btn-primary }
[Browse systems](autonomous-science/systems/){: .btn }

## [Recipes](recipes/) — what to actually do

A cookbook pairing concrete life-science problems with recommended assemblies of the cataloged components. Each recipe carries an evidence label, an availability tag, and a compute-requirements tag, and starts at the lowest rung of the simplicity ladder that solves the problem.

[Read recipes →](recipes/){: .btn .btn-primary }
[See coverage](recipes/summary.html){: .btn }

## [Shape this resource](contribute.html) — file an issue

The catalog, guide, tracker, and recipes grow in response to user input. If the cookbook doesn't answer your question, or you tried something and want to report back, [file an issue](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new/choose) using one of three short forms — no Markdown required. A bot replies in-thread within minutes; the next daily curator run ships any durable change and closes the issue with a direct link to the new page.

[How and why →](contribute.html){: .btn .btn-primary }
[File an issue](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new/choose){: .btn }

---

## Search

Use the search box at the top of every page to find a specific tool, system, or topic. Search runs across all three sections.

## Stay current

The catalog, guide, tracker, and recipes each refresh daily and post a notice to a pinned GitHub issue when content changes. Watch the [repository](https://github.com/scripps-ai-enablement/sci-ai-enabler) on GitHub to subscribe.
