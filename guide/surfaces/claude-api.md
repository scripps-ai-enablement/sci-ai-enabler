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

The API also hosts **Managed Agents** — long-running agentic sessions Anthropic runs and bills on your behalf — and supports MCP for tool use, so the same MCP servers you wire into Claude Code or Claude Desktop can be called from your application.

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

## See also

- [Authentication](../advanced/authentication.html) — credential precedence and key handling.
- [MCP servers](../mcp-servers.html) — tools you can attach to API calls.
- [`code.claude.com/docs/en/agent-sdk`](https://code.claude.com/docs/en/agent-sdk) — Agent SDK reference.

## Sources

- [Anthropic Console](https://console.anthropic.com) — verified 2026-05-21 (this run).
- [Anthropic API documentation](https://docs.claude.com/) — Anthropic docs; verified 2026-05-21.
- [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk) — Anthropic docs; verified 2026-05-21.
- [Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) — Anthropic docs; verified 2026-05-21.
