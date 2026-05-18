#!/usr/bin/env bash
# pipeline/scripts/check-attack-entry.sh <ATTACKS/path.md>
# Verifies an ATTACKS entry has frontmatter + 5 template sections (per content-drafter.md).
set -e
F="${1:-}"
[ -f "$F" ] || { echo "FAIL: $F not found"; exit 1; }
issues=0
fm=$(awk '/^---$/{c++; next} c==1' "$F")
for k in title class lane affected_systems disclosure_status disclosure_target date; do
  echo "$fm" | grep -q "^$k:" || { echo "FAIL: frontmatter missing '$k'"; issues=$((issues+1)); }
done
for s in "## Threat model" "## Scenario" "## Proof of concept" "## Result" "## Mitigation"; do
  grep -q "^$s" "$F" || { echo "FAIL: section missing '$s'"; issues=$((issues+1)); }
done
status=$(echo "$fm" | grep '^disclosure_status:' | awk '{print $2}' | tr -d '"')
case "$status" in green|yellow|red) ;; *) echo "FAIL: invalid disclosure_status='$status'"; issues=$((issues+1));; esac
[ $issues -eq 0 ] && echo "PASS: $F" || { echo "FAIL: $issues issue(s)"; exit 1; }
