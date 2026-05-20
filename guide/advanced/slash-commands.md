---
title: Slash commands and subagents
parent: Advanced
grand_parent: Guide
nav_order: 2
---

# Slash commands and subagents

> User-defined `/commands` and specialized subagent definitions you can ship with your project or install globally.

## What it is

A **slash command** is a reusable prompt invoked with `/name`. Drop a markdown file in `.claude/commands/<name>.md` (project) or `~/.claude/commands/<name>.md` (personal); Claude Code wires it up automatically. Slash commands have largely converged with [Skills](../skills.md) — both create `/name` shortcuts, but a skill folder under `.claude/skills/` also supports autonomous activation.

A **subagent** is a separately-scoped Claude instance with its own context window, tools, and system prompt. Define one in `.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md` (personal). Claude's orchestrator can spawn defined subagents via the Task tool; up to 10 can run in parallel.

## When to use it

- Slash command: you want a manual, repeatable entry point for a workflow.
- Subagent: you want Claude to delegate a sub-problem (code review, debugging) into a fresh context.
- Both: complex pipelines where a `/review` command spawns a `security-reviewer` subagent.
- Skill instead: if you want autonomous activation alongside `/name` invocation.

## How to install / enable

Create the file and start a new session.

```bash
mkdir -p .claude/commands
cat > .claude/commands/security-scan.md <<'EOF'
---
allowed-tools: Read, Grep, Glob
description: Run a security review of the codebase
---
Look for SQL injection, XSS, exposed credentials, and insecure configs.
Report findings with severity and remediation.
EOF
```

For a subagent, write `.claude/agents/<name>.md` with `name`, `description`, `tools`, and (optionally) `model` and `permissionMode` in the frontmatter, then a system prompt body.

## Common pitfalls

- Forgetting YAML frontmatter — slash commands work without it; subagents need at least `name` and `description`.
- Granting too many `allowed-tools`. Scope tightly.
- Expecting subagents to share context with the parent — they don't.
- Putting team-shared commands in `~/.claude/` instead of `.claude/` (they won't be committed).

## See also

- [Skills](../skills.md) — the newer format that supersedes `commands/` for most cases
- [Plugins](../plugins.md) — distribute commands and agents together
- [Slash commands reference](https://code.claude.com/docs/en/slash-commands) — canonical docs
- [Subagents reference](https://code.claude.com/docs/en/subagents) — canonical docs

## Sources

- [Slash Commands in the SDK](https://code.claude.com/docs/en/agent-sdk/slash-commands) — Anthropic docs; verified 2026-05-19 (this run).
- [Slash Commands (platform docs)](https://platform.claude.com/docs/en/agent-sdk/slash-commands) — Anthropic docs; verified 2026-05-19.
- [Claude Code customization guide](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/) — Alex Op; verified 2026-05-19.
