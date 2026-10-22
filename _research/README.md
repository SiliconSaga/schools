# Research workbench

Working notes, drafts, and source copies behind the site. Jekyll skips folders that start with an underscore, so nothing here appears on the site itself, but the repository is public and everything here is deliberately so: the owner keeps the research trail in the open, and anything that should not be public does not belong in this folder.

- `opra/` — owner notes on each request, the filing steps (`filing.md`), and the requester-details template; the request texts themselves are in `_includes/opra/`, shared by the ledger pages and the printed letters
- `sources/` — copies of district documents the notes cite, saved against link rot
- `tools/` — small helpers: `pdfgrep.py` prints PDF text around a search pattern (needs `pypdf`); `opra-print.py` renders the request letters to PDF for filing; `longevity-tally.py` and `para-list-tally.py` reproduce the counts the ledger cites from the May 4 reappointment list and the September 16 paraprofessional list (the latter PDF carries names and stays outside the repository); `health-rates-table.py` reproduces the premium comparison from two years of June minutes; `check-site.sh` builds the site locally and checks the ledger pages render and nothing private is published
- dated notes — what was found, when, and whether it was checked against the original
