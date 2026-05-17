# Hiring Reviewer Map

**Status:** public
**Purpose:** Give reviewers a fast path into the strongest public AI red-team evidence.

## 60-Second Path

1. **Substrate vs policy writeup (with Addendum B)**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md>
   - Why it matters: pre-registration, attribution correction, substrate isolation, and Addendum B, where a pre-registered hypothesis (H7) was falsified and the author corrected his own published takeaway.
2. **Cross-scale F1 replication ATTACKS entry**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md>
   - Why it matters: the strongest single result. Pre-registered H7 falsified at 70B: 10/10 strict canary exfil vs 0/5 at 8B, n=10, Wilson CIs, qualitative mode shift.
3. **DVL Scenario 2 ATTACKS entry**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md>
   - Why it matters: concrete ReAct-loop observation-injection evidence with practical mitigations.
4. **Substrate vs policy assessment**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/REPORTS/substrate-vs-policy-assessment.md>
   - Why it matters: concise practitioner-facing version of the flagship finding.

## 5-Minute Path

- W1-W5 pre-registration (H7 registered before the F1 cell ran, then falsified): <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/docs/preregistrations/2026-05-13-tier-a-w1-w5.md>
- Cross-model ReAct-loop writeup: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-cross-model-react-loop-injection.md>
- Substrate assessment report: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/REPORTS/substrate-vs-policy-assessment.md>
- MCP harness/eval note: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/EVALS/mcp-matrix-harness.md>

## Best First Link by Role Class

| Role class | Best first artifact |
|---|---|
| Frontier red-team / preparedness | Cross-scale F1 replication ATTACKS entry (pre-registered H7 falsified at 70B) |
| Automated red teaming / evals | W1-W5 pre-registration plus the F1 falsifier (hypotheses registered before results) |
| Agentic AI security | DVL Scenario 2 ATTACKS entry |
| AI security product / MLSecOps | Substrate vs policy assessment |
| Security consulting | Cross-model ReAct-loop writeup |

## Limits to Preserve

- The strongest claims are lab-only and disclosure-green.
- Small-n cells should be framed as mechanism evidence, not population-level rates.
- The substrate result is about typed tool-call API versus inline parser behavior, not every possible MCP client.
- The cross-scale F1 result (n=10, single payload, single client) is a mechanism-level mode shift (0/5 to 10/10 strict exfil), not a vendor or population rate. The confirmatory H10b-G grid is in progress and gated; do not quote H10b-G numbers yet.
- Public links should be checked immediately before sending a packet.
