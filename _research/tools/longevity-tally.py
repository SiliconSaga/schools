"""
Tally the Longevity column of the "Reappointments: WOEA Tenure Certificated Staff for the
2026-2027 School Year" table in the May 4, 2026 Board agenda attachments (pp. 11-32).
Usage: python _research/tools/longevity-tally.py <agenda-attachments.pdf>
Source: https://resources.finalsite.net/images/v1777924001/woboeorg/tacqxglh2ky5ceo8hyp3/UPDATEDMay42026AgendaAttachments5-4-26.pdf
Each row reads: location, name, position, guide, step, base salary, [longevity], [stipend], salary, FTE.
A row is counted only if its dollar amounts add up (base + middle amounts = salary). Needs pypdf.
"""

import collections
import re
import sys

from pypdf import PdfReader

if len(sys.argv) != 2:
    sys.exit(__doc__)

ROW = re.compile(r"TEACHER (BA|BA\+15|BA\+30|MA|MA\+15|MA\+30|MA\+45|PHD/DOC) (\d+) ((?:\$[\d,]+\.\d\d ){2,4})(\d{2,3})\b")
MONEY = re.compile(r"\$([\d,]+\.\d\d)")

rows, pages, unsummed = [], [], 0
for i, page in enumerate(PdfReader(sys.argv[1]).pages, 1):
    text = " ".join((page.extract_text() or "").split())
    if "WOEA Tenure Certificated Staff" not in text:
        continue
    pages.append(i)
    for m in ROW.finditer(text):
        amounts = [float(x.replace(",", "")) for x in MONEY.findall(m.group(3))]
        base, salary, middle = amounts[0], amounts[-1], amounts[1:-1]
        if abs(base + sum(middle) - salary) > 0.01:
            unsummed += 1
            continue
        rows.append(middle[0] if middle else 0.0)

counts = collections.Counter(rows)
print(f"table pages {pages[0]}-{pages[-1]}; staff rows {len(rows)}; rows skipped because amounts did not add up: {unsummed}")
for value, n in sorted(counts.items()):
    print(f"  {'no longevity' if value == 0 else f'${value:,.2f}':>14}: {n}")
with_longevity = [v for v in rows if v > 0]
print(f"staff with a longevity amount: {len(with_longevity)} of {len(rows)}")
print(f"total longevity: ${sum(with_longevity):,.2f}")
print(f"at $10,000 or more: {sum(1 for v in with_longevity if v >= 10000)}; at $12,000 or more: {sum(1 for v in with_longevity if v >= 12000)}")
