---
title: Immunology and Microbiology
parent: Catalog
nav_order: 2
permalink: /catalog/immunology-microbiology.html
---

# Immunology and Microbiology

Installable Claude components for immune-repertoire analysis, epitope prediction, antibody design, microbial genomics, metagenomics, and host-pathogen interaction modelling.

{% assign tools = site.pages | where_exp: "p", "p.tool_type" | sort: "title" %}
{% for tool in tools %}
{% if tool.tool_categories contains "Immunology and Microbiology" or tool.tool_categories contains "All" %}
### [{{ tool.title }}]({{ tool.url | relative_url }})
*{{ tool.tool_type }} · {{ tool.supplier }} · {{ tool.availability }}*

{{ tool.summary }}

{% endif %}
{% endfor %}
