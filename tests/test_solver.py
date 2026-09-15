from pathlib import Path

import pytest

from transportopt.fixtures import load_fixture
from transportopt.model_builder import build_model
from transportopt.solver import solve


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("filename", ["case_2x3.json", "case_3x5.json"])
def test_highs_solves_fixture(filename):
    case = load_fixture(FIXTURES / filename)
    result = solve(build_model(case))

    assert result.status == "optimal"
    assert result.shipment is not None
    assert result.objective == pytest.approx(case.expected_objective, abs=1e-8)


def test_nonoptimal_result_has_no_shipment():
    from transportopt.model_builder import LinearProgram
    import numpy as np

    result = solve(LinearProgram(np.array([1.0]), np.array([[1.0]]), np.array([0.0]), np.array([[1.0]]), np.array([1.0])))

    assert result.status == "infeasible"
    assert result.shipment is None
