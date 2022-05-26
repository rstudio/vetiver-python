from functools import singledispatch
from types import NoneType

import pandas as pd
import numpy as np
from pydantic import BaseModel, create_model


class NoAvailablePTypeError(Exception):
    """
    Throw an error if we cannot create
    a 0 row input data prototype for `model`
    """

    def __init__(
        self,
        message="There is no method available to create a 0-row input data prototype for `model`",
    ):
        self.message = message
        super().__init__(self.message)


class InvalidPTypeError(Exception):
    """
    Throw an error if ptype cannot be recognised
    """

    def __init__(
        self,
        message="`ptype_data` must be a pd.DataFrame, a pydantic BaseModel or np.ndarray",
    ):
        self.message = message
        super().__init__(self.message)


CREATE_PTYPE_TPL =  """\
Failed to create a data prototype (ptype) from data of \
type {_data_type}. If your datatype is not one of \
(pd.DataFrame, pydantic.BaseModel, np.ndarry, dict), \
you should write a function to create the ptype. Here is \
a template for such a function: \

    from pydantic import create_model
    from vetiver.ptype import vetiver_create_ptype

    @vetiver_create_ptype.register
    def _(data: {_data_type}):
        data_dict = ... # convert data to a dictionary
        ptype = create_model("ptype", **data_dict)
        return ptype

If your datatype is a common type, please consider submitting \
a pull request.
"""

@singledispatch
def vetiver_create_ptype(data):
    """Create zero row structure to save data types

    Parameters
    ----------
    data :
        Data that represents what

    Returns
    -------
    ptype
        Data prototype

    """
    raise InvalidPTypeError(
        message=CREATE_PTYPE_TPL.format(_data_type=type(data))
    )


@vetiver_create_ptype.register
def _vetiver_create_ptype(data: pd.DataFrame):
    dict_data = data.iloc[1, :].to_dict()
    ptype = create_model("ptype", **dict_data)
    return ptype


@vetiver_create_ptype.register
def _vetiver_create_ptype(data: np.ndarray):
    dict_data = dict(enumerate(data[1], 0))
    # pydantic requires strings as indicies
    dict_data = {f"{key}": value.item() for key, value in dict_data.items()}
    ptype = create_model("ptype", **dict_data)
    return ptype


@vetiver_create_ptype.register
def _vetiver_create_ptype(data: dict):
    return create_model("ptype", **data)


@vetiver_create_ptype.register
def _vetiver_create_ptype(data: BaseModel):
    return data


@vetiver_create_ptype.register
def _vetiver_create_ptype(data: NoneType):
    return None
