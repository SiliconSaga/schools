---
layout: default
title: "OPRA-001: Staffing contract and billing"
parent: "Records Requests"
nav_order: 1
---

{% assign r = site.data.opra | where: "id", "OPRA-001" | first %}

# OPRA-001: Paraprofessional staffing contract and billing

**Status:** {{ r.status | capitalize }}{% if r.filed %} · **Filed:** {{ r.filed | date: "%B %-d, %Y" }}{% endif %}{% if r.due %} · **Response due:** {{ r.due | date: "%B %-d, %Y" }}{% endif %}

## Why this request

The Board rejected the proposals it received for substitute and paraprofessional staffing on June 16, 2026, then approved an EduStaff pricing addendum estimated at $12,000,000 on July 21. The minutes do not say what the addendum covers. The district said at its September 28 meeting that it is working with EduStaff to bring paraprofessionals on, but no posted document sets out the arrangement or says how it was awarded. The union memorandum permitting the outsourcing is an attachment that is not posted with the minutes. Families were told the change saves $3 million a year. This request asks for the documents behind those decisions and for what has been billed since.

## The request

The text below is the request as prepared for filing. The filed copy carries the requester's contact details and date in place of this heading.

**To:** Custodian of Records, West Orange Board of Education, 179 Eagle Rock Avenue, West Orange, NJ 07052

**From:** Rasmus Praestholm (contact details are on the filed copy)

{% include opra/001-edustaff.md %}

## Log

- **October 1, 2026.** Drafted.
- **October 13, 2026.** Text finalized for filing.
- **October 14, 2026.** Hand-delivered to the Business Office, 179 Eagle Rock Avenue, with the district's OPRA request form. Items 1, 3, 5, and 6 are immediate-access records; the seven-business-day period for the rest runs to October 23, 2026.

## Documents

{% if r.documents.size > 0 %}{% for d in r.documents %}- [{{ d.label }}]({{ d.url }})
{% endfor %}{% else %}None yet.{% endif %}
