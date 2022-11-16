from vetiver import mock, VetiverModel, VetiverAPI
import pandas as pd
from fastapi.testclient import TestClient


def _start_application(check_ptype):
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        ptype_data=X,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    def sum_values(x):
        return x.sum()

    app = VetiverAPI(v, check_ptype=check_ptype)

    app.vetiver_post(sum_values, "sum")

    return app


def test_endpoint_adds_ptype():
    app = _start_application(check_ptype=True).app

    client = TestClient(app)
    data = {"B": [0], "C": [0], "D": [0]}
    response = client.post("/sum", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"sum": [0]}, response.json()


def test_endpoint_adds_no_ptype():
    app = _start_application(check_ptype=False).app

    client = TestClient(app)
    data = [0, 0, 0]
    response = client.post("/sum", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"sum": [0]}, response.json()
