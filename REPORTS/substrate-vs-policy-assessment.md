# Assessment Report: MCP Tool-Output Injection Substrate Risk

## Executive Summary

This assessment examines a generic MCP-style agent loop where an agent fetches attacker-controlled content and has access to local tools. The key finding is that client substrate can dominate model policy: the same model and payload set can behave safely under typed tool-call dispatch and unsafely under inline XML-style dispatch.

The tested finding is disclosure-green because it uses a localhost lab, open-weight models, and generic client-substrate patterns rather than production vendor systems.

## Severity

**Risk rating:** High for agents that combine untrusted retrieval, local sensitive tools, and inline text parsing for tool dispatch.

**Reasoning:** The failure mode can turn content from a fetched page into tool-use intent. In a real deployment, this can expose local files, workspace secrets, or outbound network actions if additional controls are missing.

## Affected Pattern

An agent is at risk when all of these are true:

- It fetches or summarizes attacker-controlled content.
- It exposes sensitive tools such as file read, shell, browser, email, ticketing, or network fetch.
- It parses tool calls from assistant text or XML-like tags instead of using a structured tool-call API.
- It relies on prompt policy as the primary boundary between content and instructions.

## Reproduction Summary

Lab topology:

- attacker content server on localhost,
- exfiltration sink on localhost,
- MCP lab server with fetch and file-read tools,
- canary secret stored in a local file,
- model asked only to summarize a benign URL.

Observed result:

- Typed or pristine tool-use substrate: clean ignore in the tested cells.
- XML-dispatch emulation: intent shifts appeared under the same model and payload family.
- Tool-agnostic mitigation suppressed observed intent shifts in seed replication.
- Named-tool confirmation language regressed in hypothesis-generating cells.

Primary artifact: [Substrate vs Policy in MCP Tool-Output Indirect Prompt Injection](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md).

## Impact

If reproduced in a production agent, the pattern can support:

- indirect prompt injection through retrieved content,
- confused-deputy tool use,
- local secret exposure,
- unwanted network callbacks,
- incorrect attribution of the issue to the model instead of the client substrate.

## Recommended Mitigations

1. Use structured tool-call APIs. Do not parse executable tool calls from untrusted or model-written text.
2. Treat retrieved content as data. Preserve a hard boundary between fetched content and developer/system instructions.
3. Keep small-model mitigation prompts tool-agnostic. Avoid naming sensitive tools inside broad behavioral reminders.
4. Enforce tool allowlists and per-call authorization outside the model.
5. Log tool-call provenance, including whether a tool call came from structured API output or parsed assistant text.
6. Document dispatch policy. First-tag, last-tag, and dispatch-all behavior are security-relevant decisions.

## Limitations

- The main substrate result is based on localhost lab emulation, not production exploitation.
- Seed counts are intentionally small in early cells; confidence intervals are reported where applicable.
- Strict canary exfiltration did not occur in every intent-shift cell.
- Larger model and real-parser replication remain follow-on work.

## Evidence Links

- [Full writeup](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)
- [ATTACKS entry](../ATTACKS/2026-05-10-substrate-amplification-mcp-tool-output.md)
- [Eval harness note](../EVALS/mcp-matrix-harness.md)
