#!/usr/bin/env bash
# cost_guard.sh — enforce monthly spend caps for Tier A track research calls.
# Usage: wrap any lab-run invocation: bash lab/mcp-matrix/scripts/cost_guard.sh <command> [args...]
# Exits 0 if under cap, 1 if warning zone, 2 if hard stop exceeded.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
CALLS_LOG="${REPO_ROOT}/docs/research/_calls.jsonl"

WARN_THRESHOLD=200.00   # emit warning, continue
HARD_THRESHOLD=280.00   # block new frontier calls (non-ollama)

total_spent=$(jq -s 'map(.cost_usd) | add // 0' "$CALLS_LOG" 2>/dev/null || echo "0")
total_spent_rounded=$(printf "%.2f" "$total_spent")

if (( $(echo "$total_spent >= $HARD_THRESHOLD" | bc -l) )); then
  echo "🚫 COST HARD STOP: total spent ${total_spent_rounded} exceeds $HARD_THRESHOLD. Refusing to proceed."
  exit 2
elif (( $(echo "$total_spent >= $WARN_THRESHOLD" | bc -l) )); then
  echo "⚠️  COST WARNING: total spent ${total_spent_rounded} is above $WARN_THRESHOLD. Proceed with caution."
  exit 1
else
  echo "✅ COST OK: total spent ${total_spent_rounded} under $WARN_THRESHOLD."
  exit 0
fi
