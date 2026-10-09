# Design: the Ledger section and the whitepaper reframe

Draft for the owner's review, September 30, 2026. Adapts the Gemini design doc (`gemini-code-1790819585981.md`) to this site. Nothing here is built yet.

## What it is for

A public, sourced record of the paraprofessional outsourcing in West Orange: what the district decided, what it said, what records were requested and what came back. It is one parent's project, written in the first person, speaking for no PTA, parent group, or union. Its force comes from being checkable, so the ledger pages state facts with their sources and leave the argument to the home page and the speeches.

It is not a campaign to flood the district with requests or to push parents into rewriting IEPs.

## Changes from the Gemini doc

| Gemini doc | Here | Why |
|---|---|---|
| New Hugo or Astro site | New section of the existing Jekyll site | One site, one audience, already live |
| JSON content files | `_data/opra.yml`, `_data/timeline.yml` | Jekyll's native data files; pages render from them |
| Timeline mixes filings and field reports as equals | Every entry carries a basis: record, statement, or report | See the evidence standard below |
| Sample entry: "Confirmed teacher resignation citing lack of aide support" | Not published | The reason is not known |
| Tokens handed out by the union and PTAs | Deferred to its own design | The owner acts as an individual; no organization has agreed to anything |
| "Trigger parent IEP enforcement campaign" | Dropped. A plain-language page on documenting missed services, later, reviewed by an advocate | Avoids steering other families' IEPs |
| Day-counted escalation playbook, published | The site states what the law provides next, when it becomes relevant | A published threat schedule reads as a campaign; the record is stronger without it |
| Hash validation for PDFs | Git history | Already tamper-evident |

## Pages

All under `ledger/`, with "The Ledger" directly below Home in the navigation.

- `/ledger/` — what happened in one screen, each line linked to its source; current status of each request.
- `/ledger/timeline/` — dated entries from `_data/timeline.yml`, newest first.
- `/ledger/opra/` — table from `_data/opra.yml`: request, filed, due, status, documents.
- `/ledger/opra/001-edustaff/`, `/ledger/opra/002-coverage/` — the request as filed, the stamped receipt, every response in full, and a dated log.
- `/ledger/statements/` — what the district said (the April 29 letter, meeting statements) beside what the records show. Starts with the statements alone; the records column fills in as responses arrive. Replaces the doc's `data/edustaff-gap`.
- `ledger/docs/` — receipts and responsive records as PDFs, with the owner's address and phone redacted.

Later phases, each with its own design: field reports through Ting, the missed-services page, and charts once there is data to chart.

## Evidence standard

Every timeline entry and every claim on a ledger page carries a label. The first three are published; the fourth is not.

- **Record** — a district or vendor document, linked, with page number. Stated as fact.
- **Press** — reported by a named news outlet, linked. Used where no district document is to hand, such as the May 4 budget vote.
- **Statement** — said by an official at a public meeting or in a letter. Quoted with the meeting date and, once posted, the video timestamp or minutes page. Figures from the owner's notes wait for the video.
- **Report** — second-hand. Not published. Reports stay in `_research/` until a record or statement backs them, and even then no school, staff member, or student is made identifiable and no cause or motive is attributed.

The district's responses are published in full. Corrections are dated and left visible.

## Reframing the existing site

- **Home page:** lead with the current situation in a few sourced lines and a link to the Ledger. Then say what the two halves of the site are: the Ledger, and the April whitepaper. Everything else on today's home page (the April 20 essay, the "Flatten the Curve" plan, the document index, the multi-organization model) moves to an archive page, `spring-2026.md`, kept as written.
- **Whitepaper framing,** on the home page, `modules.md`, and the Executive Summary: written in April 2026 in a few days by one person with AI tools, as a demonstration that a community can generate and sort many ideas quickly and hand the promising ones to volunteers. No single proposal was meant to close the gap.
- **Known fixes:** Module 4 still says the district "is considering" outsourcing; the home page has a personal Gmail address that the earlier cleanup missed; `_config.yml` title and description still say "Budget Options"; The Next Year lists pilot dates that have passed.
- **Out of scope for this pass:** a full accuracy audit of all twenty modules, the PDF build, and regenerating images that carry old addresses.

## Build and publish

Work on a branch in `components/schools`. Pushing to `main` publishes, so nothing is pushed until the owner has read the pages. Checks before that: the site builds, every ledger link resolves, and `_research/` is absent from the built output.

## Decisions (owner, October 1, 2026)

1. The section is called "The Ledger".
2. Report-level entries stay in `_research/`, unpublished, until a record or statement backs them.
3. The home page becomes a short statement of the current situation. The April 20 essay, the "Flatten the Curve" plan, the document index, and the rest of the April-era home page move to an archive page.
4. The Ting pilot described in The Next Year did not run for lack of interest. Ting remains available and untested; the page says so.
5. Open: whether request pages are published before filing as drafts, or on filing day. Until decided, the pages are built with status "drafted" and the owner chooses at push time.
