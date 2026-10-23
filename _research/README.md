# Research workbench

Working notes, drafts, and source copies behind the site. Jekyll skips folders that start with an underscore, so nothing here appears on the site itself, but the repository is public and everything here is deliberately so: the owner keeps the research trail in the open, and anything that should not be public does not belong in this folder.

- `opra/` — owner notes on each request, the filing steps (`filing.md`), and the requester-details template; the request texts themselves are in `_includes/opra/`, shared by the ledger pages and the printed letters
- `sources/` — copies of district documents the notes cite, saved against link rot
- `tools/` — small helpers: `pdfgrep.py` prints PDF text around a search pattern (needs `pypdf`); `opra-print.py` renders the request letters to PDF for filing; `longevity-tally.py` and `para-list-tally.py` reproduce the counts the ledger cites from the May 4 reappointment list and the September 16 paraprofessional list (the latter PDF carries names and stays outside the repository); `health-rates-table.py` reproduces the premium comparison from two years of June minutes; `check-site.sh` builds the site locally and checks the ledger pages render and nothing private is published
- `agents/` — raw notes from research agents; each source block is labelled [fetched], [snippet], or NOT VERIFIED with its URL, and summary bullets inherit the weakest label of what they draw on; nothing in them reaches a page until it has been re-read at the source
- dated notes — what was found, when, and whether it was checked against the original; the ones marked draft research are thinking in progress, not plans or proposals
