"""Print whitespace-collapsed PDF text around each pattern match, with page numbers.

Usage: python pdfgrep.py <pdf> <regex> [context chars, default 400]
A regex of ^ prints the start of every page.
"""
import re
import sys

from pypdf import PdfReader

if len(sys.argv) < 3:
    sys.exit(__doc__)
path, pattern = sys.argv[1], sys.argv[2]
try:
    window = int(sys.argv[3]) if len(sys.argv) > 3 else 400
except ValueError:
    sys.exit(f"context must be a whole number of characters, got {sys.argv[3]!r}")
reader = PdfReader(path)
print(f"pages: {len(reader.pages)}")
rx = re.compile(pattern, re.I)
for n, page in enumerate(reader.pages, 1):
    text = " ".join((page.extract_text() or "").split())
    last_end = -1
    for m in rx.finditer(text):
        if m.start() < last_end:
            continue
        lo, hi = max(0, m.start() - window), min(len(text), m.end() + window)
        last_end = hi
        print(f"--- p{n} ---")
        print(text[lo:hi].encode("ascii", "replace").decode())
