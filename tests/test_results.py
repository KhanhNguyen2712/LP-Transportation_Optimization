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
    solved = solve(build_model(case))
    result = analyze_result(case, solved, shipment=np.array([[50, 30, 0], [0, 30, 10]]))

    np.testing.assert_allclose(result.unused_supply, [0, 30])
    np.testing.assert_allclose(result.warehouse_utilization, [1, 40 / 70])
