---
layout: default
title: "OPRA-002: Coverage records"
parent: "Records Requests"
nav_order: 2
---

{% assign r = site.data.opra | where: "id", "OPRA-002" | first %}

# OPRA-002: Paraprofessional coverage records

**Status:** {{ r.status | capitalize }}{% if r.filed %} · **Filed:** {{ r.filed | date: "%B %-d, %Y" }}{% endif %}{% if r.due %} · **Response due:** {{ r.due | date: "%B %-d, %Y" }}{% endif %}

## Why this request

Families were told in April that students would "continue to see the same familiar faces" and that there would be "no rotation of paras". As far as I can find, the district has published nothing in writing since school opened showing how many paraprofessional positions are filled on a given day. This request asks for the district's own coverage records.

Two related records have gone to another resident: on September 16 the district released a list of 145 paraprofessionals with their employer, and on October 16 it took a two-week extension, to October 30, on a request for September's substitute-coverage report for paraprofessional absences (see [Requests by other residents](/ledger/opra/#requests-by-other-residents)).

## The request

The text below is the request as prepared for filing. The filed copy carries the requester's contact details and date in place of this heading.

**To:** Custodian of Records, West Orange Board of Education, 179 Eagle Rock Avenue, West Orange, NJ 07052

**From:** Rasmus Praestholm (contact details are on the filed copy)

{% include opra/002-coverage.md %}

## Log

- **October 1, 2026.** Drafted.
- **October 13, 2026.** Text finalized for filing.
- **October 14, 2026.** Handed to the custodian of records at the Business Office, 179 Eagle Rock Avenue, with the district's OPRA request form; the receipt copy was date-stamped the same day (see Documents). The same text was emailed to the custodian, who confirmed receipt. The seven-business-day response period runs to October 23, 2026.

## Documents

{% if r.documents.size > 0 %}{% for d in r.documents %}- [{{ d.label }}]({{ d.url }})
{% endfor %}{% else %}None yet.{% endif %}
