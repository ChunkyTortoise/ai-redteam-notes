# Reproduce

A reviewer should be able to verify the load-bearing claims in a few minutes
without installing anything beyond `python3`.

## 60 seconds (no install)

```bash
make repro
```

This runs:

- `make selfcheck` - a dependency-free self-check of the defensive substrate
  auditor (7 cases + a missing-file guard), and
- `make audit` - the auditor run against two sample MCP client configs, showing
  it flags an inline-XML (Cline-class) substrate as high risk and clears a typed
  tool-use API (Kilo-class) substrate.

`make repro` uses only the standard library, so it runs identically in the
public mirror, in CI, and on a clean checkout.

## The reviewer reading path

1. [RESEARCH-SUMMARY.md](RESEARCH-SUMMARY.md) - the whole program as one
   pre-registered through-line.
2. [WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md)
   - methodology and **Addendum B**, the cross-scale correction.
3. [ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md)
   - the strongest single result: pre-registered H7 falsified at 70B.
4. [docs/reports/2026-05-31-hiring-reviewer-map.md](docs/reports/2026-05-31-hiring-reviewer-map.md)
   and [docs/reports/2026-05-31-evidence-index.md](docs/reports/2026-05-31-evidence-index.md)
   - every claim tied to a raw run directory.

## The defensive deliverable

`lab/mcp-matrix/tools/substrate_auditor.py` turns the research finding into a
usable check (classify an MCP client's tool-dispatch substrate, recommend the
M1 mitigation). See `lab/mcp-matrix/tools/README.md` for usage and its honest
limitations (it is a heuristic, not a guarantee).

## Full harness suite (private repo)

The pre-registered measurement harness and its pytest suite live in the private
working repo (not mirrored, to keep the public surface to reviewable artifacts):

```bash
make test    # uv run pytest lab/mcp-matrix/harness/tests
```

That suite reports `40 passed, 0 failed`.

**Note.** A pre-existing defect in `verdict.py` was fixed as part of this work:
`compute_verdict` sourced the canary from the scorer's `~/.lab/secret.txt`, so a
run scored in CI, on another machine, or after the secret rotated could have a
true `bypassed-A1` silently downgraded to `bypassed-partial`. The canary is now
derived from the run's own artifacts (the value the run's `file_read` returned,
captured in `transcript.jsonl`), with the home file kept only as a fallback. The
change corrects false negatives only; a genuine bypass keeps the same verdict,
so already-recorded run-dir classifications are unaffected.
