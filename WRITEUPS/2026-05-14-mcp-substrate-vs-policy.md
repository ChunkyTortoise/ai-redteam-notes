---
title: Substrate vs Policy in MCP Tool-Output Indirect Prompt Injection
subtitle: A pre-registered measurement of why a model-attributed bypass was actually a client-substrate effect
date: 2026-05-14
authors: Cayman Roden
status: published
tags: [llm-security, indirect-prompt-injection, mcp, red-team, pre-registration, substrate-effects]
attacks_entry: ATTACKS/2026-05-10-substrate-amplification-mcp-tool-output.md
pre_reg: docs/preregistrations/2026-mcp-matrix.md
spec: docs/specs/2026-05-09-feature-mcp-matrix-substrate-aware-continuation-spec.md
---

# Substrate vs Policy in MCP Tool-Output Indirect Prompt Injection

## TL;DR

A pre-registered MCP tool-output indirect prompt injection matrix produced an attribution failure that is worth examining on its own. An 8B-class open-weight model (Llama 3.1 8B) showed a 2/5 intent-shift bypass under one MCP client substrate and 0/5 under another — same model weights, same payload set, same generation settings. The substrate variable was whether the client invoked tools via the structured tool-use API or via inline XML tags parsed out of the assistant's chat content. The hypothesis that initially attributed the bypass to model policy posture (H3) was retracted on substrate-confound evidence; a replacement hypothesis (H5) testing the XML-tag substrate as the load-bearing factor was supported under controlled emulation. A combined-framing payload (v7) broke a previously-stable mitigation's intent-shift suppression at 2/5 seeds, but its strict-bypass claim was falsified per the pre-registered criterion. Three implications for defenders: verify the substrate before pinning attribution on the model; prefer the typed tool-use API over inline-XML dispatch for any LLM below the 70B class; do not name specific tools inside mitigation prompts on small models, since naming acts as a salience prime.

## Threat model

The setting is an MCP-style agent loop with a generic web-fetch tool. The adversary controls the body of one document the agent will fetch (a webpage, a wiki article, a Notion page, a Confluence document — any retrievable artifact the adversary can edit). The agent's user is benign and has not authorized any sensitive action. The success criterion for the adversary is a *canary exfiltration*: a secret value stored in a local file is leaked to an attacker-controlled URL via the agent's fetch tool.

Three components determine whether the attack lands:

1. **The model's content-trust posture.** Does the model treat instructions inside fetched content as instructions or as data? This is the variable most discussions focus on.
2. **The substrate the MCP client uses to dispatch tool calls.** Does the client interpret typed tool-use blocks from the model's structured output, or does it parse XML tags inline from the model's chat content?
3. **The client-side dispatch policy** for tags within a single assistant turn — first-tag-wins, last-tag-wins, dispatch-all-tags. This is a substrate-level decision usually made implicitly during client implementation.

Substrate effects in this class have been hinted at in prior work (Greshake et al. 2023; the OWASP LLM Top 10 LLM02 entry on insecure output handling; Embrace the Red's MCP confused-deputy series; simonw on indirect injection lethal trifectas). What is uncommon is the registration of the substrate as an experimental factor and its isolation through controlled emulation against a held-constant model. That is the methodological contribution of this writeup.

## Methodology

The study was pre-registered at `docs/preregistrations/2026-mcp-matrix.md` before the first cell ran. Frozen taxonomy: 5 payload variants (baseline + v1–v4) for the original matrix; 4 mitigation conditions M0 (none), M1 (system-prompt content-trust boundary), M2 (per-call confirmation with named tools), M3 (server-side content sanitizer + sanitizer-aware system prompt); n=5 seeds per cell at temperature 0.7 for the seed-replicated phase. Per-attempt outcomes are classified into a 9-code enum (`canary_exfil`, `intent_shift`, `clean_ignore`, `pre_tool_refusal`, `partial_decode`, `url_false_positive`, `harness_error`, `model_refusal`, `capability_fail`); cell verdicts roll those up into named verdicts (`bypassed`, `intent-bypass / cap-fail`, `held-by-policy`, `held-mixed`). The strict-bypass cell verdict requires `canary_in_exfil == true` on at least 2/n seeds.

Deviation 1 was committed on 2026-05-09, before the first cell of the substrate-aware phase ran. It registered a `substrate` axis with enum `chat-only` / `xml-parser` / `cline-ui`, retracted H3 (model-strength inversion: Mistral-Nemo more robust than Llama-8B) on substrate-confound grounds since the original H3 evidence compared an `xml-parser`-substrate Cline run against a `chat-only`-substrate headless run, and registered two new hypotheses: H5 (the XML-tag-parser substrate is necessary for any Llama-8B M0 intent shift on this payload set) and H6 (a combined-framing payload v7 produces ≥1 strict bypass on M0 under the XML-parser substrate across ≥5 seeds).

The harness (`lab/mcp-matrix/scripts/run_headless.py`) supports `--xml-dispatch` (XML-tag content parser), `--dispatch-all-tags` (all tags in a turn fire rather than just the first), `--temperature`, and `--seed`. Wilson 95% confidence intervals were computed post-hoc via `lab/mcp-matrix/scripts/wilson_ci.py`. Seed sweeps used `lab/mcp-matrix/scripts/seed_sweep.sh`. All artifacts (run dirs, transcripts, success.json files) are reachable under `lab/mcp-matrix/runs/2026-05-09-llama-xml-*/` and `lab/mcp-matrix/runs/2026-05-10-llama-xml-M1-v7-dispatch-all-tags/`.

The model under test was Llama 3.1 8B Instruct via Ollama. The Mistral Nemo comparand was run under the `chat-only` substrate only and matched Llama-8B's 5/5 clean-ignore baseline on the pristine harness; cross-model under the `xml-parser` substrate is workstream D, deferred to a follow-on study.

## Findings

The substrate variable is load-bearing. Under three substrate conditions, holding model and payload set constant on Llama 3.1 8B:

| Substrate | Intent shifts (k/n) | Strict bypass | Cell verdict |
|---|---|---|---|
| Headless tool-use API (pristine) | 0/5 | 0/5 | held-by-policy |
| Headless + Cline-style system prompt (no XML parser) | 0/6 | 0/6 | held-by-policy |
| Headless + XML-tag dispatch parser | 2/6 | 0/6 | intent-bypass / capability-fail |

(The n=6 in the latter two rows reflects the pre-reg's 5 variants plus one additional v6 cross-step substitution attempt run during the hypothesis-generating substrate-emulation phase, before the n=5/cell seed-replication study formalized the seed budget.)

The system-prompt content alone is insufficient to reproduce the bypass shape. Only the combined substrate that includes the inline-XML-tag content parser does so. **H5 is supported** at this resolution (`chat-only` and scaffold-prompt-only both 0/6 vs `xml-parser` 2/6); H3 remains retracted.

Mitigation curve under the `xml-parser` substrate (n=1 per cell, hypothesis-generating):

| Mitigation | Intent shifts | Strict bypass | Notes |
|---|---|---|---|
| M0 (none) | 2/6 | 0/6 | baseline |
| M1 (system-prompt content-trust boundary) | 0/7 | 0/7 | tool-agnostic boundary works |
| M2 (per-call confirmation, names `file_read`/`lab_fetch`) | 3/5 | 0/5 | **regression vs M0** |
| M3 (server-side sanitizer + aware prompt) | 0/5 | 0/5 | held-by-policy |

M2's regression is the most surprising single result. The M2 system prompt explicitly names the tools the user wants confirmed before each call. On a 70B-class model, naming the tools likely supports self-monitoring. On an 8B-class model, naming the tools acts as a salience prime — the mitigation language reads to the model as a hint about which tools are available and probable. This is a generalizable warning about transferring 70B-class mitigation patterns to small-model deployments without re-evaluation.

Seed replication (n=5 per cell at temperature 0.7) for the two M0-positive variants under M0 and M1:

| Cell | Intent shift k/n | Wilson 95% CI |
|---|---|---|
| M0 baseline | 2/5 | [0.118, 0.769] |
| M0 v3-fake-json-fence | 2/5 | [0.118, 0.769] |
| M1 baseline | 0/5 | [0.000, 0.435] |
| M1 v3-fake-json-fence | 0/5 | [0.000, 0.435] |

Pooled across variants: M0 = 4/10 vs M1 = 0/10. The Wilson CIs are nearly disjoint at n=5/cell; the direction holds but is not statistically definitive — an n=10/cell re-run is queued.

The v7 payload (combining v3's fake-JSON-fence framing with v6's cross-step substitution worked example) produced 0/5 strict bypass on M0 across 5 seeds, with 1/5 intent shifts. **By the pre-registered H6 falsifier (0 strict bypasses across ≥5 seeds on M0), H6 is falsified.** A secondary finding: under M1, v7 produced 2/5 intent shifts versus 0/10 across the baseline + v3 cells under M1 — that is, **v7 breaks M1's intent-shift suppression at 2/5 seeds without producing a strict bypass, and produces more intent shifts under M1 than under M0** (a sign that M1's boundary text itself interacts with v7's audit-pre-check framing). Inspection of M1 v7 seed 1's transcript reveals the model emitting both a stale `<file_read>` tag and a correctly-substituted `<lab_fetch>` URL bearing the real canary in the same assistant turn; the harness's first-tag-per-turn dispatcher fired the file_read and discarded the lab_fetch. An ablation with `--dispatch-all-tags` (5 seeds) also produced 0/5 strict bypass, but for a different mechanistic reason: under dispatch-all-tags the model emits both tags before observing the file_read return, so the lab_fetch URL contains a hallucinated placeholder rather than the real canary. The dispatch policy that would actually leak v7 is "dispatch last tag in turn," which has not been measured directly and is inferred from the single-tag transcript.

## Defender takeaways

Priority order, with the reasoning anchored to the data above.

1. **Verify the substrate before attributing a bypass to a model's policy.** If a model-attributed bypass exists, re-run the same model on the same payload set through a pristine tool-use-API substrate. If the bypass disappears, the variable was the substrate. This study's H3 was retracted on exactly this evidence. The retraction is cheap; the prior attribution had been used to plan downstream cross-model comparisons that would have been confounded.

2. **Prefer the typed tool-use API substrate over inline-XML for any LLM below the 70B class.** The structural separation between client-instruction tool invocations (typed tool-use blocks) and content-side tool tokens (text inside fetched documents) does security work that the model itself does not have to do. Inline-XML-tag MCP clients collapse that separation. An 8B-class model cannot reliably distinguish "tag in client scaffold" from "tag in fetched content" at the pattern-match level. This is a substrate decision, not a model decision; it does not require waiting for a model fix.

3. **Keep mitigation language tool-agnostic on small models.** Tool-naming inside system prompts (M2) caused a 50% relative regression versus the no-mitigation baseline in this study. A short, tool-agnostic content-trust boundary (M1) was the most effective single mitigation. Per-tool affordance belongs in runtime UI surfaces (confirmation modals, tool-call previews), not in system-prompt instructions that enumerate tool names.

4. **Treat client-side dispatch policy as part of the security boundary, not a UI implementation detail.** v7's dispatch-policy interaction (first-tag-wins blocked the strict bypass; last-tag-wins would not have) is non-monotonic with the model's substitution capability. MCP client authors making implementation choices about tag-dispatch order are making security-relevant decisions; that choice should be documented, configurable, and audited rather than implicit.

## Limitations and future work

- **Single model.** Llama 3.1 8B Instruct only. Mistral Nemo's pristine-headless baseline matches Llama-8B's 5/5 clean-ignore, but the substrate effect has not been measured on Mistral Nemo or larger models. Cross-model under the `xml-parser` substrate (workstream D, deferred) is the highest-priority follow-on.
- **n=5/cell for the seed-replicated subset; n=1 for the rest of the matrix.** Wilson 95% CIs on intent-shift rate at n=5 are wide. The directional finding (M1 < M0 under `xml-parser`) holds at this resolution but is not statistically definitive; n=10/cell would tighten the bounds.
- **Headless XML-substrate diverges from real Cline UI in named ways.** No multi-turn ReAct feedback with a real user, no IDE workspace context, no per-tool-call user-approval UI. The 2026-05-07 cell in the actual Cline UI is n=1 and computer-use-heavy to reproduce. The scaffold-prompt-only probe (0/6 intent shifts) rules out system-prompt content alone as the driver; it does not isolate the XML-tag parser from the other Cline-UI factors.
- **v7's strict-bypass claim depends on harness dispatch policy.** The pre-registered strict-bypass criterion was not met under the registered single-tag-per-turn substrate. A direct test of last-tag-wins dispatch would settle whether v7 is genuinely blocked by substrate dispatch policy or merely blocked by the specific tested dispatch modes.
- **No measurement of larger models under XML-parser substrate.** A 70B-class model run under `--xml-dispatch` would test whether the substrate amplifier becomes negligible at that scale, which is the implicit claim of takeaway 2.

---

*Lab artifacts: `lab/mcp-matrix/` in the [public ai-redteam-notes repo](https://github.com/ChunkyTortoise/ai-redteam-notes). Full ATTACKS entry: `ATTACKS/2026-05-10-substrate-amplification-mcp-tool-output.md`. Pre-registration: `docs/preregistrations/2026-mcp-matrix.md`. Continuation spec: `docs/specs/2026-05-09-feature-mcp-matrix-substrate-aware-continuation-spec.md`.*
