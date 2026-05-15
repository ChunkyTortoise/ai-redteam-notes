# By-Role Reviewer Guide

**Audience**: hiring reviewers, technical screens, and recruiters evaluating fit for specific Agent / AI / Red-Team product-security roles.
**Last updated**: 2026-05-15

This guide answers one question per role: *if you're hiring for X, what should you read first, second, and third?* Each path leads to the strongest two or three artifacts for that role, in reading order.

If you only have five minutes, skip to [`start-here-for-hiring-reviewers.md`](start-here-for-hiring-reviewers.md). If you want the evidence-to-claim map, read [`hiring-evidence-index.md`](hiring-evidence-index.md).

---

## OpenAI — Agent Products Offensive Security

**The role asks for**: deep penetration testing of agent-powered products; web / API / cloud / identity / CI-CD / model-integrated surfaces; exploitability *and* durable fixes; automation.

**Read in this order**:

1. [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) — pre-registered MCP tool-output indirect injection study. Demonstrates end-to-end product-boundary reasoning: identify the load-bearing boundary, isolate it under controlled emulation, retract a misattribution, supply defender takeaways.
2. [`2026-05-15-agent-product-security-remediation-review.md`](2026-05-15-agent-product-security-remediation-review.md) — three findings with durable remediations, regression tests, and provenance/logging recommendations. Shows engineer-partner posture, not jailbreak-only.
3. [`2026-05-14-evidence-traceability-manifest.md`](2026-05-14-evidence-traceability-manifest.md) — three flagship claims mapped to artifacts, commands, limitations, and the talking-points version for interviews.

**Where evidence is thinner**: cloud and identity surfaces. The portfolio leads with agent / tool-boundary work; cloud-identity claims are framed as transferable methodology, not direct evidence.

---

## Google DeepMind — Agent Security (Product / Strategy)

**The role asks for**: ownership and strategy around prompt injection, anti-distillation, agent threats, system integrity, long-term control.

**Read in this order**:

1. [`claim-ledger.md`](claim-ledger.md) — every public claim with its evidence, scope, and known limit. Designed to be readable as a product-security threat list.
2. [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) — the substrate-vs-policy finding reframed as a control-design question for product owners: which architectural choice eliminates the failure class entirely?
3. [`2026-05-15-agent-product-security-remediation-review.md`](2026-05-15-agent-product-security-remediation-review.md) — control taxonomy (typed APIs, per-call confirmation, provenance, logging) phrased in roadmap-ready language.

**Framing note**: artifacts are written in engineer-IC voice. For product-strategy review, expect to read them as input to roadmap items, not as the roadmap itself.

---

## Google DeepMind — Frontier Safety Risk Assessment

**The role asks for**: decision-relevant evals, value of information, uncertain risk pathways, Python experiments, mitigation adequacy.

**Read in this order**:

1. [`2026-05-14-agent-security-eval-methodology.md`](2026-05-14-agent-security-eval-methodology.md) — threat model, canaries, local sinks, verdict taxonomy, and the transferability framing for mechanism-vs-rate work.
2. [`2026-05-14-mcp-n10-replication-negative-result.md`](2026-05-14-mcp-n10-replication-negative-result.md) — n=10 replication with 0/10 strict bypass and 2/10 intent shift, presented as a clean negative result with explicit scope.
3. [`mcp-reproducibility-checklist.md`](mcp-reproducibility-checklist.md) — the lab-runner protocol another evaluator would follow to replicate.

**Framing note**: small-n work is positioned as high-value mechanism discovery, not rate estimation. The pre-registration ([`docs/preregistrations/2026-05-13-tier-a-w1-w5.md`](../docs/preregistrations/2026-05-13-tier-a-w1-w5.md)) commits to the n=10 follow-up cells before any are run.

---

## Lakera — AI Safety / Red-Team Delivery

**The role asks for**: customer-facing agentic AI security testing, clear mitigation language, practical delivery.

**Read in this order**:

1. [`start-here-for-hiring-reviewers.md`](start-here-for-hiring-reviewers.md) — five-minute entry point. Customer-readable, no jargon stack.
2. [`hiring-reviewer-map.md`](hiring-reviewer-map.md) — claim-to-evidence map for technical screens.
3. [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) — flagship; demonstrates the end-to-end engagement shape a customer would receive.

**Framing note**: the pitch is intentionally customer-readable and disclosure-safe. Findings are lab-only; mitigation language is concrete.

---

## Anthropic / Microsoft AIRT — Frontier Red Team

**The role asks for**: novel attack discovery, methodological rigor, defender impact.

**Read in this order**:

1. [`WRITEUPS/2026-05-15-ai-redteam-defender-synthesis.md`](../WRITEUPS/2026-05-15-ai-redteam-defender-synthesis.md) — the whole portfolio in one read: four failure classes, structural mitigations, and a pre-registration/retraction methodology callout. Then drill into the substrate study below.
2. [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) — pre-registered study with retracted hypothesis (H3) and supported replacement (H5). The rigor signal.
3. [`open-weights-rationale.md`](open-weights-rationale.md) — why all work to date is on open-weight models, and why the substrate finding is expected to be transparent-to-scale. Pre-empts the "frontier?" question.
4. [`2026-05-14-evidence-traceability-manifest.md`](2026-05-14-evidence-traceability-manifest.md) — claim-to-artifact-to-command traceability suitable for an audit.

**Framing note**: novelty is claimed for the *isolation methodology* (substrate as registered factor, controlled emulation) and the *attribution retraction*, not for the attack class. Prior art is cited (Greshake et al. 2023; OWASP LLM02; Embrace the Red MCP series; simonw indirect-injection corpus).

---

## Reusable Eval / Security Engineer

**The role asks for**: someone who can build the test harness, run the cells, and ship the writeup independently.

**Read in this order**:

1. [`mcp-reproducibility-checklist.md`](mcp-reproducibility-checklist.md) — the lab protocol someone else could follow.
2. [`2026-05-14-agent-security-eval-methodology.md`](2026-05-14-agent-security-eval-methodology.md) — verdict taxonomy and the per-attempt classification enum.
3. [`hiring-evidence-index.md`](hiring-evidence-index.md) — end-to-end map of what shipped and how it connects.

---

## What this portfolio is *not*

- Not a production-exploit demonstration. All work is lab-only.
- Not a frontier-model evaluation. See [`open-weights-rationale.md`](open-weights-rationale.md).
- Not a CVD submission. Disclosure policy is in [`README.md`](../README.md); no current vendor-specific findings outside lab emulation.

## How to verify

Every claim in this portfolio is traceable to an artifact, a command, and (where applicable) a Wilson 95% interval. The [`hiring-evidence-index.md`](hiring-evidence-index.md) and [`2026-05-14-evidence-traceability-manifest.md`](2026-05-14-evidence-traceability-manifest.md) are the two places to start that traceability walk.
