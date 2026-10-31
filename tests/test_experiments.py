import csv

import numpy as np
import pytest

from scripts.run_experiments import generate_case, run_experiment, write_results


def test_generation_is_deterministic_and_runner_emits_metrics(tmp_path):
    first = generate_case(2, 3, seed=17)
    second = generate_case(2, 3, seed=17)

    np.testing.assert_array_equal(first.supply, second.supply)
    np.testing.assert_array_equal(first.demand, second.demand)
    np.testing.assert_array_equal(first.costs, second.costs)
    assert sum(first.supply) == sum(first.demand)

    row = run_experiment(2, 3, seed=17)
    assert {
        "seed",
        "warehouses",
        "customers",
        "objective",
        "runtime",
        "memory",
        "status",
        "maximum_violation",
    } <= set(row)
    assert row["status"] == "optimal"
    assert row["maximum_violation"] <= 1e-8

    output = tmp_path / "results.csv"
    write_results([row], output)
    with output.open(newline="", encoding="utf-8") as handle:
        assert next(csv.DictReader(handle))["status"] == "optimal"


def test_experiment_records_greedy_and_separate_timings():
    row = run_experiment(3, 4, seed=17)
    assert row["greedy_objective"] >= row["objective"] - 1e-8
    assert row["saving_ratio"] == pytest.approx(
        (row["greedy_objective"] - row["objective"]) / row["greedy_objective"]
    )
    assert row["greedy_maximum_violation"] <= 1e-8
    assert 0 <= row["solve_seconds"] <= row["runtime"]
    assert 0 <= row["build_seconds"] <= row["runtime"]
    assert row["greedy_seconds"] >= 0
    assert row["memory"] > 0
    assert row["repeat"] == 1
    assert row["error_message"] == ""


def test_experiment_batch_records_seeds_repeats_and_provenance(tmp_path):
    import json

    from scripts.run_experiments import run_experiments

    output = run_experiments(
        output=tmp_path / "results.csv", sizes=[(2, 3)], seeds=[17, 18], repeats=2
    )
    with output.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 4
    assert {(int(r["seed"]), int(r["repeat"])) for r in rows} == {
        (17, 1),
        (17, 2),
        (18, 1),
        (18, 2),
    }
    assert rows[0]["objective"] == rows[1]["objective"]
    metadata = json.loads(output.with_suffix(".metadata.json").read_text())
    assert metadata["seeds"] == [17, 18]
    assert metadata["repeats"] == 2
    assert "scipy" in metadata["versions"]
    assert len(metadata["source_sha256"]["scripts/run_experiments.py"]) == 64
    assert metadata["measurement"]["memory"]


def test_experiment_preserves_failure_reason(monkeypatch):
    from scripts import run_experiments as runner

    def fail(_):
        raise RuntimeError("test solver failure")

    monkeypatch.setattr(runner, "solve", fail)
    row = runner.run_experiment(2, 3, seed=17)
    assert row["status"] == "error"
    assert row["objective"] is None
    assert "test solver failure" in row["error_message"]


def test_experiment_rejects_empty_batch(tmp_path):
    from scripts.run_experiments import run_experiments

    with pytest.raises(ValueError):
        run_experiments(output=tmp_path / "results.csv", repeats=0)


def test_zero_cost_baseline_has_no_relative_saving(monkeypatch):
    from scripts import run_experiments as runner
    from transportopt.ui.input_form import case_from_tables

    case = case_from_tables(["W"], ["C"], [1], [0], [[0]])
    monkeypatch.setattr(runner, "generate_case", lambda *args: case)
    row = runner.run_experiment(1, 1, seed=17)
    assert row["status"] == "optimal"
    assert row["objective"] == row["greedy_objective"] == 0
    assert row["saving_ratio"] is None
