import pytest

sm = pytest.importorskip("statsmodels.api", reason="statsmodels library not installed")

statsmodels = pytest.importorskip(
    "statsmodels", reason="statsmodels library not installed"
)

import numpy as np  # noqa
from fastapi.testclient import TestClient  # noqa

import vetiver  # noqa


@pytest.fixture
def build_sm():

    X, y = vetiver.get_mock_data()
    glm = sm.GLM(y, X).fit()

    v = vetiver.VetiverModel(glm, "glm", X)
    return v


def test_vetiver_build(build_sm):
    api = vetiver.VetiverAPI(build_sm)
    client = TestClient(api.app)
    data = {"B": 0, "C": 0, "D": 0}
    response = client.post("/predict", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"prediction": [0.0]}, response.json()


def test_serialize(build_sm):
    import pins

    board = pins.board_temp(allow_pickle_read=True)
    vetiver.vetiver_pin_write(board=board, model=build_sm)
    assert isinstance(
        board.pin_read("glm"),
        statsmodels.genmod.generalized_linear_model.GLMResultsWrapper,
    )
    board.pin_delete("glm")
