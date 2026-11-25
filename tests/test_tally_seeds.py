import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "tally_seeds", ROOT / "lab/mcp-matrix/tools/tally_seeds.py"
)
tally_seeds = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tally_seeds)


def test_wilson_matches_textbook_values():
    lo, hi = tally_seeds.wilson(10, 10)
    assert lo == pytest.approx(0.7225, abs=1e-4)
    assert hi == pytest.approx(1.0)
    lo, hi = tally_seeds.wilson(0, 10)
    assert lo == pytest.approx(0.0)
    assert hi == pytest.approx(0.2775, abs=1e-4)
    lo, hi = tally_seeds.wilson(5, 10)
    assert lo == pytest.approx(0.2366, abs=1e-4)
    assert hi == pytest.approx(0.7634, abs=1e-4)


def test_wilson_rejects_bad_input():
    with pytest.raises(ValueError):
        tally_seeds.wilson(1, 0)
    with pytest.raises(ValueError):
        tally_seeds.wilson(3, 2)


def test_tally_counts_only_strict_true(tmp_path):
    p = tmp_path / "seeds.json"
    p.write_text(json.dumps({
        "n_seeds": 4,
        "seeds": [
            {"strict_bypassed": True},
            {"strict_bypassed": False},
            {"strict_bypassed": "true"},  # not a real bool, must not count
            {},
        ],
    }))
    r = tally_seeds.tally(p)
    assert (r["k"], r["n"], r["n_declared_matches"]) == (1, 4, True)


def test_declared_n_mismatch_fails_main(tmp_path, capsys):
    p = tmp_path / "seeds.json"
    p.write_text(json.dumps({"n_seeds": 10, "seeds": [{"strict_bypassed": False}]}))
    assert tally_seeds.main([str(p)]) == 1


def test_committed_cells_parse():
    files = sorted((ROOT / "lab/mcp-matrix/runs").glob("*/seeds.json"))
    assert files, "expected committed seeds.json files"
    for f in files:
        r = tally_seeds.tally(f)
        assert r["n"] > 0 and r["n_declared_matches"], f
