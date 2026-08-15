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

## 2026-08-15

### Updated
- **[claude-surfaces, surfaces/claude-code] Cross-session `@`-mentions (v2.1.232, 2026-08-13).** Type `@` plus a session name in any prompt to message another of your Claude Code sessions directly (routes through the existing `SendMessage`); inbound requests now show up under new `/config` rows ("Dialog expiry," "Messages from your other sessions") where you accept, hold, or refuse them. Extended the existing "Background sessions" cross-cutting bullet on `claude-surfaces.md` and the web/background paragraph on `surfaces/claude-code.md` rather than creating a new entry, since it's a direct extension of the already-documented `SendMessage`/`ListAgents` feature. Grounded in the [Claude Code changelog](https://code.claude.com/docs/en/changelog), v2.1.232, fetched this run.
- **[surfaces/claude-code] GitLab merge requests in `--worktree` and `claude agents` (v2.1.233, 2026-08-14).** Both now recognize GitLab MRs (shown as `!N`) alongside GitHub PRs — de-GitHub-centric'd the surrounding sentence. Grounded in the [Claude Code changelog](https://code.claude.com/docs/en/changelog), v2.1.233, fetched this run.
- **[marketplaces] GitLab marketplace support (v2.1.232, 2026-08-13).** Added a `https://gitlab.com/...` example to the copy-pasteable marketplace-add commands (this form was already implicitly covered by "any Git URL" but wasn't shown explicitly) and a note that a bare `gitlab.com/owner/repo` shorthand also now clones like GitHub's `owner/repo` form per the changelog — flagged that the canonical [plugin-marketplaces doc](https://code.claude.com/docs/en/plugin-marketplaces) (re-fetched this run) still only documents the full-URL form and rejects a schemeless non-GitHub host as of v2.1.196, so the page tells readers to fall back to the full URL if the shorthand doesn't resolve. This is a doc-page-lags-changelog case per the source-priority rule.
- **[advanced/slash-commands] Fork subagents now default (v2.1.232, 2026-08-13).** `subagent_type: "fork"` — a subagent that inherits the parent's full conversation and prompt cache instead of starting isolated — now runs by default whenever the orchestrator picks that type; confirmed against the canonical [Subagents reference](https://code.claude.com/docs/en/subagents) (re-fetched this run), which independently describes fork's cache-reuse behavior. Added one sentence; this is the same mechanism the existing `/fork` command already used, now generalized to any subagent spawn.
- **[claude-surfaces, surfaces/claude-code] Refreshed install-command and changelog citations.** Re-fetched `claude.com/product/claude-code` (unchanged: `curl -fsSL https://claude.ai/install.sh | bash`, same launch surfaces) and the Claude Code changelog through the current latest release, **v2.1.233 (2026-08-14)**.

### Verified (no changes)
- Skills, MCP servers, Connectors, Plugins, Decision tree, Hooks, Routines, Authentication, Reproducibility, Verification, Claude.ai, Claude Desktop, Claude Cowork, Claude API, Claude Science, Claude Tag — spot-checked, no stale claims found this run.
- v2.1.225–v2.1.230 (MCP gateway spend-limit messages, a marketplace `command` source kind for IDE-printed plugin directories, connector false-authorization-needed fix, skills-from-claude.ai hardening, MCP OAuth redirect-URI fix, MCP v2 stream-reopen fix) reviewed and judged below the beginner threshold for this guide — mostly bug fixes and an IDE-integration authoring detail, consistent with prior runs' treatment of similar internal changes.
- Anthropic news feed scanned (through 2026-08-14: "How Claude's text watermark works," "Improving Fable 5's biology safeguards," Tino Cuéllar appointment) — none are beginner-facing component-model concepts; no new page or cross-cutting bullet warranted.
- Connectors directory count — still could not confirm an updated total via WebFetch (page renders as a filtered/paginated view with no visible directory-wide count); left the existing "950+" figure in place, consistent with the prior run's note.

### Flagged for review
- **GitLab bare-URL marketplace shorthand** — changelog says it works (v2.1.232); the canonical doc page hasn't been updated to match. Re-check `plugin-marketplaces` doc next run and simplify the marketplaces.md wording once it catches up.
- **Marketplace `command` source kind (v2.1.229)** — an IDE-oriented authoring detail (local command prints the plugin directory, re-resolved each session); currently judged below the beginner bar for `marketplaces.md`'s already-long source-kind list. Revisit if it becomes a common end-user path rather than an IDE-integration internal.
- Carried over from 2026-08-08: Opus 5 fast-mode plan-tiering (still research preview); Agent SDK billing split (still paused); subagent spawn-cap history discrepancy across secondary trackers; Claude for Government / org-level DLP (admin-only, out of scope); Mythos 5 GA restricted to approved orgs; promote `security-guidance` to its own page only if a human expands the fixed topic list.

## 2026-08-08

### Added
- **[Claude surfaces, surfaces/claude-code] Self-hosted environments (Team/Enterprise).** `claude self-hosted-runner` (v2.1.224, 2026-08-07) turns your own machine or container into a place Claude Code web, mobile, and desktop sessions can run, instead of Anthropic's cloud VMs — a genuine discoverability item since it changes where a session actually executes. Added as a cross-cutting bullet on `claude-surfaces.md` and a short mention on `surfaces/claude-code.md`. Grounded in the [Claude Code changelog](https://code.claude.com/docs/en/changelog), v2.1.224, fetched this run.
- **[Claude surfaces, surfaces/claude-code] Cross-session messaging.** Same release added `SendMessage`/`ListAgents` so background sessions on different machines (macOS/Linux only) can message each other and discover reachable agents. Extended the existing "Background sessions" cross-cutting bullet and the Claude Code web/background paragraph rather than creating a new entry, since it's an extension of an already-documented feature.
- **[advanced/hooks] `DirectoryAdded` hook event (v2.1.222, 2026-08-04).** Fires after `/add-dir` or the SDK's `register_repo_root` control request registers a new working directory mid-session. Added to the events list.

### Updated
- **[marketplaces] New `archive` plugin source type.** A `marketplace.json` plugin entry can now point to a zip file over plain HTTPS with an optional SHA-256 pin (v2.1.224, 2026-08-07), alongside the existing GitHub/git/git-subdir/npm source kinds. Clarified that this is an authoring-time detail — end users still run `/plugin install <name>@<marketplace>` the same way regardless of source type. Grounded in [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) (re-fetched this run, now documents the `archive` source) and the v2.1.224 changelog.
- **[advanced/slash-commands] Corrected subagent concurrency/depth defaults and removed a stale per-session cap.** The page previously said "up to 10 parallel" and "5 levels deep" with a 200-subagent-per-session cap (`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`). The canonical [Subagents reference](https://code.claude.com/docs/en/subagents) (fetched this run) gives different current defaults: 20 concurrent (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`) and 3 levels of nesting depth (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, which the doc says moved 5 → 1 → 3 across recent releases) — and states there is no limit on total subagents spawned over a session's lifetime. The per-session cap was removed in v2.1.224 (2026-08-07) per the changelog. Rewrote the paragraph and Sources to match the canonical doc, which we treat as authoritative over the page's prior figures.

### Verified (no changes)
- Claude Code install command and launch surfaces (`claude.com/product/claude-code`, re-fetched) — unchanged.
- Claude API model guidance (Opus 5, Sonnet 5, Fable 5) — no new model launches this week; Opus 5 fast-mode plan-tiering details ($10/$50 per Mtok, Max/premium-seat only, capped at 50% of weekly limits since 2026-07-20) surfaced via search but are a research-preview power-user detail below this page's beginner threshold — not added, see Flagged for review.
- Connectors directory — could not confirm an updated total count this run (source page truncated); left the existing "950+" figure in place.
- Skills, Plugins, Decision tree, Connectors, Routines, Authentication, Claude.ai, Claude Desktop, Claude Cowork, Claude Science, Claude Tag, Claude API — spot-checked, no stale claims found this run. Cowork web/mobile confirmed still in beta (Max-first rollout continuing), matching current page text.
- v2.1.221 (Focus view chat-menu toggle) and v2.1.222–223 (permission/sandbox security hardening, session-wide WebSearch cap, MCP auto-background) reviewed and judged below the beginner threshold for this guide, consistent with prior runs' treatment of similar internal hardening changes.

### Flagged for review
- **Opus 5 fast mode plan-tiering** — Max/premium Team-Enterprise seats only, capped at 50% of weekly usage, $10/$50 per Mtok, Claude API only (not Bedrock/Vertex/Foundry). Still research preview; reconsider a one-line pitfall on `surfaces/claude-api.md` if it reaches GA.
- **Subagent spawn-cap history is inconsistent across sources.** Secondary trackers (X/changelog aggregators) describe the 200-subagent-per-session cap as newly *added* in v2.1.223 (2026-08-05) rather than dating to v2.1.212 as previously recorded in this guide's changelog; the canonical Subagents reference doesn't date the addition, only the v2.1.224 removal. We trust the canonical doc for current state (no cap) and note the discrepancy rather than resolve it.
- **Claude for Government (beta)** and **org-level inference hooks / DLP for Enterprise** — surfaced in this week's news roundup; both are enterprise/compliance-admin features, not beginner component-model concepts, so omitted by scope, consistent with prior exclusions of similar admin-only tooling.
- **Agent SDK billing split** — carried over; still paused per the help-center notice as of last verification. Re-check next run.
- Carried over from 2026-08-01: Mythos 5 GA restricted to approved orgs; promote `security-guidance` to its own page only if a human expands the fixed topic list.

## 2026-08-01

### Added
- **[Claude surfaces] Computer use (Research Preview)** — desktop screen-control shared by Claude Cowork and the Claude Code Desktop app, launched 2026-03-23 but missing from the guide; a genuine discoverability gap ([Anthropic help center](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork), verified 2026-08-01). Also mentioned on `claude-code.md`, `claude-cowork.md`, and `claude-desktop.md`.
- **[Claude surfaces] Dispatch** — mobile-to-desktop task handoff (QR-pair phone with Claude Desktop), also launched 2026-03-23 and previously undocumented ([Anthropic blog](https://claude.com/blog/dispatch-and-computer-use), [help center](https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork)).

### Updated
- **[MCP servers] MCP 2026-07-28 spec** — noted the protocol's move to a stateless request/response core, hardened OAuth/OIDC, and versioned Apps/Tasks extensions; no install-command impact ([Anthropic blog](https://claude.com/blog/bringing-mcp-2026-07-28-to-claude), [MCP spec blog](https://blog.modelcontextprotocol.io/posts/2026-07-28/), published 2026-07-28).
- **[Connectors] Directory size** — refreshed the stale "over 200 connectors" figure to Anthropic's 2026-07-28 count of 950+ MCP servers in the directory.
- **[Claude Cowork] Web/mobile beta** — added the 2026-07-07 expansion of Cowork to `claude.ai` and iOS/Android (Max-first, background execution, cross-device continuity), which had shipped but wasn't reflected on the page ([Anthropic blog](https://claude.com/blog/cowork-web-mobile)).
- **[Claude Tag] Migration deadline** — replaced the vague "30-day window" with the concrete August 3, 2026 auto-migration cutover, plus the org-vs-individual billing split (channel work bills the org, DMs bill the user), confirmed against Anthropic's help center.

### Verified (no changes)
- Claude Code install command, launch surfaces, and changelog (through v2.1.220, 2026-07-25) — no beginner-relevant changes since last run.
- Claude API model guidance (Opus 5, Sonnet 5, Fable 5) — already current, re-verified against this week's news.
- Skills, Plugins, Marketplaces, Decision tree, Hooks, Slash commands, Routines, Authentication — spot-checked, no stale claims found this run.

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

