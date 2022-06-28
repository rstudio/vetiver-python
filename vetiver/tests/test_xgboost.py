import xgboost as xgb
import pytest

from vetiver.data import mtcars
from vetiver.handlers.xgboost import XGBoostHandler


@pytest.fixture
def fit():
    # read in data
    dtrain = xgb.DMatrix(mtcars.drop(columns="mpg"), label=mtcars["mpg"])
    dtest = xgb.DMatrix(mtcars.drop(columns="mpg"))
    # specify parameters via map
    param = {"max_depth": 2, "eta": 1, "objective": "reg:squarederror"}
    num_round = 2
    fit = xgb.train(param, dtrain, num_round)

    return fit


@pytest.fixture
def handler(fit):
    return XGBoostHandler(fit, None)


def test_handler_xgboost_predict_dmatrix(handler):
    dtest = xgb.DMatrix(mtcars.drop(columns="mpg"))
    handler.handler_predict(dtest, True)


def test_handler_xgboost_predict_df(handler):
    dtest = mtcars.drop(columns="mpg")
    handler.handler_predict(dtest, True)


@pytest.mark.xfail
def test_handler_xgboost_predict_str(handler):
    # TODO: prediction from a string")
    dtest = mtcars.drop(columns="mpg")
    handler.handler_predict(dtest, False)


@pytest.mark.xfail
def test_handler_xgboost_predict_list(handler):
    # TODO: prediction from a serialized JSON list
    row = mtcars.drop(columns="mpg").iloc[0, :].tolist()
    handler.handler_predict([row], False)
