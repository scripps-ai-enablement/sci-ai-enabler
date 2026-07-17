---
description: Generate novel, falsification-tested hypotheses by bridging cross-corpus knowledge fragments
argument-hint: <research goal, e.g. "repurposable approved drugs for Alzheimer's disease">
---

A scientist wants novel, defensible hypotheses for a research goal:

> $ARGUMENTS

Use the **forge** skill (`skills/forge/SKILL.md` in this plugin) to handle this end to end: frame
the goal to ontology anchors, mine typed knowledge fragments across literature / structured
databases / raw experimental data, assemble Swanson-style bridges into candidate connections, run
every candidate through the **falsification gauntlet** (novelty, groundedness, contradiction,
plausibility — any gate can veto), rank the survivors in an adversarial tournament, and emit a
reproducible run bundle. Follow the skill's pipeline and its hard rules (no fragment → no claim;
aggressive-veto semantics; provenance binding on every claim; a discriminating experimental test
for every surviving hypothesis) exactly.

If `$ARGUMENTS` is empty, ask the scientist for their research goal (a disease, a target space, or
an observation to explain) before proceeding.
