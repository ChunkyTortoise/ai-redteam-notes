#!/usr/bin/env bash
# pipeline/scripts/check-public-urls.sh [files...]
# Optional network check for public GitHub URLs before applications, posting, or public sync.

set -euo pipefail
cd "$(dirname "$0")/../.."

if [ "$#" -gt 0 ]; then
  files=("$@")
else
  files=(
    pipeline/applications/packets/*.md
    pipeline/applications/social/2026-05-15-linkedin-post-04-substrate-vs-policy.md
    pipeline/applications/social/2026-05-16-linkedin-post-05-portfolio-upgrade.md
    pipeline/applications/social/2026-05-17-linkedin-post-06-cvd-ready.md
    pipeline/applications/social/2026-05-21-linkedin-post-10-agent-observation.md
    pipeline/reports/public-sync-candidates/*.md
  )
fi

tmp_urls=$(mktemp "${TMPDIR:-/tmp}/ai-redteam-public-urls.XXXXXX")
trap 'rm -f "$tmp_urls"' EXIT

for file in "${files[@]}"; do
  [ -f "$file" ] || continue
  grep -Eoh "https://github.com/ChunkyTortoise/ai-redteam-notes[^) >\"']+" "$file" \
    | sed 's/[.,;]*$//' >> "$tmp_urls" || true
done

sort -u "$tmp_urls" -o "$tmp_urls"

if [ ! -s "$tmp_urls" ]; then
  echo "FAIL: no public GitHub URLs found"
  exit 1
fi

issues=0
while IFS= read -r url; do
  if curl -fsSIL --max-time 15 "$url" >/dev/null; then
    echo "OK: $url"
  else
    echo "BROKEN: $url"
    issues=$((issues + 1))
  fi
done < "$tmp_urls"

if [ "$issues" -eq 0 ]; then
  echo "GATE: PASS - public GitHub URLs resolved"
  exit 0
fi

echo "GATE: FAIL - $issues broken URL(s)"
exit 1
