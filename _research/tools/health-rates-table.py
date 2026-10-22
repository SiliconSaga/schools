"""
Read the "Health Benefits Costs" resolution in two sets of West Orange Board minutes (the June
meetings, where the Board approves the next school year's monthly premium rates) and print the
rates side by side with the percentage change, as a Markdown table.
Sources: June 16, 2025 minutes, pp. 17-19, and June 16, 2026 minutes, pp. 23-25:
https://resources.finalsite.net/images/v1773255560/woboeorg/nnavnwaspbwtlzkilhp6/Minutes-June162025.pdf
https://resources.finalsite.net/images/v1784732860/woboeorg/jryunce7m2qtccixad76/June162026MINUTES.pdf
Each plan is a line naming the plan and the carrier ("SHIF - Aetna", "SHIF - Express Scripts",
"Delta"), followed by one line per coverage tier with a dollar amount. Needs pypdf 4 or later.
"""

import argparse
import re

from pypdf import PdfReader

PLAN = re.compile(r"^(?P<plan>.+?)\s{2,}(?P<carrier>SHIF - .+|Delta)\s*$")
TIER = re.compile(r"^(?P<tier>Single|Parent/Child\(ren\)|2 Adults|Family|Single\s*-\s*Dependent Age 31)\s+(?P<amount>\$[\d,]+\.\d\d|TBD)\s*$")
MAIN_PLANS = ("Open Access $10/$20", "HDHP-HRA", "NJ Educators Health Plan", "NJ Garden State Health Plan",
              "RX", "Rx - Educators Health Plan", "Rx - Garden State Health Plan", "Dental - High Option (Active Employees)")


def rates_from(pdf):
    """{plan: {tier: amount}} for every plan in the Health Benefits Costs resolution."""
    rates, plan, in_table = {}, None, False
    for page in PdfReader(pdf).pages:
        for raw in (page.extract_text(extraction_mode="layout") or "").splitlines():
            line = re.sub(r"\s{2,}", "  ", raw.strip())
            if "Health Benefits Costs" in line:
                in_table = True
            if not in_table:
                continue
            m = PLAN.match(line)
            if m:
                plan = m.group("plan")
                rates.setdefault(plan, {})
                continue
            m = TIER.match(line)
            if m and plan:
                amount = m.group("amount")
                tier = re.sub(r"\s*-\s*", "-", m.group("tier"))
                rates[plan][tier] = None if amount == "TBD" else float(amount[1:].replace(",", ""))
            elif plan and re.match(r"^\d+\.\s", line):
                in_table = False  # the next numbered resolution ends the table
    return rates


def main():
    """Print the earlier and later rates for each plan and tier, with the percentage change."""
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("earlier", help="minutes PDF for the earlier year")
    p.add_argument("later", help="minutes PDF for the later year")
    p.add_argument("--all", action="store_true", help="every plan in the resolution, not just the main ones")
    args = p.parse_args()
    a, b = rates_from(args.earlier), rates_from(args.later)
    plans = [x for x in b if args.all or x in MAIN_PLANS]
    print("| Plan | Tier | Earlier | Later | Change |")
    print("|---|---|---|---|---|")
    for plan in plans:
        for tier in ("Single", "Parent/Child(ren)", "2 Adults", "Family", "Single-Dependent Age 31"):
            x, y = a.get(plan, {}).get(tier), b.get(plan, {}).get(tier)
            if y is None:
                continue
            change = f"{(y / x - 1) * 100:+.1f}%" if x else "n/a"
            print(f"| {plan} | {tier} | {'' if x is None else f'${x:,.2f}'} | ${y:,.2f} | {change} |")


if __name__ == "__main__":
    main()
