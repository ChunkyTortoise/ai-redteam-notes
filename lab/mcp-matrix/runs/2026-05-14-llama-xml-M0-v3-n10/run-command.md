# Run Command

Services:

```bash
cd lab/mcp-matrix
MCP_LAB_RUN_DIR=runs/2026-05-14-llama-xml-M0-v3-n10 just lab-mcp-canary
MCP_LAB_RUN_DIR=runs/2026-05-14-llama-xml-M0-v3-n10 just lab-mcp-up
```

Seed sweep:

```bash
cd <repo-root>
RUN_DIR="lab/mcp-matrix/runs/2026-05-14-llama-xml-M0-v3-n10"
for seed in 1 2 3 4 5 6 7 8 9 10; do
  uv run python lab/mcp-matrix/scripts/run_headless.py \
    --model llama3.1:8b \
    --payload-url http://127.0.0.1:9001/notes/v3-fake-json-fence \
    --run-dir "$RUN_DIR" \
    --attempt "seed-$seed" \
    --system-prompt-file lab/mcp-matrix/mitigations/cline-xml-scaffold.txt \
    --xml-dispatch \
    --temperature 0.7 \
    --seed "$seed"
done
```

Note: seed 1 was run before the loop was resumed because the first shell loop used `status`, a read-only zsh variable. The seed 1 result and transcript were written successfully before that loop stopped.
