# ai-redteam-notes: agent and MCP injection research, with an offline demo of the fix run in CI

This repo is my pre-registered research on prompt injection through tool output in AI agents and MCP clients, with an offline demo of the fix and a stdlib checker for the risky dispatch pattern.

**Proof.** On Groq-hosted Llama-3.3-70B with inline-XML tool dispatch (the agent client parses tool calls out of the model's text), a defensive system prompt (M1) cut canary exfiltration to 0/10 on two payload families and left a third (v7) at 10/10. With no prompt (M0) the three families leaked 9/10, 10/10 and 10/10. A chat-only control with the same model and the baseline payload but no XML dispatch leaked 0/10. My conclusion: fix this in the agent client (typed tool-call dispatch, with authorization and provenance checks outside the model), not in the prompt. A typed-dispatch agent has not been measured at 70B ([limits](#decisions-failures-limits)).

**Run it** (no API key, no install beyond Python 3; pytest for the last command):

```bash
make repro              # auditor self-check, sample audits, recount of the committed per-seed results
python3 -m pytest -q    # offline dispatcher demo and recount tests
```

[![CI](https://github.com/ChunkyTortoise/ai-redteam-notes/actions/workflows/ci.yml/badge.svg)](https://github.com/ChunkyTortoise/ai-redteam-notes/actions/workflows/ci.yml)

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

Metric for every measured row: strict bypass, meaning the canary file's contents arrived in a real callback to the localhost exfil sink. Intervals are Wilson 95%. "Recount" rows are reproduced offline from committed `seeds.json` by `make tally`; rows marked "entry only" come from the attack entry's hand-recomputed table because their run directories are not mirrored here.

| Metric (result) | n | Dataset / cell | Date | Model | Baseline | Reproduce |
|---|---:|---|---|---|---|---|
| Strict bypass, inline-XML + M1 prompt, payload v7: **10/10** [0.72, 1.00] | 10 | H10b-G, [M1 v7 seeds](lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v7/seeds.json) | 2026-05-18 | Groq llama-3.3-70b-versatile, T=0.7 | M0 v7: 10/10 (entry only) | `make tally` |
| Strict bypass, inline-XML + M1, payload v3: **0/10** [0.00, 0.28] | 10 | H10b-G, [M1 v3 seeds](lab/mcp-matrix/runs/2026-05-18-llama70b-xml-M1-v3/seeds.json) | 2026-05-18 | same | M0 v3: 10/10 [0.72, 1.00], [seeds](lab/mcp-matrix/runs/2026-05-17-llama70b-xml-M0-v3/seeds.json) (2026-05-17) | `make tally` |
| Strict bypass, inline-XML + M1, baseline payload: **0/10** | 10 | H10b-G | 2026-05-18 | same | M0 baseline: 9/10 (entry only) | entry only ([table](ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md#result)) |
| Strict bypass, chat-only control (no XML dispatch), M0, baseline payload: **0/10** [0.00, 0.28] | 10 | H10b-G CTRL-1b, [seeds](lab/mcp-matrix/runs/2026-05-18-llama70b-chatonly-M0-baseline/seeds.json) | 2026-05-18 | same | inline-XML M0 baseline: 9/10 (entry only) | `make tally` |
| Strict bypass, Cline-class inline-XML, M0, payload v1-visible-notice: **10/10** [0.72, 1.00] | 10 | F1, [seeds](lab/mcp-matrix/runs/2026-05-16-cline-70b-M0-f1/seeds.json) | 2026-05-16 | OpenRouter llama-3.3-70b-instruct:free | Llama-3.1-8B, same setup: 0/5 ([entry](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md)) | `make tally` |
| Fixture benchmark internal consistency: **10/10** fixtures match | 10 | [fixtures](EVALS/fixtures/tool-output-injection-fixtures.json) (preserved verdicts, no model calls) | rerun 2026-11-17 | none | none | `make benchmark` |
| Offline dispatcher demo: naive dispatcher reads the canary, typed dispatcher does not | 12 tests | scripted model output in [`demo/dispatch_demo.py`](demo/dispatch_demo.py) | rerun 2026-11-17 | none (scripted) | naive inline-tag dispatcher | `python3 -m pytest -q` |

Each number above is stated once here; scope is in [Decisions, failures, limits](#decisions-failures-limits) and [Methodology & limits](#methodology--limits).

## Quickstart

From a fresh clone, with Python 3.10+ and `make` (the last command fetches pytest into a throwaway env through [uv](https://docs.astral.sh/uv/); with pytest already installed, `python3 -m pytest -q` does the same):

```bash
git clone https://github.com/ChunkyTortoise/ai-redteam-notes.git && cd ai-redteam-notes
make repro       # auditor self-check, two sample config audits, recount of committed seeds.json
make benchmark   # re-score the preserved-run fixture benchmark
uv run --no-project --with pytest python -m pytest -q   # offline dispatcher demo + recount tests
```

Expected key lines (the full list is in [REPRODUCE.md](REPRODUCE.md)):

```text
substrate : inline-xml-dispatch
risk      : high
substrate : typed-toolcall-api
risk      : low
10/10 strict  wilson95=[0.7225, 1.0000]  llama-3.3-70b-versatile xml-parser M1 v7  2026-05-18-llama70b-xml-M1-v7
GATE: PASS - fixture benchmark is internally consistent
12 passed
```

`python3 demo/dispatch_demo.py` prints which tools each dispatcher executed. `make remediation-demo` runs the auditor on a vulnerable and a typed tool-call transcript.

What the demo shows: a toy agent loop where a fetched document (attacker-controlled) contains an inline `<file_read>` tag naming a canary file. A naive dispatcher that parses tool calls out of the model's free text reads the canary. A typed dispatcher that only runs schema-validated structured calls from a separate channel does not, and the legitimate structured `lab_fetch` call still runs.

What it does NOT show: the model output is scripted, not a live model, so it says nothing about how often a real model repeats injected text. It covers one attack shape (inline XML repeated in assistant text) and one typed-dispatch design. It adds no authorization or provenance checks, so if a model put the injected `file_read` into the structured channel, this typed dispatcher would run it (a test records this). It is not a measurement. The measured results above come from the lab runs, not this demo.

**Audit your own agent client.** Point the auditor at an MCP client config (JSON/JSONC) or a captured transcript (JSONL):

```bash
python3 lab/mcp-matrix/tools/substrate_auditor.py path/to/client-config.json --json
```

It exits 1 when it rates the input high-risk (inline-XML dispatch), 0 for low-risk or unknown, and 2 on a missing file; add `--strict` to make unknown exit 1 as well. It is a text heuristic over the config or transcript. In this repo's CI it only checks the two bundled samples (`--expect-risk`); it is not wired into any deploy step here. Usage, output fields and exit codes: [lab/mcp-matrix/tools/README.md](lab/mcp-matrix/tools/README.md).

**Read the evidence.** [REPORTS/START_HERE.md](REPORTS/START_HERE.md) is the shortest path from claim to evidence. In order:

1. [H10b-G 70B grid](ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md): control-validity gate passed; M1 is variant-selective.
2. [Substrate vs policy writeup](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md): the attribution correction, controlled isolation, and Addendum B/C.
3. [F1 cross-scale replication](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md): H7 falsified at 70B under the inline-XML substrate.
4. [DVL Agent Scenario 2](ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md): ReAct-loop observation injection driving SQL exfiltration, with tool-boundary mitigations.
5. [Lakera Gandalf walkthrough](CTF/2026-05-09-lakera-gandalf-walkthrough.md): scripted probe with value extraction, a feature-inference side channel, and system-prompt exfiltration.

All 16 dated attack entries in one table (class, target, technique, outcome, evidence): [ATTACKS/README.md](ATTACKS/README.md#attack-summary). MCP threats mapped to these findings: [docs/mcp-threat-model.md](docs/mcp-threat-model.md).

Also: [RESEARCH-SUMMARY.md](RESEARCH-SUMMARY.md) (the research arc), [remediation case study](REPORTS/remediation-case-study-tool-output-injection.md) (attack to fix in one place), [claim ledger](REPORTS/claim-ledger.md) (each claim with its evidence, limitation and do-not-claim boundary), [CASE_STUDIES.md](CASE_STUDIES.md).

Re-running the experiments themselves needs the private harness and a model provider key; see [limits](#decisions-failures-limits).

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

- **Pre-registration.** Each hypothesis has a dated file meant to be frozen before the cell that tested it ran, and deviations are recorded in the entry that reports the result ([index](docs/preregistrations/INDEX.md)). The freeze commits are in the private repo, so this public history cannot prove the ordering.
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

## Decisions, failures, limits

**Decisions**

| Decision | Why | Where it's argued |
|---|---|---|
| Fix the substrate (typed tool-call dispatch) before hardening prompts | M1 went from 0/10 (v3) to 10/10 (v7) on the same model by changing only the payload | [Remediation case study](REPORTS/remediation-case-study-tool-output-injection.md#why-the-fix-is-architectural) |
| Treat client tag-dispatch order (first, last or all tags) as part of the security boundary | It changes which injected call executes | [Substrate vs policy writeup](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md) |
| Open-weight models only | Reproducible and cheap; every H10b-G call logged `cost_usd=0.0` | [Open-weights rationale](REPORTS/open-weights-rationale.md) |
| Score strict bypass (canary in a real callback) apart from intent shift | At M0 intent shift was 10/10 on every payload, which would hide the M1 effect | [Methodology](REPORTS/2026-05-14-agent-security-eval-methodology.md) |
| Three-tier disclosure ladder, checked in CI | Only `green` entries are published | [SECURITY.md](SECURITY.md) |
| Heuristic auditor that triages review, not a safety proof | Declarative signals are all a config file offers | [Auditor limitations](lab/mcp-matrix/tools/README.md#limitations-read-this) |
| Register hypotheses first, publish the nulls | So the failures below cannot be dropped quietly | [Hypothesis ledger](docs/preregistrations/INDEX.md) |

The numbered ADRs that some entries cite (for example ADR-003, the disclosure policy) live in the private working repo.

**Failures (published on purpose)**

- **H7 falsified at 70B.** The registered assumption that a larger model would be safer failed: under the same inline-XML substrate, Llama-3.3-70B leaked 10/10 where Llama-3.1-8B leaked 0/5. [F1 entry](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md) · [pre-registration](docs/preregistrations/2026-05-13-tier-a-w1-w5.md)
- **H3 retracted.** A result that looked like one open-weight model being "more resistant" than another was a substrate confound: the two runs used different client dispatch substrates. [Writeup](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)
- **H6 falsified.** The combined-framing v7 payload produced no strict bypass at M0 in the 8B-class matrix within the registered seed budget.
- **H11 falsified.** Last-tag-wins dispatch produced no strict canary exfiltration; its one real callback carried placeholder data, not the canary. [Ablation entry](ATTACKS/2026-05-15-mcp-xml-last-tag-dispatch-ablation.md)
- **M2 regressed.** Naming the tools inside the mitigation prompt did worse than no mitigation on the 8B model: the names acted as a salience prime.
- **H10b-G deviated from its pre-registration.** It ran on Groq, not the frozen OpenRouter plan (Deviation 1), so it is not the pristine H10b run.

**Limits**

- n=10 per cell supports mechanism claims, not population rates. One model per cell, one substrate (inline-XML) in the 70B grid.
- No typed-dispatch agent was measured at 70B. The only typed cell is one simulated 8B run (fixture `kilo-typed-api-m0-clean`); at 70B the isolation evidence is the chat-only control.
- Re-running the experiments needs the private harness and a provider key. The payload text, the M1 prompt and transcripts are private, and the 50 `result_path` entries in the committed `seeds.json` files point to per-seed files that are not mirrored. `make tally` recounts the outcome flags, not the transcripts.
- Three of the seven H10b-G cells (M0 baseline, M0 v7, M1 baseline) have no `seeds.json` here; their numbers come from the entry's table.
- The offline demo uses scripted model output; it shows the mechanism, not a rate.
- Auditor failures found by an external audit on 2026-11-17 and fixed with regression cases in [`selfcheck.py`](lab/mcp-matrix/tools/selfcheck.py): the bare word `continue` in a config (for example `"onError":"continue"`) was rated typed/low; a nested dispatch field (`{"client":{"toolDispatch":"xml"}}`) returned `unknown`; a typed transcript whose tool message echoed an injected tag was rated high. Still open: inline syntaxes other than `<name>...</name>` (for example `<function=read_file>`) return `unknown`, and `unknown` exits 0 unless you pass `--strict`.
- Hypothesis freeze commits are in the private repo; this public history cannot prove each file predates its cell ([INDEX](docs/preregistrations/INDEX.md)).

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
- The auditor is a heuristic, not a guarantee. It reasons from declarative signals and cannot prove the absence of an inline-XML path. Unknown clients return `unknown` with a zero exit code (nonzero with `--strict`); treat them as potentially inline-XML until the dispatch code is reviewed. Transcript detection depends on the log schema.
- The benchmark is fixture-only: it re-scores preserved verdicts for internal consistency, makes no model calls, and does not re-run experiments.

**Tests, CI and private material**
- The pre-registered measurement harness and its pytest suite (`make test`) live in the private working repo. Their test-count and coverage figures appear in [REPRODUCE.md](REPRODUCE.md) and the Makefile but cannot be verified from this repo, so they are not cited as results; `make verify-public` prints `SKIP` for that step here.
- CI makes no network or model calls. The public-URL check runs only inside `make verify-public` and needs network access.
- The automated pre-push disclosure hook described in [SECURITY.md](SECURITY.md) is not part of this repo; here, disclosure frontmatter is enforced by `make public-surface` in CI.
- Two older ATTACKS entries (`2026-05-04-garak-fullsweep-llama31`, `2026-05-06-pair-agent-dvl-scenario1`) predate the current entry template and are outside the `verify-public` template check; their disclosure status is still checked.

**Model coverage**
- Open-weight models only; no frontier-model cells. One negative lab entry ran Claude Desktop against a self-hosted MCP server (0/5, [entry](ATTACKS/2026-05-13-pair-matrix-m0-claude-desktop-negative.md)); it is not a cell in the measured grids. <!-- TODO(Cayman): confirm this wording; the 2026-05-13 Claude Desktop entry and "open-weight models only" read as a contradiction to a careful reviewer. --> The H10 frontier pre-registration is gated, and no rates are stated for it ([rationale](REPORTS/open-weights-rationale.md)).

</details>

## Roadmap

- **H10 frontier substrate replication**, once its control cell clears the gate ([pre-registration](docs/preregistrations/2026-05-15-frontier-substrate-h10.md)); and frontier rows if access allows: Cline + Claude Sonnet, Cline + GPT-5.x, a cross-frontier M0-M3 sweep ([what would change](REPORTS/open-weights-rationale.md#what-would-change-with-frontier-model-access)).
- **A registered amplification test** for the 70B-versus-8B susceptibility direction ([H10b-G limitations](ATTACKS/2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md#limitations)).
- **Cross-client parser comparisons** (D-lane: Windsurf, Continue.dev, Roo Code) and cross-payload generalization of F1 ([F1 limitations](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md#limitations), [assessment follow-up](REPORTS/substrate-vs-policy-assessment.md#limitations)).

## License

Dual: code under MIT, research content (ATTACKS/, WRITEUPS/, REPORTS/, EVALS/, CTF/) under CC BY 4.0. See [LICENSE](LICENSE).
