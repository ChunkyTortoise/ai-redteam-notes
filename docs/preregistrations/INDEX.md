# Pre-registration Index

Every hypothesis in this program was frozen in a dated pre-registration file
before the cell that tested it ran. This index makes the registered-then-tested
chain legible at a glance. The narrative source of truth is
[`../../RESEARCH-SUMMARY.md`](../../RESEARCH-SUMMARY.md); claim-to-run mapping is in
[`../reports/hiring-evidence-index.md`](../reports/hiring-evidence-index.md).

## Pre-registration files

| File | Frozen | Scope | Status |
|---|---|---|---|
| [`2026-mcp-matrix.md`](2026-mcp-matrix.md) | 2026-05-08 | 8B-class MCP tool-output injection matrix; substrate axis registered after the H3 retraction | executed |
| [`2026-05-13-tier-a-w1-w5.md`](2026-05-13-tier-a-w1-w5.md) | scaffolded 2026-05-13 (commit-SHA freeze before F1) | Tier A model-axis sweep; registers the H7 cross-scale claim | executed (F1 cell) |
| [`2026-05-15-frontier-substrate-h10.md`](2026-05-15-frontier-substrate-h10.md) | 2026-05-15 | Does frontier RLHF (claude-sonnet-4-6) dampen the 8B substrate effect (H10) | gated |
| [`2026-05-15-last-tag-wins-dispatch-ablation.md`](2026-05-15-last-tag-wins-dispatch-ablation.md) | 2026-05-15 (commit `40ad86a`) | Last-tag-wins XML dispatch ablation (H11) | executed |
| [`2026-05-16-open-source-scale-substrate-h10b.md`](2026-05-16-open-source-scale-substrate-h10b.md) | 2026-05-16 | Open-source scale replication 8B to 70B (H10b); confirmatory grid H10b-G | in progress (gated) |

## Hypothesis ledger

| Hypothesis | Registered in | Outcome |
|---|---|---|
| H3 (model-strength inversion) | `2026-mcp-matrix.md` | Retracted. Traced to a substrate confound, not model alignment. |
| H5 (substrate is load-bearing) | `2026-mcp-matrix.md` | Supported. Only the inline-XML parser config reproduced the bypass, model held constant. |
| H6 (combined-framing payload v7) | `2026-mcp-matrix.md` | Falsified. 0 strict bypasses on M0 across the registered seed budget. |
| H7 (larger model is safer here) | `2026-05-13-tier-a-w1-w5.md` | Falsified. 70B 10/10 vs 8B 0/5 strict canary exfiltration under inline-XML. |
| H10 (frontier RLHF dampens effect) | `2026-05-15-frontier-substrate-h10.md` | Gated. No rates stated until the control cell clears its packaging gate. |
| H10b / H10b-G (scale + mitigations) | `2026-05-16-open-source-scale-substrate-h10b.md` | In progress, gated. Do not quote rates pre-clearance. |
| H11 (last-tag-wins dispatch risk) | `2026-05-15-last-tag-wins-dispatch-ablation.md` | Falsified. 0/10 strict; one callback carried placeholder data, not the canary. |
| M2 (name tools inside mitigation) | `2026-mcp-matrix.md` | Regression. Performed worse than no mitigation on the 8B model. |

Negative and falsified results are kept visible by design: a portfolio that hides
its nulls is less trustworthy than one that reports them.
