from typing import Any
from vetiver.handlers import pytorch, scikitlearn
from functools import singledispatch
import sklearn

torch_exists = True
try:
    import torch
except ImportError:
    torch_exists = False

class InvalidModelError(Exception):
    """
    Throw an error if `model` is not
    from scikit-learn or torch
    """

    def __init__(
        self,
        message="The `model` argument must be a scikit-learn or torch model.",
    ):
        self.message = message
        super().__init__(self.message)

CREATE_PTYPE_TPL =  """\
Failed to create a handler from model of \
type {_model_type}. If your model is not one of \
(scikit-learn, torch), you should create and register \
the handler. Here is a template for such a function: \
    from pydantic import create_model
    from vetiver.handlers._interface import create_handler
    from vetiver.handlers.base import VetiverHandler

    class CustomTemplateHandler(VetiverHandler):
        def __init__(model, ptype_data):
            super().__init__(model, ptype_data)
        
        def vetiver_create_meta(
             user: list = None, 
             version: str = None, 
             url: str = None, 
             required_pkgs: list = []):
        \"""
        Create metadata for model. This method should include the required 
        packages necessary to create a prediction.
        \"""
        required_pkgs = required_pkgs + ["name_of_modeling_package"]
        meta = vetiver_meta(user, version, url, required_pkgs)
        
        return meta

        def handler_predict(self, input_data, check_ptype):
            \"""
            handler_predict should define how to make predictions from your model
            \"""
            ...

    @vetiver_create_ptype.register
    def _(model: {_model_type}, ptype_data):
        return CustomTemplateHandler(model, ptype_data)

If your datatype is a common type, please consider submitting \
a pull request.
"""

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
    >>> handler.create_description()
    Scikit-learn <class 'sklearn.dummy.DummyRegressor'> model
    """
    raise InvalidModelError(message=CREATE_PTYPE_TPL.format(_model_type=type(model)))

@create_handler.register
def _(model: sklearn.base.BaseEstimator, ptype_data: Any):
    return scikitlearn.SKLearnHandler(model, ptype_data)

if torch_exists:
    @create_handler.register
    def _(model: torch.nn.Module, ptype_data: Any):
        return pytorch.TorchHandler(model, ptype_data)
