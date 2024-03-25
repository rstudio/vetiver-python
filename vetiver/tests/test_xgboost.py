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
def model():
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


def test_required_pkgs(model):
    assert model.metadata.required_pkgs == ["xgboost"]
    assert not model.metadata.user


def test_vetiver_build(client):
    data = mtcars.head(1).drop(columns="mpg")

    response = vetiver.predict(endpoint="/predict/", data=data, test_client=client)

    assert response.iloc[0, 0] == PREDICT_VALUE
    assert len(response) == 1


def test_batch(client):
    data = mtcars.head(3).drop(columns="mpg")

    response = vetiver.predict(endpoint="/predict/", data=data, test_client=client)

    assert response.iloc[0, 0] == PREDICT_VALUE
    assert len(response) == 3


def test_no_ptype(client_no_prototype):
    data = mtcars.head(1).drop(columns="mpg")

    response = vetiver.predict(
        endpoint="/predict/", data=data, test_client=client_no_prototype
    )
    assert response.iloc[0, 0] == PREDICT_VALUE
    assert len(response) == 1


def test_serialize(model):
    import pins

    board = pins.board_temp(allow_pickle_read=True)
    vetiver.vetiver_pin_write(board=board, model=model)
    assert isinstance(
        board.pin_read("xgb"),
        xgb.Booster,
    )
    board.pin_delete("xgb")
