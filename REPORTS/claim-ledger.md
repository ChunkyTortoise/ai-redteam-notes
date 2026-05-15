# Hiring Claim Ledger

**Status:** public
**Purpose:** keep portfolio claims auditable, conservative, and interview-ready.

| Claim | Evidence artifact | Raw run or command | Limitation | Interview phrasing | Do not claim |
|---|---|---|---|---|---|
| Client substrate can be the load-bearing variable in MCP tool-output indirect prompt injection. | <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md> | `cd lab/mcp-matrix && just test`; raw runs under [`../lab/mcp-matrix/runs/`](../lab/mcp-matrix/runs/) | Small-n, local harness, substrate-specific, open-weight model evidence. | "I corrected a tempting model-policy explanation after substrate isolation made the client dispatch path the cleaner explanation." | A general MCP vulnerability, a production exploit, or a universal client claim. |
| The May 14 n=10 replication narrowed the MCP claim rather than confirming reliable exfiltration. | [`2026-05-14-mcp-n10-replication-negative-result.md`](2026-05-14-mcp-n10-replication-negative-result.md) | [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md) | One model, one payload, one XML-style substrate emulation, n=10. | "The strict-bypass claim did not hold, so I kept the result as intent-layer eval evidence." | Reliable data theft, production exploit rate, or frontier-model benchmark. |
| ReAct-loop observation injection can drive SQL injection in an intentionally vulnerable benchmark. | <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md> | `cd lab/vuln-agents/damn-vulnerable-llm-agent && ./run_scen2_sweep.sh` | Benchmark-local evidence against an intentionally vulnerable target. | "The durable lesson is that attacker-shaped agent state crossed into a vulnerable SQL tool boundary." | A live-product SQL injection or vendor-specific vulnerability. |
| Wrapper transferability varied across two open-weight models. | <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-cross-model-react-loop-injection.md> | `cd lab/vuln-agents/damn-vulnerable-llm-agent && ./run_scen2_sweep.sh` | n=5 per model/variant cell, temperature 0, two local open-weight models. | "Transferability cannot be assumed; matrix design catches wrapper and model interactions." | General model-family rates or broad frontier-model transferability. |
| Disclosure discipline is part of the portfolio. | [`2026-05-14-evidence-traceability-manifest.md`](2026-05-14-evidence-traceability-manifest.md) | Public-safe artifacts plus private approval gates before any live test. | No executed vendor CVD is claimed by this portfolio index. | "I kept lab evidence public-safe and separated it from target-specific disclosure work." | A submitted bounty, a CVE, or a live target-specific report. |

## Review Rule

If a claim cannot be tied to an artifact, command, limitation, and do-not-claim boundary, it should not be used in an application packet.
