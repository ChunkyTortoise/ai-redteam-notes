#!/usr/bin/env bash
# Validate reviewer/application packet-ready docs without publishing anything.

set -euo pipefail
cd "$(dirname "$0")/../.."

packet_files=(
  README.md
  REPRODUCE.md
  RESEARCH-SUMMARY.md
  REPORTS/start-here-for-hiring-reviewers.md
  REPORTS/remediation-case-study-tool-output-injection.md
  docs/reports/hiring-reviewer-map.md
  docs/reports/hiring-evidence-index.md
  EVALS/agent-tool-output-injection-benchmark.md
  lab/mcp-matrix/tools/README.md
)

for required in "${packet_files[@]}"; do
  [ -f "$required" ] || { echo "FAIL: missing packet-ready artifact $required"; exit 1; }
done

if grep -RInE '2026-05-31|Status:\s*(public-safe draft|draft-reviewer-ready|draft-review-required)' "${packet_files[@]}"; then
  echo "FAIL: future-dated or draft status text found in packet-ready docs"
  exit 1
fi

if grep -RInE '(/Users/|\.env|_burner)' "${packet_files[@]}"; then
  echo "FAIL: private path or sensitive operational marker found in packet-ready docs"
  exit 1
fi

if grep -RInE 'H10b-G[^.]*([0-9]+/[0-9]+|Wilson|OS70|CTRL)' "${packet_files[@]}"; then
  echo "FAIL: H10b-G rates or intervals are not packet-ready"
  exit 1
fi

python3 - <<'PY'
from __future__ import annotations

import re
import sys
from pathlib import Path

path = Path("REPORTS/start-here-for-hiring-reviewers.md")
text = path.read_text()

expected_roles = {
    "Frontier red-team / preparedness",
    "Agent security / tool-use security",
    "AI evals / research engineering",
    "Product security / MLSecOps",
    "Security consulting",
}

rows: dict[str, int] = {}
for line in text.splitlines():
    if not line.startswith("| ") or line.startswith("| Role ") or line.startswith("|---"):
        continue
    columns = [part.strip() for part in line.strip().strip("|").split("|")]
    if len(columns) != 4:
        continue
    role = columns[0]
    if role in expected_roles:
        rows[role] = len(re.findall(r"\[[^\]]+\]\([^)]+\)", line))

missing = sorted(expected_roles - rows.keys())
wrong_counts = {role: count for role, count in rows.items() if count != 3}
extra = sorted(set(rows) - expected_roles)

if missing or wrong_counts or extra:
    if missing:
        print(f"FAIL: missing role rows: {', '.join(missing)}")
    if wrong_counts:
        for role, count in sorted(wrong_counts.items()):
            print(f"FAIL: {role} has {count} links; expected exactly 3")
    if extra:
        print(f"FAIL: unexpected role rows: {', '.join(extra)}")
    sys.exit(1)

print("PASS: role-specific evidence blocks have exactly three links each")
PY

bash pipeline/scripts/check-secrets.sh --all "${packet_files[@]}"
bash pipeline/scripts/check-local-links.sh "${packet_files[@]}"
bash pipeline/scripts/check-public-urls.sh "${packet_files[@]}"

echo "GATE: PASS - reviewer packet docs are ready"
