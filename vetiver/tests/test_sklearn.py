from vetiver import mock, VetiverModel, VetiverAPI
from fastapi.testclient import TestClient
import numpy as np
import pytest


def _start_application(save_prototype: bool = True):
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        prototype_data=X if save_prototype else None,
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    app = VetiverAPI(v, check_prototype=save_prototype)

    return app


def test_build_sklearn():
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        ptype_data=X,
        model_name="my_model",
        description="A regression model for testing purposes",
    )

    assert v.metadata.required_pkgs == ["scikit-learn"]


def test_predict_endpoint_ptype():
    np.random.seed(500)
    client = TestClient(_start_application().app)
    data = {"B": 0, "C": 0, "D": 0}
    response = client.post("/predict", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"predict": [44.47]}, response.json()


def test_predict_endpoint_ptype_batch():
    np.random.seed(500)
    client = TestClient(_start_application().app)
    data = [{"B": 0, "C": 0, "D": 0}, {"B": 0, "C": 0, "D": 0}]
    response = client.post("/predict", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"predict": [44.47, 44.47]}, response.json()


def test_predict_endpoint_ptype_error():
    np.random.seed(500)
    client = TestClient(_start_application().app)
    data = {"B": 0, "C": "a", "D": 0}
    response = client.post("/predict", json=data)
    assert response.status_code == 422, response.text  # value is not a valid integer


def test_predict_endpoint_no_ptype():
    np.random.seed(500)
    client = TestClient(_start_application(save_prototype=False).app)
    data = [{"B": 0, "C": 0, "D": 0}]
    response = client.post("/predict", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"predict": [44.47]}, response.json()


def test_predict_endpoint_no_ptype_batch():
    np.random.seed(500)
    client = TestClient(_start_application(save_prototype=False).app)
    data = [[0, 0, 0], [0, 0, 0]]
    response = client.post("/predict", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"predict": [44.47, 44.47]}, response.json()


def test_predict_endpoint_no_ptype_error():
    np.random.seed(500)
    client = TestClient(_start_application(save_prototype=False).app)
    data = {"hell0", 9, 32.0}
    with pytest.raises(TypeError):
        client.post("/predict", json=data)
