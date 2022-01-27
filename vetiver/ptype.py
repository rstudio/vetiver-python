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
        message="The `save_ptype` argument must be TRUE, FALSE, or a dataframe.",
    ):
        self.message = message
        super().__init__(self.message)


def vetiver_create_ptype(sample, save_ptype):

    if (save_ptype == True):
        if(sample == None):
            raise ValueError
        elif(isinstance(sample, pd.DataFrame)):
            ptype = _vetiver_ptype(sample)
        elif(isinstance(sample, BaseModel)):
            ptype = sample
        else:
            raise InvalidPTypeError
    elif(save_ptype == False):
        ptype = None
    else:
        raise InvalidPTypeError

    return ptype


def _vetiver_ptype(test_data):
    
    try:
        test_data = test_data.iloc[1,:]
    except TypeError:
        raise NoAvailablePTypeError

    dict_data = test_data.to_dict()
    ptype = create_model("ptype", **dict_data)

    return ptype
