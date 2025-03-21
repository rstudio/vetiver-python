import pytest
import sys
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient
from pydantic import BaseModel, conint

from vetiver.data import mtcars
from vetiver import (
    mock,
    VetiverModel,
    VetiverAPI,
    vetiver_create_prototype,
    InvalidPTypeError,
    vetiver_endpoint,
    predict,
)


@pytest.fixture
def model():
    np.random.seed(500)
    model = mock.get_mtcars_model()
    v = VetiverModel(
        model=model,
        prototype_data=mtcars.drop(columns="cyl"),
        model_name="my_model",
        versioned=None,
        description="A logistic regression model for testing purposes",
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
            "mpg": {"example": 21.0, "type": "number"},
            "disp": {"example": 160.0, "type": "number"},
            "hp": {"example": 110.0, "type": "number"},
            "drat": {"example": 3.9, "type": "number"},
            "wt": {"example": 2.62, "type": "number"},
            "qsec": {"example": 16.46, "type": "number"},
            "vs": {"example": 0.0, "type": "number"},
            "am": {"example": 1.0, "type": "number"},
            "gear": {"example": 4.0, "type": "number"},
            "carb": {"example": 4.0, "type": "number"},
        },
        "required": [
            "mpg",
            "disp",
            "hp",
            "drat",
            "wt",
            "qsec",
            "vs",
            "am",
            "gear",
            "carb",
        ],
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
    return pd.DataFrame(
        {
            "mpg": [20, 20],
            "disp": [160, 160],
            "hp": [110, 110],
            "drat": [3.9, 3.9],
            "wt": [2.62, 2.62],
            "qsec": [16.00, 16.00],
            "vs": [0, 0],
            "am": [1, 1],
            "gear": [4, 4],
            "carb": [4, 4],
        }
    )


def test_endpoint_adds(client, data):

    response = client.post("/sum/", data=data.to_json(orient="records"))

    assert response.status_code == 200
    assert response.json() == {"sum": [40, 320, 220, 7.8, 5.24, 32.00, 0, 2, 8, 8]}


def test_endpoint_adds_no_prototype(client_no_prototype, data):

    data = pd.DataFrame({"B": [1, 1, 1], "C": [2, 2, 2], "D": [3, 3, 3]})
    response = client_no_prototype.post("/sum/", data=data.to_json(orient="records"))

    assert response.status_code == 200
    assert response.json() == {"sum": [3, 6, 9]}


def test_vetiver_post_sklearn_predict(model, data):
    api = VetiverAPI(model=model)
    api.vetiver_post("predict_proba")

    client = TestClient(api.app)
    response = predict(endpoint="/predict_proba/", data=data, test_client=client)

    assert isinstance(response, pd.DataFrame)
    assert len(response) == 2
    # Allow for slight differences in architecture or library versions
    expected = {
        "predict_proba": {
            0: [
                0.0063,
                0.9937,
                3.59e-12,
            ],
            1: [
                0.0063,
                0.9937,
                3.59e-12,
            ],
        },
    }

    response_dict = response.to_dict()
    for key, value in expected["predict_proba"].items():
        assert response_dict["predict_proba"][key] == pytest.approx(value, rel=1e-2)


def test_vetiver_post_invalid_sklearn_type(model):
    vetiver_api = VetiverAPI(model=model)

    with pytest.raises(
        ValueError,
        match="Prediction type invalid_type not available",
    ):
        vetiver_api.vetiver_post("invalid_type")
