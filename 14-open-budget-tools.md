---
layout: default
title: "Open Budget & Participatory Finance"
nav_order: 15
parent: "Modules"
---

# Module 12: Open Budget & Participatory Finance

*OpenCollective, Participatory Budgeting, and Budget Visualization as Proof of Concept*

---

- **Impact Potential:** Very High -- not primarily for the dollars raised (though
  those matter) but for the credibility it builds; showing the board a live, funded,
  transparent financial operation is the most powerful possible demonstration that
  the community can self-organize
- **Effort:** Medium -- OpenCollective setup is straightforward; participatory
  budgeting requires design and facilitation; budget visualization requires data
  extraction and development
- **Timeline:** OpenCollective can be live within days; a PTA participatory budget
  cycle could run in 2-4 weeks; budget visualization is a multi-week project
- **Key Risks:** Low adoption if parents don't understand the tool; potential
  confusion between PTA funds and district funds (keep boundaries clear);
  participatory budgeting works best with clear scope limits
- **Print Priority:** High -- this is the "show, don't tell" proof that open
  governance works; bring a screenshot of the live OpenCollective dashboard if
  possible

---


## OpenCollective as PTA Infrastructure

[OpenCollective](https://opencollective.com) is a platform for transparent,
community-managed fundraising and spending. Every dollar in and every dollar out
is visible to anyone. It enables project-based directed giving, fiscal hosting
through a 501(c)(3) sponsor, and real-time public ledger visibility.

**For the full operational model** -- including how to set up the PTA on
OpenCollective, project-based fund structure, fiscal hosting options, corporate
matching, the equity problem across schools, and the Palo Alto PiE precedent --
see [Module 14: The PTA as Community Operating System](16-pta-opencollective).

This section focuses on how OpenCollective fits into the broader open finance
toolkit alongside participatory budgeting and budget visualization.

## Participatory Budgeting

### What It Is

Participatory budgeting (PB) is a democratic process where community members
directly decide how to allocate a portion of a public budget. It has been used
successfully in:

- **New York City** -- the largest PB program in the US, allocating millions in
  city council discretionary funds
- **Multiple NJ municipalities** -- several have piloted PB for parks, infrastructure,
  and community programs
- **School districts nationally** -- students vote on how to spend activity funds
  or improvement budgets

### How to Apply It to the PTA

Before asking the district to adopt participatory budgeting (which is a longer-term
governance change), **demonstrate it with PTA funds**:

1. The PTA designates a portion of its reserves (e.g., $25,000) for participatory
   allocation
2. Any PTA member can submit a **proposal** for how to spend the funds (aligned
   with the school's needs)
3. Proposals are posted publicly for comment and refinement (2 weeks)
4. All PTA members **vote** on which proposals to fund (1 week)
5. Results are binding and published transparently

### Why This Matters Strategically

The PTA running a successful participatory budget cycle is a **proof of concept**
the board cannot ignore:

- It demonstrates that community members can make responsible allocation decisions
- It shows that transparency increases engagement rather than creating chaos
- It produces a documented, auditable decision trail
- It pressures the board to explain why their process is less open than the PTA's

### Tools

Participatory budgeting doesn't require custom software. Existing tools:

- **[Participatory Budgeting Project](https://www.participatorybudgeting.org/pb-in-schools/)** --
  the main US nonprofit promoting PB; maintains guides, case studies, and a
  [PB in Schools guide (PDF)](https://www.participatorybudgeting.org/wp-content/uploads/2016/10/PB-in-Schools-Guide_PBP.pdf)
- **[PTAlink PB resources](https://ptalink.org/topic-areas/fundraising/participatory-budgeting-1)** --
  PB guidance specifically for PTAs
- **[Decidim](https://decidim.org/)** -- open-source democratic participation platform
  ([GitHub](https://github.com/decidim/decidim)), used by Barcelona, Helsinki,
  Mexico City, and [400+ instances worldwide](https://publicadministration.desa.un.org/good-practices-for-digital-government/compendium/decidim-multipurpose-open-source-platform-e)
- **Stanford Participatory Budgeting Platform** ([pbstanford.org](https://pbstanford.org/)) --
  developed the "knapsack voting" method
- **Simple Google Forms + OpenCollective** for a quick pilot

**Real examples:**
- **[Phoenix Union HSD](https://participedia.net/case/5586)** launched the first
  US school district PB process using district-wide funds
- **P.S. 139 in Brooklyn** runs PB with students and families to allocate Parent
  Association and school funds
- **Boston's [Youth Lead the Change](https://youth.boston.gov/youth-lead-the-change/)**
  gives young people ages 12-25 control over $1M in city capital budget

Long-term, this is exactly the kind of process the Demicracy platform is designed
to coordinate.

## Budget Visualization

### The Problem with Public Budget Data

The district's budget is a public document. In practice, it is a dense spreadsheet
or PDF that almost no one reads. "Transparency" that nobody can parse is not
transparency.

### The Proposal

Take the district's published budget and CAFR (Comprehensive Annual Financial
Report) and build an **interactive visualization**:

- Start with the total budget
- Drill down: Instruction > Special Areas > Art Teachers > the 15 minutes being cut
- Show the relative scale: "The art instruction being eliminated costs $X. The
  insurance broker's commission is $Y."
- Compare year-over-year: where has spending grown? Where has it been cut?

### Why It Changes the Conversation

When a parent can see that the cost of retaining one para is less than the
district's annual spending on a single vendor contract, the "numbers are what
they are" defense collapses. The numbers are exactly what they are -- and now
everyone can read them.

### Tools

- **ClearGov** -- a commercial platform that visualizes municipal and school
  budgets (some NJ districts already use it)
- **Open Budget** tools (open-source municipal budget visualization frameworks)
- A community-built visualization using the district's CAFR data and standard
  web charting libraries

A community volunteer with data visualization skills could build a first version
in a weekend using publicly available budget data.

## Connecting the Tools

```
OpenCollective          Participatory Budget        Budget Visualization
(transparent            (community decides          (everyone can read
 fundraising)            allocation)                 the district's books)
     |                        |                           |
     +------------------------+---------------------------+
                              |
                     Demicracy Platform
                  (coordination + governance
                   infrastructure for all of it)
```

Each tool proves a principle. Together, they prove the thesis: **open, community-
driven governance is not idealistic -- it is operational, and the community is
already doing it.**

[Back to Index](index) | Next: [PTA Coordination](15-pta-coordination)
