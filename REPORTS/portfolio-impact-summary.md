# Portfolio Impact Summary

**Audience**: hiring reviewers scanning for fit in ≤90 seconds.
**Status**: public; aggregator only — every factual claim sibling-occurring in other public REPORTS, WRITEUPS, or preserved run artifacts.
**Last updated**: 2026-05-15

If you only have 90 seconds: read this file. If you have more, follow the links into the deeper artifacts.

## TL;DR

- **H3 retracted in public.** An original model-strength inversion hypothesis was retracted on substrate-confound evidence; the replacement hypothesis H5 (XML-parser substrate as load-bearing) was supported under controlled emulation. See [WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md).
- **M2 regression vs M0 on a small model.** Naming tools inside a confirmation-style mitigation prompt acts as a salience prime on 8B-class models, producing 3/5 intent shifts vs 2/6 for the no-mitigation baseline. Defender takeaway: keep mitigation language tool-agnostic on small models.
- **Kilo Code typed-tool-call-API audit (B1).** Source-level audit verified Kilo Code v1.0.13 dispatches via the typed tool-use API rather than inline XML parsing — a null cell that strengthens the negative-control arm of the substrate matrix.
- **n=10 replication narrowed (not confirmed) the strict-bypass claim.** Strict bypass 0/10; intent shift 2/10; no canary leak. Wilson 95% CI for strict bypass: [0, 0.2775]. Better hiring signal than overclaiming. See [2026-05-14-mcp-n10-replication-negative-result.md](2026-05-14-mcp-n10-replication-negative-result.md).
- **Agent-product remediation review.** Two findings reframed as code-review-style remediations (boundary, exploitability, impact, durable fix, regression test, residual risk). See [2026-05-15-agent-product-security-remediation-review.md](2026-05-15-agent-product-security-remediation-review.md).

## Five Claims With Verdicts

Verbatim from [`claim-ledger.md`](claim-ledger.md). Every claim has an evidence artifact, a run command, a limitation, and an explicit "do not claim" boundary.

| Claim | Evidence | Limitation | Do not claim |
|---|---|---|---|
| Client substrate can be the load-bearing variable in MCP tool-output indirect prompt injection. | [WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) | Small-n, local harness, substrate-specific, open-weight model evidence. | A general MCP vulnerability, a production exploit, or a universal client claim. |
| The May 14 n=10 replication narrowed the MCP claim rather than confirming reliable exfiltration. | [2026-05-14-mcp-n10-replication-negative-result.md](2026-05-14-mcp-n10-replication-negative-result.md) | One model, one payload, one XML-style substrate emulation, n=10. | Reliable data theft, production exploit rate, or frontier-model benchmark. |
| ReAct-loop observation injection can drive SQL injection in an intentionally vulnerable benchmark. | [ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md) | Benchmark-local evidence against an intentionally vulnerable target. | A live-product SQL injection or vendor-specific vulnerability. |
| Wrapper transferability varied across two open-weight models. | [WRITEUPS/2026-05-14-cross-model-react-loop-injection.md](../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md) | n=5 per model/variant cell, temperature 0, two local open-weight models. | General model-family rates or broad frontier-model transferability. |
| Disclosure discipline is part of the portfolio. | [2026-05-14-evidence-traceability-manifest.md](2026-05-14-evidence-traceability-manifest.md) | No executed vendor CVD is claimed by this portfolio index. | A submitted bounty, a CVE, or a live target-specific report. |

## What This Demonstrates About The Candidate

- **Pre-registration discipline.** Hypotheses (H1–H6 in the original MCP matrix, H7–H10 in the W1–W5 tier-A sweep) committed before cells run; retractions land as separate commits referencing the deviation. See [docs/preregistrations/2026-mcp-matrix.md](../docs/preregistrations/2026-mcp-matrix.md) and [docs/preregistrations/2026-05-13-tier-a-w1-w5.md](../docs/preregistrations/2026-05-13-tier-a-w1-w5.md).
- **Substrate-attribution rigor.** A bypass initially attributed to model policy was traced to the client substrate via controlled emulation; the original attribution was retracted in public. Methodology beats the "found a jailbreak" framing.
- **Willingness to retract when data didn't support.** H3 retracted in writing, in the same writeup that supplies the replacement hypothesis. H6's strict-bypass claim falsified per its registered criterion. The portfolio prefers a narrower true claim over a wider unsupported one.

## Reviewer Entry Points By Role

Three rows pulled from [`by-role-reviewer-guide.md`](by-role-reviewer-guide.md); the full guide covers six roles.

| Role | Read first | Why |
|---|---|---|
| **Anthropic / Microsoft AIRT — Frontier Red Team** | [WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) → [open-weights-rationale.md](open-weights-rationale.md) → [2026-05-14-evidence-traceability-manifest.md](2026-05-14-evidence-traceability-manifest.md) | Pre-registered study with retracted hypothesis and supported replacement. Methodological rigor signal. |
| **OpenAI — Agent Products Offensive Security** | [WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) → [2026-05-15-agent-product-security-remediation-review.md](2026-05-15-agent-product-security-remediation-review.md) → [2026-05-14-evidence-traceability-manifest.md](2026-05-14-evidence-traceability-manifest.md) | Product-boundary reasoning + engineer-partner posture (durable fixes, regression tests). |
| **DeepMind Frontier Safety / Reusable Eval Engineer** | [2026-05-14-agent-security-eval-methodology.md](2026-05-14-agent-security-eval-methodology.md) → [2026-05-14-mcp-n10-replication-negative-result.md](2026-05-14-mcp-n10-replication-negative-result.md) → [mcp-reproducibility-checklist.md](mcp-reproducibility-checklist.md) | Mechanism-vs-rate framing, clean negative result, replication protocol. |

## Limitations (verbatim from the flagship WRITEUP)

- **Single model.** Llama 3.1 8B Instruct only. Mistral Nemo's pristine-headless baseline matches Llama-8B's 5/5 clean-ignore, but the substrate effect has not been measured on Mistral Nemo or larger models. Cross-model under the `xml-parser` substrate (workstream D, deferred) is the highest-priority follow-on.
- **n=5/cell for the seed-replicated subset; n=1 for the rest of the matrix.** Wilson 95% CIs on intent-shift rate at n=5 are wide. The directional finding (M1 < M0 under `xml-parser`) holds at this resolution but is not statistically definitive; n=10/cell would tighten the bounds.
- **Headless XML-substrate diverges from real Cline UI in named ways.** No multi-turn ReAct feedback with a real user, no IDE workspace context, no per-tool-call user-approval UI. The 2026-05-07 cell in the actual Cline UI is n=1 and computer-use-heavy to reproduce. The scaffold-prompt-only probe (0/6 intent shifts) rules out system-prompt content alone as the driver; it does not isolate the XML-tag parser from the other Cline-UI factors.
- **v7's strict-bypass claim depends on harness dispatch policy.** The pre-registered strict-bypass criterion was not met under the registered single-tag-per-turn substrate. A direct test of last-tag-wins dispatch would settle whether v7 is genuinely blocked by substrate dispatch policy or merely blocked by the specific tested dispatch modes.
- **No measurement of larger models under XML-parser substrate.** A 70B-class model run under `--xml-dispatch` would test whether the substrate amplifier becomes negligible at that scale, which is the implicit claim of takeaway 2.

## What To Look For (and Not To Infer)

From [`start-here-for-hiring-reviewers.md`](start-here-for-hiring-reviewers.md):

**Look for**: clear separation between strict bypass, intent shift, clean ignore, and harness failure; claims that narrow after replication rather than inflate; raw artifacts that preserve commands, summaries, transcripts, and limitations; remediation language aimed at engineering controls.

**Do not infer**: production exploitability; a universal MCP vulnerability; frontier-model benchmark rates; small-n mechanism evidence as population-level prevalence.

## Frontier-model coverage

The portfolio is intentionally open-weight at this stage; see [open-weights-rationale.md](open-weights-rationale.md). A frontier substrate replication on Claude 3.5 Sonnet is the active next-phase experiment (pre-registered as H10, falsifier criteria for both replication and collapse outcomes). When that lands, the results table here will gain a "generalizes to frontier?" column.
