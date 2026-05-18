# ai-redteam-notes

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/ChunkyTortoise/ai-redteam-notes/actions/workflows/ci.yml/badge.svg)](https://github.com/ChunkyTortoise/ai-redteam-notes/actions/workflows/ci.yml)
[![Reproducible](https://img.shields.io/badge/repro-make%20repro%20(no%20API%20key)-success)](REPRODUCE.md)

> **Scope**: every experiment here targets intentionally vulnerable benchmarks (DVL Agent, vuln-agent), open-weight models via public APIs, or localhost harnesses. No production system or hosted vendor is tested without prior authorization. See [SECURITY.md](SECURITY.md).

A research engineer's portfolio on AI-agent security. The through-line: find a substrate-level indirect-prompt-injection failure, build a dependency-free auditor that detects it, and wire that auditor into a CI / pre-deploy gate. The research is pre-registered with public hypothesis retractions (Wilson 95% CIs at n=10, controlled substrate emulation) under a three-tier disclosure policy enforced by an automated pre-push hook.

**Public mirror**: [`github.com/ChunkyTortoise/ai-redteam-notes`](https://github.com/ChunkyTortoise/ai-redteam-notes) — start at [REPORTS/start-here-for-hiring-reviewers.md](https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/REPORTS/start-here-for-hiring-reviewers.md). Local packet-ready router: [REPORTS/start-here-for-hiring-reviewers.md](REPORTS/start-here-for-hiring-reviewers.md).

**Start with the research narrative**: [RESEARCH-SUMMARY.md](RESEARCH-SUMMARY.md) frames the whole program as one pre-registered through-line (attribution retraction, substrate isolation, cross-scale falsification, mitigation ordering) with negative results surfaced deliberately.

## Headline result

| Cell | Substrate | Model | Strict canary exfiltration |
|---|---|---|---|
| H10b-G M1 v7 | inline-XML dispatch + M1 | Llama-3.3-70B | 10 / 10 |
| H10b-G M1 v3 | inline-XML dispatch + M1 | Llama-3.3-70B | 0 / 10 |
| H10b-G chat-only control | no XML dispatch | Llama-3.3-70B | 0 / 10 |
| F1 (H7 falsified) | inline-XML dispatch | Llama-3.3-70B | 10 / 10 |
| baseline | inline-XML dispatch | Llama-3.1-8B | 0 / 5 |

The current strongest result is H10b-G: a single-provider 70B grid where the M1 content-trust scaffold neutralized baseline and v3 payloads but failed completely against v7. A pre-registered cross-scale safety assumption (H7: "a larger model is safer here") was also falsified. Capability amplifies exploitation inside an insecure substrate; prompt scaffolding is variant-selective, so the durable fix remains typed tool-call dispatch. Full claim-to-run mapping: [docs/reports/hiring-evidence-index.md](docs/reports/hiring-evidence-index.md).

**By the numbers**: ~2.5K LOC Python/shell harness and tooling, 45 pure-function harness tests run in CI, a zero-dependency `substrate_auditor.py`, 5 dated pre-registrations, 8 ADRs.

**Retractions and falsifications (surfaced on purpose)**: H3 retracted (substrate confound); H6, H7, H11 falsified; M2 a measured regression. Ledger: [docs/preregistrations/INDEX.md](docs/preregistrations/INDEX.md). A portfolio that hides its nulls is less trustworthy than one that reports them.

## Hiring Manager Proof Stack

```mermaid
flowchart LR
  A["Untrusted tool output"] --> B["Inline text/XML dispatch"]
  B --> C["Local canary read"]
  C --> D["Outbound exfil attempt"]
  B --> E["substrate_auditor flags high risk"]
  E --> F["Typed tool-call substrate"]
  F --> G["Detection and benchmark gates"]
```

| Proof layer | Start here | What it shows |
|---|---|---|
| Research judgment | [RESEARCH-SUMMARY.md](RESEARCH-SUMMARY.md) | A single pre-registered arc: attribution correction, substrate isolation, cross-scale falsification, and mitigation ordering. Hypothesis ledger: [docs/preregistrations/INDEX.md](docs/preregistrations/INDEX.md). |
| Reproducibility | [REPRODUCE.md](REPRODUCE.md) | `make repro` and `make benchmark` run the public-safe reviewer checks without model calls. |
| Defensive deliverable | [lab/mcp-matrix/tools/README.md](lab/mcp-matrix/tools/README.md) | `substrate_auditor.py` turns the finding into a CI/pre-deploy substrate check. |
| Remediation story | [REPORTS/remediation-case-study-tool-output-injection.md](REPORTS/remediation-case-study-tool-output-injection.md) | Attack evidence, architectural fix, detection hooks, and honest disclosure boundary in one place. |
| Raw evidence | [docs/reports/hiring-evidence-index.md](docs/reports/hiring-evidence-index.md) | Packet-ready claims tied to run directories, commands, limitations, and interview language. |

## Reviewer Path

1. [ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md](ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md) - current strongest result: H10b-G 70B grid, control-validity gate passed, M1 variant-selective.
2. [WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) - substrate attribution correction, controlled isolation, and Addendum B/C.
3. [ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md) - H7 falsified at 70B under the inline-XML substrate.
4. [ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md](ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md) - concrete ReAct-loop observation injection with tool-boundary mitigations.

One-command public-safe demo:

```bash
make repro
make benchmark
```

## Status

H10b-G is packet-ready as of 2026-05-18: all seven cells completed at n=10 on Groq-hosted Llama-3.3-70B, the chat-only control passed, and the final report documents the single-provider provenance and deviation boundary. Use the H10b-G entry as the lead hiring artifact after public mirror sync.

## Layout
| Path | Purpose |
|---|---|
| `docs/reports/` | Hiring reviewer map and claim-to-evidence index |
| `EVALS/` | Fixture-only benchmark artifacts and scorer |
| `DETECTIONS/` | Operational detection and incident-triage companion notes |
| `lab/` | Local LLM stack, garak/PyRIT/promptfoo configs, vuln-agent harnesses |
| `pipeline/` | Bounty/job tracker + weekly digests |

## Validation (CI and local)

This repo has gate scripts under `pipeline/scripts/`, and a GitHub Actions workflow that runs them on every change.

Local equivalents:

- `for f in ATTACKS/*.md; do bash pipeline/scripts/check-attack-entry.sh "$f"; done`
- `for f in ATTACKS/*.md; do bash pipeline/scripts/check-disclosure.sh "$f"; done`
- `make repro`
- `make benchmark`
- `make test`
- `make packet-ready` before using reviewer links in applications
- `make verify-public` before public sync or application packets
