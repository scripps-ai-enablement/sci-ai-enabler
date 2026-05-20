---
title: About
nav_order: 5
permalink: /about.html
---

# About this site

This site is an information resource for scientists, engineers, and clinicians who want to use Claude — and the broader ecosystem of AI scientific tools — for life-science work. It has three sections:

- [**Catalog**](catalog/) — installable Claude components: Skills, MCP servers, Plugins, and Connectors, grouped by research area.
- [**Guide**](guide/) — beginner-facing explanations of how each component type works.
- [**AI scientists**](autonomous-science/) — a tracker of named systems that take meaningful initiative in hypothesis generation, experiment design, or analysis.

## How it is maintained

The three sections are kept up to date by three independent scheduled curators running as [Claude Code GitHub Actions](https://github.com/anthropics/claude-code-base-action). Each runs daily on a GitHub-hosted runner with web search and fetch enabled, and each posts to a pinned tracking issue when a run produced changes.

| Section | Schedule (UTC) | Tracking issue |
|---|---|---|
| Catalog | Daily 13:00 | "Catalog updates" |
| Guide | Daily 14:30 | "Guide updates" |
| AI scientists | Daily 16:00 | "AI co-scientist updates" |

The curator prompts and workflow definitions are in the GitHub repository: [`AGENT.md`](https://github.com/goodb/sci-ai-enabler/blob/main/AGENT.md), [`GUIDE_AGENT.md`](https://github.com/goodb/sci-ai-enabler/blob/main/GUIDE_AGENT.md), [`COSCIENTIST_AGENT.md`](https://github.com/goodb/sci-ai-enabler/blob/main/COSCIENTIST_AGENT.md).

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
```

## Reproducing this site

The repo lives at [`goodb/sci-ai-enabler`](https://github.com/goodb/sci-ai-enabler) and is rendered as a GitHub Pages site using the [just-the-docs](https://github.com/just-the-docs/just-the-docs) theme. One-time setup if you fork it:

1. Add an `ANTHROPIC_API_KEY` repository secret (**Settings → Secrets and variables → Actions**).
2. Enable GitHub Pages from the `main` branch root (**Settings → Pages → Source: Deploy from a branch → main / (root)**).
3. Watch the repo (or the three "updates" issues once the first runs create them) to receive email notifications.

## Updates

See the [updates archive](updates/) for the change history of each section.
