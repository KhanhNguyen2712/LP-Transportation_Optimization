"""Validation for transportation-model inputs before solving."""

import numpy as np

from .domain import InvalidInputError, TransportationInput


def validate_input(case: TransportationInput) -> TransportationInput:
    """Validate a transportation input and return it unchanged when valid."""

    _validate_labels(case.warehouses, "warehouse")
    _validate_labels(case.customers, "customer")

    warehouse_count = len(case.warehouses)
    customer_count = len(case.customers)
    try:
        supply = np.asarray(case.supply, dtype=float)
        demand = np.asarray(case.demand, dtype=float)
        costs = np.asarray(case.costs, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise InvalidInputError("Supply, demand, and costs must be numeric.") from exc

    if supply.ndim != 1 or supply.shape != (warehouse_count,):
        raise InvalidInputError("Supply must have one value for each warehouse.")
    if demand.ndim != 1 or demand.shape != (customer_count,):
        raise InvalidInputError("Demand must have one value for each customer.")
    if costs.ndim != 2 or costs.shape != (warehouse_count, customer_count):
        raise InvalidInputError("Costs must match the warehouse-by-customer matrix size.")

    for name, values in (("Supply", supply), ("demand", demand), ("Costs", costs)):
        if not np.isfinite(values).all():
            raise InvalidInputError(f"{name} must contain only finite values.")
        if (values < 0).any():
            raise InvalidInputError(f"{name} cannot contain negative values.")

    if supply.sum() < demand.sum():
        raise InvalidInputError(
            "Total supply is less than total demand; add supply or reduce demand."
        )
    return case


def _validate_labels(labels: tuple[str, ...], kind: str) -> None:
    if any(not isinstance(label, str) or not label.strip() for label in labels):
        raise InvalidInputError(f"Each {kind} name must be non-empty.")
    if len(set(labels)) != len(labels):
        raise InvalidInputError(f"{kind.title()} names must be unique.")
