import numpy as np
import pytest

from app import FeasibilityGateError, _require_feasible
from transportopt.domain import TransportationInput
from transportopt.results import analyze_result
from transportopt.solver import SolveResult
from transportopt.ui.input_form import case_from_tables
from transportopt.ui.result_view import positive_route_rows


class _Analysis:
    objective = 10.0
    demand_residual = np.array([0.0])
    supply_violation = np.array([0.0])
    nonnegativity_violation = np.array([0.0])


def test_feasibility_gate_allows_verified_analysis():
    assert _require_feasible(_Analysis()) is not None


def test_feasibility_gate_rejects_unverified_analysis():
    analysis = _Analysis()
    analysis.demand_residual = np.array([0.1])

    with pytest.raises(FeasibilityGateError, match="customer demand"):
        _require_feasible(analysis)


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


def test_network_svg_escapes_names_and_omits_unused_routes():
    from xml.etree import ElementTree

    from transportopt.ui.explanation import network_svg

    case = case_from_tables(["<Kho & A>"], ["C1", "C2"], [3], [3, 0], [[4, 5]])
    svg = network_svg(case, np.array([[3.0, 0.0]]))
    root = ElementTree.fromstring(svg)
    assert "<Kho & A>" in "".join(root.itertext())
    assert "x = 3" in svg
    assert "c = 5" not in svg
    assert len(root.findall(".//{http://www.w3.org/2000/svg}path")) == 1


@pytest.mark.parametrize(
    "fixture, objective", [("2 × 3 example", "620.00"), ("3 × 5 example", "696.00")]
)
def test_demo_solves_and_keeps_result_when_filtering(fixture, objective):
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file("../app.py", default_timeout=15).run()
    at.sidebar.selectbox[0].select(fixture).run()
    at.button(key="load_fixture").click().run()
    at.button(key="solve").click().run()
    assert not at.exception
    assert objective in at.success[0].value
    analysis = at.session_state["solution"][1]
    assert float(objective) == pytest.approx(analysis.objective)
    at.selectbox(key="result_network").select(1).run()
    assert not at.exception
    assert objective in at.success[0].value
    assert at.metric[-1].value == "0.00e+00"
    at.number_input(key="warehouse_count").set_value(1).run()
    assert not at.exception
    assert at.error
    assert not at.success


def test_demo_surplus_zero_and_invalid_input():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file("../app.py", default_timeout=15)
    at.session_state["case"] = case_from_tables(
        ["W1", "W2"],
        ["C1"],
        [10, 5],
        [3],
        [[1], [2]],
    )
    at.run().button(key="solve").click().run()
    assert not at.exception
    assert "3.00" in at.success[0].value
    assert at.session_state["solution"][1].unused_supply.sum() == 12
    at.session_state["case"] = case_from_tables(["W"], ["C"], [0], [0], [[0]])
    at.run().button(key="solve").click().run()
    assert not at.exception
    assert "0.00" in at.success[0].value
    at.session_state["case"] = case_from_tables(["W"], ["C"], [-1], [0], [[0]])
    at.run()
    assert not at.exception
    assert at.error
    assert not at.success


def test_demo_cost_edit_invalidates_old_solution():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file("../app.py", default_timeout=15).run()
    at.button(key="solve").click().run()
    assert at.success
    at.session_state["costs"] = {
        "edited_rows": {0: {"C1": 9}},
        "added_rows": [],
        "deleted_rows": [],
    }
    at.run()
    assert not at.exception
    assert not at.success
    assert at.info
    at.button(key="solve").click().run()
    assert not at.exception
    assert at.success
