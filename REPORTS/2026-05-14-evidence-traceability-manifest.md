# Evidence Traceability Manifest

**Date:** 2026-05-14
**Status:** public
**Purpose:** map flagship hiring claims to artifacts, commands, limitations, and interview use.

## Claim 1: Client substrate can be the load-bearing variable in MCP tool-output indirect prompt injection.

**Source artifact:** [`../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)

**Raw run folders:** `../lab/mcp-matrix/runs/`

**Reproduction command:**

```bash
cd lab/mcp-matrix
just test
```

**Disclosure status:** green; localhost-only lab evidence.

**Limitation:** substrate-specific, small-n, local open-weight model evidence. The claim is about observed client dispatch behavior, not every MCP client or model.

**Interview talking point:** I initially had a tempting model-policy explanation, then changed the claim after substrate evidence made the client dispatch path the cleaner explanation.

## Claim 2: The May 14 n=10 replication weakened strict exfiltration while preserving a narrow intent-layer signal.

**Source artifact:** [`2026-05-14-mcp-n10-replication-negative-result.md`](2026-05-14-mcp-n10-replication-negative-result.md)

**Raw run folder:** [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/)

**Reproduction command:** [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md)

**Disclosure status:** green; localhost-only synthetic canary evidence.

**Limitation:** one model, one payload, one substrate emulation, n=10. It does not establish a production exploit rate.

**Interview talking point:** The result is stronger because it forced a narrower claim: no reliable strict bypass, but enough intent-layer signal to justify further substrate testing.

## Claim 3: ReAct-loop observation injection can drive SQL injection in an intentionally vulnerable agent benchmark.

**Source artifact:** [`../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md`](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md)

**Raw run folder:** `lab/vuln-agents/damn-vulnerable-llm-agent/`

**Reproduction command:**

```bash
cd lab/vuln-agents/damn-vulnerable-llm-agent
./run_scen2_sweep.sh
```

**Disclosure status:** green; intentionally vulnerable educational benchmark.

**Limitation:** benchmark-local evidence. The mitigation lesson is tool-boundary validation and parameterized SQL, not a claim about a live product.

**Interview talking point:** The durable lesson is not "better prompt." It is that attacker-shaped agent state crossed into a vulnerable tool boundary.

## Claim 4: Wrapper transferability varied across two open-weight models.

**Source artifact:** [`../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md`](../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md)

**Raw run folder:** `lab/vuln-agents/damn-vulnerable-llm-agent/`

**Reproduction command:**

```bash
cd lab/vuln-agents/damn-vulnerable-llm-agent
./run_scen2_sweep.sh
```

**Disclosure status:** green; intentionally vulnerable educational benchmark.

**Limitation:** n=5 per model/variant cell, temperature 0, two local open-weight models.

**Interview talking point:** Transferability cannot be assumed. Wrapper style affected models differently, which is exactly why agent-security evals need matrix design rather than one-off anecdotes.
