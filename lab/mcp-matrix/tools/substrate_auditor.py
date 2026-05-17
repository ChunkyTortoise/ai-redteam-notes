#!/usr/bin/env python3
"""Defensive substrate auditor for MCP tool-output indirect prompt injection.

Given an MCP client config (JSON / JSONC) or a captured transcript (JSONL),
classify the tool-dispatch substrate and recommend a mitigation. Grounded in
the Cline (inline-xml) vs Kilo Code (typed-toolcall-api) parser audit in
WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md (Addendum A) and the cross-scale
falsification in Addendum B (the inline-xml risk does not diminish at 70B; it
strengthens, so the recommendation holds at every model scale).

This is a heuristic, not a guarantee. It flags a likely-risky substrate from
declarative signals; it cannot prove the absence of an inline-XML dispatch path.
Confirm against the client's actual dispatch code when the verdict matters.

stdlib only (json, re, sys, argparse, pathlib) so it runs in CI and via
`make audit` with no extra dependencies.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

CITATION = "WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md (substrate-vs-policy; Addendum B: cross-scale)"

RECOMMENDATION = (
    "Prefer a typed tool-use API substrate (structured tool_call events) over "
    "inline-XML tag dispatch; this removes the dispatch vector at every model "
    "scale (capability amplifies exploitation within the insecure substrate, "
    "see Addendum B). If inline-XML cannot be replaced, apply a short "
    "tool-agnostic content-trust boundary (the M1 mitigation under "
    "lab/mcp-matrix/mitigations/) and do not enumerate tool names in the "
    "system prompt (the M2 tool-naming variant regressed versus no mitigation)."
)

_SAFE_RECOMMENDATION = (
    "Typed tool-use API substrate detected; the inline-XML dispatch vector is "
    "absent. Keep tool invocation on structured events. Still apply the M1 "
    "tool-agnostic content-trust boundary as defense in depth."
)

_UNKNOWN_RECOMMENDATION = (
    "Substrate could not be determined from declarative signals. Inspect the "
    "client's tool-dispatch code: if it scans assistant text for inline tags it "
    "is inline-XML (high risk); if it consumes structured tool_call events it is "
    "typed. Until confirmed, treat as potentially inline-XML and apply the M1 "
    "tool-agnostic content-trust boundary."
)

# Known clients from the parser audit (Addendum A). Conservative: only clients
# actually audited are registered; do not guess forks.
_CLIENT_REGISTRY = {
    "cline": "inline-xml-dispatch",
    "kilo code": "typed-toolcall-api",
    "kilocode": "typed-toolcall-api",
    "kilo": "typed-toolcall-api",
    "continue.dev": "typed-toolcall-api",
    "continue": "typed-toolcall-api",
}

_XML_FIELD_KEYS = {
    "toolparser", "tool_parser", "tooldispatch", "tool_dispatch",
    "substrate", "parser", "dispatch",
}
_XML_VALUE_TOKENS = ("xml", "inline", "tag")
_TYPED_VALUE_TOKENS = ("typed", "structured", "toolcall", "tool-call", "tool_call", "function", "api")

# Tag names that look like tool dispatch rather than prose markup.
_TOOL_TAG_HINT = re.compile(
    r"<(read_file|write_to_file|execute_command|lab_fetch|fetch|browser_action|"
    r"use_mcp_tool|access_mcp_resource|search_files|list_files|apply_diff|"
    r"[a-z][a-z0-9]*_[a-z0-9_]*)>.*?</\1>",
    re.DOTALL,
)


def _strip_jsonc(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"(^|\s)//[^\n]*", r"\1", text)
    return text


def _verdict(kind: str, substrate: str, rationale: str, path: Path) -> dict[str, str]:
    if substrate == "inline-xml-dispatch":
        risk, rec = "high", RECOMMENDATION
    elif substrate == "typed-toolcall-api":
        risk, rec = "low", _SAFE_RECOMMENDATION
    else:
        risk, rec = "unknown", _UNKNOWN_RECOMMENDATION
    return {
        "input": str(path),
        "kind": kind,
        "substrate": substrate,
        "risk": risk,
        "rationale": rationale,
        "recommendation": rec,
        "citation": CITATION,
    }


def _classify_config(raw: str, path: Path) -> dict[str, str]:
    lowered = raw.lower()
    parsed: Any = None
    try:
        parsed = json.loads(_strip_jsonc(raw))
    except (ValueError, TypeError):
        parsed = None

    # 1. Explicit dispatch field wins.
    if isinstance(parsed, dict):
        for k, v in parsed.items():
            if k.lower() in _XML_FIELD_KEYS and isinstance(v, str):
                vl = v.lower()
                if any(t in vl for t in _XML_VALUE_TOKENS):
                    return _verdict("config", "inline-xml-dispatch",
                                    f"explicit dispatch field {k!r}={v!r}", path)
                if any(t in vl for t in _TYPED_VALUE_TOKENS):
                    return _verdict("config", "typed-toolcall-api",
                                    f"explicit dispatch field {k!r}={v!r}", path)

    # 2. Known client identity.
    for name, substrate in _CLIENT_REGISTRY.items():
        if re.search(rf"\b{re.escape(name)}\b", lowered):
            return _verdict("config", substrate,
                            f"client identified as {name!r} (parser audit, Addendum A)", path)

    return _verdict("config", "unknown",
                    "no explicit dispatch field and no audited client identity", path)


def _classify_transcript(lines: list[str], path: Path) -> dict[str, str]:
    saw_structured = False
    saw_inline = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if not isinstance(rec, dict):
            continue
        msg = rec.get("message") if isinstance(rec.get("message"), dict) else rec
        if msg.get("tool_calls") or msg.get("tool_call") or rec.get("type") == "tool_call":
            saw_structured = True
        content = msg.get("content")
        if isinstance(content, str) and _TOOL_TAG_HINT.search(content):
            saw_inline = True

    if saw_inline and not saw_structured:
        return _verdict("transcript", "inline-xml-dispatch",
                        "assistant content contains inline tool-dispatch tags and no structured tool_calls", path)
    if saw_structured and not saw_inline:
        return _verdict("transcript", "typed-toolcall-api",
                        "structured tool_call events present, no inline dispatch tags", path)
    if saw_structured and saw_inline:
        return _verdict("transcript", "inline-xml-dispatch",
                        "mixed: inline dispatch tags present alongside structured calls (inline path is exploitable)", path)
    return _verdict("transcript", "unknown",
                    "no structured tool_calls and no inline dispatch tags observed", path)


def audit_path(path: str | Path) -> dict[str, str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"no such file: {p}")
    raw = p.read_text()
    if p.suffix == ".jsonl" or _looks_like_jsonl(raw):
        return _classify_transcript(raw.splitlines(), p)
    return _classify_config(raw, p)


def _looks_like_jsonl(raw: str) -> bool:
    lines = [ln for ln in raw.splitlines() if ln.strip()]
    if len(lines) < 2:
        return False
    ok = 0
    for ln in lines[:5]:
        try:
            json.loads(ln)
            ok += 1
        except ValueError:
            return False
    return ok >= 2


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Audit an MCP client config or transcript for inline-XML dispatch risk.")
    ap.add_argument("path", help="path to an MCP client config (JSON/JSONC) or a transcript (JSONL)")
    ap.add_argument("--json", action="store_true", help="emit the verdict as JSON")
    ns = ap.parse_args(argv)

    try:
        result = audit_path(ns.path)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if ns.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"substrate : {result['substrate']}")
        print(f"risk      : {result['risk']}")
        print(f"why       : {result['rationale']}")
        print(f"recommend : {result['recommendation']}")
        print(f"reference : {result['citation']}")

    return 1 if result["risk"] == "high" else 0


if __name__ == "__main__":
    raise SystemExit(main())
