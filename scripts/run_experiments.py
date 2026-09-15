"""Generate reproducible transportation cases and record solver measurements."""

from __future__ import annotations

import argparse
import csv
import random
import time
import tracemalloc
from pathlib import Path
from typing import Iterable

import numpy as np

from transportopt.domain import TransportationInput
from transportopt.model_builder import build_model
from transportopt.results import analyze_result
from transportopt.solver import solve
from transportopt.validation import validate_input


SIZES = ((2, 3), (5, 10), (10, 50), (50, 100), (100, 500))
FIELDS = (
    "seed",
    "warehouses",
    "customers",
    "objective",
    "runtime",
    "memory",
    "status",
    "maximum_violation",
)


def generate_case(warehouses: int, customers: int, seed: int) -> TransportationInput:
    """Create a deterministic, balanced, non-negative transportation input."""
    if warehouses < 1 or customers < 1:
        raise ValueError("dimensions must be positive")
    rng = random.Random(seed)
    demand = [rng.randint(10, 100) for _ in range(customers)]
    total = sum(demand)
    supply = [1] * warehouses
    for _ in range(total - warehouses):
        supply[rng.randrange(warehouses)] += 1
    costs = np.array(
        [[rng.randint(1, 100) for _ in range(customers)] for _ in range(warehouses)],
        dtype=float,
    )
    return TransportationInput(
        warehouses=tuple(f"W{i + 1}" for i in range(warehouses)),
        customers=tuple(f"C{i + 1}" for i in range(customers)),
        supply=np.asarray(supply, dtype=float),
        demand=np.asarray(demand, dtype=float),
        costs=costs,
    )


def run_experiment(warehouses: int, customers: int, seed: int) -> dict[str, object]:
    """Run validation, model construction, solve, and result analysis once."""
    tracemalloc.start()
    started = time.perf_counter()
    try:
        case = generate_case(warehouses, customers, seed)
        validate_input(case)
        solved = solve(build_model(case))
        if solved.status == "optimal":
            analyzed = analyze_result(case, solved)
            maximum_violation = float(
                max(
                    np.max(np.abs(analyzed.demand_residual)),
                    np.max(analyzed.supply_violation),
                    np.max(analyzed.nonnegativity_violation),
                )
            )
            objective = analyzed.objective
        else:
            maximum_violation = None
            objective = None
        status = solved.status
    except Exception:
        objective = None
        maximum_violation = None
        status = "error"
    runtime = time.perf_counter() - started
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "seed": seed,
        "warehouses": warehouses,
        "customers": customers,
        "objective": objective,
        "runtime": runtime,
        "memory": peak_memory,
        "status": status,
        "maximum_violation": maximum_violation,
    }


def write_results(rows: Iterable[dict[str, object]], output: str | Path) -> Path:
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return destination


def run_experiments(
    seed: int = 17,
    output: str | Path = "runs/experiments.csv",
    sizes: Iterable[tuple[int, int]] = SIZES,
) -> Path:
    rows = [run_experiment(m, n, seed) for m, n in sizes]
    return write_results(rows, output)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--output", type=Path, default=Path("runs/experiments.csv"))
    args = parser.parse_args()
    print(run_experiments(seed=args.seed, output=args.output))


if __name__ == "__main__":
    main()
