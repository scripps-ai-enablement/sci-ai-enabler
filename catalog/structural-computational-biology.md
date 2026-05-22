---
title: Integrative Structural and Computational Biology
parent: Catalog
nav_order: 3
permalink: /catalog/structural-computational-biology.html
---

# Integrative Structural and Computational Biology

Installable Claude components for protein and complex structure prediction, molecular dynamics, integrative modelling, cryo-EM analysis, and computational biology workflows that span structure, sequence, and dynamics.

{% assign tools = site.pages | where_exp: "p", "p.tool_type" | sort: "title" %}
{% for tool in tools %}
{% if tool.tool_categories contains "Integrative Structural and Computational Biology" or tool.tool_categories contains "All" %}
### [{{ tool.title }}]({{ tool.url | relative_url }})
*{{ tool.tool_type }} · {{ tool.supplier }} · {{ tool.availability }}*

{{ tool.summary }}

{% endif %}
{% endfor %}

---

## Got feedback on a tool?

Use the [tool-feedback Issue Form](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml) — pick the tool from a dropdown, describe what happened. A bot replies in-thread shortly; the next daily catalog run incorporates the feedback.
