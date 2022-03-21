import pytest

from vetiver import mock, VetiverModel, VetiverAPI
from fastapi.testclient import TestClient
import numpy as np


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

    app = VetiverAPI(v)

    return app


def test_ping_app():
    client = TestClient(_start_application().app)
    response = client.get("/ping")
    assert response.status_code == 200, response.text
    assert response.json() == {"ping": "pong"}


def test_get_docs():
    client = TestClient(_start_application().app)
    response = client.get("/docs")
    assert response.status_code == 200, response.text


def test_predict_endpoint():
    np.random.seed(500)
    client = TestClient(_start_application().app)
    data = {"B": 0, "C": 0, "D": 0}
    response = client.post("/predict/", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"prediction": [44.47]}, response.json()
