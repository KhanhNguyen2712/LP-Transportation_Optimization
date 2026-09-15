from pathlib import Path
from dataclasses import replace

import numpy as np
import pytest

from transportopt.domain import InvalidInputError
from transportopt.fixtures import load_fixture
from transportopt.validation import validate_input


FIXTURES = Path(__file__).parent / "fixtures"


def test_valid_fixture_is_accepted():
    case = load_fixture(FIXTURES / "case_2x3.json")

    assert validate_input(case) is case


def _case():
    return load_fixture(FIXTURES / "case_2x3.json")


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("warehouses", ("W1", ""), "non-empty"),
        ("customers", ("C1", "", "C3"), "non-empty"),
        ("warehouses", ("W1", "W1"), "unique"),
        ("customers", ("C1", "C1", "C3"), "unique"),
        ("supply", np.array([80.0]), "one value"),
        ("demand", np.array([50.0, 60.0]), "one value"),
        ("costs", np.ones((3, 3)), "matrix size"),
        ("supply", np.array([np.nan, 70.0]), "finite"),
        ("demand", np.array([50.0, np.inf, 40.0]), "finite"),
        ("costs", np.array([[4.0, 6.0, np.inf], [5.0, 4.0, 3.0]]), "finite"),
        ("supply", np.array([-1.0, 70.0]), "negative"),
        ("demand", np.array([50.0, -1.0, 40.0]), "negative"),
        ("costs", np.array([[4.0, -1.0, 8.0], [5.0, 4.0, 3.0]]), "negative"),
    ],
)
def test_rejects_invalid_input(field, value, message):
    case = replace(_case(), **{field: value})

    with pytest.raises(InvalidInputError, match=message):
        validate_input(case)


def test_rejects_insufficient_supply_with_explanation():
    case = replace(_case(), supply=np.array([20.0, 20.0]))

    with pytest.raises(InvalidInputError, match="supply.*less than.*demand"):
        validate_input(case)


def test_accepts_surplus_supply_and_zero_costs():
    case = replace(
        _case(),
        supply=np.array([100.0, 70.0]),
        costs=np.zeros((2, 3)),
    )

    assert validate_input(case) is case


@pytest.mark.parametrize("field", ["warehouses", "customers"])
def test_rejects_malformed_label_container(field):
    with pytest.raises(InvalidInputError, match="name"):
        validate_input(replace(_case(), **{field: None}))


def test_rejects_non_reusable_generator_labels():
    case = replace(_case(), warehouses=(label for label in ("W1", "W2")))

    with pytest.raises(InvalidInputError, match="reusable"):
        validate_input(case)


def test_rejects_insufficient_extreme_supply_without_sum_overflow():
    case = replace(
        _case(),
        supply=np.array([1e308, 1e308]),
        demand=np.array([1e308, 1e308, 1e308]),
    )

    with pytest.raises(InvalidInputError, match="supply.*less than.*demand"):
        validate_input(case)


def test_rejects_tiny_demand_beyond_large_supply():
    case = replace(
        _case(),
        supply=np.array([1e308, 0.0]),
        demand=np.array([1e308, 1e-323, 0.0]),
    )

    with pytest.raises(InvalidInputError, match="supply.*less than.*demand"):
        validate_input(case)
