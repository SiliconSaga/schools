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

**To:** Custodian of Records, West Orange Board of Education, 179 Eagle Rock Avenue, West Orange, NJ 07052

**From:** Rasmus Praestholm (contact details are on the filed copy)

This is a request for government records under the Open Public Records Act, N.J.S.A. 47:1A-1 et seq., and the common law right of access. It is not made for a commercial purpose. Electronic copies by email are requested.

1. The agreement between the Board and EduStaff in effect for the 2026-27 school year: the base agreement, all exhibits, and every addendum, amendment, renewal, or extension, including the "EduStaff Pricing Schedule Addendum-Exhibit B" approved at the July 21, 2026 meeting (Finance/Business Office item 21, estimated amount $12,000,000). Also any other agreement under which paraprofessional staffing services are provided to the District for 2026-27.
2. The Board resolution(s) that awarded, renewed, or extended the EduStaff agreement for the 2025-26 and 2026-27 school years, with the backup material attached to each agenda item.
3. The Memorandum of Agreement with the West Orange Education Association permitting the outsourcing of the paraprofessionals, approved June 16, 2026 (Personnel item 6, Att. #18), and the revised Memorandum of Agreement approved July 21, 2026 (Personnel item 3(i), Att. #2).
4. For Competitive Contracting Request for Proposal CC 25-09, Substitute Staffing and Paraprofessional Services: every proposal received, and any evaluation report or memorandum recommending the rejection approved June 16, 2026 (Finance/Business Office item 29).
5. Every invoice submitted to the District by EduStaff, or by any other vendor providing paraprofessional staffing, from July 1, 2026 through the date of this request, including any supporting detail attached to the invoice as submitted, such as hours or positions billed.
6. The purchase orders and payment records (vouchers, bill-list entries) for payments to those vendors over the same period.
7. The analysis, calculation, or cost comparison supporting the "$3 million savings" from outsourcing paraprofessional services stated in the Superintendent's community letter of April 29, 2026, and any version of it presented to the Board or to the public.

Student names, personally identifiable student information, and employees' home addresses or personal details are not sought and may be redacted.

## Log

- **October 1, 2026.** Drafted. Not yet filed.

## Documents

{% if r.documents.size > 0 %}{% for d in r.documents %}- [{{ d.label }}]({{ d.url }})
{% endfor %}{% else %}None yet.{% endif %}
