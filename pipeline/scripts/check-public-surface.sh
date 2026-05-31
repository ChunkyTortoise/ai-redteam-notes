#!/usr/bin/env bash
# Local-only public surface gate for the tracked public mirror.

set -euo pipefail
cd "$(dirname "$0")/../.."

if command -v uv >/dev/null 2>&1; then
  PY=(uv run python3)
else
  PY=(python3)
fi

issues=0

fail() {
  echo "FAIL: $*"
  issues=$((issues + 1))
}

pass() {
  echo "PASS: $*"
}

mapfile -t tracked_files < <(
  git ls-files | while IFS= read -r file; do
    [ -f "$file" ] && printf '%s\n' "$file"
  done
)
mapfile -t markdown_files < <(
  git ls-files '*.md' | while IFS= read -r file; do
    [ -f "$file" ] && printf '%s\n' "$file"
  done
)
mapfile -t content_files < <(
  git ls-files \
    | grep -E '(\.md|\.html|\.json|\.jsonl|\.ya?ml|Makefile)$' \
    | grep -Ev '^pipeline/scripts/' \
    | grep -Ev '^\.gitignore$' \
    | while IFS= read -r file; do
      [ -f "$file" ] && printf '%s\n' "$file"
    done
)

mapfile -t nested_mirror_files < <(
  git ls-files 'ai-redteam-notes/*' | while IFS= read -r file; do
    [ -e "$file" ] && printf '%s\n' "$file"
  done
)
if [ "${#nested_mirror_files[@]}" -gt 0 ]; then
  printf '%s\n' "${nested_mirror_files[@]}"
  fail "stale nested public mirror files are tracked under ai-redteam-notes/"
fi

if [ -f index.html ] && ! grep -q 'site/index.html' index.html; then
  fail "root index.html must be a stub pointing to site/index.html"
fi

if ! grep -q "path: 'site'" .github/workflows/pages.yml; then
  fail "GitHub Pages workflow must upload only the site/ directory"
fi

if git ls-files | grep -E '(__pycache__/|\.pyc$)' >/dev/null; then
  git ls-files | grep -E '(__pycache__/|\.pyc$)'
  fail "generated Python cache files are tracked"
fi

if find REPORTS docs EVALS DETECTIONS lab/mcp-matrix/tools site -type d \( -name __pycache__ -o -name .pytest_cache \) | grep -q .; then
  find REPORTS docs EVALS DETECTIONS lab/mcp-matrix/tools site -type d \( -name __pycache__ -o -name .pytest_cache \)
  fail "generated cache directories are present in public sync candidates"
fi

stale_h10bg='H10b-G[^.]*((still )?in progress|not packet-ready|excluded from packet-ready|no H10b-G rates|Do not quote|do not quote)'
if grep -InE "$stale_h10bg" "${content_files[@]}"; then
  fail "stale H10b-G gating language found in tracked public content"
fi

if grep -InE 'Status:[[:space:]]*(public-safe draft|draft-reviewer-ready|draft-review-required)' "${content_files[@]}"; then
  fail "draft status text found in tracked public content"
fi

# /Users/ must be followed by a path-like char (a real home path e.g. /Users/cave/...),
# so detection regexes like r'(~|/home/|/Users/)[^\s]+' (where /Users/ precedes a delimiter) pass.
private_marker='(/Users/[A-Za-z0-9._-]|_burner|_attic|_vendor|EnterpriseHub|routa\.db|\.mcp\.json|id_rsa|BEGIN (RSA|OPENSSH|PRIVATE) KEY)'
if grep -InE "$private_marker" "${content_files[@]}"; then
  fail "private path, workspace marker, or key-like marker found in tracked public content"
fi

today="${PUBLIC_SURFACE_TODAY:-$(date -u +%F)}"
"${PY[@]}" - "$today" "${content_files[@]}" <<'PY'
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

today = date.fromisoformat(sys.argv[1])
paths = [Path(p) for p in sys.argv[2:]]
date_re = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
issues: list[str] = []

metadata_date_re = re.compile(
    r"^\s*(?:date|last updated|\*\*date:\*\*|\*\*last updated:\*\*)"
    r"\s*:?\s*(20\d{2}-\d{2}-\d{2})\b",
    re.IGNORECASE,
)

for path in paths:
    haystacks = [(str(path), str(path))]
    try:
        lines = path.read_text(errors="ignore").splitlines()
    except OSError as exc:
        issues.append(f"{path}: could not read file: {exc}")
        continue

    for raw in date_re.findall(str(path)):
        observed = date.fromisoformat(raw)
        if observed > today:
            issues.append(f"{path}: future date {raw} in filename")

    for line_no, line in enumerate(lines, start=1):
        match = metadata_date_re.search(line)
        if not match:
            continue
        raw = match.group(1)
        observed = date.fromisoformat(raw)
        if observed > today:
            issues.append(f"{path}:{line_no}: future artifact date {raw}")

if issues:
    for issue in issues:
        print(f"FAIL: {issue}")
    raise SystemExit(1)

print(f"PASS: no artifact dates later than {today.isoformat()}")
PY

bash pipeline/scripts/check-secrets.sh --all "${tracked_files[@]}"
bash pipeline/scripts/check-local-links.sh "${markdown_files[@]}"

while IFS= read -r attack_file; do
  bash pipeline/scripts/check-disclosure.sh "$attack_file"
done < <(git ls-files 'ATTACKS/20*.md')

if [ "$issues" -eq 0 ]; then
  pass "tracked public surface passed local drift checks"
  echo "GATE: PASS - public surface is locally consistent"
  exit 0
fi

echo "GATE: FAIL - $issues public surface issue(s)"
exit 1
