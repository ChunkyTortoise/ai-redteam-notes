# Hiring Reviewer Map

**Date:** 2026-05-18
**Status:** reviewer-ready
**Purpose:** Help a recruiter, hiring manager, or technical interviewer reach the strongest AI red-team evidence quickly without exploring the repo cold.

## Hiring Thesis

Cayman can run scoped, reproducible AI-agent security experiments; distinguish model behavior from client substrate behavior; pre-register falsifiable hypotheses and report honestly when they are falsified; measure mitigation boundaries instead of assuming them; write disclosure-safe reports; and translate findings into defender recommendations.

## 60-second Path

Start from the packet-ready router: [`REPORTS/start-here-for-hiring-reviewers.md`](../../REPORTS/start-here-for-hiring-reviewers.md).

1. **H10b-G 70B substrate grid:** [`ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md`](../../ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md)
   - Proves the 70B substrate effect survives the chat-only control gate and that M1 prompt scaffolding is variant-selective: baseline/v3 held, v7 bypassed.
2. **Substrate vs policy writeup:** [`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`](../../WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)
   - Proves the original model-policy attribution was wrong, matters because it isolates client dispatch substrate as the load-bearing variable, and is bounded to measured MCP-style inline-XML versus typed-tool-call substrates.
   - Public version: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md>
3. **Cross-scale F1 replication ATTACKS entry:** [`ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md`](../../ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md)
   - Proves a pre-registered cross-scale hypothesis failed at 70B, matters because capability amplified exploitation inside the insecure substrate, and is bounded to one payload, one client class, and n=10.
   - Public version: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md>
4. **DVL Scenario 2 ATTACKS entry:** [`ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md`](../../ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md)
   - Proves ReAct-loop observation injection can drive SQL exfiltration in a vulnerable agent benchmark, matters because it translates to tool-boundary mitigations, and is bounded to localhost lab evidence.
   - Public version: <https://github.com/ChunkyTortoise/ai-redteam-notes/blob/main/ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md>

## 5-Minute Path

Read the first three artifacts above, then skim:

- [`WRITEUPS/2026-05-14-cross-model-react-loop-injection.md`](../../WRITEUPS/2026-05-14-cross-model-react-loop-injection.md) for the broader cross-model analysis behind the DVL Scenario 2 entry.
- [`docs/preregistrations/2026-mcp-matrix.md`](../preregistrations/2026-mcp-matrix.md) for the pre-registered MCP matrix design.
- [`docs/preregistrations/2026-05-13-tier-a-w1-w5.md`](../preregistrations/2026-05-13-tier-a-w1-w5.md) for **H7**, the cross-scale hypothesis that was registered before the F1 cell ran and then falsified.
- [`docs/preregistrations/2026-05-16-open-source-scale-substrate-h10b.md`](../preregistrations/2026-05-16-open-source-scale-substrate-h10b.md) and [`REPORTS/2026-05-17-h10b-g-70b-substrate-findings.md`](../../REPORTS/2026-05-17-h10b-g-70b-substrate-findings.md) for the H10b-G preregistration, provider deviation, control gate, and M1 boundary.
- [`REPORTS/substrate-vs-policy-assessment.md`](../../REPORTS/substrate-vs-policy-assessment.md) for the concise public-safe assessment and caveats.

The 5-minute story is: a substrate-attribution study, a pre-registered cross-scale replication that falsified its own hypothesis (capability amplifies exploitation, it does not wash out at 70B), a full H10b-G mitigation grid showing M1 is variant-selective, a concrete vulnerable-agent exploitation study, and a disclosure-readiness packet that ties the work to real-world reporting norms.

For the attack-to-fix version of the same story, read [`REPORTS/remediation-case-study-tool-output-injection.md`](../../REPORTS/remediation-case-study-tool-output-injection.md). It ties the exploit evidence to `substrate_auditor.py`, the typed tool-call architectural control, fixture benchmark, and detection hooks.

## Deep technical Path

- MCP matrix raw evidence:
  - [`lab/mcp-matrix/runs/2026-05-17-llama70b-xml-M0-v3/seeds.json`](../../lab/mcp-matrix/runs/2026-05-17-llama70b-xml-M0-v3/seeds.json)
  - [`lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v3/seeds.json`](../../lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v3/seeds.json)
  - [`lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v7/seeds.json`](../../lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v7/seeds.json)
  - [`lab/mcp-matrix/runs/2026-05-18-llama70b-chatonly-M0-baseline/seeds.json`](../../lab/mcp-matrix/runs/2026-05-18-llama70b-chatonly-M0-baseline/seeds.json)
  - [`lab/mcp-matrix/runs/2026-05-10-llama-xml-M1-v7-dispatch-all-tags/`](../../lab/mcp-matrix/runs/2026-05-10-llama-xml-M1-v7-dispatch-all-tags/)
  - [`lab/mcp-matrix/runs/2026-05-13-cline-M0/summary.md`](../../lab/mcp-matrix/runs/2026-05-13-cline-M0/summary.md)
- DVL Scenario 2 raw evidence:
  - [`lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/`](../../lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/)
  - [`lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/wilson_summary.json`](../../lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/wilson_summary.json)
- Harness and gate evidence:
  - [`pipeline/scripts/check-disclosure.sh`](../../pipeline/scripts/check-disclosure.sh)
  - [`EVALS/agent-tool-output-injection-benchmark.md`](../../EVALS/agent-tool-output-injection-benchmark.md)
  - [`REPORTS/remediation-case-study-tool-output-injection.md`](../../REPORTS/remediation-case-study-tool-output-injection.md)

## Role-Specific Evidence Blocks

Use [`REPORTS/start-here-for-hiring-reviewers.md`](../../REPORTS/start-here-for-hiring-reviewers.md) as the source of truth for packet-ready role blocks. Each role has exactly three links: one flagship artifact, one raw-evidence or pre-registration artifact, and one defensive or operational artifact.

## Known limitations and How to Discuss Them

- **Small-n cells:** Several matrix cells are n=5 and some early exploratory cells are n=1. Discuss these as directional, reproducible lab evidence rather than population-level rates.
- **Localhost and lab-only evidence:** The strongest artifacts are intentionally scoped to local harnesses, open-weight models, and vulnerable benchmarks. That is a safety choice, not a claim of production exploitation.
- **Substrate-specific claims:** The MCP finding is about typed tool-call API versus inline text/XML parser substrates. Do not generalize it to every MCP client without measuring the client dispatch path.
- **H10b-G boundary:** H10b-G is packet-ready but still one provider/model family: Groq-hosted Llama-3.3-70B, inline-XML substrate, n=10 cells, lab-only canaries. Discuss it as a strong mitigation-boundary result, not a production exploit or frontier-model benchmark.
- **Cross-scale (F1 / H7) boundary:** The F1 70B falsification is n=10, single payload variant (v1-visible-notice), single client (Cline inline-xml), open-weight model on a free inference tier. Discuss it as a decisive *mechanism-level* mode shift (0/5 to 10/10 strict exfil), not a population rate across payloads or vendors.
- **DVL nested repo evidence:** The Day-60 operational DVL evidence includes a local-only nested commit noted in the handoff. Treat that as private/local evidence until a public-safe copy path or writable fork exists.
- **Public mirror sync risk:** Public links should be checked before use because private repo artifacts and public mirror artifacts can drift.
- **Public assessment report:** `REPORTS/substrate-vs-policy-assessment.md` is live in the public mirror as a concise companion report. Still re-run public URL verification immediately before sending packets.
- **Remediation case study:** `REPORTS/remediation-case-study-tool-output-injection.md` is a hiring-facing synthesis artifact. Keep it aligned with the benchmark fixture count and the H10b-G claim boundary.

## What not publish Yet

- Vendor-specific target claims before explicit target approval and in-scope verification.
- Production reproduction steps or target-specific PoCs before coordinated disclosure clearance.
- Secrets, test account identifiers, bearer tokens, environment file contents, or burner-account details.
- Unfetchable nested DVL commits or local-only paths as public evidence.
- Draft LinkedIn packets as if they were already posted.

## Public Sync Plan

Public mirror sync should be a separate reviewed step. Before syncing:

1. Confirm every proposed public path exists locally.
2. Run private-path and secret-pattern checks over the candidate files.
3. Exclude local-only nested DVL evidence unless copied into a public-safe artifact.
4. Re-check GitHub URLs after push.
5. Keep target-specific CVD drafts private until submission approval and disclosure clearance.
