import pandas as pd
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
    Throw an error if `save_ptype` is not
    True, False, or data.frame
    """

    def __init__(
        self,
        message="The `save_ptype` argument must be a dataframe, a BaseModel, or FALSE.",
    ):
        self.message = message
        super().__init__(self.message)


def vetiver_create_ptype(ptype_data, save_ptype):
    
    if(save_ptype == False):
        ptype = None
    elif(save_ptype == True):
        try:
            if isinstance(ptype_data.construct(), BaseModel):
                ptype = ptype_data
        except AttributeError:
            if isinstance(ptype_data, pd.DataFrame):
                ptype = _vetiver_ptype(ptype_data.iloc[1,:])
    else:
        raise InvalidPTypeError

    return ptype


def _vetiver_ptype(train_data):

    dict_data = train_data.to_dict()
    ptype = create_model("ptype", **dict_data)

    return ptype
