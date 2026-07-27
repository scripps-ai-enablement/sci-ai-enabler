---
title: About
nav_order: 8
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

The curator prompts and workflow definitions are in the GitHub repository: [`AGENT.md`](https://github.com/scripps-ai-enablement/sci-ai-enabler/blob/main/AGENT.md), [`GUIDE_AGENT.md`](https://github.com/scripps-ai-enablement/sci-ai-enabler/blob/main/GUIDE_AGENT.md), [`COSCIENTIST_AGENT.md`](https://github.com/scripps-ai-enablement/sci-ai-enabler/blob/main/COSCIENTIST_AGENT.md), [`RECIPE_AGENT.md`](https://github.com/scripps-ai-enablement/sci-ai-enabler/blob/main/RECIPE_AGENT.md).

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

To re-run the on-demand fulfiller for a single queued user request — normally the
responder dispatches this automatically, so you only need it to retry a run that
errored or was superseded:

```sh
gh workflow run fulfill.yml -f issue=74 -f queue=recipes
gh workflow run fulfill.yml -f issue=80 -f queue=catalog
```

It refuses to run unless the issue is open and still listed under `## User requests (open)`
in that queue's `curator-state.md`, so re-dispatching a finished request is a no-op.
Setting the `FULFILL_DISABLED` repo variable turns immediate fulfillment off and reverts
to weekend-only processing.

## Reproducing this site

The repo lives at [`scripps-ai-enablement/sci-ai-enabler`](https://github.com/scripps-ai-enablement/sci-ai-enabler) and is rendered as a GitHub Pages site using the [just-the-docs](https://github.com/just-the-docs/just-the-docs) theme. One-time setup if you fork it:

1. Add an `ANTHROPIC_API_KEY` repository secret (**Settings → Secrets and variables → Actions**).
2. Enable GitHub Pages from the `main` branch root (**Settings → Pages → Source: Deploy from a branch → main / (root)**).
3. Subscribe to the **Weekly digest** issue (the `digest.yml` workflow opens it on its first run) for one summary email a week — or watch the repo, or the per-section "updates" issues, for finer-grained notifications.

## Updates

See the [updates archive](updates/) for the change history of each section.

## How user requests are handled

Two types of inbound flow are accepted via GitHub Issue Forms: **recipe questions** ("How should I do X?") and **feedback** on a recipe or catalog tool ("I tried X and…").

When you open an issue with one of the forms, a responder bot reads the issue, leaves an in-thread reply within a few minutes (linking the closest existing recipes or tools), and adds the request to the curator's work queue. It then **immediately dispatches an on-demand curator run** (`fulfill.yml`) scoped to that one request, rather than leaving it for the weekend cron. That run labels the issue `claude:working`, posts progress notes to the thread as it searches and decides, ships the durable change — a new recipe, an updated tool note, a flag — and closes the issue with a commit link and a rendered-page URL. If a request needs more wall-clock than one run, or depends on a component that isn't catalogued yet, the run says so in the thread and the request stays queued for the next scheduled pass, which retries it.

The bot that replies in-thread is **read-only on the repository**; only the curator agents change content files. The on-demand fulfiller is not a separate agent with looser rules — it is the same `RECIPE_AGENT.md` / `AGENT.md` curator, running the same evidence and simplicity-ladder rules, with its scope narrowed to a single queue entry and the ability to comment on the thread.
