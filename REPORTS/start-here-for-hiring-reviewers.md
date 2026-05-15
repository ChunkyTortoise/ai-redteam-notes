# Start Here For Hiring Reviewers

**Status:** public
**Purpose:** give a hiring reviewer a fast, conservative path through the strongest AI red-team evidence.

## Claim Boundary

This portfolio shows lab-only, disclosure-green agent-security evaluation work: small-scope experiments, synthetic canaries, localhost sinks, preserved artifacts, and conservative limitations. It does not claim a production exploit, a vendor-specific vulnerability, or a general result across all models and clients.

## If You Know The Role

Jump to the [By-Role Reviewer Guide](by-role-reviewer-guide.md). It points you at the strongest two or three artifacts in reading order for OpenAI Agent Products, DeepMind agent security or frontier safety, Lakera delivery, Anthropic / Microsoft AIRT, and a reusable eval engineer.

## Pre-empted Question

If you're about to ask "did you test on frontier models?" — the answer is in [Open-Weights Rationale](open-weights-rationale.md). Short version: substrate findings are expected to be transparent to model scale; open-weight cells are reproducible by any reader without per-call API spend.

## 60-Second Path

1. **Substrate vs policy writeup**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md>
   - Why it matters: shows pre-registration, attribution correction, and a defender-focused client-boundary conclusion.
2. **DVL Scenario 2 ATTACKS entry**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md>
   - Why it matters: concrete ReAct-loop observation-injection evidence with a practical mitigation lesson.
3. **Agent product security remediation review**
   - Public artifact: [`2026-05-15-agent-product-security-remediation-review.md`](2026-05-15-agent-product-security-remediation-review.md)
   - Why it matters: code-review-style artifact covering vulnerable boundary, exploitability, impact, durable fix, regression test, and residual risk.

## 5-Minute Path

- Hiring evidence index: [`hiring-evidence-index.md`](hiring-evidence-index.md)
- Claim ledger: [`claim-ledger.md`](claim-ledger.md)
- Substrate assessment report: [`substrate-vs-policy-assessment.md`](substrate-vs-policy-assessment.md)
- Agent-security eval methodology: [`2026-05-14-agent-security-eval-methodology.md`](2026-05-14-agent-security-eval-methodology.md)
- Negative-result note: [`2026-05-14-mcp-n10-replication-negative-result.md`](2026-05-14-mcp-n10-replication-negative-result.md)

## 20-Minute Path

- Evidence traceability manifest: [`2026-05-14-evidence-traceability-manifest.md`](2026-05-14-evidence-traceability-manifest.md)
- MCP matrix reviewer checklist: [`mcp-reproducibility-checklist.md`](mcp-reproducibility-checklist.md)
- MCP matrix README: [`../lab/mcp-matrix/README.md`](../lab/mcp-matrix/README.md)
- Preserved n=10 run summary: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md)
- Preserved n=10 run command: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md)

## What To Look For

- Clear separation between strict bypass, intent shift, clean ignore, and harness failure.
- Claims that narrow after replication rather than inflate.
- Raw artifacts that preserve commands, summaries, transcripts, and limitations.
- Remediation language aimed at engineering controls: typed tool schemas, parser hardening, provenance, confirmation flow, logging, replay, parameterized tool boundaries, and regression tests.

## What Not To Infer

- Do not infer production exploitability.
- Do not infer a universal MCP vulnerability.
- Do not infer frontier-model benchmark rates.
- Do not treat small-n mechanism evidence as population-level prevalence.
