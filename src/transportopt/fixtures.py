"""Load checked-in JSON transportation examples."""

import json
from pathlib import Path

from .domain import TransportationInput


def load_fixture(path: str | Path) -> TransportationInput:
    """Read one JSON fixture into the shared domain input contract."""

    with Path(path).open(encoding="utf-8") as file:
        return TransportationInput.from_mapping(json.load(file))
