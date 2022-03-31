import pandas as pd
import numpy as np
from pydantic import BaseModel, create_model
from uvicorn import Config


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
    Throw an error if `save_ptype` is not
    True, False, or data.frame
    """

    def __init__(
        self,
        message="The `ptype_data` argument must be a pandas.DataFrame, a pydantic BaseModel,  np.ndarray, or `save_ptype` must be FALSE.",
    ):
        self.message = message
        super().__init__(self.message)


def _vetiver_create_ptype(ptype_data, save_ptype: bool):
    """Create zero row structure to save data types
    Parameters
    ----------
    ptype_data :
        Custom function to be run at endpoint
    save_ptype : bool
        Whether or not ptype should be created

    Returns
    -------
    ptype
        Data prototype

    """
    ptype = None

    if save_ptype == False:
        pass
    elif save_ptype == True:
        try:
            if isinstance(ptype_data, np.ndarray):
                ptype = _array_to_ptype(ptype_data[1])
            elif isinstance(ptype_data.construct(), BaseModel):
                ptype = ptype_data
        except AttributeError:  # cannot construct basemodel
            if isinstance(ptype_data, pd.DataFrame):
                ptype = _df_to_ptype(ptype_data.iloc[1, :])
    else:
        raise InvalidPTypeError

    return ptype


def _df_to_ptype(train_data):

    dict_data = train_data.to_dict()
    ptype = create_model("ptype", **dict_data)

    return ptype


def _array_to_ptype(train_data):
    dict_data = dict(enumerate(train_data, 0))

    # pydantic requires strings as indicies
    dict_data = {str(key): value.item() for key, value in dict_data.items()}
    ptype = create_model("ptype", **dict_data)

    return ptype
