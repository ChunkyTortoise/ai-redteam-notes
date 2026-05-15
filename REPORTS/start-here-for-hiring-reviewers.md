# Start Here For Hiring Reviewers

**Status:** public
**Purpose:** give a hiring reviewer a fast, conservative path through the strongest AI red-team evidence.

## Claim Boundary

This portfolio shows lab-only, disclosure-green agent-security evaluation work: small-scope experiments, synthetic canaries, localhost sinks, preserved artifacts, and conservative limitations. It does not claim a production exploit, a vendor-specific vulnerability, or a general result across all models and clients.

## 60-Second Path

1. **Substrate vs policy writeup**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md>
   - Why it matters: shows pre-registration, attribution correction, and a defender-focused client-boundary conclusion.
2. **DVL Scenario 2 ATTACKS entry**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md>
   - Why it matters: concrete ReAct-loop observation-injection evidence with a practical mitigation lesson.
3. **Substrate vs policy assessment**
   - Public artifact: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/REPORTS/substrate-vs-policy-assessment.md>
   - Why it matters: concise practitioner-facing summary of the flagship finding.

## 5-Minute Path

- Hiring evidence index: [`hiring-evidence-index.md`](hiring-evidence-index.md)
- Claim ledger: [`claim-ledger.md`](claim-ledger.md)
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
- Mitigation language aimed at engineering controls: typed tool schemas, parser hardening, provenance, confirmation flow, logging, replay, and parameterized tool boundaries.

## What Not To Infer

- Do not infer production exploitability.
- Do not infer a universal MCP vulnerability.
- Do not infer frontier-model benchmark rates.
- Do not treat small-n mechanism evidence as population-level prevalence.
