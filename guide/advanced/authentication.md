---
title: Authentication
parent: Advanced
grand_parent: Guide
nav_order: 3
---

# Authentication

> Where Claude Code looks for API keys, how OAuth flows for MCP servers work, and where each kind of secret actually lives.

## What it is

Claude Code authenticates to Anthropic itself, and separately to each remote MCP server you connect to. The two are independent.

**To Anthropic.** Credentials are checked in priority order: cloud provider env (Bedrock/Vertex/Foundry) → `ANTHROPIC_AUTH_TOKEN` → `ANTHROPIC_API_KEY` → `apiKeyHelper` script → OAuth token → `/login` subscription. Whichever is found first wins. Run `/status` to confirm which one's active.

**To remote MCP servers.** Per the MCP spec, remote servers use OAuth 2.1 with PKCE — not static API keys. Claude Code opens a browser, completes the flow, and stores tokens. Some servers also accept a bearer token via `--header`.

## When to use it

- `/login` subscription — default for Pro/Max/Team/Enterprise users.
- `ANTHROPIC_API_KEY` — direct API billing, scripted use, or CI where you don't want the subscription path.
- `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token`) — CI that needs subscription credentials.
- `apiKeyHelper` — short-lived tokens fetched from a vault.

## How to install / enable

```bash
# Interactive subscription login
claude /login

# Direct API key (precedence: takes over once approved)
export ANTHROPIC_API_KEY=sk-ant-...

# One-year OAuth token for CI (subscription-backed)
claude setup-token   # copy the printed token to your CI secret store
```

For remote MCP, the OAuth flow triggers automatically the first time Claude calls a tool that needs it. Force it with `claude mcp auth <server>`.

## Common pitfalls

- An `ANTHROPIC_API_KEY` in your shell silently overrides your subscription. `unset` it to fall back.
- Putting secrets in `.claude/settings.json`. Use `.claude/settings.local.json` (gitignored) or the OS keychain / CI secret store.
- Committing `.mcp.json` with embedded tokens — keep secrets out of it.
- Using `CLAUDE_CODE_OAUTH_TOKEN` with `--bare` (it isn't read in bare mode).
- Expecting static API keys to work against remote MCP servers — they don't. Use OAuth or a bearer header.

## See also

- [MCP servers](../mcp-servers.md)
- [Authentication reference](https://code.claude.com/docs/en/authentication) — canonical docs
- [API authentication reference](https://platform.claude.com/docs/en/manage-claude/authentication) — canonical docs

## Sources

- [Claude Code authentication](https://code.claude.com/docs/en/authentication) — Anthropic docs; verified 2026-05-19 (this run).
- [API authentication](https://platform.claude.com/docs/en/manage-claude/authentication) — Anthropic API docs; verified 2026-05-19.
- [`anthropics/claude-code-action` setup](https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md) — verified 2026-05-19.
