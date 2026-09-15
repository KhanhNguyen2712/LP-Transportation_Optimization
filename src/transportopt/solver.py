"""SciPy HiGHS wrapper for transportation linear programs."""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog

from .model_builder import LinearProgram


@dataclass(frozen=True)
class SolveResult:
    status: str
    shipment: np.ndarray | None
    objective: float | None
    message: str = ""

    @property
    def solver_status(self) -> str:
        return self.status

    @property
    def solver_message(self) -> str:
        return self.message


def solve(model: LinearProgram) -> SolveResult:
    try:
        raw = linprog(
            model.c,
            A_ub=model.A_ub,
            b_ub=model.b_ub,
            A_eq=model.A_eq,
            b_eq=model.b_eq,
            bounds=model.bounds,
            method="highs",
        )
    except Exception as exc:
        return SolveResult("error", None, None, str(exc))
    if raw.status == 0:
        return SolveResult("optimal", np.asarray(raw.x), float(raw.fun), raw.message)
    status = "infeasible" if raw.status == 2 else "error"
    return SolveResult(status, None, None, raw.message)
