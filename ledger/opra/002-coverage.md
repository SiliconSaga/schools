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

## The request

**To:** Custodian of Records, West Orange Board of Education, 179 Eagle Rock Avenue, West Orange, NJ 07052

**From:** Rasmus Praestholm (contact details are on the filed copy)

This is a request for government records under the Open Public Records Act, N.J.S.A. 47:1A-1 et seq., and the common law right of access. It is not made for a commercial purpose. Electronic copies by email are requested. The period is September 1, 2026 through the date of the request.

1. Every report delivered to the District during the period by EduStaff, or by any other vendor providing paraprofessional staffing, concerning fill rates, absences, vacancies, or unfilled paraprofessional assignments.
2. A report or export from the absence-management or scheduling system used for paraprofessional assignments, whether the District operates it or the vendor operates it on the District's behalf, showing for each school day in the period, by school building, the number of paraprofessional assignments, the number filled, and the number unfilled. If no report with exactly those fields exists, the closest standard report that system produces.
3. The most recent existing document(s) showing paraprofessional positions or assignments by school for 2026-27 and which of them are vacant, such as a staffing allocation list or vacancy list.
4. Any presentation, slides, or written report on paraprofessional staffing delivered at the September 28, 2026 Board meeting.
5. The classroom aide or paraprofessional job description(s) in effect for 2026-27, and the county office of education's approval of them under N.J.A.C. 6A:14-4.1(e).

Student names, personally identifiable student information, and the names of individual paraprofessionals are not sought and may be redacted. Counts by building and date are what matter.

## Log

- **October 1, 2026.** Drafted. Not yet filed.

## Documents

{% if r.documents.size > 0 %}{% for d in r.documents %}- [{{ d.label }}]({{ d.url }})
{% endfor %}{% else %}None yet.{% endif %}
