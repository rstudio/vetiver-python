from vetiver.handlers._interface import create_handler


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
    """Create VetiverModel class for serving.

    Parameters
    ----------
    model :
        A trained model, such as an sklearn or torch model
    name : string
        Model name or ID
    ptype_data : pd.DataFrame, np.array
        Sample of data model should expect when it is being served
    versioned :
        Should the model be versioned when created?
    description : str
        A detailed description of the model. If omitted, a brief description will be generated.
    metadata : dict
        Other details to be saved and accessed for serving

    Attributes
    ----------    
    ptype : pydantic.main.BaseModel
        Data prototype
    handler_predict:
        Method to make predictions from a trained model
    
    Notes
    -----
    VetiverModel can also take an initialized custom VetiverHandler
    as a model, for advanced use cases or non-supported model types.
    
    """

    def __init__(
        self,
        model,
        model_name: str,
        ptype_data=None,
        versioned=None,
        description: str = None,
        metadata: dict = None,
        **kwargs
    ):
        translator = create_handler(model, ptype_data)

        self.model = translator.model
        self.ptype = translator.construct_ptype()
        self.model_name = model_name
        self.description = description if description else translator.describe()
        self.versioned = versioned
        self.metadata = translator.create_meta(
            metadata, required_pkgs=["vetiver"]
        )
        self.handler_predict = translator.handler_predict

        
