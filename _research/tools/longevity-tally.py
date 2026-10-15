"""
Tally the Longevity column of the "Reappointments: WOEA Tenure Certificated Staff for the
2026-2027 School Year" table in the May 4, 2026 Board agenda attachments (pp. 11-32).
Source: https://resources.finalsite.net/images/v1777924001/woboeorg/tacqxglh2ky5ceo8hyp3/UPDATEDMay42026AgendaAttachments5-4-26.pdf
The PDF is read in pypdf's layout mode, which keeps each column at its horizontal position.
Each dollar amount on a row is assigned to the column whose header sits above it (Base Salary,
Longevity, Stipend, Salary), so a stipend is never mistaken for longevity. A row is counted only
when the amounts add up (base + longevity + stipend = salary). Needs pypdf 4 or later.
"""

import argparse
import collections
import re

from pypdf import PdfReader

MONEY = re.compile(r"\$[\d,]+\.\d\d")
COLUMNS = ("Longevity", "Stipend", "Salary")


def header_spans(line):
    """Character spans of the column headers on the header line, with Base Salary set apart."""
    spans = {}
    for m in re.finditer(r"Longevity|Stipend|Salary", line):
        name = m.group(0)
        if name == "Salary":
            # The header line has "Salary Guide", then "Salary" under "Base", then the total "Salary".
            if line[m.end():m.end() + 6] == " Guide":
                continue
            name = "Base" if "Base" not in spans else "Salary"
        spans[name] = (m.start(), m.end())
    return spans if set(spans) >= {"Base", "Longevity", "Stipend", "Salary"} else None


def column_for(span, spans):
    center = (span[0] + span[1]) / 2
    return min(spans, key=lambda c: abs((spans[c][0] + spans[c][1]) / 2 - center))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("pdf", help="the agenda attachments PDF, or the saved pages 11-32")
    args = p.parse_args()

    rows, skipped, stipends = [], 0, 0
    for page in PdfReader(args.pdf).pages:
        text = page.extract_text(extraction_mode="layout")
        if "WOEA Tenure Certificated Staff" not in text:
            continue
        spans = None
        for line in text.splitlines():
            if spans is None:
                spans = header_spans(line)
                continue
            amounts = list(MONEY.finditer(line))
            if not amounts:
                continue
            by_col = {column_for(m.span(), spans): float(m.group(0)[1:].replace(",", "")) for m in amounts}
            base, longevity, stipend, salary = (by_col.get(c, 0.0) for c in ("Base", "Longevity", "Stipend", "Salary"))
            if not base or not salary or abs(base + longevity + stipend - salary) > 0.01:
                skipped += 1
                continue
            rows.append(longevity)
            stipends += bool(stipend)

    counts = collections.Counter(rows)
    print(f"staff rows {len(rows)}; rows skipped (no header found or amounts did not add up): {skipped}; rows with a stipend: {stipends}")
    for value, n in sorted(counts.items()):
        print(f"  {'no longevity' if value == 0 else f'${value:,.2f}':>14}: {n}")
    with_longevity = [v for v in rows if v > 0]
    print(f"staff with a longevity amount: {len(with_longevity)} of {len(rows)}")
    print(f"total longevity: ${sum(with_longevity):,.2f}")
    print(f"at $10,000 or more: {sum(1 for v in with_longevity if v >= 10000)}; at $12,000 or more: {sum(1 for v in with_longevity if v >= 12000)}")


if __name__ == "__main__":
    main()
