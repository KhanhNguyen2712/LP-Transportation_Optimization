"""Data-driven teaching views; the solver remains the shared HiGHS pipeline."""

from html import escape

import numpy as np
import pandas as pd

from ..model_builder import build_model


def network_svg(case, shipment=None, customer=None):
    """Draw a bipartite network with a separate label lane for each route."""
    m, n = case.costs.shape
    routes = [
        (i, j)
        for i in range(m)
        for j in range(n)
        if (customer is None or j == customer)
        and (shipment is None or shipment[i, j] > 1e-8)
    ]
    height = max(240, 75 * max(m, n), 32 * len(routes) + 60)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 {height}" '
        'role="img" aria-label="Mạng lưới phân bổ hàng từ kho đến khách hàng">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<g font-family="sans-serif" font-size="14" fill="#0f172a">',
    ]
    for side, names, amounts, x in (
        (0, case.warehouses, case.supply, 16),
        (1, case.customers, case.demand, 744),
    ):
        for k, (name, amount) in enumerate(zip(names, amounts)):
            y = (k + 0.5) * height / len(names)
            label = escape(str(name))
            kind = "Cung" if side == 0 else "Cầu"
            svg.append(
                f'<rect x="{x}" y="{y - 26}" width="200" height="52" '
                'rx="8" fill="#e0f2fe" stroke="#0284c7"/>'
                f'<text x="{x + 10}" y="{y - 5}">{label}</text>'
                f'<text x="{x + 10}" y="{y + 16}">{kind}: {amount:g}</text>'
            )
    for k, (i, j) in enumerate(routes):
        y = 30 + (k + 0.5) * (height - 60) / len(routes)
        sy, ty = (i + 0.5) * height / m, (j + 0.5) * height / n
        label = f"c = {case.costs[i, j]:g}"
        if shipment is not None:
            label = f"x = {shipment[i, j]:g} · " + label
        svg.append(
            f'<path d="M216 {sy} L340 {y} H620 L744 {ty}" '
            'fill="none" stroke="#0284c7" stroke-width="1.5"/>'
            f'<rect x="355" y="{y - 11}" width="250" height="22" fill="#f8fafc"/>'
            f'<text x="480" y="{y + 5}" text-anchor="middle">{label} →</text>'
        )
    return "".join(svg) + "</g></svg>"


def render_network(st, case, shipment=None):
    options = ["Tất cả"] + list(case.customers)
    selected = st.selectbox(
        "Tập trung vào khách hàng",
        range(len(options)),
        format_func=lambda value: options[value],
        key="input_network" if shipment is None else "result_network",
    )
    svg = network_svg(case, shipment, None if selected == 0 else selected - 1)
    st.image(svg, width="stretch")
    st.caption(
        "Kho ở bên trái, khách hàng ở bên phải. c: chi phí/đơn vị; "
        "x: lượng giao. Đây là mạng phân bổ hàng, không phải bản đồ đường đi. "
        "Chọn một khách hàng để đọc rõ từng tuyến."
    )
    st.download_button(
        "Tải sơ đồ SVG",
        svg,
        file_name="transport-network.svg",
        mime="image/svg+xml",
        key="input_svg" if shipment is None else "result_svg",
    )


def render_model(st, case):
    model = build_model(case)
    m, n = case.costs.shape
    st.subheader("Bước 2 · Từ mạng lưới đến mô hình LP")
    render_network(st, case)
    st.write(
        f"Có {m} kho × {n} khách hàng = {m * n} biến quyết định. "
        "Mỗi biến xᵢⱼ là lượng hàng từ kho i đến khách hàng j. "
        "Các lượng hàng dùng cùng một đơn vị; chi phí tính theo đơn vị chi phí."
    )
    st.latex(r"\min Z=\sum_{i=1}^{m}\sum_{j=1}^{n}c_{ij}x_{ij}")
    st.latex(
        r"\sum_j x_{ij}\le s_i\quad(\forall i),\qquad"
        r"\sum_i x_{ij}=d_j\quad(\forall j),\qquad x_{ij}\ge0"
    )
    st.caption(
        "Mỗi kho giao không vượt cung; mỗi khách hàng nhận đúng cầu. "
        "Nếu dư cung, hàng được giữ lại tại kho, không cần thêm khách hàng giả."
    )
    with st.expander("Xem cách tạo vector và ma trận thực tế"):
        variables = [f"x_{i + 1}_{j + 1}" for i in range(m) for j in range(n)]
        st.write("Xếp biến theo từng hàng: kho 1 trước, rồi kho 2, …")
        st.dataframe(
            pd.DataFrame(
                {
                    "Biến": variables,
                    "Kho": np.repeat(case.warehouses, n),
                    "Khách hàng": np.tile(case.customers, m),
                    "c": model.c,
                }
            ),
            hide_index=True,
        )
        st.latex(r"\min c^Tx,\quad A_{ub}x\le b_{ub},\quad A_{eq}x=b_{eq},\quad x\ge0")
        st.write("A_ub và b_ub · mỗi hàng là một ràng buộc cung")
        st.dataframe(
            pd.DataFrame(
                np.column_stack((model.A_ub, model.b_ub)),
                index=case.warehouses,
                columns=variables + ["b_ub"],
            )
        )
        st.write("A_eq và b_eq · mỗi hàng là một ràng buộc cầu")
        st.dataframe(
            pd.DataFrame(
                np.column_stack((model.A_eq, model.b_eq)),
                index=case.customers,
                columns=variables + ["b_eq"],
            )
        )
