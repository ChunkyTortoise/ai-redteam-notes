# Agent Product Security Remediation Review

**Date:** 2026-05-15  
**Status:** public; lab-only and disclosure-green  
**Purpose:** show remediation judgment, not only attack discovery.

## Finding 1: Tool-Output Injection Across MCP Client Boundary

**Evidence:** [`../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) and preserved runs under [`../lab/mcp-matrix/runs/`](../lab/mcp-matrix/runs/).

**Vulnerable boundary:** attacker-controlled tool output entered an agent context where the client substrate influenced whether injected instructions could become tool-use intent.

**Exploitability:** lab-only. The strongest current evidence supports client-substrate amplification and unsafe intent, not reliable production data theft. The May 14 n=10 replication produced 0/10 strict bypasses, 2/10 intent shifts, and no canary leak.

**Impact if present in a real product:** unauthorized tool use, sensitive-file reads, data egress to attacker-controlled URLs, or user-visible actions performed under misleading provenance.

**Durable remediation:**

- Use typed tool-call APIs and parameterized tool arguments rather than parser-dispatched instruction text.
- Preserve provenance on retrieved content and tool output.
- Add per-call confirmation for risky operations such as external network calls, file access, account changes, and code execution.
- Log tool inputs, tool outputs, model decisions, and confirmation outcomes for replay.

**Regression test:** replay the same injected tool-output fixture and assert that the canary never reaches the local sink. Count strict bypass, intent shift, clean ignore, and harness failure separately.

**Residual risk:** prompt-only mitigations can regress or become salience primes on smaller models. Keep prompt hardening as one layer, not the boundary.

## Finding 2: ReAct Observation Injection Into SQL Tool Boundary

**Evidence:** [`../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md`](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md) and [`../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md`](../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md).

**Vulnerable boundary:** attacker-shaped user text mimicked prior `Thought / Action / Observation` state, then crossed into a SQL tool that interpolated the value directly.

**Exploitability:** benchmark-local and intentionally vulnerable. The bare payload succeeded across two open-weight models; wrapper behavior differed by model.

**Impact if present in a real product:** cross-account data access, credential disclosure, or unsafe database reads when model-generated state is trusted as tool input.

**Durable remediation:**

- Refuse or normalize user content that mimics internal agent trace tokens.
- Parameterize SQL queries and reject non-integer user IDs at the tool boundary.
- Treat model output as untrusted until validated against the tool schema.
- Add output-shape checks so unexpected columns or credential-like fields are never rendered to the user.

**Regression test:** run the bare and camouflaged fixtures against the tool boundary, then assert that tool calls use the authenticated user ID and never render password sentinels.

**Residual risk:** structured tool APIs reduce ReAct-token spoofing, but they do not remove authorization, validation, or output-filtering requirements.

## Product-Security Takeaway

The portfolio should lead with this remediation frame in agent-product roles:

1. Identify the trust boundary.
2. Validate exploitability with harmless canaries and local sinks.
3. Separate model intent from application or client dispatch behavior.
4. Propose a fix at the load-bearing boundary.
5. Add regression tests so the failure does not return when the product changes.

That framing matches agent product security better than a list of jailbreaks. It shows the ability to find realistic failures and help engineering teams close them.
