#!/usr/bin/env bash
# Validate reviewer/application packet-ready docs without publishing anything.

set -euo pipefail
cd "$(dirname "$0")/../.."

# Use uv when available so the inline python3 check passes under a
# uv-enforcing python3 shim (mirrors the Makefile PY variable); falls
# back to plain python3 on clean CI runners / the public mirror.
if command -v uv >/dev/null 2>&1; then
  PY="uv run --no-project python3"
else
  PY="python3"
fi
export PYTHONDONTWRITEBYTECODE=1

packet_files=(
  README.md
  REPRODUCE.md
  RESEARCH-SUMMARY.md
  REPORTS/2026-05-17-h10b-g-70b-substrate-findings.md
  REPORTS/remediation-case-study-tool-output-injection.md
  REPORTS/claim-ledger.md
  EVALS/agent-tool-output-injection-benchmark.md
  EVALS/fixtures/tool-output-injection-fixtures.json
  lab/mcp-matrix/tools/README.md
  ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md
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

if grep -RInE 'H10b-G[^.]*((still )?in progress|not packet-ready|excluded from packet-ready|no H10b-G rates|Do not quote|do not quote)' "${packet_files[@]}"; then
  echo "FAIL: stale H10b-G gating language found in packet-ready docs"
  exit 1
fi

bash pipeline/scripts/check-secrets.sh --all "${packet_files[@]}"
bash pipeline/scripts/check-local-links.sh "${packet_files[@]}"
bash pipeline/scripts/check-public-urls.sh "${packet_files[@]}"

echo "GATE: PASS - core public docs are ready"
