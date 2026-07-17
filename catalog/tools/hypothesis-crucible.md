---
title: Hypothesis Crucible (Claude Plugin)
parent: All tools
grand_parent: Catalog
tool_type: Claude Plugin
supplier: Scripps AI Enablement
availability: GA
tool_categories: [Drug Repurposing and Discovery, Neuroscience, All]
last_verified: 2026-07-17
summary: Agentic cross-corpus hypothesis generation — mines typed knowledge fragments from literature, structured databases, and raw experimental data, bridges them Swanson-style into novel connections, then runs a falsification gauntlet that aggressively rejects non-novel, ungrounded, contradicted, or implausible ideas, emitting only survivors with cited support and a discriminating experimental test.
---

# Hypothesis Crucible (Claude Plugin)

A Claude Code plugin in this repo's marketplace that generates novel, falsification-tested hypotheses: it mines atomic knowledge fragments from different bodies of literature and experimental data, assembles them into candidate connections no single source states, aggressively kills the weak ones through a gauntlet of independent veto gates, and surfaces only the survivors — each with a fragment-cited mechanism, a proof-of-novelty search, and an experiment that could falsify it.

| | |
|---|---|
| **Type** | Claude Plugin (bundles the `forge` skill + `/crucible:forge` command) |
| **Supplier** | Scripps AI Enablement (this repository) |
| **Availability** | GA — shipped in the `sci-ai-enabler` marketplace |
| **Pricing** | Free / OSS |
| **Capabilities** | Read/Write — drives bio-research MCP servers; writes a reproducible run bundle to disk |

## How to install

- **Claude Code** — add this repo as a plugin marketplace, then install:
  ```
  /plugin marketplace add scripps-ai-enablement/sci-ai-enabler
  /plugin install crucible
  ```
- **Prerequisite MCP servers** — connect the `bio-research` servers the skill drives (`pubmed`,
  `ot`, `chembl`, `c-trials`, `biorxiv`, `consensus`, `biomcp`, `tooluniverse`) via `/mcp` or
  `claude mcp add …`. GEO (raw-data adapter) is reached via the `gget` skill / `tooluniverse`. The
  plugin runs without them but every fragment must be grounded in a real tool call, so an
  unconnected server means that source is skipped rather than fabricated.

## What it does

Given a research goal (e.g. "repurposable approved drugs for Alzheimer's disease"), the `forge` skill runs a six-stage pipeline: frame the goal to ontology anchors; mine typed, provenance-carrying fragments across literature, structured databases (Open Targets, ChEMBL, ClinicalTrials.gov), and a pluggable tier of raw experimental sources (GEO is the reference adapter); discover Swanson-style A–C bridges with no direct edge but multiple independent cross-corpus B-paths; run every candidate through a falsification gauntlet (G1 novelty by active negative search, G2 groundedness, G3 contradiction/red-team, G4 plausibility) where any gate can veto and every kill is logged; rank survivors in an Elo debate tournament; and emit a run bundle (`hypotheses.json`, `kill-log.jsonl`, `fragments.jsonl`, `provenance.json`, `run.bco.json`).

**Primary use cases**: drug-repurposing candidate generation; explaining an observation via cross-domain mechanism; filtering a large pool of raw hypotheses down to a defensible few before committing experimental resources. It optimizes precision over recall — it is designed to surface few, well-supported ideas and to reject aggressively.

## Notes

Distributed as a plugin (`crucible/`) in this repository. The reasoning is model-driven (a `SKILL.md` procedure), so runs are auditable via the emitted IEEE-2791 BioCompute Object rather than byte-reproducible; deterministic scoring of a captured run lives in `recipes/examples/hypothesis-crucible/eval/score.py`. Positioned as a high-precision candidate filter upstream of experimental validation, complementary to end-to-end systems like Robin, Co-Scientist, and OpenScientist.

## Sources

- [Crucible plugin skill](https://github.com/scripps-ai-enablement/sci-ai-enabler/blob/main/crucible/skills/forge/SKILL.md)
- [Worked example + evaluation harness](https://github.com/scripps-ai-enablement/sci-ai-enabler/tree/main/recipes/examples/hypothesis-crucible)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=hypothesis-crucible&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fhypothesis-crucible.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
