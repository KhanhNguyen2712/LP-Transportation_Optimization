"""Build the linear-program representation of a transportation input."""

from dataclasses import dataclass

import numpy as np

from .domain import TransportationInput


@dataclass(frozen=True)
class LinearProgram:
    c: np.ndarray
    A_ub: np.ndarray
    b_ub: np.ndarray
    A_eq: np.ndarray
    b_eq: np.ndarray
    bounds: tuple[float, None] = (0, None)


def build_model(case: TransportationInput) -> LinearProgram:
    """Map shipment ``x[i, j]`` to flat variable ``k = i * n + j``."""
    m, n = case.costs.shape
    variables = m * n
    supply_rows = np.zeros((m, variables))
    demand_rows = np.zeros((n, variables))
    for i in range(m):
        supply_rows[i, i * n : (i + 1) * n] = 1
    for j in range(n):
        demand_rows[j, j::n] = 1
    return LinearProgram(
        c=np.asarray(case.costs, dtype=float).reshape(-1),
        A_ub=supply_rows,
        b_ub=np.asarray(case.supply, dtype=float).copy(),
        A_eq=demand_rows,
        b_eq=np.asarray(case.demand, dtype=float).copy(),
    )
