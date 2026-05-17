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

## Claim 2: A pre-registered cross-scale hypothesis (H7) was falsified: capability amplifies exploitation within the insecure substrate.

**Evidence:**

- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md>
- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md> (Addendum B)
- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/docs/preregistrations/2026-05-13-tier-a-w1-w5.md> (H7, registered before the cell ran)

**Result:** Holding substrate, payload, mitigation, and dispatch policy constant and varying only the model 8B to 70B (n=10): strict canary exfil 0/5 at 8B versus 10/10 at 70B (Wilson 95% CI [0.72, 1.0]). H7 (`|rate_70b - rate_8b| <= 0.15`) is falsified by 0.60.

**Disclosure:** green; open-weight Llama-3.3-70B via a free tier, same localhost-only harness and canary as the 8B cells; $0.

**Limitations:** n=10, single payload variant, single client; a mechanism-level qualitative mode shift, not a population rate. The confirmatory mitigation-tested grid (H10b-G) is in progress and gated; no H10b-G rate is claimed here.

## Claim 3: ReAct-loop observation injection can drive SQL injection in an intentionally vulnerable agent benchmark.

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

## Claim 4: Wrapper transferability varied across two open-weight models.

**Evidence:**

- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-cross-model-react-loop-injection.md>
- <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md>

**Disclosure:** green; lab-only benchmark evidence.

**Limitations:** n=5 per model/variant cell, temperature 0, two local open-weight models.

## Claim 5: Disclosure discipline is part of the portfolio, but no live target-specific report is claimed.

**Evidence:**

- The public portfolio contains disclosure-green lab artifacts.
- Target-specific testing and submission are outside the claims made by this public index.

**Disclosure:** no live target-specific submission is claimed by this public index.

**Limitations:** public evidence should not be treated as a production exploit or vendor-specific proof of vulnerability.
