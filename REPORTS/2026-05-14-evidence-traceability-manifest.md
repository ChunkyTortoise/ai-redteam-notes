# Evidence Traceability Manifest

**Date:** 2026-05-14
**Status:** public
**Purpose:** map flagship claims to artifacts, commands and limitations.

## Claim 1: Client substrate can be the load-bearing variable in MCP tool-output indirect prompt injection.

**Source artifact:** [`../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)

**Raw run folders:** `../lab/mcp-matrix/runs/`

**Reproduction command:**

```bash
# Private repo only: not in this public mirror. From here, run make repro and make tally at the repo root.
cd lab/mcp-matrix
just test
```

**Disclosure status:** green; localhost-only lab evidence.

**Limitation:** substrate-specific, small-n, local open-weight model evidence. The claim is about observed client dispatch behavior, not every MCP client or model.

## Claim 2: The May 14 n=10 replication weakened strict exfiltration while preserving a narrow intent-layer signal.

**Source artifact:** [`2026-05-14-mcp-n10-replication-negative-result.md`](2026-05-14-mcp-n10-replication-negative-result.md)

**Raw run folder:** [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/)

**Reproduction command:** [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md)

**Disclosure status:** green; localhost-only synthetic canary evidence.

**Limitation:** one model, one payload, one substrate emulation, n=10. It does not establish a production exploit rate.

## Claim 3: ReAct-loop observation injection can drive SQL injection in an intentionally vulnerable agent benchmark.

**Source artifact:** [`../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md`](../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md)

**Raw run folder:** `lab/vuln-agents/damn-vulnerable-llm-agent/`

**Reproduction command:**

```bash
# Private repo only: not in this public mirror. From here, run make repro and make tally at the repo root.
cd lab/vuln-agents/damn-vulnerable-llm-agent
./run_scen2_sweep.sh
```

**Disclosure status:** green; intentionally vulnerable educational benchmark.

**Limitation:** benchmark-local evidence. The mitigation lesson is tool-boundary validation and parameterized SQL, not a claim about a live product.

## Claim 4: Wrapper transferability varied across two open-weight models.

**Source artifact:** [`../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md`](../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md)

**Raw run folder:** `lab/vuln-agents/damn-vulnerable-llm-agent/`

**Reproduction command:**

```bash
# Private repo only: not in this public mirror. From here, run make repro and make tally at the repo root.
cd lab/vuln-agents/damn-vulnerable-llm-agent
./run_scen2_sweep.sh
```

**Disclosure status:** green; intentionally vulnerable educational benchmark.

**Limitation:** n=5 per model/variant cell, temperature 0, two local open-weight models.

