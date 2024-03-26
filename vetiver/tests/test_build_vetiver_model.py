import sklearn
import sys
import pytest

import vetiver
from vetiver import (
    VetiverModel,
    mock,
    InvalidModelError,
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


# --- test prototypes ---
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
    assert v.prototype.model_json_schema() == {
        "properties": {
            "0": {"example": 96, "title": "0", "type": "integer"},
            "1": {"example": 11, "title": "1", "type": "integer"},
            "2": {"example": 33, "title": "2", "type": "integer"},
        },
        "required": ["0", "1", "2"],
        "title": "prototype",
        "type": "object",
    }


@pytest.mark.parametrize("prototype_data", [{"B": 96, "C": 11, "D": 33}, X_df])
def test_vetiver_model_dict_like_prototype(prototype_data):
    v = VetiverModel(
        model=model,
        prototype_data=prototype_data,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert v.model == model
    # change to model_construct for pydantic v3
    assert isinstance(v.prototype.construct(), pydantic.BaseModel)
    assert v.prototype.model_json_schema() == {
        "properties": {
            "B": {"example": 96, "title": "B", "type": "integer"},
            "C": {"example": 11, "title": "C", "type": "integer"},
            "D": {"example": 33, "title": "D", "type": "integer"},
        },
        "required": ["B", "C", "D"],
        "title": "prototype",
        "type": "object",
    }


@pytest.mark.parametrize("prototype_data", [MockPrototype(B=4, C=0, D=0), None])
def test_vetiver_model_prototypes(prototype_data):
    v = VetiverModel(
        model=model,
        prototype_data=prototype_data,
        model_name="model",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert v.model == model
    assert v.prototype is prototype_data


# --- test from pins ---
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


# --- test handlers
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
