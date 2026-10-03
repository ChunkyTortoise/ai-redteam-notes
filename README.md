# ai-redteam-notes: agent and MCP injection research, with the fix wired into CI

When an AI agent reads tool output an attacker controls, can it be tricked into leaking data? In a pre-registered experiment on Llama-3.3-70B, a defensive system prompt blocked two families of injection payloads and did nothing against a third ([Results](#results)). With the same model and payloads but without inline-XML tool dispatch, nothing leaked. My conclusion is architectural: fix it in the agent client (typed tool-call dispatch, with authorization and provenance checks outside the model), not in the prompt. A typed-dispatch agent has not been measured at 70B yet ([limits](#methodology--limits)).

This repo holds the experiments, the hypotheses that failed along the way (published, not hidden), and `substrate_auditor.py`, a dependency-free check for the risky dispatch pattern that runs in CI. All published experiments are lab-only and disclosure-green ([scope](#methodology--limits), [SECURITY.md](SECURITY.md)).

[![CI](https://github.com/ChunkyTortoise/ai-redteam-notes/actions/workflows/ci.yml/badge.svg)](https://github.com/ChunkyTortoise/ai-redteam-notes/actions/workflows/ci.yml)
[![Reproducible](https://img.shields.io/badge/repro-make%20repro%20(no%20API%20key)-success)](REPRODUCE.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

```mermaid
flowchart LR
  A["Untrusted tool output"] --> B["Inline text/XML dispatch"]
  B --> C["Local canary read"]
  C --> D["Outbound exfil attempt"]
  B --> E["substrate_auditor flags high risk"]
  E --> F["Typed tool-call substrate"]
  F --> G["Detection and benchmark gates"]
```

## Results

| Kind | Result | Value | Source |
|---|---|---|---|
| Measured | H10b-G: strict canary exfiltration through inline-XML tool dispatch on Groq-hosted Llama-3.3-70B, 7-cell grid, n=10 seeds per cell | M1 scaffold: **0/10** on baseline and v3 payloads, **10/10** on v7. Same payloads without it (M0): **9/10**, **10/10**, **10/10**. Chat-only control (no XML dispatch): **0/10** | [H10b-G entry, Result](ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md#result) · per-seed runs: [M0 v3](lab/mcp-matrix/runs/2026-05-17-llama70b-xml-M0-v3/seeds.json), [M1 v3](lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v3/seeds.json), [M1 v7](lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v7/seeds.json), [control](lab/mcp-matrix/runs/2026-05-18-llama70b-chatonly-M0-baseline/seeds.json) |
| CI gate | On every PR and every push to `main`: the auditor self-check, the auditor must rate the inline-XML sample high-risk and the typed sample low-risk, and the fixture benchmark must re-score cleanly | **7** self-check cases plus a missing-file guard · **10/10** benchmark fixtures match | [`ci.yml`](.github/workflows/ci.yml) · [`selfcheck.py`](lab/mcp-matrix/tools/selfcheck.py) · [`Makefile`](Makefile) (`audit`, `--expect-risk`) · [benchmark fixtures](EVALS/fixtures/tool-output-injection-fixtures.json) |
| Inventory | Dated pre-registrations, each frozen before the cells it governs | **4** files in this repo | [`docs/preregistrations/`](docs/preregistrations/) · [hypothesis ledger](docs/preregistrations/INDEX.md) |

This table is the one place each number is stated. The scope of each one is in [Methodology & limits](#methodology--limits).

### What didn't hold (published on purpose)

- **H7 falsified at 70B.** The pre-registered assumption that a larger model would be safer here failed. Under the same inline-XML substrate, Llama-3.3-70B was exploited more reliably than Llama-3.1-8B, not less: capability amplifies exploitation inside an insecure substrate. [F1 entry](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md) · [pre-registration](docs/preregistrations/2026-05-13-tier-a-w1-w5.md)
- **H3 retracted.** A result that looked like one open-weight model being "more robust" than another was a substrate confound: the two runs used different client dispatch substrates. [Writeup](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)
- **H6 falsified.** The combined-framing v7 payload produced no strict bypass at M0 in the 8B-class matrix within the registered seed budget.
- **H11 falsified.** Last-tag-wins dispatch produced no strict canary exfiltration; its one real callback carried placeholder data, not the canary. [Ablation entry](ATTACKS/2026-05-15-mcp-xml-last-tag-dispatch-ablation.md)
- **M2 regressed.** Naming the tools inside the mitigation prompt did worse than no mitigation on the 8B model: the names acted as a salience prime.
- **M1 is not a substrate fix.** It is useful defense in depth, but the v7 row in [Results](#results) shows it can be fully transparent to one payload family.

Full ledger: [docs/preregistrations/INDEX.md](docs/preregistrations/INDEX.md). Research that hides its nulls is less trustworthy than research that reports them.

## Quickstart

**1. Run the defensive checks (no API key, no GPU, no install).** Python 3 standard library only, from the repository root:

```bash
make repro             # auditor self-check, then audit two sample MCP client configs
make remediation-demo  # same auditor on a vulnerable vs a typed tool-call transcript
make benchmark         # re-score the preserved-run fixture benchmark
```

Expected key lines (the full list is in [REPRODUCE.md](REPRODUCE.md)):

```text
substrate : inline-xml-dispatch
risk      : high
substrate : typed-toolcall-api
risk      : low
GATE: PASS - fixture benchmark is internally consistent
```

**2. Audit your own agent client.** Point the auditor at an MCP client config (JSON/JSONC) or a captured transcript (JSONL):

```bash
python3 lab/mcp-matrix/tools/substrate_auditor.py path/to/client-config.json --json
```

It exits non-zero when it detects inline-XML dispatch, so it can gate a CI or deploy step. Usage, output fields and exit codes: [lab/mcp-matrix/tools/README.md](lab/mcp-matrix/tools/README.md).

**3. Start here: read the evidence.** [REPORTS/START_HERE.md](REPORTS/START_HERE.md) is the shortest path from claim to evidence. In order:

1. [H10b-G 70B grid](ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md): control-validity gate passed; M1 is variant-selective.
2. [Substrate vs policy writeup](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md): the attribution correction, controlled isolation, and Addendum B/C.
3. [F1 cross-scale replication](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md): H7 falsified at 70B under the inline-XML substrate.
4. [DVL Agent Scenario 2](ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md): ReAct-loop observation injection driving SQL exfiltration, with tool-boundary mitigations.
5. [Lakera Gandalf walkthrough](CTF/2026-05-09-lakera-gandalf-walkthrough.md): scripted probe with value extraction, a feature-inference side channel, and system-prompt exfiltration.

Also: [RESEARCH-SUMMARY.md](RESEARCH-SUMMARY.md) (the research arc), [remediation case study](REPORTS/remediation-case-study-tool-output-injection.md) (attack to fix in one place), [claim ledger](REPORTS/claim-ledger.md) (each claim with its evidence, limitation and do-not-claim boundary), [CASE_STUDIES.md](CASE_STUDIES.md).

Re-running the experiments themselves needs the private harness and a model provider key; see [Methodology & limits](#methodology--limits).

## How it works

The diagram at the top is the chain under test and where the defense sits.

- **The attack.** An agent fetches a document whose body the attacker controls; the user is benign. If the client parses tool calls out of the assistant's text (inline-XML dispatch), injected text can become a tool call that reads a local canary and sends it to an outbound sink. A strict bypass requires the canary to land in a real callback to the localhost sink ([scenario](ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md#scenario)).
- **The variable that matters.** Holding the model and payloads constant, only the configuration with an inline-XML tag parser reproduced the bypass; a typed tool-use API substrate and a scaffold-prompt-only probe did not (H5, [research arc](RESEARCH-SUMMARY.md#the-arc)).
- **Mitigations, in order.** Substrate first (typed tool-call dispatch), provenance and authorization outside the model second, prompt hardening third. A short tool-agnostic content-trust prompt (M1) helps as defense in depth; tool-naming prompts (M2) can backfire ([why the fix is architectural](REPORTS/remediation-case-study-tool-output-injection.md#why-the-fix-is-architectural)).
- **Dispatch order is a security boundary.** Whether a client acts on the first tag, the last tag or all tags changes what an injection can do, so that choice should be documented and audited ([writeup](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)).
- **The auditor.** `substrate_auditor.py` classifies a config or transcript as `inline-xml-dispatch`, `typed-toolcall-api` or `unknown` and recommends a mitigation ([tool README](lab/mcp-matrix/tools/README.md)).
- **Detection.** Untrusted fetch, then sensitive read, then outbound send becomes an alertable chain ([detections](DETECTIONS/tool-chain-detections.md), [mock incident triage](DETECTIONS/mock-incident-triage-tool-output-injection.md)).

<details>
<summary>Repository layout</summary>

| Path | Purpose |
|---|---|
| `ATTACKS/` | Dated attack entries with threat model, proof of concept, result, mitigation and disclosure frontmatter |
| `WRITEUPS/` | Long-form research writeups |
| `REPORTS/` | Start-here router, assessments, claim ledger, remediation case study |
| `docs/preregistrations/` | Dated pre-registrations and the hypothesis ledger |
| `docs/reports/` | Reading map and claim-to-evidence index |
| `EVALS/` | Fixture-only benchmark artifacts and scorer |
| `DETECTIONS/` | Operational detection and incident-triage companion notes |
| `lab/` | MCP matrix run evidence and the `substrate_auditor` tool; promptfoo run outputs |
| `CTF/` | CTF walkthroughs and probe scripts |
| `pipeline/scripts/` | Disclosure, secrets, link and public-surface gate scripts |
| `site/` | GitHub Pages landing page |

</details>

## How it's evaluated

- **Pre-registration.** Each hypothesis was frozen in a dated file before the cell that tested it ran, and deviations are recorded in the entry that reports the result ([index](docs/preregistrations/INDEX.md)).
- **Control-validity gate.** A bypass is attributed to the substrate only if a chat-only control with the identical payload holds clean. H10b-G's control did (see [Results](#results)).
- **Strict scoring with intervals.** Strict bypass (canary in a real exfil callback) is scored separately from intent shift, and cell rates carry Wilson intervals; H10b-G's were hand-recomputed from the result JSON ([methodology](REPORTS/2026-05-14-agent-security-eval-methodology.md)).
- **CI gate, every PR and every push to `main`** ([`ci.yml`](.github/workflows/ci.yml), no network or model calls): `make repro` (auditor self-check plus expected-risk audits), `make benchmark` (fixture re-score), and `make public-surface` (disclosure frontmatter on every dated ATTACKS entry, secret-pattern scan, local link check, no future-dated artifacts, no private paths).
- **Pre-publication gate.** `make verify-public` adds the remediation demo, entry-template and disclosure checks on the published ATTACKS entries, and a network check that public GitHub links resolve.
- **Disclosure ladder.** Every ATTACKS entry is `green`, `yellow` or `red`; only `green` is public ([SECURITY.md](SECURITY.md)).

Run the same checks locally:

```bash
make repro && make benchmark && make public-surface   # what CI runs
make verify-public                                    # pre-publication gate; needs network
make help                                             # every target
```

## Design decisions

| Decision | Where it's argued |
|---|---|
| Fix the substrate (typed tool-call dispatch) before hardening prompts | [Remediation case study](REPORTS/remediation-case-study-tool-output-injection.md#why-the-fix-is-architectural) |
| Treat client tag-dispatch order as part of the security boundary | [Substrate vs policy writeup](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) |
| Open-weight models only, for reproducibility and cost discipline | [Open-weights rationale](REPORTS/open-weights-rationale.md) |
| A three-tier disclosure ladder, linted in CI | [SECURITY.md](SECURITY.md) |
| A heuristic auditor that triages review rather than proving safety | [Auditor limitations](lab/mcp-matrix/tools/README.md#limitations-read-this) |
| Register hypotheses first, then publish the nulls | [Hypothesis ledger](docs/preregistrations/INDEX.md) |

The numbered ADRs that some entries cite (for example ADR-003, the disclosure policy) live in the private working repo.

## Methodology & limits

<details>
<summary>What each number covers, and what is not established here</summary>

**Scope**
- Every experiment targets intentionally vulnerable benchmarks (DVL Agent, vuln-agent), open-weight models via public APIs, or localhost harnesses. No production system or hosted vendor is tested without prior authorization. Canary and exfil sinks are localhost only ([SECURITY.md](SECURITY.md)).
- Nothing here is a production-vendor vulnerability claim, a population rate, or a frontier-model benchmark.

**H10b-G (the Measured row)**
- Single provider and model: Groq-hosted Llama-3.3-70B-versatile, completed 2026-05-18. This deviates from the frozen OpenRouter pre-registration (Deviation 1), so it is not the pristine H10b run ([use boundary](REPORTS/START_HERE.md#use-boundary), [entry limitations](ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md#limitations)).
- Single substrate (inline-XML). Cross-client variation is isolated in separate D-lane cells.
- Cells are small: they support mechanism-level claims, not population rates. Wilson intervals are 95%. A registered amplification test is still owed for the post-hoc "70B is more susceptible than 8B" direction note.
- Per-seed `seeds.json` for M0 v3, M1 v3, M1 v7 and the control are in this repo. The M0 baseline, M0 v7 and M1 baseline figures come from the entry's hand-recomputed results table; those run directories, the sweep script and the provider call log are not mirrored.

**H7 / F1 (What didn't hold)**
- One payload (v1-visible-notice), one client class, OpenRouter `:free` tier (quantization and inference details are provider-controlled).
- The 8B comparison baseline was n=5 on a free inference tier, smaller than the 70B cell, so the comparison is directional and the 8B interval is wide ([F1 limitations](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md#limitations)).

**Typed-substrate evidence**
- "Typed dispatch is the fix" is architectural reasoning backed by thin measurement. The typed (Kilo-class) cell is a single simulated 8B run ([fixture](EVALS/fixtures/tool-output-injection-fixtures.json), `kilo-typed-api-m0-clean`). At 70B the isolation check is the chat-only control, not a typed substrate.
- The headless XML-substrate harness diverges from the real Cline UI: no multi-turn user, no IDE workspace context, no per-tool-call approval UI ([writeup limitations](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md#limitations-and-future-work)).
- Several earlier 8B cells are n=5, and some exploratory cells are n=1 ([assessment limitations](REPORTS/substrate-vs-policy-assessment.md#limitations)).

**Auditor and benchmark**
- The auditor is a heuristic, not a guarantee. It reasons from declarative signals and cannot prove the absence of an inline-XML path. Unknown clients return `unknown` with a zero exit code; treat them as potentially inline-XML until the dispatch code is reviewed. Transcript detection depends on the log schema.
- The benchmark is fixture-only: it re-scores preserved verdicts for internal consistency, makes no model calls, and does not re-run experiments.

**Tests, CI and private material**
- The pre-registered measurement harness and its pytest suite (`make test`) live in the private working repo. Their test-count and coverage figures appear in [REPRODUCE.md](REPRODUCE.md) and the Makefile but cannot be verified from this repo, so they are not cited as results; `make verify-public` prints `SKIP` for that step here.
- CI makes no network or model calls. The public-URL check runs only inside `make verify-public` and needs network access.
- The automated pre-push disclosure hook described in [SECURITY.md](SECURITY.md) is not part of this repo; here, disclosure frontmatter is enforced by `make public-surface` in CI.
- Two older ATTACKS entries (`2026-05-04-garak-fullsweep-llama31`, `2026-05-06-pair-agent-dvl-scenario1`) predate the current entry template and are outside the `verify-public` template check; their disclosure status is still checked.

**Model coverage**
- Open-weight models only; no frontier-model cells. The H10 frontier pre-registration is gated, and no rates are stated for it ([rationale](REPORTS/open-weights-rationale.md)).

</details>

## Roadmap

- **H10 frontier substrate replication**, once its control cell clears the gate ([pre-registration](docs/preregistrations/2026-05-15-frontier-substrate-h10.md)); and frontier rows if access allows: Cline + Claude Sonnet, Cline + GPT-5.x, a cross-frontier M0-M3 sweep ([what would change](REPORTS/open-weights-rationale.md#what-would-change-with-frontier-model-access)).
- **A registered amplification test** for the 70B-versus-8B susceptibility direction ([H10b-G limitations](ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md#limitations)).
- **Cross-client parser comparisons** (D-lane: Windsurf, Continue.dev, Roo Code) and cross-payload generalization of F1 ([F1 limitations](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md#limitations), [assessment follow-up](REPORTS/substrate-vs-policy-assessment.md#limitations)).

## License

MIT
