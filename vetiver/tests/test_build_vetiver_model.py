import sklearn
import sys
import pytest

import vetiver
from vetiver import (
    VetiverModel,
    mock,
    InvalidModelError,
    VetiverMeta,
    get_mock_data,
    get_mock_model,
    vetiver_pin_write,
)

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
    v = VetiverModel(
        model=model,
        prototype_data=X_array,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert v.model == model
    assert issubclass(v.prototype, vetiver.Prototype)
    # change to model_construct for pydantic v3
    assert isinstance(v.prototype.construct(), pydantic.BaseModel)
    assert v.prototype.construct().__dict__ == {"0": 96, "1": 11, "2": 33}


def test_vetiver_model_df_prototype():
    v = VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert v.model == model
    # change to model_construct for pydantic v3
    assert isinstance(v.prototype.construct(), pydantic.BaseModel)
    assert v.prototype.construct().B == 96


def test_vetiver_model_dict_prototype():
    dict_data = {"B": 0, "C": 0, "D": 0}
    v = VetiverModel(
        model=model,
        prototype_data=dict_data,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert v.model == model
    # change to model_construct for pydantic v3
    assert isinstance(v.prototype.construct(), pydantic.BaseModel)
    assert v.prototype.construct().B == 0


def test_vetiver_model_basemodel_prototype():

    m = MockPrototype(B=4, C=0, D=0)
    v = VetiverModel(
        model=model,
        prototype_data=m,
        model_name="model",
        versioned=False,
        description=None,
    )

    assert v.model == model
    assert v.prototype is m


def test_vetiver_model_no_prototype():
    v = VetiverModel(
        model=model,
        prototype_data=None,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert v.model == model
    assert v.prototype is None


def test_vetiver_model_use_ptype():
    v = VetiverModel(
        model=model,
        prototype_data=None,
        model_name="model",
        versioned=None,
        description=None,
        metadata={"test": 123},
    )

    assert v.model == model
    assert v.prototype is None
    assert v.metadata == VetiverMeta(
        user={"test": 123},
        version=None,
        url=None,
        required_pkgs=["scikit-learn"],
        python_version=tuple(sys.version_info),
    )


def test_vetiver_model_from_pin():

    v = VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        versioned=None,
        description=None,
        metadata={"test": 123},
    )

    board = pins.board_temp(allow_pickle_read=True)
    vetiver_pin_write(board=board, model=v)
    v2 = VetiverModel.from_pin(board, "model")

    assert isinstance(v2, VetiverModel)
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

    v = VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        versioned=None,
        description=None,
        metadata=custom_meta,
    )

    board = pins.board_temp(allow_pickle_read=True)
    vetiver_pin_write(board=board, model=v)
    v2 = VetiverModel.from_pin(board, "model")

    assert isinstance(v2, VetiverModel)
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

    v = VetiverModel(
        model=model,
        prototype_data=X_df,
        model_name="model",
        metadata=custom_meta,
    )

    board = pins.board_temp(allow_pickle_read=True)
    vetiver_pin_write(board=board, model=v)
    v2 = VetiverModel.from_pin(board, "model")

    assert v2.metadata.required_pkgs == ["scikit-learn"]
    assert v2.metadata.python_version is None

    board.pin_delete("model")


def test_no_model_handler_found():
    X, y = mock.get_mock_data()

    with pytest.raises(InvalidModelError):
        VetiverModel(
            model=y,
            prototype_data=X,
            model_name="my_model",
            versioned=None,
            description="A regression model for testing purposes",
        )
