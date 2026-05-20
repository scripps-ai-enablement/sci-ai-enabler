---
title: Drug Repurposing and Discovery
parent: Catalog
nav_order: 7
permalink: /catalog/drug-repurposing-discovery.html
---

# Drug Repurposing and Discovery

Installable Claude components for target identification, virtual screening, lead optimization, ADMET prediction, drug-repurposing knowledge graphs, and end-to-end discovery agents.

{% assign tools = site.pages | where_exp: "p", "p.tool_type" | sort: "title" %}
{% for tool in tools %}
{% if tool.tool_categories contains "Drug Repurposing and Discovery" or tool.tool_categories contains "All" %}
### [{{ tool.title }}]({{ tool.url | relative_url }})
*{{ tool.tool_type }} · {{ tool.supplier }} · {{ tool.availability }}*

{{ tool.summary }}

{% endif %}
{% endfor %}
