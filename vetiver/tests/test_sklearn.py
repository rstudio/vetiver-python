import pytest

import numpy as np
import pandas as pd
from requests.exceptions import HTTPError
from fastapi.testclient import TestClient

from vetiver import mock, VetiverModel, VetiverAPI
from vetiver.server import predict

np.random.seed(500)
X, y = mock.get_mock_data()


@pytest.fixture
def vetiver_model():
    np.random.seed(500)
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        prototype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    return v


@pytest.fixture
def vetiver_client(vetiver_model):  # With check_ptype=True
    app = VetiverAPI(vetiver_model, check_prototype=True)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.fixture
def vetiver_client_check_ptype_false(vetiver_model):  # With check_ptype=False
    app = VetiverAPI(vetiver_model, check_prototype=False)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.mark.parametrize(
    "data,length",
    [({"B": 0, "C": 0, "D": 0}, 1), (pd.Series(data=[0, 0, 0]), 1), (X, 100)],
)
def test_predict_sklearn_ptype(data, length, vetiver_client):

    response = predict(endpoint=vetiver_client, data=data)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == length


@pytest.mark.parametrize(
    "data,length",
    [({"B": 0, "C": 0, "D": 0}, 1), (pd.Series(data=[0, 0, 0]), 1), (X, 100)],
)
def test_predict_sklearn_no_ptype(data, length, vetiver_client_check_ptype_false):
    X, y = mock.get_mock_data()
    response = predict(endpoint=vetiver_client_check_ptype_false, data=data)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == length


@pytest.mark.parametrize("data", [(0), 0, 0.0, "0"])
def test_predict_sklearn_type_error(data, vetiver_client):

    msg = str(
        "[{'type': 'list_type', 'loc': ('body',), 'msg': 'Input should be a valid list', \
        'input': '0', 'url': 'https://errors.pydantic.dev/2.0.3/v/list_type'}]"
    )

    with pytest.raises(TypeError, match=msg):
        predict(endpoint=vetiver_client, data=data)


def test_predict_server_error(vetiver_model):
    X, y = mock.get_mock_data()
    app = VetiverAPI(vetiver_model, check_prototype=True)
    app.app.root_path = "/i_do_not_exists"
    client = TestClient(app.app)

    with pytest.raises(HTTPError):
        predict(endpoint=client, data=X)
