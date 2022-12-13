import sklearn

import vetiver as vt
from vetiver.mock import get_mock_data, get_mock_model

import pandas as pd
import pydantic
import pins

# Load data, model
X_df, y = get_mock_data()
X_array = pd.DataFrame(X_df).to_numpy()
model = get_mock_model().fit(X_df, y)


def test_vetiver_model_array_ptype():
    # build VetiverModel, no ptype
    vt1 = vt.VetiverModel(
        model=model,
        prototype_data=X_array,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt1.model == model
    assert isinstance(vt1.prototype.construct(), pydantic.BaseModel)
    assert list(vt1.prototype.__fields__.values())[0].type_ == int


def test_vetiver_model_df_ptype():
    # build VetiverModel, df ptype_data
    vt2 = vt.VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt2.model == model
    assert isinstance(vt2.prototype.construct(), pydantic.BaseModel)
    assert list(vt2.prototype.__fields__.values())[0].type_ == int


def test_vetiver_model_dict_ptype():
    dict_data = {"B": 0, "C": 0, "D": 0}
    vt3 = vt.VetiverModel(
        model=model,
        prototype_data=dict_data,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt3.model == model
    assert isinstance(vt3.prototype.construct(), pydantic.BaseModel)
    assert list(vt3.prototype.__fields__.values())[0].type_ == int


def test_vetiver_model_no_ptype():
    # build VetiverModel, no ptype
    vt4 = vt.VetiverModel(
        model=model,
        prototype_data=None,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt4.model == model
    assert vt4.prototype is None


def test_vetiver_model_from_pin():

    v = vt.VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )
    board = pins.board_temp(allow_pickle_read=True)
    vt.vetiver_pin_write(board=board, model=v)
    v2 = vt.VetiverModel.from_pin(board, "model")
    assert isinstance(v2, vt.VetiverModel)
    assert isinstance(v2.model, sklearn.base.BaseEstimator)
    assert isinstance(v2.prototype.construct(), pydantic.BaseModel)
    board.pin_delete("model")
