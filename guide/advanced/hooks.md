# Hooks

> Shell commands Claude Code runs automatically in response to events — e.g., before/after a tool call or on session end.

_Last updated: 2026-05-19_

## What it is

A hook is a deterministic handler that fires on a named Claude Code lifecycle event. Events include `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `Notification`, and `SessionStart`. Handlers can be `command` (shell), `prompt`, `agent`, or `http`. A `PreToolUse` hook that exits 2 blocks the pending tool call — this is the main guardrail mechanism.

Hooks run outside the model. They see structured JSON on stdin and respond via exit codes or stdout JSON.

## When to use it

- Enforce a policy (block `rm -rf`, refuse edits to protected paths).
- Auto-format or lint files after `Write`/`Edit`/`MultiEdit`.
- Log tool calls for audit.
- Redact secrets from tool output before Claude sees it.
- Route notifications to Slack or a desktop alert.

## How to install / enable

The interactive path is easiest:

```bash
# inside a Claude Code session
/hooks
```

Or edit `.claude/settings.json` (project, committed) or `~/.claude/settings.json` (personal) directly:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{
        "type": "command",
        "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
      }]
    }]
  }
}
```

Reload by restarting the session or running `/hooks` again.

## Common pitfalls

- Putting secrets in `.claude/settings.json` — it's designed to be committed.
- Omitting the `matcher` regex, which causes the hook to fire for every tool call.
- Relying on `PostToolUse` to undo an action — it can't. Use `PreToolUse` to block.
- Letting a hook hang. Long-running commands stall the session; background or short-circuit them.
- Echoing tool input back unchanged from a `command` hook and assuming it bypasses permissions; use the `permissionDecision` JSON shape instead.

## See also

- [Plugins](../plugins.md) — distribute hooks alongside skills and MCP
- [Authentication](authentication.md)
- [Hooks reference](https://code.claude.com/docs/en/hooks) — canonical docs

## Sources

- [Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide) — Anthropic docs; verified 2026-05-19 (this run).
- [Hooks reference](https://code.claude.com/docs/en/hooks) — Anthropic docs; verified 2026-05-19.
