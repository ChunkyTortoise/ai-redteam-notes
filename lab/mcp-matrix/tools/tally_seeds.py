#!/usr/bin/env python3
"""Recount strict-bypass outcomes from mirrored per-seed `seeds.json` files.

Stdlib only, no network, no model calls. For each file it reads the per-seed
`strict_bypassed` flags, reports k/n, and computes a Wilson 95% interval, so a
reviewer can check the Results table numbers against the committed data.

Usage:
    python3 lab/mcp-matrix/tools/tally_seeds.py                 # every runs/*/seeds.json
    python3 lab/mcp-matrix/tools/tally_seeds.py path/seeds.json [...]
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

RUNS_DIR = Path(__file__).resolve().parent.parent / "runs"
Z95 = 1.959963984540054


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    """Wilson score interval for k successes in n trials."""
    if n <= 0:
        raise ValueError("n must be positive")
    if not 0 <= k <= n:
        raise ValueError("k must be between 0 and n")
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def tally(path: Path) -> dict:
    data = json.loads(path.read_text())
    seeds = data.get("seeds", [])
    n = len(seeds)
    k = sum(1 for s in seeds if s.get("strict_bypassed") is True)
    declared = data.get("n_seeds")
    lo, hi = wilson(k, n) if n else (float("nan"), float("nan"))
    return {
        "file": str(path),
        "cell": data.get("cell"),
        "model": data.get("model"),
        "mitigation": data.get("mitigation"),
        "substrate": data.get("substrate"),
        "variant": data.get("variant"),
        "k": k,
        "n": n,
        "n_declared_matches": declared is None or declared == n,
        "wilson95": [round(lo, 4), round(hi, 4)],
    }


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv] or sorted(RUNS_DIR.glob("*/seeds.json"))
    if not paths:
        print("no seeds.json files found", file=sys.stderr)
        return 2
    bad = 0
    for p in paths:
        if not p.is_file():
            print(f"missing: {p}", file=sys.stderr)
            return 2
        r = tally(p)
        flag = "" if r["n_declared_matches"] else "  (n_seeds field disagrees)"
        bad += 0 if r["n_declared_matches"] else 1
        lo, hi = r["wilson95"]
        print(
            f"{r['k']:>2}/{r['n']:<2} strict  wilson95=[{lo:.4f}, {hi:.4f}]  "
            f"{r['model']} {r['substrate']} {r['mitigation']} {r['variant']}  "
            f"{p.parent.name}{flag}"
        )
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
