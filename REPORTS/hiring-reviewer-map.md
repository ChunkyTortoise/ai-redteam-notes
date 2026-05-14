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

- Cross-model ReAct-loop writeup: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-cross-model-react-loop-injection.md>
- Substrate assessment report: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/REPORTS/substrate-vs-policy-assessment.md>
- MCP harness/eval note: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/EVALS/mcp-matrix-harness.md>

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
- Public links should be checked immediately before sending a packet.
