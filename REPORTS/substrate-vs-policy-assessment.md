# Substrate vs Policy Assessment

**Status:** public-safe
**Date:** 2026-05-17
**Disclosure status:** green, lab-only
**Primary writeup:** [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)

## Executive Summary

The MCP substrate study found that a bypass initially attributed to model policy was better explained by the client dispatch substrate. Holding the model and payload family constant, the typed tool-use API path held in tested cells, while an inline text/XML parser substrate produced intent-shift behavior under the same model family.

This is not a production-vendor vulnerability claim. The evidence comes from a localhost lab harness, open-weight models, controlled canary data, and public-safe run artifacts.

## What Changed the Attribution

The original hypothesis framed the result as a model robustness difference. That framing was retracted after the experiment separated model behavior from client substrate behavior:

- typed tool-use API substrate: no measured intent shift in the relevant held-constant cells
- scaffold-prompt-only condition: no measured intent shift
- inline XML-style parser substrate: intent-shift behavior appeared under the same model/payload family

The practical lesson is that client dispatch architecture can be part of the security boundary. A reviewer should not attribute an agent bypass to "the model" until the dispatch path has been isolated.

## Evidence

- Long-form writeup: [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)
- Run output: [`lab/mcp-matrix/runs/2026-05-10-llama-xml-M1-v7-dispatch-all-tags/`](../lab/mcp-matrix/runs/2026-05-10-llama-xml-M1-v7-dispatch-all-tags/)
- Defensive fixture benchmark: [`EVALS/agent-tool-output-injection-benchmark.md`](../EVALS/agent-tool-output-injection-benchmark.md)

## Defensive Takeaways

1. Prefer typed tool-call APIs over parsing executable tool calls from assistant text.
2. Treat retrieved content as untrusted data, not as instruction or prior agent state.
3. Keep prompt-level content-trust boundaries tool-agnostic on small models.
4. Put authorization, validation, and provenance checks outside the model.
5. Document client dispatch policy, including first-tag, last-tag, and dispatch-all behavior.

## Limitations

- Small-n evidence: several cells are n=5 and some exploratory cells are n=1.
- Local lab scope: localhost harness, canary data, and open-weight models only.
- Substrate-specific claim: the result supports a typed-tool-call versus inline-parser distinction, not a universal statement about every MCP client.
- Follow-up needed: more real-client parser comparisons and publication only after each follow-up control gate clears.

## Use in Hiring or Disclosure

Use this report as a concise practitioner-facing companion to the longer writeup. It is suitable for hiring packets and public portfolio navigation, but it should not be used as evidence of a live production vulnerability.
