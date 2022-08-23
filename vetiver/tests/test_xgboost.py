import pytest

xgb = pytest.importorskip("xgboost", reason="xgboost library not installed")

from vetiver.data import mtcars  # noqa
from vetiver.handlers.xgboost import XGBoostHandler  # noqa
import numpy as np  # noqa
from fastapi.testclient import TestClient  # noqa

import vetiver  # noqa


@pytest.fixture
def build_xgb():
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


def test_vetiver_build(build_xgb):
    api = vetiver.VetiverAPI(build_xgb)
    client = TestClient(api.app)
    data = mtcars.head(1).drop(columns="mpg")

    response = vetiver.predict(endpoint=client, data=data)

    assert response.iloc[0, 0] == 21.064373016357422
    assert len(response) == 1


def test_batch(build_xgb):
    api = vetiver.VetiverAPI(build_xgb)
    client = TestClient(api.app)
    data = mtcars.head(3).drop(columns="mpg")

    response = vetiver.predict(endpoint=client, data=data)

    assert response.iloc[0, 0] == 21.064373016357422
    assert len(response) == 3


def test_no_ptype(build_xgb):
    api = vetiver.VetiverAPI(build_xgb, check_ptype=False)
    client = TestClient(api.app)
    data = mtcars.head(1).drop(columns="mpg")

    response = vetiver.predict(endpoint=client, data=data)

    assert response.iloc[0, 0] == 21.064373016357422
    assert len(response) == 1


def test_serialize(build_xgb):
    import pins

    board = pins.board_temp(allow_pickle_read=True)
    vetiver.vetiver_pin_write(board=board, model=build_xgb)
    assert isinstance(
        board.pin_read("xgb"),
        xgb.Booster,
    )
    board.pin_delete("xgb")
