# Remediation Case Study: Tool-Output Injection

**Date:** 2026-05-17
**Status:** reviewer-ready
**Purpose:** Show the full loop a hiring manager cares about: reproduce the risk, classify the unsafe substrate, apply the durable control, and describe what to monitor afterward.

## Executive Summary

The measured failure mode is not just "the model followed a bad prompt." In the MCP matrix runs, the risky client class treated assistant text as an executable tool-dispatch substrate. That made attacker-controlled tool output part of the control plane. The durable fix is to move tool invocation to structured tool-call events and preserve provenance through authorization checks. Prompt text can help, but it is not the main security boundary.

## Before And After

| Stage | Evidence | Result | Hiring signal |
|---|---|---|---|
| Unsafe substrate | `make audit` against `cline-sample.json` | Auditor flags `inline-xml-dispatch` as high risk | Can turn a research finding into a pre-deploy check |
| Exploit evidence | [`ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md`](../ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md) | H7 falsified; capability amplified exploitation inside the insecure substrate | Pre-registered, bounded, falsifiable security research |
| Safer substrate | `make audit` against `kilo-sample.json` | Auditor clears `typed-toolcall-api` as low risk | Architectural mitigation, not prompt-only hardening |
| Detection layer | [`DETECTIONS/tool-chain-detections.md`](../DETECTIONS/tool-chain-detections.md) | Untrusted fetch -> sensitive read -> outbound send becomes alertable | Product security and MLSecOps translation |

## Reproduce The Defensive Check

```bash
make repro
make remediation-demo
make benchmark
```

Expected reviewer-level outcome:

- `make repro` runs the dependency-free self-check and shows the auditor flagging an inline-XML sample while clearing a typed-tool-call sample.
- `make remediation-demo` compares an inline XML dispatch transcript against a structured tool-call transcript.
- `make benchmark` validates the fixture set that ties preserved runs to bounded verdicts.

## Why The Fix Is Architectural

The unsafe path lets assistant text carry executable-looking tags such as `<file_read>` or `<lab_fetch>`. Once a client parses those tags for dispatch, model output becomes part of the privileged tool-control plane. A typed tool-call API moves dispatch back into structured events and makes tool calls easier to authorize, log, and block.

The M1 content-trust boundary remains useful defense in depth. The M2 tool-naming variant is kept as a cautionary result: naming specific tools inside a prompt mitigation can increase tool salience for smaller models. That is why the recommended order is substrate first, provenance and authorization second, prompt hardening third.

## Detection Hooks

Use these signals in staging, CI, or agent telemetry:

- untrusted fetch followed by local sensitive read
- local sensitive read followed by outbound request to a non-allowlisted host
- synthetic canary value appearing in URLs, headers, or request bodies
- assistant text containing inline tool syntax in clients that parse text for dispatch
- tool calls whose nearest causal text span came from untrusted tool output

## Reviewer Boundary

All evidence cited here is disclosure-green: localhost harnesses, open-weight models, canary files, and intentionally vulnerable benchmarks. No production vendor target is claimed. H10b-G remains excluded from packet-ready claims until its full grid and control-validity gate clear.
