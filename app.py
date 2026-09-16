"""Small Streamlit front end for the transportation linear program."""

import numpy as np


class FeasibilityGateError(RuntimeError):
    """The solver returned a result that fails the presentation safety gate."""


def _require_feasible(analysis, tolerance=1e-8):
    checks = (
        ("customer demand", analysis.demand_residual),
        ("warehouse supply", analysis.supply_violation),
        ("nonnegative shipment", analysis.nonnegativity_violation),
    )
    for label, values in checks:
        values = np.asarray(values, dtype=float)
        if (
            not np.isfinite(values).all()
            or np.max(np.abs(values), initial=0.0) > tolerance
        ):
            raise FeasibilityGateError(
                f"{label} check failed; result was not displayed."
            )
    if not np.isfinite(float(analysis.objective)):
        raise FeasibilityGateError("Objective check failed; result was not displayed.")
    return analysis


def _resize(values, size, fill):
    values = list(values[:size])
    return values + [fill] * (size - len(values))


def _resize_matrix(values, rows, columns):
    return [
        _resize(values[row] if row < len(values) else [], columns, 0.0)
        for row in range(rows)
    ]


def main():
    import pandas as pd
    import streamlit as st

    from transportopt.domain import InvalidInputError
    from transportopt.model_builder import build_model
    from transportopt.results import analyze_result
    from transportopt.solver import solve
    from transportopt.ui.input_form import (
        case_from_tables,
        fixture_options,
        load_named_fixture,
    )
    from transportopt.ui.result_view import render_result
    from transportopt.validation import validate_input

    st.set_page_config(page_title="TransportOpt")
    st.title("TransportOpt")
    st.caption("Solve a transportation problem with linear programming.")

    if "case" not in st.session_state:
        st.session_state.case = load_named_fixture(fixture_options()[0])

    with st.sidebar:
        st.header("Examples")
        fixture_name = st.selectbox("Load a fixture", fixture_options())
        if st.button("Load fixture"):
            st.session_state.case = load_named_fixture(fixture_name)
            st.rerun()

    current = st.session_state.case
    warehouse_count = st.number_input(
        "Warehouses", min_value=1, max_value=20, value=len(current.warehouses), step=1
    )
    customer_count = st.number_input(
        "Customers", min_value=1, max_value=20, value=len(current.customers), step=1
    )
    rows = _resize(current.warehouses, warehouse_count, "Warehouse")
    columns = _resize(current.customers, customer_count, "Customer")
    supply = _resize(current.supply.tolist(), warehouse_count, 0.0)
    demand = _resize(current.demand.tolist(), customer_count, 0.0)
    costs = _resize_matrix(current.costs.tolist(), warehouse_count, customer_count)

    st.subheader("Model input")
    left, right = st.columns(2)
    with left:
        st.write("Warehouse names and supply")
        warehouse_data = pd.DataFrame({"name": rows, "supply": supply})
        warehouse_data = st.data_editor(
            warehouse_data, hide_index=True, num_rows="fixed", key="warehouses"
        )
    with right:
        st.write("Customer names and demand")
        customer_data = pd.DataFrame({"name": columns, "demand": demand})
        customer_data = st.data_editor(
            customer_data, hide_index=True, num_rows="fixed", key="customers"
        )

    cost_data = pd.DataFrame(
        costs, index=list(warehouse_data["name"]), columns=list(customer_data["name"])
    )
    st.write("Unit cost matrix")
    cost_data = st.data_editor(cost_data, key="costs", use_container_width=True)

    if st.button("Validate and solve", type="primary"):
        try:
            case = case_from_tables(
                warehouse_data["name"].tolist(),
                customer_data["name"].tolist(),
                warehouse_data["supply"].tolist(),
                customer_data["demand"].tolist(),
                cost_data.to_numpy(),
            )
            validate_input(case)
            solved = solve(build_model(case))
            if solved.status == "infeasible":
                st.error(
                    f"No feasible solution exists for these inputs: {solved.message}"
                )
            elif solved.status == "error":
                st.error(
                    f"The solver failed before producing a result: {solved.message}"
                )
            elif solved.status != "optimal":
                st.error(f"Solver returned an unexpected status: {solved.status}")
            else:
                analysis = _require_feasible(analyze_result(case, solved))
                render_result(st, analysis, case.warehouses)
        except FeasibilityGateError as exc:
            st.error(f"The solution could not be verified: {exc}")
        except (InvalidInputError, TypeError, ValueError) as exc:
            st.error(f"Please fix the input: {exc}")


if __name__ == "__main__":
    main()
