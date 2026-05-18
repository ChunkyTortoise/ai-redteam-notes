#!/usr/bin/env bash
# pipeline/scripts/check-local-links.sh [files...]
# Verifies local Markdown links resolve from each source file's directory.

set -euo pipefail
cd "$(dirname "$0")/../.."

if [ "$#" -gt 0 ]; then
  files=("$@")
else
  files=(
    REPORTS/substrate-vs-policy-assessment.md
    docs/reports/*.md
    pipeline/reports/public-sync-candidates/*.md
    EVALS/*.md
    DETECTIONS/*.md
  )
fi

issues=0
checked=0

fail() {
  echo "FAIL: $*"
  issues=$((issues + 1))
}

pass() {
  echo "PASS: $*"
}

while IFS= read -r entry; do
  file="${entry%%	*}"
  rest="${entry#*	}"
  line="${rest%%	*}"
  url="${rest#*	}"

  case "$url" in
    http://*|https://*|mailto:*|\#*|"")
      continue
      ;;
  esac

  target="${url%%#*}"
  target="${target%%\?*}"

  case "$target" in
    /*)
      fail "$file:$line uses absolute local path '$url'"
      continue
      ;;
  esac

  [ -n "$target" ] || continue
  checked=$((checked + 1))

  resolved="$(dirname "$file")/$target"
  if [ -e "$resolved" ]; then
    continue
  fi

  fail "$file:$line has broken local link '$url' -> $resolved"
done < <(
  for file in "${files[@]}"; do
    [ -f "$file" ] || continue
    perl -ne 'while (/\[[^]]+\]\(([^)[:space:]]+)\)/g) { print "$ARGV\t$.\t$1\n" }' "$file"
  done
)

if [ "$checked" -eq 0 ]; then
  fail "no local Markdown links checked"
fi

if [ "$issues" -eq 0 ]; then
  pass "local Markdown links resolved ($checked checked)"
  echo "GATE: PASS - local report links resolve"
  exit 0
fi

echo "GATE: FAIL - $issues broken local link(s)"
exit 1
