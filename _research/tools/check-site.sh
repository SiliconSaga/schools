#!/usr/bin/env bash
# Builds the site without the remote theme (no layout, content only) and checks that the
# ledger renders from its data files and that nothing private is published.
# Usage: bash _research/tools/check-site.sh   (from anywhere; needs the jekyll 3.10.0 gem)
set -uo pipefail
cd "$(dirname "$0")/../.."
out="$(mktemp -d)"
log="$out.log"
if ! jekyll _3.10.0_ build --destination "$out" > "$log" 2>&1; then
  cat "$log"
  echo "FAIL build"
  exit 1
fi
fail=0
for f in index.html ledger/index.html ledger/timeline.html ledger/statements.html \
         ledger/opra/index.html ledger/opra/001-edustaff.html ledger/opra/002-coverage.html \
         spring-2026.html; do
  [ -f "$out/$f" ] || { echo "MISSING $f"; fail=1; }
done
[ ! -e "$out/_research" ] || { echo "LEAK _research is published"; fail=1; }
grep -q "Liquid" "$log" && { echo "LIQUID warning or error:"; grep "Liquid" "$log"; fail=1; }
grep -q "EduStaff Pricing Schedule" "$out/ledger/timeline.html" || { echo "timeline data not rendered"; fail=1; }
grep -q "OPRA-002" "$out/ledger/opra/index.html" || { echo "request table not rendered"; fail=1; }
grep -q "OPRA-001" "$out/ledger/index.html" || { echo "request table missing on ledger home"; fail=1; }
grep -q "{{" "$out/ledger/opra/001-edustaff.html" && { echo "unrendered Liquid in request page"; fail=1; }
grep -rlE "@gmail\.com" "$out" --include="*.html" && { echo "LEAK personal email in pages above"; fail=1; }
echo "entries on timeline: $(grep -c "<h3" "$out/ledger/timeline.html")"
[ "$fail" -eq 0 ] && echo "OK site checks passed ($out)"
exit "$fail"
