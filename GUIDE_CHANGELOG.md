---
title: Guide updates
parent: Updates
nav_order: 2
permalink: /updates/guide.html
---

# Guide updates

Reverse-chronological log of changes to the [guide]({{ '/guide/' | relative_url }}). Newest at the top.

<!-- Curator appends new dated entries directly below this line. -->

Older entries live in [GUIDE_CHANGELOG_ARCHIVE.md](GUIDE_CHANGELOG_ARCHIVE.md).

## 2026-07-25

### Updated
- **[surfaces/claude-code] Claude Opus 5 is now the default (v2.1.219, 2026-07-24).** Replaced the Sonnet-5-default model line with Opus 5: `claude-opus-5`, 1M context, priced identically to Opus 4.8 ($5 / $25 per Mtok), with automatic fallback to Opus 4.8 when a safety classifier trips. Sonnet 5 and Opus 4.8 remain selectable. Grounded in [Introducing Claude Opus 5](https://www.anthropic.com/news/claude-opus-5) (2026-07-24) and the [Claude Code changelog](https://code.claude.com/docs/en/changelog) v2.1.219, both fetched this run.
- **[surfaces/claude-api] Opus 5 added to the model line and pitfalls.** Updated "Default model IDs change" so `claude-opus-5` is the current `opus` alias (1M context, thinking on by default, $5/$25 unchanged from Opus 4.8, on API/Bedrock/Vertex/Foundry); added Opus 5 to the `temperature`/`top_p`/`top_k` 400-rejection pitfall and a new pitfall on thinking-on-by-default (disabling above `high` effort → 400) plus the consumer-surface fallback to Opus 4.8. Grounded in the Opus 5 news post plus [The Decoder](https://the-decoder.com/anthropic-claims-its-new-claude-opus-5-delivers-near-fable-5-performance-at-half-the-token-price/) (2026-07-24) as secondary confirmation (the `whats-new-claude-opus-5` API doc 404s as of this run).
- **[surfaces/claude-science] De-pinned the model name.** Changed "Opus 4.8, Sonnet 5" to "the current Opus and Sonnet lines" so the generic statement doesn't go stale on each model launch.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebFetch of `claude.com/product/claude-code`: native installer canonical, no deprecation banner; Terminal / VS Code / JetBrains / web / Desktop / iOS / Android / Slack / GitHub surfaces unchanged. Changelog re-fetched: latest release **v2.1.220 (2026-07-25)**; v2.1.215–v2.1.220 mostly below the beginner threshold (`/verify` and `/code-review` no longer auto-run and now run as background subagents, `sandbox.filesystem.disabled` setting, emoji shortcode autocomplete, `--forward-subagent-text`, screen-reader deletion announcements, quadratic-slowdown fix) other than the Opus 5 default captured above.
- anthropic.com/news scanned — Economic Index connector (2026-07-22, all plans, one-click in the connectors directory), Claude for Teachers (2026-07-14), AI-for-Science rare-disease grants, funding/governance items — none meet the beginner cross-cutting / component bar for a new page. Economic Index is a single first-party connector already covered by the connectors page's "growing directory" framing.
- claude-surfaces.md, surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-tag.md — unchanged (Claude Tag's "Opus 4.8" is a sourced historical launch fact).
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md, advanced/reproducibility.md, advanced/verification.md — unchanged.

### Flagged for review
- **`whats-new-claude-opus-5` API doc missing** — `platform.claude.com/docs/en/about-claude/models/whats-new-claude-opus-5` 404s as of this run; Opus 5 API-level claims are grounded in the news post + secondary coverage. Re-check next run and swap in the canonical doc when it's live.
- **Opus 5 as `opus` alias / Max default** — confirm against the canonical model docs once published, and watch whether Sonnet 5 remains the Claude Code default on Pro vs. Opus 5 on Max.
- **Economic Index connector** — first-party, all-plans; watch whether the connectors directory grows enough distinct first-party connectors to warrant naming them individually on connectors.md.
- **Agent SDK billing split** — carried over; paused, not cancelled. Re-verify the help-center pause notice each run.
- **Mythos 5 general availability** — restricted to approved U.S. orgs; watch for broader availability.
- **Claude Tag** — Team/Enterprise beta; watch the old Claude-in-Slack app retirement (~early Aug 2026).
- **Promote `security-guidance` to its own page** — carried over; stays inside `plugins.md` unless a human expands the topic list.

## 2026-07-18

### Updated
- **[advanced/slash-commands, surfaces/claude-code] `/fork` and `/subtask` split (v2.1.212, 2026-07-17).** `/fork` now copies your whole conversation into its own background-session row (a new row in `claude agents`) so you keep working in the original; the in-session subagent launcher it used to be is now the separate `/subtask` command. Added `/subtask` to the subagents paragraph on the slash-commands page (plus the new per-session subagent spawn cap of 200, `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`, reset by `/clear`), and noted the new `/fork` behavior in the Claude Code web/background-sessions bullet. Grounded in the [Claude Code changelog](https://code.claude.com/docs/en/changelog) fetched this run (v2.1.212, 2026-07-17).

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebFetch of `claude.com/product/claude-code`: native installer canonical, no deprecation banner; Terminal / VS Code / JetBrains / web / Desktop / iOS / Android / Slack / GitHub surfaces unchanged. Changelog re-fetched: latest release is **v2.1.214 (2026-07-18)**; v2.1.208–v2.1.214 are otherwise below the beginner threshold (screen-reader mode `--ax-screen-reader`, vim insert-mode remaps, live elapsed-time counter, permission-preview hardening, session-wide WebSearch cap, MCP auto-background after 2 min, EndConversation tool for abusive/jailbreak sessions). Sonnet 5 default, Claude in Chrome GA, Dynamic Workflows, Channels, Claude Security, MCP tunnels, routines all current.
- surfaces/claude-api.md — Sonnet 5, Opus 4.8, Fable 5 (redeployed), model-deprecation past tense, Agent SDK pause, Managed Agents all current.
- anthropic.com/news scanned — July items (Claude for Teachers, Reflection usage-insight feature, Long-Term Benefit Trust appointment, Canadian AI research funding) do not meet the beginner cross-cutting / component bar; no new page warranted.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-science.md, surfaces/claude-tag.md — unchanged.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/routines.md, advanced/authentication.md, advanced/reproducibility.md, advanced/verification.md — unchanged.

### Flagged for review
- **Claude for Teachers / Claude Reflection (July 2026)** — new consumer-facing surfaces/features; watch for beginner relevance or cross-surface reach before adding a page.
- **Agent SDK billing split** — carried over; paused, not cancelled. Re-verify the help-center pause notice each run.
- **Mythos 5 general availability** — restricted to approved U.S. orgs (Project Glasswing); watch for broader availability.
- **Claude Tag** — Team/Enterprise beta; watch the old Claude-in-Slack app retirement (~early Aug 2026 per secondary coverage).
- **Claude in Chrome** — if it becomes a distinct beginner-facing component rather than a Claude Code companion, consider promoting the cross-cutting bullet to a sub-page.
- **Promote `security-guidance` to its own page** — carried over; stays inside `plugins.md` unless a human expands the topic list.

## 2026-07-11

### Added
- **[surfaces/claude-science] New surface sub-page for Claude Science.** Anthropic launched Claude Science on 2026-06-30 (beta 2026-07-01) — a standalone macOS/Linux research workbench app at `claude.com/science` that orchestrates 60+ curated skills, scientific database connectors (UniProt, PDB, Ensembl, ClinVar, ChEMBL, GEO), and specialist/reviewer subagents, and records code + environment + message history per figure. It's a distinct, beginner-facing surface directly relevant to this repo's life-sciences audience, running the same models (Opus 4.8 / Sonnet 5) with no gating. Added `guide/surfaces/claude-science.md` and wired it into the surfaces table on `claude-surfaces.md`, the `README.md` reading-order line, and a new `decision-tree.md` row for reproducible scientific analysis. Grounded in [Claude Science, an AI workbench for scientists](https://www.anthropic.com/news/claude-science-ai-workbench) (2026-06-30), the [`claude.com/science`](https://claude.com/science) landing page, and [STAT News](https://www.statnews.com/2026/06/30/anthropic-release-claude-science-ceo-dario-amodei/) (2026-06-30), all fetched this run.

### Updated
- **[advanced/reproducibility] Cross-link to Claude Science.** Added a sentence noting Claude Science bakes in per-figure code + environment + history, which is exactly the discipline this page advocates. Grounded in the Claude Science landing page fetched this run.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebFetch of `claude.com/product/claude-code`: native installer canonical, no deprecation banner; Terminal / VS Code / JetBrains / web / Desktop / iOS / Android / Slack surfaces unchanged. Claude Code changelog re-fetched: latest release is **v2.1.207 (2026-07-11)**; v2.1.202–v2.1.207 are below the beginner threshold (Dynamic-workflow-size setting, `/cd` path suggestions, `/commit-push-pr` push auto-allow, `/doctor` CLAUDE.md trim hint, background-agent status/login-warning fixes, SessionStart hook-streaming fix, auto-mode on Bedrock/Vertex/Foundry by default). Sonnet 5 default, Claude in Chrome GA, Dynamic Workflows, Channels, Claude Security, MCP tunnels, routines all current.
- surfaces/claude-api.md — Sonnet 5, Opus 4.8, Fable 5 (redeployed), model-deprecation past tense, Agent SDK pause, Managed Agents all current.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md — unchanged.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- **Claude Science topic set** — added as a surface sub-page under the fixed topic list; if it grows its own component model (Science-specific plugins/skills distribution), consider a dedicated deeper page. Watch for Windows client and GA.
- **Agent SDK billing split** — carried over; paused, not cancelled. Re-verify the help-center pause notice each run.
- **Mythos 5 general availability** — restricted to approved U.S. orgs (Project Glasswing); watch for broader availability.
- **Claude Tag** — Team/Enterprise beta; if it reaches Pro or becomes a primary surface, consider a `guide/surfaces/claude-tag.md` sub-page. Watch the old Claude-in-Slack app retirement (~early Aug 2026 per secondary coverage).
- **Claude in Chrome** — if it becomes a distinct beginner-facing component rather than a Claude Code companion, consider promoting the cross-cutting bullet to a sub-page.
- **Agent teams (experimental)** — `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; still env-gated and below beginner threshold — watch for GA.
- **Promote `security-guidance` to its own page** — carried over; stays inside `plugins.md` unless a human expands the topic list.

## 2026-07-04

### Added
- **[claude-surfaces, surfaces/claude-code] Claude in Chrome reached GA (2026-07-01).** The browser extension is now generally available and pairs with Claude Code for a build-test-verify loop. Added a cross-cutting bullet on the surfaces page (it's effectively a sixth place to reach Claude and a discoverability gap for beginners) and a short note on the Claude Code page. Grounded in [Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome) and the v2.1.198 changelog, both fetched this run.
- **[skills] `/dataviz` built-in skill + stacked skill invocation.** v2.1.198 (2026-07-01) shipped a built-in `/dataviz` skill (charts/dashboards + color-palette validator); v2.1.199 (2026-07-02) made stacked `/a /b /c` invocations load up to 5 skills instead of only the first. Grounded in the Claude Code changelog fetched this run.

### Updated
- **[surfaces/claude-code, surfaces/claude-api] Claude Sonnet 5 is the new default (2026-06-30).** Sonnet 5 (`claude-sonnet-5`, the `sonnet` alias) is now the default for Free/Pro and the default in Claude Code, with a native 1M-token context window and intro pricing ($2/$10 per Mtok through 2026-08-31). Rewrote the Claude Code model-picker line (was "Opus 4.8 is the default") and the Claude API model-line pitfall, and added a pitfall covering Sonnet 5's ~30%-heavier tokenizer, adaptive-thinking default, and sampling-parameter 400s. Grounded in [Introducing Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5) and [What's new in Claude Sonnet 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5), both fetched this run.
- **[surfaces/claude-code, surfaces/claude-api] Fable 5 is available again.** The U.S. export-control order was lifted 2026-06-30 and Fable 5 was redeployed globally on 2026-07-01 (Mythos 5 restricted to approved U.S. orgs). Reversed the "currently unavailable" content in both pages back to available, restoring the Fable 5 behavior detail on the API page. Grounded in [Redeploying Claude Fable 5](https://www.anthropic.com/news/redeploying-fable-5) fetched this run.
- **[advanced/slash-commands] Subagents run in the background by default (v2.1.198).** Claude keeps working while subagents run and is notified on completion; each inherits the session's extended-thinking config. Grounded in the Claude Code changelog fetched this run.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebFetch of `claude.com/product/claude-code`: native installer canonical, no deprecation banner; Terminal / VS Code / JetBrains / web / Desktop / Slack / mobile surfaces unchanged. Latest release is **v2.1.201 (2026-07-03)**; v2.1.200's "permission dialogs require manual approval by default" is a sensible-default change noted in Sources but below the beginner topic threshold. Channels, Dynamic Workflows, Claude Security, MCP tunnels, routines all current.
- surfaces/claude-api.md — Agent SDK / `claude -p` billing split still **paused** (help-center pause notice re-verified this run); Managed Agents, Opus 4.8, model-deprecation past tense all current.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged.
- mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/routines.md, advanced/authentication.md, advanced/reproducibility.md — unchanged.

### Flagged for review
- **Agent SDK billing split** — carried over; paused, not cancelled. Re-verify the help-center pause notice each run.
- **Mythos 5 general availability** — restricted to approved U.S. orgs (Project Glasswing); watch for broader availability.
- **Claude Tag** — Team/Enterprise beta; if it reaches Pro or becomes a primary surface, consider a `guide/surfaces/claude-tag.md` sub-page. Watch the old Claude-in-Slack app retirement (~early Aug 2026 per secondary coverage).
- **Claude in Chrome** — if it becomes a distinct beginner-facing component rather than a Claude Code companion, consider promoting the cross-cutting bullet to a sub-page.
- **Agent teams (experimental)** — `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; still env-gated and below beginner threshold — watch for GA.
- **Advisor tool (API)** — carried over; advanced cost-optimization pattern, omitted by scope.
- **Promote `security-guidance` to its own page** — carried over; stays inside `plugins.md` unless a human expands the topic list.

## 2026-06-27

### Added
- **[claude-surfaces] Claude Tag (Slack) cross-cutting note.** Anthropic launched Claude Tag on 2026-06-23 — a Slack-native `@Claude` that joins channels, takes delegated tasks, works async, and is admin-scoped per channel. It's effectively a fifth surface and explicitly replaces the old Claude-in-Slack app (30-day admin opt-in to migrate), so beginners on Team/Enterprise need to know it exists. Added a cross-cutting bullet on the surfaces page rather than a new sub-page (Team/Enterprise beta only; topic set is fixed). Grounded in [Introducing Claude Tag](https://www.anthropic.com/news/introducing-claude-tag) (2026-06-23) fetched this run.

### Updated
- **[mcp-servers, advanced/authentication] `claude mcp login` / `claude mcp logout` replace `claude mcp auth`.** v2.1.186 (2026-06-22) added shell-level MCP OAuth: `claude mcp login <name>` runs a server's OAuth flow without opening a session, `claude mcp logout <name>` revokes it, and `--no-browser` supports SSH. The old `claude mcp auth <server>` is no longer documented. Replaced the stale `claude mcp auth` line in authentication.md and added the new commands to the mcp-servers install section. Grounded in [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) re-fetched this run.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebFetch of `claude.com/product/claude-code`: native installer canonical, no deprecation banner; Terminal / VS Code / JetBrains / web / Desktop / Slack / mobile surfaces unchanged. Latest release is **v2.1.195 (2026-06-26)**; v2.1.183–v2.1.195 are mostly below the beginner threshold (`/rewind`, `/config` mouse settings, `--safe-mode`, `autoMode.classifyAllShell`, `sandbox.credentials`, voice-dictation fixes, hook-matcher exact-match fix, org model-restriction messaging). Fable 5 / Mythos 5 still suspended worldwide (no restoration); Agent SDK billing split still paused; Dynamic Workflows, Channels, Claude Security, MCP tunnels, routines all current.
- surfaces/claude-api.md — Fable 5 suspension, Opus 4.8 default, model-deprecation past tense, Agent SDK pause, Managed Agents all current.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged.
- skills.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/reproducibility.md — unchanged.

### Flagged for review
- **Fable 5 / Mythos 5 restoration** — carried over; suspension still open-ended with no Anthropic timeline. Re-check each run and restore the Fable 5 lines when access returns.
- **Agent SDK billing split** — carried over; paused, not cancelled. Re-verify the help-center pause notice each run.
- **Claude Tag** — Team/Enterprise beta; if it reaches Pro or becomes a primary surface, consider a `guide/surfaces/claude-tag.md` sub-page. Watch the old Claude-in-Slack app retirement (~early Aug 2026 per secondary coverage).
- **Anthropic news (06-17 to 06-23): Seoul office, Korean partnerships, Claude Public Record** — not beginner-facing components; out of scope.
- **Agent teams (experimental)** — `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; `teammateMode: "iterm2"` added v2.1.186. Still experimental and env-gated; below beginner threshold — watch for GA.
- **Advisor tool (API)** — carried over; advanced cost-optimization pattern, omitted by scope.
- **Promote `security-guidance` to its own page** — carried over; stays inside `plugins.md` unless a human expands the topic list.

## 2026-06-20

### Updated
- **[surfaces/claude-code, surfaces/claude-api] Fable 5 / Mythos 5 suspended worldwide.** On 2026-06-12 a U.S. government export-control directive forced Anthropic to disable Fable 5 and Mythos 5 for *all* customers worldwide; the previously-documented "free in the picker through 2026-06-22" framing is now wrong. Rewrote the Claude Code model-picker line and the Claude API model-IDs / Fable-5 pitfalls to state Fable 5 is currently unavailable (Opus 4.8 is the default and is unaffected), folding the old Fable-5 behavior/refusal detail into one parenthetical. Grounded in [Anthropic's statement](https://www.anthropic.com/news/fable-mythos-access) (2026-06-12) re-fetched this run.
- **[surfaces/claude-code, surfaces/claude-api] Agent SDK / `claude -p` billing split was paused, not shipped.** Anthropic shelved the planned 2026-06-15 move of programmatic usage onto a separate credit pool; the Help Center now opens with a pause notice. Rewrote both billing pitfalls from "moves on 2026-06-15" to "was paused; still draws from your subscription." Grounded in the [Agent SDK plan help-center article](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) re-fetched this run.
- **[surfaces/claude-api] Sonnet 4 / Opus 4 retirement is now past, not pending.** Changed the deprecation pitfall to past tense (IDs and the `-4-0` aliases now error as of 2026-06-15 9am PT), pointed the Opus migration at `claude-opus-4-8`, and noted consumer Claude.ai / Claude Code managed environments were unaffected. Grounded in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) re-fetched this run.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebFetch of `claude.com/product/claude-code`: native installer canonical, no deprecation banner; Terminal / VS Code / JetBrains / web / Slack / Desktop surfaces unchanged. Latest release is **v2.1.183 (2026-06-19)**; v2.1.178–v2.1.183 are mostly below the beginner threshold (`/config key=value`, `--safe-mode`, `/cd`, agent-teams setup simplification, destructive-git-command guard). Channels, Dynamic Workflows (`ultracode`), Claude Security, MCP tunnels, routines, per-surface sandboxing all current.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- **Fable 5 / Mythos 5 restoration** — suspension is open-ended with no Anthropic timeline; re-check the statement and model docs each run and restore the Fable 5 lines when access returns.
- **Agent SDK billing split** — paused, not cancelled; Anthropic says it will give notice before any future change. Re-verify the help-center pause notice each run.
- **Anthropic news (06-11 to 06-17): Claude Corps, TCS / DXC regulated-industry partnerships, Seoul office, Public Record** — none are beginner-facing components; out of scope.
- **Agent teams (experimental)** — `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; spawn simplified in v2.1.178. Experimental and env-gated; below beginner threshold for now — watch for GA.
- **Advisor tool (API)** — carried over; advanced cost-optimization pattern, omitted by scope.
- **Promote `security-guidance` to its own page** — carried over; stays inside `plugins.md` unless a human expands the topic list.

## 2026-06-13

### Updated
- **[plugins] Noted the `/plugin` marketplace search box.** v2.1.172 (2026-06-10) added a type-to-filter search to `/plugin` marketplace browsing — a small discoverability win for beginners scanning a large marketplace. Added one clause to the management paragraph. Grounded in the [Claude Code changelog](https://code.claude.com/docs/en/changelog) (v2.1.172) re-fetched this run.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebFetch of `claude.com/product/claude-code`: native installer canonical, no deprecation banner on the landing page; Desktop/VS Code/JetBrains/web/Slack/iOS surfaces unchanged. Latest release is **v2.1.176 (2026-06-12)**; v2.1.174–176 are bug fixes plus admin/enterprise-only settings (`enforceAvailableModels`, `footerLinksRegexes`, Bedrock credential caching, hook `if`-condition path-matching fix for `Edit(src/**)` / `Read(~/.ssh/**)`) — all below the beginner threshold. `/code-review` vs `/simplify` split, Channels, Dynamic Workflows (`ultracode`), Claude Security, MCP tunnels, routines, Fable 5 picker, per-surface sandboxing all current.
- surfaces/claude-api.md — Fable 5 / Opus 4.8 model lines, effort ladder, Managed Agents, mid-conversation system messages, prompt caching, sampling-parameter 400 all current.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged.
- skills.md, mcp-servers.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged. (Hooks `if`-condition path-matching fix in v2.1.176 corrects existing behavior the page does not document; no edit warranted.)

### Flagged for review
- **`claude -p` / Agent SDK billing split lands 2026-06-15** — carried over; 2 days out. Re-verify after 06-15 that `surfaces/claude-code.md` and `surfaces/claude-api.md` describe live behavior.
- **Sonnet 4 / Opus 4 retirement 2026-06-15 9am PT** — carried over; re-verify `surfaces/claude-api.md` after the date that the exact IDs now error.
- **Fable 5 subscription-availability flips 2026-06-23** — carried over; re-verify the "free until / credits from" dates after 06-22.
- **Anthropic news (06-11 to 06-12): Claude Corps fellowship, TCS / DXC regulated-industry partnerships** — none are beginner-facing components; out of scope.
- **Advisor tool (API)** — carried over; advanced cost-optimization pattern, omitted by scope.
- **Promote `security-guidance` to its own page** — carried over; stays inside `plugins.md` unless a human expands the topic list.

## 2026-06-11

### Added
- **[advanced/slash-commands] Nested subagents (up to 5 levels deep).** v2.1.172 (2026-06-09) reversed the long-standing rule that a subagent could not spawn subagents — now any subagent can call the Task tool, down to a hard 5-level cap, to keep noisy sub-tasks out of the main conversation's context. Added one clause to the subagent definition. Grounded in the [Claude Code changelog](https://code.claude.com/docs/en/changelog) (v2.1.172) cross-checked against [a v2.1.172 writeup](https://claudefa.st/blog/guide/agents/nested-subagents).

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebFetch of `claude.com/product/claude-code`: native installer canonical, no deprecation banner; Windows/winget/brew/npm-deprecated options unchanged. Latest release is v2.1.173 (2026-06-11); v2.1.171–v2.1.173 are bug fixes plus below-beginner-threshold items (`/cd`, `--safe-mode`, `continueOnBlock`, `defaultEnabled: false`). `/code-review` vs `/simplify` split, Channels, Dynamic Workflows (`ultracode`), Claude Security, MCP tunnels, routines, Fable 5 picker, per-surface sandboxing all current.
- surfaces/claude-api.md — Fable 5 / Opus 4.8 model lines, effort ladder, Managed Agents, mid-conversation system messages, prompt caching, sampling-parameter 400 all current.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- **`claude -p` / Agent SDK billing split lands 2026-06-15** — carried over; 4 days out. Re-verify after 06-15 that `surfaces/claude-code.md` and `surfaces/claude-api.md` describe live behavior.
- **Sonnet 4 / Opus 4 retirement 2026-06-15 9am PT** — carried over; re-verify `surfaces/claude-api.md` after the date that the IDs now error.
- **Fable 5 subscription-availability flips 2026-06-23** — carried over; re-verify the "free until / credits from" dates after 06-22.
- **Anthropic news (06-01 to 06-03): SEC S-1 draft, Services Track / Partner Hub, AI cyber-threats report, Project Glasswing expansion** — none are beginner-facing components; out of scope.
- **Advisor tool (API)** — carried over; advanced cost-optimization pattern, omitted by scope.
- **Promote `security-guidance` to its own page** — carried over; stays inside `plugins.md` unless a human expands the topic list.

## 2026-06-10

### Added
- **[surfaces/claude-api] Claude Fable 5 / Mythos 5 (Mythos-class tier).** Anthropic shipped Fable 5 (`claude-fable-5`) on 2026-06-09 — its most capable generally-available model, a tier above Opus. Added to the model-IDs pitfall plus two new pitfalls covering its different behavior (adaptive-thinking-only, `effort`-controlled, never returns raw CoT, $10/$50 per Mtok, 1M context / 128k output) and its higher refusal rate (HTTP-200 `stop_reason: "refusal"` with `stop_details`; prompt-stage refusals unbilled, mid-stream billed). Noted `claude-mythos-5` is invitation-only (Project Glasswing). Grounded in [Anthropic news](https://www.anthropic.com/news/claude-fable-5-mythos-5) (2026-06-09) and [the model docs](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) (verified this run).
- **[surfaces/claude-code] Fable 5 in the model picker.** Selectable via `/model` as of v2.1.170 (2026-06-09); free on Pro/Max/Team/Enterprise through 2026-06-22, then usage-credit-gated from 2026-06-23; cybersecurity / bio-chem / distillation prompts auto-route to Opus 4.8 (<5% of sessions); Opus 4.8 stays the default. Touches ≥2 surfaces (API + Claude Code), so documented per the cross-cutting directive.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebFetch of `claude.com/product/claude-code`: native installer canonical, no deprecation banner on the landing page; Windows `irm …/install.ps1 | iex` / `winget install Anthropic.ClaudeCode`, `brew install --cask claude-code` (stable) / `claude-code@latest`, npm-with-deprecation-banner all unchanged. Latest release is v2.1.170 (2026-06-09); its only non-model change is a VS-code-terminal transcript bug fix (below beginner threshold). `/code-review` vs `/simplify` split, Channels, Dynamic Workflows (`ultracode`), Claude Security, MCP tunnels, routines, per-surface sandboxing all current.
- surfaces/claude-api.md — Opus 4.8 default + low/medium/high/xhigh/max effort ladder unchanged; Managed Agents (Outcomes/Dreams/orchestration), mid-conversation system messages, prompt caching, `temperature`/`top_p`/`top_k` 400 all current.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- **WebFetch worked this run** for `claude.com/product/claude-code` and `anthropic.com/news/claude-fable-5-mythos-5`; the prior Haiku-404 regression appears resolved. Model-docs detail (`platform.claude.com`) was grounded via WebSearch summary as a backstop.
- **`claude -p` / Agent SDK billing split lands 2026-06-15** — carried over; still 5 days out as of today (2026-06-10). Re-verify after 06-15 that `surfaces/claude-code.md` and `surfaces/claude-api.md` describe live behavior.
- **Sonnet 4 / Opus 4 retirement 2026-06-15 9am PT** — carried over; re-verify `surfaces/claude-api.md` after the date that the IDs now error.
- **Fable 5 subscription-availability flips 2026-06-23** — newly added. Re-verify after 06-22 that the "free until / credits from" dates on `surfaces/claude-api.md` and `surfaces/claude-code.md` reflect live state, and update if Anthropic restores Fable 5 as a standard subscription feature.
- **Claude Mythos 5 / Project Glasswing** — noted as invitation-only, not a beginner component; left as a one-line aside.
- **Advisor tool (API)** — carried over; advanced developer cost-optimization pattern, omitted by scope.
- **Promote `security-guidance` to its own page** — carried over; schema fixes the file set, stays inside `plugins.md` unless a human expands the topic list.

## 2026-06-09

### Added
- **[surfaces/claude-api] New pitfall: Opus 4.7 / 4.8 reject `temperature`, `top_p`, `top_k` with a 400.** Rejection is by presence (not value) and the SDK won't catch it at compile time, so it bites beginners migrating off older models — especially via OpenAI-compat layers or frameworks that inject `temperature`. Grounded in [What's new in Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8) (verified this run via WebSearch summary). The page already covered the `budget_tokens` → adaptive-thinking deprecation; this completes the sampling-parameter story.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebSearch against `claude.com/product/claude-code`: native installer canonical, Windows `irm …/install.ps1 | iex` / `winget install Anthropic.ClaudeCode`, `brew install --cask claude-code` (stable) / `claude-code@latest`, npm-with-deprecation-banner all unchanged. Latest documented release is v2.1.169 (June): v2.1.165–v2.1.169 are bug fixes plus the `fallbackModel` setting (up to three fallbacks when primary is overloaded), deny-rule glob support, and cross-session-messaging hardening — all below the beginner threshold. `/code-review` (bug-hunting) vs `/simplify` (cleanup-only) split, Channels, Dynamic Workflows (`ultracode`), Claude Security, MCP tunnels, routines, per-surface sandboxing all current.
- surfaces/claude-api.md — Opus 4.8 default + low/medium/high/xhigh/max effort ladder unchanged; Managed Agents (Outcomes/Dreams/orchestration), mid-conversation system messages, prompt caching all current.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged. June legal/Cowork-plugin and connector news already reflected.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch remained unavailable this run (404 on `claude-3-5-haiku-20241022`, same regression as prior runs). All verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `github.com/anthropics/claude-code/releases`, `releasebot.io/updates/anthropic`, `anthropic.com/news`, and `platform.claude.com` docs. A human should spot-check the product landing page and changelog directly.
- **`claude -p` / Agent SDK billing split lands 2026-06-15** — carried over; still 6 days out as of today (2026-06-09); credit-claim emails reportedly arriving ~2026-06-08. Re-verify after 06-15 that `surfaces/claude-code.md` and `surfaces/claude-api.md` describe live behavior, not the pre-launch announcement.
- **Sonnet 4 / Opus 4 retirement 2026-06-15 9am PT** — carried over; re-verify `surfaces/claude-api.md` after the date that the IDs now error.
- **Advisor tool (API)** — carried over; still an advanced developer cost-optimization pattern, omitted by scope.
- **Promote `security-guidance` to its own page** — carried over; schema fixes the file set, stays inside `plugins.md` unless a human expands the topic list.

## 2026-06-08

No substantive updates — 17 pages spot-checked, all current.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebSearch against `claude.com/product/claude-code`: native installer canonical and recommended; Windows `irm https://claude.ai/install.ps1 | iex` / `winget install Anthropic.ClaudeCode`, `brew install --cask claude-code` (stable) / `claude-code@latest`, and npm-with-deprecation-banner all unchanged. Latest documented Claude Code release is v2.1.168 (June 7); v2.1.165–v2.1.168 are dominated by bug fixes plus the `fallbackModel` setting and cross-session-messaging hardening — below the beginner threshold. `/code-review` (bug-hunting) vs `/simplify` (cleanup-only) split, Channels, Dynamic Workflows (`ultracode`), Claude Security, MCP tunnels, routines, and per-surface sandboxing all current.
- surfaces/claude-api.md — Opus 4.8 default + low/medium/high/xhigh/max effort ladder confirmed unchanged. The new **advisor tool** (public beta, `advisor-tool-2026-03-01` header; pairs an Opus advisor with a Sonnet/Haiku executor inside one API call) was assessed and deliberately omitted: it is an advanced developer cost-optimization tool-use pattern, not a beginner component-model concept, and lives outside this page's orientation scope and word budget.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch remained unavailable this run (404 on `claude-3-5-haiku-20241022`, same regression as prior runs). All verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `github.com/anthropics/claude-code/releases`, `releasebot.io/updates/anthropic`, `anthropic.com/news`, and `support.claude.com` release notes. A human should spot-check the product landing page and changelog directly.
- **`claude -p` / Agent SDK billing split lands 2026-06-15** — carried over; still future as of today (2026-06-08). Re-verify after the date that `surfaces/claude-code.md` and `surfaces/claude-api.md` describe live behavior, not the pre-launch announcement. (Eligible users reportedly receive the credit-claim email around 2026-06-08, but the billing split itself is still 06-15.)
- **Sonnet 4 / Opus 4 retirement 2026-06-15 9am PT** — carried over; re-verify `surfaces/claude-api.md` after the date.
- **Advisor tool (API)** — newly noted. If it reaches GA or becomes a beginner-facing surface, reconsider a brief mention in `surfaces/claude-api.md`.
- **Promote `security-guidance` to its own page** — carried over. Not done: the schema fixes the file set, so it stays documented inside `plugins.md` unless a human expands the topic list.
- **Claude Mythos / critical-infrastructure expansion** — carried over; corporate/infra news, not a beginner component-model change.

## 2026-06-07

No substantive updates — 17 pages spot-checked, all current.

### Verified (no changes)
- claude-surfaces.md, surfaces/claude-code.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebSearch against `claude.com/product/claude-code`; native installer canonical, npm still prints the deprecation banner, `winget install Anthropic.ClaudeCode` / `brew install --cask claude-code` unchanged. v2.1.166–v2.1.168 (June 6–7) are bug fixes plus a `fallbackModel` setting (up to three fallback models when the primary is overloaded) — below the beginner threshold. `/code-review` vs `/simplify` split re-confirmed current against [Code review docs](https://code.claude.com/docs/en/code-review): `/code-review` is bug-hunting (fixes only with `--fix`), `/simplify` is cleanup-only and auto-applies. Channels, Dynamic Workflows (`ultracode`), Claude Security, MCP tunnels, routines, sandboxing all current.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged. Opus 4.8 default/effort ladder unchanged.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch remained unavailable this run (404 on `claude-3-5-haiku-20241022`, same regression as prior runs). All verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `code.claude.com/docs/en/code-review`, `github.com/anthropics/claude-code/releases`, `anthropic.com/news`, `releasebot.io/updates/anthropic`, and `claudeupdates.dev`. A human should spot-check the product landing page and changelog directly.
- **`claude -p` / Agent SDK billing split lands 2026-06-15** — carried over; still future as of this run. Re-verify after the date that `surfaces/claude-code.md` and `surfaces/claude-api.md` describe the live behavior, not the pre-launch announcement.
- **Sonnet 4 / Opus 4 retirement 2026-06-15 9am PT** — carried over; re-verify `surfaces/claude-api.md` after the date.
- **Promote `security-guidance` to its own page** — carried over. Not done: the schema fixes the file set, so it stays documented inside `plugins.md` unless the topic list is expanded by a human.
- **Claude Mythos / Project Glasswing public release** — carried over; June 2/3 expansion is critical-infrastructure cohort + corporate news, not a beginner component-model change.

