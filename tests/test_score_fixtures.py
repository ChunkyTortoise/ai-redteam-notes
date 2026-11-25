import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "EVALS"))
import score_tool_output_injection as sc

FIXTURES = ROOT / "EVALS" / "fixtures" / "tool-output-injection-fixtures.json"


def _score(tmp_path, monkeypatch, data):
    monkeypatch.chdir(ROOT)  # fixture sources are repo-relative
    p = tmp_path / "fx.json"
    p.write_text(json.dumps(data))
    return sc.score(p)


def _first_seeds_fixture(data):
    return next(fx for fx in data["fixtures"] if fx["source"].endswith("seeds.json"))


def test_committed_fixtures_pass(tmp_path, monkeypatch):
    rc, issues = _score(tmp_path, monkeypatch, json.loads(FIXTURES.read_text()))
    assert (rc, issues) == (0, [])


def test_wrong_wilson_interval_fails(tmp_path, monkeypatch):
    data = copy.deepcopy(json.loads(FIXTURES.read_text()))
    _first_seeds_fixture(data)["intent_shift"]["wilson_95"] = [0.8, 1.0]
    rc, issues = _score(tmp_path, monkeypatch, data)
    assert rc == 1 and any("does not match recomputed" in i for i in issues)


def test_count_that_disagrees_with_seeds_file_fails(tmp_path, monkeypatch):
    data = copy.deepcopy(json.loads(FIXTURES.read_text()))
    fx = _first_seeds_fixture(data)
    k, n = fx["strict_bypass"]["k"], fx["strict_bypass"]["n"]
    new_k = n - 1 if k == n else k + 1
    lo, hi = sc.wilson(new_k, n)
    # Self-consistent block (interval matches k/n) that the seeds file contradicts.
    fx["strict_bypass"] = {"k": new_k, "n": n, "wilson_95": [round(lo, 4), round(hi, 4)]}
    rc, issues = _score(tmp_path, monkeypatch, data)
    assert rc == 1 and any("recounted from" in i for i in issues)
