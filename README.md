# AI Agent Security Portfolio

Public portfolio for AI red teaming, agent/tool-use security, indirect prompt injection, MCP substrate analysis, and automated evaluation. The work here is intentionally scoped to lab targets, public CTFs, open-weight models, and disclosure-safe research artifacts.

## Reviewer Path: 5 Minutes

1. [Substrate vs Policy in MCP Tool-Output Indirect Prompt Injection](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) - pre-registered MCP matrix showing why an apparent model-policy bypass was actually a client-substrate effect.
2. [Cross-Model ReAct Loop Injection Benchmark](WRITEUPS/2026-05-14-cross-model-react-loop-injection.md) - DVL-Agent Scenario 2 benchmark comparing llama3.1:8b and mistral-nemo behavior under bare vs camouflaged payloads.
3. [Policy Isn't a Mechanism](WRITEUPS/2026-05-09-policy-isnt-a-mechanism.md) - assessment-style writeup on why prompt policy is not an access-control boundary in ReAct agents.

## Portfolio Snapshot

| Signal | Current public evidence |
|---|---:|
| ATTACKS entries | 10 |
| Long-form writeups | 3 |
| CTF / arena artifacts | 1 |
| Customer-style reports | 1 |
| Eval / automation notes | 1 |
| Disclosure status | Green-only public artifacts |

Primary tools and targets: MCP lab harness, promptfoo, garak, PyRIT, AgentDojo, Damn Vulnerable LLM Agent, Lakera Gandalf, llama3.1:8b, mistral-nemo, Claude Desktop, Cline, Kilo Code, Windsurf.

## Pinned Work

### Research: MCP substrate attribution

- [Writeup](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)
- [ATTACKS entry](ATTACKS/2026-05-10-substrate-amplification-mcp-tool-output.md)
- [Customer-ready assessment](REPORTS/substrate-vs-policy-assessment.md)
- [Eval harness note](EVALS/mcp-matrix-harness.md)

What it demonstrates: pre-registration, hypothesis retraction, controlled substrate emulation, Wilson confidence intervals, mitigation analysis, and honest limitations.

### Benchmark: DVL-Agent cross-model injection

- [Writeup](WRITEUPS/2026-05-14-cross-model-react-loop-injection.md)
- [ATTACKS entry](ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md)

What it demonstrates: small-n statistical benchmarking, cross-model comparison, payload-family sensitivity, and reproducible lab reporting.

### Assessment: prompt policy vs enforcement

- [Writeup](WRITEUPS/2026-05-09-policy-isnt-a-mechanism.md)
- [ATTACKS entry](ATTACKS/2026-05-03-indirect-injection-tool-description.md)

What it demonstrates: threat modeling, root-cause analysis, mitigation framing, and practitioner-oriented communication.

## Case Studies

For a faster hiring-manager scan, start with [CASE_STUDIES.md](CASE_STUDIES.md). It reframes the raw artifacts as:

- client assessment,
- research investigation,
- automated eval / benchmark.

## Index

- [ATTACKS/](ATTACKS/) - reproducible attack entries with scope, result, mitigation, and disclosure status.
- [WRITEUPS/](WRITEUPS/) - long-form research and practitioner writeups.
- [REPORTS/](REPORTS/) - customer-ready assessment reports.
- [EVALS/](EVALS/) - harness, benchmark, and automation notes.
- [CTF/](CTF/) - AI security challenge writeups.
- [BOUNTIES/](BOUNTIES/) - post-disclosure bounty artifacts only.

## Disclosure Policy

All public entries are scoped to intentionally vulnerable labs, open benchmarks, public CTFs, or generic research patterns. Vendor-specific findings are withheld until coordinated disclosure clears. Public artifacts use green disclosure status only.

Coordinated disclosure default: 90 days from vendor first contact, with non-response escalation after 30 days. No production systems are tested from this repository.

## Why This Repo Exists

The goal is to show work that is useful to AI security teams hiring for agentic red teaming, automated red teaming, model/tool-use evals, and customer-facing AI security research: reproducible methods, clear threat models, measured results, and mitigations that can be explained to engineering teams.
