---
title: Contribute
nav_order: 5
permalink: /contribute.html
---

# Help shape this resource

The catalog, guide, recipes, and AI-scientist tracker are kept up to date by automated curators that run daily. But *what* they cover is driven by the working scientists, engineers, and clinicians who use the site. Three lightweight Issue Forms let you tell the curators what to write next.

## Three things you can file

### Ask a recipe question — *"How should I do X?"*

[Open the form →](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-question.yml)

Use this when the cookbook doesn't already have a recipe for what you're trying to do. A bot replies in-thread within a few minutes pointing to the closest existing recipes or tools. The next daily Recipes curator run writes a durable recipe page if one doesn't exist yet, then comments on your issue with a direct link to the new page and closes it.

Good prompts here are concrete and goal-shaped: *"I have a counts matrix from a bulk RNA-seq experiment with batch effects across 4 sites — how should I run DE?"* — not *"how do I do bioinformatics?"*

### Share feedback on a recipe — *"I tried X and…"*

[Open the form →](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml)

Worked great, worked but slow, got stuck, found a better way, something else — every report tightens the evidence label on the recipe page, adds a field-report note, or flags the recipe for review if multiple people hit the same wall.

Concrete details are what make these reports useful: the commands you ran, dataset size, hardware, wall-clock, exact error messages, any workaround you found.

### Share feedback on a catalog tool — *"I installed Y and…"*

[Open the form →](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml)

Same idea, scoped to one tool from the catalog. This is how `last_verified` stays honest and how install-path notes accumulate across operating systems and Python versions. Mention OS, install path, errors, and any workarounds.

## What happens after you file

1. **Within minutes** — a bot reads your issue and posts an in-thread comment with the closest existing recipes or tools (or a best-effort answer if no good match exists), and queues your request for the next curator run.
2. **Within ~24h** — the next daily scheduled curator run (Recipes runs at 10:00 UTC; Catalog at 07:00 UTC) ships any durable change: a new recipe page, an updated tool note, an evidence-label bump, or a flag for review.
3. **At loop-close** — the curator posts a comment on your issue with a direct link to the rendered page and closes the issue. You'll get a GitHub notification when this happens.

If a request needs more than one run — for example because the curator wants to read a paper before publishing — it stays in the queue and is retried next run. Nothing gets dropped.

## What you need

- A GitHub account (free). [Sign up here](https://github.com/signup) if you don't have one.
- No Markdown knowledge required. The forms ask plain-text questions and dropdown choices.
- No special permissions. Anyone can file.

## What the bot can and can't do

The in-thread responder is **read-only on the site content** — it only reads existing pages and posts a comment. Durable changes are made by the scheduled curator agents, which run with the full evidence rules, simplicity ladder, and source-verification machinery applied. That keeps the rules consistent on every change, regardless of whether the trigger was a user request or the daily directed pass.

The bot will not invent tools or recipes that don't exist. If a question reaches beyond what's catalogued today, it'll say so plainly and queue the gap for the curator to consider in the next run.

## Other ways to engage

- **General discussion** — open-ended questions and chatter that don't fit a form belong in [Discussions](https://github.com/scripps-ai-enablement/sci-ai-enabler/discussions).
- **Track changes** — each section posts to a pinned tracking issue when a daily run produced changes. Watch the [repository](https://github.com/scripps-ai-enablement/sci-ai-enabler) on GitHub to subscribe by email.
- **See the machinery** — the [About](about.html) page describes the four scheduled curator agents and how the schedules are wired up.
