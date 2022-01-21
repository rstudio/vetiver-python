import pandas as pd
import numpy as np
from vetiver.ptype import vetiver_create_ptype

class NoAvailableDescriptionError(Exception):
    """
    Throw an error if we don't find a method 
    available to create a description for `model`
    """

    def __init__(
        self,
        message="There is no method available to create a description for `model`",
    ):
        self.message = message
        super().__init__(self.message)

class NoModelAvailableError(Exception):
    """
    Throw an error if we don't find a method 
    available to prepare a `model`
    """

    def __init__(
        self,
        message="There is no model available",
    ):
        self.message = message
        super().__init__(self.message)


class VetiverModel():
    """
    explanation

    Parameters
    ----------
    model :  
    model_name : 
    description :  
    metadata : 
    save_ptype :
    versioned :

    Examples
    --------
    
    """

    def __init__(self, model, name = None, 
        description = None, metadata = list(), 
        save_ptype = True, versioned = None,
        test_data = None, **kw):

       
        self.model = model,
        self.name = name,
        self.description = _vetiver_create_description(model, name, description),
        self.metadata = metadata,
        self.ptype = vetiver_create_ptype(test_data, save_ptype),
        self.versioned = versioned

        if(description == None):
            description = _vetiver_create_description(model, name, description)

        # metadata = vetiver_create_meta(model, metadata)

# create description
def _vetiver_create_description(model, name, description):
    if (description == None):
        description = f'{name} is a {type(model)} vetiver model.'
    return description


# def _vetiver_prepare_model(model):
#     try:
#         model
#     except:
#         raise NoModelAvailableError