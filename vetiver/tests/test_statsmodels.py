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
def sm_model():

    X, y = vetiver.get_mock_data()
    glm = sm.GLM(y, X).fit()

    v = vetiver.VetiverModel(glm, "glm", X)
    return v


@pytest.fixture
def vetiver_client(sm_model):  # With check_prototype=True
    app = vetiver.VetiverAPI(sm_model, check_prototype=True)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.fixture
def vetiver_client_check_ptype_false(sm_model):  # With check_prototype=True
    app = vetiver.VetiverAPI(sm_model, check_prototype=False)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


def test_vetiver_build(vetiver_client):
    data = [{"B": 0, "C": 0, "D": 0}]

    response = vetiver.predict(endpoint=vetiver_client, data=data)

    assert response.iloc[0, 0] == 0.0
    assert len(response) == 1


def test_batch(vetiver_client):
    data = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))

    response = vetiver.predict(endpoint=vetiver_client, data=data)

    assert len(response) == 100


def test_no_ptype(vetiver_client_check_ptype_false):
    data = [0, 0, 0]

    response = vetiver.predict(endpoint=vetiver_client_check_ptype_false, data=data)

    assert response.iloc[0, 0] == 0.0
    assert len(response) == 1


def test_serialize(sm_model):
    import pins

    board = pins.board_temp(allow_pickle_read=True)
    vetiver.vetiver_pin_write(board=board, model=sm_model)
    assert isinstance(
        board.pin_read("glm"),
        statsmodels.genmod.generalized_linear_model.GLMResultsWrapper,
    )
    board.pin_delete("glm")
