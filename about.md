---
title: About
nav_order: 6
permalink: /about.html
---

# About this site

This site is an information resource for scientists, engineers, and clinicians who want to use Claude — and the broader ecosystem of AI scientific tools — for life-science work. It has four sections:

- [**Catalog**](catalog/) — installable Claude components: Skills, MCP servers, Plugins, and Connectors, grouped by research area.
- [**Guide**](guide/) — beginner-facing explanations of how each component type works.
- [**AI scientists**](autonomous-science/) — a tracker of named systems that take meaningful initiative in hypothesis generation, experiment design, or analysis.
- [**Recipes**](recipes/) — a cookbook pairing concrete problems with recommended assemblies of the cataloged components, with explicit evidence labels and availability/compute metadata.

## How it is maintained

The four sections are kept up to date by four independent scheduled curators running as [Claude Code GitHub Actions](https://github.com/anthropics/claude-code-base-action). Each runs daily on a GitHub-hosted runner with web search and fetch enabled, and each posts to a pinned tracking issue when a run produced changes.

| Section | Schedule (UTC) | Tracking issue |
|---|---|---|
| Catalog | Daily 07:00 | "Catalog updates" |
| Guide | Daily 08:00 | "Guide updates" |
| AI scientists | Daily 09:00 | "AI co-scientist updates" |
| Recipes | Daily 10:00 | "Recipes updates" |

The curator prompts and workflow definitions are in the GitHub repository: [`AGENT.md`](https://github.com/goodb/sci-ai-enabler/blob/main/AGENT.md), [`GUIDE_AGENT.md`](https://github.com/goodb/sci-ai-enabler/blob/main/GUIDE_AGENT.md), [`COSCIENTIST_AGENT.md`](https://github.com/goodb/sci-ai-enabler/blob/main/COSCIENTIST_AGENT.md), [`RECIPE_AGENT.md`](https://github.com/goodb/sci-ai-enabler/blob/main/RECIPE_AGENT.md).

## Running an update on demand

From the GitHub **Actions** tab → choose the workflow → **Run workflow**. You can optionally scope the run to a single category or topic.

From the terminal:

```sh
gh workflow run curate.yml                       # whole catalog
gh workflow run curate.yml -f category=chemistry # one category
gh workflow run guide.yml                        # whole guide
gh workflow run guide.yml -f topic=skills        # one topic
gh workflow run coscientist.yml                  # autonomous-science update
gh workflow run coscientist.yml -f scope=bootstrap  # re-seed from sources/
gh workflow run recipes.yml                      # whole cookbook
gh workflow run recipes.yml -f scope=chemistry   # one subject area
```

## Reproducing this site

The repo lives at [`goodb/sci-ai-enabler`](https://github.com/goodb/sci-ai-enabler) and is rendered as a GitHub Pages site using the [just-the-docs](https://github.com/just-the-docs/just-the-docs) theme. One-time setup if you fork it:

1. Add an `ANTHROPIC_API_KEY` repository secret (**Settings → Secrets and variables → Actions**).
2. Enable GitHub Pages from the `main` branch root (**Settings → Pages → Source: Deploy from a branch → main / (root)**).
3. Watch the repo (or the three "updates" issues once the first runs create them) to receive email notifications.

## Updates

See the [updates archive](updates/) for the change history of each section.

## How user requests are handled

Two types of inbound flow are accepted via GitHub Issue Forms: **recipe questions** ("How should I do X?") and **feedback** on a recipe or catalog tool ("I tried X and…").

When you open an issue with one of the forms, a responder bot reads the issue, leaves an in-thread reply within a few minutes (linking the closest existing recipes or tools), and adds the request to the curator's work queue. The next daily scheduled curator run (~24h) ships any durable change — a new recipe, an updated tool note, a flag — and closes the issue with a commit link. If a request needs more than one run to address, it stays in the queue and is retried.

The bot that replies in-thread is **read-only on the repository**; only the scheduled curator agents change content files. That keeps the existing evidence and simplicity-ladder rules in force on every durable change.
