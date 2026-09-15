"""Result presentation helpers."""

from typing import Any, Sequence

from ..results import ResultAnalysis


def positive_route_rows(analysis: ResultAnalysis) -> list[dict[str, Any]]:
    return [dict(route) for route in analysis.routes]


def render_result(
    st: Any, analysis: ResultAnalysis, warehouses: Sequence[str]
) -> None:
    st.success(f"Optimal solution found · total cost: {analysis.objective:.2f}")
    st.subheader("Positive routes")
    st.dataframe(positive_route_rows(analysis), use_container_width=True)

    st.subheader("Warehouse usage")
    rows = [
        {
            "warehouse": warehouse,
            "unused supply": float(unused),
            "utilization": f"{float(utilization):.1%}",
        }
        for warehouse, unused, utilization in zip(
            warehouses, analysis.unused_supply, analysis.warehouse_utilization
        )
    ]
    st.dataframe(rows, use_container_width=True)
