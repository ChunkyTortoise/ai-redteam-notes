# MCP Matrix Reproducibility Checklist

**Status:** public
**Purpose:** separate fast artifact review from environment-dependent local reruns.

## Fast Review: Replay Preserved Artifacts

Use this path when reviewing the portfolio without starting local services or models.

- Read the lab overview: [`../lab/mcp-matrix/README.md`](../lab/mcp-matrix/README.md)
- Read the n=10 scenario: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/scenario.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/scenario.md)
- Read the preserved command: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md)
- Read the summary: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/summary.md)
- Read the aggregate verdict: [`../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/success.json`](../lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/success.json)

Expected preserved result: strict bypass `0/10`, intent shift / capability fail `2/10`, clean ignore `8/10`, and no canary leak.

## Harness Logic Check

Use this path to verify the verdict and orchestration tests without rerunning a model cell.

```bash
uv run pytest lab/mcp-matrix/harness/tests
```

Expected output:

```text
8 passed
```

## Environment-Dependent Rerun

Use this path only when local model and service dependencies are available.

Requirements:

- `uv`
- `just`
- Ollama or another configured local model endpoint
- local ports `9001`, `9002`, and model endpoint availability

Run command:

```bash
cat lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10/run-command.md
```

The model-cell rerun is not required to review the current hiring claim. The preserved artifacts are sufficient to inspect what was run and how the claim was narrowed.

## Environmental Caveat

`check-d60.sh` depends on `localhost:11434` responding with enough local Ollama models. If Ollama is down or unavailable in a sandbox, the Day-60 lab-operational gate can fail even when the repo artifacts are intact. Treat that as a local runtime caveat, not a content regression.
