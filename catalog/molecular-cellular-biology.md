---
title: Molecular and Cellular Biology
parent: Catalog
nav_order: 4
permalink: /catalog/molecular-cellular-biology.html
---

# Molecular and Cellular Biology

Installable Claude components for genomics, transcriptomics, single-cell analysis, gene regulation, CRISPR design, cell imaging, and other molecular- and cell-scale biology applications.

{% assign tools = site.pages | where_exp: "p", "p.tool_type" | sort: "title" %}
{% for tool in tools %}
{% if tool.tool_categories contains "Molecular and Cellular Biology" or tool.tool_categories contains "All" %}
### [{{ tool.title }}]({{ tool.url | relative_url }})
*{{ tool.tool_type }} · {{ tool.supplier }} · {{ tool.availability }}*

{{ tool.summary }}

{% endif %}
{% endfor %}

---

## Got feedback on a tool?

Use the [tool-feedback Issue Form](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml) — pick the tool from a dropdown, describe what happened. A bot replies in-thread shortly; the next daily catalog run incorporates the feedback.
