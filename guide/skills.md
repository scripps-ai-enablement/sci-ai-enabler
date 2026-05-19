# Skills

> A focused capability a Claude agent can adopt for one kind of task.

_Last updated: 2026-05-19_

## What it is

A Skill is a folder containing a `SKILL.md` file (markdown with YAML frontmatter) plus optional scripts and reference files. The frontmatter tells Claude when to activate the skill; the body tells it what to do. Skills are filesystem-based in Claude Code and Claude Desktop, and uploaded as a `.zip` on Claude.ai. The same `SKILL.md` format works everywhere.

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

To browse and install skills shipped via a plugin marketplace, type `/plugin` inside Claude Code. List active skills with `/skills`.

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
