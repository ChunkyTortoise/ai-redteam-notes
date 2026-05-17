# ai-redteam reproduce / audit entrypoints.
# Mirror-safe: selfcheck, audit, repro depend only on python3 + stdlib and the
# substrate auditor, so they run identically in the public mirror and in CI.
# `test` runs the full private pre-registered harness suite (private repo only).

# Use uv locally (project shim requires it); plain python3 on clean CI runners.
PY := $(shell command -v uv >/dev/null 2>&1 && echo "uv run python3" || echo "python3")
AUDITOR := lab/mcp-matrix/tools/substrate_auditor.py
SAMPLES := lab/mcp-matrix/tools/samples

.PHONY: help repro selfcheck audit test

help:
	@echo "make repro      - 60-second reviewer path: selfcheck + auditor demo (no install)"
	@echo "make selfcheck  - dependency-free substrate_auditor self-check"
	@echo "make audit      - run the defensive substrate auditor on the sample configs"
	@echo "make test       - full pre-registered harness pytest suite (private repo)"

selfcheck:
	$(PY) lab/mcp-matrix/tools/selfcheck.py

audit:
	@echo "== risky (Cline / inline-xml) =="
	-$(PY) $(AUDITOR) $(SAMPLES)/cline-sample.json
	@echo
	@echo "== safe (Kilo Code / typed API) =="
	$(PY) $(AUDITOR) $(SAMPLES)/kilo-sample.json

repro: selfcheck audit
	@echo
	@echo "Reviewer path: RESEARCH-SUMMARY.md -> WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md (Addendum B)"
	@echo "Strongest single result: ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md"
	@echo "Full pre-registered harness suite lives in the private repo (make test):"
	@echo "40 passed, 0 failed. See REPRODUCE.md for the verdict canary-sourcing fix."

test:
	$(PY) -m pytest lab/mcp-matrix/harness/tests -q
