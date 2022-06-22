import pytest

from vetiver.vetiver_model import VetiverModel
from vetiver.mock import get_mock_data, get_mock_model
from vetiver.pin_read_write import pin_write

import pandas as pd
import pydantic
import pins

# Load data, model
X_df, y = get_mock_data()
X_array = pd.DataFrame(X_df).to_numpy()
model = get_mock_model().fit(X_df, y)


def test_vetiver_model_array_ptype():
    # build VetiverModel, no ptype
    vt1 = VetiverModel(
        model=model,
        ptype_data=X_array,
        model_name="iris",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt1.model == model
    assert isinstance(vt1.ptype.construct(), pydantic.BaseModel)
    assert list(vt1.ptype.__fields__.values())[0].type_ == int


def test_vetiver_model_df_ptype():
    # build VetiverModel, df ptype_data
    vt2 = VetiverModel(
        model=model,
        ptype_data=X_df,
        model_name="iris",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt2.model == model
    assert isinstance(vt2.ptype.construct(), pydantic.BaseModel)
    assert list(vt2.ptype.__fields__.values())[0].type_ == int


def test_vetiver_model_dict_ptype():
    dict_data = {"B": 0, "C": 0, "D": 0}
    vt3 = VetiverModel(
        model=model,
        ptype_data=dict_data,
        model_name="iris",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt3.model == model
    assert isinstance(vt3.ptype.construct(), pydantic.BaseModel)
    assert list(vt3.ptype.__fields__.values())[0].type_ == int


def test_vetiver_model_no_ptype():
    # build VetiverModel, no ptype
    vt4 = VetiverModel(
        model=model,
        ptype_data=None,
        model_name="iris",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt4.model == model
    assert vt4.ptype == None

def test_vetiver_model_from_pin():

    v = VetiverModel(
        model=model,
        ptype_data=None,
        model_name="iris",
        versioned=None,
        description=None,
        metadata=None,
    )
    board = pins.board_temp(allow_pickle_read=True)
    vetiver_pin_write(board=board, model=v)
    v = VetiverModel.from_pin(board, "model")
    assert isinstance(v, VetiverModel) 
    assert vt5.model == model
    assert isinstance(vt5.ptype.construct(), pydantic.BaseModel)
    board.pin_delete("model")