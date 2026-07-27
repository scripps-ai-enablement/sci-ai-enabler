---
title: Libraries
parent: Recipes
nav_order: 2
permalink: /recipes/dependencies.html
---

# Libraries recipes install

{: .no_toc }

Some recipes don't drive a Claude Skill or MCP server at all — they have Claude Code `pip install` a
scientific library and write a script against it. Those libraries are **dependencies**, not catalog
entries: they have no catalog page, no shelf card, and no verification badge, because they aren't
Claude components. This page is the index of every one of them, so you can see what the cookbook
actually reaches for.

Each row is declared in a recipe's `## Dependencies` block with an exact pin, its license, the module
name to import, and a dated primary source. Where the **Checked** column shows a verdict, that
pinned install and that import were **executed** in a secretless container — not just looked up.

**These need a local execution environment.** They work in Claude Code; they are not available in
Claude.ai chat, which has nowhere to install them. If you're on Claude.ai, you want a
[Connector]({{ '/catalog/' | relative_url }}) instead.

{% assign deps = site.data.dependencies.dependencies %}
{% if deps and deps.size > 0 %}

| Library | Pinned | License | Import | Used by | Checked |
|---|---|---|---|---|---|
{% for d in deps -%}
| {% if d.source_url != "" %}[{{ d.package }}]({{ d.source_url }}){% else %}{{ d.package }}{% endif %} | `{{ d.pin }}` | {{ d.license }} | `{{ d.import }}` | {% for r in d.recipes %}[{{ r }}]({{ '/recipes/items/' | relative_url }}{{ r }}.html){% unless forloop.last %}, {% endunless %}{% endfor %} | {% if d.verdict == "pass" %}install + import OK ({{ d.verdict_on }}){% elsif d.verdict != "" %}**{{ d.verdict }}** ({{ d.verdict_on }}){% else %}—{% endif %} |
{% endfor %}

{{ deps.size }} librar{% if deps.size == 1 %}y{% else %}ies{% endif %}, generated
{{ site.data.dependencies.generated }}.

{% else %}

_No recipe declares a library dependency yet._

{% endif %}

## How a library gets on this page

It is pulled in by a recipe, never surfaced on its own. When a recipe needs a library that has no
Claude wrapper, the assembler records it with a pinned version, its license, the import module, and a
source it fetched that day. That is the whole intake rule — this page can only ever list what the
cookbook actually uses, which is why it will never grow into a mirror of PyPI.

Only `pip`-installable packages qualify today. conda, npm, CRAN/Bioconductor, compiled binaries, and
hosted services can't be verified in the sandbox, so a recipe needing one is deferred instead
of shipped on an unchecked claim.

## What "Checked" means, and doesn't

A `pass` means the pinned version installed cleanly and the declared module imported, in a
throwaway container with no credentials. It does **not** mean the library is safe — `pip install`
already runs the package's own build hooks — and it does **not** cover first-run downloads like model
weights or atlas volumes, which the import never touches. Recipes that need those say so.

An empty **Checked** cell means the dependency hasn't come up in the rotation yet, not that it
failed.

A verdict is also **environment-specific**. The check runs in a Linux container provisioned to
resemble the laptop these recipes target, graphics libraries included — because a package like
`opencv-python` imports fine on a laptop and fails on a bare headless server. Where that distinction
matters, the recipe says so and gives the remedy; a verdict here is evidence about one environment,
not a universal claim.
