---
title: Contribute
nav_order: 7
permalink: /contribute.html
---

# Help shape this resource

The catalog, guide, recipes, and AI-scientist tracker are kept up to date by automated curators that run daily. But *what* they cover is driven by the working scientists, engineers, and clinicians who use the site. Four lightweight Issue Forms let you tell the curators what to write next.

## Four things you can file

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

### Request a new catalog tool — *"You're missing Z"*

[Open the form →](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-request.yml)

Use this when a tool you rely on isn't in the catalog yet. A bot replies in-thread — pointing you to the existing page if it's already covered, otherwise confirming it's been picked up. A Catalog curator run then evaluates it and, if it's in scope and installable, adds a tool page and closes your issue with a link. Include a repo/docs/PyPI URL and the install path if you know it — that's what lets the curator verify it fast.

## What happens after you file

Filing an issue starts a curator run on your request straight away — you're not waiting for the weekend batch.

1. **Within minutes** — a bot reads your issue and posts an in-thread comment with the closest existing recipes or tools (or a best-effort answer if no good match exists).
2. **Right after that** — a curator run starts on your request specifically. The issue gets a `claude:working` label, and the curator posts what it's doing in your thread as it goes: what it searched, what it found or ruled out, what it's about to write.
3. **Usually within the hour** — the durable change ships: a new recipe page, an updated tool note, an evidence-label bump, or a flag for review. The curator comments with the commit and a direct link to the rendered page, then closes the issue. You'll get a GitHub notification.

Your issue is only closed when there's a real answer — shipped, already covered, or a plainly stated no. It is never closed just because a run finished.

### When the answer needs something that isn't catalogued yet

The cookbook won't write a recipe from memory — that would hand you an install path nobody checked. But what counts as "catalogued" depends on what's missing:

- **A missing library** — something Claude Code can just `pip install` — is not a blocker. The recipe declares it as a dependency with an exact pinned version, its license, and the module to import, and that pinned install and import get **executed** in a clean container. You can browse everything the cookbook reaches for on the [library index](recipes/dependencies.html).
- **A missing Claude component** — a Skill, MCP server, plugin, or connector — *is* a blocker, because without it there's nothing for you to install.

So sometimes the honest answer is still "this is a good request, and one piece is missing."

When that happens your issue is **not closed**. It gets labelled `claude:blocked-on-catalog`, and the request is handed straight to the catalog curator, which evaluates the missing components right away against the usual bar (real, installable, license-clear, in scope). If they clear it, the request comes back to the recipe assembler automatically and the recipe gets written — all in your thread, with no action from you. If they don't clear it (no license, out of scope, unverifiable), you get told exactly why rather than a silent close.

Every scheduled curator pass also re-checks blocked requests, so a component catalogued later by any route still unblocks yours.

Requests that simply run out of time stay queued and are retried on the next scheduled pass (Catalog and Recipes both run through all seven subject areas each weekend). Nothing gets dropped.

## What you need

- A GitHub account (free). [Sign up here](https://github.com/signup) if you don't have one.
- No Markdown knowledge required. The forms ask plain-text questions and dropdown choices.
- No special permissions. Anyone can file.

## What the bot can and can't do

The in-thread responder that replies first is **read-only on the site content** — it only reads existing pages and posts a comment. Durable changes are made by the curator agents, with the full evidence rules, simplicity ladder, and source-verification machinery applied. The on-demand run triggered by your issue is the *same* curator agent under the *same* rules as the weekend pass, just scoped to your one request — responding fast doesn't lower the bar.

The bot will not invent tools or recipes that don't exist. If a question reaches beyond what's catalogued today, it'll say so plainly and record the gap rather than papering over it.

## Other ways to engage

- **General discussion** — open-ended questions and chatter that don't fit a form belong in [Discussions](https://github.com/scripps-ai-enablement/sci-ai-enabler/discussions).
- **Track changes** — the easiest way to follow along is the **[Weekly digest](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/29)**: one prioritized summary of the week's catalog, guide, tracker, and recipe activity, posted every Sunday. Open it and click **Subscribe** (top-right) to get it by email. For every change as it lands instead, watch the [repository](https://github.com/scripps-ai-enablement/sci-ai-enabler).
- **See the machinery** — the [About](about.html) page describes the four scheduled curator agents and how the schedules are wired up.
