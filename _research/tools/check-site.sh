#!/usr/bin/env bash
# Builds the site without the remote theme (no layout, content only) and checks that the
# ledger renders from its data files and that nothing private is published.
# Usage: bash _research/tools/check-site.sh   (from anywhere; needs the jekyll 3.10.0 gem)
# The build directory is removed on success and kept, with its path printed, on failure.
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1
out="$(mktemp -d)"
log="$out.log"
cleanup() { rm -rf "$out" "$log"; }
if ! jekyll _3.10.0_ build --destination "$out" > "$log" 2>&1; then
  cat "$log"
  echo "FAIL build (output kept in $out)"
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
# Any email address in the built site must belong to a domain that is meant to be public.
allowed='@(frontstate\.org|westorangeschools\.org|woboe\.org|doe\.nj\.gov|nj\.gov)$'
leaks="$(grep -rhoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' "$out" --include='*.html' --include='*.xml' --include='*.json' --include='*.txt' | sort -u | grep -vE "$allowed")"
[ -z "$leaks" ] || { echo "LEAK email address(es) in built site:"; echo "$leaks"; fail=1; }
echo "entries on timeline: $(grep -c "<h3" "$out/ledger/timeline.html")"
if [ "$fail" -eq 0 ]; then
  echo "OK site checks passed"
  cleanup
else
  echo "FAIL (output kept in $out)"
fi
exit "$fail"
