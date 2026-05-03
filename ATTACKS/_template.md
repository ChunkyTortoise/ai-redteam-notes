---
title: "<short attack title>"
class: "<OWASP LLM Top 10 ID + name>"
lane: 3
affected_systems: "<generic class - e.g., 'CRM-integrated agents with tool calling'>"
disclosure_status: green
disclosure_target: "none"
disclosure_first_contact: null
disclosure_clearance_date: null
disclosure_notes: "Generic open-weight model / vuln-agent reproduction. No specific vendor."
date: 2026-MM-DD
---

# <Attack title>

## Threat model

What attacker, what capability, what goal. One paragraph.

## Scenario

Concrete reproduction. Diagram if helpful (mermaid):

```mermaid
sequenceDiagram
  Attacker->>WebPage: plant indirect injection
  User->>Agent: "summarize my email"
  Agent->>WebPage: fetch
  WebPage-->>Agent: hidden instruction
  Agent->>Tool: invoke (against user's interest)
```

## Proof of concept

Generic targets only. No account-binding info.

```bash
# exact reproduction commands - paste-runnable
docker compose -f lab/docker-compose.yml up -d
ollama pull <model>
python -m garak --model_type litellm --model_name ollama/<model> --probes <probe>
```

## Result

Success rate over N trials. Logs / screenshots redacted.

## Mitigation

What defenders should do. Reference framework guidance:

- OWASP LLM Top 10 mitigation for [LLM01 / LLM06 / etc.]
- MITRE ATLAS technique [Txxxx] with countermeasures [Mxxxx]
- NIST AI RMF mapping if applicable

## References

- digest: `content/drafts/digest-<slug>.md`
- run: `content/drafts/run-<slug>.md`
- prior art: <citations>
