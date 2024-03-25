import pytest
from vetiver import VetiverModel, VetiverAPI
from vetiver.helpers import api_data_to_frame
from starlette.testclient import TestClient


def sum_values(x):
    return x.sum().to_list()


def sum_values_no_prototype(x):
    return api_data_to_frame(x).sum().to_list()


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
