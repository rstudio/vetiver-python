import pytest

xgb = pytest.importorskip("xgboost", reason="xgboost library not installed")

from vetiver.data import mtcars  # noqa
from vetiver.handlers.xgboost import XGBoostHandler  # noqa
import numpy as np  # noqa
import sys  # noqa
from fastapi.testclient import TestClient  # noqa

import vetiver  # noqa

PREDICT_VALUE = 19.963224411010742


@pytest.fixture
def xgb_model():
    # read in data
    dtrain = xgb.DMatrix(mtcars.drop(columns="mpg"), label=mtcars["mpg"])
    # specify parameters via map
    param = {
        "max_depth": 2,
        "eta": 1,
        "objective": "reg:squarederror",
        "random_state": 0,
    }
    num_round = 2
    fit = xgb.train(param, dtrain, num_round)

    return vetiver.VetiverModel(fit, "xgb", mtcars.drop(columns="mpg"))


@pytest.fixture
def vetiver_client(xgb_model):  # With check_prototype=True
    app = vetiver.VetiverAPI(xgb_model, check_prototype=True)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


@pytest.fixture
def vetiver_client_check_ptype_false(xgb_model):  # With check_prototype=True
    app = vetiver.VetiverAPI(xgb_model, check_prototype=False)
    app.app.root_path = "/predict"
    client = TestClient(app.app)

    return client


def test_model(xgb_model):
    v = xgb_model

    assert v.metadata.required_pkgs == ["xgboost"]
    assert not v.metadata.user


def test_vetiver_build(vetiver_client):
    data = mtcars.head(1).drop(columns="mpg")

    response = vetiver.predict(endpoint=vetiver_client, data=data)

    assert response.iloc[0, 0] == PREDICT_VALUE
    assert len(response) == 1


def test_batch(vetiver_client):
    data = mtcars.head(3).drop(columns="mpg")

    response = vetiver.predict(endpoint=vetiver_client, data=data)

    assert response.iloc[0, 0] == PREDICT_VALUE
    assert len(response) == 3


def test_no_ptype(vetiver_client_check_ptype_false):
    data = mtcars.head(1).drop(columns="mpg")

    response = vetiver.predict(endpoint=vetiver_client_check_ptype_false, data=data)

    assert response.iloc[0, 0] == PREDICT_VALUE
    assert len(response) == 1


def test_serialize(xgb_model):
    import pins

    board = pins.board_temp(allow_pickle_read=True)
    vetiver.vetiver_pin_write(board=board, model=xgb_model)
    assert isinstance(
        board.pin_read("xgb"),
        xgb.Booster,
    )
    board.pin_delete("xgb")
