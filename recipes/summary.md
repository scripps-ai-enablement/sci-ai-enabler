---
title: Landscape
parent: Recipes
nav_order: 1
permalink: /recipes/summary.html
---

# Recipe landscape

This cookbook pairs concrete life-science problems with recommended assemblies of the components catalogued elsewhere on this site. Each recipe is the answer to "I have this problem — what's the simplest viable assembly that has evidence behind it?" The recipes are deliberately biased toward the lowest rung of the [simplicity ladder](./#the-simplicity-ladder) that actually solves the problem.

## Coverage by problem class

{% assign recipes = site.pages | where_exp: "p", "p.problem_class" | sort: "title" %}
{% assign classes = "Literature triage,Hypothesis generation,Experimental design,Data analysis,Knowledge synthesis,Manuscript prep,Workflow automation" | split: "," %}
{% for class in classes %}
### {{ class }}

{% assign matched = recipes | where: "problem_class", class %}
{% if matched.size == 0 %}
_No recipes yet._
{% else %}
{% for recipe in matched %}
- [{{ recipe.title }}]({{ recipe.url | relative_url }}) — *{{ recipe.complexity }} · {{ recipe.evidence_level }} · {{ recipe.availability }} · {{ recipe.compute_requirements }}*. {{ recipe.summary }}
{% endfor %}
{% endif %}
{% endfor %}

## How evidence is distributed

The cookbook mixes three evidence levels:

- **Validated** — at least one peer-reviewed paper or independent benchmark reports the assembly working.
- **Reported** — a preprint, blog post, or case study documents someone running the assembly.
- **Proposed** — rational composition from the catalog; no documented attempt is yet known.

Use the front-matter on each recipe to filter by the bar you need.

## Gaps

Problem classes with no recipes yet are listed above as `_No recipes yet._`. Subject areas that are under-covered are noted in the curator's internal state file as `Deferred` candidates and surfaced here when they cluster into a pattern.
