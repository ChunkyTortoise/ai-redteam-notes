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
    # Only the full name: the bare word "continue" also appears as an ordinary
    # config value (for example "onError": "continue") and caused false lows.
    "continue.dev": "typed-toolcall-api",
}

_XML_FIELD_KEYS = {
    "toolparser", "tool_parser", "tooldispatch", "tool_dispatch",
    "substrate", "parser", "dispatch",
}
_XML_VALUE_TOKENS = ("xml", "inline", "tag")
# Typed tokens must stand alone ("native_api" counts, "therapist" does not):
# a typed verdict exits 0, so a substring false positive fails open.
_TYPED_VALUE_RE = re.compile(
    r"(?<![a-z])(typed|structured|toolcall|tool[-_]call|function|api)s?(?![a-z])"
)


def _is_dispatch_key(key: str) -> bool:
    k = key.lower()
    return k in _XML_FIELD_KEYS or "dispatch" in k or "parser" in k

# Tag names that look like tool dispatch rather than prose markup.
_TOOL_TAG_HINT = re.compile(
    r"<(read_file|write_to_file|execute_command|lab_fetch|fetch|browser_action|"
    r"use_mcp_tool|access_mcp_resource|search_files|list_files|apply_diff|"
    r"[a-z][a-z0-9]*_[a-z0-9_]*)>.*?</\1>"
    # Function-equals style used by some open-model tool formats.
    r"|<function=[\w.-]+>.*?</function>",
    re.DOTALL,
)


def _text_of(content: Any) -> str:
    """Flatten message content: a string, or a list of text blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and isinstance(block.get("text"), str):
                parts.append(block["text"])
        return "\n".join(parts)
    return ""


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


def _iter_string_fields(node: Any, depth: int = 0):
    """Yield (key, value) for every string-valued field in nested dicts/lists."""
    if depth > 32:
        return
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str):
                yield str(k), v
            else:
                yield from _iter_string_fields(v, depth + 1)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_string_fields(item, depth + 1)


def _classify_config(raw: str, path: Path) -> dict[str, str]:
    lowered = raw.lower()
    parsed: Any = None
    parse_ok = True
    try:
        parsed = json.loads(_strip_jsonc(raw))
    except (ValueError, TypeError):
        parsed = None
        parse_ok = False

    # 1. Explicit dispatch field wins, at any nesting depth. If fields
    # disagree, inline-XML wins because that path is the exploitable one.
    typed_hit: tuple[str, str] | None = None
    for k, v in _iter_string_fields(parsed):
        if not _is_dispatch_key(k):
            continue
        vl = v.lower()
        if any(t in vl for t in _XML_VALUE_TOKENS):
            return _verdict("config", "inline-xml-dispatch",
                            f"explicit dispatch field {k!r}={v!r}", path)
        if typed_hit is None and _TYPED_VALUE_RE.search(vl):
            typed_hit = (k, v)
    if typed_hit is not None:
        k, v = typed_hit
        return _verdict("config", "typed-toolcall-api",
                        f"explicit dispatch field {k!r}={v!r}", path)

    # 2. Known client identity. If the file did not parse, a name match is
    # only a substring of unstructured text, so it may raise risk but never
    # lower it (an unparsed dispatch field could still say xml).
    for name, substrate in _CLIENT_REGISTRY.items():
        if not parse_ok and substrate != "inline-xml-dispatch":
            continue
        if re.search(rf"\b{re.escape(name)}\b", lowered):
            return _verdict("config", substrate,
                            f"client identified as {name!r} (parser audit, Addendum A)", path)

    if not parse_ok:
        return _verdict("config", "unknown",
                        "config did not parse as JSON/JSONC; no inline-XML signal in its text", path)
    return _verdict("config", "unknown",
                    "no explicit dispatch field and no audited client identity", path)


def _classify_transcript(lines: list[str], path: Path) -> dict[str, str]:
    saw_structured = False
    saw_inline = False
    unparsed = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            unparsed += 1
            continue
        if not isinstance(rec, dict):
            unparsed += 1
            continue
        msg = rec.get("message") if isinstance(rec.get("message"), dict) else rec
        if msg.get("tool_calls") or msg.get("tool_call") or rec.get("type") == "tool_call":
            saw_structured = True
        # Only assistant text can be dispatched. Tags inside user or tool
        # messages are untrusted data (the injection itself), not dispatch.
        role = msg.get("role", rec.get("role"))
        if role is not None and str(role).lower() != "assistant":
            continue
        if _TOOL_TAG_HINT.search(_text_of(msg.get("content"))):
            saw_inline = True

    if saw_inline and not saw_structured:
        return _verdict("transcript", "inline-xml-dispatch",
                        "assistant content contains inline tool-dispatch tags and no structured tool_calls", path)
    if saw_structured and not saw_inline and unparsed:
        # A skipped line could hold the inline tag, so do not report low.
        return _verdict("transcript", "unknown",
                        f"structured tool_calls present but {unparsed} line(s) did not parse as JSON objects", path)
    if saw_structured and not saw_inline:
        return _verdict("transcript", "typed-toolcall-api",
                        "structured tool_call events present, no inline dispatch tags", path)
    if saw_structured and saw_inline:
        return _verdict("transcript", "inline-xml-dispatch",
                        "mixed: inline dispatch tags present alongside structured calls (inline path is exploitable)", path)
    return _verdict("transcript", "unknown",
                    "no structured tool_calls and no inline dispatch tags observed", path)


class UnreadableInput(Exception):
    """The input exists but is not readable UTF-8 text (binary, a directory)."""


def audit_path(path: str | Path) -> dict[str, str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"no such file: {p}")
    try:
        raw = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise UnreadableInput(f"cannot read {p} as UTF-8 text: {e}") from e
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
    ap.add_argument("--strict", action="store_true",
                    help="also exit 1 when the substrate is unknown (for gating unreviewed clients)")
    ap.add_argument("--expect-risk", choices=("high", "low", "unknown"), help="return 0 only if the observed risk matches")
    ns = ap.parse_args(argv)

    try:
        result = audit_path(ns.path)
    except (FileNotFoundError, UnreadableInput) as e:
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

    if ns.expect_risk is not None:
        if result["risk"] != ns.expect_risk:
            print(f"error: expected risk {ns.expect_risk!r}, got {result['risk']!r}", file=sys.stderr)
            return 1
        return 0

    if result["risk"] == "high":
        return 1
    if ns.strict and result["risk"] == "unknown":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
