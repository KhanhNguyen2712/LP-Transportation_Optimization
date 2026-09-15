import numpy as np

from transportopt.ui.input_form import case_from_tables
from transportopt.ui.result_view import positive_route_rows
from transportopt.domain import TransportationInput
from transportopt.results import analyze_result
from transportopt.solver import SolveResult


def test_case_from_tables_builds_dimensioned_input():
    case = case_from_tables(
        ["W1", "W2"],
        ["C1", "C2"],
        [10, 20],
        [15, 10],
        [[1, 2], [3, 4]],
    )

    assert isinstance(case, TransportationInput)
    assert case.costs.shape == (2, 2)
    np.testing.assert_array_equal(case.supply, [10, 20])


def test_positive_route_rows_exposes_only_shipped_routes():
    case = TransportationInput.from_mapping(
        {
            "warehouses": ["W1"],
            "customers": ["C1", "C2"],
            "supply": [3],
            "demand": [2, 1],
            "costs": [[4, 5]],
        }
    )
    analysis = analyze_result(
        case,
        SolveResult("optimal", np.array([2.0, 1.0]), 13.0),
    )

    assert positive_route_rows(analysis) == [
        {"warehouse": "W1", "customer": "C1", "flow": 2.0, "cost": 4.0},
        {"warehouse": "W1", "customer": "C2", "flow": 1.0, "cost": 5.0},
    ]
