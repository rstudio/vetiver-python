import json
from warnings import warn
from vetiver.handlers.base import create_handler


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
    model_name : string
        Model name or ID
    prototype_data : pd.DataFrame, np.array
        Sample of data model should expect when it is being served
    versioned :
        Should the model be versioned when created?
    description : str
        A detailed description of the model.
        If omitted, a brief description will be generated.
    metadata : dict
        Other details to be saved and accessed for serving
    **kwargs: dict
        Deprecated parameters.

    Attributes
    ----------
    prototype : vetiver.Prototype
        Data prototype
    handler_predict: Callable
        Method to make predictions from a trained model

    Notes
    -----
    VetiverModel can also take an initialized custom VetiverHandler
    as a model, for advanced use cases or non-supported model types.
    Parameter `ptype_data` was changed to `prototype_data`. Handling of `ptype_data`
    will be removed in a future version.

    Examples
    -------
    >>> from vetiver import mock, VetiverModel
    >>> X, y = mock.get_mock_data()
    >>> model = mock.get_mock_model().fit(X, y)
    >>> v = VetiverModel(model = model, model_name = "my_model", prototype_data = X)
    >>> v.description
    'A scikit-learn DummyRegressor model'
    """

    def __init__(
        self,
        model,
        model_name: str,
        prototype_data=None,
        versioned=None,
        description: str = None,
        metadata: dict = None,
        **kwargs
    ):
        if "ptype_data" in kwargs:
            prototype_data = kwargs.pop("ptype_data")
            warn(
                "argument for saving input data prototype has changed to "
                "prototype_data, from ptype_data",
                DeprecationWarning,
                stacklevel=2,
            )

        translator = create_handler(model, prototype_data)

        self.model = translator.model
        self.prototype = translator.construct_prototype()
        self.model_name = model_name
        self.description = description if description else translator.describe()
        self.versioned = versioned
        self.handler_predict = translator.handler_predict
        self.metadata = translator.create_meta(metadata)

    @classmethod
    def from_pin(cls, board, name: str, version: str = None):
        """
        Create VetiverModel from pinned model.

        Parameters
        ----------
        board :
            `pins` board where model is located
        name : str
            Model name inside pins board
        version : str
            What model version should be loaded
        """
        model = board.pin_read(name, version)
        meta = board.pin_meta(name, version)

        if "vetiver_meta" in meta.user:
            get_prototype = meta.user.get("vetiver_meta").get("prototype", None)
            required_pkgs = meta.user.get("vetiver_meta").get("required_pkgs", None)
            python_version = meta.user.get("vetiver_meta").get("python_version", None)
            meta.user.pop("vetiver_meta")
        # old pin type
        else:
            get_prototype = meta.user.get("ptype")
            required_pkgs = meta.user.get("required_pkgs")
            python_version = meta.user.get("python_version")

        return cls(
            model=model,
            model_name=name,
            description=meta.description,
            metadata={
                "user": meta.user.get("user"),
                "version": meta.version.version,
                "url": meta.local.get("url"),  # None all the time, besides Connect,
                "required_pkgs": required_pkgs,
                "python_version": python_version,
            },
            prototype_data=json.loads(get_prototype) if get_prototype else None,
            versioned=True,
        )
