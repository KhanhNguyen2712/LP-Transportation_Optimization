"""Input-table helpers used by the Streamlit form and its tests."""

from pathlib import Path
from typing import Sequence

import numpy as np

from ..domain import TransportationInput
from ..fixtures import load_fixture

_FIXTURES = Path(__file__).parents[3] / "tests" / "fixtures"
_FIXTURE_FILES = {
    "2 × 3 example": "case_2x3.json",
    "3 × 5 example": "case_3x5.json",
}


def fixture_options() -> tuple[str, ...]:
    return tuple(_FIXTURE_FILES)


def load_named_fixture(name: str) -> TransportationInput:
    try:
        filename = _FIXTURE_FILES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown fixture: {name}") from exc
    return load_fixture(_FIXTURES / filename)


def case_from_tables(
    warehouses: Sequence[str],
    customers: Sequence[str],
    supply: Sequence[float],
    demand: Sequence[float],
    costs: Sequence[Sequence[float]],
) -> TransportationInput:
    """Convert editable table values into the shared domain input contract."""

    return TransportationInput(
        warehouses=tuple(str(value) for value in warehouses),
        customers=tuple(str(value) for value in customers),
        supply=np.asarray(supply, dtype=float),
        demand=np.asarray(demand, dtype=float),
        costs=np.asarray(costs, dtype=float),
    )
