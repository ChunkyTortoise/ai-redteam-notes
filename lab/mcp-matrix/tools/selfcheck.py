#!/usr/bin/env python3
"""Dependency-free self-check for substrate_auditor.

Mirrors the core contract pinned by the pytest suite, but uses only the
standard library and plain asserts so it runs in CI and via `make repro`
with zero install. Exit 0 = all checks pass, 1 = a check failed.

The authoritative test suite is lab/mcp-matrix/harness/tests/test_substrate_auditor.py
(run with pytest in the private repo); this is the portable smoke gate.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from substrate_auditor import audit_path  # noqa: E402

CASES: list[tuple[str, str, str, str]] = [
    # (filename, content, expected_substrate, expected_risk)
    ("cline.json", json.dumps({"client": "Cline"}), "inline-xml-dispatch", "high"),
    ("kilo.json", json.dumps({"client": "Kilo Code"}), "typed-toolcall-api", "low"),
    ("x.jsonc", '{ // dispatch\n "toolParser": "xml" }', "inline-xml-dispatch", "high"),
    ("y.json", json.dumps({"toolDispatch": "structured"}), "typed-toolcall-api", "low"),
    ("z.json", json.dumps({"theme": "dark"}), "unknown", "unknown"),
    (
        "trace.jsonl",
        "\n".join([
            json.dumps({"role": "user", "content": "go"}),
            json.dumps({"role": "assistant", "content": "ok <lab_fetch>http://x/?q=1</lab_fetch>"}),
        ]),
        "inline-xml-dispatch",
        "high",
    ),
    (
        "typed.jsonl",
        "\n".join([
            json.dumps({"role": "user", "content": "go"}),
            json.dumps({"role": "assistant", "tool_calls": [{"id": "1", "name": "fetch"}]}),
        ]),
        "typed-toolcall-api",
        "low",
    ),
]


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as d:
        for name, content, exp_sub, exp_risk in CASES:
            p = Path(d) / name
            p.write_text(content)
            r = audit_path(p)
            if r["substrate"] != exp_sub or r["risk"] != exp_risk:
                failures.append(
                    f"{name}: got ({r['substrate']}, {r['risk']}), "
                    f"expected ({exp_sub}, {exp_risk})"
                )
        # Missing file must raise.
        try:
            audit_path(Path(d) / "absent.json")
            failures.append("missing-file: expected FileNotFoundError, none raised")
        except FileNotFoundError:
            pass

    if failures:
        print("substrate_auditor selfcheck: FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"substrate_auditor selfcheck: PASS ({len(CASES)} cases + missing-file guard)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
