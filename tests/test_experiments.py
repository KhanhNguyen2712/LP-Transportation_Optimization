import csv

import numpy as np

from scripts.run_experiments import generate_case, run_experiment, write_results


def test_generation_is_deterministic_and_runner_emits_metrics(tmp_path):
    first = generate_case(2, 3, seed=17)
    second = generate_case(2, 3, seed=17)

    np.testing.assert_array_equal(first.supply, second.supply)
    np.testing.assert_array_equal(first.demand, second.demand)
    np.testing.assert_array_equal(first.costs, second.costs)
    assert sum(first.supply) == sum(first.demand)

    row = run_experiment(2, 3, seed=17)
    assert set(row) == {
        "seed",
        "warehouses",
        "customers",
        "objective",
        "runtime",
        "memory",
        "status",
        "maximum_violation",
    }
    assert row["status"] == "optimal"
    assert row["maximum_violation"] <= 1e-8

    output = tmp_path / "results.csv"
    write_results([row], output)
    with output.open(newline="", encoding="utf-8") as handle:
        assert next(csv.DictReader(handle))["status"] == "optimal"
