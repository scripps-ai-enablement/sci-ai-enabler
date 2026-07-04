---
title: Skills
parent: Guide
nav_order: 2
---

# Skills

> A focused capability a Claude agent can adopt for one kind of task.

## What it is

A Skill is a folder containing a `SKILL.md` file (markdown with YAML frontmatter) plus optional scripts and reference files. The frontmatter tells Claude when to activate the skill; the body tells it what to do. Skills are filesystem-based in Claude Code, Claude Desktop, and Cowork, and uploaded as a `.zip` on Claude.ai. The `SKILL.md` format is now an open standard adopted by Codex CLI, Cursor, Gemini CLI, and GitHub Copilot — same file, multiple agents.

Skills add focused know-how, not new APIs. If you need network access, pair a skill with an MCP server.

## When to use it

- You have a repeatable workflow (e.g., "write a clinical trial protocol") with specific conventions.
- You want Claude to auto-apply a procedure when the user's request matches a description.
- You want to ship a `/skill-name` invocation alongside autonomous activation.
- You need to bundle small helper scripts with the prompt.

## How to install / enable

Put the skill folder under `~/.claude/skills/` (personal, all projects) or `.claude/skills/` (project, committed to the repo). Only `SKILL.md` is required.

```bash
mkdir -p ~/.claude/skills/my-skill
# place SKILL.md inside ~/.claude/skills/my-skill/
```

To browse and install skills shipped via a plugin marketplace, type `/plugin` inside Claude Code. List active skills with `/skills` — the picker has a type-to-filter search box for long lists. A plugin with a root-level `SKILL.md` (no `skills/` subdirectory) is now surfaced as a skill automatically. Invoke several skills at once by stacking them in one message — `/skill-a /skill-b /skill-c` loads all of them (up to 5), not just the first (v2.1.199, June 2026). `/usage` breaks down current usage by skill, subagent, plugin, and MCP server. After editing a `SKILL.md`, run `/reload-skills` to re-scan directories without restarting the session (v2.1.152, May 2026).

Anthropic bundles a growing set of built-in skills. The newest, `/dataviz` (v2.1.198, 2026-07-01), designs charts and dashboards and runs a color-palette validator; no install needed.

Skills can narrow Claude's tool access while active. Add a `disallowed-tools:` list to the YAML frontmatter (v2.1.152+) to remove specific tools — useful for read-only or audit skills that should not touch `Edit` / `Write`.

## Common pitfalls

- Nesting one level too deep. The path must be `~/.claude/skills/<name>/SKILL.md`, not `~/.claude/skills/<name>/<subdir>/SKILL.md`.
- Missing or invalid YAML frontmatter — Claude won't auto-trigger the skill.
- Treating Skills as a substitute for MCP. Skills carry instructions; MCP carries tool calls.
- Installing skills from untrusted sources without reading `SKILL.md` first.

## See also

- [Plugins](plugins.md) — the easiest way to distribute multiple skills together
- [MCP servers](mcp-servers.md) — for skills that need live data or external APIs
- [Slash commands & subagents](advanced/slash-commands.md)
- [Skills reference](https://code.claude.com/docs/en/skills) — canonical docs
- [`anthropics/skills`](https://github.com/anthropics/skills) — canonical examples

## Sources

- [Extend Claude with skills](https://code.claude.com/docs/en/skills) — Anthropic docs; verified 2026-05-19 (this run).
- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — Anthropic API docs; verified 2026-05-19.
- [Introducing Agent Skills](https://www.anthropic.com/news/skills) — published 2025-10-16.
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — Anthropic engineering blog; published 2025-10-16.
- [Claude Code changelog (May–July 2026)](https://code.claude.com/docs/en/changelog) — type-to-filter `/skills`, nested SKILL.md surfacing, root-level SKILL.md surfaced as skill, `/usage` per-category breakdown, `/reload-skills` + `disallowed-tools` frontmatter (v2.1.152, 2026-05-27); stacked slash-skill invocations load up to 5 skills (v2.1.199, 2026-07-02); built-in `/dataviz` skill (v2.1.198, 2026-07-01); verified 2026-07-04 (this run).
- [`anthropics/skills`](https://github.com/anthropics/skills) — canonical examples repo; verified 2026-05-19.
