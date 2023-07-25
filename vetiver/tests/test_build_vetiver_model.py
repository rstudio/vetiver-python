import sklearn
import sys

import vetiver as vt
from vetiver.meta import VetiverMeta
from vetiver.mock import get_mock_data, get_mock_model

import pandas as pd
import pydantic
import pins
import numpy as np

np.random.seed(50)

# Load data, model
X_df, y = get_mock_data()
X_array = pd.DataFrame(X_df).to_numpy()
model = get_mock_model().fit(X_df, y)


class MockPrototype(pydantic.BaseModel):
    B: int
    C: int
    D: int


def test_vetiver_model_array_prototype():
    vt1 = vt.VetiverModel(
        model=model,
        prototype_data=X_array,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt1.model == model
    assert issubclass(vt1.prototype, vt.Prototype)
    # change to model_construct for pydantic v3
    assert isinstance(vt1.prototype.construct(), pydantic.BaseModel)
    assert vt1.prototype.construct().__dict__ == {"0": 96, "1": 11, "2": 33}


def test_vetiver_model_df_prototype():
    vt2 = vt.VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt2.model == model
    # change to model_construct for pydantic v3
    assert isinstance(vt2.prototype.construct(), pydantic.BaseModel)
    assert vt2.prototype.construct().B == 96


def test_vetiver_model_dict_prototype():
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
    # change to model_construct for pydantic v3
    assert isinstance(vt3.prototype.construct(), pydantic.BaseModel)
    assert vt3.prototype.construct().B == 0


def test_vetiver_model_basemodel_prototype():

    m = MockPrototype(B=4, C=0, D=0)
    vt4 = vt.VetiverModel(
        model=model,
        prototype_data=m,
        model_name="model",
        versioned=False,
        description=None,
    )

    assert vt4.model == model
    assert vt4.prototype is m


def test_vetiver_model_no_prototype():
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


def test_vetiver_model_use_ptype():
    vt5 = vt.VetiverModel(
        model=model,
        prototype_data=None,
        model_name="model",
        versioned=None,
        description=None,
        metadata={"test": 123},
    )

    assert vt5.model == model
    assert vt5.prototype is None
    assert vt5.metadata == VetiverMeta(
        user={"test": 123},
        version=None,
        url=None,
        required_pkgs=["scikit-learn"],
        python_version=tuple(sys.version_info),
    )


def test_vetiver_model_from_pin():

    v = vt.VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        versioned=None,
        description=None,
        metadata={"test": 123},
    )

    board = pins.board_temp(allow_pickle_read=True)
    vt.vetiver_pin_write(board=board, model=v)
    v2 = vt.VetiverModel.from_pin(board, "model")

    assert isinstance(v2, vt.VetiverModel)
    assert isinstance(v2.model, sklearn.base.BaseEstimator)
    # change to model_construct for pydantic v3
    assert isinstance(v2.prototype.construct(), pydantic.BaseModel)
    assert v2.metadata.user == {"test": 123}
    assert v2.metadata.version is not None
    assert v2.metadata.required_pkgs == ["scikit-learn"]
    assert v2.metadata.python_version == tuple(sys.version_info)

    board.pin_delete("model")


def test_vetiver_model_from_pin_user_metadata():
    """
    Test if standard keys as part of :dataclass:`VetiverMeta` are picked
    """
    custom_meta = {
        "test": 123,
        "required_pkgs": ["foo", "bar"],
        "python_version": [3, 10, 6, "final", 0],
    }
    loaded_pkgs = custom_meta["required_pkgs"] + ["scikit-learn"]

    v = vt.VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        versioned=None,
        description=None,
        metadata=custom_meta,
    )

    board = pins.board_temp(allow_pickle_read=True)
    vt.vetiver_pin_write(board=board, model=v)
    v2 = vt.VetiverModel.from_pin(board, "model")

    assert isinstance(v2, vt.VetiverModel)
    assert isinstance(v2.model, sklearn.base.BaseEstimator)
    # change to model_construct for pydantic v3
    assert isinstance(v2.prototype.construct(), pydantic.BaseModel)
    assert v2.metadata.user == custom_meta
    assert v2.metadata.version is not None
    assert v2.metadata.required_pkgs == loaded_pkgs
    assert v2.metadata.python_version == tuple(custom_meta["python_version"])

    board.pin_delete("model")


def test_vetiver_model_from_pin_no_version():
    """
    Test if standard keys as part of :dataclass:`VetiverMeta` are picked
    """
    custom_meta = {
        "required_pkgs": None,
        "python_version": None,
    }

    v = vt.VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        metadata=custom_meta,
    )

    board = pins.board_temp(allow_pickle_read=True)
    vt.vetiver_pin_write(board=board, model=v)
    v2 = vt.VetiverModel.from_pin(board, "model")

    assert v2.metadata.required_pkgs == ["scikit-learn"]
    assert v2.metadata.python_version is None

    board.pin_delete("model")
