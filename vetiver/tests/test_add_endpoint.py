import pytest

import numpy as np
import pandas as pd
from fastapi.testclient import TestClient

from vetiver import mock, VetiverModel, VetiverAPI
from vetiver.helpers import api_data_to_frame
import vetiver


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


def sum_values(x):
    return x.sum().to_list()


def sum_values_no_prototype(x):
    return api_data_to_frame(x).sum().to_list()


@pytest.fixture
def vetiver_client(vetiver_model):  # With check_prototype=True

    app = VetiverAPI(vetiver_model, check_prototype=True)
    app.vetiver_post(sum_values, "sum")

    app.app.root_path = "/sum"
    client = TestClient(app.app)

    return client


@pytest.fixture
def vetiver_client_check_ptype_false(vetiver_model):  # With check_prototype=False

    app = VetiverAPI(vetiver_model, check_prototype=False)
    app.vetiver_post(sum_values_no_prototype, "sum")

    app.app.root_path = "/sum"
    client = TestClient(app.app)

    return client


def test_endpoint_adds_ptype(vetiver_client):

    data = pd.DataFrame({"B": [1, 1, 1], "C": [2, 2, 2], "D": [3, 3, 3]})
    response = vetiver.predict(endpoint=vetiver_client, data=data)

    assert isinstance(response, pd.DataFrame)
    assert response.to_json() == '{"sum":{"0":3,"1":6,"2":9}}', response.to_json()


def test_endpoint_adds_no_ptype(vetiver_client_check_ptype_false):

    data = pd.DataFrame({"B": [1, 1, 1], "C": [2, 2, 2], "D": [3, 3, 3]})
    response = vetiver.predict(endpoint=vetiver_client_check_ptype_false, data=data)

    assert isinstance(response, pd.DataFrame)
    assert response.to_json() == '{"sum":{"0":3,"1":6,"2":9}}', response.to_json()
