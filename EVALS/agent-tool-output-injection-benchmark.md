# Agent Tool-Output Injection Benchmark

**Status:** fixture-only, disclosure-green
**Purpose:** Give hiring reviewers a small, repeatable eval artifact that turns the MCP substrate research into a measurable benchmark shape.

## What It Measures

Each fixture captures one agent tool-output injection cell:

- payload variant
- tool-dispatch substrate
- mitigation
- model
- expected verdict
- recorded verdict
- strict-bypass and intent-shift Wilson intervals
- disclosure status

The scorer performs no model calls. It validates preserved evidence and makes the claim structure auditable in CI.

## Run

```bash
make benchmark
```

Expected output:

```text
benchmark: agent-tool-output-injection-fixture-v1
fixtures : 10
matches  : 10/10
GATE: PASS - fixture benchmark is internally consistent
```

## Fixture Schema

Fixtures live in [`fixtures/tool-output-injection-fixtures.json`](fixtures/tool-output-injection-fixtures.json). Required fields are:

`id`, `source`, `payload`, `substrate`, `mitigation`, `model`, `expected_verdict`, `actual_verdict`, `strict_bypass`, `intent_shift`, and `disclosure_status`.

`strict_bypass` and `intent_shift` each require `k`, `n`, and `wilson_95`.

## Why This Helps Hiring Reviewers

The repo already shows attack writeups. This benchmark adds the eval-engineering layer: preserved runs become structured fixtures, fixtures are checked in CI, and the same schema can accept future clients, mitigations, or models after disclosure gates clear.

The current fixture set covers:

- 70B inline-XML strict bypass under M0
- H10b-G 70B M1 variant-selective boundary: v3 held at zero while v7 bypassed
- H10b-G chat-only control holding at zero
- 8B inline-XML intent-shift without strict bypass
- typed tool-call clean behavior
- M1 mitigation holding strict bypass at zero for a v7 all-tags cell
- M2 tool-name salience regression as intent-shift evidence
- DVL Scenario 2 ReAct-loop SQL exfiltration in an intentionally vulnerable benchmark
