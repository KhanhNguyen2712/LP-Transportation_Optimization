import numpy as np

from transportopt.domain import TransportationInput
from transportopt.model_builder import build_model
from transportopt.results import analyze_result
from transportopt.solver import solve


def _case(supply, demand, costs):
    return TransportationInput(
        warehouses=tuple(f"W{i}" for i in range(len(supply))),
        customers=tuple(f"C{i}" for i in range(len(demand))),
        supply=np.asarray(supply, dtype=float),
        demand=np.asarray(demand, dtype=float),
        costs=np.asarray(costs, dtype=float),
    )


def test_surplus_supply_is_reported_after_solving():
    case = _case([5], [3], [[7]])
    result = analyze_result(case, solve(build_model(case)))

    np.testing.assert_allclose(result.unused_supply, [2])


def test_insufficient_supply_is_infeasible():
    case = _case([2], [3], [[7]])
    result = solve(build_model(case))

    assert result.status == "infeasible"
    assert result.shipment is None


def test_large_costs_preserve_objective():
    case = _case([2], [2], [[1e12]])
    result = analyze_result(case, solve(build_model(case)))

    assert result.objective == 2e12


def test_multiple_optima_still_produce_a_feasible_result():
    case = _case([2, 2], [2, 2], [[0, 0], [0, 0]])
    result = analyze_result(case, solve(build_model(case)))

    assert result.objective == 0
    assert np.max(np.abs(result.demand_residual)) <= 1e-8
    assert np.max(result.supply_violation) <= 1e-8
