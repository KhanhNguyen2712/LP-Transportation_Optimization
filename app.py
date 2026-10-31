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
    from transportopt.ui.explanation import render_model
    from transportopt.ui.input_form import (
        case_from_tables,
        fixture_options,
        load_named_fixture,
    )
    from transportopt.ui.result_view import render_result
    from transportopt.validation import validate_input

    st.set_page_config(page_title="TransportOpt · Demo vận tải", layout="wide")
    st.title("TransportOpt")
    st.caption("Tối ưu phân bổ hàng từ kho đến khách hàng · Quy hoạch tuyến tính")
    st.write("Nhập dữ liệu → Lập mô hình → Giải bằng HiGHS → Kiểm chứng phương án")

    if "case" not in st.session_state:
        st.session_state.case = load_named_fixture(fixture_options()[0])

    with st.sidebar:
        st.header("Dữ liệu demo")
        fixture_name = st.selectbox("Chọn ví dụ", fixture_options())
        if st.button("Nạp ví dụ", key="load_fixture"):
            st.session_state.case = load_named_fixture(fixture_name)
            for key in (
                "warehouses",
                "customers",
                "costs",
                "solution",
                "input_network",
                "result_network",
            ):
                st.session_state.pop(key, None)
            st.session_state.warehouse_count = len(st.session_state.case.warehouses)
            st.session_state.customer_count = len(st.session_state.case.customers)
            st.rerun()
        st.caption("2 × 3: chi phí 620 · 3 × 5: chi phí 696")
        st.caption("Mô hình một loại hàng, chi phí tuyến tính, cung/cầu đã biết.")

    st.subheader("Bước 1 · Nhập kho, khách hàng và chi phí")
    current = st.session_state.case
    warehouse_count = st.number_input(
        "Số kho",
        min_value=1,
        max_value=20,
        value=len(current.warehouses),
        step=1,
        key="warehouse_count",
    )
    customer_count = st.number_input(
        "Số khách hàng",
        min_value=1,
        max_value=20,
        value=len(current.customers),
        step=1,
        key="customer_count",
    )
    rows = [
        current.warehouses[i] if i < len(current.warehouses) else f"Kho {i + 1}"
        for i in range(warehouse_count)
    ]
    columns = [
        current.customers[j] if j < len(current.customers) else f"Khách {j + 1}"
        for j in range(customer_count)
    ]
    supply = _resize(current.supply.tolist(), warehouse_count, 0.0)
    demand = _resize(current.demand.tolist(), customer_count, 0.0)
    costs = _resize_matrix(current.costs.tolist(), warehouse_count, customer_count)

    left, right = st.columns(2)
    with left:
        st.write("Tên kho và lượng cung (supply)")
        warehouse_data = pd.DataFrame({"name": rows, "supply": supply})
        warehouse_data = st.data_editor(
            warehouse_data, hide_index=True, num_rows="fixed", key="warehouses"
        )
    with right:
        st.write("Tên khách hàng và lượng cầu (demand)")
        customer_data = pd.DataFrame({"name": columns, "demand": demand})
        customer_data = st.data_editor(
            customer_data, hide_index=True, num_rows="fixed", key="customers"
        )

    cost_data = pd.DataFrame(
        costs, index=list(warehouse_data["name"]), columns=list(customer_data["name"])
    )
    st.write("Ma trận chi phí/đơn vị · hàng là kho, cột là khách hàng")
    cost_data = st.data_editor(cost_data, key="costs", width="stretch")

    try:
        case = case_from_tables(
            warehouse_data["name"].tolist(),
            customer_data["name"].tolist(),
            warehouse_data["supply"].tolist(),
            customer_data["demand"].tolist(),
            cost_data.to_numpy(),
        )
        validate_input(case)
    except (InvalidInputError, TypeError, ValueError) as exc:
        st.session_state.pop("solution", None)
        st.error(f"Dữ liệu chưa hợp lệ: {exc}")
        return

    signature = (
        case.warehouses,
        case.customers,
        case.supply.tobytes(),
        case.demand.tobytes(),
        case.costs.tobytes(),
    )
    previous = st.session_state.get("solution")
    if previous is not None and previous[0] != signature:
        st.session_state.pop("solution", None)
        st.info("Dữ liệu đã thay đổi. Bấm giải lại để cập nhật phương án.")

    left, middle, right = st.columns(3)
    left.metric("Tổng cung", f"{case.supply.sum():g}")
    middle.metric("Tổng cầu", f"{case.demand.sum():g}")
    right.metric("Cung dư", f"{case.supply.sum() - case.demand.sum():g}")
    render_model(st, case)
    st.subheader("Bước 3 · Giải bài toán")
    st.caption(
        "SciPy linprog(method='highs') nhận mô hình LP và tìm nghiệm tối ưu. "
        "Phần diễn giải trình bày cách lập mô hình và kiểm chứng kết quả; "
        "không phải nhật ký các vòng lặp Simplex/MODI bên trong solver."
    )
    if st.button("Tìm phương án tối ưu", type="primary", key="solve"):
        st.session_state.pop("solution", None)
        try:
            solved = solve(build_model(case))
            if solved.status == "optimal":
                analysis = _require_feasible(analyze_result(case, solved))
                st.session_state.solution = (signature, analysis)
            else:
                st.error(
                    f"Không tìm được nghiệm tối ưu ({solved.status}): {solved.message}"
                )
        except FeasibilityGateError as exc:
            st.error(f"Không thể xác minh nghiệm: {exc}")
        except (InvalidInputError, TypeError, ValueError) as exc:
            st.error(f"Không thể giải bài toán: {exc}")

    if "solution" in st.session_state:
        render_result(st, st.session_state.solution[1], case)


if __name__ == "__main__":
    main()
