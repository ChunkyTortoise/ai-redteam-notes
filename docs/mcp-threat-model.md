# MCP and agent tool-use threat model

A threat model for agents that call tools through MCP or a similar tool layer, limited to what this repo's experiments, demo and detection notes actually show. Category labels use the OWASP Top 10 for LLM Applications (2025) IDs. Every row links to the repo artifact behind it; rows with no artifact are listed separately as not tested.

## System and trust boundaries

```text
user (trusted intent)
   |
   v
agent client  <-- system prompt / mitigation prompt (M1, M2)
   |   ^
   |   |  model output: free text, or structured tool_call events
   v   |
 dispatcher  ---- the boundary this repo is about: text-parsed (inline-XML, ReAct tokens) vs typed
   |
   v
MCP tools: lab_fetch (network), file_read (local files), log_event
   |
   v
tool output (UNTRUSTED: attacker-controlled document, DB rows, observations)
```

Assets: local secrets (modelled by a canary file), the user's data in tool backends, and outbound network reach. Attacker: controls the content of one fetched document or tool observation; the user is benign. All targets here are localhost harnesses, local models or intentionally vulnerable benchmarks ([SECURITY.md](../SECURITY.md)).

## Threats observed in this repo

| ID | Threat | OWASP LLM | Attack path | Evidence in repo | Observed outcome | Mitigation and its evidence |
|---|---|---|---|---|---|---|
| T1 | Indirect injection through tool output becomes a tool call | LLM01 | Fetched document carries tool-call text; client parses it out of the model's reply | [H10b-G](../ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md), [F1](../ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md), seeds under [`lab/mcp-matrix/runs/`](../lab/mcp-matrix/runs/) | M0 strict bypass 9/10, 10/10, 10/10 on Llama-3.3-70B; F1 10/10 | Typed tool-call dispatch. Measured only indirectly: the chat-only control was 0/10; one simulated 8B typed cell ([fixtures](../EVALS/fixtures/tool-output-injection-fixtures.json)); mechanism shown in the [offline demo](../demo/dispatch_demo.py) |
| T2 | Text-parsed dispatch makes assistant text part of the security boundary | LLM05 | Any tag-shaped text the model repeats is executed | [Substrate amplification](../ATTACKS/2026-05-10-substrate-amplification-mcp-tool-output.md), [writeup](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md), [demo tests](../tests/test_dispatch_demo.py) | 8B bypass disappeared (0/5) when XML-tag scaffolding was removed; demo naive dispatcher reads the canary, typed one does not | Structured `tool_call` events only; [`substrate_auditor.py`](../lab/mcp-matrix/tools/substrate_auditor.py) flags inline-XML configs (heuristic, known false results in the [README limits](../README.md#decisions-failures-limits)) |
| T3 | Exfiltration of local secrets through an outbound tool | LLM02 | `file_read` of the canary, then `lab_fetch` to an attacker URL | Strict-bypass definition in the [H10b-G scenario](../ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md#scenario) | Canary reached a real localhost callback in every counted strict bypass | Outbound host allowlist, confirmation on sensitive reads and cross-boundary sends, canary alerts ([detections](../DETECTIONS/tool-chain-detections.md)); not measured as controls here. The offline demo has a sketch of the read-confirmation control (`provenance_gate`, [tests](../tests/test_dispatch_demo.py)) against a scripted hijacked model; it does not gate outbound sends |
| T4 | Prompt-only mitigation is payload-specific | LLM01 | Attacker changes payload family until the content-trust prompt stops matching | H10b-G M1 cells | M1: 0/10 baseline, 0/10 v3, 10/10 v7. M2 (tool-naming prompt) did worse than no prompt on 8B | Keep M1 as defense in depth only; fix the dispatcher first ([remediation case study](../REPORTS/remediation-case-study-tool-output-injection.md#why-the-fix-is-architectural)) |
| T5 | Dispatch order (first, last or all tags) changes what an injection can trigger | LLM05 | Injected tag placed before or after the legitimate one | [Last-tag ablation](../ATTACKS/2026-05-15-mcp-xml-last-tag-dispatch-ablation.md) | Last-tag-wins: 0/10 strict (H11 falsified) | Document and audit the client's tag-dispatch rule |
| T6 | Injected text forging agent state or system authority | LLM01 | `(#system)` directive or fake `Thought:/Action:/Observation:` tokens in user-reachable content | [Spoofed system directive](../ATTACKS/2026-05-03-indirect-injection-tool-description.md), [DVL scenario 2](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md), [PAIR scenario 1](../ATTACKS/2026-05-06-pair-agent-dvl-scenario1.md) | User isolation overridden; flag exfiltrated in 4 PAIR turns; UNION SQL exfil 10/10 on llama3.1:8b | Strip or reject agent-state tokens before the loop; structured dispatch ([scenario 2 mitigations](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md#mitigation)) |
| T7 | Injection reaching a tool backend (SQL) through tool arguments | LLM05 | Model passes attacker string as `userId` into an interpolated query | [DVL scenario 2](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md) | llama3.1:8b 10/10 pooled, mistral-nemo 5/10 | Parameterised queries and type checks at the tool boundary, independent of the model |
| T8 | Excessive agency and MCP-protocol authority claims | LLM06 | User text asks the agent to update balances, delete records, or "use the MCP protocol" to call a privileged tool | [DVL promptfoo run](../ATTACKS/2026-05-12-dvl-agent-promptfoo-baseline.md), [AgentDojo Granite](../ATTACKS/2026-05-04-agentdojo-granite-4-1-8b.md) | promptfoo: 4/24 strict, MCP-abuse cases 1 FAIL / 2 PASS; AgentDojo: all 3 injection tasks executed | Least-privilege tool sets and authorization outside the model (recommended; not measured here) |

## Detection

Chains to alert on, from [DETECTIONS/tool-chain-detections.md](../DETECTIONS/tool-chain-detections.md): untrusted fetch then sensitive read then outbound request; tool calls whose nearest causal span is tool output; canary values in outbound URLs or bodies; inline tool syntax in assistant text in text-parsing clients. A worked triage: [mock incident](../DETECTIONS/mock-incident-triage-tool-output-injection.md).

## Not tested in this repo

These are common MCP threats with no experiment, demo or finding here. They are listed so the table above is not read as complete.

- Tool description poisoning (malicious instructions in a server's tool metadata) and description changes after approval.
- Malicious or impersonated MCP servers, server-to-server confusion, and tool name collisions.
- Authentication, token handling and credential scope between client, server and upstream APIs.
- Supply chain of MCP server packages.
- Typed-dispatch clients at 70B or on frontier models (the main open question in the [roadmap](../README.md#roadmap)).

<!-- TODO(Cayman): review the OWASP LLM ID chosen for each row (LLM05 for dispatch rows is a judgment call) before citing this doc in an interview. -->
