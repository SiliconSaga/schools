"""
Tally the paraprofessional list the district released on September 16, 2026 in answer to a
resident's OPRA request of September 4, 2026 ("the list of names of paraprofessionals that are
employed through Edustaff and assigned to work as paraprofessionals ... for the 2026-2027 school
year"). The record is five pages with the columns Last Name, First Name, Assignment, Notes; Notes
is "Edustaff" or "Employed by West Orange". The PDF is read in pypdf's layout mode and each line
is sliced at the header positions. A row is counted when its Notes cell holds one of the two
values; the names are never printed. --names-removed writes the Assignment and Notes columns, in
the record's order, with a bracketed surname inside an assignment replaced by "(name removed)",
as the copy the ledger publishes. Needs pypdf 4 or later.
"""

import argparse
import collections
import re

from pypdf import PdfReader

EMPLOYERS = ("Edustaff", "Employed by West Orange")
# Three assignments carry a surname in brackets, presumably the classroom teacher's.
NAME_IN_BRACKETS = re.compile(r"\([A-Za-z]+\)")
BUILDINGS = (
    ("BMELC", "Betty Maddalena Early Learning Center at Mt. Pleasant"),
    ("ECLC", "Early Childhood Learning Center"),
    ("WOHS", "West Orange High School"),
    ("EDISON", "Edison"),
    ("LIBERTY", "Liberty"),
    ("ROOSEVELT", "Roosevelt"),
    ("GREGORY", "Gregory"),
    ("HAZEL", "Hazel"),
    ("KELLY", "Kelly"),
    ("MT PLEASANT", "Mt. Pleasant"),
    ("MT.PLEASANT", "Mt. Pleasant"),
    ("MT. PLEASANT", "Mt. Pleasant"),
    ("REDWOOD", "Redwood"),
    ("ST. CLOUD", "St. Cloud"),
    ("ST.CLOUD", "St. Cloud"),
    ("ST CLOUD", "St. Cloud"),
    ("WASH", "Washington"),
)


def building(assignment):
    """The school or program named in an assignment, or "not stated"."""
    text = assignment.upper()
    for key, name in BUILDINGS:
        if key in text:
            return name
    return "not stated"


def rows_from(pdf):
    """(assignment, employer) for each row, in the record's order."""
    rows = []
    for page_no, page in enumerate(PdfReader(pdf).pages, 1):
        text = page.extract_text(extraction_mode="layout")
        for line_no, line in enumerate(text.splitlines(), 1):
            cells = re.split(r"\s{2,}", line.strip())
            # Errors give the position only: the line itself would carry a name.
            if cells[-1] in EMPLOYERS:
                # Last Name, First Name, Assignment, Notes; a surname wrapped onto its own line
                # above leaves that line with no Notes cell, and it is skipped. One assignment
                # holds a double space, so it is everything between the first name and the Notes.
                if len(cells) < 4:
                    raise SystemExit(f"page {page_no} line {line_no}: fewer than four cells")
                assignment = NAME_IN_BRACKETS.sub("(name removed)", " ".join(cells[2:-1]))
                rows.append((assignment, cells[-1]))
            elif "Edustaff" in line or "West Orange" in line:
                raise SystemExit(f"page {page_no} line {line_no}: employer text outside the Notes cell")
    return rows


def main():
    """Print the counts and, if asked, write the names-removed copy."""
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("pdf", help="the five-page attachment to the custodian's letter of September 16, 2026")
    p.add_argument("--names-removed", metavar="FILE", help="write the Assignment and Notes columns to FILE")
    args = p.parse_args()

    rows = rows_from(args.pdf)
    by_employer = collections.Counter(e for _, e in rows)
    print(f"rows: {len(rows)}")
    for e in EMPLOYERS:
        print(f"  {e}: {by_employer[e]}")
    print("by building (Edustaff / Employed by West Orange):")
    by_building = collections.defaultdict(collections.Counter)
    for a, e in rows:
        by_building[building(a)][e] += 1
    for b, c in sorted(by_building.items(), key=lambda kv: -sum(kv[1].values())):
        print(f"  {b}: {c[EMPLOYERS[0]]} / {c[EMPLOYERS[1]]}")
    print("assignments that name 26-27 reassignment or addition:",
          sum(1 for a, _ in rows if "26-27" in a))

    if args.names_removed:
        width = max(len(a) for a, _ in rows)
        with open(args.names_removed, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"{'Assignment':<{width}}  Notes\n")
            for a, e in rows:
                f.write(f"{a:<{width}}  {e}\n")
        print(f"wrote {args.names_removed}")


if __name__ == "__main__":
    main()
