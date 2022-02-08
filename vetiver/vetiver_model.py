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


class VetiverModel:
    """
    Create VetiverModel class for serving.

    vetiver will recognize instances of this class as properly
    formatted for serving.

    Parameters
    ----------
    model :  a trained model, such as an sklearn or spacy model
    name : model name or ID
    save_ptype :  should an input data prototype be saved with the model? 'TRUE' or 'FALSE'
    ptype_data: sample of data model should expect when it is being served
    versioned : should the model be served when created?
    description : a detailed description of the model. if omitted, a brief description will be generated
    metadata : other details to be saved and accessed for serving

    Methods
    -------

    Examples
    --------

    """

    def __init__(
        self,
        model,
        model_name=None,
        save_ptype=True,
        ptype_data=None,
        versioned=None,
        description=None,
        metadata=list(),
    ):

        self.model = (model,)
        self.name = (model_name,)
        self.description = (
            _vetiver_create_description(model, model_name, description),
        )
        self.metadata = (metadata,)
        self.ptype = (vetiver_create_ptype(ptype_data, save_ptype),)
        self.versioned = versioned

        if description == None:
            description = _vetiver_create_description(model, model_name, description)


# create description
def _vetiver_create_description(model, name, description):
    if description == None:
        description = f"{name} is a {type(model)} vetiver model."
    return description


# def _vetiver_prepare_model(model):
#     try:
#         model
#     except:
#         raise NoModelAvailableError
