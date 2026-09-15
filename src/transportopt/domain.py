"""Small domain contract shared by validation, solver, and presentation layers."""

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray


class InvalidInputError(ValueError):
    """The requested transportation model is malformed or invalid."""


class SolverInfeasibleError(RuntimeError):
    """A valid model has no feasible solution."""


@dataclass(frozen=True)
class TransportationInput:
    """Input arrays and labels for one transportation model."""

    warehouses: tuple[str, ...]
    customers: tuple[str, ...]
    supply: NDArray[np.float64]
    demand: NDArray[np.float64]
    costs: NDArray[np.float64]
    expected_objective: float | None = None

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "TransportationInput":
        return cls(
            warehouses=tuple(data["warehouses"]),
            customers=tuple(data["customers"]),
            supply=np.asarray(data["supply"], dtype=float),
            demand=np.asarray(data["demand"], dtype=float),
            costs=np.asarray(data["costs"], dtype=float),
            expected_objective=data.get("expected_objective"),
        )


@dataclass(frozen=True)
class TransportationResult:
    """Solver output; infeasibility is represented separately by its exception."""

    shipment: NDArray[np.float64]
    objective: float
    solver_status: str
    solver_message: str = ""
