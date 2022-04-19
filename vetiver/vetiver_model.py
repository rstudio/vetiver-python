from vetiver.handlers._interface import create_translator


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

    Attributes
    ----------
    model :
        A trained model, such as an sklearn or spacy model
    name : string
        Model name or ID
    save_ptype :  bool
        Should an input data prototype be saved with the model? 'TRUE' or 'FALSE'
    ptype_data : pd.DataFrame, np.array
        Sample of data model should expect when it is being served
    versioned :
        Should the model be served when created?
    description : str
        A detailed description of the model. if omitted, a brief description will be generated
    metadata : dict
        Other details to be saved and accessed for serving
    """

    def __init__(
        self,
        model,
        model_name: str,
        save_ptype: bool = True,
        ptype_data=None,
        versioned=None,
        description: str = None,
        metadata: dict = None,
        **kwargs
    ):
        translator = create_translator(model, ptype_data, save_ptype)

        if save_ptype is True:
            if ptype_data is None:
                raise AttributeError

        self.model = model
        self.save_ptype = save_ptype
        self.ptype = translator.ptype()
        self.model_name = model_name
        self.description = description if description else translator.create_description()
        self.versioned = versioned
        self.metadata = translator.vetiver_create_meta(
            metadata, required_pkgs=["vetiver"]
        )
        self.handler_predict = translator.handler_predict

        
