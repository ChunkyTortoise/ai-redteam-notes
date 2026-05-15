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

**Claim ledger:** [`claim-ledger.md`](claim-ledger.md)

**Proof layer:**

- [`start-here-for-hiring-reviewers.md`](start-here-for-hiring-reviewers.md)
- [`2026-05-15-agent-product-security-remediation-review.md`](2026-05-15-agent-product-security-remediation-review.md)
- [`claim-ledger.md`](claim-ledger.md)
- [`mcp-reproducibility-checklist.md`](mcp-reproducibility-checklist.md)
- [`2026-05-14-agent-security-eval-methodology.md`](2026-05-14-agent-security-eval-methodology.md)
- [`2026-05-14-evidence-traceability-manifest.md`](2026-05-14-evidence-traceability-manifest.md)
- [`../lab/mcp-matrix/README.md`](../lab/mcp-matrix/README.md)

## Claim 1a: The May 14 n=10 replication narrowed the MCP claim rather than confirming reliable exfiltration.

**Evidence:**

- [`2026-05-14-mcp-n10-replication-negative-result.md`](2026-05-14-mcp-n10-replication-negative-result.md)
- [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md)
- [`mcp-reproducibility-checklist.md`](mcp-reproducibility-checklist.md)

**Command shape:**

See the preserved run command: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md)

To verify the harness logic without rerunning the model cell:

```bash
uv run pytest lab/mcp-matrix/harness/tests
```

**Disclosure:** lab-only, disclosure-green.

**Limitations:** one model, one payload, one XML-style substrate emulation, n=10. The result supports a narrow intent-layer claim, not reliable data theft.

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

**Remediation review:** [`2026-05-15-agent-product-security-remediation-review.md`](2026-05-15-agent-product-security-remediation-review.md)

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

## Claim 5: The strongest hiring signal is remediation-oriented security judgment, not only attack discovery.

**Evidence:**

- [`2026-05-15-agent-product-security-remediation-review.md`](2026-05-15-agent-product-security-remediation-review.md)
- [`hiring-reviewer-map.md`](hiring-reviewer-map.md)

**Command shape:**

The public remediation review is prose-only. The private source repo also keeps a small pytest remediation-proof lab for local regression framing.

**Disclosure:** lab-only, disclosure-green.

**Limitations:** the remediation review is an engineering judgment artifact, not a claim that the public repo contains production exploit code or vendor-specific proof.
