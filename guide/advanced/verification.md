---
title: How catalog entries are verified
parent: Advanced
grand_parent: Guide
nav_order: 6
---

# How catalog entries are verified

Every tool in the [Catalog](../../catalog/) points at a third-party component — a Skill, MCP
server, plugin, or connector maintained by someone else. (The same machinery also checks the
[libraries recipes install](../../recipes/dependencies.md), which are not catalog entries and carry
no badge — see the end of this page.) To make the catalog trustworthy, an
automated **Verifier agent** checks each entry and stamps it with two badges you'll see in the
entry's metadata table and on the area-page cards.

## The two badges

**Verified** — does the entry still work?
- `works` — the install target resolves and the documented install path is current (and, for the
  open subset, the component actually installs/boots in a sandbox).
- `degraded` — it resolves but something is off: an install path that was just auto-corrected, a
  component that boots with errors, or a tool gated behind auth/subscription/institutional access
  that can't be functionally exercised (the note says which).
- `broken` — no working install path (removed, renamed, or 404) and not auto-fixable.

**Security** — a static supply-chain assessment (the component is **never executed** to judge it):
- `cleared` — provenance matches the stated supplier, a real license, no known advisories, actively
  maintained, no risky install patterns.
- `caution` — minor concerns (unmaintained/archived, license unstated, single maintainer).
- `flagged` — serious: provenance mismatch/typosquatting, a known CVE/advisory, or install-time
  code-execution / secret-exfiltration signals.
- `unknown` — couldn't be assessed (closed source, no resolvable repository).

Each badge carries the date it was set and a one-line rationale. Badges are **informational** — they
describe the catalog's own vetting; they don't change what the Composer installs.

## How it's checked — and the safety model

The Verifier runs as two separate GitHub Actions jobs, split deliberately for safety:

1. **A quarantined smoke-test job** installs and boots only the *safe subset* — open, no-auth,
   no-cost Skills and MCP servers chosen by a deterministic, code-reviewed selector
   (`scripts/select_smoke_targets.py`) that excludes anything requiring credentials, a subscription,
   institutional access, or that could spend money or touch a wet lab. That job holds **no secrets**
   and **cannot write the repository**; it runs in an ephemeral container as a non-root user with
   per-command timeouts, and the runner is destroyed afterward. Executing an untrusted package there
   can do nothing but burn its own throwaway VM.
2. **The agent job** does the rest **statically** — it resolves install targets against GitHub / npm
   / PyPI, checks provenance/license/advisories, reads manifests for risky patterns, and reads the
   smoke-test verdicts. It never runs component code itself. It writes the stamps, fixes broken
   catalog entries (never the external tool), and commits.

Everything is initially stamped in a bootstrap pass, then re-checked on a rolling 30-day cycle as
part of ongoing maintenance. This complements — it does not replace — the curator's `last_verified`
date, which records the last manual link/pricing review.

The 30-day cycle is enforced in code, not by convention: `scripts/select_verify_targets.py` serves
only pages whose `verified_on` is more than 30 days old, oldest first. A run with nothing due does no
work and calls no model at all. A page whose `verified_on` is missing or unreadable is always treated
as due, so a page can never fall out of the rotation by being unparseable.

## Libraries recipes install

Some recipes have Claude Code `pip install` a scientific library and write a script against it. Those
libraries aren't Claude components, so they get no catalog page and **no badge** — but the same
quarantined job still checks them: it installs the exact pinned version the recipe declares and runs
the declared import. Verdicts land on the [library index](../../recipes/dependencies.md).

Two limits worth knowing. The probe proves the package installs and imports; it is **not** a safety
claim, because `pip install` already executes the package's own build hooks. And it never exercises
first-run downloads — model weights, atlas volumes — so a recipe that needs those says so in its own
text. Only `pip` packages are checked at all: the container has no conda, R, or compiler, so a recipe
needing one of those is deferred rather than shipped on a claim nobody can test.

The import command is **synthesized** from a validated module identifier, never copied out of the
page. Pages here are written by an agent, so scraping a literal `python3 -c "…"` string would let a
page choose what runs in the container; extracting only a dotted name and rebuilding the command
keeps that decision in auditable code.
