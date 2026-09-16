from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from transportopt.fixtures import load_fixture
from transportopt.model_builder import build_model
from transportopt.results import analyze_result
from transportopt.solver import solve

FIXTURES = Path(__file__).parent / "fixtures"


def test_analysis_recomputes_routes_residuals_and_utilization():
    case = load_fixture(FIXTURES / "case_2x3.json")
    solved = solve(build_model(case))
    result = analyze_result(case, solved)

    assert result.objective == pytest.approx(np.sum(case.costs * result.shipment))
    np.testing.assert_allclose(result.demand_residual, 0, atol=1e-8)
    assert result.supply_violation.max() <= 1e-8
    assert result.nonnegativity_violation.max() <= 1e-8
    assert np.all(result.shipment >= -1e-8)
    assert all(route["flow"] > 0 for route in result.routes)
    np.testing.assert_allclose(result.unused_supply, [0, 0])
    np.testing.assert_allclose(result.warehouse_utilization, [1, 1])


def test_analysis_reports_surplus_supply():
    case = load_fixture(FIXTURES / "case_2x3.json")
    case = replace(case, supply=np.array([80.0, 100.0]))
    solved = solve(build_model(case))
    result = analyze_result(case, solved, shipment=np.array([[50, 30, 0], [0, 30, 40]]))

    np.testing.assert_allclose(result.unused_supply, [0, 30])
    np.testing.assert_allclose(result.warehouse_utilization, [1, 0.7])


def test_case_3x5_analysis_is_feasible():
    case = load_fixture(FIXTURES / "case_3x5.json")
    result = analyze_result(case, solve(build_model(case)))

    assert result.objective == pytest.approx(696.0, abs=1e-8)
    assert np.max(np.abs(result.demand_residual)) <= 1e-8
    assert np.max(result.supply_violation) <= 1e-8
    assert np.max(result.nonnegativity_violation) <= 1e-8


@pytest.mark.parametrize(
    ("shipment", "message"),
    [
        (np.array([[50, 0, 0], [0, 60, 0]]), "demand residual"),
        (np.array([[50, 60, 0], [0, 0, 40]]), "exceeds warehouse supply"),
        (np.array([[50, 30, -1], [0, 30, 41]]), "negative flow"),
    ],
)
def test_analysis_rejects_infeasible_manual_shipment(shipment, message):
    case = load_fixture(FIXTURES / "case_2x3.json")

    with pytest.raises(ValueError, match=message):
        analyze_result(case, solve(build_model(case)), shipment=shipment)
