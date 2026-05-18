# Start Here for Hiring Reviewers

**Date:** 2026-05-17
**Status:** reviewer-ready
**Audience:** Recruiters, hiring managers, and technical interviewers.

## 60-Second Path

1. **Substrate vs policy:** [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) proves the original model-policy attribution was wrong, matters because it isolates client dispatch substrate as the load-bearing variable, and is bounded to measured MCP-style inline-XML versus typed-tool-call substrates.
2. **F1 / H7 falsification:** [`ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md`](../ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md) proves a pre-registered cross-scale hypothesis failed at 70B, matters because capability amplified exploitation inside the insecure substrate, and is bounded to one payload, one client class, and n=10.
3. **DVL Scenario 2:** [`ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md`](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md) proves ReAct-loop observation injection can drive SQL exfiltration in a vulnerable agent benchmark, matters because it translates to tool-boundary mitigations, and is bounded to localhost lab evidence.

For a runnable public-safe proof path:

```bash
make repro
make benchmark
```

For the attack-to-fix story, read [`REPORTS/remediation-case-study-tool-output-injection.md`](remediation-case-study-tool-output-injection.md).

For deeper review, continue to [`docs/reports/hiring-reviewer-map.md`](../docs/reports/hiring-reviewer-map.md) and [`docs/reports/hiring-evidence-index.md`](../docs/reports/hiring-evidence-index.md).

## Role-Specific Evidence Blocks

| Role | Flagship artifact | Raw evidence / pre-registration | Defensive / operational artifact |
|---|---|---|---|
| Frontier red-team / preparedness | [`ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md`](../ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md) | [`docs/preregistrations/2026-05-13-tier-a-w1-w5.md`](../docs/preregistrations/2026-05-13-tier-a-w1-w5.md) | [`REPORTS/substrate-vs-policy-assessment.md`](substrate-vs-policy-assessment.md) |
| Agent security / tool-use security | [`ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md`](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md) | [`lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/wilson_summary.json`](../lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/wilson_summary.json) | [`DETECTIONS/tool-chain-detections.md`](../DETECTIONS/tool-chain-detections.md) |
| AI evals / research engineering | [`EVALS/agent-tool-output-injection-benchmark.md`](../EVALS/agent-tool-output-injection-benchmark.md) | [`docs/preregistrations/2026-mcp-matrix.md`](../docs/preregistrations/2026-mcp-matrix.md) | [`lab/mcp-matrix/tools/README.md`](../lab/mcp-matrix/tools/README.md) |
| Product security / MLSecOps | [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) | [`ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md`](../ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md) | [`REPORTS/remediation-case-study-tool-output-injection.md`](remediation-case-study-tool-output-injection.md) |
| Security consulting | [`WRITEUPS/2026-05-14-cross-model-react-loop-injection.md`](../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md) | [`docs/reports/hiring-evidence-index.md`](../docs/reports/hiring-evidence-index.md) | [`REPORTS/remediation-case-study-tool-output-injection.md`](remediation-case-study-tool-output-injection.md) |

## Use Boundary

H10b-G is still in progress and not packet-ready. Do not quote H10b-G rates or use its interim report in applications until the full grid completes and the control-validity gate clears.
