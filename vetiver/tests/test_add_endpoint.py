import pytest
import pandas as pd
from vetiver import mock, VetiverModel


@pytest.fixture()
def model():
    X, y = mock.get_mock_data()
    model = mock.get_mock_model()

    return VetiverModel(model.fit(X, y), "model", prototype_data=X)


@pytest.fixture
def data() -> pd.DataFrame:
    return pd.DataFrame({"B": [1, 1, 1], "C": [2, 2, 2], "D": [3, 3, 3]})


def test_endpoint_adds(client, data):
    response = client.post("/sum/", data=data.to_json(orient="records"))

    assert response.status_code == 200
    assert response.json() == {"sum": [3, 6, 9]}


def test_endpoint_adds_no_prototype(client_no_prototype, data):

    data = pd.DataFrame({"B": [1, 1, 1], "C": [2, 2, 2], "D": [3, 3, 3]})
    response = client_no_prototype.post("/sum/", data=data.to_json(orient="records"))

    assert response.status_code == 200
    assert response.json() == {"sum": [3, 6, 9]}
