---
title: Guide updates
parent: Updates
nav_order: 2
permalink: /updates/guide.html
---

# Guide updates

Reverse-chronological log of changes to the [guide](guide/). Newest at the top.

<!-- Curator appends new dated entries directly below this line. -->

## 2026-06-06

### Updated
- **[claude-surfaces, surfaces/claude-code] Dynamic-workflow trigger keyword renamed `workflow` → `ultracode` (v2.1.160).** Per the [dynamic workflows docs](https://code.claude.com/docs/en/workflows) (verified this run via WebSearch summary, corroborated by v2.1.160 release coverage), the single-task trigger keyword changed from `workflow` to `ultracode`; the bare word `workflow` no longer fires a run. Both pages previously told beginners to "include the word `workflow` in your prompt" — stale since the v2.1.160 rename. Rewrote both bullets to say `ultracode` (noting the rename) and clarified that `/effort ultracode` is a session setting (sends xhigh + auto-orchestration), not a model effort level. Beginner-relevant because anyone copying the old instruction from a late-May tutorial silently gets no workflow.
- **[plugins] `/plugin list` gained `--enabled` / `--disabled` filters (v2.1.163, 2026-06-04).** Added the filter flags to the management-commands sentence and refreshed the changelog source line ([Claude Code changelog](https://code.claude.com/docs/en/changelog)).

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified against `claude.com/product/claude-code`; Channels, Claude Security, MCP tunnels, routines, sandboxing all current. June news (Claude Partner Network 2026-06-03, Project Glasswing/Mythos critical-infrastructure expansion 2026-06-02, doubled Claude Code rate limits) is corporate/infra, not beginner component-model material.
- surfaces/claude-code.md — install methods, `/code-review`/`/simplify` split, `/goal`, background sessions all current. v2.1.163 (2026-06-04) and v2.1.165 are dominated by bug fixes, version-gating managed settings, and a slash-command autocomplete UX tweak (click fills instead of runs) — below the beginner threshold.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged. Opus 4.8 effort ladder (low/medium/high/xhigh/max) confirmed unchanged; only the default shifted to high.
- skills.md, mcp-servers.md, marketplaces.md, connectors.md, decision-tree.md — unchanged this run.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch remained unavailable this run (404 on `claude-3-5-haiku-20241022`, same regression as prior runs). All verification went through WebSearch summaries of `code.claude.com/docs/en/workflows`, `code.claude.com/docs/en/changelog`, `claude.com/product/claude-code`, `github.com/anthropics/claude-code/releases`, `anthropic.com/news`, `releasebot.io/updates/anthropic`, plus secondary v2.1.160/4.8 coverage. A human should spot-check the workflows docs page directly to confirm the `ultracode`-keyword wording is canonical.
- **Effort ladder vs `ultracode` future drift** — `ultracode` is currently a session setting layered over `xhigh`. If Anthropic promotes it to a real effort level or renames the keyword again, revisit both Dynamic Workflows bullets.
- **`claude -p` / Agent SDK billing split lands 2026-06-15** — carried over; re-verify after the date.
- **Sonnet 4 / Opus 4 retirement 2026-06-15 9am PT** — carried over; re-verify after the date.
- **Promote `security-guidance` to its own page** — carried over from 2026-06-04.
- **Claude Mythos public release** — carried over.

## 2026-06-05

### Updated
- **[surfaces/claude-code] `/simplify` is no longer an alias for `/code-review --fix`.** Per the [v2.1.154 changelog (2026-05-28)](https://code.claude.com/docs/en/changelog) and corroborating coverage at [neoteric.no](https://www.neoteric.no/blog/claude-code-s-simplify-stopped-fixing-code-yesterday/), `/simplify` returned as a distinct cleanup-only command (reuse, simplification, efficiency, altitude — no bug-hunting). The previous claim on `surfaces/claude-code.md` that "`/simplify` now invokes `/code-review --fix`" was correct for v2.1.152 only and went stale a day later. Rewrote the `/code-review` bullet to spell out the current split (`/code-review` for bug-hunting, `/simplify` for cleanup-only) and updated the changelog source line. Beginner-relevant because anyone who scripted `/simplify` for bug-finding off a tutorial from May 27 will get different behavior today.
- **[surfaces/claude-code] `claude --bg --exec` and `!` background-job prefix in `claude agents`.** Per the May 2026 release notes (consolidated at [claudefa.st changelog](https://claudefa.st/blog/guide/changelog) and [Anthropic's agent-view blog post](https://claude.com/blog/agent-view-in-claude-code)), in `claude agents` you can prefix a shell command with `!` to spin it up as a detachable background job, equivalent to `claude --bg --exec '<command>'` from the shell. Added a single-sentence clarification to the existing `claude --bg` bullet. Beginner-relevant because the `!` shortcut is the path most users will discover first from the agent view UI.

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified via WebSearch against `claude.com/product/claude-code`; Channels, Dynamic Workflows, Claude Security, MCP tunnels, routines, sandboxing all current. The 2026-06-05 "Claude will remain ad-free" announcement is corporate policy, not a product change.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged this run.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged this run. The `security-guidance` plugin (added 2026-06-04) remains the latest plugins.md addition.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was unavailable again this run (404 on `claude-3-5-haiku-20241022`, same regression as the past several runs). All source verification this run went through WebSearch summaries of `code.claude.com/docs/en/changelog`, `code.claude.com/docs/en/code-review`, `code.claude.com/docs/en/whats-new/2026-w22`, `github.com/anthropics/claude-code/blob/main/CHANGELOG.md`, `claudefa.st/blog/guide/changelog`, `claude.com/blog/agent-view-in-claude-code`, `neoteric.no/blog/claude-code-s-simplify-stopped-fixing-code-yesterday/`, `anthropic.com/news`, and `claudelog.com/faqs/claude-code-release-notes/`. A human should spot-check the Code review docs page directly to confirm the wording that `/simplify` "runs a separate cleanup-only review that applies fixes without hunting for bugs" is still on the canonical page.
- **`/simplify` vs `/code-review` future drift.** The two commands have changed roles three times in eight days (rename → alias → split). If Anthropic merges them again, or further differentiates the cleanup categories, revisit. The bullet is now intentionally explicit about the split so a future merge will be visible as a rewrite.
- **Claude Mythos public release** — carried over from 2026-06-04.
- **Project Glasswing expansion 2026-06-02** — carried over.
- **`--channels` allowlist expansion** — carried over from 2026-06-03.
- **`/code-review --comment` lock-in** — carried over.
- **Sonnet 4 / Opus 4 retirement follow-up after 2026-06-15** — carried over.
- **`claude -p` / Agent SDK billing split lands 2026-06-15** — carried over.
- **Promote `security-guidance` to its own page** — carried over from 2026-06-04.

## 2026-06-04

### Added
- **[plugins] `security-guidance` plugin as recommended first install.** Per [Catch security issues as Claude writes code](https://code.claude.com/docs/en/security-guidance) (Anthropic docs) and the [Week 22 release notes](https://code.claude.com/docs/en/whats-new/2026-w22) (2026-05-25 – 2026-05-29), Anthropic shipped a free `security-guidance` plugin to `claude-plugins-official` that has Claude review its own code edits for common vulnerabilities (injection, unsafe deserialization, unsafe DOM APIs) and fix findings in the same session. Three layers: deterministic per-edit pattern check (no model call, no cost), end-of-turn diff review by a separate Claude instance, and an agentic commit review (capped 20 / rolling hour). Install via `/plugin install security-guidance@claude-plugins-official` then `/reload-plugins`. Requires Claude Code v2.1.144+ and Python 3.8+. Reportedly cut security-related PR comments by 30–40% in Anthropic's internal rollout; 157k downloads in the first 24 hours. Added a sentence to the install section of `plugins.md` next to the existing `claude-code-setup` recommendation, plus two new source lines. Beginner-relevant because it's free, pre-registered, no separate marketplace step, and answers a question every new Claude Code user has ("how do I keep Claude from writing unsafe code?"). Surfaced via the discovery directive — the launch was 2026-05-27 and the guide had simply missed it.

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) and the existing cross-cutting features (Channels, Dynamic Workflows, Claude Security, background sessions, MCP tunnels, routines, sandboxing) all current. v2.1.162 (published ~2026-06-03) is a 28-change CLI release dominated by bug fixes and a refinement to `WebFetch(domain:NAME)` deny/ask/allow precedence — below the threshold for this page.
- surfaces/claude-code.md — `/code-review --comment` (added 2026-06-03), `/goal`, Dynamic Workflows, background sessions, install methods all unchanged. v2.1.162 introduces no new beginner-facing user-visible features.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged this run.
- skills.md, mcp-servers.md, marketplaces.md, connectors.md, decision-tree.md — unchanged this run. (`security-guidance` is a plugin, so the addition lives on `plugins.md`.)
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was unavailable again this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `code.claude.com/docs/en/security-guidance`, `code.claude.com/docs/en/whats-new/2026-w22`, `code.claude.com/docs/en/changelog`, `claude.com/plugins/security-guidance`, `github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance`, `helpnetsecurity.com/2026/05/27/anthropic-claude-code-security-guidance-plugin/`, `cybersecuritynews.com/free-security-plugin-for-claude-code/`, `securityweek.com/anthropic-releases-new-claude-sandbox-security-guidance-plugin/`, and `claudefa.st/blog/guide/changelog`. A human should spot-check `claude.com/plugins/security-guidance` directly to confirm the install command is still `/plugin install security-guidance@claude-plugins-official` (some secondary sources show variations).
- **Promote `security-guidance` to its own `advanced/security-guidance.md` page?** Today it's a sentence on `plugins.md`. If Anthropic ships analogous plugins for other domains (lint, performance, accessibility) the pattern starts to look like a class of feature, not a single plugin, and would warrant its own advanced page. Hold off until then.
- **Claude Mythos public release** — carried over from 2026-06-03.
- **Project Glasswing expansion 2026-06-02** — carried over.
- **`--channels` allowlist expansion** — carried over from 2026-06-03.
- **`/code-review --comment` lock-in** — carried over.
- **Sonnet 4 / Opus 4 retirement follow-up after 2026-06-15** — carried over.
- **`claude -p` / Agent SDK billing split lands 2026-06-15** — carried over.

## 2026-06-03

### Added
- **[claude-surfaces, mcp-servers] Channels (Research Preview) — MCP push-mode.** Per the [Channels reference](https://code.claude.com/docs/en/channels-reference) and [Vibe Sparking AI's v2.1.80 changelog post](https://www.vibesparking.com/en/blog/ai/claude-code/changelog/2026-03-20-claude-code-2180-channels-mcp-push-messages/), Claude Code v2.1.80 (2026-03-20) added the `--channels` flag that lets allowlisted MCP servers *push* events into a running session — inverting MCP from pull-only to bidirectional. Bundled plugins: Telegram, Discord, iMessage, `fakechat`. Requires `claude.ai` OAuth (no API-key auth); Team / Enterprise admins must set `channelsEnabled: true` and may curate `allowedChannelPlugins`. Custom channels need `--dangerously-load-development-channels`. This is a 2.5-month-old shipped feature that the guide had simply missed — picked up via the directive to scan for cross-cutting features beginners would otherwise miss. Added a bullet to `claude-surfaces.md` cross-cutting features, a pitfall on `mcp-servers.md` ("Assuming MCP is pull-only"), and Sources updates on both. Beginner-relevant because channels change the mental model of what an MCP server can do (no longer just a tool the model calls).
- **[surfaces/claude-code] `/code-review --comment` for inline GitHub PR comments.** Per the [Code review docs](https://code.claude.com/docs/en/code-review) and the v2.1.161 changelog (2026-06-02), `/code-review` now accepts `--comment` to post findings as inline PR comments (≥ 80-confidence, deduped, no duplicate suggestions). Added a "When to use it" bullet on `surfaces/claude-code.md` covering the three flags (`/code-review`, `--comment`, `--fix`) as a single review path that doesn't require installing the GitHub App. Beginner-relevant because PR review is a primary Claude Code job-to-be-done and `--comment` finally closes the loop without extra setup.

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified against [`claude.com/product/claude-code`](https://claude.com/product/claude-code) via WebSearch; Dynamic Workflows, Claude Security, background sessions, MCP tunnels, routines, sandboxing all current. v2.1.158–v2.1.161 introduce no other new beginner-facing claims for this page beyond the Channels addition.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged this run. The 2026-06-01 IPO filing is corporate news (already flagged 2026-06-02); Project Glasswing expansion (2026-06-02) and Claude Mythos public-release signals are tracked under Flagged for review.
- skills.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged this run. The `effort` frontmatter on skills and slash commands (v2.1.161) extends the existing `disallowed-tools` story but is below the threshold for beginner pages.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was unavailable again this run (404 on `claude-3-5-haiku-20241022`). Source verification went through WebSearch summaries of `code.claude.com/docs/en/changelog`, `code.claude.com/docs/en/channels-reference`, `code.claude.com/docs/en/code-review`, `claude.com/product/claude-code`, `anthropic.com/news`, `techcrunch.com/2026/06/02/`, `cybersecuritynews.com`, `9to5mac.com/2026/06/02/`, and `simonwillison.net/2026/Jun/1/may-newsletter/`. A human should spot-check the Channels reference page directly to confirm the per-plan defaults (`channelsEnabled: false` on Team / Enterprise) and the `allowedChannelPlugins` managed-setting name.
- **Claude Mythos public release.** Per [9to5Mac 2026-06-02](https://9to5mac.com/2026/06/02/anthropic-expands-glasswing-as-it-promises-public-claude-mythos-class-model-releases/), [Bleeping Computer](https://www.bleepingcomputer.com/news/artificial-intelligence/anthropics-restricted-claude-mythos-model-may-be-coming-to-claude-code/), and [TechCrunch 2026-06-02](https://techcrunch.com/2026/06/02/anthropic-scales-claude-mythos-to-critical-infrastructure-in-15-countries/), Anthropic confirmed Mythos-class models will reach all customers "in the coming weeks" and the model ID `claude-mythos-1-preview` briefly appeared in public Claude Code and Claude Security toggles before being pulled. When it ships, the `surfaces/claude-api.md` model-family list (Opus 4.8 / Sonnet 4.6 / Haiku 4.5) will need a fourth tier and `surfaces/claude-code.md` will likely need a Mythos pitfall analogous to Opus 4.8's effort-default note.
- **Project Glasswing expansion 2026-06-02.** Anthropic added ~150 organizations across 15+ countries to Glasswing (power, water, healthcare, communications, hardware). The expansion itself is a B2B program, not a beginner-facing product. The connected **Cyber Verification Program** that would let outside orgs use Mythos-class capabilities for cyberdefense tasks could become beginner-relevant if it ships as a self-service offering — track.
- **`--channels` allowlist expansion.** Today the only allowlisted channel plugins are Telegram, Discord, iMessage, and `fakechat` (in `claude-plugins-official`). If Anthropic ever flips channels out of research preview or expands the allowlist (e.g., Slack, webhook generic), revisit `mcp-servers.md` to widen the pitfall and consider promoting Channels to its own `advanced/channels.md` page.
- **`/code-review --comment` lock-in.** Once `--comment` is the default review path for PRs (it appears Anthropic is positioning it as such over the GitHub App), consider rewriting the bullet to lead with `--comment` rather than describing all three flags symmetrically.
- **Sonnet 4 / Opus 4 retirement follow-up after 2026-06-15.** Carried over: once those IDs are off the platform, drop the dated pitfall and fold the lesson into the existing "default model IDs change" bullet on `surfaces/claude-api.md`.
- **`claude -p` / Agent SDK billing split lands 2026-06-15.** Carried over: after the date, the "moves to a separate Agent SDK credit on 2026-06-15" pitfalls on `surfaces/claude-api.md` and `surfaces/claude-code.md` shift from forward-looking warnings to plain present-tense facts.

## 2026-06-02

### Added
- **[surfaces/claude-api, surfaces/claude-code] Agent SDK / `claude -p` billing split, effective 2026-06-15.** Per Anthropic's 2026-05-14 announcement ([InfoWorld 2026-05-14](https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html), [The New Stack 2026-05-15](https://thenewstack.io/anthropic-agent-sdk-credits/)), Claude Agent SDK usage, `claude -p` (headless Claude Code), Claude Code GitHub Actions, and third-party harnesses that auth via the Agent SDK leave the subscription rate-limit pool on 2026-06-15 and move to a separate dollar-denominated "Agent SDK credit" billed at standard API rates (Pro $20, Max 5x $100, Max 20x $200, Team $100/seat, Enterprise $200/seat; one-time opt-in, no rollover, refreshes monthly). Interactive `claude` in the terminal, Claude.ai chat, and Cowork stay on subscription limits. Added a pitfall on `surfaces/claude-api.md` (full per-plan amounts) and a pointer pitfall on `surfaces/claude-code.md` (which surface is affected and where to read the detail). Beginner-relevant because the change directly affects whether agentic usage is "included" in a Pro/Max plan as of 2026-06-15 — touches the API and Claude Code surfaces both.
- **[surfaces/claude-api] Sonnet 4 / Opus 4 retirement on 2026-06-15.** Per [`platform.claude.com/docs/en/about-claude/model-deprecations`](https://platform.claude.com/docs/en/about-claude/model-deprecations), `claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire on 2026-06-15 at 9am PT and will return errors after that date. Added a dedicated pitfall under "Default model IDs change" naming the retiring IDs, the recommended replacements (`claude-sonnet-4-6` / `claude-opus-4-7`), and that `budget_tokens` for extended thinking is deprecated in favor of `thinking: {type: "adaptive"}`. Beginner-relevant because hard-coded model IDs from a year-old tutorial break in two weeks.

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`), Dynamic Workflows, Claude Security, background sessions, MCP tunnels, routines, sandboxing all current. v2.1.157 (.claude/skills auto-load, `claude plugin init`), v2.1.158 (Auto mode on Bedrock/Vertex/Foundry), and v2.1.159 (internal infra) introduce no new beginner-facing claims for this page.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged this run. The 2026-06-01 IPO filing is a corporate milestone, not a product change.
- skills.md, mcp-servers.md, plugins.md (`.claude/skills/` auto-load + `claude plugin init` from v2.1.157 already documented 2026-05-30), marketplaces.md, connectors.md, decision-tree.md — unchanged this run.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `code.claude.com/docs/en/changelog`, `github.com/anthropics/claude-code/releases`, `claude.com/product/claude-code`, `anthropic.com/news`, `platform.claude.com/docs/en/about-claude/model-deprecations`, `infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html`, `thenewstack.io/anthropic-agent-sdk-credits/`, and `simonwillison.net/2026/Jun/1/may-newsletter/`. A human should spot-check the Agent SDK credit terms directly via the Anthropic Help Center once the 2026-06-08 credit-claim email goes out — the per-plan amounts and the one-time-opt-in step are consistent across multiple independent sources but worth confirming on the first-party page.
- **Dedicated `advanced/agent-sdk-credits.md` or `surfaces/claude-api.md` reorg.** Today the billing split is two pitfalls (one on `claude-api.md`, one on `claude-code.md`). If the credit pool becomes the default way beginners think about agentic usage (e.g., Anthropic ships a Console page showing credit balance separately), promote to its own advanced page next to `authentication.md`.
- **Sonnet 4 / Opus 4 retirement follow-up after 2026-06-15.** Once those IDs are off the platform, drop the dated pitfall and fold the lesson into the existing "default model IDs change" bullet.
- **Claude Mythos public release.** Anthropic's Opus 4.8 announcement hinted Mythos-class models will reach customers "in the coming weeks". When they ship, the `surfaces/claude-api.md` model-family list will need a fourth tier.

## 2026-05-31

### Added
- **[claude-surfaces] Sandboxing differs by surface — cross-cutting note.** Per Anthropic's engineering post [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) (late May 2026, surfaced 2026-05-30 on [Simon Willison's link blog](https://simonwillison.net/2026/May/30/how-we-contain-claude/)), each Claude surface uses a different containment stack: gVisor for Claude.ai, Seatbelt (macOS) / Bubblewrap (Linux) for Claude Code running locally with reads allowed / writes scoped to the workspace / network denied by default, and a full VM (Apple Virtualization on macOS, HCS on Windows) for Cowork. Local MCP servers wired into Claude Desktop run with the user's permissions, not inside a sandbox. Added as a cross-cutting bullet on `claude-surfaces.md` with sources. Beginner-relevant because it answers "what can Claude actually touch on my machine?" — a question several existing pitfalls (Claude Desktop MCP, Cowork VM, Claude Code on the web) hint at but none answered coherently.

### Verified (no changes)
- claude-surfaces.md — install command, Dynamic Workflows, Claude Security, background sessions, MCP tunnels, routines all current. The sandboxing addition above is the only structural change.
- surfaces/claude-code.md — `curl -fsSL https://claude.ai/install.sh | bash` re-verified against `claude.com/product/claude-code`. v2.1.158 (2026-05-30, Auto mode env var on Bedrock/Vertex/Foundry) remains too internal for beginner pages — already flagged 2026-05-30. No new releases through 2026-05-31.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged this run.
- skills.md, mcp-servers.md, plugins.md (`.claude/skills/` auto-load + `claude plugin init` from v2.1.157), marketplaces.md, connectors.md, decision-tree.md — unchanged this run.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `code.claude.com/docs/en/changelog`, `code.claude.com/docs/en/whats-new`, `claude.com/product/claude-code`, `anthropic.com/news`, `anthropic.com/engineering/how-we-contain-claude`, `simonwillison.net/2026/May/30/how-we-contain-claude/`, `releasebot.io/updates/anthropic/claude-code`, and `claudefa.st/blog/guide/changelog`. A human should spot-check the engineering post directly to confirm the per-surface containment stack (gVisor / Seatbelt / Bubblewrap / Apple Virtualization / HCS) and the late-May publication date.
- **Dedicated `advanced/sandboxing.md` page.** Today the containment model is a single cross-cutting bullet on `claude-surfaces.md`. If Anthropic ships per-surface sandbox controls users can configure (e.g., a `--no-sandbox` flag, custom egress allowlists, or trust-prompt overrides) the bullet should be promoted to its own advanced page.
- **`How we contain Claude` exact publication date.** The engineering post lacks an explicit datestamp on the page in search-index excerpts; placeholder is "late May 2026". A human should verify the exact date by viewing the page directly.

## 2026-05-30

### Updated
- **[plugins] Plugin auto-loading from `.claude/skills/` and `claude plugin init` scaffolding.** Per the [Claude Code v2.1.157 changelog](https://code.claude.com/docs/en/changelog) (released 2026-05-29), any plugin placed inside a `.claude/skills/` directory (project or user) is now auto-loaded with no marketplace registration step, and `claude plugin init <name>` scaffolds a starter plugin there. Added a "Author a plugin without a marketplace" paragraph to the install section on `plugins.md` and refreshed the changelog source line. Beginner-relevant because it collapses the "create a marketplace just to try out a local plugin" hurdle into a single command.

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`), Dynamic Workflows, Claude Security, background sessions, MCP tunnels, routines all current. v2.1.156 (bug fixes; combined auth notification) and v2.1.158 (auto mode on Bedrock/Vertex/Foundry behind `CLAUDE_CODE_ENABLE_AUTO_MODE=1`) introduce no new beginner-facing claims.
- surfaces/claude-code.md — `/goal`, Dynamic Workflows, background sessions, `claude agents`, `claude --bg`, install methods all unchanged.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged this run.
- skills.md — `~/.claude/skills/` layout, `/skills` picker, `/reload-skills`, `disallowed-tools` frontmatter unchanged. The v2.1.157 plugin-auto-loading change touches plugin authoring rather than skill authoring, so it belongs on `plugins.md` not `skills.md`.
- mcp-servers.md, marketplaces.md, connectors.md, decision-tree.md — unchanged this run.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `code.claude.com/docs/en/changelog`, `github.com/anthropics/claude-code/releases`, `releasebot.io/updates/anthropic/claude-code`, `claude.com/product/claude-code`, `anthropic.com/news`, and `simonwillison.net/2026/`. A human should spot-check the v2.1.157 entry on `code.claude.com/docs/en/changelog` directly to confirm `.claude/skills/` (not `.claude/plugins/`) is the auto-load directory — older plugin docs scaffolded into `.claude-plugin/` and the rename is easy to miss.
- **`CLAUDE_CODE_ENABLE_AUTO_MODE=1` on Bedrock/Vertex/Foundry (v2.1.158, 2026-05-30).** Held off documenting — Auto mode is already enabled by default on the Anthropic API, and the env-var workaround is a cloud-provider specific configuration that doesn't belong in beginner-facing prose. Revisit if Anthropic flips the default on those clouds and the env var becomes legacy.
- **`claude doctor` last-update-result reporting + status-line `COLUMNS`/`LINES` env vars (v2.1.156).** Both are observability / TUI niceties below the threshold for beginner pages.

## 2026-05-29 (later run)

### Added
- **[surfaces/claude-api] Mid-conversation system messages on Opus 4.8.** Per [Mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages) (verified 2026-05-29) and Simon Willison's [Opus 4.8 post](https://simonwillison.net/2026/May/28/claude-opus-4-8/) (2026-05-28), the Messages API now accepts `role: "system"` entries inside the `messages` array (placed immediately after a user turn) on Opus 4.8 only. Lets you update instructions mid-conversation without restating the top-level system prompt and without invalidating the cached prefix — useful for long agentic loops. Earlier models 400 on `role: "system"` in `messages`. Available on the Claude API and Claude Platform on AWS; not yet on Bedrock, Vertex, or Foundry. Folded into the prompt-caching pitfall on `surfaces/claude-api.md` and added a source. Beginner-relevant for anyone building on the API who already understands prompt caching.

### Verified (no changes)
- claude-surfaces.md — Dynamic Workflows, Claude Security, background sessions, MCP tunnels, routines all current. v2.1.155 (Windows/Terminal fixes) and v2.1.156 (MCP/agent bug fixes) introduce no new beginner-facing claims.
- surfaces/claude-code.md — `curl -fsSL https://claude.ai/install.sh | bash` re-verified against `claude.com/product/claude-code`; install methods, `/goal`, Dynamic Workflows, background sessions, `claude agents`, `claude --bg` all unchanged. v2.1.155/156 are bug-fix patch releases.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged this run.
- skills.md, mcp-servers.md, plugins.md, marketplaces.md, connectors.md, decision-tree.md — unchanged this run.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). Source verification went through WebSearch summaries of `code.claude.com/docs/en/changelog`, `claude.com/product/claude-code`, `anthropic.com/news`, `simonwillison.net/2026/May/28/claude-opus-4-8/`, `platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages`, and `releasebot.io/updates/anthropic/claude-code`. A human should spot-check `platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages` directly to confirm the placement constraints and 400-error behavior on earlier models.
- **Enterprise connector permissions in custom roles (2026-05-28).** Admin-only and currently captured nowhere in the guide. Held off because the beginner pages don't yet enumerate Team/Enterprise admin controls. Revisit if the same controls reach Pro/Team or surface in the Claude.ai Settings UI rather than the Admin console.
- **Combined "needs authentication" startup notification** (v2.1.155-ish, May 2026): a small UX consolidation merging the separate MCP-server and connector auth notifications into one. Too internal for a beginner page, but a candidate `Common pitfalls` bullet on `mcp-servers.md` if users start asking about it.

## 2026-05-29

### Added
- **[claude-surfaces, surfaces/claude-code] Dynamic Workflows in Claude Code.** Per [Introducing dynamic workflows in Claude Code](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) (2026-05-28) and the [official workflows doc](https://code.claude.com/docs/en/workflows), Anthropic shipped Dynamic Workflows in research preview on 2026-05-28 alongside Opus 4.8 and v2.1.154. Claude writes an orchestration script on the fly and runs up to 1,000 parallel subagents (16 concurrent) for migrations, audits, and other large jobs. Trigger via the keyword `workflow` in a prompt or `/effort ultracode`. On by default on Max / Team, admin-gated on Enterprise, off by default on Pro (toggle in `/config`). Spans CLI / Desktop / VS Code extension — qualifies as cross-cutting. Added a bullet to `claude-surfaces.md` cross-cutting features and a "When to use it" bullet on `surfaces/claude-code.md` pointing back to it; Sources expanded on both. Beginner-relevant because the `workflow` keyword now changes Claude Code behavior even for users who don't opt in deliberately.
- **[surfaces/claude-api] Claude Opus 4.8.** Per [Introducing Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) (2026-05-28) and the [What's new in Opus 4.8 doc](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8), the `opus` alias on the Anthropic API now resolves to `claude-opus-4-8` with 1M-token context by default (no beta header, no premium pricing). On Bedrock / Vertex / Foundry aliases lag; pin the full ID or set `ANTHROPIC_DEFAULT_OPUS_MODEL`. Updated the "Default model IDs change" pitfall and added two sources.
- **[surfaces/claude-ai] Claude Design.** Per [Introducing Claude Design by Anthropic Labs](https://www.anthropic.com/news/claude-design-anthropic-labs) (2026-04-17), Anthropic shipped a quick-visuals tool at `claude.ai/design` covering prototypes, slides, and one-pagers. Available to Pro / Max / Team / Enterprise (off by default on Enterprise until admin enables). Added a one-line "When to use it" bullet and a source. Beginner-relevant because `claude.ai/design` is now a new top-level destination alongside `/code`, `/security`, `/directory/connectors`, and most beginners arriving via `claude.ai` should know it exists.

### Updated
- **[skills, advanced/slash-commands] `/reload-skills` and `disallowed-tools` frontmatter.** Per the Claude Code v2.1.152 changelog (2026-05-27), skills and slash commands can set `disallowed-tools:` in YAML frontmatter to remove specific tools while active, and `/reload-skills` re-scans skill directories without restarting. Replaced the prior "restart session to reload" guidance on `skills.md` and added the new frontmatter option on both `skills.md` and `advanced/slash-commands.md`. Sources refreshed.
- **[advanced/hooks] `MessageDisplay` event + `SessionStart.reloadSkills` + `sessionTitle`.** Per the v2.1.152 changelog, hooks gained a `MessageDisplay` event (transform / hide assistant message text) and `SessionStart` hooks can return `reloadSkills: true` or set the session title via `hookSpecificOutput.sessionTitle`. Added to the events list and source line.

### Verified (no changes)
- claude-surfaces.md — install command, Claude Security cross-cutting bullet, background sessions, routines, MCP tunnels unchanged. The Dynamic Workflows addition above is the only structural change.
- mcp-servers.md — `claude mcp add --transport http`, scope semantics, MCP tunnels Research Preview unchanged. v2.1.153 stateful-MCP reconnect-loop fix is internal stability; no beginner-facing change.
- plugins.md — `claude-plugins-official` pre-registration, `--plugin-dir` zip, `--plugin-url`, dependency-aware disable, `claude plugin prune`, `/plugin` Discover/Browse previews unchanged.
- marketplaces.md — source forms, seed-managed read-only behavior, finance + life-sciences marketplaces unchanged.
- connectors.md — `claude.ai/directory/connectors`, "over 200" framing, May 12 legal push, creative-tools wave unchanged.
- decision-tree.md — table unchanged.
- surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged this run. Effort control launching on Claude.ai and Cowork on 2026-05-28 is captured implicitly via the Dynamic Workflows / Opus 4.8 entries; deliberate not to over-instrument beginner pages with `/effort` mechanics yet.
- advanced/routines.md, advanced/authentication.md — unchanged this run.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `code.claude.com/docs/en/workflows`, `claude.com/blog/introducing-dynamic-workflows-in-claude-code`, `anthropic.com/news/claude-opus-4-8`, `platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8`, `anthropic.com/news/claude-design-anthropic-labs`, `dev.classmethod.jp/en/articles/20260524-claude-code-updates-v2-1-152/`, and `dev.classmethod.jp/en/articles/20260528-claude-code-updates-v2-1-153/`. A human should occasionally verify the `claude.com/blog/introducing-dynamic-workflows-in-claude-code` blog post directly to confirm the Pro-plan default (sources disagree on whether Pro gets workflows off-by-default in `/config` or not at all).
- **Dynamic Workflows as a dedicated `advanced/workflows.md` page.** Currently captured as a cross-cutting bullet on `claude-surfaces.md` and a single line on `surfaces/claude-code.md`. If usage settles (it leaves research preview, the `workflow` keyword trigger or `/effort ultracode` ergonomics change, or the 1,000-agent cap becomes relevant for routine work), promote to a dedicated `guide/advanced/workflows.md` page alongside hooks / slash-commands / routines.
- **Effort control on Claude.ai and Cowork.** Anthropic announced effort control extending beyond Claude Code on 2026-05-28 but the per-surface ergonomics aren't yet documented; revisit when the `claude.ai` and Cowork UIs surface an `/effort` equivalent or model-selector.

## 2026-05-27

### Added
- **[surfaces/claude-code] `/goal` completion-condition loop.** Per the [Anthropic docs](https://code.claude.com/docs/en/goal) and the Claude Code v2.1.139 changelog (released 2026-05-12), `/goal "<condition>"` keeps Claude working across turns until a separate evaluator model confirms the condition holds (e.g., `npm test exits 0`). Added a one-line "When to use it" bullet and refreshed the changelog source line. Beginner-relevant because it's a first-class entry point for unattended Claude Code work; pairs with the existing `claude --bg` / `claude agents` background-session story.
- **[marketplaces, plugins] Anthropic finance-services marketplace.** Per [Agents for financial services](https://www.anthropic.com/news/finance-agents) (2026-05-05) and the [Cowork install help center page](https://support.claude.com/en/articles/13851150-install-financial-services-plugins-for-cowork), Anthropic shipped 10 finance agent templates (pitch builder, KYC screener, month-end closer, …) as plugins for both Cowork and Claude Code from `anthropics/financial-services`. Added a second domain-marketplace example alongside `anthropics/life-sciences` on `marketplaces.md` (with the canonical `/plugin marketplace add anthropics/financial-services` + `financial-analysis@claude-for-financial-services` install), and noted the marketplace on `plugins.md` under "When to use it" and Sources. Beginner-relevant because finance is the second discipline (after life sciences) where Anthropic ships a curated domain marketplace; helps beginners pattern-match to their own field.

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`), background sessions, MCP tunnels Research Preview, Claude Security cross-cutting bullet all current per `claude.com/product/claude-code`. No new launches in the 2026-05-26/27 window — the 2026-05-26 "Claude stays ad-free" post is narrative, not a feature change.
- skills.md — `~/.claude/skills/` layout, `/skills` type-to-filter picker, root-level `SKILL.md` surfacing unchanged.
- mcp-servers.md — `claude mcp add --transport http`, scope semantics, MCP tunnels Research Preview unchanged. The v2.1.149 enterprise-only `allowAllClaudeAiMcps` setting and v2.1.150 MCP `--channels` research preview both remain too advanced for the beginner page.
- connectors.md — `claude.ai/directory/connectors`, "over 200" framing, May 12 legal push, creative-tools wave unchanged. Finance partner connectors (FactSet, Moody's, S&P Capital IQ, …) ship through the new marketplace plugin set rather than as one-click Claude.ai connectors, so they belong on `marketplaces.md`/`plugins.md` and not here.
- decision-tree.md — table unchanged.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged this run. The finance push lands on Cowork and Claude Code via the new marketplace; the surface sub-pages link out to `marketplaces.md`/`plugins.md` rather than duplicating the install command.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged this run.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `code.claude.com/docs/en/goal`, `anthropic.com/news`, `anthropic.com/news/finance-agents`, `github.com/anthropics/financial-services`, `support.claude.com/en/articles/13851150-install-financial-services-plugins-for-cowork`, `explainx.ai/blog/anthropic-claude-code-agent-view-goal-command`, and `venturebeat.com/orchestration/claude-codes-goals-separates-the-agent-that-works-from-the-one-that-decides-its-done`. A human should occasionally verify `/goal` syntax directly via `claude --help` or by running `/goal` in a session.
- **`/goal` as a beginner concept vs. an advanced one.** Currently captured only as a one-line bullet on `surfaces/claude-code.md`. If `/goal` continues to expand (e.g., scheduled `/goal` or chained completion conditions), promote to a dedicated `advanced/goal.md` page.
- **Finance partner connectors.** Several finance data providers (Moody's, FactSet, S&P, PitchBook, Daloopa, Morningstar) are referenced as MCP/connector integrations behind the finance plugins, but they aren't (yet) one-click Claude.ai connectors. If/when Anthropic surfaces them on `claude.ai/directory/connectors`, expand the connectors-page recent-waves list.

## 2026-05-26

### Added
- **[claude-surfaces, surfaces/claude-ai] Claude Security as a cross-cutting feature.** Per the [Anthropic blog](https://claude.com/blog/claude-security-public-beta) (2026-05-04) and the [getting-started tutorial](https://claude.com/resources/tutorials/getting-started-with-claude-security), Claude Security entered public beta on Enterprise plans: a vulnerability-scanning product at `claude.ai/security` (sidebar icon in Claude.ai) that opens a Claude Code on the web remediation session and drafts a PR for each finding. Touches two surfaces — qualifies for the cross-cutting list. Added a bullet to `claude-surfaces.md` cross-cutting features and a "(Enterprise)" entry in the Claude.ai "When to use it" list pointing back to it; Sources expanded on both pages. Held off creating a dedicated `advanced/` page because the product is Enterprise-gated today.

### Updated
- **[surfaces/claude-code] `winget install Anthropic.ClaudeCode` for first-time Windows installs.** The page only listed `winget upgrade Anthropic.ClaudeCode`, which fails on a clean machine because there's nothing to upgrade. The `claude.com/product/claude-code` landing page lists `winget install Anthropic.ClaudeCode` as the first-time command. Updated the bullet to show install first with upgrade as a follow-up note; refreshed the landing-page and setup-doc verified dates.

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`), background sessions, MCP tunnels Research Preview all current per `claude.com/product/claude-code`. v2.1.150 (2026-05-23, infra-only) and v2.1.149 (2026-05-22, security/stability + `/usage` per-category breakdown) introduce no new beginner-facing claims for this page.
- skills.md — `~/.claude/skills/` layout, `/skills` type-to-filter picker, `/usage` per-category breakdown unchanged. v2.1.149 reaffirms `/usage`.
- mcp-servers.md — `claude mcp add --transport http`, scope semantics, MCP tunnels Research Preview unchanged. v2.1.149 added enterprise-only `allowAllClaudeAiMcps` managed setting — still held off documenting for beginners (enterprise-managed config path).
- plugins.md — `claude-plugins-official` pre-registration, `--plugin-dir` zip, `--plugin-url`, dependency-aware disable, `claude plugin prune`, `/plugin` Discover/Browse previews unchanged.
- marketplaces.md — source forms, seed-managed read-only behavior, pre-registration unchanged.
- connectors.md — `claude.ai/directory/connectors`, "over 200" framing, May 12 legal push, creative-tools wave unchanged.
- decision-tree.md — table unchanged.
- surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged this run.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged this run.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `claude.com/blog/claude-security-public-beta`, `claude.com/resources/tutorials/getting-started-with-claude-security`, `helpnetsecurity.com/2026/05/04/anthropic-claude-security-public-beta/`, `anthropic.com/news`, and `dev.classmethod.jp/en/articles/20260524-claude-code-updates-v2-1-150/`. A human should spot-check `claude.ai/security` directly to confirm the sidebar entry point.
- **Claude Security Team / Max access.** Anthropic announced Team and Max access is "coming soon" but has not yet shipped as of 2026-05-26. When it does, drop the "Enterprise only today" qualifier from both pages and consider promoting Claude Security to a dedicated `guide/advanced/claude-security.md` page.

## 2026-05-25

### Updated
- **[surfaces/claude-code] npm install path now flagged as deprecated.** Per the [Claude Code v2.1.149 release notes](https://github.com/anthropics/claude-code/releases/tag/v2.1.149) and recent secondary commentary ([vanja.io/install-claude-code](https://vanja.io/install-claude-code/), [DEV community 2026](https://dev.to/vpetreski/how-to-install-claude-code-the-right-way-in-2026-52kb)), Anthropic now prints a yellow "npm installation is deprecated" banner for users on the npm package. The prior wording ("still works and wraps the same native binary") understated this. Updated the install bullet and refreshed the changelog source line to cover v2.1.149 and v2.1.150 (2026-05-22 / 2026-05-23). Added a secondary source.
- **[surfaces/claude-cowork] Windows is GA, not preview.** Per [eWeek coverage](https://www.eweek.com/news/claude-cowork-general-availability-enterprise-controls/) and the [Anthropic help center](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork), Claude Cowork went generally available on macOS and Windows on 2026-04-09. The page previously said "Windows in preview" — corrected. Added a one-line note about Cowork's higher token consumption relative to chat and the lack of a Linux desktop client. Sources expanded.

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`), WinGet, Homebrew, apt/dnf/apk, background sessions (`claude --bg`, `/resume`, `claude agents`), MCP tunnels Research Preview unchanged. The npm-deprecation note lives on the Claude Code sub-page where the install list is exhaustive; the parent surfaces table does not enumerate install methods so no edit needed here.
- skills.md — `~/.claude/skills/` layout, `SKILL.md` open standard, `/skills` type-to-filter picker, `/usage` per-category breakdown (which v2.1.149 [release notes](https://github.com/anthropics/claude-code/releases/tag/v2.1.149) reaffirm) unchanged.
- mcp-servers.md — `claude mcp add --transport http`, scope semantics, MCP tunnels Research Preview unchanged. v2.1.149 added an enterprise-only `allowAllClaudeAiMcps` managed setting; held off documenting it since this page is beginner-facing and the setting is administered through enterprise managed-mcp configuration.
- plugins.md — `claude-plugins-official` pre-registration, `--plugin-dir` zip, `--plugin-url`, dependency-aware disable, `claude plugin prune`, `/plugin` Discover/Browse previews, Claude for Small Business example unchanged.
- marketplaces.md — source forms, seed-managed read-only behavior, pre-registration unchanged.
- connectors.md — Connectors directory at `claude.ai/directory/connectors`, "over 200" attributed to Anthropic blog, creative-tools wave (2026-04-28), legal push (2026-05-12), Claude for Small Business pointer unchanged.
- decision-tree.md — table unchanged.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-api.md — unchanged this run.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged this run.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). Primary-source verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `github.com/anthropics/claude-code/releases/tag/v2.1.149`, `eweek.com/news/claude-cowork-general-availability-enterprise-controls/`, `support.claude.com/en/articles/13345190-get-started-with-claude-cowork`, `anthropic.com/news`, and secondary commentary on the npm deprecation banner. A human should occasionally verify the deprecation banner text directly (search results report it as "npm installation is deprecated" but the exact wording may have been adjusted across releases).
- **Enterprise-only `allowAllClaudeAiMcps` managed setting (v2.1.149).** Not yet documented because it lives on Enterprise managed-mcp config rather than the beginner-facing `claude mcp add` path. Revisit if Anthropic surfaces it through the `/mcp` command or as a per-user toggle.

## 2026-05-24

### Updated
- **[skills] Root-level `SKILL.md` plugins now auto-surface as skills; `/usage` adds per-category breakdown.** Per the [Claude Code changelog](https://code.claude.com/docs/en/changelog) (May 2026), a plugin with a root-level `SKILL.md` and no `skills/` subdirectory is now recognized as a skill, and `/usage` shows what's driving limits usage broken down by skill, subagent, plugin, and per-MCP-server cost. Added one sentence each to the install section; sources updated.
- **[surfaces/claude-code] `claude agents` configuration flags and `/code-review --comment`.** Per the May 2026 changelog, `claude agents` now accepts `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--model`, `--effort` for configuring dispatched background sessions; the renamed `/code-review` command takes a `--comment` flag to post findings as inline GitHub PR comments; and fast mode now defaults to Opus 4.7 (previously 4.6). Source line refreshed accordingly.
- **[connectors] Creative-tools wave (2026-04-28) added; "over 200" framed as Anthropic's published count, not a current total.** Per [9to5Mac coverage](https://9to5mac.com/2026/04/28/anthropic-releases-9-new-claude-connectors-for-creative-tools-including-blender-and-adobe/), Anthropic added nine creative-tool connectors on 2026-04-28 (Blender, Adobe, Ableton, SketchUp, Splice, Affinity by Canva, etc.). The directory has visibly grown beyond Anthropic's last-published "over 200" figure (third-party trackers now list ≈ 414), so the page now explicitly attributes "over 200" to Anthropic's blog and lists the recent waves that have grown it further, rather than implying it's a current total. Source list expanded.

### Verified (no changes)
- claude-surfaces.md — `curl -fsSL https://claude.ai/install.sh | bash`, WinGet, Homebrew, apt/dnf/apk, npm wrapper, background sessions (`claude --bg`, `/resume`, `claude agents`), MCP tunnels Research Preview re-verified against `claude.com/product/claude-code` and `code.claude.com/docs/en/changelog`.
- mcp-servers.md — `claude mcp add --transport http`, scope semantics, MCP tunnels Research Preview unchanged.
- plugins.md — `claude-plugins-official` pre-registration, `--plugin-dir` zip, `--plugin-url`, dependency-aware disable, `claude plugin prune`, `/plugin` Discover/Browse previews, Claude for Small Business example unchanged. The root-level SKILL.md surfacing is captured on the skills page rather than duplicated here.
- marketplaces.md — source forms, seed-managed read-only behavior, pre-registration unchanged.
- decision-tree.md — table unchanged.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged this run; Opus 4.7 pricing/availability and Claude Managed Agents endpoints all still current.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `anthropic.com/news/claude-opus-4-7`, `claude.com/blog/connectors-for-everyday-life`, and `9to5mac.com/2026/04/28/anthropic-releases-9-new-claude-connectors-for-creative-tools-including-blender-and-adobe/`. A human should occasionally verify the connector-count discrepancy: third-party trackers now list ~414 connectors but Anthropic's own most recent blog still says "over 200" — if a fresher first-party count appears, the connectors page should adopt it.
- **Claude Design** (`claude.ai/design`, Anthropic Labs, launched with Opus 4.7 on 2026-04-16) is still in research preview and not yet promoted to a surface sub-page. Revisit when it exits research preview or develops a component model of its own.

## 2026-05-23

### Updated
- **[surfaces/claude-api] Claude Managed Agents now occupies real space on the API surface page.** The page previously mentioned Managed Agents in a single sentence; Anthropic moved three advanced capabilities to public beta at Code with Claude on 2026-05-06 (per the [launch blog](https://claude.com/blog/new-in-claude-managed-agents) and follow-up coverage), and beginners reading this page should know they exist. Added: the `/v1/agents` / `/v1/environments` / `/v1/sessions` endpoint family and `managed-agents-2026-04-01` beta header; one-line summaries of **Outcomes** (rubric-graded self-correction; canonical docs at [`platform.claude.com/docs/en/managed-agents/define-outcomes`](https://platform.claude.com/docs/en/managed-agents/define-outcomes)) and **Multi-agent Orchestration** (public beta); and **Dreams** in research preview (async memory consolidation, beta header `dreaming-2026-04-21`, canonical docs at [`platform.claude.com/docs/en/managed-agents/dreams`](https://platform.claude.com/docs/en/managed-agents/dreams)). Added a pitfall noting Managed Agents lives on separate endpoints — calling `/v1/messages` doesn't get you these features. Sources expanded to include the Outcomes and Dreams API doc pages, the launch blog, and Simon Willison's live blog of the keynote.
- **[surfaces/claude-code] Pinned background sessions.** Per [Claude Code changelog v2.1.147 (2026-05-21)](https://code.claude.com/docs/en/changelog), `claude agents` now supports Ctrl+T to pin a background session — pinned sessions stay alive when idle, are restarted in place on Claude Code updates, and are shed under memory pressure only after un-pinned sessions. Added as a refinement to the existing "background sessions accumulate" pitfall. Sources updated to reflect the v2.1.139–v2.1.148 range (which also confirms `/code-review` was renamed from `/simplify` in v2.1.147).

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified against `claude.com/product/claude-code` and `code.claude.com/docs/en/setup`; Windows PowerShell `irm https://claude.ai/install.ps1 | iex`, WinGet, Homebrew, apt/dnf/apk, npm wrapper, and Windows CMD `install.cmd` all still current. Sources `verified` dates refreshed.
- skills.md — `~/.claude/skills/` layout, `SKILL.md` open standard, `/skills` type-to-filter picker unchanged.
- mcp-servers.md — `claude mcp add --transport http` syntax, scope semantics, MCP tunnels Research Preview unchanged.
- plugins.md — `claude-plugins-official` pre-registered, `--plugin-dir` zip support, `--plugin-url`, dependency-aware disable, `claude plugin prune`, `/plugin` Discover/Browse previews, Claude for Small Business Cowork example unchanged. The reserved-name list and `claude.com/plugins` catalog URL surfaced in this run's research but adding either would push the page past its budget without informing a beginner's first install.
- marketplaces.md — source forms, seed-managed read-only behavior, pre-registration unchanged.
- connectors.md — `claude.ai/directory/connectors`, "over 200" count, May 12 legal push, Claude for Small Business pointer unchanged.
- decision-tree.md — table unchanged.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md — unchanged this run.
- advanced/hooks.md, advanced/slash-commands.md, advanced/routines.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `code.claude.com/docs/en/setup`, `claude.com/blog/new-in-claude-managed-agents`, `platform.claude.com/docs/en/managed-agents/{define-outcomes,dreams}`, `anthropic.com/news`, and `simonwillison.net/2026/May/6/code-w-claude-2026/`. A human should occasionally spot-check the Managed Agents docs to confirm `client.beta.agents` is still the canonical SDK entry point — it was named in two independent sources this run but not seen directly.
- **Claude Managed Agents as a dedicated guide topic.** It now hosts Outcomes, Dreams, Multi-agent Orchestration, Memory Stores — enough surface area to merit a dedicated `guide/advanced/managed-agents.md` page rather than a paragraph on `claude-api.md`. Held off this run because (a) the audience is beginners who mostly aren't shipping API products, and (b) the policy is to add a cross-cutting page only when a feature touches ≥ 2 surfaces — Managed Agents currently lives only on the API. Revisit if Claude.ai or Claude Code start surfacing Managed Agents UIs directly (the existing routines page already wraps a related cloud-execution surface).

## 2026-05-22

### Updated
- **[advanced/routines] Major corrections from the now-published primary docs.** The official [Automate work with routines](https://code.claude.com/docs/en/routines) page and the [research-preview launch blog](https://claude.com/blog/introducing-routines-in-claude-code) (2026-04-14) supersede the in-session observations the page was previously grounded on. Specifically: cron expressions are interpreted in your **local timezone** and converted to UTC automatically (not "cron is UTC" as the page claimed — flipped); triggers include **schedule, API, and GitHub events** (previously only schedule was named); **daily run caps** are 5 / 15 / 25 for Pro / Max / Team-Enterprise; the API beta header is `experimental-cc-routine-2026-04-01`; the `run_once_at` API field and the API "cannot delete" pitfall were dropped as no longer reflected in the canonical doc. Lede, "When to use it", and Sources rewritten accordingly.
- **[surfaces/claude-code] Desktop app redesign (2026-04-14) added as a fourth form.** Per the Anthropic [desktop-redesign blog](https://claude.com/blog/claude-code-desktop-redesign), the Claude Code desktop app was rebuilt around parallel sessions: session sidebar across repos, drag-and-drop panes, in-app file editor and diff viewer, SSH on macOS, per-session Git worktree. The "three forms" list became four; the lede was updated; `claude agents` is now described as the single-screen view of running/blocked/finished sessions per v2.1.139–v2.1.142 (Week 20, May 11–15). Sources updated to include the redesign blog post and the changelog range that introduced `/code-review` (renamed from `/simplify` in v2.1.146, 2026-05-21).
- **[advanced/hooks] New handler type `mcp_tool` and richer hook input.** Per the Claude Code changelog: hooks can now invoke an MCP tool directly via `type: "mcp_tool"` (previously only `command` / `prompt` / `agent` / `http`); `PostToolUse` and `PostToolUseFailure` input includes `duration_ms`; `Stop` and `SubagentStop` input includes `background_tasks` and `session_crons`. Sources verified date refreshed.

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`) re-verified against `claude.com/product/claude-code`; Homebrew `claude-code`/`claude-code@latest`, `winget upgrade Anthropic.ClaudeCode`, npm package wraps native binary, and apt/dnf/apk all still current. Background-session / `claude agents` text unchanged.
- skills.md — `~/.claude/skills/` layout, `SKILL.md` open standard, `/skills` type-to-filter picker unchanged.
- mcp-servers.md — `claude mcp add --transport http`, scope semantics, MCP tunnels Research Preview unchanged.
- plugins.md — `claude-plugins-official` pre-registered, `--plugin-dir` zip support, `--plugin-url`, dependency-aware disable, `claude plugin prune`, `/plugin` Discover/Browse previews, Claude for Small Business Cowork example unchanged.
- marketplaces.md — source forms, seed-managed read-only behavior, pre-registration unchanged.
- connectors.md — `claude.ai/directory/connectors`, "over 200" count from Anthropic blog, May 12 legal push, Claude for Small Business pointer unchanged.
- decision-tree.md — table unchanged.
- surfaces/claude-ai.md, surfaces/claude-desktop.md, surfaces/claude-cowork.md, surfaces/claude-api.md — unchanged this run (Opus 4.7 model claim on claude-api.md confirmed by Anthropic's 2026-05-04 launch announcement; SDK install commands match current README).
- advanced/slash-commands.md, advanced/authentication.md — unchanged.

### Flagged for review
- WebFetch was again unavailable this run (404 on `claude-3-5-haiku-20241022`). All primary-source verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `code.claude.com/docs/en/routines`, `claude.com/blog/introducing-routines-in-claude-code`, `claude.com/blog/claude-code-desktop-redesign`, `anthropic.com/news`, and `platform.claude.com/docs/en/api/claude-code/routines-fire`. A human should spot-check the routines docs page directly to confirm the local-timezone-by-default behavior — one secondary source still reports the older UTC-by-default default for CLI cron tools (vs the web/UI), which suggests there may be a CLI/web split worth surfacing on the next run.
- **Claude Design** (Anthropic Labs, launched 2026-04-17 at `claude.ai/design`) and the **Stainless acquisition** (2026-05-18) are noted but not yet promoted to surface pages. Claude Design is in research preview and is more of a Labs product than a primary surface; revisit when it exits research preview. Stainless is back-end (Anthropic SDK generation) — no user-facing change to the API surface page is warranted yet.

## 2026-05-21

### Added
- **[surfaces/*, advanced/routines] Surfaces section now has one sub-page per surface, and routines is documented as a cross-cutting feature.** Restructured `guide/claude-surfaces.md` into a thin parent index (`has_children: true`) with a comparison table, and added `guide/surfaces/{claude-ai, claude-desktop, claude-code, claude-cowork, claude-api}.md` for surface-specific install and feature detail. Added `guide/advanced/routines.md` covering scheduled remote Claude Code agents (created via `/schedule`, viewed at `claude.ai/code/routines`, cron in UTC with 1-hour minimum, MCP-connector-aware, fully isolated per firing). The routines page is cross-linked from the Claude Code and Claude.ai sub-pages — first formal example of the "cross-cutting features" pattern described in GUIDE_AGENT.md.
- **[GUIDE_AGENT] "Cross-cutting features" section and ongoing-discovery directive.** Curator now maintains a single page per cross-cutting feature in `guide/advanced/` and cross-links from each relevant surface sub-page; on every run, scans Anthropic news / Claude Code changelog / named secondary commentary for newly-shipped cross-surface features (routines, background sessions, MCP tunnels, Cowork plugins, `--teleport`) that beginners would otherwise miss, and adds them. Topics table updated to include the five surface sub-pages and `advanced/routines.md`. Page schema updated with `parent: Claude surfaces` / `grand_parent: Guide` convention for surface sub-pages.

### Updated
- **[claude-surfaces] Expanded install methods and added background-session note** — `claude.com/product/claude-code` now documents `winget upgrade Anthropic.ClaudeCode`, Homebrew `claude-code@latest` for the latest channel, and `apt`/`dnf`/`apk` packages alongside the canonical `curl …/install.sh`. Removed "npm is deprecated" wording since the npm package now wraps the same native binary. Added `claude --bg` / `/resume` / `claude agents` for background sessions per the May 18–19 changelog (v2.1.144–v2.1.145). Then refactored this page into a parent index (see Added).
- **[guide/README] Surfaces now has sub-pages; advanced section now mentions routines** — added the Cowork surface to the top-line description, noted that each surface has its own sub-page with install and feature detail, and added routines to the advanced one-liner.
- **[advanced/README] Routines added to the advanced index.**
- **[plugins] `/plugin` Discover/Browse component previews and Claude for Small Business example** — noted that the Discover and Browse panes now preview a plugin's commands/agents/skills/hooks/MCP/LSP servers before install (May 2026 changelog), and added Claude for Small Business (2026-05-13) as the canonical example of a single-toggle Cowork plugin bundling connectors + workflows.
- **[connectors] Corrected directory size estimate** — replaced "past 375" with Anthropic's own most-recent count of "over 200" since July 2025 launch (per `claude.com/blog/connectors-for-everyday-life`); the 375 figure was sourced from secondary commentary only. Kept the May 12 legal push (20+ connectors, 12 practice-area plugins). Added a pitfall pointer to the Claude for Small Business Cowork bundle for users hunting SMB connectors.

### Verified (no changes)
- skills.md — `~/.claude/skills/` layout, open-standard claim, `/skills` picker unchanged this run.
- mcp-servers.md — `claude mcp add --transport http` syntax, MCP tunnels (Research Preview), and `--scope` semantics unchanged.
- marketplaces.md — source forms and seed-managed read-only behavior unchanged.
- decision-tree.md — table unchanged; Cowork row covers the SMB scenario adequately at this granularity.
- advanced/hooks.md, advanced/slash-commands.md, advanced/authentication.md — unchanged this run.

### Flagged for review
- WebFetch remained unavailable (model 404 for `claude-3-5-haiku-20241022`) — all source verification this run went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `claude.com/blog/connectors-for-everyday-life`, `anthropic.com/news/claude-for-small-business`, and `github.com/anthropics/claude-plugins-official`. A human should occasionally check the actual connector count on `claude.ai/directory/connectors`; Anthropic's blog says "over 200" but third-party trackers list far more.
- **New surface sub-pages and `advanced/routines.md` were drafted in-session without a fresh per-page source fetch.** The content draws on existing claude-surfaces.md (already source-grounded), direct observation of the Anthropic routines API in this session (the `claude.ai/code/routines/<id>` URL and create-body shape were returned live by `RemoteTrigger`), and the curator's prior research. Each new page lists candidate sources, but the next scheduled run should fetch them per `GUIDE_AGENT.md`'s per-page grounding rule and tighten any claim that doesn't survive verification. Specific items to re-verify on the next run: (1) the exact local-MCP config path on Windows for Claude Desktop, (2) current Anthropic SDK install commands and example, (3) presence and naming of an Anthropic-published "routines" or "managed agents" doc page suitable as a primary source.

## 2026-05-20

### Updated
- **[connectors] Directory size and "Claude for Legal" launch** — bumped catalog estimate from "past 200" to "past 375" prebuilt integrations and called out the May 12 legal push (DocuSign, LexisNexis, Westlaw, Everlaw, iManage, Harvey, Ironclad, …) which added 20+ connectors and 12 practice-area plugins ([LawSites 2026-05-12](https://www.lawnext.com/2026/05/anthropic-goes-all-in-on-legal-releasing-more-than-20-connectors-and-12-practice-area-plugins-for-claude.html); awesome-claude-connectors enumerates ~398 entries as of 2026-05-15).
- **[plugins] Surfaced `claude-code-setup`** — added the official onboarding plugin as a recommended first install from `claude-plugins-official` (project-scanning helper that suggests hooks, skills, MCP servers, and subagents).
- **[mcp-servers] MCP tunnels (Research Preview)** — added a pitfall pointer for exposing MCP servers inside private networks, with the new `cloudflared`-based outbound-only tunnels announced 2026-05-19 at Code with Claude London ([Anthropic blog](https://claude.com/blog/claude-managed-agents-updates), [InfoQ 2026-05-19](https://www.infoq.com/news/2026/05/claude-mcp-tunnels/)).
- **[advanced/hooks] `terminalSequence` JSON field** — noted that any hook can now emit desktop notifications, set window titles, or ring the bell without a controlling terminal (May 2026 Claude Code changelog).

### Verified (no changes)
- claude-surfaces.md — install command (`curl -fsSL https://claude.ai/install.sh | bash`), Cowork, Claude Code on the web all still current per `claude.com/product/claude-code` and surrounding May 2026 coverage.
- skills.md — `~/.claude/skills/` layout and open-standard claim unchanged this run.
- marketplaces.md — source forms and seed-managed read-only behavior unchanged this run.
- advanced/slash-commands.md, advanced/authentication.md — unchanged this run.

### Flagged for review
- WebFetch was again unavailable this run (the model name it shells out to returns 404). All primary-source verification went through WebSearch summaries of `claude.com/product/claude-code`, `code.claude.com/docs/en/changelog`, `claude.com/blog/claude-managed-agents-updates`, and `github.com/anthropics/claude-plugins-official`. A human should occasionally double-check the directory-size figure on `claude.ai/directory/connectors` directly, since the 375+ number is corroborated only by secondary commentary (Anthropic's directory page itself doesn't publish a count).

## 2026-05-19

### Updated
- **[claude-surfaces] Added Claude Cowork as a surface** — Cowork launched 2026-01-13 as the non-developer counterpart to Claude Code (sandboxed desktop agent for file/spreadsheet/slide work); expanded across paid plans by 2026-01-23 and gained department-specific plugins on 2026-02-24. Previously omitted ([source](https://www.infoq.com/news/2026/01/claude-cowork/), [Cowork plugins](https://claude.com/blog/cowork-plugins-across-enterprise)).
- **[skills] Open-standard adoption and Claude Code UX** — noted `SKILL.md` is now used by Codex CLI, Cursor, Gemini CLI, and GitHub Copilot, and `/skills` has type-to-filter search ([Claude Code changelog](https://code.claude.com/docs/en/changelog)).
- **[plugins] New install flags and dependency management** — documented `claude --plugin-dir <dir-or-zip>`, `claude --plugin-url`, dependency-aware `/plugin disable`, and `claude plugin prune` (May 2026 changelog).
- **[marketplaces] Seed-managed marketplaces and unified Directory pointer** — noted read-only seed marketplaces (containerized deployments) and the `claude.ai/directory` Plugins tab on the Claude.ai side, separate from the Claude Code marketplace mechanism.
- **[connectors] Unified Directory URL and 200+ catalog growth** — pointed canonical install path at `claude.ai/directory/connectors`; added everyday-life connectors (AllTrails, Uber, Spotify, …) per the May 2026 blog post.
- **[advanced/hooks] PostToolUse `updatedToolOutput` for all tools** — added the May 2026 generalization (previously MCP-only), the `Stop`-hook loop cap, and the `$CLAUDE_EFFORT` environment variable.
- **[decision-tree] Cowork row, current date** — added a row for non-coding desktop automation and replaced the "pending first guide run" date.

### Verified (no changes)
- mcp-servers.md — `claude mcp add --transport http` syntax and `--scope` semantics unchanged; sources re-verified.
- advanced/slash-commands.md — frontmatter and `.claude/agents/` schema unchanged this run.
- advanced/authentication.md — credential precedence and `claude setup-token` flow unchanged this run.

### Flagged for review
- WebFetch was unavailable this run (model error), so all primary-source verification went through WebSearch. Landing-page text (`claude.com/product/claude-code`) was last directly fetched on 2026-05-19 (previous run); install command is corroborated by multiple May 2026 secondary sources.

## 2026-05-19

### Updated
- **[claude-surfaces] Re-verify install commands against product landing pages** — replaced the deprecated `npm install -g @anthropic-ai/claude-code` with the canonical native installer `curl -fsSL https://claude.ai/install.sh | bash`, added the Windows PowerShell variant `irm https://claude.ai/install.ps1 | iex` and Homebrew option, and added [`claude.com/product/claude-code`](https://claude.com/product/claude-code) and [`code.claude.com/docs/en/setup`](https://code.claude.com/docs/en/setup) to the Sources section. No other guide page contained the stale npm command.

## 2026-05-19

### Added
- **[all] Sources sections to all guide pages** — every topic page (claude-surfaces, skills, mcp-servers, plugins, marketplaces, connectors, hooks, slash-commands, authentication) now lists the dated URLs that ground its claims, per the per-page grounding rule introduced in `GUIDE_AGENT.md`.

### Updated
- **[claude-surfaces] Added Claude Code on the web** — `claude.ai/code` launched 2025-10-20 on Anthropic-managed cloud VMs; previously omitted. Reframed the surfaces list and added the `--teleport` hand-off note ([source](https://www.anthropic.com/news/claude-code-on-the-web)).
- **[plugins] Corrected install flow** — `claude-plugins-official` is pre-registered when Claude Code starts; reworked the example to install from it directly instead of `anthropics/claude-code` (the demo marketplace).
- **[marketplaces] Clarified pre-registered marketplace** — noted that `claude-plugins-official` ships pre-added; updated examples to install from `anthropics/life-sciences` and the community marketplace.

## 2026-05-19 (initial)

### Added
- **[claude-surfaces] First-run content** — beginner orientation across Claude.ai, Claude Desktop, Claude Code, and the Claude API ([source](https://code.claude.com/docs/)).
- **[skills] First-run content** — install paths under `~/.claude/skills/` and `.claude/skills/`, format pointers ([source](https://code.claude.com/docs/en/skills)).
- **[mcp-servers] First-run content** — canonical `claude mcp add` examples for HTTP and stdio transports, with scopes ([source](https://code.claude.com/docs/en/mcp)).
- **[plugins] First-run content** — `/plugin marketplace add` and `/plugin install <name>@<marketplace>` flow ([source](https://code.claude.com/docs/en/plugins)).
- **[marketplaces] First-run content** — supported source forms and the Anthropic life-sciences/cross-domain marketplaces ([source](https://code.claude.com/docs/en/discover-plugins)).
- **[connectors] First-run content** — Claude.ai Settings → Connectors flow, custom remote MCP connectors, Team/Enterprise admin path ([source](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)).
- **[advanced/hooks] First-run content** — `PreToolUse`/`PostToolUse` events, `.claude/settings.json` schema, exit-code-2 guardrail ([source](https://code.claude.com/docs/en/hooks)).
- **[advanced/slash-commands] First-run content** — `.claude/commands/` vs. `.claude/agents/`, convergence with Skills ([source](https://code.claude.com/docs/en/slash-commands)).
- **[advanced/authentication] First-run content** — Anthropic credential precedence, `claude setup-token`, MCP OAuth 2.1 ([source](https://code.claude.com/docs/en/authentication)).

