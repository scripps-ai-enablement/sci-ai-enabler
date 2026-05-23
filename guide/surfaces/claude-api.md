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
- Default model IDs change. The current Claude 4 family includes Opus 4.7, Sonnet 4.6, and Haiku 4.5; check the SDK README before pinning a model in production.
- Prompt caching is opt-in but cheap to enable; turn it on when you reuse the same system prompt or tool schema across many calls.
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
