import pytest
import pins
from vetiver import vetiver_pin_read, vetiver_pin_write, VetiverModel, VetiverAPI, mock
from fastapi.testclient import TestClient
import numpy as np

def _make_model(save_ptype: bool):
    np.random.seed(500)
    X, y = mock.get_mock_data()
    model = mock.get_mock_model().fit(X, y)
    v = VetiverModel(
        model=model,
        save_ptype=save_ptype,
        ptype_data=X,
        model_name="model",
        versioned=None,
        description="A regression model for testing purposes",
    )

    return v

def test_board_pin_rountrip_ptype_sklearn():
    np.random.seed(500)
    v = _make_model(save_ptype=True)
    board = pins.board_temp(allow_pickle_read=True)
    vetiver_pin_write(board=board, model=v)
    v = vetiver_pin_read(board, "model")
    assert isinstance(v, VetiverModel)

    api = VetiverAPI(v, check_ptype=True)
    client = TestClient(api.app)
    data = {"B": 0, "C": 0, "D": 0}
    response = client.post("/predict/", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"prediction": [44.47]}, response.json()


def test_board_pin_rountrip_no_ptype_sklearn():
    np.random.seed(500)
    v = _make_model(save_ptype=False)
    board = pins.board_temp(allow_pickle_read=True)
    vetiver_pin_write(board=board, model=v)
    v = vetiver_pin_read(board, "model")
    assert isinstance(v, VetiverModel)

    api = VetiverAPI(v, check_ptype=False)
    client = TestClient(api.app)
    data = [[0,0,0]]
    response = client.post("/predict/", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"prediction": [44.47]}, response.json()