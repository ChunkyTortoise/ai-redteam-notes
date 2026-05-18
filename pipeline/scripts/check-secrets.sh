#!/usr/bin/env bash
# Blocks obvious API key patterns from entering git history.
# Default mode scans staged changes. `--all [paths...]` scans tracked/untracked
# text files for the public verification gate.

set -euo pipefail
cd "$(dirname "$0")/../.."

pattern='(sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9_-]{40,}|gsk_[A-Za-z0-9_-]{20,})'

if [ "${1:-}" = "--all" ]; then
  shift
  if [ "$#" -gt 0 ]; then
    files=("$@")
  else
    files=()
    while IFS= read -r file; do
      files+=("$file")
    done < <(git ls-files -co --exclude-standard)
  fi

  issues=0
  for file in "${files[@]}"; do
    [ -f "$file" ] || continue
    if grep -IEn "$pattern" "$file" >/tmp/ai-redteam-secret-hit.$$ 2>/dev/null; then
      sed "s#^#$file:#" /tmp/ai-redteam-secret-hit.$$
      issues=$((issues + 1))
    fi
    rm -f /tmp/ai-redteam-secret-hit.$$
  done

  if [ "$issues" -eq 0 ]; then
    echo "GATE: PASS - no API key patterns found"
    exit 0
  fi
  echo "GATE: FAIL - $issues file(s) contain API key-like patterns"
  exit 1
fi

if git diff --cached -U0 | grep -qE "$pattern"; then
  echo "ERROR: API key pattern detected in staged changes - rotate and remove before committing"
  exit 1
fi
exit 0
