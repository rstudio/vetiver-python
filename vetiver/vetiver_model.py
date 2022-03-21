from .ptype import vetiver_create_ptype
from .handlers._interface import create_translator


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
    """Create VetiverModel class for serving.

    Attributes
    ----------
    model :
        a trained model, such as an sklearn or spacy model
    name : string
        model name or ID
    save_ptype :  bool
        should an input data prototype be saved with the model? 'TRUE' or 'FALSE'
    ptype_data : pd.DataFrame, np.array
        sample of data model should expect when it is being served
    versioned :
        should the model be served when created?
    description : str
        a detailed description of the model. if omitted, a brief description will be generated
    metadata : dict
        other details to be saved and accessed for serving

    Methods
    -------

    """

    def __init__(
        self,
        model,  # takes model and return adapter standin load translator, take model and return translator object
        save_ptype: bool = True,
        ptype_data=None,
        model_name: str = None,
        versioned=None,
        description: str = None,
        metadata=list(),
    ):
        translator = create_translator(model)

        self.model = translator.model
        self.save_ptype = save_ptype
        self.ptype = vetiver_create_ptype(ptype_data, save_ptype)
        self.name = model_name
        self.description = description
        self.metadata = metadata
        self.versioned = versioned
        self.handler_predict = translator.handler_predict

        if not description:
            description = translator.create_description()

    # create description
    def _create_description(self):
        description = f"{self.name} is a {type(self.model)} vetiver model."
        return description
