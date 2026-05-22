# GitHub inbound responder — design

Status: draft, awaiting review
Date: 2026-05-21
Owner: @goodb

## Problem

Today the repository runs four scheduled Claude agents (catalog, guide, autonomous-science, recipes) that maintain the site outbound. There is no inbound path for users to ask questions or share feedback. We want to enable two new flows:

1. **Recipe requests** — "How should I do X?" (a working scientist with a problem in hand).
2. **Feedback** — "I tried recipe/tool Y and got stuck / it worked / there's a better way."

The repo is public, so the path must be friendly to non-expert GitHub users while remaining safe to run with an `ANTHROPIC_API_KEY` exposed to public traffic.

## Goals

- Non-expert users can file structured requests without writing Markdown.
- Each request gets an immediate, helpful in-thread reply.
- Durable site changes (new recipe, evidence-label updates, flags) flow through the existing scheduled curators, not the interactive responder.
- The loop closes back to the user: when a request ships, they're notified and the issue closes.
- Cost and abuse exposure is bounded by minimal, easy-to-tighten controls.

## Non-goals (v1)

- Web form on the Pages site (revisit if Issue Forms prove too unfriendly).
- Inbound forms for the Guide and Autonomous Science tracks (different shape of user input; defer until demand shows up).
- Per-author or repo-wide rate-limit counters (defer until traffic warrants).
- Static-first responder as cost optimization (Phase 2 on top of this).
- Multi-language form fields.

## Architecture

```
User → fills GitHub Issue Form → issue opens (with auto-applied label)
                                         │
                                         ▼
                       .github/workflows/responder.yml
                              (triggers on issues.opened)
                                         │
                            ┌────────────┴────────────┐
                            ▼                         ▼
                  form-check + body-length cap   if pass: Claude responds
                  (bail if missing label or       with in-thread comment
                   body too long; spam label      (read-only tools)
                   bails silently)                       │
                                                        ▼
                                       parse reply trailer & append a
                                       line to the right curator-state.md
                                       (recipes/ or catalog/) under
                                       `## User requests (open)`
                                                        │
                                                        ▼
                       next daily scheduled run consumes the queue,
                       commits the durable change, moves the queue
                       entry from (open) to (closed) with a result note;
                       loop-closer step comments + closes the issue
```

The interactive responder is **read-only on repo content**. Only the scheduled curator agents write to `catalog/tools/`, `recipes/items/`, and other site files. This preserves the existing safety properties of the scheduled runs (Opus model, full curator prompt, evidence rules, simplicity ladder).

## Components

### 1. Issue forms

Three forms under `.github/ISSUE_TEMPLATE/`, plus a `config.yml` that disables blank issues and links to the forms.

**`recipe-question.yml`** — "Ask how to do something"

| Field | Type | Required | Notes |
|---|---|---|---|
| What are you trying to do? | textarea | yes | 80–800 chars |
| Subject area | dropdown | yes | seven canonical categories + "I'm not sure" |
| What you've already tried | textarea | no | |

Auto-label: `claude:recipe-question`.

**`recipe-feedback.yml`** — "Share feedback on a recipe"

| Field | Type | Required | Notes |
|---|---|---|---|
| Which recipe? | dropdown | yes | populated from `recipes/items/*.md` slugs + "Not listed" |
| How did it go? | dropdown | yes | worked great / worked but slow / got stuck / found a better way / something else |
| Tell us more | textarea | yes | 40–800 chars |

Auto-label: `claude:recipe-feedback`.

**`tool-feedback.yml`** — "Share feedback on a catalog tool"

| Field | Type | Required | Notes |
|---|---|---|---|
| Which tool? | dropdown | yes | populated from `catalog/tools/*.md` slugs + "Not listed" |
| How did it go? | dropdown | yes | same set as recipe-feedback |
| Tell us more | textarea | yes | 40–800 chars |

Auto-label: `claude:tool-feedback`.

**Rationale for three forms instead of one:** non-experts answer concrete fielded questions ("which recipe?") much more reliably than open ones ("what's this about?"). Labels also let the workflow route by intent without parsing free text.

### 2. Form dropdown refresher

GitHub Issue Forms do not auto-sync with repo file listings. A small workflow keeps the recipe and tool dropdowns current.

**File:** `.github/workflows/refresh-form-dropdowns.yml`

**Trigger:** `push` to `main` affecting `recipes/items/**` or `catalog/tools/**`.

**Loop guard:** the workflow's commits use a bot author (`form-refresher[bot]`) and the workflow's `if:` skips runs whose head commit author matches that bot, preventing the refresh from triggering itself.

**What it does:** small shell script reads the current slugs in `recipes/items/*.md` and `catalog/tools/*.md`, regenerates the `dropdown` blocks in `recipe-feedback.yml` and `tool-feedback.yml`, and commits the change back to `main` if anything moved. Skip-on-no-change to avoid commit churn.

### 3. Responder workflow

**File:** `.github/workflows/responder.yml`

**Trigger:**
```yaml
on:
  issues:
    types: [opened]
```

Only `opened`. Not `edited` (cheap abuse vector). Not `labeled` (we don't want a maintainer label to re-trigger after a `spam` review).

**Permissions:** `issues: write` (comment), `contents: write` (append the queue line + push).

**Concurrency:** `group: responder-${{ github.event.issue.number }}`, `cancel-in-progress: false`. One in-flight response per issue.

**Steps:**

1. **Repo-level off switch.** Check the `RESPONDER_DISABLED` repository variable; exit 0 if set.
2. **Form check.** Bail if the issue is not labeled with one of `claude:recipe-question | claude:recipe-feedback | claude:tool-feedback`. Free-text issues are silently ignored (no comment — commenting on every random issue is its own DOS surface).
3. **Body-length cap.** If `length(body) > 4000`, post "Please shorten your description (the responder bounds prompt size) and reopen." and exit 0.
4. **Spam label check.** If a maintainer labeled the issue `spam` between trigger and run start, bail silently.
5. **Compose context-bounded prompt.** Write a `.run-prompt.md` containing the responder spec, the issue body and metadata (label, author, timestamp), and a file listing of `catalog/tools/`, `recipes/items/`, `autonomous-science/systems/`. The agent uses `Read`/`Grep`/`Glob` to pull only what it needs.
6. **Claude run.** Invoke `anthropics/claude-code-base-action`:
   - `model: claude-sonnet-4-6`
   - `timeout_minutes: "6"`
   - `allowed_tools: "Read,Glob,Grep,Bash(gh issue comment:*)"` — explicitly no `Write` or `Edit`.
7. **Parse trailer + queue.** Fetch the bot's most recent comment via `gh api`, extract the last `<!-- queue: ... -->` line, format it as a bullet, and append to the right `curator-state.md` under `## User requests (open)`. **Fallback:** if no trailer is found (bot violated the spec or the Claude run errored after commenting), synthesize a minimal queue entry from the issue label + title + author so nothing is silently dropped — the curator will see it next run and can decide what to do. Commit (`auto-queue: issue #NN`) and push.

### 4. Responder spec

**File:** `RESPONDER_AGENT.md` (~60 lines). Sibling to `AGENT.md` / `RECIPE_AGENT.md`.

**Behavior contract:**

- Identify intent from the auto-applied label.
- **For recipe-questions:** search `recipes/items/` for matches.
  - If one or more solid matches exist, lead with "The closest existing recipes are:" with links to the rendered Pages URLs.
  - If no good match, give a best-effort answer drawn from `catalog/tools/`. Name only tools that exist in `catalog/tools/`; never invent.
  - Always close with: "I've queued this so the recipe assembler can write it up properly in the next scheduled run."
- **For recipe/tool feedback:** paraphrase the feedback in one sentence to confirm understanding, link to the relevant page, and note "queued for the next curator run."
- **Hard rules:**
  - Never claim a tool exists that isn't in `catalog/tools/`.
  - Never recommend a recipe that isn't in `recipes/items/`.
  - Never write or edit files.
  - Always end the reply with one trailer line.

**Trailer formats:**

```
<!-- queue: recipes | question="<original question, ≤200 chars>" | author=@x | issue=NN -->
<!-- queue: recipes | feedback-on=<recipe-slug> | sentiment=<choice> | author=@x | issue=NN -->
<!-- queue: catalog | feedback-on=<tool-slug> | sentiment=<choice> | author=@x | issue=NN -->
```

**Model choice:** Sonnet 4.6 not Opus. These are short look-things-up answers; Sonnet is fast and accurate enough. Opus stays reserved for the scheduled jobs that author content.

### 5. Queue handoff

A new section in each of `recipes/curator-state.md` and `catalog/curator-state.md`:

```markdown
## User requests (open)

- [#42 @alice 2026-05-21] question="How do I dock an antibody to a viral spike?" — responder linked: build-target-dossier, triage-new-preprints. No exact match.
- [#43 @bob 2026-05-21] feedback-on=run-bulk-rnaseq-differential-expression sentiment=got-stuck — "PyDESeq2 failed on Mac M1; fixed by using conda-forge build."

## User requests (closed this run)

_(populated by the scheduled curator agent; consumed by the loop-closer step)_
```

The responder appends to `(open)`. The scheduled curator agent (per updated `AGENT.md` / `RECIPE_AGENT.md`) processes every entry in `(open)`, takes the appropriate action (write a new recipe, update an existing page, flag for review, defer with reason), and moves each entry to `(closed this run)` with a `→` note describing what shipped or why it didn't.

The curator agent stays in charge of judgment — when a request maps to an existing recipe, when it needs a new page, when it should be deferred again. The queue is just an input feed.

### 6. Loop closure

Added to each scheduled workflow's commit step (`recipes.yml`, `curate.yml`):

After `git push` succeeds, a small shell step parses the `## User requests (closed this run)` block from the committed `curator-state.md`, then for each entry with an `issue=NN` reference:

```sh
gh issue comment "$NUM" --body "Shipped in <commit-link>. See: <URL of the new/updated page>. Closing — feel free to reopen if this missed the mark."
gh issue close "$NUM"
```

Finally, the loop-closer empties the `(closed this run)` section back to `_None._` and commits that as a follow-up (`loop-closed: N issues`). This keeps `curator-state.md` from accumulating closed history; the issue thread is the audit trail.

If a scheduled run fails or skips a queue entry, the entry stays in `(open)` and is retried on the next run. No special retry plumbing required.

### 7. User-facing documentation

- Footer paragraph on `recipes/README.md` and each `catalog/<category>.md` page: "Got a question or feedback? Open an issue with one of [our forms](link)."
- One-paragraph addition to `about.md` explaining the ~24h durable-answer cycle.

## Cost and abuse posture

Minimal in v1. Defenses grow with need.

- Form check (free; rejects non-form issues).
- Body length cap (4000 chars; bounds prompt size).
- Spam label (maintainer escape hatch).
- Repo-level `RESPONDER_DISABLED` variable (kill switch).

Explicitly deferred until traffic shows the need: per-author daily counters, repo-wide daily counters, graceful-degrade behavior when caps trip.

## Files added / touched

| New | Touched |
|---|---|
| `.github/ISSUE_TEMPLATE/recipe-question.yml` | `recipes/curator-state.md` (new sections) |
| `.github/ISSUE_TEMPLATE/recipe-feedback.yml` | `catalog/curator-state.md` (new sections) |
| `.github/ISSUE_TEMPLATE/tool-feedback.yml` | `AGENT.md` (queue-processing instructions) |
| `.github/ISSUE_TEMPLATE/config.yml` | `RECIPE_AGENT.md` (queue-processing instructions) |
| `.github/workflows/responder.yml` | `.github/workflows/recipes.yml` (queue + loop-closer) |
| `.github/workflows/refresh-form-dropdowns.yml` | `.github/workflows/curate.yml` (queue + loop-closer) |
| `RESPONDER_AGENT.md` | `recipes/README.md` (footer link to forms) |
| | `catalog/<category>.md` × 7 (footer link to forms) |
| | `about.md` (one-paragraph cycle explanation) |

## Build order

Each step ships independently and leaves the system in a coherent state.

1. **Forms + dropdown refresher.** Front door ships as a no-op; maintainer can respond manually. Validates that the forms capture what we want.
2. **Responder workflow.** In-thread auto-reply lights up. Bot is read-only and queues into `curator-state.md`. Requests are acknowledged but the queue isn't consumed yet.
3. **Scheduler queue-consumption + loop-closer.** Extends `recipes.yml` and `curate.yml` (and the respective `AGENT.md` files) to read the queue, do the work, and close issues. Loop is complete.
4. **Footer links on user-facing pages.** Last, after the pipeline works end-to-end. Don't drive traffic to a half-built path.

If step 2 misbehaves, revert it; steps 1 and 3 still leave a working manual workflow (maintainer reads the form, edits the queue by hand, scheduled run picks it up).

## Open questions

None blocking. Items worth revisiting after v1 ships:

- If most recipe-questions can be answered by linking to one existing recipe, evaluate Option C (static-first responder) as a cost optimization.
- If Issue Form friction is real, evaluate a web form on the Pages site that deep-links to a pre-filled issue.
- If feedback velocity grows, evaluate auto-flagging negative feedback for review rather than waiting for the next scheduled run.
