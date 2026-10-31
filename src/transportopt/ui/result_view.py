"""Result presentation helpers."""

from typing import Any

import numpy as np
import pandas as pd

from ..domain import TransportationInput
from ..results import ResultAnalysis
from .explanation import render_network


def positive_route_rows(analysis: ResultAnalysis) -> list[dict[str, Any]]:
    return [dict(route) for route in analysis.routes]


def render_result(st: Any, analysis: ResultAnalysis, case: TransportationInput) -> None:
    st.subheader("Bước 4 · Đọc và kiểm chứng phương án")
    st.success(f"Đã tìm thấy nghiệm tối ưu · tổng chi phí: {analysis.objective:.2f}")
    network, details, checks = st.tabs(
        [
            "Sơ đồ vận chuyển",
            "Phân bổ và chi phí",
            "Kiểm chứng nghiệm",
        ]
    )
    with network:
        st.write("Chỉ các tuyến có lượng giao dương được vẽ trong phương án.")
        render_network(st, case, analysis.shipment)
    with details:
        st.write("Ma trận lượng giao X · ô bằng 0 là tuyến không sử dụng")
        st.dataframe(
            pd.DataFrame(
                analysis.shipment,
                index=case.warehouses,
                columns=case.customers,
            )
        )
        routes = pd.DataFrame(
            positive_route_rows(analysis),
            columns=[
                "warehouse",
                "customer",
                "flow",
                "cost",
            ],
        )
        routes["Thành tiền"] = routes["flow"] * routes["cost"]
        routes = routes.rename(
            columns={
                "warehouse": "Kho",
                "customer": "Khách hàng",
                "flow": "Lượng giao",
                "cost": "Chi phí/đơn vị",
            }
        )
        st.write("Tính chi phí từng tuyến: lượng giao × chi phí/đơn vị")
        st.dataframe(routes, hide_index=True)
        st.code(
            " + ".join(
                f"{route['flow']:g} × {route['cost']:g}" for route in analysis.routes
            )
            + f" = {analysis.objective:g}",
            language=None,
        )
        st.latex(r"Z=\sum_{i,j}c_{ij}x_{ij}=" + f"{analysis.objective:g}")
        st.caption(
            "Tổng cột Thành tiền bằng tổng chi phí; không làm tròn trước khi tính."
        )
        st.download_button(
            "Tải phương án CSV",
            routes.to_csv(index=False).encode("utf-8-sig"),
            file_name="transport-plan.csv",
            mime="text/csv",
        )
    with checks:
        st.write("Kiểm tra cung: tổng theo hàng của X không vượt cung kho")
        warehouse_rows = pd.DataFrame(
            {
                "Kho": case.warehouses,
                "Cung": case.supply,
                "Đã giao": analysis.shipment.sum(axis=1),
                "Còn lại": analysis.unused_supply,
                "Sử dụng (%)": 100 * analysis.warehouse_utilization,
            }
        ).set_index("Kho")
        st.dataframe(warehouse_rows)
        st.bar_chart(warehouse_rows[["Đã giao", "Còn lại"]], stack=True)
        st.write("Kiểm tra cầu: tổng theo cột của X bằng nhu cầu khách hàng")
        st.dataframe(
            pd.DataFrame(
                {
                    "Khách hàng": case.customers,
                    "Cầu": case.demand,
                    "Đã nhận": analysis.shipment.sum(axis=0),
                    "Sai số": analysis.demand_residual,
                }
            ),
            hide_index=True,
        )
        residual = max(
            np.max(np.abs(analysis.demand_residual), initial=0),
            np.max(analysis.supply_violation, initial=0),
            np.max(analysis.nonnegativity_violation, initial=0),
        )
        st.metric("Vi phạm lớn nhất (ngưỡng 1e-8)", f"{residual:.2e}")
        st.caption(
            "Kiểm chứng trên xác nhận tính khả thi. Tính tối ưu dựa trên trạng thái "
            "optimal của HiGHS; có thể tồn tại nhiều phương án cùng chi phí tối ưu."
        )
        st.code(analysis.solver_message, language=None)
