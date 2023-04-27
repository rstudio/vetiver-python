from vetiver import mock, VetiverModel, VetiverAPI
from fastapi.testclient import TestClient
import pytest
import sys


@pytest.fixture
def vetiver_model():
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
def client(vetiver_model):
    app = VetiverAPI(vetiver_model)

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

def test_get_prototype(client):
    response = client.get("/prototype")
    assert response.status_code == 200, response.text
    assert response.json() == {
    "title": "my_model prototype",
    "$ref": "#/definitions/prototype",
    "definitions": {
        "prototype": {
        "title": "prototype",
        "type": "object",
        "properties": {
            "B": {
            "title": "B",
            "default": 6,
            "type": "integer"
            },
            "C": {
            "title": "C",
            "default": 10,
            "type": "integer"
            },
            "D": {
            "title": "D",
            "default": 8,
            "type": "integer"
            }
        }
        }
    }
    }