import numpy as np
import pytest

from transportopt.baselines import greedy_nearest_cost
from transportopt.domain import InvalidInputError
from transportopt.model_builder import build_model
from transportopt.solver import solve
from transportopt.ui.input_form import case_from_tables, load_named_fixture


def test_greedy_is_feasible_but_can_be_more_expensive_than_lp():
    case = case_from_tables(["A", "B"], ["X", "Y"], [1, 1], [1, 1], [[1, 2], [2, 100]])
    shipment = greedy_nearest_cost(case)
    np.testing.assert_array_equal(shipment, [[1, 0], [0, 1]])
    assert np.sum(shipment * case.costs) == 101
    assert solve(build_model(case)).objective == pytest.approx(4)


@pytest.mark.parametrize("fixture", ["2 × 3 example", "3 × 5 example"])
def test_greedy_respects_supply_demand_and_does_not_mutate_input(fixture):
    case = load_named_fixture(fixture)
    original = case.supply.copy()
    shipment = greedy_nearest_cost(case)
    np.testing.assert_allclose(shipment.sum(axis=0), case.demand)
    assert (shipment.sum(axis=1) <= case.supply + 1e-8).all()
    assert (shipment >= 0).all()
    np.testing.assert_array_equal(case.supply, original)
    assert np.sum(shipment * case.costs) >= solve(build_model(case)).objective - 1e-8


def test_greedy_handles_surplus_zero_demand_and_ties():
    case = case_from_tables(["A", "B"], ["X", "Y"], [3, 2], [0, 2], [[1, 1], [1, 1]])
    np.testing.assert_array_equal(greedy_nearest_cost(case), [[0, 2], [0, 0]])


def test_greedy_rejects_insufficient_supply():
    case = case_from_tables(["A"], ["X"], [1], [2], [[1]])
    with pytest.raises(InvalidInputError):
        greedy_nearest_cost(case)
