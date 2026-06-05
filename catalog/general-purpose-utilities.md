---
title: General-Purpose Utilities
parent: Catalog
nav_order: 8
permalink: /catalog/general-purpose-utilities.html
---

# General-Purpose Utilities

Domain-agnostic building blocks that scientific recipes reuse regardless of research area: data wrangling, plotting and visualization, general machine learning and statistics, numerical and symbolic computing, scientific communication (writing, figures, posters, citation management, literature and web search), compute infrastructure, and adjacent-domain scientific tools (quantum, materials, astronomy, geospatial) that overlap life-science problems. These are tagged for the utilities shelf only, so they stay off the seven research-area pages while remaining available to assemble into workflows.

{% assign tools = site.pages | where_exp: "p", "p.tool_type" | sort: "title" %}
{% for tool in tools %}
{% if tool.tool_categories contains "General-Purpose Utilities" %}
### [{{ tool.title }}]({{ tool.url | relative_url }})
*{{ tool.tool_type }} · {{ tool.supplier }} · {{ tool.availability }}*

{{ tool.summary }}

{% endif %}
{% endfor %}

---

## Got feedback on a tool?

Use the [tool-feedback Issue Form](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml) — pick the tool from a dropdown, describe what happened. A bot replies in-thread shortly; the next daily catalog run incorporates the feedback.
