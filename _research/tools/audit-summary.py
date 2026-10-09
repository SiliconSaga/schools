"""Print a compact summary of the page-audit workflow result (a JSON file with a `pages` list).

Usage: python audit-summary.py <result.json> [table|concerns|decisions|verify]
"""
import json
import sys

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
        tot_a += p["applied"]
        tot_n += p["not_applied"]
        out(f"{p['key']:34} applied {p['applied']:3}  not {p['not_applied']:3}  banner: {p['banner']}")
        for h in p["high_not_applied"]:
            out(f"    HIGH OPEN  {h}")
    out(f"TOTAL applied {tot_a}, not applied {tot_n}; failed: {data.get('failed')}")
elif mode == "open":
    for p in pages:
        if p["open_questions"]:
            out(f"\n## {p['key']}")
            for q in p["open_questions"]:
                out(f"- {q}")
elif mode == "table":
    out(f"{'page':34} high med low | links dead blocked unsupp | verify C/R/U")
    tot = [0] * 9
    for p in pages:
        a, v = p["audit"], p.get("verify") or {}
        row = [a["high"], a["medium"], a["low"], a["links_total"], a["links_dead"], a.get("links_blocked", 0),
               a["links_not_supporting"], v.get("confirmed", 0), v.get("refuted", 0)]
        tot = [t + r for t, r in zip(tot, row)]
        out(f"{a['key']:34} {row[0]:4} {row[1]:3} {row[2]:3} | {row[3]:5} {row[4]:4} {row[5]:7} {row[6]:6} | "
            f"{v.get('confirmed', '-')}/{v.get('refuted', '-')}/{v.get('uncertain', '-')}")
    out(f"{'TOTAL':34} {tot[0]:4} {tot[1]:3} {tot[2]:3} | {tot[3]:5} {tot[4]:4} {tot[5]:7} {tot[6]:6} | {tot[7]}/{tot[8]}")
    out(f"failed: {data.get('failed')}")
elif mode == "concerns":
    for p in pages:
        a = p["audit"]
        out(f"\n## {a['key']} (high {a['high']}, medium {a['medium']})")
        for c in a["top_concerns"]:
            out(f"- {c}")
elif mode == "decisions":
    for p in pages:
        a = p["audit"]
        if a["owner_decisions"]:
            out(f"\n## {a['key']}")
            for c in a["owner_decisions"]:
                out(f"- {c}")
elif mode == "verify":
    for p in pages:
        v = p.get("verify")
        if v:
            out(f"\n## {p['audit']['key']}: C{v['confirmed']} R{v['refuted']} U{v['uncertain']} refuted={v['refuted_ids']}")
            out(f"  {v['notes']}")
