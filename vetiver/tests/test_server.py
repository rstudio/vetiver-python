from vetiver import (
    mock,
    VetiverModel,
    VetiverAPI,
    vetiver_create_prototype,
    InvalidPTypeError,
    vetiver_endpoint,
    predict,
)
from pydantic import BaseModel, conint
from fastapi.testclient import TestClient
import numpy as np
import pytest
import sys
import pandas as pd
from vetiver.handlers.sklearn import SKLearnHandler


@pytest.fixture
def model():
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
def complex_prototype_client():
    np.random.seed(500)

    class CustomPrototype(BaseModel):
        B: conint(gt=42)
        C: conint(gt=42)
        D: conint(gt=42)

    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        # move to model_construct for pydantic 3
        prototype_data=CustomPrototype.construct(),
        model_name="my_model",
        versioned=None,
        description="A regression model for testing purposes",
    )
    # dont actually want to make predictions, just for looking at schema
    app = VetiverAPI(v, check_prototype=False)

    return TestClient(app.app)


def test_get_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200, response.text
    assert response.json() == {"ping": "pong"}


def test_get_docs(client):
    response = client.get("/__docs__")
    assert response.status_code == 200, response.text


def test_get_metadata(client):
    response = client.get("/metadata")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "user": {},
        "version": None,
        "url": None,
        "required_pkgs": ["scikit-learn"],
        "python_version": list(sys.version_info),  # JSON will return a list
    }


def test_get_prototype(client, model):
    response = client.get("/prototype")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "properties": {
            "B": {"example": 55, "type": "integer"},
            "C": {"example": 65, "type": "integer"},
            "D": {"example": 17, "type": "integer"},
        },
        "required": ["B", "C", "D"],
        "title": "prototype",
        "type": "object",
    }

    assert (
        model.prototype.construct().dict()
        == vetiver_create_prototype(response.json()).construct().dict()
    )


def test_complex_prototype(complex_prototype_client):
    response = complex_prototype_client.get("/prototype")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "properties": {
            "B": {"exclusiveMinimum": 42, "type": "integer"},
            "C": {"exclusiveMinimum": 42, "type": "integer"},
            "D": {"exclusiveMinimum": 42, "type": "integer"},
        },
        "required": ["B", "C", "D"],
        "title": "CustomPrototype",
        "type": "object",
    }

    with pytest.raises(InvalidPTypeError):
        vetiver_create_prototype(response.json())


def test_predict_wrong_input(client):
    with pytest.raises(TypeError):
        predict(endpoint="/predict/", data=[{"B": 43, "C": 43}], test_client=client)


def test_vetiver_endpoint():
    url_raw = "http://127.0.0.1:8000/predict/"
    url = vetiver_endpoint(url_raw)

    assert url == "http://127.0.0.1:8000/predict"


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


def test_vetiver_post_sklearn_predict(model):
    vetiver_api = VetiverAPI(model=model)
    if not isinstance(vetiver_api.model, SKLearnHandler):
        pytest.skip("Test only applicable for SKLearnHandler models")

    vetiver_api.vetiver_post("predict_proba")

    client = TestClient(vetiver_api.app)
    response = client.post(
        "/predict_proba", json=vetiver_api.model.prototype.construct().dict()
    )
    assert response.status_code == 200


def test_vetiver_post_invalid_sklearn_type(model):
    vetiver_api = VetiverAPI(model=model)
    if not isinstance(vetiver_api.model, SKLearnHandler):
        pytest.skip("Test only applicable for SKLearnHandler models")

    with pytest.raises(
        ValueError,
        match="The 'endpoint_fx' parameter can only be a string \
            when using scikit-learn models.",
    ):
        vetiver_api.vetiver_post("invalid_type")
