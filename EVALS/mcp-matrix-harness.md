# Eval Note: MCP Tool-Output Injection Matrix Harness

This note documents the automation shape behind the MCP substrate work. It is written for reviewers looking for automated red-team and eval evidence rather than only final writeups.

## Goal

Measure whether an agent treats fetched, attacker-controlled content as instructions when local tools are available. The harness separates three variables:

- model behavior,
- client substrate,
- mitigation or dispatch policy.

## Core Inputs

| Input | Examples |
|---|---|
| Payload variant | baseline, visible notice, details block, fake JSON fence, tag smuggle, fence-handhold |
| Model | llama3.1:8b, mistral-nemo |
| Substrate | typed tool-call API, chat-only, inline XML-dispatch emulation |
| Mitigation | M0 none, M1 tool-agnostic boundary, M2 named-tool confirmation, M3 sanitizer |
| Seed / temperature | seed sweep at temperature 0.7 for selected cells |

## Output Taxonomy

Attempt outcomes are classified into a fixed enum:

- `canary_exfil`
- `intent_shift`
- `clean_ignore`
- `pre_tool_refusal`
- `partial_decode`
- `url_false_positive`
- `harness_error`
- `model_refusal`
- `capability_fail`

Cell verdicts roll those attempts into labels such as `bypassed`, `intent-bypass / cap-fail`, `held-by-policy`, and `held-mixed`.

## Reproduction Commands

Representative commands from the private lab harness:

```bash
cd lab/mcp-matrix
python scripts/run_headless.py --xml-dispatch --seed 1 --temperature 0.7
bash scripts/seed_sweep.sh M0 baseline 5
python scripts/wilson_ci.py runs/<cell>/success.json
```

The public writeups preserve the claims and summarized outputs. Sensitive local runtime paths and transient process files are not required to understand the findings.

## Evidence Pattern

Each completed cell should produce:

- transcript JSONL,
- per-attempt result JSON,
- cell-level `success.json`,
- Wilson confidence interval where seed counts support it,
- short summary or ATTACKS entry,
- green disclosure status before publication.

## Why This Matters For Automated Red Teaming

The harness is designed to make agent failures comparable. A reviewer can see not just "a jailbreak happened," but which substrate, payload wrapper, mitigation, and model produced the result. That makes the work usable for regression testing, mitigation design, and hiring discussions about methodology.

## Related Artifacts

- [Substrate vs Policy writeup](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)
- [Customer assessment](../REPORTS/substrate-vs-policy-assessment.md)
- [ATTACKS entry](../ATTACKS/2026-05-10-substrate-amplification-mcp-tool-output.md)
