import pytest

from vetiver import mock, VetiverModel, VetiverAPI
from fastapi.testclient import TestClient


def _start_application():
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        save_ptype=True,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    def sum_values(x):
        return x.sum()

    app = VetiverAPI(v)

    app.vetiver_post(sum_values, "sum")

    return app


def test_endpoint_adds():
    app = _start_application().app

    client = TestClient(app)
    data = {"B": 0, "C": 0, "D": 0}
    response = client.post("/sum/", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"sum": 0}, response.json()
