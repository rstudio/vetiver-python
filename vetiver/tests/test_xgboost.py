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
    param = {'max_depth':2, 'eta':1, 'objective':'reg:squarederror' }
    num_round = 2
    fit = xgb.train(param, dtrain, num_round)

    return fit


@pytest.fixture
def handler(fit):
    return XGBoostHandler(fit, None)


def test_handler_xgboost_predict(handler):
    dtest = xgb.DMatrix(mtcars.drop(columns="mpg"))
    handler.handler_predict(dtest, True)

