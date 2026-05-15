# Hiring Reviewer Map

**Status:** public
**Purpose:** Give reviewers a fast path into the strongest public AI red-team evidence.

## 60-Second Path

1. **Substrate vs policy writeup**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md>
   - Why it matters: pre-registration, attribution correction, substrate isolation, and defender recommendations.
2. **DVL Scenario 2 ATTACKS entry**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md>
   - Why it matters: concrete ReAct-loop observation-injection evidence with practical mitigations.
3. **Substrate vs policy assessment**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/REPORTS/substrate-vs-policy-assessment.md>
   - Why it matters: concise practitioner-facing version of the flagship finding.

## 5-Minute Path

- Start-here reviewer page: [`start-here-for-hiring-reviewers.md`](start-here-for-hiring-reviewers.md)
- Claim ledger: [`claim-ledger.md`](claim-ledger.md)
- Cross-model ReAct-loop writeup: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-cross-model-react-loop-injection.md>
- Substrate assessment report: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/REPORTS/substrate-vs-policy-assessment.md>
- MCP harness/eval note: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/EVALS/mcp-matrix-harness.md>

## 20-Minute Path

- Evidence index: [`hiring-evidence-index.md`](hiring-evidence-index.md)
- MCP reproducibility checklist: [`mcp-reproducibility-checklist.md`](mcp-reproducibility-checklist.md)
- Evidence traceability manifest: [`2026-05-14-evidence-traceability-manifest.md`](2026-05-14-evidence-traceability-manifest.md)
- Preserved n=10 summary: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md)
- Preserved n=10 run command: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md)

## Public Proof Layer

- Start-here reviewer page: [`start-here-for-hiring-reviewers.md`](start-here-for-hiring-reviewers.md)
- Claim ledger: [`claim-ledger.md`](claim-ledger.md)
- MCP reproducibility checklist: [`mcp-reproducibility-checklist.md`](mcp-reproducibility-checklist.md)
- Negative-result note: [`2026-05-14-mcp-n10-replication-negative-result.md`](2026-05-14-mcp-n10-replication-negative-result.md)
- Agent security eval methodology: [`2026-05-14-agent-security-eval-methodology.md`](2026-05-14-agent-security-eval-methodology.md)
- Evidence traceability manifest: [`2026-05-14-evidence-traceability-manifest.md`](2026-05-14-evidence-traceability-manifest.md)
- MCP reviewer reproduction path: [`../lab/mcp-matrix/README.md`](../lab/mcp-matrix/README.md)

These files are the proof layer underneath the existing top-three public links.

## Best First Link by Role Class

| Role class | Best first artifact |
|---|---|
| Frontier red-team / preparedness | Substrate vs policy writeup |
| Automated red teaming / evals | Substrate vs policy writeup |
| Agentic AI security | DVL Scenario 2 ATTACKS entry |
| AI security product / MLSecOps | Substrate vs policy assessment |
| Security consulting | Cross-model ReAct-loop writeup |

## Limits to Preserve

- The strongest claims are lab-only and disclosure-green.
- Small-n cells should be framed as mechanism evidence, not population-level rates.
- The substrate result is about typed tool-call API versus inline parser behavior, not every possible MCP client.
- The May 14 n=10 replication weakens strict-exfiltration language and should be used as a claim-boundary artifact.
- Public links should be checked immediately before sending a packet.
