---
layout: default
title: "Timeline"
parent: "The Ledger"
nav_order: 1
---

# Timeline

What was decided and said, newest first. Each entry links to its source. The labels are explained on [The Ledger](/ledger/#how-to-read-this).

{% assign entries = site.data.timeline | sort: "date" | reverse %}
{% for e in entries %}
---

### {{ e.date | date: "%B %-d, %Y" }}: {{ e.title }}

{% if e.basis == "record" %}<span class="label label-blue">Record</span>{% elsif e.basis == "statement" %}<span class="label label-purple">Statement</span>{% elsif e.basis == "press" %}<span class="label label-yellow">Press</span>{% endif %}

{{ e.summary }}

{% if e.sources.size > 0 %}Source: {% for s in e.sources %}[{{ s.label }}]({{ s.url }}){% unless forloop.last %}; {% endunless %}{% endfor %}{% endif %}
{% endfor %}
