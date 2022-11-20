import pytest

import numpy as np
import pandas as pd
from requests.exceptions import HTTPError
from fastapi.testclient import TestClient

from vetiver import mock, VetiverModel, VetiverAPI
from vetiver.server import predict


def test_predict_sklearn_dict_ptype():
    np.random.seed(500)
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )
    app = VetiverAPI(v, check_ptype=True)
    app.app.root_path = '/predict'
    client = TestClient(app.app)
    data = {"B": 0, "C": 0, "D": 0}

    response = predict(endpoint=client, data=data)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 1


def test_predict_sklearn_no_ptype():
    np.random.seed(500)
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )
    app = VetiverAPI(v, check_ptype=False)
    app.app.root_path = '/predict'
    client = TestClient(app.app)

    response = predict(endpoint=client, data=X)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 100


def test_predict_sklearn_df_check_ptype():
    np.random.seed(500)
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )
    app = VetiverAPI(v, check_ptype=True)
    app.app.root_path = '/predict'
    client = TestClient(app.app)

    response = predict(endpoint=client, data=X)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 100


def test_predict_sklearn_series_check_ptype():
    np.random.seed(500)
    X, y = mock.get_mock_data()
    ser = pd.Series(data=[0, 0, 0])
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )
    app = VetiverAPI(v, check_ptype=True)
    app.app.root_path = '/predict'
    client = TestClient(app.app)

    response = predict(endpoint=client, data=ser)

    assert isinstance(response, pd.DataFrame), response
    assert response.iloc[0, 0] == 44.47
    assert len(response) == 1

@pytest.mark.parametrize(
    'data', [(0,0), 0, 0., '0'])
def test_predict_sklearn_type_error(data):
    np.random.seed(500)
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )
    app = VetiverAPI(v, check_ptype=True)
    app.app.root_path = '/predict'
    client = TestClient(app.app)
    msg = f"Predict expects a DataFrame or dict. Given type is {type(data)}"

    with pytest.raises(TypeError, match=msg):
        predict(endpoint=client, data=data)

def test_predict_server_error():
    np.random.seed(500)
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )
    app = VetiverAPI(v, check_ptype=True)
    app.app.root_path = '/i_do_not_exists'
    client = TestClient(app.app)

    with pytest.raises(HTTPError):
        res = predict(endpoint=client, data=X)
