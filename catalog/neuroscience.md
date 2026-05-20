---
title: Neuroscience
parent: Catalog
nav_order: 5
permalink: /catalog/neuroscience.html
---

# Neuroscience

Installable Claude components for neural-data analysis, brain imaging, connectomics, electrophysiology, behavioral assays, and computational neuroscience.

{% assign tools = site.pages | where_exp: "p", "p.tool_type" | sort: "title" %}
{% for tool in tools %}
{% if tool.tool_categories contains "Neuroscience" or tool.tool_categories contains "All" %}
### [{{ tool.title }}]({{ tool.url | relative_url }})
*{{ tool.tool_type }} · {{ tool.supplier }} · {{ tool.availability }}*

{{ tool.summary }}

{% endif %}
{% endfor %}
