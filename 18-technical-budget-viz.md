---
layout: default
title: "Budget Visualization"
parent: "Appendix"
nav_order: 2
---

# Technical Design: District Budget Visualization

*Making the Numbers Legible -- Interactive Budget Explorer from Public CAFR Data*

> **Document Type:** Technical design plan -- for developers and data-skilled
> volunteers. Not part of the printed whitepaper.
> **Audience:** Developers, data visualization volunteers, civic tech contributors
> **Prerequisite reading:** [Module 12 (Open Budget Tools)](14-open-budget-tools)

---

## Purpose

The district publishes its budget and CAFR (Comprehensive Annual Financial Report)
as PDF documents. These are public records. They are also effectively unreadable
to anyone who isn't a school finance professional.

This project takes that data and makes it interactive: a web-based explorer where
any resident can drill from "total budget" down to "the specific line item being
cut" and compare it to other line items (broker commissions, vendor contracts,
administrative overhead).

The goal is not editorial commentary. The goal is legibility. When the numbers
speak for themselves, commentary is unnecessary.

## Data Sources

### Primary: The Annual Budget (User-Friendly Budget)

NJ districts are required to publish a "User-Friendly Budget" (UFB) alongside
the formal budget. This simplified document contains:

- Revenue by source (local taxes, state aid, federal aid)
- Expenditures by function (instruction, support services, administration,
  operations, debt service)
- Per-pupil spending comparisons
- Year-over-year changes

The UFB is usually a PDF. The formal budget (A-148 form) contains detailed
line items.

### Secondary: The CAFR

The Comprehensive Annual Financial Report includes:

- Fund balance (surplus/deficit) history
- Debt obligations
- Capital expenditure plans
- Detailed revenue and expenditure schedules
- Comparative data (prior year actuals vs. current year budget)

### Tertiary: State Data

The NJ DOE publishes comparative spending data for all districts:

- Per-pupil expenditures by category
- Administrative spending ratios
- State aid allocations
- Comparative rankings

This context is critical: "We spend $X per pupil on administration" means nothing
without knowing the state median.

## Data Pipeline

```
PDF Budget Documents          NJ DOE Comparative Data
       │                              │
       ▼                              ▼
  Manual extraction            API/CSV download
  (tabula-py or                (NJ DOE data portal)
   camelot for tables)                │
       │                              │
       ▼                              ▼
  Structured JSON/CSV         Structured JSON/CSV
       │                              │
       └──────────┬───────────────────┘
                  ▼
         Normalized Data Store
         (static JSON files in repo --
          no database needed)
                  │
                  ▼
         Static Site Generator
         (Astro, Next.js, or plain
          HTML + D3/Observable)
                  │
                  ▼
         GitHub Pages
         (hosted alongside whitepaper)
```

### Data Extraction Notes

- **Tabula-py** or **Camelot** can extract tables from budget PDFs with reasonable
  accuracy. Manual cleanup will be needed.
- The NJ DOE data portal provides CSV exports of comparative spending data. No
  scraping needed.
- Budget line items should be normalized to a consistent taxonomy across years for
  year-over-year comparison.
- **Important:** Store extracted data as versioned JSON in the repo. This makes
  the extraction auditable -- anyone can verify the visualization matches the
  source documents.

## Visualization Design

### View 1: The Treemap (Where Does the Money Go?)

A hierarchical treemap showing budget allocation at three levels:

```
Level 1: Major categories (Instruction, Support Services, Admin, Operations)
Level 2: Sub-categories (Regular Instruction, Special Ed, Art/Music/Library, ...)
Level 3: Line items (Teacher salaries, Para salaries, Benefits, Supplies, ...)
```

Each rectangle's area is proportional to spending. Color indicates year-over-year
change (green = increased, red = decreased, gray = stable).

**The key insight this enables:** A parent can see at a glance that "Art & Library
instruction" is a tiny rectangle compared to "Health Insurance Premiums" or
"Administrative Salaries." The visual immediately reframes "we can't afford art
teachers" into "we can't afford art teachers *while spending X on Y*."

### View 2: The Waterfall (How Did We Get Here?)

A waterfall chart showing how the budget changed from last year to this year:

```
Last Year Budget → +State Aid Change → +Enrollment Change → +Insurance Increase
                 → -Revenue Loss → = This Year Gap → Proposed Cuts to Close
```

This makes the deficit's *causes* visible. If health insurance accounts for 60%
of the cost increase, that's immediately apparent. The board can't hide behind
"the numbers are what they are" when the visualization shows exactly which numbers
changed and by how much.

### View 3: The Comparison (How Do We Stack Up?)

Side-by-side comparison with:

- State median per-pupil spending by category
- Comparable districts (similar size, demographics, DFG -- District Factor Group)
- The district's own historical trend (5-year spending by category)

**What to look for:**

- Administrative spending above state median → potential savings target
- Per-pupil instructional spending below median → evidence that cuts have already
  gone too far
- Benefit costs above comparable districts → supports the insurance transparency
  argument (Module 5)

### View 4: The Impact Calculator

An interactive tool where residents can model "what if" scenarios:

- "If we saved 7% on health insurance, how many paras could we retain?"
- "If the Open Image Project generates $80,000/year, what does that fund?"
- "If we used our banked levy cap, what's the impact on the average tax bill?"

This directly supports the whitepaper's arguments with personalized numbers.

## Technology Choices

### Recommended Stack

For a small civic tech project maintained by volunteers:

- **Static site** (Astro or plain HTML) -- no server to maintain, free hosting
- **D3.js** or **Observable Plot** for visualizations -- industry standard,
  well-documented, handles all four view types
- **GitHub Pages** for hosting -- free, automatic deployment, version-controlled
- **JSON data files** in the repo -- no database, no API, no ops burden

### Why Not a Framework-Heavy Approach?

- Volunteer-maintained projects die when the maintainer leaves. Static sites
  survive indefinitely.
- The data changes once a year (budget cycle). There is no need for dynamic
  data fetching.
- GitHub Pages is free forever. A server costs money and requires upkeep.
- D3.js skills are common in the data visualization community. React/Vue skills
  are common in web dev. The intersection is smaller than either alone.

### Accessibility

- All visualizations must have text-based alternatives (tables, summaries)
- Color choices must be colorblind-safe (use viridis or similar palettes)
- Charts must be navigable by keyboard
- Mobile-responsive layouts (parents will view this on phones)

## Integration Points

### With the Whitepaper Site

The budget visualization lives on the same GitHub Pages site as the whitepaper.
The INDEX.md links to it. Individual modules link to relevant views:

- Module 1 (Bridge Grant) → treemap zoomed to Art/Library line items
- Module 4 (Para Audit) → comparison of para costs vs. agency contract estimates
- Module 5 (Health Insurance) → waterfall showing insurance as % of deficit
- Module 13 (Regulatory Leverage) → comparison view vs. state median

### With OpenCollective

The Impact Calculator can pull live data from the PTA's OpenCollective projects:

"The Curriculum Preservation Fund has raised $42,000 of its $75,000 target.
That's enough to preserve 56% of the art instruction gap. [Contribute →]"

This turns the budget visualization from a critique into a call to action.

## Development Plan

### Sprint 1: Data Foundation (1-2 weekends)

- Extract current year budget and prior year actuals from PDF
- Normalize to JSON schema
- Download NJ DOE comparative data
- Commit to repo with source PDF links for auditability

### Sprint 2: Core Treemap (1 weekend)

- Static HTML + D3.js treemap of current year budget
- Click-to-drill interaction (category → sub-category → line item)
- Color coding for year-over-year change
- Deploy to GitHub Pages

### Sprint 3: Waterfall & Comparison (1-2 weekends)

- Waterfall chart showing deficit composition
- Comparison charts vs. state median and similar districts
- Text summaries for accessibility

### Sprint 4: Impact Calculator (1 weekend)

- Interactive sliders for "what if" scenarios
- Integration with OpenCollective API for live fund status
- Shareable URLs for specific scenarios ("look what 7% insurance savings does")

### Total Estimated Effort

A skilled volunteer could produce a functional version in 4-6 weekends. The
first sprint (data extraction) is the most labor-intensive and least fun -- this
is where the grant writing team's data skills or a student project volunteer
could help.

---

[Back to Index](index)
