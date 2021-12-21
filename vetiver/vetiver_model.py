import pandas as pd
import numpy as np
from .ptype import vetiver_create_ptype

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
    save_ptye :
    versioned :

    Examples
    --------
    
    """

    def __init__(self, model, name, 
        description = None, metadata = list(), 
        save_ptype = True, versioned = None, 
        **kwargs):

       
        self.model = _vetiver_prepare_model(model),
        self.name = name,
        self.description = _vetiver_create_description(model, name, description),
        self.metadata = metadata,
        self.ptype = vetiver_create_ptype(model, save_ptype),
        self.versioned = versioned

        if(description == None):
            description = _vetiver_create_description(model)

        # metadata = vetiver_create_meta(model, metadata)

# create description
def _vetiver_create_description(model, name, description):
    if (description == None):
        try:
            description = f'{name} is a {type(model)} vetiver model.'
        except Exception:
            raise NoAvailableDescriptionError
    return description


def _vetiver_prepare_model(model):
    try:
        model
    except:
        raise NoModelAvailableError