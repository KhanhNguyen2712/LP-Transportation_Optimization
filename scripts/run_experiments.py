"""Generate reproducible transportation cases and record solver measurements."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import random
import subprocess
import time
import tracemalloc
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np

from transportopt.baselines import greedy_nearest_cost
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
    "repeat",
    "build_seconds",
    "solve_seconds",
    "greedy_seconds",
    "greedy_objective",
    "greedy_maximum_violation",
    "saving_ratio",
    "error_message",
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


def run_experiment(
    warehouses: int,
    customers: int,
    seed: int,
    repeat: int = 1,
) -> dict[str, object]:
    """Measure the LP pipeline; generation and greedy run outside that interval."""
    case = generate_case(warehouses, customers, seed)
    row = dict.fromkeys(FIELDS)
    row.update(
        seed=seed,
        warehouses=warehouses,
        customers=customers,
        repeat=repeat,
        status="error",
        error_message="",
    )
    tracemalloc.start()
    started = time.perf_counter()
    try:
        validate_input(case)
        before = time.perf_counter()
        model = build_model(case)
        row["build_seconds"] = time.perf_counter() - before
        before = time.perf_counter()
        solved = solve(model)
        row["solve_seconds"] = time.perf_counter() - before
        row["status"] = solved.status
        if solved.status == "optimal":
            analyzed = analyze_result(case, solved)
            row["maximum_violation"] = float(
                max(
                    np.max(np.abs(analyzed.demand_residual), initial=0),
                    np.max(analyzed.supply_violation, initial=0),
                    np.max(analyzed.nonnegativity_violation, initial=0),
                )
            )
            if not np.isfinite(analyzed.shipment).all() or not np.isfinite(
                analyzed.objective
            ):
                raise ValueError("LP result contains nonfinite values.")
            row["objective"] = analyzed.objective
        else:
            row["error_message"] = solved.message
    except Exception as exc:
        row.update(status="error", error_message=f"{type(exc).__name__}: {exc}")
    finally:
        row["runtime"] = time.perf_counter() - started
        _, row["memory"] = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    try:
        before = time.perf_counter()
        greedy = greedy_nearest_cost(case)
        row["greedy_seconds"] = time.perf_counter() - before
        row["greedy_maximum_violation"] = float(
            max(
                np.max(np.abs(greedy.sum(axis=0) - case.demand), initial=0),
                np.max(greedy.sum(axis=1) - case.supply, initial=0),
                np.max(-greedy, initial=0),
            )
        )
        if not np.isfinite(greedy).all() or row["greedy_maximum_violation"] > 1e-8:
            raise ValueError("Greedy shipment failed feasibility checks.")
        row["greedy_objective"] = float(np.sum(case.costs * greedy))
        if row["status"] == "optimal":
            difference = row["greedy_objective"] - row["objective"]
            if difference < -1e-8:
                raise ValueError("LP objective exceeds the feasible baseline cost.")
            # A zero-cost baseline leaves the relative saving undefined.
            if row["greedy_objective"] > 0:
                row["saving_ratio"] = difference / row["greedy_objective"]
    except Exception as exc:
        row.update(status="error", error_message=f"{type(exc).__name__}: {exc}")
    return row


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
    seeds: Iterable[int] | None = None,
    repeats: int = 1,
) -> Path:
    sizes = list(sizes)
    seeds = [seed] if seeds is None else list(seeds)
    if repeats < 1 or not seeds or not sizes or len(set(seeds)) != len(seeds):
        raise ValueError("Use positive repeats, distinct seeds and nonempty sizes.")
    rows = []
    for m, n in sizes:
        for current_seed in seeds:
            for repeat in range(1, repeats + 1):
                row = run_experiment(m, n, current_seed, repeat)
                rows.append(row)
                print(
                    f"{m}x{n} seed={current_seed} repeat={repeat}: {row['status']}",
                    flush=True,
                )
    destination = write_results(rows, output)
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__).relative_to(root)] + sorted(
        path.relative_to(root) for path in (root / "src/transportopt").rglob("*.py")
    )

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True, check=True
        ).stdout.strip()

    cpu = platform.processor()
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        cpu = next(
            (
                line.split(":", 1)[1].strip()
                for line in cpuinfo.read_text().splitlines()
                if line.startswith("model name")
            ),
            cpu,
        )
    metadata = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "seeds": seeds,
        "repeats": repeats,
        "sizes": sizes,
        "versions": {
            name: importlib.metadata.version(name)
            for name in ("numpy", "scipy", "pandas", "streamlit")
        },
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu": cpu,
        "logical_cpus": os.cpu_count(),
        "system_memory_bytes": os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES"),
        "git_commit": git("rev-parse", "HEAD"),
        "git_dirty": bool(git("status", "--porcelain")),
        "source_sha256": {
            str(path): hashlib.sha256((root / path).read_bytes()).hexdigest()
            for path in sources
        },
        "measurement": {
            "runtime": (
                "seconds: validation + model build + solve + analysis; "
                "excludes generation and greedy"
            ),
            "build_seconds": "seconds: build_model only",
            "solve_seconds": (
                "seconds: solve wrapper including SciPy conversion, presolve and HiGHS"
            ),
            "memory": (
                "bytes: peak tracemalloc allocation during LP pipeline; "
                "not total process RSS or native solver RAM"
            ),
            "greedy_seconds": (
                "seconds: greedy validation + allocation; "
                "excludes objective and residual checks"
            ),
            "saving_ratio": (
                "(greedy_objective - objective) / greedy_objective; "
                "blank if denominator is zero"
            ),
            "order": (
                "sequential: size, seed, repeat; no warmup; "
                "tracemalloc enabled during LP timings"
            ),
        },
    }
    destination.with_suffix(".metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--seeds", nargs="+", type=int)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--output", type=Path, default=Path("runs/experiments.csv"))
    args = parser.parse_args()
    output = run_experiments(
        seed=args.seed, output=args.output, seeds=args.seeds, repeats=args.repeats
    )
    print(output)
    with output.open(newline="", encoding="utf-8") as handle:
        if any(row["status"] != "optimal" for row in csv.DictReader(handle)):
            raise SystemExit("One or more experiments failed; inspect error_message.")


if __name__ == "__main__":
    main()
