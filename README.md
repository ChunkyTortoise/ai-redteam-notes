# AI Agent Product Security Portfolio

[![ci](https://github.com/ChunkyTortoise/ai-redteam-notes/actions/workflows/ci.yml/badge.svg)](https://github.com/ChunkyTortoise/ai-redteam-notes/actions/workflows/ci.yml)

**Pre-registered AI red-team research with public hypothesis retractions when data didn't support.** Methodology-first portfolio covering indirect prompt injection, unsafe tool use, MCP client substrate risk, remediation review, and automated evaluation. Wilson 95% confidence intervals at n=10, controlled substrate emulation, three-tier disclosure policy with automated pre-push gating. The work here is intentionally scoped to lab targets, public CTFs, open-weight models, and disclosure-safe research artifacts.

## Start Here

**Read first:** [RESEARCH-SUMMARY.md](RESEARCH-SUMMARY.md) frames the whole portfolio as one pre-registered research program: an attribution retraction, the substrate isolated as a registered factor, a cross-scale hypothesis (H7) falsified at 70B, mitigation ordering, and negative results surfaced deliberately. Reproduce the defensive deliverable in 60 seconds with `make repro`.

For a fast hiring-reviewer path through the strongest evidence, then see [Start Here For Hiring Reviewers](REPORTS/start-here-for-hiring-reviewers.md). It links the flagship writeups, remediation review, claim ledger, reproducibility checklist, and preserved MCP n=10 artifacts.

For a web landing page candidate, see [index.html](index.html). It is built for GitHub Pages from this repo root.

## Reviewer Path: 5 Minutes

0. [Portfolio Impact Summary](REPORTS/portfolio-impact-summary.md) - 90-second aggregated view: five claims with verdicts, what this demonstrates, role-specific entry points, limitations.
0b. [Defender-Synthesis Whitepaper](WRITEUPS/2026-05-15-ai-redteam-defender-synthesis.md) - the whole portfolio reduced to four defendable failure classes, each with a structural mitigation and a pre-registration/retraction methodology callout.
1. [By-Role Reviewer Guide](REPORTS/by-role-reviewer-guide.md) - if you're hiring for a specific role (OpenAI Agent Products, DeepMind, Lakera, Anthropic / Microsoft AIRT, reusable eval engineer), this points you at the strongest two or three artifacts in reading order.
2. [Hiring Reviewer Map](REPORTS/hiring-reviewer-map.md) - fastest route through the strongest public artifacts by role class.
3. [Hiring Evidence Index](REPORTS/hiring-evidence-index.md) - claim-to-evidence map with commands, disclosure status, and limitations.
4. [Agent Product Security Remediation Review](REPORTS/2026-05-15-agent-product-security-remediation-review.md) - code-review-style remediation artifact: boundary, exploitability, impact, fix, regression test, and residual risk.
5. [Substrate vs Policy in MCP Tool-Output Indirect Prompt Injection](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) - pre-registered MCP matrix showing why an apparent model-policy bypass was actually a client-substrate effect. See **Addendum B**: the pre-registered cross-scale hypothesis H7 was falsified at 70B (the strongest single result).
5b. [Cross-scale F1 replication](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md) - the H7 falsifier as a standalone ATTACKS entry: 10/10 strict canary exfil at 70B vs 0/5 at 8B, n=10, Wilson CIs.
6. [Cross-Model ReAct Loop Injection Benchmark](WRITEUPS/2026-05-14-cross-model-react-loop-injection.md) - DVL-Agent Scenario 2 benchmark comparing llama3.1:8b and mistral-nemo behavior under bare vs camouflaged payloads.

## Why open weights?

If you're about to ask "did you test on frontier?", read [Open-Weights Rationale](REPORTS/open-weights-rationale.md). Short answer: the pre-registered cross-scale cell (H7) shows the substrate effect does not wash out as the model gets more capable; it strengthens (8B reached 0/5 strict exfil, 70B reached 10/10). Open-weight cells are therefore a conservative lower bound for frontier behavior, and every cell is reproducible by any reader.

## Portfolio Snapshot

| Signal | Current public evidence |
|---|---:|
| ATTACKS entries | 11 |
| Long-form writeups | 3 |
| CTF / arena artifacts | 1 |
| Customer-style reports | 4 |
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

### Review: agent product remediation

- [Remediation review](REPORTS/2026-05-15-agent-product-security-remediation-review.md)
- [Evidence index](REPORTS/hiring-evidence-index.md)
- [Reviewer map](REPORTS/hiring-reviewer-map.md)

What it demonstrates: exploitability triage, trust-boundary analysis, durable remediation, regression-test framing, and residual-risk communication.

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
