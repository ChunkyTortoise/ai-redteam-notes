# substrate_auditor

A defensive companion to the substrate-vs-policy research. It turns the finding
into a usable check: given an MCP client config (JSON / JSONC) or a captured
transcript (JSONL), it classifies the tool-dispatch substrate and recommends a
mitigation.

For hiring reviewers, this is the reusable deliverable: it converts the research
claim into a dependency-free CI/pre-deploy check. The fastest path is:

```bash
make repro
make remediation-demo
```

The companion case study is
`REPORTS/remediation-case-study-tool-output-injection.md`.

## Why

The research result (`WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md`) is that the
client's tool-dispatch substrate, not the model, is the load-bearing variable in
MCP tool-output indirect prompt injection, and that the inline-XML risk does not
diminish at larger model scale (Addendum B: it strengthens). The defensive
consequence is operational: before trusting an agent deployment, determine which
substrate it uses. This tool automates that first check.

## Usage

```bash
python lab/mcp-matrix/tools/substrate_auditor.py <path-to-config-or-transcript>
python lab/mcp-matrix/tools/substrate_auditor.py client.json --json
make audit
make remediation-demo
```

Exit code: `1` when a high-risk (inline-XML dispatch) substrate is detected,
`0` for typed/low-risk or unknown, `2` on a missing file. This makes it usable
as a CI / pre-deploy gate.

Output fields: `substrate` (`inline-xml-dispatch` | `typed-toolcall-api` |
`unknown`), `risk`, `rationale`, `recommendation`, `citation`.

## Expected output

Risky inline-XML sample:

```text
substrate : inline-xml-dispatch
risk      : high
why       : client identified as 'cline' (parser audit, Addendum A)
recommend : Prefer a typed tool-use API substrate ...
```

Typed tool-call sample:

```text
substrate : typed-toolcall-api
risk      : low
why       : explicit dispatch field 'toolDispatch'='structured'
recommend : Typed tool-use API substrate detected ...
```

JSON mode is intended for CI:

```bash
python lab/mcp-matrix/tools/substrate_auditor.py lab/mcp-matrix/tools/samples/cline-sample.json --json
```

## What it checks

- **Config:** an explicit dispatch field (`toolParser`, `toolDispatch`,
  `substrate`, ...) wins; otherwise the client identity is matched against the
  audited registry (Cline = inline-xml; Kilo Code / Continue.dev = typed, per
  Addendum A of the writeup).
- **Transcript:** structured `tool_calls` events imply a typed substrate; inline
  tool-dispatch tags in assistant content with no structured calls imply
  inline-XML. A transcript showing both is reported as inline-XML because the
  inline path is the exploitable one.

## Limitations (read this)

This is a **heuristic, not a guarantee.**

- It reasons from declarative signals. It cannot prove the absence of an
  inline-XML dispatch path; a config can look typed while the client still
  scans assistant text for tags.
- The client registry is conservative and only contains clients actually
  audited. Unknown clients return `unknown`, which should be treated as
  potentially inline-XML until the dispatch code is inspected.
- Transcript detection depends on the log schema. It recognizes common shapes
  (`tool_calls`, `message.content`); bespoke schemas may return `unknown`.

When the verdict matters, confirm against the client's actual tool-dispatch
source code. The tool exists to triage and prioritize that review, not replace it.

## Tests

`uv run pytest lab/mcp-matrix/harness/tests/test_substrate_auditor.py`

CI / pre-publication gates:

```bash
make selfcheck
make remediation-demo
make verify-public
```

## Portfolio Signal

This tool is intentionally small. That is the point: a hiring manager can see the
full security loop without trusting a live model call. The writeup explains the
failure mode, this CLI classifies the risky substrate, `make benchmark` validates
preserved fixtures, and the detection notes describe how the same chain would be
monitored in staging.
