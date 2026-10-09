"""Print a compact summary of a page-audit workflow result (JSON with a `pages` list).

Usage: python audit-summary.py <result.json> [mode] [output file]
Modes for the audit result: table (default), concerns, decisions, verify.
Modes for the correction-pass result: applied, open.
With an output file the summary is written there instead of printed.
"""
import json
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)
data = json.load(open(sys.argv[1], encoding="utf-8"))
data = data.get("result", data)
mode = sys.argv[2] if len(sys.argv) > 2 else "table"
pages = data["pages"]
OUT_FILE = open(sys.argv[3], "w", encoding="utf-8", newline="\n") if len(sys.argv) > 3 else None


def out(text):
    if OUT_FILE:
        OUT_FILE.write(text + "\n")
    else:
        print(text.encode("ascii", "replace").decode())


if mode == "applied":
    tot_a = tot_n = 0
    for p in pages:
        tot_a += p.get("applied", 0)
        tot_n += p.get("not_applied", 0)
        out(f"{p['key']:34} applied {p.get('applied', 0):3}  not {p.get('not_applied', 0):3}  banner: {p.get('banner', '-')}")
        for h in p.get("high_not_applied", []):
            out(f"    HIGH OPEN  {h}")
    out(f"TOTAL applied {tot_a}, not applied {tot_n}; failed: {data.get('failed')}")
elif mode == "open":
    for p in pages:
        if p.get("open_questions"):
            out(f"\n## {p['key']}")
            for q in p["open_questions"]:
                out(f"- {q}")
elif mode == "table":
    out(f"{'page':34} high med low | links dead blocked unsupp | verify C/R/U")
    tot = [0] * 10
    for p in pages:
        a, v = p["audit"], p.get("verify") or {}
        row = [a.get("high", 0), a.get("medium", 0), a.get("low", 0), a.get("links_total", 0), a.get("links_dead", 0),
               a.get("links_blocked", 0), a.get("links_not_supporting", 0),
               v.get("confirmed", 0), v.get("refuted", 0), v.get("uncertain", 0)]
        tot = [t + r for t, r in zip(tot, row, strict=True)]
        out(f"{a['key']:34} {row[0]:4} {row[1]:3} {row[2]:3} | {row[3]:5} {row[4]:4} {row[5]:7} {row[6]:6} | "
            f"{v.get('confirmed', '-')}/{v.get('refuted', '-')}/{v.get('uncertain', '-')}")
    out(f"{'TOTAL':34} {tot[0]:4} {tot[1]:3} {tot[2]:3} | {tot[3]:5} {tot[4]:4} {tot[5]:7} {tot[6]:6} | {tot[7]}/{tot[8]}/{tot[9]}")
    out(f"failed: {data.get('failed')}")
elif mode == "concerns":
    for p in pages:
        a = p["audit"]
        out(f"\n## {a['key']} (high {a.get('high', 0)}, medium {a.get('medium', 0)})")
        for c in a.get("top_concerns", []):
            out(f"- {c}")
elif mode == "decisions":
    for p in pages:
        a = p["audit"]
        if a.get("owner_decisions"):
            out(f"\n## {a['key']}")
            for c in a["owner_decisions"]:
                out(f"- {c}")
elif mode == "verify":
    for p in pages:
        v = p.get("verify")
        if v:
            out(f"\n## {p['audit']['key']}: C{v.get('confirmed', 0)} R{v.get('refuted', 0)} U{v.get('uncertain', 0)} refuted={v.get('refuted_ids', [])}")
            out(f"  {v.get('notes', '')}")
else:
    sys.exit(f"unknown mode: {mode}\n{__doc__}")
