# ai-redteam reproduce / audit / verification entrypoints.
# Mirror-safe: selfcheck, audit, repro depend only on python3 + stdlib and the
# substrate auditor, so they run identically in the public mirror and in CI.
# `test` runs the full private pre-registered harness suite (private repo only).

# Use uv locally (project shim requires it); plain python3 on clean CI runners.
# Disable bytecode writes so reviewer/public checks do not generate __pycache__.
PY := $(shell command -v uv >/dev/null 2>&1 && echo "PYTHONDONTWRITEBYTECODE=1 uv run python3" || echo "PYTHONDONTWRITEBYTECODE=1 python3")
AUDITOR := lab/mcp-matrix/tools/substrate_auditor.py
SAMPLES := lab/mcp-matrix/tools/samples

.PHONY: help repro selfcheck audit remediation-demo benchmark test packet-ready verify-public

help:
	@echo "make repro      - 60-second reviewer path: selfcheck + auditor demo (no install)"
	@echo "make selfcheck  - dependency-free substrate_auditor self-check"
	@echo "make audit      - run the defensive substrate auditor on the sample configs"
	@echo "make remediation-demo - show vulnerable vs mitigated substrate traces"
	@echo "make benchmark  - score fixture-only agent tool-output injection benchmark"
	@echo "make test       - full pre-registered harness pytest suite (private repo)"
	@echo "make packet-ready - validate reviewer/application packet-ready docs"
	@echo "make verify-public - pre-publication gate: repro, optional private tests, disclosure, links, secrets"

selfcheck:
	$(PY) lab/mcp-matrix/tools/selfcheck.py

audit:
	@echo "== risky (Cline / inline-xml) =="
	-$(PY) $(AUDITOR) $(SAMPLES)/cline-sample.json
	@echo
	@echo "== safe (Kilo Code / typed API) =="
	$(PY) $(AUDITOR) $(SAMPLES)/kilo-sample.json

remediation-demo:
	@echo "== before: inline XML dispatch transcript =="
	-$(PY) $(AUDITOR) $(SAMPLES)/before-inline-xml-transcript.jsonl
	@echo
	@echo "== after: structured tool-call transcript =="
	$(PY) $(AUDITOR) $(SAMPLES)/after-typed-toolcall-transcript.jsonl

repro: selfcheck audit
	@echo
	@echo "Reviewer path: REPORTS/start-here-for-hiring-reviewers.md -> WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md (Addendum B)"
	@echo "Strongest current result: ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md"
	@echo "Full pre-registered harness suite lives in the private repo (make test):"
	@echo "45 passed, 0 failed. See REPRODUCE.md for the verdict canary-sourcing fix."

benchmark:
	$(PY) EVALS/score_tool_output_injection.py EVALS/fixtures/tool-output-injection-fixtures.json

test:
	$(PY) -m pytest lab/mcp-matrix/harness/tests -q

packet-ready:
	bash pipeline/scripts/check-packet-ready.sh

verify-public:
	bash pipeline/scripts/verify-public.sh
