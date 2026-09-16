from pathlib import Path

import pytest

from transportopt.domain import TransportationInput
from transportopt.fixtures import load_fixture

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    ("filename", "shape", "objective"),
    [("case_2x3.json", (2, 3), 620.0), ("case_3x5.json", (3, 5), 696.0)],
)
def test_loads_valid_transportation_fixture(filename, shape, objective):
    case = load_fixture(FIXTURES / filename)

    assert isinstance(case, TransportationInput)
    assert case.costs.shape == shape
    assert sum(case.supply) >= sum(case.demand)
    assert case.expected_objective == objective


def test_case_3x5_is_balanced():
    case = load_fixture(FIXTURES / "case_3x5.json")

    assert sum(case.supply) == sum(case.demand) == 55


def test_invalid_input_and_solver_infeasible_are_distinct():
    from transportopt.domain import InvalidInputError, SolverInfeasibleError

    assert not issubclass(InvalidInputError, SolverInfeasibleError)
    assert not issubclass(SolverInfeasibleError, InvalidInputError)
