---
title: Claude API
parent: Claude surfaces
grand_parent: Guide
nav_order: 5
---

# Claude API

> The developer endpoint — call Anthropic models from your own code via REST or an Anthropic SDK.

## What it is

The Claude API is what you build with when you're shipping your own product, agent, or backend integration. Authentication is via an API key from the Anthropic Console. SDKs exist for Python and TypeScript; the underlying interface is plain REST.

The API also hosts **Claude Managed Agents** — long-running agentic sessions Anthropic runs and bills on your behalf, on a separate endpoint family under `/v1/agents`, `/v1/environments`, and `/v1/sessions` (beta header `managed-agents-2026-04-01`). At Code with Claude on 2026-05-06 Anthropic moved three advanced capabilities into public beta: **Outcomes** (a self-grading loop — you define a rubric, a separate grader agent evaluates each iteration, the agent revises until the rubric passes) and **Multi-agent Orchestration** (a lead agent fans tasks to specialist sub-agents in parallel), plus **Dreams** in research preview (an async job that consolidates a memory store from past session transcripts; beta header `dreaming-2026-04-21`). The API also supports MCP for tool use, so the same MCP servers you wire into Claude Code or Claude Desktop can be called from your application.

## When to use it

- Building a product, internal tool, or backend service that calls Claude.
- Running batch or background inference jobs at scale.
- Programmatic agent loops (the SDK ships an Agent SDK for this).
- Connecting MCP servers to your own code rather than to Claude.ai or Claude Code.

## How to install / enable

- Create an API key at `https://console.anthropic.com` (Settings → API keys).
- Install an SDK.

  ```bash
  pip install anthropic
  # or
  npm install @anthropic-ai/sdk
  ```

- Set the key as an environment variable.

  ```bash
  export ANTHROPIC_API_KEY=sk-ant-...
  ```

- Make a request — see the SDK README for the current minimal example.
- For MCP from your code: the SDK exposes `tools` and supports MCP servers as a tool source. See [MCP servers](../mcp-servers.html).

## Common pitfalls

- API usage is metered and billed separately from a Pro/Max subscription — even if you're a Pro user, API calls draw from your API credit balance.
- **Agent SDK and `claude -p` (headless Claude Code) move to a separate "Agent SDK credit" on 2026-06-15.** Per Anthropic's 2026-05-14 announcement, programmatic usage exits the subscription rate-limit pool and onto a dollar-denominated credit billed at standard API rates (Pro $20, Max 5x $100, Max 20x $200, Team $100/seat, Enterprise $200/seat). One-time opt-in required; credits refresh monthly with the billing cycle and do **not** roll over. Interactive Claude Code in the terminal, Claude.ai chat, and Cowork continue drawing from normal subscription limits. Third-party agent harnesses that authenticate via subscription (Zed, Conductor, …) are affected too.
- Default model IDs change. The current line is **Claude Fable 5** (`claude-fable-5`, shipped 2026-06-09) — a "Mythos-class" tier above Opus, Anthropic's most capable generally-available model — plus Opus 4.8 (`claude-opus-4-8`, the `opus` alias on the Anthropic API), Sonnet 4.6, and Haiku 4.5. Model IDs are dateless pinned snapshots from the 4.6 generation on. On Bedrock / Vertex / Foundry the aliases lag — pin the full model ID or set `ANTHROPIC_DEFAULT_OPUS_MODEL` to override.
- **Fable 5 behaves differently from Opus.** Adaptive thinking is the only thinking mode (`thinking: {type: "disabled"}` is unsupported); steer depth with `effort`. The raw chain of thought is never returned (`thinking.display` defaults to `"omitted"`; set `"summarized"` for readable summaries). It costs $10 / $50 per million input / output tokens (≈ double Opus 4.8) and supports 1M context with up to 128k output. `claude-mythos-5` is a separate, invitation-only Project Glasswing model — not for general use.
- **Plan for Fable 5 refusals.** It ships with blocking classifiers for dual-use cybersecurity and biology content; a blocked request returns HTTP 200 with `stop_reason: "refusal"` and a `stop_details` category, not an error. Refusal rates are materially higher than on prior models — handle `refusal` as a primary response path. Prompt-stage refusals aren't billed; mid-stream ones are billed for tokens generated before the block.
- **`claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire 2026-06-15 at 9am PT.** API calls to those exact IDs error after that date. Migrate to `claude-sonnet-4-6` and `claude-opus-4-7` (or `-4-8`); `budget_tokens` for extended thinking is deprecated — use `thinking: {type: "adaptive"}` instead.
- **Opus 4.7 and 4.8 reject `temperature`, `top_p`, and `top_k`.** Sending any of these — even at a "default" value — returns a 400; rejection is by presence, not value, and the SDK won't catch it at compile time. Omit them entirely and steer behavior with prompting plus the `effort` parameter. Watch for OpenAI-compat layers, gateways, or frameworks that inject `temperature` for you.
- Prompt caching is opt-in but cheap to enable; turn it on when you reuse the same system prompt or tool schema across many calls. On Opus 4.8 only, you can append a `role: "system"` entry inside the `messages` array (immediately after a user turn) to update instructions mid-conversation without restating the top-level system prompt or invalidating the cached prefix — useful for long agentic loops. See [mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages). Earlier models 400 on `role: "system"` in `messages`. Available on the Claude API and Claude Platform on AWS; not yet on Bedrock, Vertex, or Foundry.
- Don't put API keys in client-side code — keys are bearer tokens.
- Managed Agents lives on its own endpoints; calling `/v1/messages` won't give you Outcomes, Dreams, or multi-agent orchestration. Use the SDK's `client.beta.agents` namespace (which sets beta headers automatically).

## See also

- [Authentication](../advanced/authentication.html) — credential precedence and key handling.
- [MCP servers](../mcp-servers.html) — tools you can attach to API calls.
- [`code.claude.com/docs/en/agent-sdk`](https://code.claude.com/docs/en/agent-sdk) — Agent SDK reference.
- [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/) — canonical docs for the agentic endpoints.

## Sources

- [Anthropic Console](https://console.anthropic.com) — verified 2026-05-23 (this run).
- [Anthropic API documentation](https://docs.claude.com/) — Anthropic docs; verified 2026-05-23.
- [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk) — Anthropic docs; verified 2026-05-23.
- [Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) — Anthropic docs; verified 2026-05-23.
- [Define outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes) — Anthropic API docs; verified 2026-05-23 — Outcomes self-grading loop, rubric and grader semantics, `managed-agents-2026-04-01` beta header.
- [Dreams](https://platform.claude.com/docs/en/managed-agents/dreams) — Anthropic API docs; verified 2026-05-23 — async memory-consolidation job, research preview, `dreaming-2026-04-21` beta header.
- [New in Claude Managed Agents: dreaming, outcomes, and multi-agent orchestration](https://claude.com/blog/new-in-claude-managed-agents) — Anthropic blog; published 2026-05-06 — Code with Claude 2026 launch announcement.
- [Live blog: Code w/ Claude 2026](https://simonwillison.net/2026/May/6/code-w-claude-2026/) — Simon Willison; published 2026-05-06 — independent coverage of the keynote announcements.
- [Introducing Claude Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) — Anthropic news; published 2026-05-28 — Opus 4.8 ship date, 1M context default, no premium pricing, available on Claude API / Bedrock / Vertex / Foundry.
- [What's new in Claude Opus 4.8](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-8) — Anthropic API docs; verified 2026-06-09 (this run) — `opus` alias resolution per surface, `claude-opus-4-8` model ID, `ANTHROPIC_DEFAULT_OPUS_MODEL` env var; `temperature` / `top_p` / `top_k` rejected with 400 (by presence, inherited from Opus 4.7); adaptive thinking replaces `budget_tokens`.
- [Mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages) — Anthropic API docs; verified 2026-05-29 — Opus 4.8 accepts `role: "system"` in `messages` after a user turn; placement constraints and prompt-cache benefit.
- [Anthropic puts Claude agents on a meter across its subscriptions](https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html) — InfoWorld; published 2026-05-14 — Agent SDK + `claude -p` move to separate dollar-denominated credit pool on 2026-06-15; per-plan credit amounts; one-time opt-in; verified 2026-06-02 (this run).
- [Anthropic splits billing again: Agent SDK gets separate credit pools](https://thenewstack.io/anthropic-agent-sdk-credits/) — The New Stack; published 2026-05-15 — independent coverage of the 2026-06-15 billing split; no rollover; verified 2026-06-02.
- [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — Anthropic API docs; verified 2026-06-02 (this run) — `claude-sonnet-4-20250514` and `claude-opus-4-20250514` retire 2026-06-15 at 9am PT; recommended replacements `claude-sonnet-4-6` / `claude-opus-4-7`; adaptive thinking replaces `budget_tokens`.
- [Claude Fable 5 and Claude Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) — Anthropic news; published 2026-06-09 — Mythos-class tier; Fable 5 = public model with Opus-4.8 safety fallback, Mythos 5 = Project Glasswing only; $10/$50 per Mtok; subscription-free through 2026-06-22 then usage-credit-gated; GA on Claude API / AWS / Bedrock / Vertex / Foundry.
- [Introducing Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) — Anthropic API docs; verified 2026-06-10 (this run) — `claude-fable-5` / `claude-mythos-5` IDs (dateless pinned snapshots), adaptive-thinking-only with `effort` control, `thinking.display` omitted-by-default, 1M context / 128k output, HTTP-200 `stop_reason: "refusal"` + `stop_details`, refusal billing rules.
