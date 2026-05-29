# GitHub Inbound Responder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enable users to file structured recipe questions and feedback via GitHub Issue Forms; auto-reply in-thread (read-only Claude run) and queue durable work for the existing scheduled curators, which close the loop by commenting and closing the issue when the change ships.

**Architecture:** New isolated `responder.yml` workflow triggers on `issues.opened`, validates the issue came from one of three new Issue Forms, runs a Claude (Sonnet 4.6) read-only reply, and appends a one-line entry to either `recipes/curator-state.md` or `catalog/curator-state.md` under a new `## User requests (open)` section. The existing daily scheduled workflows (`recipes.yml`, `curate.yml`) consume that queue, ship the durable change, and a loop-closer step posts back and closes the issue.

**Tech Stack:** GitHub Actions YAML, `anthropics/claude-code-base-action`, `gh` CLI, shell (`bash`, `awk`, `jq`), GitHub Issue Forms (YAML schema), Just-the-docs (existing site).

**Reference spec:** `docs/superpowers/specs/2026-05-21-github-inbound-responder-design.md`

**Operating note:** This codebase is YAML/Markdown/shell, not application code. "Tests" here are linting (`yamllint`, `actionlint`), structural assertions on generated files, and manual end-to-end runs via `gh workflow run` and `gh issue create`. The plan calls for those explicitly instead of a unit-test framework.

---

## Pre-flight (Task 0)

### Task 0: Confirm tooling and branch

**Files:** none

- [ ] **Step 1: Confirm working directory and clean tree**

Run:
```bash
cd /Users/bgood/Documents/GitHub/sci-ai-enabler
git status
```
Expected: branch `main`, working tree clean (the spec commit `2d7cf39` already landed).

- [ ] **Step 2: Create a feature branch**

Run:
```bash
git checkout -b feat/inbound-responder
```
Expected: switches to new branch.

- [ ] **Step 3: Install / verify linting tools used in later tasks**

Run:
```bash
brew install yamllint actionlint 2>/dev/null || true
yamllint --version
actionlint -version
gh --version
```
Expected: each prints a version. If `actionlint` is missing on a CI runner, the plan's manual `gh workflow run` step still validates behavior end-to-end.

---

## Phase 1 — Forms and dropdown refresher

### Task 1: Add `config.yml` to disable blank issues and link to forms

**Files:**
- Create: `.github/ISSUE_TEMPLATE/config.yml`

- [ ] **Step 1: Create the config file**

```yaml
# .github/ISSUE_TEMPLATE/config.yml
blank_issues_enabled: false
contact_links:
  - name: General discussion
    url: https://github.com/scripps-ai-enablement/sci-ai-enabler/discussions
    about: For open-ended questions or chatter that doesn't fit a recipe request or feedback report.
```

- [ ] **Step 2: Lint**

Run:
```bash
yamllint .github/ISSUE_TEMPLATE/config.yml
```
Expected: clean output (or only warnings about line length — fine).

- [ ] **Step 3: Commit**

```bash
git add .github/ISSUE_TEMPLATE/config.yml
git commit -m "Disable blank issues; point them at Discussions"
```

---

### Task 2: Add `recipe-question.yml` Issue Form

**Files:**
- Create: `.github/ISSUE_TEMPLATE/recipe-question.yml`

- [ ] **Step 1: Create the form**

```yaml
# .github/ISSUE_TEMPLATE/recipe-question.yml
name: Ask a recipe question
description: "How should I do X? — we'll reply in-thread and queue a durable recipe for the next scheduled run."
title: "[Recipe question] "
labels: ["claude:recipe-question"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for asking. A bot will reply in this thread shortly with the best match from the existing cookbook. The next scheduled curator run (within ~24h) will write up a durable recipe page if one doesn't already exist.
  - type: textarea
    id: problem
    attributes:
      label: What are you trying to do?
      description: 1–3 sentences describing the scientific problem you're trying to solve and what "done" looks like for you.
      placeholder: "e.g., I have a counts matrix from a bulk RNA-seq experiment with 4 conditions and I want to run differential expression with proper batch correction."
    validations:
      required: true
  - type: dropdown
    id: subject_area
    attributes:
      label: Subject area
      description: Pick the closest match. If you're not sure, pick the last option.
      options:
        - Chemistry
        - Immunology and Microbiology
        - Integrative Structural and Computational Biology
        - Molecular and Cellular Biology
        - Neuroscience
        - Translational Medicine
        - Drug Repurposing and Discovery
        - I'm not sure
    validations:
      required: true
  - type: textarea
    id: tried
    attributes:
      label: What have you already tried? (optional)
      description: If you've already attempted something, share what worked or didn't. This helps the bot avoid suggesting paths you've ruled out.
```

- [ ] **Step 2: Lint**

Run:
```bash
yamllint .github/ISSUE_TEMPLATE/recipe-question.yml
```
Expected: clean.

- [ ] **Step 3: Sanity-check that GitHub parses the schema**

Push the branch and open it in the browser — `https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-question.yml` should render the form once the branch is pushed. (Skip if not yet pushing; validation happens in Task 8.)

- [ ] **Step 4: Commit**

```bash
git add .github/ISSUE_TEMPLATE/recipe-question.yml
git commit -m "Add 'Ask a recipe question' Issue Form"
```

---

### Task 3: Add `recipe-feedback.yml` Issue Form (initial static dropdown)

**Files:**
- Create: `.github/ISSUE_TEMPLATE/recipe-feedback.yml`

The dropdown of recipe slugs will be regenerated automatically by the refresher workflow in Task 5. This first version uses the current set of `recipes/items/*.md` slugs hard-coded so the form is usable from the moment it ships.

- [ ] **Step 1: Snapshot current recipe slugs**

Run:
```bash
ls recipes/items/*.md | grep -v index.md | xargs -n1 basename | sed 's/\.md$//'
```
Expected output (currently):
```
build-target-dossier
qc-single-cell-rna-seq
run-bulk-rnaseq-differential-expression
triage-new-preprints
```

- [ ] **Step 2: Create the form**

```yaml
# .github/ISSUE_TEMPLATE/recipe-feedback.yml
name: Share feedback on a recipe
description: "I tried recipe X and… — we'll reply in-thread and queue the feedback for the next scheduled run."
title: "[Recipe feedback] "
labels: ["claude:recipe-feedback"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for sharing your experience. Concrete details (commands you ran, errors, hardware, datasets) make the next curator run much more useful.
  - type: dropdown
    id: recipe
    attributes:
      label: Which recipe?
      description: Auto-synced from the cookbook. Pick "Not listed" if your feedback isn't about one of these.
      options:
        - build-target-dossier
        - qc-single-cell-rna-seq
        - run-bulk-rnaseq-differential-expression
        - triage-new-preprints
        - Not listed
    validations:
      required: true
  - type: dropdown
    id: sentiment
    attributes:
      label: How did it go?
      options:
        - worked great
        - worked but slow
        - got stuck
        - found a better way
        - something else
    validations:
      required: true
  - type: textarea
    id: details
    attributes:
      label: Tell us more
      description: 40–800 characters. Mention concrete details — commands, errors, dataset size, hardware, wall-clock.
      placeholder: "I ran the recipe on a 12-sample dataset; PyDESeq2 install failed on Mac M1 with X error, fixed by using the conda-forge build."
    validations:
      required: true
```

- [ ] **Step 3: Lint and commit**

```bash
yamllint .github/ISSUE_TEMPLATE/recipe-feedback.yml
git add .github/ISSUE_TEMPLATE/recipe-feedback.yml
git commit -m "Add 'Share feedback on a recipe' Issue Form"
```

---

### Task 4: Add `tool-feedback.yml` Issue Form (initial static dropdown)

**Files:**
- Create: `.github/ISSUE_TEMPLATE/tool-feedback.yml`

- [ ] **Step 1: Snapshot current tool slugs**

Run:
```bash
ls catalog/tools/*.md | grep -v index.md | xargs -n1 basename | sed 's/\.md$//' | sort
```
Capture the output — use it as the initial dropdown options.

- [ ] **Step 2: Create the form**

```yaml
# .github/ISSUE_TEMPLATE/tool-feedback.yml
name: Share feedback on a catalog tool
description: "I installed tool Y and… — we'll reply in-thread and queue the feedback for the next scheduled run."
title: "[Tool feedback] "
labels: ["claude:tool-feedback"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for the field report. The catalog's job is to be accurate about what's installable and what works; concrete reports keep it honest.
  - type: dropdown
    id: tool
    attributes:
      label: Which tool?
      description: Auto-synced from the catalog. Pick "Not listed" if your feedback isn't about one of these.
      options:
        # FILL FROM Step 1 output, sorted, plus "Not listed" as the final entry
        - Not listed
    validations:
      required: true
  - type: dropdown
    id: sentiment
    attributes:
      label: How did it go?
      options:
        - worked great
        - worked but slow
        - got stuck
        - found a better way
        - something else
    validations:
      required: true
  - type: textarea
    id: details
    attributes:
      label: Tell us more
      description: 40–800 characters. Mention concrete details — install path, OS, error messages, dataset.
    validations:
      required: true
```

Replace the `# FILL FROM Step 1 output` comment line with the actual slugs (one per line, indented with `- `). Keep `Not listed` as the final option.

- [ ] **Step 3: Lint and commit**

```bash
yamllint .github/ISSUE_TEMPLATE/tool-feedback.yml
git add .github/ISSUE_TEMPLATE/tool-feedback.yml
git commit -m "Add 'Share feedback on a catalog tool' Issue Form"
```

---

### Task 5: Add the dropdown refresher workflow

**Files:**
- Create: `.github/workflows/refresh-form-dropdowns.yml`
- Create: `.github/scripts/refresh-form-dropdowns.sh`

- [ ] **Step 1: Write the refresher script**

```bash
# .github/scripts/refresh-form-dropdowns.sh
#!/usr/bin/env bash
# Regenerate the `dropdown` block in recipe-feedback.yml and tool-feedback.yml
# from the current set of recipes/items/*.md and catalog/tools/*.md.
# Idempotent: writes nothing if content is unchanged.
set -euo pipefail

regen_form() {
  local form="$1"
  local items_glob="$2"
  local block_id="$3"   # the `id:` of the dropdown to replace

  # Collect slugs, sorted, excluding index.md
  local slugs
  slugs=$(ls $items_glob 2>/dev/null | grep -v '/index.md$' | xargs -n1 basename | sed 's/\.md$//' | sort)

  # Build the new options block as YAML lines (prefixed with 8 spaces for indent under `options:`)
  local opts
  opts=$(printf '        - %s\n' $slugs)
  opts="${opts}"$'\n        - Not listed'

  # In-place rewrite: replace the lines from `    id: $block_id` down to the next field id (or end of body),
  # specifically only the `options:` list. Use python for reliable YAML-ish edit.
  python3 - "$form" "$block_id" <<'PY' "$opts"
import re, sys, pathlib
path = pathlib.Path(sys.argv[1])
block_id = sys.argv[2]
new_opts = sys.argv[3]
text = path.read_text()

# Pattern: find the dropdown with the right id, then replace its `options:` body
pattern = re.compile(
    r"(    id:\s*" + re.escape(block_id) + r".*?options:\n)(?:        - .*\n)+",
    re.DOTALL,
)
new_text, n = pattern.subn(lambda m: m.group(1) + new_opts + "\n", text, count=1)
if n != 1:
    sys.stderr.write(f"ERROR: did not match exactly one options block for id={block_id} in {path}\n")
    sys.exit(1)
if new_text != text:
    path.write_text(new_text)
    print(f"updated {path}")
else:
    print(f"unchanged {path}")
PY
}

regen_form ".github/ISSUE_TEMPLATE/recipe-feedback.yml" "recipes/items/*.md" "recipe"
regen_form ".github/ISSUE_TEMPLATE/tool-feedback.yml"   "catalog/tools/*.md"  "tool"
```

Make it executable:
```bash
chmod +x .github/scripts/refresh-form-dropdowns.sh
```

- [ ] **Step 2: Smoke-test the script locally**

Run:
```bash
.github/scripts/refresh-form-dropdowns.sh
git diff .github/ISSUE_TEMPLATE/recipe-feedback.yml .github/ISSUE_TEMPLATE/tool-feedback.yml
```
Expected: either no diff (Task 3/4 already used the current slugs) or a diff that only reorders/adds slug lines under `options:` inside the right `dropdown` block. **If the diff touches anything else, fix the script before continuing.**

- [ ] **Step 3: Write the workflow**

```yaml
# .github/workflows/refresh-form-dropdowns.yml
name: Refresh Issue Form dropdowns

on:
  push:
    branches: [main]
    paths:
      - 'recipes/items/**'
      - 'catalog/tools/**'

permissions:
  contents: write

concurrency:
  group: refresh-form-dropdowns
  cancel-in-progress: true

jobs:
  refresh:
    # Skip runs whose head commit was made by this bot, to break the self-trigger loop.
    if: github.event.head_commit.author.email != 'form-refresher@users.noreply.github.com'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Regenerate dropdowns
        run: .github/scripts/refresh-form-dropdowns.sh
      - name: Commit if changed
        run: |
          if [ -z "$(git status --porcelain .github/ISSUE_TEMPLATE/)" ]; then
            echo "No dropdown changes."
            exit 0
          fi
          git config user.name "form-refresher[bot]"
          git config user.email "form-refresher@users.noreply.github.com"
          git add .github/ISSUE_TEMPLATE/recipe-feedback.yml .github/ISSUE_TEMPLATE/tool-feedback.yml
          git commit -m "Refresh Issue Form dropdowns"
          git push
```

- [ ] **Step 4: Lint and commit**

```bash
yamllint .github/workflows/refresh-form-dropdowns.yml
actionlint .github/workflows/refresh-form-dropdowns.yml
git add .github/scripts/refresh-form-dropdowns.sh .github/workflows/refresh-form-dropdowns.yml
git commit -m "Add dropdown refresher workflow + script"
```

---

## Phase 2 — Responder workflow

### Task 6: Write `RESPONDER_AGENT.md`

**Files:**
- Create: `RESPONDER_AGENT.md`

- [ ] **Step 1: Write the spec**

```markdown
# Life Science AI Responder

You are an in-thread responder. A user has filed a GitHub Issue using one of three forms; the workflow has invoked you with that issue's body and label. Your job is to leave one helpful comment on the issue and exit. You are **read-only on repo content** — never write or edit files. Use `gh issue comment` to post the reply.

## Identify intent from the auto-applied label

- `claude:recipe-question` — the user is asking how to do something.
- `claude:recipe-feedback` — the user is reporting how a specific recipe went.
- `claude:tool-feedback` — the user is reporting how a specific catalog tool went.

## Behavior contract

### For `claude:recipe-question`

1. Grep `recipes/items/*.md` for the strongest matches against the user's problem. Read the candidate pages.
2. If one or more strong matches exist (subject area and problem-class both align), open the reply with:
   > "The closest existing recipes are:"
   > followed by a bulleted list of links to the rendered Pages URLs (`https://scripps-ai-enablement.github.io/sci-ai-enabler/recipes/items/<slug>.html`) with a one-line "use this when…" for each.
3. If no strong match exists, give a best-effort answer drawn from `catalog/tools/*.md`. Name only tools that have a `catalog/tools/<slug>.md` page; **never invent a tool**.
4. Always close with: "I've queued this so the recipe assembler can write it up properly in the next scheduled run."

### For `claude:recipe-feedback` and `claude:tool-feedback`

1. Read the relevant `recipes/items/<slug>.md` or `catalog/tools/<slug>.md` page.
2. Paraphrase the feedback in one sentence to confirm you understood it. Link to the page.
3. If the feedback is "got stuck" or "something else", offer 1–2 concrete troubleshooting pointers drawn from the page's content (not invented).
4. Close with: "Queued for the next curator run."

## Hard rules

- Never claim a tool exists that isn't in `catalog/tools/`.
- Never recommend a recipe that isn't in `recipes/items/`.
- Never write or edit files. Your only side effect is one `gh issue comment` call.
- Always end the reply with **exactly one** trailer line in one of these forms:

```
<!-- queue: recipes | question="<original question, ≤200 chars, double-quotes escaped>" | author=@<login> | issue=<number> -->
<!-- queue: recipes | feedback-on=<recipe-slug> | sentiment=<dropdown choice> | author=@<login> | issue=<number> -->
<!-- queue: catalog | feedback-on=<tool-slug> | sentiment=<dropdown choice> | author=@<login> | issue=<number> -->
```

The post-step parses the **last** `<!-- queue: ... -->` line in your most recent comment. If you write multiple queue trailers, only the last one is consumed.

## Tone

- Helpful, terse, second person. No marketing, no apology, no emoji.
- Lead with the answer; explanation follows.
- If you cannot answer (e.g., the user's question is out of scope), say so plainly, name what's missing from the catalog, and still emit a trailer so the curator sees the request.

## Wall-clock

You have 6 minutes. Spend it on reading the right files and writing one good comment — not on exhaustive searches.
```

- [ ] **Step 2: Commit**

```bash
git add RESPONDER_AGENT.md
git commit -m "Add responder agent spec"
```

---

### Task 7: Seed the `## User requests (open)` sections in both curator-state files

**Files:**
- Modify: `recipes/curator-state.md`
- Modify: `catalog/curator-state.md`

- [ ] **Step 1: Add the two new sections to `recipes/curator-state.md`**

Insert immediately after the `## Missing components` section (which is the last section today). Final tail of the file should read:

```markdown
## Missing components

_None._

## User requests (open)

_None._

## User requests (closed this run)

_None._
```

- [ ] **Step 2: Add the same two sections to `catalog/curator-state.md`**

Insert immediately after that file's last section. Same `_None._` placeholders.

- [ ] **Step 3: Verify with grep**

Run:
```bash
grep -n "User requests" recipes/curator-state.md catalog/curator-state.md
```
Expected: four hits (two per file).

- [ ] **Step 4: Commit**

```bash
git add recipes/curator-state.md catalog/curator-state.md
git commit -m "Seed 'User requests' sections in both curator-state files"
```

---

### Task 8: Write the responder workflow skeleton (no Claude call yet)

**Files:**
- Create: `.github/workflows/responder.yml`

This task gets the trigger, label filtering, kill switch, length cap, and spam check working **without** invoking Claude. It will simply comment "skeleton OK" on any qualifying issue. The Claude call lands in Task 9.

- [ ] **Step 1: Write the skeleton workflow**

```yaml
# .github/workflows/responder.yml
name: Responder

on:
  issues:
    types: [opened]

permissions:
  contents: write
  issues: write

concurrency:
  group: responder-${{ github.event.issue.number }}
  cancel-in-progress: false

jobs:
  respond:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Repo-level kill switch
        env:
          DISABLED: ${{ vars.RESPONDER_DISABLED }}
        run: |
          if [ -n "${DISABLED}" ]; then
            echo "RESPONDER_DISABLED is set; exiting."
            exit 0
          fi

      - name: Form check (label must be present)
        id: formcheck
        env:
          LABELS: ${{ toJson(github.event.issue.labels) }}
        run: |
          MATCH=$(echo "$LABELS" | jq -r '.[].name' | grep -E '^claude:(recipe-question|recipe-feedback|tool-feedback)$' | head -1)
          if [ -z "$MATCH" ]; then
            echo "No claude:* form label on this issue; exiting silently."
            echo "skip=true" >> "$GITHUB_OUTPUT"
            exit 0
          fi
          echo "label=$MATCH" >> "$GITHUB_OUTPUT"

      - name: Spam-label check
        if: steps.formcheck.outputs.skip != 'true'
        env:
          LABELS: ${{ toJson(github.event.issue.labels) }}
        run: |
          if echo "$LABELS" | jq -r '.[].name' | grep -q '^spam$'; then
            echo "Issue is labeled spam; exiting silently."
            exit 0
          fi

      - name: Body-length cap
        if: steps.formcheck.outputs.skip != 'true'
        id: lencheck
        env:
          BODY: ${{ github.event.issue.body }}
          GH_TOKEN: ${{ github.token }}
          REPO: ${{ github.repository }}
          NUM: ${{ github.event.issue.number }}
        run: |
          LEN=${#BODY}
          echo "Body length: $LEN"
          if [ "$LEN" -gt 4000 ]; then
            gh issue comment "$NUM" --repo "$REPO" --body "Please shorten the description to under 4000 characters and reopen — the responder bounds its input size."
            echo "skip=true" >> "$GITHUB_OUTPUT"
          fi

      - name: Checkout (only if we'll actually respond)
        if: steps.formcheck.outputs.skip != 'true' && steps.lencheck.outputs.skip != 'true'
        uses: actions/checkout@v4

      - name: Skeleton reply (placeholder for Claude call in Task 9)
        if: steps.formcheck.outputs.skip != 'true' && steps.lencheck.outputs.skip != 'true'
        env:
          GH_TOKEN: ${{ github.token }}
          REPO: ${{ github.repository }}
          NUM: ${{ github.event.issue.number }}
          LABEL: ${{ steps.formcheck.outputs.label }}
        run: |
          gh issue comment "$NUM" --repo "$REPO" --body "Responder skeleton received label $LABEL. (Claude reply lands in Task 9.)"
```

- [ ] **Step 2: Lint**

```bash
yamllint .github/workflows/responder.yml
actionlint .github/workflows/responder.yml
```

- [ ] **Step 3: Commit, push the branch, and merge to main for end-to-end test**

Issue Forms and `issues.opened` triggers must be on `main` to actually fire. Push the branch and open a PR for review; merge after a self-review. (For solo work: `git push -u origin feat/inbound-responder` then `gh pr create` and self-merge once the workflow files are validated.)

```bash
git add .github/workflows/responder.yml
git commit -m "Add responder workflow skeleton (no Claude call yet)"
```

- [ ] **Step 4: End-to-end smoke test (requires merge to main)**

After merging:
```bash
gh issue create --title "[Recipe question] Smoke test for skeleton" \
  --body "How do I run RNA-seq differential expression on a small counts matrix?" \
  --label "claude:recipe-question"
```
Then watch:
```bash
gh run watch
```
Expected: workflow runs, comments "Responder skeleton received label claude:recipe-question." on the issue. Close the test issue afterward.

If the smoke test fails, fix and re-run before proceeding to Task 9.

---

### Task 9: Add the Claude run + trailer-parse step

**Files:**
- Modify: `.github/workflows/responder.yml`

- [ ] **Step 1: Replace the "Skeleton reply" step with the Claude run and post-processing**

In `.github/workflows/responder.yml`, **delete** the `- name: Skeleton reply (placeholder for Claude call in Task 9)` step and **append** the following steps in its place:

```yaml
      - name: Compose prompt
        if: steps.formcheck.outputs.skip != 'true' && steps.lencheck.outputs.skip != 'true'
        env:
          ISSUE_BODY: ${{ github.event.issue.body }}
          ISSUE_TITLE: ${{ github.event.issue.title }}
          ISSUE_NUM: ${{ github.event.issue.number }}
          ISSUE_AUTHOR: ${{ github.event.issue.user.login }}
          LABEL: ${{ steps.formcheck.outputs.label }}
        run: |
          {
            cat RESPONDER_AGENT.md
            echo ""
            echo "---"
            echo ""
            echo "## This issue"
            echo "- Number: #${ISSUE_NUM}"
            echo "- Author: @${ISSUE_AUTHOR}"
            echo "- Label: ${LABEL}"
            echo "- Title: ${ISSUE_TITLE}"
            echo ""
            echo "### Body"
            echo ""
            echo "${ISSUE_BODY}"
            echo ""
            echo "---"
            echo ""
            echo "## Available context (read with Read / Glob / Grep as needed)"
            echo ""
            echo "- \`recipes/items/\` — existing recipe pages"
            echo "- \`catalog/tools/\` — installable components"
            echo "- \`autonomous-science/systems/\` — named systems"
            echo ""
            echo "Post your reply with:"
            echo "  gh issue comment ${ISSUE_NUM} --repo ${{ github.repository }} --body-file <path>"
            echo ""
            echo "End the reply with exactly one trailer line per RESPONDER_AGENT.md."
          } > .responder-prompt.md

      - uses: anthropics/claude-code-base-action@e8132bc5e637a42c27763fc757faa37e1ee43b34
        if: steps.formcheck.outputs.skip != 'true' && steps.lencheck.outputs.skip != 'true'
        with:
          prompt_file: .responder-prompt.md
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: claude-sonnet-4-6
          timeout_minutes: "6"
          allowed_tools: "Read,Glob,Grep,Bash(gh issue comment:*)"

      - name: Parse trailer and append to queue
        if: steps.formcheck.outputs.skip != 'true' && steps.lencheck.outputs.skip != 'true'
        env:
          GH_TOKEN: ${{ github.token }}
          REPO: ${{ github.repository }}
          NUM: ${{ github.event.issue.number }}
          AUTHOR: ${{ github.event.issue.user.login }}
          LABEL: ${{ steps.formcheck.outputs.label }}
          TITLE: ${{ github.event.issue.title }}
        run: |
          rm -f .responder-prompt.md
          # Fetch the most recent comment authored by github-actions on this issue.
          LATEST=$(gh api "repos/${REPO}/issues/${NUM}/comments" \
            --jq '[.[] | select(.user.login == "github-actions[bot]")] | last | .body // empty')

          # Extract the last queue trailer line.
          TRAILER=$(printf '%s\n' "$LATEST" | grep -E '^<!--\s*queue:' | tail -n 1 || true)

          # Determine target file: trailer says recipes|catalog, fallback derives from label.
          if [ -n "$TRAILER" ]; then
            case "$TRAILER" in
              *"queue: catalog"*) TARGET="catalog/curator-state.md" ;;
              *)                  TARGET="recipes/curator-state.md" ;;
            esac
            # Strip the <!-- --> wrappers for the bullet form.
            INNER=$(printf '%s' "$TRAILER" | sed -E 's/^<!--\s*//; s/\s*-->$//')
            BULLET="- [#${NUM} @${AUTHOR} $(date -u +%Y-%m-%d)] ${INNER}"
          else
            # Fallback: bot didn't emit a trailer; synthesize a minimal entry from the label.
            case "$LABEL" in
              claude:tool-feedback) TARGET="catalog/curator-state.md" ;;
              *)                    TARGET="recipes/curator-state.md" ;;
            esac
            SAFE_TITLE=$(printf '%s' "$TITLE" | tr '\n' ' ' | cut -c1-200)
            BULLET="- [#${NUM} @${AUTHOR} $(date -u +%Y-%m-%d)] (no trailer emitted; needs curator triage) title=\"${SAFE_TITLE}\" label=${LABEL}"
          fi

          # Append under "## User requests (open)" — replace the "_None._" placeholder if present,
          # otherwise insert the bullet immediately before "## User requests (closed this run)".
          python3 - "$TARGET" "$BULLET" <<'PY'
          import re, sys, pathlib
          path = pathlib.Path(sys.argv[1])
          bullet = sys.argv[2]
          text = path.read_text()
          marker_open = "## User requests (open)"
          marker_closed = "## User requests (closed this run)"
          if marker_open not in text or marker_closed not in text:
              sys.stderr.write(f"ERROR: required sections missing in {path}\n")
              sys.exit(1)
          # Slice out the (open) block.
          start = text.index(marker_open)
          end = text.index(marker_closed)
          block = text[start:end]
          # Drop a leading "_None._" placeholder if present.
          new_block = re.sub(r"_None\._\s*\n", "", block, count=1)
          # Ensure block ends with a blank line, then append the bullet + blank.
          if not new_block.endswith("\n"):
              new_block += "\n"
          new_block = new_block.rstrip() + "\n\n" + bullet + "\n\n"
          path.write_text(text[:start] + new_block + text[end:])
          print(f"appended to {path}")
          PY

          git config user.name "responder-bot[bot]"
          git config user.email "responder-bot@users.noreply.github.com"
          git add "$TARGET"
          git commit -m "auto-queue: issue #${NUM}"
          git pull --rebase origin main
          git push
```

- [ ] **Step 2: Lint**

```bash
yamllint .github/workflows/responder.yml
actionlint .github/workflows/responder.yml
```

- [ ] **Step 3: Commit, push, merge to main**

```bash
git add .github/workflows/responder.yml
git commit -m "Wire Claude reply and queue append into responder workflow"
```

Then push and merge as in Task 8.

- [ ] **Step 4: End-to-end smoke test**

```bash
gh issue create --title "[Recipe question] How do I QC a single-cell dataset?" \
  --body "I have a 10x h5 file with about 8000 cells and I want a first-pass QC before downstream analysis. Mostly running on a laptop." \
  --label "claude:recipe-question"
gh run watch
```
Expected: workflow runs, Claude comments in-thread (should mention `qc-single-cell-rna-seq`), a follow-up commit appears on `main` adding a bullet under `## User requests (open)` in `recipes/curator-state.md`.

Verify the queue line:
```bash
git pull
grep -A 5 "User requests (open)" recipes/curator-state.md
```

If the trailer fallback fires (no `<!-- queue: ... -->` from the bot), the bullet will say "(no trailer emitted; needs curator triage)". Both paths are acceptable — the fallback is the safety net.

Close the test issue afterward.

---

## Phase 3 — Scheduler queue-consumption and loop-closer

### Task 10: Update `AGENT.md` to consume `## User requests (open)`

**Files:**
- Modify: `AGENT.md`

- [ ] **Step 1: Append a new section to `AGENT.md`**

Add at the end of the file:

```markdown
## User requests (consumed each run)

`catalog/curator-state.md` has a `## User requests (open)` section that the inbound responder workflow appends to whenever a user files `claude:tool-feedback`. Each entry looks like:

```
- [#NN @author 2026-MM-DD] queue: catalog | feedback-on=<tool-slug> | sentiment=<choice> | author=@x | issue=NN
```

Or, if the responder fell back without a trailer:

```
- [#NN @author 2026-MM-DD] (no trailer emitted; needs curator triage) title="…" label=claude:tool-feedback
```

**Each run, process every entry in `## User requests (open)`:**

1. Read the linked tool page (`catalog/tools/<tool-slug>.md`).
2. Apply the appropriate update based on `sentiment`:
   - `worked great` — consider bumping `availability` evidence in **Notes** and refresh `last_verified`. Add a one-line field-report note in **Notes** if it adds signal.
   - `worked but slow` — add a perf note in **Notes**; do not change availability.
   - `got stuck` — investigate. If credible, add to **Notes** with the workaround if the user supplied one. If the install path appears broken, flag the tool in `## Flagged for review`.
   - `found a better way` — record in **Notes**; if the better path is a different cataloged tool, link it.
   - `something else` — read the issue body via `gh issue view <NN>` and exercise judgment.
3. For `(no trailer emitted; needs curator triage)` entries, read the issue body via `gh issue view <NN>` and decide what to do (often: leave alone and let the next run reconsider; or flag the request as unactionable).
4. **Move each processed entry** from `## User requests (open)` to `## User requests (closed this run)` and append `→ <result note>` describing what shipped or why nothing did. Example:

```
- [#43 @bob 2026-05-21] queue: catalog | feedback-on=pydeseq2 | sentiment=got-stuck | author=@bob | issue=43 → added Mac M1 conda-forge workaround to pydeseq2 Notes; last_verified bumped.
```

Entries not actioned this run stay in `## User requests (open)` and are retried next run. If `## User requests (open)` is empty after processing, leave the section as `_None._`.

Do not delete `## User requests (closed this run)` entries — the loop-closer step in `curate.yml` reads them after the curator agent exits and resets the section to `_None._` itself.
```

- [ ] **Step 2: Commit**

```bash
git add AGENT.md
git commit -m "Teach catalog curator to consume the user-requests queue"
```

---

### Task 11: Update `RECIPE_AGENT.md` to consume `## User requests (open)`

**Files:**
- Modify: `RECIPE_AGENT.md`

- [ ] **Step 1: Append a new section to `RECIPE_AGENT.md`**

Add at the end of the file (same structure as Task 10, adapted for recipes):

```markdown
## User requests (consumed each run)

`recipes/curator-state.md` has a `## User requests (open)` section that the inbound responder workflow appends to whenever a user files `claude:recipe-question` or `claude:recipe-feedback`. Each entry looks like one of:

```
- [#NN @author 2026-MM-DD] queue: recipes | question="…" | author=@x | issue=NN
- [#NN @author 2026-MM-DD] queue: recipes | feedback-on=<recipe-slug> | sentiment=<choice> | author=@x | issue=NN
- [#NN @author 2026-MM-DD] (no trailer emitted; needs curator triage) title="…" label=claude:recipe-…
```

**Each run, process every entry in `## User requests (open)`:**

1. For a `question=` entry: check if an existing recipe in `recipes/items/` already covers it.
   - If yes, no new page is needed; record that and close.
   - If no, write a new recipe page following the schema in this file. Stay under the simplicity-ladder rule. The recipe gets `Proposed` evidence unless you find a peer-reviewed or preprint source via the `papers` MCP that documents the assembly.
2. For a `feedback-on=` entry: read the named `recipes/items/<recipe-slug>.md` and apply the appropriate update based on `sentiment`:
   - `worked great` — refresh `last_verified`; consider promoting `Proposed` → `Reported` if this is the first field report. Add a one-line **Field reports** subsection under **Evidence** if it adds signal.
   - `worked but slow` — add a perf note under **Compute requirements**; do not change evidence.
   - `got stuck` — investigate. Add a one-line **Field reports** note. If multiple users hit the same wall, flag the recipe in `## Flagged for review` and consider raising the rung on the simplicity ladder.
   - `found a better way` — read the issue body via `gh issue view <NN>`. If the better path uses different cataloged tools, update **Alternatives considered** or write a sibling recipe.
   - `something else` — read the issue body and exercise judgment.
3. For `(no trailer emitted; needs curator triage)` entries, read the issue body via `gh issue view <NN>` and decide what to do.
4. **Move each processed entry** from `## User requests (open)` to `## User requests (closed this run)` and append `→ <result note>` describing what shipped or why nothing did.

Entries not actioned this run stay in `## User requests (open)` and are retried next run. The loop-closer step in `recipes.yml` reads `## User requests (closed this run)` after you exit and resets the section to `_None._` itself.

The soft cap of **≤ 3 new recipes per run** still applies. User-requested new recipes count toward it but get priority over the directed-pass picks.
```

- [ ] **Step 2: Commit**

```bash
git add RECIPE_AGENT.md
git commit -m "Teach recipes curator to consume the user-requests queue"
```

---

### Task 12: Add the loop-closer step to `recipes.yml`

**Files:**
- Modify: `.github/workflows/recipes.yml`

- [ ] **Step 1: Append a loop-closer step after the existing "Commit, push, and notify" step**

In `.github/workflows/recipes.yml`, after the existing final step, append:

```yaml
      - name: Close user-request issues that shipped this run
        env:
          GH_TOKEN: ${{ github.token }}
          REPO: ${{ github.repository }}
          SERVER_URL: ${{ github.server_url }}
        run: |
          STATE="recipes/curator-state.md"
          [ -f "$STATE" ] || exit 0

          # Extract the (closed this run) block.
          BLOCK=$(awk '
            /^## User requests \(closed this run\)/ { capture=1; next }
            /^## / && capture { exit }
            capture
          ' "$STATE")

          if [ -z "$BLOCK" ] || echo "$BLOCK" | grep -q '^_None\._'; then
            echo "No closed user requests this run."
            exit 0
          fi

          SHA=$(git rev-parse HEAD)
          COMMIT_URL="${SERVER_URL}/${REPO}/commit/${SHA}"

          # For each line with an issue number, comment and close.
          while IFS= read -r LINE; do
            NUM=$(printf '%s' "$LINE" | grep -oE 'issue=[0-9]+' | head -1 | cut -d= -f2)
            if [ -z "$NUM" ]; then
              # Fallback: try the "[#NN ...]" prefix.
              NUM=$(printf '%s' "$LINE" | grep -oE '\[#[0-9]+' | head -1 | tr -d '[#')
            fi
            [ -z "$NUM" ] && continue
            RESULT=$(printf '%s' "$LINE" | sed -E 's/.*→ //')
            gh issue comment "$NUM" --repo "$REPO" --body "Shipped in ${COMMIT_URL}. ${RESULT}"$'\n\nClosing — feel free to reopen if this missed the mark.' || true
            gh issue close "$NUM" --repo "$REPO" --reason completed || true
          done <<< "$BLOCK"

          # Reset the (closed this run) section to _None._ and commit.
          python3 - "$STATE" <<'PY'
          import re, pathlib, sys
          path = pathlib.Path(sys.argv[1])
          text = path.read_text()
          pattern = re.compile(
              r"(## User requests \(closed this run\)\n\n)(?:.*?)(\n## |\Z)",
              re.DOTALL,
          )
          new_text, n = pattern.subn(lambda m: m.group(1) + "_None._\n" + m.group(2), text, count=1)
          if n == 1 and new_text != text:
              path.write_text(new_text)
              print("reset (closed this run) to _None._")
          PY

          if ! git diff --quiet "$STATE"; then
            git add "$STATE"
            git commit -m "loop-closed: reset closed-this-run section"
            git pull --rebase origin main
            git push
          fi
```

- [ ] **Step 2: Lint**

```bash
yamllint .github/workflows/recipes.yml
actionlint .github/workflows/recipes.yml
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/recipes.yml
git commit -m "Add loop-closer step to recipes workflow"
```

---

### Task 13: Mirror the loop-closer in `curate.yml`

**Files:**
- Modify: `.github/workflows/curate.yml`

- [ ] **Step 1: Append the same loop-closer step to `curate.yml`**

Identical to Task 12's step but with `STATE="catalog/curator-state.md"`. Paste the entire `- name: Close user-request issues that shipped this run` block at the end of the `curate.yml` job, changing only the `STATE` variable.

- [ ] **Step 2: Lint**

```bash
yamllint .github/workflows/curate.yml
actionlint .github/workflows/curate.yml
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/curate.yml
git commit -m "Add loop-closer step to curate workflow"
```

---

### Task 14: End-to-end test of the queue + loop-closer

**Files:** none (manual validation)

- [ ] **Step 1: Push and merge the branch to main**

```bash
git push -u origin feat/inbound-responder
gh pr create --title "Inbound responder: forms + responder + queue + loop-closer" \
  --body "Implements docs/superpowers/specs/2026-05-21-github-inbound-responder-design.md"
# self-review then:
gh pr merge --squash --auto
```

- [ ] **Step 2: File a test recipe question on `main`**

```bash
gh issue create --title "[Recipe question] How do I score variants from clinical sequencing data?" \
  --body "I have a VCF from a clinical sequencing run and want to prioritize variants by gene + cancer relevance." \
  --label "claude:recipe-question"
```
Wait for the responder to comment (~2–4 min) and verify a bullet appears under `## User requests (open)` in `recipes/curator-state.md` (via `git pull && grep`).

- [ ] **Step 3: Trigger a scheduled run on demand**

```bash
gh workflow run recipes.yml -f scope=all
gh run watch
```
Expected: the recipes curator runs, processes the queued entry (likely defers it to a new recipe or links to an existing one), moves it to `## User requests (closed this run)`, then the loop-closer step comments on the issue with the commit URL and closes the issue. The next commit (`loop-closed: ...`) resets `(closed this run)` back to `_None._`.

- [ ] **Step 4: Verify on the issue thread**

Run:
```bash
gh issue view <NN>
```
Expected: at least two bot comments (responder + loop-closer) and state `closed`.

If any step fails, debug from the workflow logs and patch.

---

## Phase 4 — Footer links on user-facing pages

### Task 15: Add a "Got a question?" footer to `recipes/README.md`

**Files:**
- Modify: `recipes/README.md`

- [ ] **Step 1: Append the footer**

Add at the bottom of `recipes/README.md`:

```markdown
---

## Got a question or feedback?

Use one of our Issue Forms — no Markdown knowledge required:

- [Ask a recipe question](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-question.yml) — "How should I do X?"
- [Share feedback on a recipe](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml) — "I tried X and…"
- [Share feedback on a catalog tool](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml) — "I installed Y and…"

A bot replies in-thread shortly; the next daily curator run ships any durable changes and closes the issue.
```

- [ ] **Step 2: Commit**

```bash
git add recipes/README.md
git commit -m "Link Issue Forms from the recipes landing page"
```

---

### Task 16: Add the cycle explanation to `about.md`

**Files:**
- Modify: `about.md`

- [ ] **Step 1: Append a section to `about.md`**

Add at the bottom:

```markdown
## How user requests are handled

Two types of inbound flow are accepted via GitHub Issue Forms: **recipe questions** ("How should I do X?") and **feedback** on a recipe or catalog tool ("I tried X and…").

When you open an issue with one of the forms, a responder bot reads the issue, leaves an in-thread reply within a few minutes (linking the closest existing recipes or tools), and adds the request to the curator's work queue. The next daily scheduled curator run (~24h) ships any durable change — a new recipe, an updated tool note, a flag — and closes the issue with a commit link. If a request needs more than one run to address, it stays in the queue and is retried.

The bot that replies in-thread is **read-only on the repository**; only the scheduled curator agents change content files. That keeps the existing evidence and simplicity-ladder rules in force on every durable change.
```

- [ ] **Step 2: Commit**

```bash
git add about.md
git commit -m "Document the user-requests cycle in about page"
```

---

### Task 17: Add footer links to each `catalog/<category>.md` page

**Files:**
- Modify: `catalog/chemistry.md`
- Modify: `catalog/immunology-microbiology.md`
- Modify: `catalog/structural-computational-biology.md`
- Modify: `catalog/molecular-cellular-biology.md`
- Modify: `catalog/neuroscience.md`
- Modify: `catalog/translational-medicine.md`
- Modify: `catalog/drug-repurposing-discovery.md`

- [ ] **Step 1: Append the same footer to each category page**

To each of the seven files, append at the bottom:

```markdown
---

## Got feedback on a tool?

Use the [tool-feedback Issue Form](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml) — pick the tool from a dropdown, describe what happened. A bot replies in-thread shortly; the next daily catalog run incorporates the feedback.
```

Do this in a single commit. (Be careful not to insert it inside the Liquid `{% raw %}…{% endraw %}` loop — it must come **after** the `{% endraw %}` close tag at the file end.)

- [ ] **Step 2: Verify the loop isn't broken**

Run:
```bash
grep -c "endraw" catalog/chemistry.md
```
Expected: at least one match. If the build runs locally, run `bundle exec jekyll build` and confirm each category page still renders.

- [ ] **Step 3: Commit**

```bash
git add catalog/*.md
git commit -m "Link tool-feedback form from each catalog category page"
```

---

### Task 18: Final end-to-end smoke test and merge

**Files:** none

- [ ] **Step 1: Push and merge**

```bash
git push
gh pr create --title "Inbound responder: footer links" --body "Phase 4 footer links."
gh pr merge --squash --auto
```

(If the Phase 1–3 PR was already merged in Task 14, this is a follow-up PR on the same branch — or just push to `main` if working solo.)

- [ ] **Step 2: File one of each form type and verify the full loop for each**

```bash
gh issue create --title "[Recipe question] Final test" --body "A short final test." --label "claude:recipe-question"
gh issue create --title "[Recipe feedback] Final test" --body "I ran triage-new-preprints and it worked well on a stack of 12 papers." --label "claude:recipe-feedback"
gh issue create --title "[Tool feedback] Final test" --body "Installed pydeseq2 via the K-Dense skill; worked on Linux, failed on Mac M1 — fixed with conda-forge." --label "claude:tool-feedback"
```

Watch the responder run on each, verify queue entries appear in the right `curator-state.md` file, trigger the relevant scheduled workflow (`recipes.yml` or `curate.yml`), and confirm loop closure on each issue.

- [ ] **Step 3: Toggle the kill switch once to verify**

In **Settings → Secrets and variables → Actions → Variables**, set `RESPONDER_DISABLED=1`. File one more `claude:recipe-question` test issue. Expected: workflow runs, exits at step 1 without commenting. Unset the variable. Done.

---

## Definition of done

- All four Phases merged to `main`.
- The three Issue Forms are accessible from `https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new/choose` and render correctly.
- A user can file any of the three forms; the responder bot replies within ~6 min with a relevant comment ending in a queue trailer; a bullet appears in the right `curator-state.md`.
- The next scheduled `recipes.yml` or `curate.yml` run consumes the bullet, ships the durable change, and the loop-closer step comments on the issue with the commit link and closes the issue.
- The `RESPONDER_DISABLED` kill switch works.
- Footer links exist on `recipes/README.md`, `about.md`, and all seven `catalog/<category>.md` pages.
