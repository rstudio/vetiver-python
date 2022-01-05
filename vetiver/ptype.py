import pandas as pd

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

def _vetiver_ptype(model, **kwargs):

    try:
        ptype = type(model)
    except:
       raise NoAvailablePTypeError
    
    return ptype

def vetiver_create_ptype(df, save_ptype, **kwargs):

    if (save_ptype == True):
        ptype = _vetiver_ptype(df)
    elif(save_ptype == False):
        ptype = None
    elif(isinstance(save_ptype, pd.DataFrame)):
        ptype = save_ptype.dtypes
    else:
        raise InvalidPTypeError

    return ptype


def create_ptype(test_data):

    if test_data != pd.DataFrame():
        test_data = pd.DataFrame(test_data)

    assert len(test_data.columns)==len(test_data.dtypes)

    ptype = pd.DataFrame(columns=test_data.columns).astype(dtype = test_data.dtypes)
    
    return ptype