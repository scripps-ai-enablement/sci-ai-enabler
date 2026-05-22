---
title: Translational Medicine
parent: Catalog
nav_order: 6
permalink: /catalog/translational-medicine.html
---

# Translational Medicine

Installable Claude components bridging discovery and clinical application — clinical-trial tooling, biomarker discovery, patient stratification, real-world evidence, EHR-aware agents, and regulatory-document assistants.

{% assign tools = site.pages | where_exp: "p", "p.tool_type" | sort: "title" %}
{% for tool in tools %}
{% if tool.tool_categories contains "Translational Medicine" or tool.tool_categories contains "All" %}
### [{{ tool.title }}]({{ tool.url | relative_url }})
*{{ tool.tool_type }} · {{ tool.supplier }} · {{ tool.availability }}*

{{ tool.summary }}

{% endif %}
{% endfor %}

---

## Got feedback on a tool?

Use the [tool-feedback Issue Form](https://github.com/goodb/sci-ai-enabler/issues/new?template=tool-feedback.yml) — pick the tool from a dropdown, describe what happened. A bot replies in-thread shortly; the next daily catalog run incorporates the feedback.
