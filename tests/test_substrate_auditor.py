"""Adversarial cases for substrate_auditor: inputs that must not come back low.

Each case is a config or transcript that carries an inline-XML signal (or
cannot be read) but that an earlier version rated typed/low, which exits 0
even under --strict.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lab" / "mcp-matrix" / "tools"))
import substrate_auditor as sa

TAG = "<read_file><path>a.txt</path></read_file>"
TYPED_LINE = json.dumps({"role": "assistant", "tool_calls": [{"id": "1", "name": "fetch"}]})


def _write(tmp_path, name, content):
    p = tmp_path / name
    if isinstance(content, bytes):
        p.write_bytes(content)
    else:
        p.write_text(content)
    return p


def _risk(tmp_path, name, content):
    return sa.audit_path(_write(tmp_path, name, content))["risk"]


def test_unparseable_config_is_not_low_from_a_name_substring(tmp_path):
    # Broken JSON whose only typed signal is the word "kilo" in a comment.
    raw = '{"toolDispatch": "xml", // migrated from kilo\n'
    assert _risk(tmp_path, "broken.json", raw) != "low"


def test_dispatch_key_variants_are_read(tmp_path):
    cfg = {"servers": {"kilo": {}}, "dispatchMode": "inline-xml"}
    assert _risk(tmp_path, "mode.json", json.dumps(cfg)) == "high"


def test_typed_tokens_need_word_boundaries(tmp_path):
    # "api" inside an unrelated word is not a typed-dispatch signal.
    assert _risk(tmp_path, "word.json", json.dumps({"parser": "therapist"})) == "unknown"
    assert _risk(tmp_path, "api.json", json.dumps({"parser": "native_api"})) == "low"


def test_role_match_is_case_insensitive(tmp_path):
    line = json.dumps({"role": "Assistant", "content": TAG})
    assert _risk(tmp_path, "caps.jsonl", TYPED_LINE + "\n" + line) == "high"


def test_content_block_lists_are_scanned(tmp_path):
    line = json.dumps({"role": "assistant", "content": [{"type": "text", "text": TAG}]})
    assert _risk(tmp_path, "blocks.jsonl", TYPED_LINE + "\n" + line) == "high"


def test_unparseable_transcript_line_blocks_a_low_verdict(tmp_path):
    broken = '{"role": "assistant", "content": "' + TAG + '"'
    assert _risk(tmp_path, "badline.jsonl", TYPED_LINE + "\n" + broken + "\n") == "unknown"


def test_function_equals_inline_syntax_is_detected(tmp_path):
    text = "<function=read_file><parameter=path>a.txt</parameter></function>"
    lines = [json.dumps({"role": "user", "content": "go"}),
             json.dumps({"role": "assistant", "content": text})]
    assert _risk(tmp_path, "fn.jsonl", "\n".join(lines)) == "high"


def test_function_equals_in_tool_output_is_not_dispatch(tmp_path):
    text = "<function=read_file><parameter=path>a.txt</parameter></function>"
    lines = [TYPED_LINE, json.dumps({"role": "tool", "content": text})]
    assert _risk(tmp_path, "fn-tool.jsonl", "\n".join(lines)) == "low"


@pytest.mark.parametrize("make_input", ["binary", "directory"])
def test_unreadable_input_exits_2_without_traceback(tmp_path, capsys, make_input):
    if make_input == "binary":
        target = _write(tmp_path, "bin.json", b"\xff\xfe\x00garbage")
    else:
        target = tmp_path / "adir"
        target.mkdir()
    assert sa.main([str(target), "--strict"]) == 2
    assert "error:" in capsys.readouterr().err


@pytest.mark.parametrize("content,expected_exit", [
    (json.dumps({"theme": "dark"}), 1),           # unknown
    (json.dumps({"toolDispatch": "xml"}), 1),     # high
    (json.dumps({"toolDispatch": "structured"}), 0),  # low
])
def test_strict_exit_codes(tmp_path, content, expected_exit):
    p = _write(tmp_path, "c.json", content)
    assert sa.main([str(p), "--strict"]) == expected_exit
