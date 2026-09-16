from pathlib import Path

import numpy as np

from transportopt.fixtures import load_fixture
from transportopt.model_builder import build_model

FIXTURES = Path(__file__).parent / "fixtures"


def test_builds_flattened_transportation_constraints():
    model = build_model(load_fixture(FIXTURES / "case_2x3.json"))

    assert model.c.shape == (6,)
    np.testing.assert_array_equal(model.c, [4, 6, 8, 5, 4, 3])
    assert model.A_ub.shape == (2, 6)
    assert model.A_eq.shape == (3, 6)
    np.testing.assert_array_equal(model.A_ub, [[1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1]])
    np.testing.assert_array_equal(
        model.A_eq, [[1, 0, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 0, 1]]
    )
    np.testing.assert_array_equal(model.b_ub, [80, 70])
    np.testing.assert_array_equal(model.b_eq, [50, 60, 40])
    assert model.bounds == (0, None)
