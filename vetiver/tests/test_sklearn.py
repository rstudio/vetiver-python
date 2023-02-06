import pytest

import numpy as np
import pandas as pd
from requests.exceptions import HTTPError
from fastapi.testclient import TestClient

from vetiver import mock, VetiverModel, VetiverAPI
from vetiver.server import predict


@pytest.fixture
def vetiver_model():
    np.random.seed(500)
    X, y = mock.get_mock_data()
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


def test_predict_sklearn_dict_ptype(vetiver_client):
    data = {"B": 0, "C": 0, "D": 0}

    response = predict(endpoint=vetiver_client, data=data)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 1


def test_predict_sklearn_no_ptype(vetiver_client_check_ptype_false):
    X, y = mock.get_mock_data()
    response = predict(endpoint=vetiver_client_check_ptype_false, data=X)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 100


def test_predict_sklearn_df_check_ptype(vetiver_client):
    X, y = mock.get_mock_data()
    response = predict(endpoint=vetiver_client, data=X)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 100


def test_predict_sklearn_series_check_ptype(vetiver_client):
    ser = pd.Series(data=[0, 0, 0])
    response = predict(endpoint=vetiver_client, data=ser)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 1


@pytest.mark.parametrize("data", [(0), 0, 0.0, "0"])
def test_predict_sklearn_type_error(data, vetiver_client):
    import re

    msg = re.sub(
        r"\n",
        ": ",
        "1 validation error for Request\nbody\n  value is not a valid list \(type=type_error.list\)",  # noqa
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
