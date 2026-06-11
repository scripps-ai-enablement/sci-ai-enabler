---
description: Compose a grounded, runnable Claude solution for a scientific problem
argument-hint: <describe the problem you're trying to solve>
---

A scientist wants help solving a problem with Claude. Their problem:

> $ARGUMENTS

Use the **compose** skill (`skills/compose/SKILL.md` in this plugin) to handle this end to end:
classify the problem, reuse a curated recipe if one fits, otherwise compose the simplest grounded
assembly from the catalog, recommend a pre-built autonomous system when that is the right rung, then
offer to actually set the solution up and run it. Follow the skill's pipeline and its hard rules
(simplicity ladder, grounding, evidence/availability/compute caveats, and the capture step) exactly.

If `$ARGUMENTS` is empty, ask the scientist what they're trying to do before proceeding.
