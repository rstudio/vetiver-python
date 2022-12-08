from functools import singledispatch

try:
    from types import NoneType
except ImportError:
    # python < 3.10
    NoneType = type(None)

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
        message="There is no method to create a 0-row input data prototype for `model`",
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


CREATE_PTYPE_TPL = """\
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
    data : object
        An object with information (data) whose layout is to be determined.

    Returns
    -------
    ptype : pydantic.main.BaseModel
        Data prototype

    """
    raise InvalidPTypeError(message=CREATE_PTYPE_TPL.format(_data_type=type(data)))


@vetiver_create_ptype.register
def _(data: pd.DataFrame):
    """
    Create input data prototype for a pandas dataframe

    Parameters
    ----------
    data : DataFrame
        Pandas dataframe

    Examples
    --------
    >>> from pydantic import BaseModel
    >>> df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    >>> prototype = vetiver_create_ptype(df)
    >>> issubclass(prototype, BaseModel)
    True
    >>> prototype()
    ptype(x=1, y=4)

    The data prototype created for the dataframe is equivalent to:

    >>> class another_prototype(BaseModel):
    ...     class Config:
    ...         title = 'ptype'
    ...     x: int = 1
    ...     y: int = 4

    >>> another_prototype()
    another_prototype(x=1, y=4)
    >>> another_prototype() == prototype()
    True

    Changing the title using `class Config` ensures that the
    also json/schemas match.

    >>> another_prototype.schema() == prototype.schema()
    True
    """
    dict_data = data.iloc[0, :].to_dict()
    ptype = create_model("ptype", **dict_data)
    return ptype


@vetiver_create_ptype.register
def _(data: np.ndarray):
    """
    Create input data prototype for a numpy array

    Parameters
    ----------
    data : ndarray
        2-Dimensional numpy array

    Examples
    --------
    >>> arr = np.array([[1, 4], [2, 5], [3, 6]])
    >>> prototype = vetiver_create_ptype(arr)
    >>> prototype()
    ptype(0=1, 1=4)

    >>> arr2 = np.array([[1, 'a'], [2, 'b'], [3, 'c']], dtype=object)
    >>> prototype2 = vetiver_create_ptype(arr2)
    >>> prototype2()
    ptype(0=1, 1='a')
    """

    def _item(value):
        # pydantic needs python objects. .item() converts a numpy
        # scalar type to a python equivalent, and if the ndarray
        # is dtype=object, it may have python objects
        try:
            return value.item()
        except AttributeError:
            return value

    dict_data = dict(enumerate(data[0], 0))
    # pydantic requires strings as indicies
    dict_data = {f"{key}": _item(value) for key, value in dict_data.items()}
    ptype = create_model("ptype", **dict_data)
    return ptype


@vetiver_create_ptype.register
def _(data: dict):
    """
    Create input data prototype for a dict

    Parameters
    ----------
    data : dict
        Dictionary
    """
    return create_model("ptype", **data)


@vetiver_create_ptype.register
def _(data: BaseModel):
    """
    Create input data prototype for a pydantic BaseModel object

    Parameters
    ----------
    data : pydantic.BaseModel
        Pydantic BaseModel
    """
    return data


@vetiver_create_ptype.register
def _(data: NoneType):
    """
    Create input data prototype for None

    Parameters
    ----------
    data : None
        None
    """
    return None
