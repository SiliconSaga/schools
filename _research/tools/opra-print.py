"""
Render the OPRA request letters for filing.
Usage: python _research/tools/opra-print.py [OPRA-001 ...]
Reads the request texts from _includes/opra/<slug>.md (the same files the ledger pages include),
the request list from _data/opra.yml, and the requester's details from _research/opra/requester.yml.
Writes _research/opra/out/<id>-<name>.pdf (and the .html it was printed from) using Microsoft Edge
in headless mode. Needs the `markdown` and `pyyaml` modules.
"""

import datetime
import html
import os
import subprocess
import sys

import markdown
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REQUESTER = os.path.join(ROOT, "_research", "opra", "requester.yml")
OUT_DIR = os.path.join(ROOT, "_research", "opra", "out")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

ADDRESSEE = [
    "Custodian of Records",
    "West Orange Board of Education",
    "Business Office",
    "179 Eagle Rock Avenue",
    "West Orange, NJ 07052",
]

CSS = """
@page { size: Letter; margin: 1in; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 11.5pt; line-height: 1.4; color: #000; }
.block { margin-bottom: 1.4em; white-space: pre-line; }
.re { font-weight: bold; margin-bottom: 1.4em; }
ol li, ul li { margin-bottom: 0.5em; }
.sign { margin-top: 2.5em; }
.sign .space { height: 3.5em; }
"""


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def long_date(iso):
    d = datetime.date.fromisoformat(str(iso))
    return f"{d:%B} {d.day}, {d.year}"


def letter_html(req, who):
    with open(os.path.join(ROOT, "_includes", "opra", req["slug"] + ".md"), encoding="utf-8") as f:
        body = markdown.markdown(f.read())
    sender = "\n".join(html.escape(x) for x in [
        who["name"], who["address_line1"], who["address_line2"], who["email"], who["phone"],
    ])
    addressee = "\n".join(html.escape(x) for x in ADDRESSEE)
    subject = html.escape(f'OPRA request: {req["title"]} (requester reference {req["id"]})')
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>{subject}</title><style>{CSS}</style></head>
<body>
<div class="block">{sender}</div>
<div class="block">{long_date(who["date"])}</div>
<div class="block">{addressee}</div>
<div class="re">Re: {subject}</div>
<p>Dear Custodian of Records,</p>
{body}
<p>Please confirm receipt of this request. Thank you.</p>
<div class="sign">Sincerely,<div class="space"></div>{html.escape(who["name"])}<br>{html.escape(who["email"])}<br>{html.escape(who["phone"])}</div>
</body></html>
"""


def print_pdf(html_path, pdf_path):
    if not os.path.exists(EDGE):
        sys.exit(f"Edge not found at {EDGE}; open the .html in a browser and print it to PDF instead")
    profile = os.path.join(OUT_DIR, ".edge-profile")
    subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-first-run",
        f"--user-data-dir={profile}", "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}", "file:///" + html_path.replace(os.sep, "/"),
    ], check=True, timeout=120, capture_output=True)


def main():
    if not os.path.exists(REQUESTER):
        sys.exit(f"missing {REQUESTER}; copy requester.example.yml and fill it in")
    who = load_yaml(REQUESTER)
    missing = [k for k in ("name", "address_line1", "address_line2", "email", "phone", "date")
               if not who.get(k) or str(who[k]).startswith("[")]
    if missing:
        print(f"WARNING placeholder or empty field(s) in requester.yml: {', '.join(missing)}")
    wanted = set(sys.argv[1:])
    os.makedirs(OUT_DIR, exist_ok=True)
    for req in load_yaml(os.path.join(ROOT, "_data", "opra.yml")):
        if wanted and req["id"] not in wanted:
            continue
        base = os.path.join(OUT_DIR, f'{req["id"]}-{req["slug"].split("-", 1)[1]}')
        with open(base + ".html", "w", encoding="utf-8") as f:
            f.write(letter_html(req, who))
        print_pdf(base + ".html", base + ".pdf")
        print(f'{req["id"]}: {base}.pdf')


if __name__ == "__main__":
    main()
