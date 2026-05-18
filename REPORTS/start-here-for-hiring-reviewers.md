# Start Here for Hiring Reviewers

**Date:** 2026-05-18
**Status:** reviewer-ready
**Audience:** Recruiters, hiring managers, and technical interviewers.

## 60-Second Path

1. **H10b-G mitigation boundary:** [`ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md`](../ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md) proves the 70B substrate effect survives the control gate and that the M1 scaffold is variant-selective: it holds baseline/v3 but fails on v7.
2. **Substrate vs policy:** [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) proves the original model-policy attribution was wrong, matters because it isolates client dispatch substrate as the load-bearing variable, and is bounded to measured MCP-style inline-XML versus typed-tool-call substrates.
3. **F1 / H7 falsification:** [`ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md`](../ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md) proves a pre-registered cross-scale hypothesis failed at 70B, matters because capability amplified exploitation inside the insecure substrate, and is bounded to one payload, one client class, and n=10.
4. **DVL Scenario 2:** [`ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md`](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md) proves ReAct-loop observation injection can drive SQL exfiltration in a vulnerable agent benchmark, matters because it translates to tool-boundary mitigations, and is bounded to localhost lab evidence.

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
| Frontier red-team / preparedness | [`ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md`](../ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md) | [`docs/preregistrations/2026-05-16-open-source-scale-substrate-h10b.md`](../docs/preregistrations/2026-05-16-open-source-scale-substrate-h10b.md) | [`REPORTS/2026-05-17-h10b-g-70b-substrate-findings.md`](2026-05-17-h10b-g-70b-substrate-findings.md) |
| Agent security / tool-use security | [`ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md`](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md) | [`lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/wilson_summary.json`](../lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/wilson_summary.json) | [`DETECTIONS/tool-chain-detections.md`](../DETECTIONS/tool-chain-detections.md) |
| AI evals / research engineering | [`EVALS/agent-tool-output-injection-benchmark.md`](../EVALS/agent-tool-output-injection-benchmark.md) | [`lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v7/seeds.json`](../lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v7/seeds.json) | [`lab/mcp-matrix/tools/README.md`](../lab/mcp-matrix/tools/README.md) |
| Product security / MLSecOps | [`ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md`](../ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md) | [`REPORTS/2026-05-17-h10b-g-70b-substrate-findings.md`](2026-05-17-h10b-g-70b-substrate-findings.md) | [`REPORTS/remediation-case-study-tool-output-injection.md`](remediation-case-study-tool-output-injection.md) |
| Security consulting | [`WRITEUPS/2026-05-14-cross-model-react-loop-injection.md`](../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md) | [`docs/reports/hiring-evidence-index.md`](../docs/reports/hiring-evidence-index.md) | [`REPORTS/remediation-case-study-tool-output-injection.md`](remediation-case-study-tool-output-injection.md) |

## Use Boundary

H10b-G is packet-ready but remains bounded: it is a lab-only, single-provider Groq-hosted Llama-3.3-70B grid. Do not describe it as the pristine frozen OpenRouter H10b run, a production exploit, or a frontier-model benchmark.
