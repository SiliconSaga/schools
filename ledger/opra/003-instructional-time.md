---
layout: default
title: "OPRA-003: Schedules and class coverage"
parent: "Records Requests"
nav_order: 3
---

{% assign r = site.data.opra | where: "id", "OPRA-003" | first %}

# OPRA-003: Instructional schedules, class coverage, and movies

**Status:** {{ r.status | capitalize }}{% if r.filed %} · **Filed:** {{ r.filed | date: "%B %-d, %Y" }}{% endif %}{% if r.due %} · **Response due:** {{ r.due | date: "%B %-d, %Y" }}{% endif %}

## Why this request

I have heard from my own children and from other parents about movies shown during the school day and about classes covered without a substitute this fall. Those are reports, not records, and this ledger does not publish them. The records that would show how instructional time is being used when staff are short are the school schedules, the district's own policy on showing films, the teacher-absence data the substitute system already holds, and whatever guidance staff were given. This request asks for those.

## The request

The text below is the request as prepared for filing. The filed copy carries the requester's contact details and date in place of this heading.

**To:** Custodian of Records, West Orange Board of Education, 179 Eagle Rock Avenue, West Orange, NJ 07052

**From:** Rasmus Praestholm (contact details are on the filed copy)

{% include opra/003-instructional-time.md %}

## Log

- **October 1, 2026.** Drafted.
- **October 13, 2026.** Text finalized for filing.
- **October 14, 2026.** Handed to the custodian of records at the Business Office, 179 Eagle Rock Avenue, with the district's OPRA request form; the receipt copy was date-stamped the same day (see Documents). The same text was emailed to the custodian, who confirmed receipt. The seven-business-day response period runs to October 23, 2026.

## Documents

{% if r.documents.size > 0 %}{% for d in r.documents %}- [{{ d.label }}]({{ d.url }})
{% endfor %}{% else %}None yet.{% endif %}
