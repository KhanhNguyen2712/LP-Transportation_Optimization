"""Deterministic feasible allocation for comparison with the LP optimum."""

import numpy as np

from .domain import TransportationInput
from .validation import validate_input


def greedy_nearest_cost(case: TransportationInput) -> np.ndarray:
    """Serve customers in input order, cheapest available warehouse first.

    Equal costs use warehouse input order. This is not a global optimum claim.
    """
    validate_input(case)
    remaining_supply = case.supply.copy()
    shipment = np.zeros_like(case.costs)
    for j, demand in enumerate(case.demand):
        remaining = float(demand)
        for i in np.argsort(case.costs[:, j], kind="stable"):
            quantity = min(remaining, remaining_supply[i])
            shipment[i, j] = quantity
            remaining_supply[i] -= quantity
            remaining -= quantity
            if remaining <= 0:
                break
        if remaining > 1e-8:
            raise ValueError("Greedy allocation could not satisfy customer demand.")
    return shipment
