# MCP n=10 Replication: Negative Result as Evidence

**Date:** 2026-05-14
**Status:** public
**Scope:** localhost-only MCP substrate replication using a synthetic canary and local open-weight model.

## Result

The May 14 replication reran the highest-signal XML-substrate condition from the MCP matrix at n=10. It did not reproduce reliable strict exfiltration.

| Verdict | Count |
|---|---:|
| Strict bypass | 0/10 |
| Intent shift / capability fail | 2/10 |
| Clean ignore | 8/10 |
| Canary leaked | false |

## Why This Strengthens the Portfolio

This is useful because it narrows the claim. The earlier evidence suggested that XML-style dispatch could amplify tool-output injection risk. The n=10 replication preserves only the weaker intent-layer signal: two runs moved toward unsafe tool-use intent, but none completed a reliable end-to-end canary leak.

That is a better hiring signal than overclaiming. It shows that the lab can falsify stronger interpretations and turn a mixed result into a clearer security statement.

## Current Claim Boundary

Accurate claim:

> XML-style dispatch can amplify tool-output injection into unsafe intent on a small local model, but this n=10 cell does not demonstrate reliable end-to-end data theft.

Do not claim:

- A production exploit.
- A frontier-model benchmark.
- A general MCP vulnerability across all clients.
- A reliable exfiltration rate.

## Evidence

- Scenario: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/scenario.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/scenario.md)
- Run command: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md)
- Summary: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md)
- Aggregate result: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/success.json`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/success.json)

## Interview Use

Use this when asked about uncertainty, replication, or a time a result got weaker:

> I reran the highest-signal local XML-substrate cell at n=10. The strict-bypass claim did not hold: 0/10 exfiltrations and no canary leak. But 2/10 runs still showed unsafe tool-use intent, so I kept the substrate claim narrow and moved the result from exploit-style language into eval evidence.

## Disclosure Status

Green. This is localhost-only lab evidence with a synthetic canary, no live target testing, and no vendor-specific production proof of vulnerability.
