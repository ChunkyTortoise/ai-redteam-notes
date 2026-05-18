#!/usr/bin/env bash
# Pre-publication verification for hiring-facing artifacts.

set -euo pipefail
cd "$(dirname "$0")/../.."

public_files=(
  README.md
  REPRODUCE.md
  RESEARCH-SUMMARY.md
  Makefile
  site/index.html
  REPORTS/start-here-for-hiring-reviewers.md
  REPORTS/substrate-vs-policy-assessment.md
  REPORTS/2026-05-17-h10b-g-70b-substrate-findings.md
  REPORTS/remediation-case-study-tool-output-injection.md
  docs/reports/hiring-reviewer-map.md
  docs/reports/hiring-evidence-index.md
  docs/preregistrations/2026-05-16-open-source-scale-substrate-h10b.md
  EVALS/agent-tool-output-injection-benchmark.md
  EVALS/score_tool_output_injection.py
  EVALS/fixtures/tool-output-injection-fixtures.json
  DETECTIONS/README.md
  DETECTIONS/tool-chain-detections.md
  DETECTIONS/mock-incident-triage-tool-output-injection.md
  lab/mcp-matrix/tools/README.md
  lab/mcp-matrix/tools/substrate_auditor.py
  lab/mcp-matrix/tools/selfcheck.py
  lab/mcp-matrix/tools/samples/cline-sample.json
  lab/mcp-matrix/tools/samples/kilo-sample.json
  lab/mcp-matrix/tools/samples/before-inline-xml-transcript.jsonl
  lab/mcp-matrix/tools/samples/after-typed-toolcall-transcript.jsonl
)
evidence_files=(
  lab/mcp-matrix/runs/2026-05-16-cline-70b-M0-f1/seeds.json
  lab/mcp-matrix/runs/2026-05-17-llama70b-xml-M0-v3/seeds.json
  lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v3/seeds.json
  lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v7/seeds.json
  lab/mcp-matrix/runs/2026-05-18-llama70b-chatonly-M0-baseline/seeds.json
  lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/success.json
  lab/mcp-matrix/runs/2026-05-12-kilocode-M0/success.json
  lab/mcp-matrix/runs/2026-05-10-llama-xml-M1-v7-dispatch-all-tags/success.json
  lab/mcp-matrix/runs/2026-05-09-llama-xml-M2/success.json
  lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/wilson_summary.json
)
writeup_files=(
  WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md
)
attack_files=(
  ATTACKS/2026-05-03-indirect-injection-tool-description.md
  ATTACKS/2026-05-04-pair-llama31-persona-dan.md
  ATTACKS/2026-05-04-pair-matrix-llama31-vs-mistral7b.md
  ATTACKS/2026-05-10-substrate-amplification-mcp-tool-output.md
  ATTACKS/2026-05-12-dvl-agent-promptfoo-baseline.md
  ATTACKS/2026-05-13-pair-matrix-m0-claude-desktop-negative.md
  ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md
  ATTACKS/2026-05-15-mcp-xml-last-tag-dispatch-ablation.md
  ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md
  ATTACKS/2026-05-16-open-source-scale-substrate-h10b.md
  ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md
)
public_scan_files=("${public_files[@]}" "${evidence_files[@]}" "${writeup_files[@]}" "${attack_files[@]}")

for required in "${public_files[@]}"; do
  [ -f "$required" ] || { echo "FAIL: missing public artifact $required"; exit 1; }
done
for required in "${writeup_files[@]}"; do
  [ -f "$required" ] || { echo "FAIL: missing public artifact $required"; exit 1; }
done
for required in "${evidence_files[@]}"; do
  [ -f "$required" ] || { echo "FAIL: missing public evidence artifact $required"; exit 1; }
done

if find REPORTS docs/reports EVALS DETECTIONS -type f -name '2026-05-31*' | grep -q .; then
  echo "FAIL: future-dated public artifact names found"
  find REPORTS docs/reports EVALS DETECTIONS -type f -name '2026-05-31*'
  exit 1
fi

if grep -RInE '2026-05-31|Status:\s*(public-safe draft|draft-reviewer-ready|draft-review-required)' "${public_scan_files[@]}"; then
  echo "FAIL: future-dated or draft status text found in public surface"
  exit 1
fi

if grep -RInE 'H10b-G[^.]*((still )?in progress|not packet-ready|excluded from packet-ready|no H10b-G rates|Do not quote|do not quote)' "${public_scan_files[@]}"; then
  echo "FAIL: stale H10b-G gating language found in public surface"
  exit 1
fi

if git ls-files | grep -E '(__pycache__/|\.pyc$)' >/dev/null; then
  echo "FAIL: generated Python cache files are tracked"
  git ls-files | grep -E '(__pycache__/|\.pyc$)'
  exit 1
fi

if find REPORTS docs/reports EVALS DETECTIONS lab/mcp-matrix/tools -type d \( -name __pycache__ -o -name .pytest_cache \) | grep -q .; then
  echo "FAIL: generated cache directories are present in public sync candidates"
  find REPORTS docs/reports EVALS DETECTIONS lab/mcp-matrix/tools -type d \( -name __pycache__ -o -name .pytest_cache \)
  exit 1
fi

make repro
make remediation-demo
make benchmark
if [ -f pyproject.toml ]; then
  make test
else
  echo "SKIP: private pytest harness not present in this public mirror checkout"
fi

for f in "${attack_files[@]}"; do
  bash pipeline/scripts/check-attack-entry.sh "$f"
  bash pipeline/scripts/check-disclosure.sh "$f"
done

bash pipeline/scripts/check-secrets.sh --all "${public_scan_files[@]}" EVALS/fixtures/tool-output-injection-fixtures.json
bash pipeline/scripts/check-local-links.sh "${public_scan_files[@]}"
bash pipeline/scripts/check-public-urls.sh "${public_scan_files[@]}"

echo "GATE: PASS - public hiring surface verified"
