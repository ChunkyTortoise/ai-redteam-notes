# Open-Weights Rationale

**Last updated**: 2026-05-15
**Purpose**: pre-empt the inevitable hiring-reviewer question: *"did you test this on frontier models?"*

## Short answer

No. Every published cell uses open-weight models served via Ollama (Llama 3.1 8B, Mistral Nemo, qwen2.5) or free-tier hosted endpoints (Llama 3.3 70B via OpenRouter `:free`). This is a deliberate methodology choice, not a budget shortfall. The reasoning is below.

## Why open weights

Three reasons drive the choice:

**1. Substrate effects are expected to be transparent to model scale.**

The flagship finding — that an inline-XML MCP client substrate amplifies tool-output indirect prompt injection while a typed tool-use API substrate suppresses it — is a *parser-architecture* claim, not a *model-capability* claim. The dispatch happens (or fails to happen) in the client, not in the model. Demonstrating the effect at 8B is sufficient to establish the mechanism; demonstrating it at 70B (W2 F-cells, pre-registered) tests scale-invariance; the prior is that the effect persists because nothing about it depends on model capability.

**2. Reproducibility for any reader, not just well-funded labs.**

Open-weight models are reproducible. Anyone with an Ollama install and a GPU can replicate every cell. The lab harness ([`mcp-reproducibility-checklist.md`](mcp-reproducibility-checklist.md)) is designed to run end-to-end on a laptop. Frontier-model claims, by contrast, are reproducible only by people with the relevant API keys, and the underlying weights drift across model versions without notice. A finding tied to "GPT-4o circa 2026-05" is half-life-limited; a finding on Llama 3.1 8B is replicable for years.

**3. Cost discipline.**

The Tier A track operates under a $300 hard spending cap (see [`README.md`](../README.md) for cap context). Free-tier OpenRouter `:free` endpoints and local Ollama keep marginal cost at $0 per cell, which lets the cell count grow without per-experiment friction. Frontier-model API calls in any meaningful volume would consume the cap within a single sweep.

## What this means for the portfolio's scope

- **Substrate / parser findings**: load-bearing claim. Expected to generalize across model scale (pre-registered W2-W5 cells will test this directly).
- **Model-policy findings**: deliberately retracted. The H3 hypothesis ("Mistral-Nemo more robust than Llama-8B") was retracted on substrate-confound grounds. The portfolio does not currently claim model-strength orderings, and would not claim them based on small-n frontier comparisons either.
- **Mechanism vs rate**: small-n work is positioned as mechanism discovery, not as rate estimation. The interim WRITEUP cut on 2026-06-15 will tighten Wilson intervals at n=10 for the F-cells but not pivot to rate claims.

## What would change with frontier-model access

Specific cells we would add if frontier-model access were unconstrained:

- Cline + Claude Sonnet under the inline-XML substrate (does the effect survive at frontier capability?)
- Cline + GPT-5.x under same (independent provider check)
- A cross-frontier sweep at M0-M3 mitigations to compare attenuation curves

None of these would change the substrate-vs-policy thesis; they would test its scale boundary. The pre-registered H7 hypothesis explicitly commits to falsification if the 70B replication shows different behavior; H7 at frontier scale would extend the same falsification posture.

## Citations

- Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz (2023). *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injections.* arXiv:2302.12173. — the originating treatment of indirect injection; substrate isolation extends this corpus.
- OWASP LLM Top 10 — LLM02 (Insecure Output Handling). Substrate effects are a special case of this class.
- Pre-registration: [`docs/preregistrations/2026-05-13-tier-a-w1-w5.md`](../docs/preregistrations/2026-05-13-tier-a-w1-w5.md) — commits H7/H8/H9 hypotheses before W2 F-cells run.

## TL;DR for the hiring reviewer

Open weights are the *right* substrate for this body of work, not a compromise. A frontier-model row would be additive evidence on a substrate-transparency hypothesis, not a correction. We're shipping the mechanism finding first because the mechanism is the load-bearing contribution.
