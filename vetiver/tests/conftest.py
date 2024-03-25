import pytest
import numpy as np
from vetiver import VetiverModel, VetiverAPI, mock
from vetiver.helpers import api_data_to_frame
from starlette.testclient import TestClient


def sum_values(x):
    return x.sum().to_list()


def sum_values_no_prototype(x):
    return api_data_to_frame(x).sum().to_list()


def model() -> VetiverModel:
    np.random.seed(500)
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    return VetiverModel(
        model=model,
        prototype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )


@pytest.fixture
def client(model: VetiverModel) -> TestClient:
    app = VetiverAPI(model, check_prototype=True)
    app.vetiver_post(sum_values, "sum")
    client = TestClient(app.app)

    return client


@pytest.fixture
def client_no_prototype(model: VetiverModel) -> TestClient:
    app = VetiverAPI(model, check_prototype=False)
    app.vetiver_post(sum_values_no_prototype, "sum")
    client = TestClient(app.app)

    return client
