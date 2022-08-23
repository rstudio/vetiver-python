from vetiver.handlers import base
from functools import singledispatch
from contextlib import suppress

from ..ptype import vetiver_create_ptype
from ..meta import _model_meta


class InvalidModelError(Exception):
    """
    Throw an error if `model` is not registered.
    """

    def __init__(
        self,
        message="The `model` argument must be a supported or custom type.",
    ):
        self.message = message
        super().__init__(self.message)


@singledispatch
def create_handler(model, ptype_data):
    """check for model type to handle prediction

    Parameters
    ----------
    model: object
        Description of parameter `x`.
    ptype_data : object
        An object with information (data) whose layout is to be determined.

    Returns
    -------
    handler
        Handler class for specified model type


    Examples
    --------
    >>> import vetiver
    >>> X, y = vetiver.mock.get_mock_data()
    >>> model = vetiver.mock.get_mock_model()
    >>> handler = vetiver.create_handler(model, X)
    >>> handler.describe()
    "Scikit-learn <class 'sklearn.dummy.DummyRegressor'> model"
    """

    raise InvalidModelError(
        "Model must be a supported model type, or a "
        "custom handler must be used. See the docs for more info on custom handlers and"
        "supported types https://rstudio.github.io/vetiver-python/"
    )


# BaseHandler uses create_handler to register subclasses based on model_class


class BaseHandler:
    """Base handler class for creating VetiverModel of different type.

    Parameters
    ----------
    model :
        a trained model
    ptype_data :
        An object with information (data) whose layout is to be determined.
    """

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        with suppress(AttributeError, NameError):
            create_handler.register(cls.model_class(), cls)

    def __init__(self, model, ptype_data):
        self.model = model
        self.ptype_data = ptype_data

    def describe(self):
        """Create description for model"""
        desc = f"{self.model.__class__} model"
        return desc

    def create_meta(
        user: list = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for a model"""
        meta = _model_meta(user, version, url, required_pkgs)

        return meta

    def construct_ptype(self):
        """Create data prototype for a model

        Parameters
        ----------
        ptype_data : pd.DataFrame, np.ndarray, or None
            Training data to create ptype

        Returns
        -------
        ptype : pd.DataFrame or None
            Zero-row DataFrame for storing data types
        """
        ptype = vetiver_create_ptype(self.ptype_data)
        return ptype

    def handler_startup():
        """Include required packages for prediction

        The `handler_startup` function executes when the API starts. Use this
        function for tasks like loading packages.
        """
        ...

    def handler_predict(self, input_data, check_ptype):
        """Generates method for /predict endpoint in VetiverAPI

        The `handler_predict` function executes at each API call. Use this
        function for calling `predict()` and any other tasks that must be executed
        at each API call.

        Parameters
        ----------
        input_data:
            Data used to generate prediction
        check_ptype:
            If type should be checked against `ptype` or not

        Returns
        -------
        prediction
            Prediction from model
        """
        ...


# BaseHandler for subclassing, Handler for new model types
Handler = BaseHandler


@create_handler.register
def _(model: base.BaseHandler, ptype_data):
    if model.ptype_data is None and ptype_data is not None:
        model.ptype_data = ptype_data

    return model
