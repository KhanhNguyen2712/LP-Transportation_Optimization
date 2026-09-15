"""Recompute and summarize a solved transportation shipment."""

from dataclasses import dataclass

import numpy as np

from .domain import TransportationInput
from .solver import SolveResult


@dataclass(frozen=True)
class ResultAnalysis:
    shipment: np.ndarray
    objective: float
    routes: tuple[dict[str, object], ...]
    unused_supply: np.ndarray
    demand_residual: np.ndarray
    supply_violation: np.ndarray
    nonnegativity_violation: np.ndarray
    warehouse_utilization: np.ndarray
    solver_status: str
    solver_message: str = ""

    @property
    def cost(self) -> float:
        return self.objective

    @property
    def customer_residual(self) -> np.ndarray:
        return self.demand_residual


def analyze_result(
    case: TransportationInput,
    solved: SolveResult,
    shipment: np.ndarray | None = None,
    tolerance: float = 1e-8,
) -> ResultAnalysis:
    values = solved.shipment if shipment is None else shipment
    if solved.status != "optimal" or values is None:
        raise ValueError("Cannot analyze a non-optimal solve result without shipment.")
    matrix = np.asarray(values, dtype=float).reshape(case.costs.shape)
    shipped_by_warehouse = matrix.sum(axis=1)
    demand_residual = matrix.sum(axis=0) - case.demand
    unused_supply = case.supply - shipped_by_warehouse
    supply_violation = np.maximum(shipped_by_warehouse - case.supply, 0)
    nonnegativity_violation = np.maximum(-matrix, 0)
    utilization = np.divide(
        shipped_by_warehouse,
        case.supply,
        out=np.zeros_like(shipped_by_warehouse),
        where=case.supply != 0,
    )
    routes = tuple(
        {"warehouse": case.warehouses[i], "customer": case.customers[j], "flow": float(matrix[i, j]), "cost": float(case.costs[i, j])}
        for i in range(matrix.shape[0])
        for j in range(matrix.shape[1])
        if matrix[i, j] > tolerance
    )
    return ResultAnalysis(
        shipment=matrix,
        objective=float(np.sum(case.costs * matrix)),
        routes=routes,
        unused_supply=unused_supply,
        demand_residual=demand_residual,
        supply_violation=supply_violation,
        nonnegativity_violation=nonnegativity_violation,
        warehouse_utilization=utilization,
        solver_status=solved.status,
        solver_message=solved.message,
    )


analyze = analyze_result
