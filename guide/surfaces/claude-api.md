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
- **The planned Agent SDK / `claude -p` billing split was paused.** Anthropic had announced (2026-05-14) that programmatic usage — Agent SDK, `claude -p`, Claude Code GitHub Actions, third-party harnesses — would move off subscription limits onto a separate dollar-denominated credit pool on 2026-06-15. On that date Anthropic shelved the change; the Help Center now opens with a pause notice. For now, Agent SDK and `claude -p` usage still draws from your normal subscription limits. Anthropic says it will give notice before any future change, so treat the separate-credit design as possible-but-not-live.
- Default model IDs change. The current generally-available line is **Opus 4.8** (`claude-opus-4-8`, the `opus` alias on the Anthropic API), Sonnet 4.6, and Haiku 4.5. Model IDs are dateless pinned snapshots from the 4.6 generation on. On Bedrock / Vertex / Foundry the aliases lag — pin the full model ID or set `ANTHROPIC_DEFAULT_OPUS_MODEL` to override.
- **Fable 5 (`claude-fable-5`) and Mythos 5 are currently unavailable.** Anthropic shipped Fable 5 on 2026-06-09, but on 2026-06-12 a U.S. government export-control directive forced it to disable both models for *all* customers worldwide. Calls to `claude-fable-5` fail until access is restored; Anthropic is contesting the order and gives no timeline. All other models (incl. Opus 4.8) are unaffected — don't pin `claude-fable-5` in production until it returns. (For reference, when live it was adaptive-thinking-only, never returned raw chain of thought, cost $10 / $50 per million input / output tokens, supported 1M context / 128k output, and refused dual-use cybersecurity and biology prompts via HTTP-200 `stop_reason: "refusal"`.)
- **`claude-sonnet-4-20250514` and `claude-opus-4-20250514` retired 2026-06-15 at 9am PT.** API calls to those exact IDs (and the `claude-opus-4-0` / `claude-sonnet-4-0` aliases that resolved to them) now error. Migrate to `claude-sonnet-4-6` and `claude-opus-4-8`; the Opus path also drops `temperature` / `top_p` / `top_k` and `budget_tokens` (all now 400) — use `thinking: {type: "adaptive"}` instead. Consumer Claude.ai and Claude Code managed environments pick models automatically and were unaffected.
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
- [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) — Anthropic help center; verified 2026-06-20 (this run) — opening notice confirms the planned Agent SDK / `claude -p` billing split is **paused** as of 2026-06-15; usage still draws from subscription limits; planned (not-live) per-plan credit amounts listed.
- [Anthropic puts Claude agents on a meter across its subscriptions](https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html) — InfoWorld; published 2026-05-14 — original announcement of the (now-paused) 2026-06-15 Agent SDK billing split and per-plan credit amounts.
- [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — Anthropic API docs; verified 2026-06-20 (this run) — `claude-sonnet-4-20250514` and `claude-opus-4-20250514` retired 2026-06-15 at 9am PT (along with the `-4-0` aliases); recommended replacements `claude-sonnet-4-6` / `claude-opus-4-8`; adaptive thinking replaces `budget_tokens`.
- [Claude Fable 5 and Claude Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) — Anthropic news; published 2026-06-09 — Fable 5 = public model, Mythos 5 = Project Glasswing only; $10/$50 per Mtok; adaptive-thinking-only; 1M context / 128k output; HTTP-200 `stop_reason: "refusal"`.
- [Statement on the US government directive to suspend access to Fable 5 and Mythos 5](https://www.anthropic.com/news/fable-mythos-access) — Anthropic news; published 2026-06-12; verified 2026-06-20 (this run) — export-control directive received 5:21pm ET 2026-06-12; both models disabled for all customers worldwide; all other models (incl. Opus 4.8) unaffected; no restoration timeline.
