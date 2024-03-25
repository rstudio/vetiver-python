import pytest

sm = pytest.importorskip("statsmodels.api", reason="statsmodels library not installed")

statsmodels = pytest.importorskip(
    "statsmodels", reason="statsmodels library not installed"
)

import numpy as np  # noqa
import pandas as pd  # noqa
from fastapi.testclient import TestClient  # noqa

import vetiver  # noqa


@pytest.fixture
def model():

    X, y = vetiver.get_mock_data()
    glm = sm.GLM(y, X).fit()

    v = vetiver.VetiverModel(glm, "glm", X)
    return v


def test_vetiver_build(client):
    data = [{"B": 0, "C": 0, "D": 0}]

    response = vetiver.predict(endpoint="/predict/", data=data, test_client=client)

    assert response.iloc[0, 0] == 0.0
    assert len(response) == 1


def test_batch(client):
    data = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))

    response = vetiver.predict(endpoint="/predict/", data=data, test_client=client)

    assert len(response) == 100


def test_no_ptype(client_no_prototype):
    data = [0, 0, 0]

    response = vetiver.predict(
        endpoint="/predict/", data=data, test_client=client_no_prototype
    )

    assert response.iloc[0, 0] == 0.0
    assert len(response) == 1


def test_serialize(model):
    import pins

    board = pins.board_temp(allow_pickle_read=True)
    vetiver.vetiver_pin_write(board=board, model=model)
    assert isinstance(
        board.pin_read("glm"),
        statsmodels.genmod.generalized_linear_model.GLMResultsWrapper,
    )
    board.pin_delete("glm")
