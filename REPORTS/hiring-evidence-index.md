# Hiring Evidence Index

**Status:** public
**Purpose:** Tie public hiring claims to artifacts, commands, limitations, and disclosure status.

## Claim 1: Client substrate can be the load-bearing variable in MCP tool-output indirect prompt injection.

**Evidence:**

- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md>
- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/REPORTS/substrate-vs-policy-assessment.md>

**Command shape:**

```bash
cd lab/mcp-matrix
just test
```

**Disclosure:** lab-only, disclosure-green.

**Limitations:** small-n cells, localhost harness, open-weight models, and substrate-specific claims.

## Claim 2: ReAct-loop observation injection can drive SQL injection in an intentionally vulnerable agent benchmark.

**Evidence:**

- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md>
- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-cross-model-react-loop-injection.md>

**Command shape:**

```bash
cd lab/vuln-agents/damn-vulnerable-llm-agent
./run_scen2_sweep.sh
```

**Disclosure:** green; intentionally vulnerable educational benchmark.

**Limitations:** local benchmark evidence only; mitigation lesson should be framed around tool-boundary validation and parameterized SQL.

## Claim 3: Wrapper transferability varied across two open-weight models.

**Evidence:**

- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-cross-model-react-loop-injection.md>
- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md>

**Disclosure:** green; lab-only benchmark evidence.

**Limitations:** n=5 per model/variant cell, temperature 0, two local open-weight models.

## Claim 4: Disclosure discipline is part of the portfolio, but no live target-specific report is claimed.

**Evidence:**

- The public portfolio contains disclosure-green lab artifacts.
- Target-specific testing and submission are outside the claims made by this public index.

**Disclosure:** no live target-specific submission is claimed by this public index.

**Limitations:** public evidence should not be treated as a production exploit or vendor-specific proof of vulnerability.
