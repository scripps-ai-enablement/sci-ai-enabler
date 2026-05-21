---
title: Recipes
nav_order: 4
has_children: true
permalink: /recipes/
---

# Recipes

Concrete pairings of a life-science problem with a recommended assembly of the Claude components catalogued in this repo. Each recipe names the tools, links the install pages, states the evidence, and flags the availability and compute requirements so you can decide in 30 seconds whether it fits your situation.

The recipes deliberately favor the simplest viable approach. Most well-scoped problems are solved at rung 1 or 2 of the ladder below — full autonomous-science systems are only recommended when a documented workflow actually used one.

## Where to start

- **[Landscape](summary.html)** — what's covered, where the gaps are, how evidence is distributed across recipes.
- **[All recipes](items/)** — every recipe, one page each.

## How recipes are scoped

Each recipe sits in one **problem class**:

| Class | Examples |
|---|---|
| Literature triage | Surveying a stack of new preprints, ranking by relevance |
| Hypothesis generation | Proposing testable mechanisms, candidate targets |
| Experimental design | Selecting controls, conditions, primers, sgRNAs |
| Data analysis | Running a pipeline (RNA-seq, single-cell, variant calling) |
| Knowledge synthesis | Cross-database target dossiers, ADMET profiles, repurposing scans |
| Manuscript prep | Figure assembly, statistics review, reference checking |
| Workflow automation | Wiring tools together for repeated runs |

…and one or more of the seven life-science **subject areas** used elsewhere in this site (Chemistry, Immunology and Microbiology, Integrative Structural and Computational Biology, Molecular and Cellular Biology, Neuroscience, Translational Medicine, Drug Repurposing and Discovery), or `All` for cross-cutting recipes.

## The simplicity ladder

Recipes recommend the cheapest rung that solves the problem:

1. **Claude Code alone** — no Skill, no MCP, no Plugin.
2. **Claude Code + one Skill or MCP server.**
3. **Claude Code + a small toolbelt** (≤ 3 components).
4. **A documented [autonomous-science system](../autonomous-science/)** (Biomni, Robin, Co-Scientist, OpenScientist, ChemCrow, …).

When a recipe escalates to a higher rung, the **Alternatives considered** section explains why a lower rung isn't enough.

## Evidence labels

Each recipe carries one of:

- **Validated** — peer-reviewed paper or independent benchmark reports the assembly solving the problem, with quantitative results.
- **Reported** — preprint, blog post, vendor case study, or conference proceedings documents someone running it.
- **Proposed** — rational composition from the catalog; no documented attempt is known. Each component has independent evidence, the assembly does not.

`Proposed` recipes name the closest documented analogue under **Evidence**.

## What this isn't

- Not an install tutorial — each step links to the underlying [catalog](../catalog/) page that owns the install instructions.
- Not a vendor comparison — see the [guide](../guide/) for "which component type should I use".
- Not Scripps-specific. Recipes are written for any academic researcher; the `availability` and `compute_requirements` metadata is what a Scripps reader uses to self-filter.
