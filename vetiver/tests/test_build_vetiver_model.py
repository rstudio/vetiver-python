import pytest

from vetiver.vetiver_model import VetiverModel
from vetiver.mock import get_mock_data, get_mock_model

import pandas as pd
from numpy import int64

# Load data, model
X_df, y = get_mock_data()
X_array = pd.DataFrame(X_df).to_numpy()
model = get_mock_model().fit(X_df, y)


def test_vetiver_model_array_ptype():
    # build VetiverModel, no ptype
    vt1 = VetiverModel(
        model=model,
        save_ptype=True,
        ptype_data=X_array,
        model_name="iris",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt1.model == model
    assert list(vt1.ptype.__fields__.values())[0].type_ == int


def test_vetiver_model_df_ptype():
    # build VetiverModel, df ptype_data
    vt2 = VetiverModel(
        model=model,
        save_ptype=True,
        ptype_data=X_df,
        model_name="iris",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt2.model == model
    assert list(vt2.ptype.__fields__.values())[0].type_ == int


def test_vetiver_model_no_ptype():
    # build VetiverModel, no ptype
    vt3 = VetiverModel(
        model=model,
        save_ptype=False,
        ptype_data=X_df,
        model_name="iris",
        versioned=None,
        description=None,
        metadata=None,
    )

    assert vt3.model == model
    assert vt3.ptype == None
